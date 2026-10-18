"""Drishti Security Layer - Cryptographic Informed Consent Vault, PII Masking, and RBAC Auth."""
from backend.security.consent_vault import InformedConsentVault, ConsentRequest, ConsentReceipt, default_consent_vault
from backend.security.pii import TokenVault, PIITokenizer
from backend.security.auth import (
    Role,
    User,
    get_current_user,
    require_roles,
    create_access_token,
    verify_access_token,
)

__all__ = [
    "InformedConsentVault",
    "ConsentRequest",
    "ConsentReceipt",
    "default_consent_vault",
    "TokenVault",
    "PIITokenizer",
    "Role",
    "User",
    "get_current_user",
    "require_roles",
    "create_access_token",
    "verify_access_token",
]
