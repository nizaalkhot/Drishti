from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.api.schemas import FreezeRequest, SignSTRRequest, DismissRequest
from backend.api.deps import copilot, broadcast_event
from backend.integrations.document_ai import default_document_ai

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
