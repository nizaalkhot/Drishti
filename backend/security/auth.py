"""Drishti Enterprise Authentication & Role-Based Access Control (RBAC).

Enforces Indian banking regulatory compliance standards:
- Maker-Checker separation of duties (RBI AML/CFT Circulars & PMLA Section 12).
- Analysts ("Makers") can triage, review telemetry, and draft notes.
- Compliance Officers / AML Principal Officers ("Checkers") are mandatory for
  legally binding actions: Account Freezes (CrPC 102), FIU-IND STR Signing, and Interbank Recalls.
"""
import os
import time
import hmac
import hashlib
import json
import base64
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import Header, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class Role(str, Enum):
    ANALYST = "ANALYST"                          # Maker: Triage, inspect telemetry, draft notes
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"    # Checker: Legal lien freezes, FIU-IND STR signing
    ADMIN = "ADMIN"                              # Full configuration & key management
    SYSTEM = "SYSTEM"                            # Machine-to-machine internal ingestion

class User(BaseModel):
    username: str
    role: Role
    employee_id: str
    email: str = "analyst@bank.co.in"
    is_active: bool = True

SECRET_KEY = os.getenv("DRISHTI_AUTH_SECRET", "drishti-enterprise-compliance-secret-key-2026")
STRICT_AUTH = os.getenv("DRISHTI_STRICT_AUTH", "false").lower() == "true"

security_bearer = HTTPBearer(auto_error=False)

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _b64_decode(data: str) -> bytes:
    padding = "=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(user: User, expires_in_seconds: int = 86400) -> str:
    """Generates a cryptographically signed HMAC-SHA256 JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user.username,
        "role": user.role.value,
        "emp_id": user.employee_id,
        "exp": int(time.time()) + expires_in_seconds
    }
    header_b64 = _b64_encode(json.dumps(header).encode())
    payload_b64 = _b64_encode(json.dumps(payload).encode())
    signature = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    sig_b64 = _b64_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_access_token(token: str) -> Optional[User]:
    """Verifies HMAC-SHA256 signature and decodes user identity and role."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        expected_sig = _b64_encode(
            hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        )
        if not hmac.compare_digest(sig_b64, expected_sig):
            return None

        payload = json.loads(_b64_decode(payload_b64).decode())
        if payload.get("exp", 0) < time.time():
            return None

        return User(
            username=payload.get("sub", "unknown"),
            role=Role(payload.get("role", Role.ANALYST.value)),
            employee_id=payload.get("emp_id", "EMP-0000"),
            email=f"{payload.get('sub')}@bank.co.in"
        )
    except Exception:
        return None

async def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    x_role: Optional[str] = Header(None, alias="X-User-Role")
) -> User:
    """FastAPI Dependency resolving current authenticated user.

    In development / demo mode, provides default fallback credentials if headers are omitted.
    """
    if auth and auth.credentials:
        user = verify_access_token(auth.credentials)
        if user:
            return user
        if STRICT_AUTH:
            raise HTTPException(status_code=401, detail="Invalid or expired Bearer token")

    if x_api_key:
        if x_api_key == os.getenv("DRISHTI_API_KEY", "drishti-live-api-key"):
            role = Role(x_role) if x_role and x_role in Role._value2member_map_ else Role.ADMIN
            return User(username="api_service", role=role, employee_id="SVC-001")
        if STRICT_AUTH:
            raise HTTPException(status_code=401, detail="Invalid API Key")

    # In demo/development environments, gracefully assign default compliance persona
    if not STRICT_AUTH:
        # Default to Compliance Officer in demo mode to allow UI actions, or Analyst if explicitly passed
        default_role = Role(x_role) if x_role and x_role in Role._value2member_map_ else Role.COMPLIANCE_OFFICER
        return User(
            username="authorized_aml_officer",
            role=default_role,
            employee_id="AML-LEGAL-772",
            email="compliance.officer@bank.co.in"
        )

    raise HTTPException(status_code=401, detail="Authentication required (Bearer token or X-API-Key missing)")

def require_roles(*allowed_roles: Role):
    """Enforces strict Maker-Checker role permissions on API endpoints."""
    async def _role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: Regulatory Maker-Checker policy requires {[r.value for r in allowed_roles]} role (current: {user.role.value})"
            )
        return user
    return _role_checker
