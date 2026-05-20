# Dockerfile
# Production image for the RAG Assistant app
# ─────────────────────────────────────────────────────────────────────────────

# Use official Python slim image — smaller than full Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# ── Install system dependencies ───────────────────────────────────────────────
# gcc and g++ needed to compile some Python packages (chromadb, sentence-transformers)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first — Docker caches this layer if requirements don't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application code ─────────────────────────────────────────────────────
COPY ingest.py .
COPY retriever.py .
COPY rag_chain.py .
COPY app.py .
COPY data/ ./data/
COPY static/ ./static/

# ── Environment variables (overridable at runtime) ────────────────────────────
ENV CHROMA_DB_PATH=./chroma_db
ENV OLLAMA_BASE_URL=http://ollama:11434

# ── Expose the FastAPI port ───────────────────────────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# ── Start the FastAPI app ─────────────────────────────────────────────────────
# --host 0.0.0.0 makes it accessible outside the container
# --workers 1 keeps it simple (RAG chain is stateful, 1 worker is safe)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
