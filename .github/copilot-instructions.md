# GitHub Copilot Instructions

## Project Overview
This is a **RAG (Retrieval-Augmented Generation) learning project** for a half-day
training course. Students are software engineers learning to build RAG pipelines
from scratch using LangChain, ChromaDB, and Ollama — all running locally with no
cloud dependencies.

## Project Goal
Students fill in `TODO` sections in 4 files to build a complete RAG pipeline:
1. `ingest.py` — load documents, split, embed, store in ChromaDB
2. `retriever.py` — query ChromaDB with similarity search
3. `rag_chain.py` — connect retrieval + prompt + Ollama LLM via LangChain LCEL
4. `app.py` — interactive CLI loop

## Tech Stack — Always Use These
| Layer | Tool | Do NOT suggest alternatives |
|-------|------|-----------------------------|
| RAG Framework | LangChain (LCEL style) | Do not suggest LlamaIndex |
| Embeddings | `HuggingFaceEmbeddings` with `sentence-transformers/all-MiniLM-L6-v2` | Do not suggest OpenAI embeddings |
| Vector Store | `Chroma` from `langchain_community.vectorstores` | Do not suggest FAISS or Pinecone |
| LLM | `OllamaLLM` with model `mistral:7b-instruct` | Do not suggest OpenAI or Anthropic LLMs |
| Document Loader | `DirectoryLoader` + `TextLoader` | Fine to suggest PDFLoader for extension tasks |
| Text Splitter | `RecursiveCharacterTextSplitter` | This is the default — always use this unless asked |
| Output Parser | `StrOutputParser` | |

## Key Configuration Constants — Always Use These Values
```python
CHROMA_DB_PATH = "./chroma_db"
DATA_PATH = "./data"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistral:7b-instruct"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
```

## LangChain Patterns — Always Prefer LCEL Style
When building chains, always use LCEL pipe syntax:
```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```
Do NOT suggest legacy `LLMChain` or `RetrievalQA` patterns.

## Imports — Preferred Sources
```python
# Vector store
from langchain_community.vectorstores import Chroma

# Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# LLM
from langchain_ollama import OllamaLLM

# Loaders
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Prompt
from langchain.prompts import PromptTemplate

# Chain building blocks
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
```

## RAG Prompt — Always Ground the LLM
When suggesting prompt templates, always include:
1. An instruction to answer ONLY from the provided context
2. A fallback instruction: say "I don't have enough information" if the answer isn't in the context
3. `{context}` and `{question}` as the two placeholders

Example:
```python
RAG_PROMPT_TEMPLATE = """You are a helpful and precise assistant.
Answer the user's question using ONLY the information provided in the context below.
If the answer cannot be found in the context, respond with:
"I don't have enough information to answer that based on the available documents."
Do not make up information or use your general knowledge.

Context:
{context}

Question: {question}

Answer:"""
```

## Error Handling Expectations
- Always check if `./chroma_db` exists before re-ingesting (use `shutil.rmtree`)
- Wrap Ollama calls in try/except for `ConnectionRefusedError` with a helpful message
- Print clear progress messages with emojis (✅ ⏳ ❌ 🎉) so students know what's happening

## What Copilot Should Help Students Do
- Complete TODO sections with correct LangChain code
- Suggest the right class names and parameters from the stack above
- Follow the existing code style in each file
- Add helpful inline comments explaining what each step does

## What Copilot Should NOT Do
- Suggest OpenAI, Anthropic, or any cloud-based LLM or embedding API
- Suggest API keys or environment variables for LLMs (everything runs locally)
- Rewrite or refactor code outside the TODO sections
- Suggest async patterns — keep everything synchronous for simplicity
- Add unnecessary abstractions — keep code beginner-friendly and readable
