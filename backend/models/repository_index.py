from typing import Dict, List, Tuple
from pydantic import BaseModel, Field
from backend.models.code_file import CodeFile
from backend.models.code_entity import CodeEntity

class RepositoryIndex(BaseModel):
    repository_path: str
    name: str
    indexed_at: str
    files: Dict[str, CodeFile] = Field(default_factory=dict)
    languages: Dict[str, int] = Field(default_factory=dict)
    dependency_edges: List[Tuple[str, str]] = Field(default_factory=list)
    call_edges: List[Tuple[str, str]] = Field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_entities(self) -> int:
        return sum(len(f.entities) for f in self.files.values())

    @property
    def all_entities(self) -> List[CodeEntity]:
        all_e = []
        for f in self.files.values():
            all_e.extend(f.entities)
        return all_e

    def find_entity_by_name(self, name: str) -> List[CodeEntity]:
        """Case-insensitive exact or partial match for entity names."""
        name_lower = name.lower()
        return [
            e for e in self.all_entities
            if e.name.lower() == name_lower or e.qualified_name.lower() == name_lower
        ]
