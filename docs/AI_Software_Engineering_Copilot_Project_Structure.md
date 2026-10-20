# AI Software Engineering Copilot for Large Codebases

## Repository-Aware RAG-Based Intelligent Developer Assistant

**Project Type:** Artificial Intelligence / Software Engineering\
**Primary Goal:** Build an AI-powered developer assistant that
understands an entire software repository and provides
repository-grounded answers for code explanation, debugging, code
search, dependency analysis, and change-impact analysis.

------------------------------------------------------------------------

# 1. Project Overview

Modern software repositories can contain thousands of files, classes,
functions, APIs, configurations, tests, and dependencies. A conventional
chatbot cannot reliably answer questions about such repositories because
it does not inherently understand the repository's structure or
relationships.

This project develops a **Repository-Aware AI Software Engineering
Copilot** that combines:

-   Repository parsing
-   Abstract Syntax Tree (AST) analysis
-   Code entity extraction
-   Dependency and call-relationship analysis
-   Hybrid code search
-   Semantic embeddings
-   Vector databases
-   Retrieval-Augmented Generation (RAG)
-   Local Large Language Models (LLMs)
-   Repository-grounded reasoning

The system first converts a repository into a structured representation.
It then retrieves the most relevant code and contextual information for
a developer's question and provides an answer grounded in the actual
repository.

------------------------------------------------------------------------

# 2. Project Name

## AI Software Engineering Copilot for Large Codebases

### Full Technical Name

**Repository-Aware RAG-Based Intelligent Developer Assistant**

### Short Description

An intelligent developer assistant that understands large codebases
using program analysis, semantic search, dependency relationships, and
Retrieval-Augmented Generation.

------------------------------------------------------------------------

# 3. Problem Statement

Developers working with large codebases frequently face problems such
as:

-   Finding where a particular feature is implemented
-   Understanding unfamiliar functions or classes
-   Tracing function calls across multiple files
-   Understanding module dependencies
-   Debugging repository-specific problems
-   Determining which files may be affected by a code change
-   Searching for code using natural language
-   Understanding how different components interact
-   Maintaining knowledge of large and continuously changing
    repositories

Traditional keyword-based search is insufficient for many of these
tasks.

A generic LLM also has limitations because:

1.  It may not have access to the repository.
2.  It may hallucinate functions or files.
3.  It may miss relationships between files.
4.  Large repositories cannot fit entirely into an LLM context window.
5.  It cannot reliably determine repository-specific dependencies
    without analysis.

Therefore, this project introduces a system that combines **static code
analysis + repository indexing + semantic retrieval + RAG + LLM
reasoning**.

------------------------------------------------------------------------

# 4. Objectives

## Primary Objectives

1.  Parse software repositories automatically.
2.  Identify source files and supported programming languages.
3.  Extract classes, functions, methods, imports, and function calls.
4.  Build a structured repository index.
5.  Split source code into meaningful code chunks.
6.  Generate semantic embeddings for code and documentation.
7.  Store embeddings in a vector database.
8.  Support semantic and hybrid code search.
9.  Retrieve repository-specific context for user queries.
10. Generate grounded responses using an LLM.
11. Provide code explanation and debugging assistance.
12. Provide dependency and change-impact analysis.

## Secondary Objectives

-   Support large repositories.
-   Reduce LLM hallucinations.
-   Preserve relationships between code entities.
-   Provide explainable retrieval.
-   Support local/private LLM execution.
-   Create a modular architecture that can be extended to additional
    languages.

------------------------------------------------------------------------

# 5. Core Features

## 5.1 Repository Discovery

The system scans a repository and identifies relevant source files.

It filters:

-   Source files
-   Configuration files
-   Documentation
-   Tests

and ignores unnecessary directories such as:

-   `.git`
-   virtual environments
-   build directories
-   cache directories
-   generated files
-   dependency directories

------------------------------------------------------------------------

## 5.2 Language Detection

The system determines the programming language of each source file.

The current implementation focuses on **Python repository analysis**.

The architecture can later be extended to:

-   C
-   C++
-   Java
-   JavaScript
-   TypeScript
-   Go
-   Rust
-   C#
-   Kotlin

------------------------------------------------------------------------

## 5.3 AST-Based Parsing

Tree-sitter is used to parse source code.

The parser provides structural information rather than treating source
code as plain text.

Example:

``` text
Repository
 └── backend
      └── main.py
           ├── import
           ├── class
           │    └── method
           └── function
```

------------------------------------------------------------------------

## 5.4 Code Entity Extraction

The system extracts entities such as:

-   Classes
-   Functions
-   Methods
-   Imports
-   Function calls
-   Source locations
-   Line ranges

Example:

``` python
class UserService:

    def get_user(self, user_id):
        return repository.find(user_id)
```

The system can represent this as:

``` text
Class:
    UserService

Method:
    get_user

Call:
    repository.find
```

------------------------------------------------------------------------

# 6. Repository Index

The repository index is the central structural representation of the
codebase.

It contains information about:

``` text
Repository
 ├── Files
 │    ├── Imports
 │    ├── Classes
 │    ├── Functions
 │    └── Calls
 │
 └── Relationships
      ├── File → File
      ├── Class → Method
      ├── Function → Function
      └── Symbol → Symbol
```

The index allows the system to understand not only individual code
snippets but also their relationships.

------------------------------------------------------------------------

# 7. High-Level Architecture

``` text
                         ┌──────────────────────┐
                         │       Developer      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    User Interface    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ Query Analysis │ │ Repository     │ │ Code Search    │
        │                │ │ Understanding  │ │                │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                │                  ▼                  │
                │        ┌──────────────────┐         │
                │        │ Tree-sitter      │         │
                │        │ Parser           │         │
                │        └────────┬─────────┘         │
                │                 │                   │
                │                 ▼                   │
                │        ┌──────────────────┐         │
                │        │ Repository Index │         │
                │        └────────┬─────────┘         │
                │                 │                   │
                └─────────────────┼───────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Code Chunking    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Embedding Model  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Vector Database  │
                         │      FAISS       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Hybrid Retrieval │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ RAG Context      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Local LLM        │
                         │ Ollama           │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Grounded Answer  │
                         └──────────────────┘
```

------------------------------------------------------------------------

# 8. Proposed Project Structure

``` text
ai-software-engineering-copilot/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   ├── search.py
│   │   ├── chat.py
│   │   └── analysis.py
│   │
│   ├── parsing/
│   │   ├── __init__.py
│   │   ├── repository_scanner.py
│   │   ├── language_detector.py
│   │   ├── tree_sitter_parser.py
│   │   ├── ast_traversal.py
│   │   ├── entity_extractor.py
│   │   ├── import_extractor.py
│   │   └── call_extractor.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── code_entity.py
│   │   ├── code_file.py
│   │   └── repository_index.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── metadata.py
│   │   └── pipeline.py
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedding_service.py
│   │
│   ├── vectorstore/
│   │   ├── __init__.py
│   │   ├── faiss_store.py
│   │   └── retriever.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── query_analyzer.py
│   │   ├── context_builder.py
│   │   ├── prompt_builder.py
│   │   └── rag_pipeline.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── ollama_client.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── dependency_graph.py
│   │   ├── call_graph.py
│   │   └── impact_analysis.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       ├── logging.py
│       └── file_utils.py
│
├── data/
│   ├── repositories/
│   ├── chunks/
│   ├── vector_store/
│   └── indexes/
│
├── tests/
│   ├── test_parsing.py
│   ├── test_repository_index.py
│   ├── test_ingestion.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   └── test_rag.py
│
├── frontend/
│   └── ...
│
├── scripts/
│   ├── index_repository.py
│   ├── build_embeddings.py
│   └── test_pipeline.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

> Note: The structure above represents the target modular architecture.
> The currently completed implementation is primarily concentrated in
> the repository-understanding/parsing portion. Modules planned for
> later phases can be added incrementally.

------------------------------------------------------------------------

# 9. Directory and Module Responsibilities

## `backend/`

Contains the main backend application.

------------------------------------------------------------------------

## `backend/main.py`

Main FastAPI application entry point.

Responsibilities:

-   Create FastAPI application
-   Register API routes
-   Configure application startup
-   Provide health/status endpoints
-   Connect higher-level services

Example:

``` text
Client
   ↓
FastAPI
   ↓
Services
   ↓
Repository / Retrieval / RAG
```

------------------------------------------------------------------------

# 10. Parsing Layer

Directory:

``` text
backend/parsing/
```

This is one of the most important components of Phase 1.

------------------------------------------------------------------------

## 10.1 Repository Scanner

Responsible for:

-   Traversing repository directories
-   Finding source files
-   Filtering unwanted directories
-   Filtering unsupported files
-   Returning file paths

Example:

``` text
repository/
├── backend/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── .git/

Scanner:
    backend/main.py
    backend/utils.py
    tests/test_main.py
```

`.git/` is ignored.

------------------------------------------------------------------------

## 10.2 Language Detector

Determines language using file extensions and other repository
information.

Example:

``` text
.py      → Python
.java    → Java
.cpp     → C++
.js      → JavaScript
.ts      → TypeScript
```

Current primary implementation:

``` text
Python
```

------------------------------------------------------------------------

## 10.3 Tree-sitter Parser

Tree-sitter converts source code into a syntax tree.

Example:

``` python
def add(a, b):
    return a + b
```

Conceptual AST:

``` text
function_definition
├── name: add
├── parameters
│   ├── a
│   └── b
└── return_statement
    └── binary_expression
```

This structure is used for reliable code extraction.

------------------------------------------------------------------------

## 10.4 AST Traversal

Traverses Tree-sitter nodes recursively.

Responsibilities:

-   Visit nodes
-   Identify relevant node types
-   Extract source ranges
-   Extract names
-   Build structural information

------------------------------------------------------------------------

## 10.5 Entity Extraction

Extracts:

-   Classes
-   Functions
-   Methods
-   Variables where useful
-   Source locations
-   Line numbers

Example:

``` text
CodeEntity
    name
    entity_type
    file_path
    start_line
    end_line
    source
```

------------------------------------------------------------------------

## 10.6 Import Extraction

Extracts relationships created by imports.

Example:

``` python
from backend.utils import helper
```

Stored conceptually as:

``` text
backend/main.py
       |
       └── imports → backend/utils.py
```

This becomes useful for dependency analysis.

------------------------------------------------------------------------

## 10.7 Call Extraction

Extracts function and method calls.

Example:

``` python
result = helper()
```

Relationship:

``` text
main_function
      |
      └── calls → helper
```

This is important for future call-graph and impact analysis.

------------------------------------------------------------------------

# 11. Data Models

## 11.1 CodeEntity

Represents a logical code element.

Example fields:

``` text
CodeEntity
├── name
├── type
├── file_path
├── start_line
├── end_line
├── source
└── metadata
```

Possible entity types:

``` text
class
function
method
```

------------------------------------------------------------------------

## 11.2 CodeFile

Represents one source file.

Conceptually:

``` text
CodeFile
├── path
├── language
├── source
├── imports
├── entities
└── calls
```

------------------------------------------------------------------------

## 11.3 RepositoryIndex

Represents the complete indexed repository.

Conceptually:

``` text
RepositoryIndex
├── repository_path
├── files
├── entities
├── imports
└── relationships
```

------------------------------------------------------------------------

# 12. Repository Indexing Pipeline

The current Phase 1 pipeline follows:

``` text
Repository
      ↓
File Discovery
      ↓
Language Detection
      ↓
Source Loading
      ↓
Tree-sitter Parsing
      ↓
AST Traversal
      ↓
Entity Extraction
      ↓
Import Extraction
      ↓
Call Extraction
      ↓
CodeFile Creation
      ↓
RepositoryIndex Creation
```

This is the foundation for all later AI functionality.

------------------------------------------------------------------------

# 13. Ingestion Pipeline

After repository understanding, the system converts code into
retrieval-friendly chunks.

``` text
Repository Index
       ↓
Code Entities
       ↓
Chunk Generation
       ↓
Metadata Attachment
       ↓
Embedding Generation
       ↓
Vector Storage
```

------------------------------------------------------------------------

# 14. Code Chunking

The project should avoid blindly splitting code every N characters.

Instead, chunks should preferably follow logical code boundaries.

Examples:

``` text
Class
Function
Method
Module
Documentation block
Configuration section
```

A chunk may contain:

``` text
Chunk
├── source_code
├── file_path
├── symbol_name
├── symbol_type
├── start_line
├── end_line
├── imports
└── related_symbols
```

This makes retrieval more meaningful.

------------------------------------------------------------------------

# 15. Embeddings

Embeddings convert code and text into numerical vectors.

Current embedding model:

``` text
nomic-embed-text
```

Conceptual process:

``` text
Code Chunk
    ↓
Embedding Model
    ↓
Vector
    ↓
FAISS
```

Similar code should produce vectors that are close in embedding space.

------------------------------------------------------------------------

# 16. Vector Database

The current planned vector store is:

``` text
FAISS
```

FAISS provides efficient similarity search over embeddings.

Example:

``` text
User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Top-K Relevant Chunks
```

Current configuration:

``` text
TOP_K=8
```

------------------------------------------------------------------------

# 17. Hybrid Search

Pure semantic search is not enough for software repositories.

The project should combine:

### Semantic Search

Useful for queries such as:

> Where is user authentication implemented?

### Keyword / Symbol Search

Useful for:

> Find every occurrence of `UserService`.

### Structural Search

Useful for:

> Which functions call `authenticate()`?

### Hybrid Search

Combines all of the above.

``` text
User Query
    │
    ├── Keyword Search
    ├── Semantic Search
    └── Structural Search
             │
             ▼
       Result Fusion
             │
             ▼
       Ranked Results
```

------------------------------------------------------------------------

# 18. RAG Architecture

RAG stands for:

**Retrieval-Augmented Generation**

The system does not ask the LLM to answer solely from its internal
knowledge.

Instead:

``` text
User Question
      ↓
Query Analysis
      ↓
Repository Retrieval
      ↓
Relevant Code
      ↓
Context Construction
      ↓
LLM
      ↓
Repository-Grounded Answer
```

------------------------------------------------------------------------

# 19. Query Analysis

The query analyzer determines what the developer is asking.

Examples:

### Code Explanation

``` text
"Explain the login function."
```

### Code Search

``` text
"Where is JWT authentication implemented?"
```

### Debugging

``` text
"Why does this API return 500?"
```

### Dependency Analysis

``` text
"What files depend on database.py?"
```

### Impact Analysis

``` text
"What will break if I modify UserService?"
```

The query type can influence retrieval strategy.

------------------------------------------------------------------------

# 20. Context Builder

The context builder combines retrieved information.

Example:

``` text
Retrieved Chunk 1
    ↓
Retrieved Chunk 2
    ↓
Related imports
    ↓
Related callers
    ↓
Related files
    ↓
Final Context
```

This is more powerful than sending isolated code snippets to the LLM.

------------------------------------------------------------------------

# 21. Prompt Builder

The prompt should instruct the LLM to:

1.  Use repository context.
2.  Avoid unsupported claims.
3.  Identify relevant files and symbols.
4.  Explain reasoning clearly.
5.  State when the repository does not contain enough information.

Example conceptual instruction:

``` text
You are a repository-aware software engineering assistant.

Answer using the supplied repository context.

Do not invent files, functions, classes, or dependencies.

When possible, mention:
- file path
- symbol name
- relevant line range
- dependency relationship

If the context is insufficient, explicitly state that.
```

------------------------------------------------------------------------

# 22. Local LLM

The project uses:

``` text
Ollama
```

Current LLM:

``` text
qwen2.5:latest
```

The model runs locally.

Advantages:

-   Privacy
-   No external API requirement
-   Works with private repositories
-   Lower long-term API cost
-   Suitable for experimentation

------------------------------------------------------------------------

# 23. Current Environment Configuration

The project uses a `.env` configuration.

Current configuration:

``` env
OLLAMA_BASE_URL=http://localhost:11434

LLM_MODEL=qwen2.5:latest

EMBEDDING_MODEL=nomic-embed-text

VECTOR_STORE_PATH=data/vector_store

REPOSITORY_PATH=data/repositories

CHUNK_PATH=data/chunks

TOP_K=8
```

------------------------------------------------------------------------

# 24. Technology Stack

## Backend

``` text
Python
FastAPI
```

## Code Analysis

``` text
Tree-sitter
```

## LLM

``` text
Ollama
Qwen
```

## Embeddings

``` text
nomic-embed-text
```

## Vector Search

``` text
FAISS
```

## RAG / AI Orchestration

Planned/possible:

``` text
LangChain
LlamaIndex
```

The architecture should avoid unnecessary coupling to one framework.

------------------------------------------------------------------------

# 25. Supporting Technologies

The broader project technology set includes:

``` text
Python
FastAPI
Tree-sitter
FAISS
Ollama
LangChain / LlamaIndex
Piper TTS
faster-whisper
```

Voice functionality can later allow developers to interact with the
copilot using speech.

------------------------------------------------------------------------

# 26. Current Project Status

## Phase 1 --- Repository Understanding

### Completed

-   Environment setup
-   Project foundation
-   Tree-sitter installation
-   Python parsing
-   Syntax-tree traversal
-   Repository file discovery
-   Directory filtering
-   Python language detection
-   Class extraction
-   Function extraction
-   Method extraction
-   Source extraction
-   Line-range extraction
-   Import extraction
-   Function-call extraction
-   `CodeEntity` model
-   `CodeFile` model
-   `RepositoryIndex` model
-   End-to-end repository indexing pipeline
-   Repository indexing tests

The latest indexing tests successfully discovered and processed
repository source files.

------------------------------------------------------------------------

# 27. Phase 2 --- Code Ingestion

## Planned Tasks

-   Design code chunking strategy
-   Entity-aware chunking
-   Metadata generation
-   Documentation ingestion
-   Test-code ingestion
-   Chunk persistence
-   Embedding generation
-   FAISS index creation

Pipeline:

``` text
RepositoryIndex
      ↓
Chunking
      ↓
Metadata
      ↓
Embeddings
      ↓
FAISS
```

------------------------------------------------------------------------

# 28. Phase 3 --- Retrieval

## Planned Tasks

-   Semantic search
-   Keyword search
-   Symbol search
-   Hybrid retrieval
-   Result ranking
-   Metadata filtering
-   Repository-aware retrieval
-   Top-K selection

Example:

``` text
Query
 ↓
Query Embedding
 ↓
Semantic Search
 ↓
Keyword Search
 ↓
Structural Search
 ↓
Score Fusion
 ↓
Top Results
```

------------------------------------------------------------------------

# 29. Phase 4 --- RAG Assistant

## Planned Tasks

-   Query classification
-   Context construction
-   Prompt generation
-   LLM integration
-   Grounded answer generation
-   Source/file references
-   Confidence handling
-   Hallucination reduction

------------------------------------------------------------------------

# 30. Phase 5 --- Developer Intelligence

Advanced capabilities:

## Code Explanation

``` text
Explain this class.
```

## Debugging

``` text
Why is this function failing?
```

## Dependency Analysis

``` text
What depends on this module?
```

## Call Graph

``` text
Who calls this function?
```

## Change Impact Analysis

``` text
What can be affected if I change this function?
```

## Refactoring Assistance

``` text
How can this module be refactored?
```

------------------------------------------------------------------------

# 31. Phase 6 --- User Interface

A possible frontend:

``` text
frontend/
```

The UI can contain:

``` text
┌───────────────────────────────────────────────┐
│ Repository-Aware AI Software Copilot         │
├───────────────────────────────────────────────┤
│ Repository: my-project                       │
├───────────────────────────────────────────────┤
│                                               │
│ Ask a question...                             │
│                                               │
│ [ Explain authentication flow ]               │
│                                               │
├───────────────────────────────────────────────┤
│ Answer                                        │
│                                               │
│ Authentication starts in                      │
│ backend/auth.py ...                           │
│                                               │
├───────────────────────────────────────────────┤
│ Relevant Files                                │
│                                               │
│ backend/auth.py                               │
│ backend/routes.py                             │
│ backend/database.py                           │
└───────────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 32. Optional Voice Interface

The project can later include:

``` text
Microphone
    ↓
faster-whisper
    ↓
Text Query
    ↓
RAG Pipeline
    ↓
LLM
    ↓
Answer
    ↓
Piper TTS
    ↓
Voice Output
```

This enables hands-free developer interaction.

------------------------------------------------------------------------

# 33. End-to-End System Flow

The complete system will operate approximately as follows:

``` text
Developer
   │
   ▼
Upload / Select Repository
   │
   ▼
Repository Scanner
   │
   ▼
Language Detection
   │
   ▼
Tree-sitter Parser
   │
   ▼
AST Analysis
   │
   ├───────────────┐
   ▼               ▼
Entities        Relationships
   │               │
   └───────┬───────┘
           ▼
    Repository Index
           │
           ▼
      Code Chunking
           │
           ▼
       Embeddings
           │
           ▼
          FAISS
           │
           │
Developer ─┤
 Question  │
           ▼
     Query Analyzer
           │
           ▼
      Hybrid Retrieval
           │
           ▼
    Context Construction
           │
           ▼
       Prompt Builder
           │
           ▼
      Local LLM / Ollama
           │
           ▼
    Grounded Response
```

------------------------------------------------------------------------

# 34. Example User Interaction

## User

``` text
Where is authentication implemented?
```

## System

1.  Analyze query.
2.  Search authentication-related symbols.
3.  Perform semantic retrieval.
4.  Inspect imports and relationships.
5.  Retrieve relevant files.
6.  Construct context.
7.  Send context to LLM.
8.  Generate answer.

Example response:

``` text
Authentication is primarily implemented in:

1. backend/auth.py
   - authenticate_user()
   - create_access_token()

2. backend/routes.py
   - login()

The login route calls authenticate_user(), which validates
the user and then generates a JWT token.
```

------------------------------------------------------------------------

# 35. Example Debugging Flow

User:

``` text
Why does the login API return 401?
```

System:

``` text
Query
 ↓
Retrieve login route
 ↓
Retrieve authentication function
 ↓
Retrieve token validation
 ↓
Retrieve user lookup
 ↓
Construct dependency-aware context
 ↓
LLM analysis
```

The answer can identify likely causes based on actual repository code
instead of generic guesses.

------------------------------------------------------------------------

# 36. Dependency Graph

The system can represent dependencies as a graph.

``` text
main.py
  │
  ├── routes.py
  │      │
  │      ├── auth.py
  │      │      │
  │      │      └── database.py
  │      │
  │      └── users.py
  │
  └── config.py
```

This graph can later be used for impact analysis.

------------------------------------------------------------------------

# 37. Call Graph

Example:

``` text
login()
   │
   ▼
authenticate_user()
   │
   ▼
get_user()
   │
   ▼
database.query()
```

This allows questions such as:

``` text
Who calls authenticate_user()?
```

or:

``` text
What happens after login() is called?
```

------------------------------------------------------------------------

# 38. Change Impact Analysis

Suppose:

``` text
database.py
```

is modified.

The system can traverse the dependency graph:

``` text
database.py
    ↑
    │
auth.py
    ↑
    │
routes.py
    ↑
    │
main.py
```

It can then report potentially affected modules.

This is one of the important advanced capabilities of the project.

------------------------------------------------------------------------

# 39. Data Flow

## Repository Ingestion

``` text
Raw Repository
      ↓
Source Files
      ↓
AST
      ↓
Entities
      ↓
Relationships
      ↓
Repository Index
```

## Retrieval

``` text
Question
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Relevant Code
```

## Generation

``` text
Relevant Code
      ↓
Context
      ↓
Prompt
      ↓
LLM
      ↓
Answer
```

------------------------------------------------------------------------

# 40. Testing Strategy

Testing should be performed at multiple levels.

## Unit Tests

Test:

-   File discovery
-   Language detection
-   AST parsing
-   Entity extraction
-   Import extraction
-   Call extraction
-   Chunk generation
-   Embedding generation

## Integration Tests

Test:

``` text
Repository
   ↓
Parser
   ↓
Index
   ↓
Chunker
   ↓
Embedding
   ↓
FAISS
   ↓
Retriever
```

## End-to-End Tests

Test:

``` text
User Query
    ↓
RAG
    ↓
LLM
    ↓
Final Answer
```

------------------------------------------------------------------------

# 41. Validation

The system should validate:

-   Repository path
-   File existence
-   Supported language
-   Parser availability
-   Source-code encoding
-   Empty repositories
-   Corrupted files
-   Duplicate entities
-   Invalid configuration
-   Missing embedding model
-   Missing LLM
-   Vector-store consistency

------------------------------------------------------------------------

# 42. Error Handling

Errors should be handled at each layer.

Example:

``` text
Repository Scanner
       ↓
File access error
       ↓
Log error
       ↓
Continue with remaining files
```

A single malformed source file should ideally not terminate the entire
indexing process.

The system should report:

``` text
File
Error Type
Error Message
```

------------------------------------------------------------------------

# 43. Logging

Logging should provide information such as:

``` text
INFO  Repository scan started
INFO  Found 20 source files
INFO  Parsing backend/main.py
INFO  Extracted 4 functions
INFO  Extracted 2 classes
INFO  Extracted 8 imports
INFO  Repository indexing completed
```

Errors:

``` text
ERROR Failed to parse file: example.py
ERROR Unsupported syntax node
```

------------------------------------------------------------------------

# 44. Configuration Management

Configuration should be centralized.

Example:

``` text
backend/utils/config.py
```

Configuration values include:

``` text
OLLAMA_BASE_URL
LLM_MODEL
EMBEDDING_MODEL
VECTOR_STORE_PATH
REPOSITORY_PATH
CHUNK_PATH
TOP_K
```

This avoids hardcoding values throughout the application.

------------------------------------------------------------------------

# 45. Security Considerations

Because this system analyzes potentially private source code, security
is important.

## Local Processing

Using Ollama allows source code to remain local.

## Repository Isolation

Each repository should have an isolated index.

## Input Validation

Repository paths and API inputs should be validated.

## Secrets

API keys and secrets must never be stored directly in source code.

Use:

``` text
.env
```

and exclude it from Git.

------------------------------------------------------------------------

# 46. `.gitignore`

The project should ignore:

``` text
.venv/
__pycache__/
*.pyc
.env
data/repositories/
data/vector_store/
data/chunks/
.idea/
.vscode/
```

Large generated vector indexes should not normally be committed unless
required.

------------------------------------------------------------------------

# 47. Installation

## Create Virtual Environment

``` bash
python -m venv .venv
```

## Activate on Windows

``` powershell
.venv\Scripts\activate
```

## Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 48. Ollama Setup

Install Ollama and ensure the local server is available.

Check:

``` bash
ollama list
```

Run the LLM:

``` bash
ollama run qwen2.5:latest
```

Run the embedding model:

``` bash
ollama run nomic-embed-text
```

Default Ollama endpoint:

``` text
http://localhost:11434
```

------------------------------------------------------------------------

# 49. Running the Project

The exact command can depend on the final application entry point.

For FastAPI, a typical command is:

``` bash
uvicorn backend.main:app --reload
```

The API can then be accessed locally.

------------------------------------------------------------------------

# 50. Development Workflow

Recommended workflow:

``` text
1. Modify code
      ↓
2. Run unit tests
      ↓
3. Run repository indexing
      ↓
4. Verify RepositoryIndex
      ↓
5. Build/update chunks
      ↓
6. Update embeddings
      ↓
7. Test retrieval
      ↓
8. Test RAG
      ↓
9. Test API
```

------------------------------------------------------------------------

# 51. Phase-Wise Development Plan

  Phase     Component                    Status
  --------- ---------------------------- -----------
  Phase 1   Repository Understanding     Completed
  Phase 2   Code Ingestion               Planned
  Phase 3   Vector Search                Planned
  Phase 4   RAG Assistant                Planned
  Phase 5   Dependency/Impact Analysis   Planned
  Phase 6   Web UI                       Planned
  Phase 7   Voice Interface              Optional
  Phase 8   Evaluation & Optimization    Planned

------------------------------------------------------------------------

# 52. Current Milestone

The project has successfully established the most important foundation:

``` text
Repository
     ↓
File Discovery
     ↓
Tree-sitter
     ↓
AST Analysis
     ↓
Code Entities
     ↓
Imports
     ↓
Calls
     ↓
RepositoryIndex
```

This means the project has moved beyond a simple chatbot concept and has
a genuine **repository-understanding layer**.

------------------------------------------------------------------------

# 53. Next Immediate Tasks

The recommended next implementation sequence is:

### Step 1

Finalize the repository index schema.

### Step 2

Implement entity-aware code chunking.

### Step 3

Generate embeddings using:

``` text
nomic-embed-text
```

### Step 4

Create FAISS vector storage.

### Step 5

Implement semantic retrieval.

### Step 6

Add hybrid retrieval.

### Step 7

Connect retrieval to Ollama.

### Step 8

Implement the first RAG query endpoint.

### Step 9

Test questions such as:

``` text
Explain this repository.
Where is authentication implemented?
What does this function do?
Which files call this function?
Where is the database connection created?
```

------------------------------------------------------------------------

# 54. Expected Final Capabilities

The completed system should be able to answer questions such as:

### Repository Understanding

``` text
What does this repository do?
```

### Code Explanation

``` text
Explain the UserService class.
```

### Code Search

``` text
Where is authentication implemented?
```

### Debugging

``` text
Why might this function fail?
```

### Dependency Analysis

``` text
What modules depend on database.py?
```

### Call Analysis

``` text
Who calls process_request()?
```

### Impact Analysis

``` text
What could be affected if I modify this function?
```

### Architecture

``` text
Explain the architecture of this project.
```

------------------------------------------------------------------------

# 55. Research / Academic Contribution

The project combines several areas of computer science and artificial
intelligence:

``` text
Program Analysis
       +
AST Parsing
       +
Information Retrieval
       +
Vector Search
       +
Embeddings
       +
RAG
       +
LLMs
       +
Software Engineering
```

The key research/engineering contribution is the integration of
**structural program understanding with retrieval-augmented LLM
reasoning**.

Rather than treating source code as ordinary text, the system preserves:

-   Symbols
-   File boundaries
-   Line ranges
-   Imports
-   Calls
-   Dependencies
-   Repository structure

This produces more relevant context for software-engineering questions.

------------------------------------------------------------------------

# 56. Advantages

## Compared with Generic Chatbots

-   Repository-specific answers
-   Better grounding
-   Lower hallucination risk
-   Code-aware retrieval
-   Dependency awareness

## Compared with Keyword Search

-   Semantic understanding
-   Natural-language queries
-   Context-aware retrieval
-   Relationship-aware analysis

## Compared with Cloud-Only AI

-   Local processing
-   Better privacy
-   No mandatory external API
-   Suitable for private repositories

------------------------------------------------------------------------

# 57. Limitations

Current limitations include:

-   Primary parser support is currently focused on Python.
-   Static analysis may not resolve all dynamic Python behavior.
-   LLM answers depend on retrieval quality.
-   Very large repositories require efficient indexing.
-   Dynamic imports can be difficult to analyze.
-   Runtime behavior cannot always be inferred from static source code.
-   Call resolution can be ambiguous in dynamically typed languages.

These limitations can be addressed through improved static analysis,
language-specific parsers, runtime telemetry, better retrieval, and
graph-based reasoning.

------------------------------------------------------------------------

# 58. Future Enhancements

Potential future features:

1.  Multi-language repository support.
2.  Git history analysis.
3.  Commit-aware reasoning.
4.  Pull-request review.
5.  Automatic bug localization.
6.  Automated test generation.
7.  Code refactoring suggestions.
8.  Security vulnerability detection.
9.  Architecture visualization.
10. Dependency graph visualization.
11. Call graph visualization.
12. IDE integration.
13. Voice-based interaction.
14. Multi-repository search.
15. Agentic software engineering workflows.

------------------------------------------------------------------------

# 59. Final Architecture Summary

``` text
                 ┌─────────────────────────┐
                 │        Developer        │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      Copilot UI/API     │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │     Query Analyzer      │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Hybrid Retrieval      │
                 └────────────┬────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
       ┌────────────────┐          ┌────────────────┐
       │ Vector Search  │          │ Code Structure │
       │     FAISS      │          │ / Graph Index  │
       └───────┬────────┘          └───────┬────────┘
               │                           │
               └─────────────┬─────────────┘
                             ▼
                   ┌───────────────────┐
                   │ Context Builder   │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │ Prompt Generator  │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │ Ollama / Qwen LLM │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │ Grounded Answer   │
                   └───────────────────┘


       Repository Ingestion Pipeline

       Repository
           ↓
       Scanner
           ↓
       Tree-sitter
           ↓
       AST Analysis
           ↓
       Entity Extraction
           ↓
       Import + Call Extraction
           ↓
       RepositoryIndex
           ↓
       Chunking
           ↓
       Embeddings
           ↓
       FAISS
```

------------------------------------------------------------------------

# 60. Conclusion

The **AI Software Engineering Copilot for Large Codebases** is designed
as a repository-aware developer assistant rather than a generic
conversational AI.

The key foundation is the **Repository Understanding Layer**, which
converts raw source code into a structured representation containing
files, symbols, imports, calls, and relationships.

The next major milestone is to connect this structured representation to
the **embedding and retrieval layer**, followed by **RAG-based LLM
reasoning**.

The overall progression is:

``` text
Understand the Repository
          ↓
Index the Repository
          ↓
Embed the Repository
          ↓
Retrieve Relevant Code
          ↓
Build Context
          ↓
Reason with LLM
          ↓
Assist the Developer
```

This architecture provides a strong foundation for a semester-level AI
project and can later be extended into an advanced software-engineering
agent capable of repository analysis, debugging, impact analysis, code
review, and automated development workflows.

------------------------------------------------------------------------

# Project Status

**Current Phase:** Phase 1 --- Repository Understanding\
**Phase 1 Status:** Completed\
**Next Phase:** Phase 2 --- Code Ingestion + Embeddings + Vector Search
