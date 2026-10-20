from typing import List
from pydantic import BaseModel, Field
from backend.models.code_entity import CodeEntity

class CodeFile(BaseModel):
    path: str
    relative_path: str
    language: str
    content_hash: str
    line_count: int
    imports: List[str] = Field(default_factory=list)
    entities: List[CodeEntity] = Field(default_factory=list)
    all_calls: List[str] = Field(default_factory=list)

    @property
    def classes(self) -> List[CodeEntity]:
        return [e for e in self.entities if e.entity_type == "class"]

    @property
    def functions(self) -> List[CodeEntity]:
        return [e for e in self.entities if e.entity_type in ("function", "method")]
