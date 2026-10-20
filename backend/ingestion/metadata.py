import re
from typing import Set, List
from backend.models.chunk import CodeChunk

IDENTIFIER_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

def split_identifier(identifier: str) -> List[str]:
    """Split camelCase and snake_case into component terms."""
    # Split on underscore
    parts = identifier.split("_")
    subparts = []
    for part in parts:
        # Split on camelCase
        matches = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)", part)
        if matches:
            subparts.extend(matches)
        elif part:
            subparts.append(part)
    return [p.lower() for p in subparts if len(p) > 1]

def extract_search_keywords(chunk: CodeChunk) -> Set[str]:
    """Extract tokenized search keywords for BM25 and exact matching."""
    keywords = set()
    if chunk.entity_name:
        keywords.add(chunk.entity_name.lower())
        keywords.update(split_identifier(chunk.entity_name))
    
    path_tokens = re.split(r"[/\\._-]", chunk.relative_path)
    for tok in path_tokens:
        if len(tok) > 2:
            keywords.add(tok.lower())

    for call in chunk.calls:
        clean_call = call.split(".")[-1]
        keywords.add(clean_call.lower())

    return keywords
