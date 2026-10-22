# AI Software Engineering Copilot for Large Codebases

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3_Flash-4285F4.svg)](https://aistudio.google.com/)
[![Groq](https://img.shields.io/badge/Groq-LPU_Inference-F55036.svg)](https://console.groq.com/)
[![Tree-sitter](https://img.shields.io/badge/Tree--sitter-AST-orange.svg)](https://tree-sitter.github.io/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Store-blueviolet.svg)](https://github.com/facebookresearch/faiss)
[![Ollama](https://img.shields.io/badge/Ollama-Offline_Local-black.svg)](https://ollama.ai)

An enterprise-grade, **Repository-Aware RAG Intelligent Developer Assistant** that understands entire software codebases using multi-language Abstract Syntax Tree (AST) parsing, call and dependency graph analysis, context-enriched breadcrumb chunking, hybrid retrieval (FAISS + BM25), and sub-second multi-model reasoning powered by **Google Gemini**, **Groq Cloud**, **xAI Grok**, and **Local Ollama**.

---

## 🌟 Key Features

1. **Ultra-Fast Sub-Second Inference (< 1s Streaming)**
   - **Multi-Model Routing:** Seamlessly switch between **Google Gemini 3 Flash**, **Groq LPU (GPT-OSS)**, **xAI Grok**, or **Local Ollama (Qwen2.5-Coder)**.
   - **Real-Time Streaming Metrics:** Live tokens/second calculation (`~150–350 tok/s`), live generation timer, and immediate **Stop** generation button.

2. **Batched Cloud Embeddings (Instant Codebase Indexing)**
   - High-speed batched embedding via Google Cloud (`gemini-embedding-001` with exact 768-dim FAISS alignment).
   - Reduces repository cloning and indexing time from **several minutes down to ~2–5 seconds**.
   - Automatic local fallback to Ollama (`nomic-embed-text`) when offline.

3. **Multi-Language AST Analysis (Tree-sitter)**
   - Extracts classes, methods, functions, docstrings, type annotations, decorators, line ranges, imports, and cross-function calls.
   - Built-in support for **Python, TypeScript, JavaScript, Java, C++, C, Go, and Rust**.

4. **Context-Enriched Breadcrumb Chunking**
   - Eliminates out-of-context code snippets by attaching hierarchical scope headers (`# File: ... # Class Scope: ... # Decorators: ... # Imports: ...`) to every chunk before embedding.

5. **Hybrid Code Retrieval & Reciprocal Rank Fusion (RRF)**
   - **Dense Semantic Retrieval:** 768-dimensional FAISS vector similarity search.
   - **Lexical Keyword Retrieval:** Custom BM25 Okapi code search engine with camelCase and snake_case identifier tokenization.
   - **Exact Symbol Boost:** Automatically matches query symbols to exact AST entity definitions.
   - **RRF Ranking:** Blends dense, sparse, and symbol results into a unified, high-precision rank list.

6. **Program Graph & Change Impact Analysis**
   - **Dependency Graph:** NetworkX-powered file import graph detecting circular dependencies and calculating PageRank architecture hubs.
   - **Call Graph:** Inter-function caller/callee resolution.
   - **Blast Radius Impact Analysis:** Predicts affected downstream modules, callers, risk level (LOW $\rightarrow$ CRITICAL), and recommends test files before making changes.

7. **Dual Reasoning Modes**
   - **⚡ Direct RAG Streaming:** Ultra-fast sub-second answers grounded strictly in retrieved code with exact citations (`file:start-end`).
   - **🧠 Autonomous ReAct Agent:** Multi-step autonomous agent that executes tools (`search_code`, `get_symbol_callers`, `get_dependencies`, `read_file`, `get_impact`) to solve complex architectural questions.

8. **Modern Dark-Mode Web Interface**
   - Built-in **Model & API Keys Configuration Modal** with live connection speed & latency testing.
   - 1-click **Quick Prompt Chips** (Project Overview, Architecture, DB & Models, Find Bugs).
   - Multi-chat isolation with repository switching, syntax highlighting, and 1-click code copying.

---

## 🏗️ Architecture

```
                       ┌──────────────────────┐
                       │      Developer       │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │  Web UI / CLI / API  │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │     FastAPI Core     │
                       └──────────┬───────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
 │ Query Analysis │      │ Program Graphs │      │ Hybrid Search  │
 │   & Routing    │      │ (Deps / Calls) │      │  (FAISS+BM25)  │
 └────────┬───────┘      └────────┬───────┘      └────────┬───────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │ Context Builder │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Unified LLM   │
                         │     Router      │
                         └────────┬────────┘
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
 │ Google Gemini  │      │   Groq Cloud   │      │  Local Ollama  │
 │ 3 Flash (Free) │      │  LPU Inference │      │  (Offline)     │
 └────────┬───────┘      └────────┬───────┘      └────────┬───────┘
          └───────────────────────┼───────────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │ Grounded Answer │
                         │ with Citations  │
                         └─────────────────┘
```

---

## 🚀 Quickstart

### 1. Install Python Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Environment (Optional but Recommended)
Copy the example environment file:
```bash
cp .env.example .env
```
Paste your free API keys into `.env` (or configure them directly in the Web UI):
```env
# Google AI Studio free key (https://aistudio.google.com/apikey):
GEMINI_API_KEY=your_gemini_key_here

# Groq Cloud free key (https://console.groq.com/keys):
GROQ_API_KEY=your_groq_key_here
```

> **Note:** If you prefer running 100% locally and offline, start [Ollama](https://ollama.ai) with:
> `ollama pull qwen2.5-coder:7b` and `ollama pull nomic-embed-text:latest`.

### 3. Launch the Copilot Web UI
```bash
python run.py
```
Open your browser at **`http://localhost:8000`**.

### 4. Index a Repository
- **From the Web UI:** Click **"+ New Chat"** $\rightarrow$ select **"GitHub Link"** or **"Local Path"** to clone and index automatically.
- **Or via CLI:**
  ```bash
  # Index a local directory:
  python scripts/index_repository.py

  # Or clone & index any public GitHub repo:
  python scripts/index_repository.py "https://github.com/pallets/flask"
  ```

---

## 💻 CLI Commands

### Direct Terminal Question Answering
```bash
python scripts/query_copilot.py "Where is the Tree-sitter parser initialized?"
```

### Retrieval Evaluation Benchmark
Run the automated benchmark measuring Hit Rate@K and Mean Reciprocal Rank (MRR):
```bash
python scripts/evaluate_copilot.py
```

### Run Automated Unit & API Tests
```bash
python -m pytest -v
```

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/chat/stream` | Stream RAG response tokens via Server-Sent Events (SSE) |
| `POST` | `/api/chat` | Synchronous grounded RAG query |
| `POST` | `/api/agent/run` | Execute autonomous multi-step ReAct reasoning |
| `GET` | `/api/settings` | Get active provider, configured key status, and model catalog |
| `POST` | `/api/settings` | Update runtime API keys, default provider, and model |
| `POST` | `/api/settings/test` | Test live inference connectivity and measure latency (ms) |
| `POST` | `/api/repository/clone` | Shallow-clone (`--depth 1`) and index any GitHub repo |
| `POST` | `/api/repository/index` | Parse AST, chunk, and index a local repository path |
| `GET` | `/api/repository/list` | List all indexed repositories on disk |
| `GET` | `/api/repository/status` | Get current indexed repository statistics |
| `POST` | `/api/search` | Execute hybrid search (FAISS + BM25 + Symbol definition) |
| `GET` | `/api/analysis/dependencies` | Get dependency graph nodes, edges, and PageRank hubs |
| `POST` | `/api/analysis/impact` | Calculate change blast radius and affected callers |

---

## 📚 Project Documentation

Additional design specifications, research papers, and implementation reports are available in the [`docs/`](docs/) directory:

- [Project Implementation Document](docs/PROJECT_IMPLEMENTATION_DOCUMENT.md)
- [Project Review Report](docs/PROJECT_REVIEW_REPORT.md)
- [Comprehensive Architecture & Structure](docs/AI_Software_Engineering_Copilot_Project_Structure.md)
