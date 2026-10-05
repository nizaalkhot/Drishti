"""Case Dossier and AML Investigation Action Routes."""
from fastapi import APIRouter, HTTPException

from backend.api.schemas import FreezeRequest, SignSTRRequest, DismissRequest
from backend.api.deps import copilot, broadcast_event

router = APIRouter(tags=["Cases & AML Investigation"])

@router.get("/api/v1/cases")
async def list_cases():
    return copilot.list_cases()

@router.get("/api/v1/cases/{case_id}")
async def get_case(case_id: str):
    case = copilot.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/api/v1/cases/{case_id}/freeze")
async def freeze_account(case_id: str, req: FreezeRequest):
    try:
        res = copilot.freeze_account(case_id, reason=req.reason)
        await broadcast_event("ACCOUNT_FROZEN", {"case_id": case_id, "details": res})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/cases/{case_id}/export-str")
async def export_str(case_id: str, req: SignSTRRequest):
    try:
        res = copilot.sign_and_export_str(case_id, officer_name=req.officer_name)
        await broadcast_event("STR_APPROVED", {"case_id": case_id, "details": res})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/cases/{case_id}/dismiss")
async def dismiss_case(case_id: str, req: DismissRequest):
    try:
        res = copilot.dismiss_false_positive(case_id, notes=req.analyst_notes)
        await broadcast_event("CASE_DISMISSED", {"case_id": case_id, "details": res})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
