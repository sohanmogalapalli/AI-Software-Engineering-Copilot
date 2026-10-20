from typing import List, Optional
from pydantic import BaseModel, Field

class CodeEntity(BaseModel):
    name: str
    entity_type: str  # "class", "function", "method"
    file_path: str
    start_line: int
    end_line: int
    source: str
    docstring: Optional[str] = None
    parent_entity: Optional[str] = None
    parameters: List[str] = Field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)
    calls: List[str] = Field(default_factory=list)

    @property
    def qualified_name(self) -> str:
        if self.parent_entity:
            return f"{self.parent_entity}.{self.name}"
        return self.name

    @property
    def line_span(self) -> int:
        return max(1, self.end_line - self.start_line + 1)
