# Python Coding Instructions for GitHub Copilot

## Python Version
Target **Python 3.11+**. You may use f-strings, `match` statements, and modern
type hints. Do not use deprecated Python 2 patterns.

## Code Style
- Follow **PEP 8** — 4-space indentation, snake_case for variables and functions
- Maximum line length: **100 characters**
- Use **f-strings** for all string formatting (not `.format()` or `%`)
- Add a **blank line between logical sections** inside functions
- Keep functions **short and focused** — one function does one thing

## Type Hints
Always add type hints to function signatures:
```python
# ✅ Correct
def search(query: str, k: int = 3) -> list:
def format_docs(docs: list) -> str:
def build_rag_chain():  # return type optional if complex

# ❌ Avoid
def search(query, k):
```

## Comments and Docstrings
- Add a **one-line docstring** to every function explaining its purpose
- Use **inline comments** to explain non-obvious LangChain behaviour
- Use the **section divider style** already established in the starter files:
```python
# ── Step 1: Load documents ────────────────────────────────────────────────────
```

## Constants
- Define all configuration values as **UPPER_CASE constants** at the top of the file
- Never hardcode paths, model names, or sizes inside functions
```python
# ✅ Correct
CHUNK_SIZE = 500
splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE)

# ❌ Avoid
splitter = RecursiveCharacterTextSplitter(chunk_size=500)
```

## Print Statements for Student Feedback
This is a learning project — students need to see progress. Always add print
statements at key steps using this emoji convention:
```python
print("⏳ Loading embedding model...")   # something is happening, wait
print("✅ Loaded 3 documents")           # step completed successfully
print("❌ Could not connect to Ollama")  # error occurred
print("🎉 Pipeline complete!")           # major milestone
print("🔍 Searching vector store...")    # search/retrieval happening
print("💬 Answer: ...")                  # LLM response
```

## Error Handling Patterns

### Ollama connection errors
```python
try:
    answer = chain.invoke(question)
except Exception as e:
    if "connection" in str(e).lower() or "refused" in str(e).lower():
        print("❌ Cannot connect to Ollama. Make sure 'ollama serve' is running.")
    else:
        print(f"❌ Error: {e}")
```

### ChromaDB re-ingestion
```python
import os, shutil
if os.path.exists(CHROMA_DB_PATH):
    shutil.rmtree(CHROMA_DB_PATH)
    print("🗑️  Cleared existing vector store")
```

### Missing chroma_db folder
```python
if not os.path.exists(CHROMA_DB_PATH):
    print("❌ Vector store not found. Run ingest.py first!")
    return
```

## LangChain-Specific Patterns

### Always use `as_retriever()` — not raw `similarity_search()` in chains
```python
# ✅ Correct — works with LCEL chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ❌ Avoid inside chains
results = vectorstore.similarity_search(query, k=3)
```

### format_docs helper — always include this when building chains
```python
def format_docs(docs: list) -> str:
    """Concatenate retrieved document chunks into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)
```

### Similarity search with scores — use this in retriever.py for debugging
```python
# Returns list of (Document, float) tuples — score is distance (lower = more similar)
results = vectorstore.similarity_search_with_score(query, k=3)
for doc, score in results:
    print(f"Score: {score:.4f} | Content: {doc.page_content[:100]}")
```

### OllamaLLM — always set temperature=0 for RAG (deterministic, factual)
```python
llm = OllamaLLM(model=LLM_MODEL, temperature=0)
```

### PromptTemplate — always use from_template()
```python
prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
```

## What NOT to Suggest
- `asyncio`, `async def`, `await` — keep everything synchronous
- `os.environ` or `dotenv` for API keys — no API keys needed in this project
- `pip install openai` or any cloud SDK
- `LLMChain`, `RetrievalQA`, or any legacy LangChain v0.1 patterns
- `vectorstore.persist()` — not needed in ChromaDB 0.4+, it auto-persists
- Jupyter notebook syntax (`display()`, `%%time`) — this is a `.py` project

## Beginner-Friendly Code Principles
Students are software engineers but new to AI/ML. Copilot suggestions should:
- **Prefer clarity over cleverness** — avoid one-liners that are hard to read
- **Avoid list comprehensions inside list comprehensions** — break into steps
- **Name variables descriptively** — `embedding_model` not `em`, `vectorstore` not `vs`
- **Add a comment before every LangChain class instantiation** explaining what it does
