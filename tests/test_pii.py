import pytest
from backend.security.pii import PIITokenizer, TokenVault

def test_tokenize_aadhaar():
    tokenizer = PIITokenizer()
    text = "Customer Aadhaar is 5489 1234 5678 and needs verification."
    masked, vault = tokenizer.tokenize(text)
    
    assert "5489 1234 5678" not in masked
    assert "[AADHAAR_" in masked
    restored = tokenizer.detokenize(masked, vault)
    assert restored == text

def test_tokenize_pan():
    tokenizer = PIITokenizer()
    text = "PAN card number ABCDE1234F provided during KYC."
    masked, vault = tokenizer.tokenize(text)
    
    assert "ABCDE1234F" not in masked
    assert "[PAN_" in masked
    restored = tokenizer.detokenize(masked, vault)
    assert restored == text

def test_tokenize_phone_and_vpa():
    tokenizer = PIITokenizer()
    text = "Send money to rajesh.kumar@okaxis or call +91 9876543210 immediately."
    masked, vault = tokenizer.tokenize(text)
    
    assert "rajesh.kumar@okaxis" not in masked
    assert "9876543210" not in masked
    assert "[VPA_" in masked
    assert "[PHONE_" in masked
    
    restored = tokenizer.detokenize(masked, vault)
    assert restored == text

def test_tokenize_account_number():
    tokenizer = PIITokenizer()
    text = "Transfer to beneficiary A/C 987654321012345 IFSC HDFC0001234."
    masked, vault = tokenizer.tokenize(text)
    
    assert "987654321012345" not in masked
    assert "[ACCOUNT_" in masked
    restored = tokenizer.detokenize(masked, vault)
    assert restored == text
