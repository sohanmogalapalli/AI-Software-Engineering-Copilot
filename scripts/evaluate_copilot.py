import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.state import app_state
from backend.utils.logging import logger
from rich.console import Console
from rich.table import Table

TEST_BENCHMARK = [
    {
        "query": "Where is the TreeSitterManager defined?",
        "expected_file": "backend/parsing/tree_sitter_parser.py",
        "expected_symbol": "TreeSitterManager"
    },
    {
        "query": "How is the AST traversal implemented?",
        "expected_file": "backend/parsing/ast_traversal.py",
        "expected_symbol": "traverse_tree"
    },
    {
        "query": "Where are context enriched chunks created?",
        "expected_file": "backend/ingestion/chunker.py",
        "expected_symbol": "ContextEnrichedChunker"
    },
    {
        "query": "How does BM25 keyword search work?",
        "expected_file": "backend/vectorstore/bm25_store.py",
        "expected_symbol": "BM25CodeStore"
    },
    {
        "query": "Where is the change impact analysis logic?",
        "expected_file": "backend/analysis/impact_analysis.py",
        "expected_symbol": "ImpactAnalysisService"
    },
    {
        "query": "Where is the FastAPI application entrypoint?",
        "expected_file": "backend/main.py",
        "expected_symbol": "app"
    }
]

def evaluate():
    app_state.initialize()
    if not app_state.retriever:
        logger.error("No index found. Run index_repository.py first.")
        return

    console = Console()
    table = Table(title="AI Copilot Retrieval Benchmark (Hit Rate & MRR)")
    table.add_column("Query", style="cyan")
    table.add_column("Expected File", style="magenta")
    table.add_column("Rank", style="green")
    table.add_column("Hit@3", style="yellow")
    table.add_column("Reciprocal Rank", style="blue")

    reciprocal_ranks = []
    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0

    for item in TEST_BENCHMARK:
        results = app_state.retriever.retrieve(item["query"], top_k=10)
        found_rank = None

        for rank, (chunk, score, prov) in enumerate(results, start=1):
            if item["expected_file"] in chunk.relative_path or (item["expected_symbol"] and chunk.entity_name == item["expected_symbol"]):
                found_rank = rank
                break

        if found_rank:
            rr = 1.0 / found_rank
            reciprocal_ranks.append(rr)
            if found_rank == 1:
                hits_at_1 += 1
            if found_rank <= 3:
                hits_at_3 += 1
            if found_rank <= 5:
                hits_at_5 += 1
            hit_str = "YES" if found_rank <= 3 else "NO"
            table.add_row(item["query"], item["expected_file"], str(found_rank), hit_str, f"{rr:.3f}")
        else:
            reciprocal_ranks.append(0.0)
            table.add_row(item["query"], item["expected_file"], "MISS", "NO", "0.000")

    console.print(table)
    total = len(TEST_BENCHMARK)
    mrr = sum(reciprocal_ranks) / total if total > 0 else 0.0

    console.print(f"\n[bold]Summary Metrics:[/bold]")
    console.print(f"Hit Rate @ 1: {hits_at_1}/{total} ({hits_at_1/total*100:.1f}%)")
    console.print(f"Hit Rate @ 3: {hits_at_3}/{total} ({hits_at_3/total*100:.1f}%)")
    console.print(f"Hit Rate @ 5: {hits_at_5}/{total} ({hits_at_5/total*100:.1f}%)")
    console.print(f"Mean Reciprocal Rank (MRR): [bold green]{mrr:.4f}[/bold green]\n")

if __name__ == "__main__":
    evaluate()
