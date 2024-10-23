import spacy
from redactor import redact_dates

nlp = spacy.load('en_core_web_lg')

def test_redact_dates():
    text = "The event is scheduled on 5th October 2023."
    doc = nlp(text)
    stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}
    redacted = redact_dates(text, doc, stats)
    
    assert redacted == "The event is scheduled on ████████████████."
    assert stats['dates'] == 1
    assert stats['entities'][0] == ('5th October 2023', 26, 42, 'DATE')
