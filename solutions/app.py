# app.py
# RAG Service — FastAPI backend + serves Chat UI
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import sys
import os

from rag_chain import build_rag_chain

# ── App Setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="RAG Assistant API",
    description="RAG-powered Q&A service built with LangChain, ChromaDB and Ollama",
    version="1.0.0",
)

# ── Request / Response Models ─────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str

# ── Global RAG chain (loaded once on startup) ─────────────────────────────────
rag_chain = None


@app.on_event("startup")
async def startup_event():
    """Run ingestion and load RAG chain when the app starts."""
    global rag_chain

    # Step 1: Run ingestion if chroma_db doesn't exist yet
    chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    if not os.path.exists(chroma_db_path):
        print("⏳ Vector store not found — running ingestion...")
        result = subprocess.run(
            [sys.executable, "ingest.py"],
            capture_output=True, text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Ingestion failed: {result.stderr}")
            raise RuntimeError("Ingestion failed on startup")
        print("✅ Ingestion complete")
    else:
        print("✅ Vector store found — skipping ingestion")

    # Step 2: Build the RAG chain
    print("⏳ Loading RAG chain...")
    rag_chain = build_rag_chain()
    print("✅ RAG chain ready — app is live!")


# ── API Endpoints ─────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def serve_ui():
    """Serve the Chat UI."""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Check if the app and RAG chain are ready."""
    return {
        "status": "ok" if rag_chain else "loading",
        "rag_chain_ready": rag_chain is not None,
    }


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question — returns a grounded answer from the knowledge base.
    The LLM will say it doesn't know if the answer isn't in the documents.
    """
    if not rag_chain:
        raise HTTPException(status_code=503, detail="RAG chain not ready yet. Try again in a moment.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = rag_chain.invoke(request.question)
        return AnswerResponse(question=request.question, answer=answer)
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Cannot connect to Ollama. Make sure the Ollama service is running."
            )
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


# ── Serve static files ────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Run directly (student mode: python app.py) ────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
