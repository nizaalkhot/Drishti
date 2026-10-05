import re
from typing import Dict, Tuple

class TokenVault:
    def __init__(self):
        self.token_to_val: Dict[str, str] = {}
        self.val_to_token: Dict[str, str] = {}
        self.counters: Dict[str, int] = {}

    def get_or_create(self, val: str, prefix: str) -> str:
        if val in self.val_to_token:
            return self.val_to_token[val]
        count = self.counters.get(prefix, 0) + 1
        self.counters[prefix] = count
        token = f"[{prefix}_{count}]"
        self.val_to_token[val] = token
        self.token_to_val[token] = val
        return token

    def restore(self, token: str) -> str:
        return self.token_to_val.get(token, token)


class PIITokenizer:
    # Regex patterns for Indian financial PII
    AADHAAR_REGEX = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
    PAN_REGEX = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b')
    VPA_REGEX = re.compile(r'\b[a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+\b')
    PHONE_REGEX = re.compile(r'(?:\+91[\-\s]?)?[6-9]\d{9}\b')
    ACCOUNT_REGEX = re.compile(r'\b\d{11,18}\b')

    def tokenize(self, text: str) -> Tuple[str, TokenVault]:
        vault = TokenVault()
        result = text

        # 1. Aadhaar
        def replace_aadhaar(match):
            val = match.group(0)
            return vault.get_or_create(val, "AADHAAR")
        result = self.AADHAAR_REGEX.sub(replace_aadhaar, result)

        # 2. PAN
        def replace_pan(match):
            val = match.group(0)
            return vault.get_or_create(val, "PAN")
        result = self.PAN_REGEX.sub(replace_pan, result)

        # 3. UPI VPA
        def replace_vpa(match):
            val = match.group(0)
            return vault.get_or_create(val, "VPA")
        result = self.VPA_REGEX.sub(replace_vpa, result)

        # 4. Phone
        def replace_phone(match):
            val = match.group(0)
            return vault.get_or_create(val, "PHONE")
        result = self.PHONE_REGEX.sub(replace_phone, result)

        # 5. Account Number
        def replace_acc(match):
            val = match.group(0)
            return vault.get_or_create(val, "ACCOUNT")
        result = self.ACCOUNT_REGEX.sub(replace_acc, result)

        return result, vault

    def detokenize(self, masked_text: str, vault: TokenVault) -> str:
        res = masked_text
        for token, original in vault.token_to_val.items():
            res = res.replace(token, original)
        return res
