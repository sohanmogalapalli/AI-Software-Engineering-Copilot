from typing import List, Optional
from pydantic import BaseModel, Field

class CodeChunk(BaseModel):
    chunk_id: str
    file_path: str
    relative_path: str
    language: str
    entity_name: Optional[str] = None
    entity_type: str  # "class", "function", "method", "module_overview"
    start_line: int
    end_line: int
    content: str
    enriched_content: str
    docstring: Optional[str] = None
    imports: List[str] = Field(default_factory=list)
    calls: List[str] = Field(default_factory=list)
