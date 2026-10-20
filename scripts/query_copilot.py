import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.state import app_state
from backend.utils.logging import logger
from rich.console import Console
from rich.markdown import Markdown

def main():
    parser = argparse.ArgumentParser(description="Query the AI Software Engineering Copilot CLI")
    parser.add_argument("query", help="Question to ask about the codebase")
    parser.add_argument("--top-k", type=int, default=8, help="Number of retrieved chunks")
    args = parser.parse_args()

    app_state.initialize()
    if not app_state.rag_pipeline:
        logger.error("No indexed repository found. Run python scripts/index_repository.py first.")
        sys.exit(1)

    console = Console()
    console.print(f"\n[bold cyan]Query:[/bold cyan] {args.query}\n")

    res = app_state.rag_pipeline.query(args.query, top_k=args.top_k)

    console.print(f"[bold yellow]Intent:[/bold yellow] {res['intent']}")
    console.print("[bold green]Answer:[/bold green]")
    console.print(Markdown(res["answer"]))

    console.print("\n[bold magenta]Citations:[/bold magenta]")
    for cit in res["citations"]:
        console.print(f"- `{cit['file']}:{cit['lines']}` ({cit['entity']} - {cit['type']})")

if __name__ == "__main__":
    main()
