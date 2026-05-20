# ingest.py
# RAG Course — Exercise 1: Document Ingestion Pipeline
#
# GOAL: Load documents → split into chunks → embed → store in ChromaDB
#
# TIP: Use GitHub Copilot! Write a comment describing what you want,
#      then press Tab to accept the suggestion.
# ─────────────────────────────────────────────────────────────────────────────

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil

# ── Configuration ─────────────────────────────────────────────────────────────
CHROMA_DB_PATH = "./chroma_db"
DATA_PATH = "./data"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def ingest_documents():

    # ── Step 1: Load documents from the data/ folder ──────────────────────────
    # Use DirectoryLoader to load all .txt files from DATA_PATH
    # Hint: DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
    loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    print(f"✅ Loaded {len(documents)} document(s)")

    # ── Step 2: Split documents into chunks ───────────────────────────────────
    # Use RecursiveCharacterTextSplitter with CHUNK_SIZE and CHUNK_OVERLAP
    # Hint: splitter = RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)
    # TODO: Write your code here — create the splitter and call split_documents()



    print(f"✅ Split into {len(chunks)} chunks")

    # ── Step 3: Load the embedding model ──────────────────────────────────────
    # Use HuggingFaceEmbeddings with EMBEDDING_MODEL
    # Note: First run downloads ~90MB — this is normal, wait for it!
    # Hint: embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    # TODO: Write your code here

    print("⏳ Loading embedding model (first run downloads ~90MB)...")

    print("✅ Embedding model ready")

    # ── Step 4: Store chunks in ChromaDB ──────────────────────────────────────
    # First clear any existing DB to avoid duplicates, then create a new one
    # Hint: Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=CHROMA_DB_PATH)
    # TODO: Clear existing chroma_db folder if it exists (use shutil.rmtree)

    # TODO: Create the ChromaDB vector store from chunks



    print(f"✅ Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DB_PATH}")
    print("🎉 Ingestion complete! You can now run retriever.py")


if __name__ == "__main__":
    ingest_documents()
