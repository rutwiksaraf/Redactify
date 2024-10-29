import argparse
import glob
import spacy
import en_core_web_md
import re
import os
import sys
from spacy.matcher import PhraseMatcher

nlp = en_core_web_md.load()

# Reading input files:
def readingInput(file_type):
    files = glob.glob(file_type)
    content = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content[file] = f.read()
    return content

# Extracting Named Entities:
def redact_names(text, doc, stats):
    redacted_text = list(text)  # Use a list to keep track of positions easily.
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            start, end = entity.start_char, entity.end_char
            redacted_text[start:end] = "█" * (end - start)
            stats['names'] += 1
            stats['entities'].append((entity.text, start, end, "PERSON"))
    return ''.join(redacted_text)

from spacy.matcher import Matcher

def redact_dates(text, doc, stats):
    matcher = Matcher(doc.vocab)
    date_patterns = [
        [{"TEXT": {"REGEX": r"(\d{1,2}(st|nd|rd|th)?)"}}, {"LOWER": {"IN": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]}}, {"TEXT": {"REGEX": r"\d{4}"}}],
        [{"LOWER": {"IN": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]}}, {"TEXT": {"REGEX": r"\d{1,2}(st|nd|rd|th)?"}}, {"TEXT": {"REGEX": r"\d{4}"}}],
        [{"TEXT": {"REGEX": r"\d{1,2}/\d{1,2}/\d{4}"}}],
    ]
    
    matcher.add("DATE", date_patterns)
    matches = matcher(doc)
    
    redacted_text = list(text)
    
    # Replace matched dates with redaction blocks
    for match_id, start, end in matches:
        span = doc[start:end]
        redacted_text[span.start_char:span.end_char] = "█" * (span.end_char - span.start_char)
        stats["dates"] += 1
        stats["entities"].append((span.text, span.start_char, span.end_char, "DATE"))

    return ''.join(redacted_text)



def redact_addresses(text, doc, stats):
    redacted_text = list(text)
    for entity in doc.ents:
        if entity.label_ in ["GPE", "LOC", "FAC"]:
            start, end = entity.start_char, entity.end_char
            redacted_text[start:end] = "█" * (end - start)
            stats['addresses'] += 1
            stats['entities'].append((entity.text, start, end, entity.label_))
    return ''.join(redacted_text)

def redact_phoneNumbers(text, stats):
    phone_pattern = r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b'
    censored_text = list(text)
    for match in re.finditer(phone_pattern, text):
        start, end = match.start(), match.end()
        censored_text[start:end] = "█" * (end - start)
        stats['phones'] += 1
        stats['entities'].append((match.group(), start, end, "PHONE"))
    return ''.join(censored_text)

# Keep the formatting of text intact while censoring based on concepts
def redact_concepts(text, doc, concepts, stats):
    redacted_text = list(text)
    matcher = PhraseMatcher(nlp.vocab)

    # Convert the concepts to Spacy patterns
    patterns = [nlp(concept.lower()) for concept in concepts]
    matcher.add("CONCEPTS", None, *patterns)

    # Iterate over sentences and redact those containing the concepts
    for sent in doc.sents:
        matches = matcher(nlp(sent.text.lower()))
        if matches:
            start, end = sent.start_char, sent.end_char
            redacted_text[start:end] = "█" * (end - start)
            stats['entities'].append((sent.text, start, end, "CONCEPT"))
    return ''.join(redacted_text)


def conditional_redact(content, flags, stats, concepts):
    doc = nlp(content)
    redacted_content = content  # Keep the original text.

    if flags["names"]:
        redacted_content = redact_names(redacted_content, doc, stats)

    if flags["dates"]:
        redacted_content = redact_dates(redacted_content, doc, stats)

    if flags["addresses"]:
        redacted_content = redact_addresses(redacted_content, doc, stats)

    if flags["phones"]:
        redacted_content = redact_phoneNumbers(redacted_content, stats)

    if concepts:
        redacted_content = redact_concepts(redacted_content, doc, concepts, stats)

    return redacted_content

def save_redacted(file_name, content, output_dir):
    """Saves the redacted content to a new file in the output directory."""
    output_file = os.path.join(output_dir, f'{os.path.basename(file_name)}.censored')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to handle stats output
def write_stats(file_name, stats, output):
    """Writes the redaction stats to the specified output (file, stderr, or stdout)."""
    stats_output = (
        f"Statistics for file: {file_name}\n"
        f"Censor Statistics:\n"
        f"Total names redacted: {stats['names']}\n"
        f"Total dates redacted: {stats['dates']}\n"
        f"Total addresses redacted: {stats['addresses']}\n"
        f"Total phone numbers redacted: {stats['phones']}\n"
        f"Total concept sentences redacted: {len([e for e in stats['entities'] if e[3] == 'CONCEPT'])}\n"
        f"Detailed censored items (text, start, end, type):\n"
    )

    for entity in stats['entities']:
        stats_output += f"{entity}\n"

    if output == "stderr":
        print(stats_output, file=sys.stderr)
    elif output == "stdout":
        print(stats_output)
    else:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(stats_output)

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Redacting sensitive information from text files.")
    parser.add_argument('--input', type=str, required=True, help="Input file pattern (e.g., '*.txt')")
    parser.add_argument('--names', action='store_true', help="Redact names")
    parser.add_argument('--dates', action='store_true', help="Redact dates")
    parser.add_argument('--addresses', action='store_true', help="Redact addresses")
    parser.add_argument('--phones', action='store_true', help="Redact phone numbers")
    parser.add_argument('--concept', action='append', help="Redact based on a concept (can be repeated)", required=False)
    parser.add_argument('--output', type=str, required=True, help="Directory to store censored files")
    parser.add_argument('--stats', type=str, required=True, help="File or special output (stderr/stdout) to write stats")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Load all input files based on the pattern
    input_files_content = readingInput(args.input)

    flags = {
        "names": args.names,
        "dates": args.dates,
        "addresses": args.addresses,
        "phones": args.phones
    }

    concepts = args.concept if args.concept else []

    # Process each file
    for file_name, content in input_files_content.items():
        stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}

        # Redact content
        redacted_content = conditional_redact(content, flags, stats, concepts)

        # Save redacted file
        save_redacted(file_name, redacted_content, args.output)

        # Write stats
        write_stats(file_name, stats, args.stats)

if __name__ == '__main__':
    main()
