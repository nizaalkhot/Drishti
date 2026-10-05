"""I4C NCRP / NPCI Consortium Registry Lookup Routes."""
from typing import Optional
from fastapi import APIRouter

from backend.consortium.i4c_registry import default_i4c_registry

router = APIRouter(tags=["Consortium & Threat Intel"])

@router.get("/api/v1/consortium/lookup")
async def lookup_consortium(vpa: str, account: Optional[str] = None, device_id: Optional[str] = None):
    match = default_i4c_registry.lookup(vpa, receiver_account=account, device_id=device_id)
    if not match:
        return {"matched": False, "details": None}
    return {"matched": True, "details": match.model_dump(mode="json")}
