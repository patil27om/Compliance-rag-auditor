import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "src"))

from rag_pipeline import run_compliance_rag

app = FastAPI(title="Enterprise Compliance RAG Auditor API", version="1.0")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Enterprise Compliance RAG Auditor API is running. Use /audit for queries or /docs for Swagger UI."}

@app.post("/audit")
def audit_endpoint(payload: QueryRequest):
    try:
        result = run_compliance_rag(payload.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "compliance-rag-auditor"}