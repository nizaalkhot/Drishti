from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response, Depends
from pydantic import BaseModel, Field

from backend.schemas import FreezeRequest, SignSTRRequest, DismissRequest
from backend.security.auth import Role, User, require_roles
from backend.api.deps import copilot, broadcast_event
from backend.integrations.document_ai import default_document_ai
from backend.compliance.finnet_generator import generate_finnet2_xml
from backend.compliance.iso20022 import generate_camt056_recall

class DocumentAnalysisRequest(BaseModel):
    document_text: str = Field(..., description="Document content or OCR text to parse with Document AI")
    mime_type: str = Field("text/plain", description="MIME type of document")
    document_name: Optional[str] = "suspicious_notice.pdf"

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
async def freeze_account(
    case_id: str,
    req: FreezeRequest,
    user: User = Depends(require_roles(Role.COMPLIANCE_OFFICER, Role.ADMIN))
):
    try:
        res = copilot.freeze_account(case_id, reason=req.reason)
        await broadcast_event("ACCOUNT_FROZEN", {"case_id": case_id, "details": res, "authorized_by": user.username})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/cases/{case_id}/export-str")
async def export_str(
    case_id: str,
    req: SignSTRRequest,
    user: User = Depends(require_roles(Role.COMPLIANCE_OFFICER, Role.ADMIN))
):
    try:
        officer = req.officer_name or user.username
        res = copilot.sign_and_export_str(case_id, officer_name=officer)
        await broadcast_event("STR_APPROVED", {"case_id": case_id, "details": res, "signed_by": officer})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/cases/{case_id}/dismiss")
async def dismiss_case(
    case_id: str,
    req: DismissRequest,
    user: User = Depends(require_roles(Role.ANALYST, Role.COMPLIANCE_OFFICER, Role.ADMIN))
):
    try:
        res = copilot.dismiss_false_positive(case_id, notes=req.analyst_notes)
        await broadcast_event("CASE_DISMISSED", {"case_id": case_id, "details": res, "analyst": user.username})
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/cases/{case_id}/analyze-document")
async def analyze_case_document(case_id: str, req: DocumentAnalysisRequest):
    case = copilot.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    try:
        analysis = default_document_ai.analyze_document(req.document_text, mime_type=req.mime_type)
        audit_entry = {
            "action": "DOCUMENT_AI_ANALYSIS",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "document_name": req.document_name,
            "is_forgery_suspected": analysis.is_forgery_suspected,
            "detected_document_type": analysis.detected_document_type,
            "forgery_indicators": analysis.forgery_indicators,
            "extracted_entities": analysis.extracted_entities
        }
        case.audit_history.append(audit_entry)
        copilot._persist_dossier_async(case)
        await broadcast_event("DOCUMENT_ANALYZED", {"case_id": case_id, "analysis": analysis.model_dump()})
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document AI analysis failed: {str(e)}")

@router.get("/api/v1/cases/{case_id}/finnet-xml")
async def export_finnet_xml(case_id: str, officer_name: str = "Authorized AML Principal Officer"):
    case = copilot.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case_dict = case.model_dump() if hasattr(case, "model_dump") else dict(case)
    xml_content = generate_finnet2_xml(case_dict, officer_name=officer_name)
    return Response(content=xml_content, media_type="application/xml")

@router.post("/api/v1/cases/{case_id}/dispatch-recall")
async def dispatch_iso20022_recall(case_id: str):
    case = copilot.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case_dict = case.model_dump() if hasattr(case, "model_dump") else dict(case)
    recall_res = generate_camt056_recall(case_dict)
    await broadcast_event("INTERBANK_RECALL_DISPATCHED", {"case_id": case_id, "recall": recall_res})
    return recall_res
