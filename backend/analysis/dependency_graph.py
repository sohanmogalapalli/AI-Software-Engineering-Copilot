from typing import Dict, List, Set, Tuple
import networkx as nx
from backend.models.repository_index import RepositoryIndex
from backend.utils.logging import logger

class DependencyGraphService:
    def __init__(self, index: RepositoryIndex):
        self.index = index
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self) -> None:
        """Construct directed dependency graph from repository index."""
        # Add all files as nodes
        for rel_path, code_file in self.index.files.items():
            self.graph.add_node(
                rel_path,
                language=code_file.language,
                line_count=code_file.line_count,
                entity_count=len(code_file.entities)
            )

        # Add dependency edges (from_file -> to_file)
        for src, dst in self.index.dependency_edges:
            if self.graph.has_node(src) and self.graph.has_node(dst):
                self.graph.add_edge(src, dst)

        logger.info(
            f"Dependency Graph constructed: {self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges."
        )

    def get_dependencies(self, file_path: str) -> List[str]:
        """Get direct dependencies (files this file imports)."""
        if not self.graph.has_node(file_path):
            return []
        return list(self.graph.successors(file_path))

    def get_dependents(self, file_path: str) -> List[str]:
        """Get direct dependents (files that import this file)."""
        if not self.graph.has_node(file_path):
            return []
        return list(self.graph.predecessors(file_path))

    def get_transitive_dependents(self, file_path: str, max_depth: int = 4) -> Set[str]:
        """Get all downstream files that transitively depend on this file."""
        if not self.graph.has_node(file_path):
            return set()

        dependents = set()
        queue = [(file_path, 0)]
        visited = {file_path}

        while queue:
            curr, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for pred in self.graph.predecessors(curr):
                if pred not in visited:
                    visited.add(pred)
                    dependents.add(pred)
                    queue.append((pred, depth + 1))

        return dependents

    def find_circular_dependencies(self) -> List[List[str]]:
        """Detect any circular import dependency cycles."""
        try:
            return list(nx.simple_cycles(self.graph))
        except Exception:
            return []

    def get_central_files(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """Calculate PageRank to identify core hub files in the repository."""
        if self.graph.number_of_nodes() == 0:
            return []
        try:
            ranks = nx.pagerank(self.graph)
            sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
            return sorted_ranks[:top_k]
        except Exception:
            return []
