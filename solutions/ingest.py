# solutions/ingest.py — COMPLETE SOLUTION
import os
import shutil

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

os.environ["ANONYMIZED_TELEMETRY"] = "false"

CHROMA_DB_PATH  = "./chroma_db"
DATA_PATH       = "./data"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE      = 500
CHUNK_OVERLAP   = 50


def ingest_documents():
    # Step 1: Load documents
    loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} document(s)")

    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")

    # Step 3: Load embedding model
    print("⏳ Loading embedding model (first run downloads ~90MB)...")
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print("✅ Embedding model ready")

    # Step 4: Store in ChromaDB
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)
        print("🗑️  Cleared existing vector store")

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=CHROMA_DB_PATH,
    )
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DB_PATH}")
    print("🎉 Ingestion complete! You can now run retriever.py")


if __name__ == "__main__":
    ingest_documents()
