from redactor import redact_phoneNumbers

def test_redact_phones():
    text = "My phone number is 123-456-7890."
    stats = {"names": 0, "dates": 0, "addresses": 0, "phones": 0, "entities": []}
    redacted = redact_phoneNumbers(text, stats)
    
    assert redacted == "My phone number is ████████████."
    assert stats['phones'] == 1
    assert stats['entities'][0] == ('123-456-7890', 19, 31, 'PHONE')
