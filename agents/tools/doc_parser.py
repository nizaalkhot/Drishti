"""
Google ADK Document AI Tool for Case Evidence Forensics.
"""
from typing import Dict, Any
from google.adk.tools import FunctionTool
from backend.integrations.document_ai import default_document_ai, ForensicDocumentAnalysis

def analyze_case_document(document_text_or_base64: str) -> str:
    """
    Analyzes an uploaded suspect legal notice, police summons, or KYC notice
    using Google Cloud Document AI to detect signs of forgery or coercion.
    """
    content_bytes = document_text_or_base64.encode("utf-8")
    analysis: ForensicDocumentAnalysis = default_document_ai.analyze_document(content_bytes)
    
    indicators = "; ".join(analysis.forgery_indicators) if analysis.forgery_indicators else "No overt forgery detected."
    return (
        f"Document Type: {analysis.detected_document_type} | "
        f"Claimed Authority: {analysis.issuing_authority_claimed or 'None'} | "
        f"Forgery Suspected: {analysis.is_forgery_suspected} (Confidence: {analysis.confidence_score:.2f}) | "
        f"Forensic Indicators: {indicators}"
    )

document_ai_tool = FunctionTool(analyze_case_document)
