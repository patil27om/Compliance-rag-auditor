import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Ensure src is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "src"))

from api import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enterprise Compliance RAG Auditor API" in response.json()["message"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "compliance-rag-auditor"}

def test_audit_endpoint_success():
    payload = {
        "query": "What is the fulfillment deadline for Data Subject Access Requests (DSAR)?"
    }
    response = client.post("/audit", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "cited_sections" in data
    assert "confidence_score" in data
    assert "2.1" in data["cited_sections"]

def test_audit_endpoint_invalid_payload():
    # Sending empty or malformed payload
    response = client.post("/audit", json={})
    assert response.status_code == 422  # Unprocessable Entity validation error