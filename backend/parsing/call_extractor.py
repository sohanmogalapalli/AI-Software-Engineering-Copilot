from typing import List
from tree_sitter import Node
from backend.parsing.ast_traversal import get_node_text, traverse_tree

class CallExtractor:
    @staticmethod
    def extract_calls(node: Node, source_code: str, language: str) -> List[str]:
        calls: List[str] = []
        if language == "python":
            for n in traverse_tree(node):
                if n.type == "call":
                    func_node = n.child_by_field_name("function")
                    if func_node:
                        call_text = get_node_text(func_node, source_code).strip()
                        # normalize attribute calls e.g. self.helper -> helper or db.query -> db.query
                        if call_text and call_text not in calls:
                            calls.append(call_text)
        elif language in ("javascript", "typescript"):
            for n in traverse_tree(node):
                if n.type == "call_expression":
                    func_node = n.child_by_field_name("function")
                    if func_node:
                        call_text = get_node_text(func_node, source_code).strip()
                        if call_text and call_text not in calls:
                            calls.append(call_text)
        else:
            for n in traverse_tree(node):
                if "call" in n.type:
                    text = get_node_text(n, source_code).split("(")[0].strip()
                    if text and text not in calls:
                        calls.append(text)
        return calls
