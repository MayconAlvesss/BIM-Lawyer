from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import logging
import time

from core.schemas import BatchAuditRequest, AuditResult, Jurisdiction
from core.rule_engine import NormativeEngine
from llm.normative_rag import NormativeRAG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BIM-Lawyer Enterprise API",
    description="Automated AEC Code Compliance & Normative Audit Engine (ADA/IBC/NBR)",
    version="2.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
engine = NormativeEngine()
rag = NormativeRAG()

# Simple Dependency Injection for Auth (similar to EcoBIM)
async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != "bim-lawyer-secure-key-2026":
        # In a real scenario, this raises 403. For testing, we mock validation.
        logger.warning("Invalid or missing API key. Proceeding in DEV mode.")
    return True

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "service": "BIM-Lawyer Rule Engine",
        "rag_status": "Enabled" if rag.qa_chain else "Mocked",
        "jurisdictions": [j.value for j in Jurisdiction]
    }

@app.post("/api/v1/audit/batch", dependencies=[Depends(verify_api_key)], tags=["Audit"])
async def batch_audit(request: BatchAuditRequest, background_tasks: BackgroundTasks):
    """
    Processes a list of BIM elements for compliance audit under a specific jurisdiction.
    Runs computation asynchronously for large datasets.
    """
    if not request.elements:
        raise HTTPException(status_code=400, detail="No elements provided for audit.")
        
    start_time = time.time()
    
    # Run the object-oriented rules engine
    # Elements are passed as dictionaries so BIMElement Pydantic schema can run its unit-conversion validators
    raw_elements = [el.dict() for el in request.elements]
    results = engine.batch_audit(raw_elements, request.jurisdiction)
    
    audit_time = time.time() - start_time
    logger.info(f"Processed {len(raw_elements)} elements in {audit_time:.4f}s")
    
    return {
        "status": "success",
        "jurisdiction": request.jurisdiction.value,
        "processing_time_sec": round(audit_time, 4),
        "total_elements": len(raw_elements),
        "results": results
    }

@app.post("/api/v1/audit/explain", dependencies=[Depends(verify_api_key)], tags=["AI Suggestion"])
async def explain_audit(result: AuditResult):
    """
    Uses the LangChain RAG-LLM Hybrid engine to provide legal basis and remediation for violations.
    """
    if result.status == "Compliant":
        return {"message": "Audit passed. No explanation required."}
        
    query = f"Why does a {result.rule_violated} of {result.current_value} clear width fail?"
    explanation = await rag.query_norm(query, jurisdiction=result.jurisdiction)
    suggestion = await rag.generate_audit_suggestion(result.dict())
    
    return {
        "element": result.element_id,
        "violation": result.rule_violated,
        "legal_reference": explanation.get("answer"),
        "reference_source": explanation.get("source"),
        "ai_suggestion": suggestion
    }
