"""Domain Unit Tests for Authentication, RBAC, and Maker-Checker Enforcement."""
import pytest
from fastapi import HTTPException
from backend.security.auth import (
    Role,
    User,
    create_access_token,
    verify_access_token,
    require_roles,
)

def test_create_and_verify_jwt_token():
    user = User(
        username="officer_kapoor",
        role=Role.COMPLIANCE_OFFICER,
        employee_id="AML-9901",
        email="kapoor@bank.in"
    )
    token = create_access_token(user, expires_in_seconds=3600)
    assert token != ""
    assert len(token.split(".")) == 3

    verified = verify_access_token(token)
    assert verified is not None
    assert verified.username == "officer_kapoor"
    assert verified.role == Role.COMPLIANCE_OFFICER
    assert verified.employee_id == "AML-9901"

def test_expired_token_rejected():
    user = User(username="analyst_test", role=Role.ANALYST, employee_id="EMP-01")
    expired_token = create_access_token(user, expires_in_seconds=-10)
    assert verify_access_token(expired_token) is None

@pytest.mark.asyncio
async def test_maker_checker_compliance_enforcement():
    checker_dependency = require_roles(Role.COMPLIANCE_OFFICER, Role.ADMIN)

    # Compliance officer allowed
    officer = User(username="checker_officer", role=Role.COMPLIANCE_OFFICER, employee_id="EMP-02")
    res = await checker_dependency(officer)
    assert res.role == Role.COMPLIANCE_OFFICER

    # Analyst (Maker) blocked from executing Checker actions
    analyst = User(username="maker_analyst", role=Role.ANALYST, employee_id="EMP-03")
    with pytest.raises(HTTPException) as exc:
        await checker_dependency(analyst)
    assert exc.value.status_code == 403
    assert "Regulatory Maker-Checker policy requires" in exc.value.detail
