import os
from pathlib import Path
from typing import List, TypedDict
from dotenv import load_dotenv
import chromadb
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# Load environment variables (.env for OPENAI_API_KEY)
load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = ROOT_DIR / "data" / "chroma_db"

# 1. Define Strict Pydantic Output Schema for Compliance Answers
class ComplianceResponse(BaseModel):
    answer: str = Field(description="Direct, professional answer to the compliance query based strictly on retrieved policy context.")
    cited_sections: List[str] = Field(description="Exact section numbers cited, e.g., ['1.1', '1.3']")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0 based on context relevance.")

# 2. Define LangGraph State
class AgentState(TypedDict):
    query: str
    retrieved_docs: List[dict]
    response: dict

def retrieve_node(state: AgentState):
    """Retrieves top-k relevant policy chunks from ChromaDB."""
    query = state["query"]
    
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(name="compliance_policies")
    
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    retrieved_docs = []
    if results and results["documents"]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            retrieved_docs.append({
                "content": doc,
                "section_number": meta["section_number"],
                "section_title": meta["section_title"],
                "title": meta["title"]
            })
            
    return {"retrieved_docs": retrieved_docs}

def generate_node(state: AgentState):
    """Generates a structured compliance response with strict citation guardrails."""
    query = state["query"]
    docs = state["retrieved_docs"]
    
    context_str = "\n\n".join([f"[{d['title']} - Section {d['section_number']}: {d['section_title']}]\n{d['content']}" for d in docs])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert enterprise compliance auditor and Forward Deployed Engineer. "
                   "Answer the query using ONLY the provided regulatory context. "
                   "You must cite the exact section numbers used in your justification. "
                   "If the answer cannot be found in the context, state that explicitly."),
        ("human", "Context:\n{context}\n\nQuery: {query}")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    structured_llm = llm.with_structured_output(ComplianceResponse)
    
    chain = prompt | structured_llm
    result = chain.invoke({"context": context_str, "query": query})
    
    return {"response": result.model_dump()}

def run_compliance_rag(query: str):
    """Executes the two-step retrieval and generation graph."""
    from langgraph.graph import StateGraph, END
    
    workflow = StateGraph(AgentState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    app = workflow.compile()
    
    initial_state = {"query": query, "retrieved_docs": [], "response": {}}
    final_state = app.invoke(initial_state)
    return final_state["response"]

if __name__ == "__main__":
    # Test query
    test_query = "What is the review timeframe for transaction monitoring alerts exceeding $10,000?"
    print(f"Query: {test_query}\n")
    
    # Make sure OPENAI_API_KEY is set in environment or .env file
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable is not set. Please add it to your .env file.")
    else:
        res = run_compliance_rag(test_query)
        print("Generated Compliance Response:")
        print(res)