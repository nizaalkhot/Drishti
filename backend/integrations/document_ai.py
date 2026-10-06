"""
Google Cloud Document AI Forensic Notice Parser.
Extracts structured text, entities, and detects forgery signals from uploaded
legal summons, police notices, electricity penalty bills, and KYC records.
"""
import os
import re
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("drishti.documentai")

class ForensicDocumentAnalysis(BaseModel):
    is_forgery_suspected: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    detected_document_type: str  # COURT_WARRANT, POLICE_NOTICE, ELECTRICITY_BILL, KYC_RECORD, UNKNOWN
    issuing_authority_claimed: Optional[str] = None
    extracted_entities: Dict[str, str] = Field(default_factory=dict)
    forgery_indicators: List[str] = Field(default_factory=list)
    raw_text_summary: str = ""
    processor_version: str = "v1"

class DocumentAIService:
    """
    Forensic document intelligence using Google Cloud Document AI.
    Analyzes scanned PDFs and images for scam hallmarks in Digital Arrest & KYC fraud.
    """
    SUSPICIOUS_COURT_TERMS = ["supreme court", "high court", "cbi arrest", "cyber cell", "digital arrest", "non-bailable"]
    COERCIVE_DEADLINES = ["2 hours", "immediate transfer", "security bond", "clearance deposit", "trai block"]

    def __init__(self, project_id: Optional[str] = None, location: str = "us"):
        self.project_id = project_id or os.getenv("GCP_PROJECT", "team-gain")
        self.location = location
        self.processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID")
        self._client = None
        self._is_cloud_active = False

        try:
            from google.cloud import documentai_v1 as documentai
            self._client = documentai.DocumentProcessorServiceClient()
            if self.processor_id:
                self._is_cloud_active = True
        except Exception as e:
            logger.info("Document AI initialized in local forensic mode: %s", e)

    def analyze_document(
        self,
        content_bytes: Any,
        mime_type: str = "application/pdf"
    ) -> ForensicDocumentAnalysis:
        """
        Parses document bytes or text via Document AI or forensic rule extractor.
        """
        if isinstance(content_bytes, str):
            content_bytes = content_bytes.encode("utf-8")
        raw_text = ""
        entities = {}

        if self._is_cloud_active and self._client and self.processor_id:
            try:
                from google.cloud import documentai_v1 as documentai
                name = self._client.processor_path(self.project_id, self.location, self.processor_id)
                raw_document = documentai.RawDocument(content=content_bytes, mime_type=mime_type)
                request = documentai.ProcessRequest(name=name, raw_document=raw_document)
                result = self._client.process_document(request=request)
                document = result.document
                raw_text = document.text or ""
                for entity in document.entities:
                    entities[entity.type_] = entity.mention_text
            except Exception as e:
                logger.warning("Cloud Document AI execution failed, falling back to heuristic parsing: %s", e)

        if not raw_text:
            # Decode textual representation if PDF/text stream
            try:
                raw_text = content_bytes.decode("utf-8", errors="ignore")
            except Exception:
                raw_text = "Standard Scanned Document"

        # Forensic Scam Heuristics
        text_lower = raw_text.lower()
        forgery_indicators = []
        is_forgery = False
        claimed_authority = None
        doc_type = "UNKNOWN"

        if "cbi" in text_lower or "central bureau of investigation" in text_lower:
            claimed_authority = "Central Bureau of Investigation (CBI)"
            doc_type = "POLICE_NOTICE"
        elif "supreme court" in text_lower or "high court" in text_lower:
            claimed_authority = "Supreme Court of India"
            doc_type = "COURT_WARRANT"
        elif "electricity" in text_lower or "bill update" in text_lower:
            claimed_authority = "State Electricity Board"
            doc_type = "ELECTRICITY_BILL"

        # Detect forgery hallmarks common in Digital Arrest documents
        if any(term in text_lower for term in self.SUSPICIOUS_COURT_TERMS):
            if "deposit" in text_lower or "transfer" in text_lower or "rbi safe account" in text_lower:
                forgery_indicators.append("Fraudulent judicial demand: Official courts never mandate bank transfers into private escrow accounts.")
                is_forgery = True

        if any(deadline in text_lower for deadline in self.COERCIVE_DEADLINES):
            forgery_indicators.append("Extreme coercive urgency detected: Time-limited threat designed to induce panic.")
            is_forgery = True

        # Check for personal mobile numbers in claimed supreme court/CBI headers
        phones = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}', raw_text)
        if phones and claimed_authority:
            forgery_indicators.append(f"Mismatched contact: Personal mobile {phones[0]} listed as official judicial contact.")
            entities["contact_phone"] = phones[0]
            is_forgery = True

        score = 0.95 if is_forgery else 0.10

        return ForensicDocumentAnalysis(
            is_forgery_suspected=is_forgery,
            confidence_score=score,
            detected_document_type=doc_type,
            issuing_authority_claimed=claimed_authority,
            extracted_entities=entities,
            forgery_indicators=forgery_indicators,
            raw_text_summary=raw_text[:300].strip() if raw_text else "Document parsed.",
            processor_version="docai-fraud-v2"
        )

# Global singleton instance
default_document_ai = DocumentAIService()
