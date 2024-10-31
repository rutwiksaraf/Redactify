import spacy
from redactor import redact_concepts

nlp = spacy.load('en_core_web_lg')

def test_redact_concepts():
    text = "Artificial intelligence is evolving rapidly."
    doc = nlp(text)
    stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}
    concepts = ["Artificial intelligence"]
    redacted = redact_concepts(text, doc, concepts, stats)
    
    assert redacted == "████████████████████████████████████████████"
    assert len([e for e in stats['entities'] if e[3] == 'CONCEPT']) == 1
