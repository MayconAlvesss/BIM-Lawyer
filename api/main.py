"""
BIM-Lawyer — FastAPI Interface
==============================
Cloud-based Automated Rule Checking (ARC) service.
Exposes normative auditing and legal compliance tools for BIM models.
"""

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from core.rule_engine import RuleEngine
from llm.normative_rag import NormativeRAG

app = FastAPI(
    title="BIM-Lawyer API",
    description="Autonomous Building Code Compliance & Audit Engine",
    version="1.0.0"
)

# Initialize engines
engine = RuleEngine()
rag    = NormativeRAG()

@app.get("/")
async def root():
    return {
        "status": "BIM-Lawyer Audit Engine Online",
        "compliance_standards": ["IBC 2021", "ADA", "ISO 21597"],
        "ai_status": "RAG-LLM Hybrid Ready"
    }

@app.post("/audit/batch")
async def batch_audit(elements: List[Dict[str, Any]]):
    """
    Runs a batch audit session on a list of BIM elements.
    """
    if not elements:
        raise HTTPException(status_code=400, detail="No elements provided for audit.")
        
    results = engine.batch_audit(elements)
    return results

@app.post("/audit/explain")
async def explain_violation(violation: Dict[str, Any]):
    """
    Uses LLM to explain a specific violation and suggest design remedies.
    """
    query = f"Explain building code violation: {violation.get('description')}"
    explanation = await rag.query_norm(query)
    remedy = await rag.generate_audit_suggestion(violation)
    
    return {
        "violation": violation,
        "legal_reference": explanation["answer"],
        "source": explanation["source"],
        "ai_suggestion": remedy
    }
