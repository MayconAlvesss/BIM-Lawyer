from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from core.schemas import BatchAuditRequest, AuditResult, Jurisdiction
from core.rule_engine import NormativeEngine
from llm.normative_rag import NormativeRAG

app = FastAPI(
    title="BIM-Lawyer API",
    description="Automated AEC Code Compliance & Normative Audit Engine",
    version="1.0.0"
)

# Initialize engines
engine = NormativeEngine()
# Note: RAG requires API Keys/Settings, keeping as placeholder for logic parity
rag = NormativeRAG() 

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "BIM-Lawyer Normative Backend",
        "jurisdictions": ["ADA", "NBR9050", "IBC"],
        "version": "1.0.0"
    }

@app.post("/audit/batch")
async def batch_audit(request: BatchAuditRequest):
    """
    Processes a list of BIM elements for compliance audit under a specific jurisdiction.
    """
    if not request.elements:
        raise HTTPException(status_code=400, detail="No elements provided for audit.")
        
    results = engine.batch_audit([el.dict() for el in request.elements], request.jurisdiction)
    return results

@app.post("/audit/explain")
async def explain_audit(result: AuditResult):
    """
    Uses the RAG-LLM Hybrid engine to provide legal basis and remediation for violations.
    """
    if result.status == "Compliant":
        return {"message": "Audit passed. No explanation required."}
        
    explanation = await rag.query_norm(f"Why does a {result.rule_violated} of {result.current_value} fail in {result.jurisdiction}?")
    suggestion = await rag.generate_audit_suggestion(result.dict())
    
    return {
        "violation": result.rule_violated,
        "legal_reference": explanation.get("answer", "Reference not found in context."),
        "ai_suggestion": suggestion
    }
