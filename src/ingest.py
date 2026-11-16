import os
import re
from pathlib import Path
import pymupdf  # Updated from fitz
import chromadb

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DOCS_DIR = ROOT_DIR / "raw_docs"
DB_DIR = ROOT_DIR / "data" / "chroma_db"

def parse_pdf_to_chunks(pdf_path):
    doc = pymupdf.open(pdf_path)
    filename = Path(pdf_path).name
    doc_id = filename.replace(".pdf", "")
    
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
        
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    title = lines[0] if lines else filename
    
    matches = list(re.finditer(r"Section\s+(\d+\.\d+):\s+([^\n]+)", full_text))
    
    chunks = []
    for i, match in enumerate(matches):
        sec_num = match.group(1)
        sec_title = match.group(2).strip()
        
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(full_text)
        
        content = full_text[start_idx:end_idx].strip()
        content = " ".join(content.split())
        
        chunk_id = f"{doc_id}_sec_{sec_num.replace('.', '_')}"
        
        chunks.append({
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "title": title,
            "section_number": sec_num,
            "section_title": sec_title,
            "content": f"Document: {title}\nSection {sec_num}: {sec_title}\n{content}"
        })
        
    return chunks

def ingest_docs():
    if not RAW_DOCS_DIR.exists():
        print(f"Directory '{RAW_DOCS_DIR}' not found. Run generate_docs.py first.")
        return

    DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(name="compliance_policies")
    
    all_chunks = []
    for file in RAW_DOCS_DIR.glob("*.pdf"):
        chunks = parse_pdf_to_chunks(file)
        all_chunks.extend(chunks)
        print(f"Parsed {file.name}: {len(chunks)} sections extracted.")
            
    if not all_chunks:
        print("No PDF documents found to ingest.")
        return

    ids = [c["chunk_id"] for c in all_chunks]
    documents = [c["content"] for c in all_chunks]
    metadatas = [{
        "doc_id": c["doc_id"],
        "title": c["title"],
        "section_number": c["section_number"],
        "section_title": c["section_title"]
    } for c in all_chunks]
    
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Successfully ingested {len(all_chunks)} chunks into ChromaDB at '{DB_DIR}'.")

if __name__ == "__main__":
    ingest_docs()