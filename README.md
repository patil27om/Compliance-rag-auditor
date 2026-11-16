# Compliance RAG Auditor

A production-grade Retrieval-Augmented Generation (RAG) tool and automated drift auditor built for forward-deployed engineering scenarios where regulatory documents shift and compliance answers must be strictly traceable.

## What Problem Does This Solve?
Enterprise RAG systems often fail silently when internal compliance guidelines or regulations change. If a vector database becomes stale, the system can hallucinate or cite outdated policies. This project provides a lightweight pipeline that ingests compliance PDFs, enforces strict section-level citations using structured outputs, and runs continuous regression tests to flag semantic drift before deployment.

## Project Structure
```text
compliance-rag-auditor/
├── data/               # Persistent ChromaDB storage
├── raw_docs/           # Generated compliance policy PDFs
├── src/
│   ├── generate_docs.py # Synthetic policy PDF generator
│   ├── ingest.py       # PDF parser & metadata vector loader
│   ├── rag_pipeline.py # LangGraph RAG agent with strict citations
│   ├── api.py          # FastAPI backend server
│   └── app.py          # Streamlit executive dashboard
├── tests/
│   ├── test_compliance.py # Pytest regression suite for drift detection
│   └── test_api.py     # API endpoint unit tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Tech Stack
- **Orchestration:** LangGraph & LangChain (Python)
- **LLM:** OpenAI (`gpt-4o-mini`) with Pydantic structured outputs
- **Vector Store:** ChromaDB with metadata filtering
- **Backend & UI:** FastAPI & Streamlit
- **Testing:** Pytest regression and drift harness

## Getting Started Locally

### 1. Clone & Setup Environment
```bash
git clone https://github.com/YOUR_USERNAME/compliance-rag-auditor.git
cd compliance-rag-auditor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Generate Docs & Populate Vector Store
```bash
python src/generate_docs.py
python src/ingest.py
```

### 4. Run Tests
```bash
pytest tests/ -v
```

### 5. Launch FastAPI & Streamlit
- **Start FastAPI Backend:**
  ```bash
  uvicorn src.api:app --reload
  ```
- **Start Streamlit Dashboard:**
  ```bash
  streamlit run src/app.py
  ```

## Running with Docker Compose
To run both the API and Streamlit UI containerized:
```bash
docker compose up --build
```
- Swagger Docs: `http://localhost:8000/docs`
- Streamlit UI: `http://localhost:8501`