import spacy
from redactor import redact_addresses

nlp = spacy.load('en_core_web_lg')

def test_redact_addresses():
    text = "I live in New York."
    doc = nlp(text)
    stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}
    redacted = redact_addresses(text, doc, stats)
    
    assert redacted == "I live in ████████."
    assert stats['addresses'] == 1
    assert stats['entities'][0] == ('New York', 10, 18, 'GPE')
