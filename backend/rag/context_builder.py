from typing import List, Optional, Tuple, Dict, Any
from backend.models.chunk import CodeChunk

class ContextBuilder:
    @staticmethod
    def build_context(
        retrieved_chunks: List[Tuple[CodeChunk, float, str]],
        extra_graph_info: Optional[Dict[str, Any]] = None,
        max_chars: int = 4800
    ) -> str:
        """
        Synthesize retrieved code chunks and graph relationships into a
        structured prompt context optimized for low-latency generation.
        """
        parts = ["### REPOSITORY CODE CONTEXT:"]
        current_chars = len(parts[0])

        # Add chunks
        for rank, (chunk, score, provenance) in enumerate(retrieved_chunks, start=1):
            chunk_header = (
                f"\n--- [Source #{rank}] File: `{chunk.relative_path}` "
                f"(Lines {chunk.start_line}-{chunk.end_line}) | Type: {chunk.entity_type} "
                f"| Matched via: {provenance} ---"
            )
            # Truncate very long individual chunks to 900 chars to maximize diversity
            chunk_text = chunk.content[:900] + ("\n...[truncated]" if len(chunk.content) > 900 else "")
            code_block = f"```{chunk.language}\n{chunk_text}\n```"
            entry = f"{chunk_header}\n{code_block}"

            if current_chars + len(entry) > max_chars:
                parts.append("\n[Additional lower-ranked snippets omitted for speed]")
                break

            parts.append(entry)
            current_chars += len(entry)

        # Add structural graph information if provided
        if extra_graph_info:
            graph_header = "\n### REPOSITORY STRUCTURAL RELATIONSHIPS:"
            graph_lines = [graph_header]
            if "direct_dependents" in extra_graph_info and extra_graph_info["direct_dependents"]:
                graph_lines.append(f"- Direct Dependents: {', '.join(extra_graph_info['direct_dependents'])}")
            if "affected_callers" in extra_graph_info and extra_graph_info["affected_callers"]:
                callers_desc = [f"{c.get('symbol')} in `{c.get('file')}`" for c in extra_graph_info["affected_callers"][:8]]
                graph_lines.append(f"- Callers: {', '.join(callers_desc)}")
            
            graph_text = "\n".join(graph_lines)
            if current_chars + len(graph_text) <= max_chars + 2000:
                parts.append(graph_text)

        return "\n".join(parts)
