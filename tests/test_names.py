import spacy
from redactor import redact_names

nlp = spacy.load('en_core_web_md')

def test_redact_names():
    text = "John went to the store."
    doc = nlp(text)
    stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}
    redacted = redact_names(text, doc, stats)
    
    assert redacted == "████ went to the store."
    assert stats['names'] == 1
    assert stats['entities'][0] == ('John', 0, 4, 'PERSON')
