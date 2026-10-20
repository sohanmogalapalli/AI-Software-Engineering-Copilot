from typing import Dict, List, Set, Tuple
import networkx as nx
from backend.models.repository_index import RepositoryIndex
from backend.utils.logging import logger

class CallGraphService:
    def __init__(self, index: RepositoryIndex):
        self.index = index
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self) -> None:
        """Build directed call graph where edges represent caller -> callee."""
        # Add all defined entities as nodes
        for code_file in self.index.files.values():
            for entity in code_file.entities:
                node_id = f"{code_file.relative_path}:{entity.qualified_name}"
                self.graph.add_node(
                    node_id,
                    name=entity.name,
                    qualified_name=entity.qualified_name,
                    file=code_file.relative_path,
                    entity_type=entity.entity_type
                )

        # Connect callers to callees
        for code_file in self.index.files.values():
            for entity in code_file.entities:
                caller_id = f"{code_file.relative_path}:{entity.qualified_name}"
                for call_name in entity.calls:
                    clean_target = call_name.split(".")[-1]
                    # Find candidate target nodes
                    for node_id, data in self.graph.nodes(data=True):
                        if data.get("name") == clean_target and node_id != caller_id:
                            self.graph.add_edge(caller_id, node_id)

        logger.info(
            f"Call Graph constructed: {self.graph.number_of_nodes()} symbols, "
            f"{self.graph.number_of_edges()} call relationships."
        )

    def get_callers(self, symbol_name: str) -> List[Dict[str, str]]:
        """Find functions/methods that call this symbol."""
        callers = []
        clean_name = symbol_name.split(":")[-1].split(".")[-1].lower()

        target_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get("name", "").lower() == clean_name or symbol_name in node
        ]

        for target in target_nodes:
            for pred in self.graph.predecessors(target):
                data = self.graph.nodes[pred]
                callers.append({
                    "node_id": pred,
                    "symbol": data.get("qualified_name", pred),
                    "file": data.get("file", ""),
                    "type": data.get("entity_type", "")
                })

        return callers

    def get_callees(self, symbol_name: str) -> List[Dict[str, str]]:
        """Find functions/methods called by this symbol."""
        callees = []
        clean_name = symbol_name.split(":")[-1].split(".")[-1].lower()

        target_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get("name", "").lower() == clean_name or symbol_name in node
        ]

        for target in target_nodes:
            for succ in self.graph.successors(target):
                data = self.graph.nodes[succ]
                callees.append({
                    "node_id": succ,
                    "symbol": data.get("qualified_name", succ),
                    "file": data.get("file", ""),
                    "type": data.get("entity_type", "")
                })

        return callees
