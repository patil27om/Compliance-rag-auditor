import pytest
from pathlib import Path
import sys

# Ensure src is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "src"))

from rag_pipeline import run_compliance_rag

# Define a "golden dataset" of compliance audit test cases
GOLDEN_TEST_CASES = [
    {
        "query": "What is the review timeframe for transaction monitoring alerts exceeding $10,000?",
        "expected_section": "1.1",
        "required_keywords": ["48 business hours", "transaction monitoring"]
    },
    {
        "query": "What are the record retention requirements for AML and CIP records?",
        "expected_section": "1.3",
        "required_keywords": ["5 years", "immutable"]
    },
    {
        "query": "What is the fulfillment deadline for Data Subject Access Requests (DSAR)?",
        "expected_section": "2.1",
        "required_keywords": ["30 calendar days"]
    },
    {
        "query": "What encryption standard is required for cross-border PII transfers?",
        "expected_section": "2.2",
        "required_keywords": ["AES-256"]
    }
]

@pytest.mark.parametrize("test_case", GOLDEN_TEST_CASES)
def test_compliance_rag_accuracy(test_case):
    """
    Evaluates RAG pipeline responses against golden compliance test cases 
    to guard against semantic drift and hallucination.
    """
    query = test_case["query"]
    result = run_compliance_rag(query)
    
    answer = result.get("answer", "").lower()
    cited_sections = result.get("cited_sections", [])
    confidence = result.get("confidence_score", 0.0)
    
    # Assertions for enterprise compliance guardrails
    assert test_case["expected_section"] in cited_sections, \
        f"Drift Detected! Expected section {test_case['expected_section']} not cited for query: '{query}'. Cited: {cited_sections}"
    
    assert confidence >= 0.8, \
        f"Low Confidence Warning: Score {confidence} is below the 0.8 threshold."
    
    for keyword in test_case["required_keywords"]:
        assert keyword.lower() in answer, \
            f"Hallucination/Drift Check Failed: Required keyword '{keyword}' missing from answer: '{answer}'"

def test_out_of_domain_query():
    """Tests how the RAG pipeline handles queries outside compliance scope."""
    query = "What is the best recipe for chocolate chip cookies?"
    result = run_compliance_rag(query)
    
    # Should either have low confidence or fail to cite valid regulatory sections
    cited_sections = result.get("cited_sections", [])
    assert len(cited_sections) == 0 or result.get("confidence_score", 1.0) < 0.5, \
        "Security Risk: RAG hallucinated compliance citations for an out-of-domain query."