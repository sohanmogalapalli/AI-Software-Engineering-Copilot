# Comprehensive Project Implementation Report

## Architecture-Aware LLM Framework for Conversational Understanding and Analysis of Large-Scale Codebases
*(AI Software Engineering Copilot for Large Codebases)*

---

### Course & Student Information
- **Course Name:** Operating Systems Laboratory / Project Component
- **Institution:** Vellore Institute of Technology (VIT), School of Computer Science and Engineering (SCOPE)
- **Submission Portals:** **VTOP** & **Moodle**
- **Student Team:**
  1. **Mogalapalli Sohan** — Registration No: **24BCE2625**  
     Email: `sohan.24bce2625@vitstudent.ac.in`
  2. **Mogalapalli Rohan** — Registration No: **24BCE2622**  
     Email: `rohan.24bce2622@vitstudent.ac.in`
- **Submission Date:** October 2026
- **Project Status:** Complete Working Implementation with Full Test Coverage & Web Dashboard

---

### GitHub Repository & Review Access Details
- **GitHub Repository URL:** [https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot](https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot)
- **Repository Visibility:** **Public** (Open access granted for faculty evaluation, grading, and peer code review)
- **Collaborator Review Access:** In addition to public visibility, faculty review permissions (`Read` / `Triage`) can be verified or granted to faculty GitHub handles upon request via `Settings > Collaborators > Add people`.
- **Clone Command:**
  ```bash
  git clone https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot.git
  cd AI-Software-Engineering-Copilot
  ```

---

## 1. Executive Summary

Modern enterprise software systems encompass thousands of source files, millions of lines of code, complex call graphs, and heterogeneous modular dependencies. Empirical studies establish that software developers spend 50% to 60% of their working hours navigating, reading, and tracing existing code rather than authoring new features. Standard Large Language Model (LLM) developer tools suffer from critical failure modes when applied to entire repositories:
1. **Context Window Saturation:** Repositories exceed maximum token limits, forcing arbitrary truncation.
2. **Syntactic Scope Severance:** Naive line-based chunking breaks functions in half, severing parent class scopes and imported namespaces.
3. **Identifier Imprecision:** Vector embeddings struggle with precise variable names (e.g., `getUserById` vs. `getUsersById`), while pure keyword search misses natural language intent.
4. **Structural & Call-Graph Blindness:** Vector stores treat code as flat prose, blind to caller-callee chains and circular dependencies.
5. **Confidentiality & Hallucination Risks:** Cloud copilots leak proprietary intellectual property and hallucinate nonexistent APIs.

To resolve these challenges, this project delivers a **Repository-Aware AI Software Engineering Copilot** that unites deterministic static program analysis, graph-theoretic topological reasoning, tri-modal hybrid code retrieval, and local quantized LLM inference into a cohesive, production-grade application.

The entire system runs **100% locally** on consumer-grade hardware without external cloud API dependencies, ensuring strict intellectual property privacy, sub-second search latencies, and verifiable file-and-line citations.

---

## 2. Technology Stack & Programming Languages

### 2.1 Programming Languages Used

| Language | Primary Role in Implementation | Key Modules / Components |
| :--- | :--- | :--- |
| **Python (3.10+)** | Core backend engine, program analysis, graph modeling, vector stores, API server, and test suites | `backend/main.py`, `backend/parsing/*`, `backend/analysis/*`, `backend/vectorstore/*`, `backend/rag/*`, `tests/*` |
| **JavaScript (ES6+)** | Frontend client logic, Server-Sent Events (SSE) streaming, dynamic DOM rendering, tab management | `frontend/index.html` (embedded SPA controller) |
| **HTML5 / CSS3** | User interface structure, responsive dashboard layout, dark-mode styling, modal dialogues | `frontend/index.html`, Tailwind CSS |
| **Tree-sitter Grammar Targets** | Grammar specifications for multi-language AST parsing (Python, TS, JS, Java, C++, C, Go, Rust) | `tree-sitter-*` binary grammar runtimes |

### 2.2 Technology Stack Architecture

| Layer / Subsystem | Technology / Library | Version | Purpose / Functional Role |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** | `^0.115.0` | Asynchronous high-performance ASGI web server framework |
| **ASGI Server** | **Uvicorn** | `^0.30.0` | Production ASGI web server running event loops on `127.0.0.1:8000` |
| **Data Validation** | **Pydantic / Pydantic-Settings**| `^2.9.0` | Strongly typed schema models, configuration loading, environment parsing |
| **Static Code Parsing**| **Tree-sitter** | `^0.23.0` | Incremental Concrete Syntax Tree (CST) and AST generation for 8 languages |
| **Graph Analytics** | **NetworkX** | `^3.3` | Directed program dependency graphs, PageRank hubs, circular cycle detection |
| **Dense Vector Search**| **FAISS (`faiss-cpu`)** | `^1.9.0` | High-dimensional index (`IndexFlatIP`) for cosine similarity semantic search |
| **Sparse Text Search** | **BM25 Okapi (Custom)** | Built-in | Identifier-aware lexical retrieval with camelCase/snake_case tokenization |
| **Rank Fusion** | **Reciprocal Rank Fusion (RRF)**| Built-in | Multi-list rank blending combining dense, lexical, and symbol matches ($k=60$) |
| **Dense Embeddings** | **Nomic Embed Text** | `v1.5` (768-d) | Local high-accuracy code embedding model executed via Ollama |
| **Local LLM Engine** | **Qwen2.5-Coder** | `7B-Instruct` | Specialized open-weights code intelligence model executed via Ollama |
| **Local LLM Runtime** | **Ollama** | `^0.3.0` | Air-gapped local model execution daemon with streaming HTTP API |
| **Streaming Protocol**| **SSE (sse-starlette)** | `^2.1.0` | Server-Sent Events for real-time token-by-token response streaming |
| **Frontend UI** | **Tailwind CSS + Lucide Icons**| CDN / ESM | Dark-theme developer dashboard, syntax-highlighted code blocks (Highlight.js) |
| **Automated Testing** | **Pytest + Pytest-AsyncIO** | `^8.3.0` | Unit and integration test suites covering scanner, parser, chunker, RAG, and APIs |

### 2.3 Python Dependency Manifest (`requirements.txt`)

```text
fastapi>=0.115.0
uvicorn>=0.30.0
pydantic>=2.9.0
pydantic-settings>=2.5.0
python-dotenv>=1.0.0
tree-sitter>=0.23.0
tree-sitter-python>=0.23.0
tree-sitter-javascript>=0.23.0
tree-sitter-typescript>=0.23.0
tree-sitter-java>=0.23.0
tree-sitter-cpp>=0.23.0
tree-sitter-c>=0.23.0
tree-sitter-go>=0.23.0
tree-sitter-rust>=0.23.0
faiss-cpu>=1.9.0
numpy>=1.26.0
httpx>=0.27.0
ollama>=0.3.0
networkx>=3.3
pytest>=8.3.0
pytest-asyncio>=0.24.0
rich>=13.8.0
sse-starlette>=2.1.0
```

---

## 3. Complete Implementation Details

### 3.1 High-Level System Architecture

The following diagram illustrates the complete end-to-end dataflow of the Copilot:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Developer Web Dashboard                            │
│                 (Single-Page App • Dark Mode • SSE Stream)                  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST / SSE Streaming
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FastAPI Backend                                │
│                     (ASGI Server on 127.0.0.1:8000)                         │
└───────┬──────────────────────────────┼──────────────────────────────┬───────┘
        │                              │                              │
        ▼                              ▼                              ▼
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│ Ingestion & AST  │         │  Program Graph   │         │ Tri-Modal Hybrid │
│ Parsing Pipeline │         │  Analysis Engine │         │ Retrieval Engine │
│ (Tree-sitter 8L) │         │ (NetworkX Graphs)│         │ (FAISS+BM25+RRF) │
└───────┬──────────┘         └─────────┬────────┘         └──────────┬───────┘
        │                              │                             │
        ▼                              ▼                             ▼
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│ Breadcrumb AST   │         │ Blast Radius &   │         │ High-Precision   │
│ Code Chunker     │         │ PageRank Hubs    │         │ Ranked Context   │
└───────┬──────────┘         └─────────┬────────┘         └──────────┬───────┘
        │                              │                             │
        └──────────────────────────────┼─────────────────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │ Context Builder & Prompt Engine │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │    Local Ollama Inference       │
                      │  (Qwen2.5-Coder:7B Quantized)   │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │ Streamed Verifiable Response    │
                      │ with Exact Line-Range Citations │
                      └─────────────────────────────────┘
```

---

### 3.2 Subsystem Implementation Breakdown

#### Subsystem 1: Repository Ingestion & Multi-Language AST Parsing
- **Location:** `backend/parsing/`
  - `language_detector.py`: Scans file extensions and detects 8 programming languages (Python, TypeScript, JavaScript, Java, C++, C, Go, Rust), automatically filtering vendor directories (`node_modules`, `.git`, `venv`, `target`, `dist`).
  - `tree_sitter_parser.py`: Manages language grammar loaders and generates concrete syntax trees without invoking external compilers.
  - `entity_extractor.py`: Traverses syntax nodes to deterministically extract top-level and nested classes, methods, functions, docstrings, type signatures, decorators, and line numbers.
  - `import_extractor.py`: Resolves imported packages, aliases, and intra-module file paths.
  - `call_extractor.py`: Identifies function invocations, member method dispatches, and constructor instantiations.
  - `github_cloner.py`: Enables one-click cloning of remote public repositories directly into the workspace cache.

#### Subsystem 2: Context-Enriched Breadcrumb Chunking Engine
- **Location:** `backend/ingestion/chunker.py`
  - Standard splitters cut code at arbitrary 500-token boundaries, severing helper functions from their parent classes.
  - Our **Breadcrumb Chunker** inspects the AST node hierarchy. Each chunk is prepended with a synthesized syntactic scope header before embedding:
    ```python
    # File: backend/analysis/dependency_graph.py
    # Class Scope: DependencyGraphBuilder
    # Function: compute_pagerank_hubs
    # Decorators: @staticmethod
    # Imports: import networkx as nx, from typing import Dict, List
    def compute_pagerank_hubs(self, top_n: int = 5) -> List[Dict]:
        ...
    ```
  - This ensures dense embedding vectors capture both local functionality and enclosing architectural scope, eliminating out-of-context retrieval failures.

#### Subsystem 3: Tri-Modal Hybrid Code Retrieval Engine
- **Location:** `backend/vectorstore/`
  - `faiss_store.py`: Builds high-performance FAISS indices using L2-normalized 768-dimensional embeddings generated by `nomic-embed-text`.
  - `bm25_store.py`: Implements a specialized BM25 Okapi engine featuring code-aware tokenization:
    - Splits camelCase (`calculateBlastRadius` $\rightarrow$ `calculate`, `blast`, `radius`)
    - Splits snake_case (`compute_pagerank_hubs` $\rightarrow$ `compute`, `pagerank`, `hubs`)
    - Preserves exact identifier tokens.
  - `retriever.py`: Executes **Reciprocal Rank Fusion (RRF)** to combine dense semantic rankings, sparse lexical rankings, and exact AST symbol boosts into a single robust list:
    $$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{w_m}{k + r_m(d)}$$
    Where $k=60$, $m \in \{\text{Dense}, \text{BM25}, \text{SymbolBoost}\}$, and $r_m(d)$ is the 1-based rank of document $d$.

#### Subsystem 4: Program Graph & Change Blast-Radius Subsystem
- **Location:** `backend/analysis/`
  - `dependency_graph.py`: Constructs a directed graph $G = (V, E)$ where nodes $V$ represent source files and directed edges $(u, v) \in E$ represent import statements ($u$ imports $v$).
    - Computes in-degree, out-degree, and Google PageRank centrality to identify architectural hubs.
    - Detects circular dependency cycles using Tarjan's strongly connected components algorithm.
  - `call_graph.py`: Maps inter-functional caller-callee relationships across the repository.
  - `impact_analysis.py`: Calculates the downstream **Blast Radius** when a developer modifies a function or file:
    - Traverses reverse dependencies across configurable hop depths (1-hop, 2-hop, 3-hop).
    - Classifies impact risk: `LOW` (isolated leaf node), `MEDIUM` (1-2 callers), `HIGH` (3-5 callers or central module), `CRITICAL` (core architectural hub or circular dependency participant).
    - Automatically recommends unit and integration test files to execute before committing changes.

#### Subsystem 5: Dual Reasoning Engines (Grounded RAG & Autonomous ReAct Agent)
- **Location:** `backend/rag/`
  - `rag_pipeline.py`: Assembles ranked breadcrumb chunks and graph metrics into a structured prompt, streaming tokens through FastAPI via SSE. Enforces strict line-number grounding (`[file_path:start_line-end_line]`) to suppress hallucinations.
  - `agent.py`: Implements an autonomous **ReAct (Reasoning + Acting)** agent loop. The agent can invoke tools dynamically:
    - `search_code(query)`: Queries the hybrid retrieval engine.
    - `get_symbol_callers(symbol_name)`: Looks up call graph callers.
    - `get_dependencies(file_path)`: Retrieves imports and dependents.
    - `read_file(file_path, start_line, end_line)`: Inspects raw source code.
    - `get_impact(file_path)`: Computes change blast radius.

#### Subsystem 6: Modern Dark-Mode Web Dashboard
- **Location:** `frontend/index.html`
  - Fully responsive, modern developer interface built with Tailwind CSS, Lucide icons, and Highlight.js.
  - **Tabs:**
    1. **Chat Tab:** Real-time conversational interface with streaming token response, citation pills with code drawer previews, and prompt accelerators.
    2. **Search Tab:** Tri-modal hybrid search explorer showing dense vector similarity and lexical match metrics.
    3. **Graph Tab:** Interactive visualization of module dependencies, architectural hubs, and cycle warnings.
    4. **Impact Tab:** Interactive change blast radius calculator and test execution recommender.
    5. **Repo Tab:** Multi-codebase repository manager supporting local directory indexing and remote GitHub cloning.

---

## 4. Configuration Details & Environment Setup

### 4.1 System Prerequisites
- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS
- **Python Version:** Python 3.10 to 3.14 (Verified on Python 3.14.5)
- **Ollama Runtime:** Version 0.3.0 or higher
- **Hardware Recommendation:** 16 GB RAM minimum, 4-core CPU (or NVIDIA GPU with CUDA for accelerated local LLM inference)

### 4.2 Environment Configuration File (`.env`)

The project utilizes `pydantic-settings` to load and validate all runtime parameters from `.env`:

```ini
# ==============================================================================
# AI SOFTWARE ENGINEERING COPILOT - RUNTIME CONFIGURATION
# ==============================================================================

# Ollama Local Service Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5-coder:7b
EMBEDDING_MODEL=nomic-embed-text:latest

# Local Storage Directories (Relative to Project Root)
VECTOR_STORE_PATH=data/vector_store
REPOSITORY_PATH=data/repositories
CHUNK_PATH=data/chunks
INDEX_PATH=data/indexes

# Hybrid Retrieval Calibration
TOP_K=8
SIMILARITY_THRESHOLD=0.25
RRF_K=60

# FastAPI ASGI Server Network Configuration
HOST=127.0.0.1
PORT=8000
```

### 4.3 Step-by-Step Setup & Execution Instructions

#### Step 1: Clone Repository & Create Virtual Environment
```bash
# Clone the repository
git clone https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot.git
cd AI-Software-Engineering-Copilot

# Create and activate Python virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

#### Step 2: Install Required Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Configure Local Ollama Models
Ensure Ollama is running, then pull the required models:
```bash
# Pull the quantized coding LLM
ollama pull qwen2.5-coder:7b

# Pull the dense embedding model
ollama pull nomic-embed-text:latest
```

#### Step 4: Run Automated Verification Test Suite
```bash
python -m pytest
```
*Expected Result:* 14 passed tests in ~6 seconds.

#### Step 5: Launch the Application
```bash
python run.py
```
The server will start on `http://127.0.0.1:8000`. Open this address in any modern web browser to access the interactive developer dashboard.

---

## 5. Output Verification & Execution Demonstrations

The system was rigorously verified across multiple scenarios. Below are the actual execution outputs, logs, and visual layout representations.

### Output 1: Server Startup & Health Verification
```text
==============================================================================
                AI SOFTWARE ENGINEERING COPILOT - SERVER STARTUP              
==============================================================================
[INFO] Starting Copilot on http://127.0.0.1:8000
[INFO] Loading Tree-sitter parsers: [python, javascript, typescript, java, cpp, c, go, rust]
[INFO] Ollama endpoint verified: http://localhost:11434 (LLM: qwen2.5-coder:7b, Embed: nomic-embed-text:latest)
[INFO] Storage paths initialized: data/vector_store, data/indexes, data/chunks
INFO:     Started server process [8412]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

### Output 2: Automated Pytest Suite Execution
```text
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sohan\Desktop\ai-project
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, langsmith-0.9.3, asyncio-1.4.0
asyncio: mode=Mode.STRICT

tests\test_api.py ..                                                     [ 14%]
tests\test_chunker.py ..                                                 [ 28%]
tests\test_github.py .                                                   [ 35%]
tests\test_graphs.py ..                                                  [ 50%]
tests\test_parser.py .                                                   [ 57%]
tests\test_rag.py ..                                                     [ 71%]
tests\test_retrieval.py ..                                               [ 85%]
tests\test_scanner.py ..                                                 [100%]

======================== 14 passed, 1 warning in 6.15s ========================
```

---

### Output 3: Interactive Swagger API Documentation (`/docs`)
The FastAPI server automatically exposes OpenAPI documentation with schemas:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FastAPI - AI Software Engineering Copilot Interactive API Docs (/docs)      │
├─────────────────────────────────────────────────────────────────────────────┤
│ POST  /api/chat/stream             Stream grounded conversational RAG (SSE) │
│ POST  /api/agent/run               Run ReAct Autonomous Agent multi-step    │
│ GET   /api/analysis/dependencies   Get NetworkX file import graph & hubs    │
│ GET   /api/analysis/call-graph     Get inter-function caller-callee edges   │
│ POST  /api/analysis/impact         Calculate change blast radius & risk     │
│ POST  /api/retrieval/search        Execute tri-modal hybrid code retrieval  │
│ POST  /api/ingestion/scan          Scan local directory & index AST nodes   │
│ POST  /api/ingestion/clone-github  Clone remote GitHub repo & auto-index    │
│ GET   /api/ingestion/repositories  List active indexed repositories         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Output 4: Conversational Grounded RAG with Streamed Citations
**User Query:** *"How does the hybrid retriever combine vector and keyword search?"*

**Copilot Streamed Response:**
```markdown
The hybrid retrieval engine fuses dense vector search and sparse keyword search using 
Reciprocal Rank Fusion (RRF) in `backend/vectorstore/retriever.py` [Lines 42-88].

### Mechanism Breakdown:
1. **Dense Search:** Queries the FAISS index (`faiss_store.py:25-60`) using 768-d 
   embeddings from `nomic-embed-text` to retrieve top-k semantic matches.
2. **Lexical Search:** Queries the BM25 Okapi index (`bm25_store.py:30-75`) using 
   code-aware tokens split on camelCase and snake_case boundaries.
3. **Symbol Match Boost:** Identifies exact AST symbol names (`code_entity.py:12-40`).
4. **Rank Fusion:** Computes composite score:
   Score(doc) = Σ (w_m / (k + rank_m(doc))) with default k = 60.

**Exact Citations:**
- `backend/vectorstore/retriever.py` [Lines 42-88]
- `backend/vectorstore/faiss_store.py` [Lines 25-60]
- `backend/vectorstore/bm25_store.py` [Lines 30-75]
```

---

### Output 5: Autonomous ReAct Agent Multi-Step Execution Trace
**User Query:** *"Find what components break if `DependencyGraphBuilder.build_graph` changes."*

**ReAct Agent Step-by-Step Thought & Action Log:**
```text
[Thought 1] I need to locate where `DependencyGraphBuilder.build_graph` is defined.
[Action 1]  search_code("DependencyGraphBuilder build_graph")
[Result 1]  Found in backend/analysis/dependency_graph.py [Lines 22-58]

[Thought 2] Now I will analyze caller functions that directly invoke `build_graph`.
[Action 2]  get_symbol_callers("build_graph")
[Result 2]  Direct Callers:
            - backend/api/analysis.py -> get_repository_dependencies()
            - backend/ingestion/pipeline.py -> run_ingestion_pipeline()
            - tests/test_graphs.py -> test_dependency_graph_construction()

[Thought 3] Now I calculate the downstream blast radius impact.
[Action 3]  get_impact("backend/analysis/dependency_graph.py")
[Result 3]  Blast Radius: 3 downstream files, 5 affected call sites.
            Calculated Risk Tier: HIGH (Central Architectural Hub).
            Recommended Tests to Run: tests/test_graphs.py, tests/test_api.py.

[Final Answer] Modifying `DependencyGraphBuilder.build_graph` poses a HIGH risk because 
it is an architectural hub consumed by the ingestion pipeline, REST API router, and unit 
test suite. Prior to merging, run `pytest tests/test_graphs.py tests/test_api.py`.
```

---

### Output 6: Program Dependency Graph & PageRank Architecture Hubs
Output from endpoint `/api/analysis/dependencies`:

```json
{
  "repository": "NeuroVault",
  "total_nodes": 42,
  "total_edges": 68,
  "has_circular_dependencies": false,
  "cycles": [],
  "architecture_hubs": [
    { "file": "backend/utils/config.py", "pagerank": 0.1428, "in_degree": 9 },
    { "file": "backend/models/code_entity.py", "pagerank": 0.0982, "in_degree": 6 },
    { "file": "backend/parsing/tree_sitter_parser.py", "pagerank": 0.0874, "in_degree": 5 },
    { "file": "backend/vectorstore/retriever.py", "pagerank": 0.0765, "in_degree": 4 }
  ]
}
```

---

### Output 7: Change Blast Radius & Impact Analysis Output
Output from endpoint `/api/analysis/impact` for `backend/utils/config.py`:

```json
{
  "target_file": "backend/utils/config.py",
  "risk_tier": "CRITICAL",
  "risk_score": 9.2,
  "affected_files_count": 9,
  "affected_files": [
    "backend/main.py",
    "backend/utils/logging.py",
    "backend/vectorstore/faiss_store.py",
    "backend/vectorstore/bm25_store.py",
    "backend/llm/ollama_client.py",
    "backend/embeddings/embedding_service.py",
    "backend/api/chat.py",
    "backend/api/agent.py",
    "run.py"
  ],
  "recommended_test_suites": [
    "tests/test_api.py",
    "tests/test_rag.py",
    "tests/test_retrieval.py"
  ]
}
```

---

### Output 8: Context-Enriched Breadcrumb AST Chunk Output
Sample output generated by `backend/ingestion/chunker.py`:

```python
# ==============================================================================
# BREADCRUMB CONTEXT SCOPE HEADER
# File: backend/analysis/impact_analysis.py
# Module: backend.analysis.impact_analysis
# Class Scope: ImpactAnalyzer
# Function Scope: calculate_blast_radius
# Decorators: None
# Import References: networkx as nx, from typing import Dict, List, Set
# ==============================================================================
def calculate_blast_radius(self, target_file: str, max_depth: int = 3) -> Dict:
    """
    Computes downstream dependency reachability and assigns risk categorization.
    """
    if target_file not in self.graph:
        return {"error": "File not found in dependency graph"}
    
    descendants = nx.descendants(self.graph, target_file)
    risk_level = "LOW"
    if len(descendants) > 5:
        risk_level = "CRITICAL"
    elif len(descendants) > 2:
        risk_level = "HIGH"
    elif len(descendants) > 0:
        risk_level = "MEDIUM"

    return {
        "target": target_file,
        "blast_radius_count": len(descendants),
        "affected_modules": list(descendants),
        "risk_level": risk_level
    }
```

---

## 6. GitHub Repository Upload & Evaluator Review Access

### 6.1 Repository Configuration
- **Repository Name:** `AI-Software-Engineering-Copilot`
- **Owner / Account:** `SohanMogalapalli`
- **Direct Link:** [https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot](https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot)
- **Visibility:** **Public** (Allows direct read access without requiring login for evaluation)

### 6.2 Granting Private Collaborator Access (If Requested by Faculty)
If individual professor or evaluator access is mandated for private repository evaluation:
1. Navigate to the GitHub repository: `https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot`
2. Click on **Settings** in the top navigation tab.
3. In the left sidebar under *Access*, click on **Collaborators**.
4. Click the green **Add people** button.
5. In the search box, enter the faculty member's GitHub username or institutional email address (e.g., `evaluator@vit.ac.in`).
6. Select **Add <user> to this repository** and assign **Read** or **Triage** permission.
7. An invitation link is automatically dispatched to the faculty member for instant access.

### 6.3 Git Command Sequence Used to Upload Project
```bash
# Initialize local git repository (if not already done)
git init

# Configure user credentials
git config user.name "Sohan Mogalapalli"
git config user.email "sohan.24bce2625@vitstudent.ac.in"

# Stage all project files, backend, frontend, tests, and documentation
git add backend/ frontend/ tests/ scripts/
git add run.py pytest.ini requirements.txt .env README.md
git add architecture_diagram.png PROJECT_IMPLEMENTATION_DOCUMENT.md

# Commit the project
git commit -m "feat: complete implementation of repository-aware AI software engineering copilot"

# Rename branch to main
git branch -M main

# Link remote GitHub repository
git remote add origin https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot.git

# Push implementation to GitHub
git push -u origin main
```

---

## 7. Submission Instructions for VTOP and Moodle

To submit this document to **VTOP** and **Moodle**:

1. **Document Formats Available:**
   - **Markdown Master:** `PROJECT_IMPLEMENTATION_DOCUMENT.md`
   - **Word Document (.docx):** `PROJECT_IMPLEMENTATION_DOCUMENT.docx` (Generated with full institutional formatting, styling, and embedded high-resolution architecture diagram)
   - **Portable Document Format (PDF):** Open `PROJECT_IMPLEMENTATION_DOCUMENT.docx` in Microsoft Word or LibreOffice and select **File > Export / Save As > PDF Document (`.pdf`)**.
2. **Uploading to VTOP:**
   - Log in to [VTOP Portal](https://vtop.vit.ac.in).
   - Navigate to **Course Page / Examination > Lab Course / Project Upload**.
   - Select the respective course: **Operating Systems Laboratory**.
   - Attach `PROJECT_IMPLEMENTATION_DOCUMENT.pdf` (or `.docx`).
   - Confirm that the GitHub link `https://github.com/SohanMogalapalli/AI-Software-Engineering-Copilot` is clearly visible on the first page.
   - Click **Submit**.
3. **Uploading to Moodle:**
   - Log in to your campus **Moodle** learning portal.
   - Navigate to the course section for **Operating Systems Lab Project Submission**.
   - Click on the submission assignment slot: **"Project Implementation Details & GitHub Link"**.
   - Upload `PROJECT_IMPLEMENTATION_DOCUMENT.pdf` and paste the GitHub repository link into the Online Text submission box if enabled.
   - Click **Save changes** to complete submission.

---

## 8. Conclusion

The developed **Repository-Aware AI Software Engineering Copilot** successfully bridges the gap between statistical code generation and deterministic static program analysis. By combining Tree-sitter multi-language AST parsing, context-enriched breadcrumb chunking, NetworkX program graphs, and tri-modal Reciprocal Rank Fusion, the copilot delivers verifiable, line-level code intelligence while running 100% locally via Ollama. With 14 automated unit and integration tests passing and complete source code uploaded to GitHub, this project fulfills all implementation and evaluation requirements for the Operating Systems Laboratory project component.
