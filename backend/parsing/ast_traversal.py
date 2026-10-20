from typing import Generator, List, Optional
from tree_sitter import Node

def get_node_text(node: Node, source_code: str) -> str:
    """Extract text from source code corresponding to a tree-sitter node."""
    start_byte = node.start_byte
    end_byte = node.end_byte
    return source_code.encode("utf-8")[start_byte:end_byte].decode("utf-8", errors="replace")

def find_children_by_type(node: Node, type_name: str) -> List[Node]:
    """Find immediate children matching node type."""
    return [child for child in node.children if child.type == type_name]

def find_first_child_by_type(node: Node, type_name: str) -> Optional[Node]:
    """Find the first immediate child matching node type."""
    for child in node.children:
        if child.type == type_name:
            return child
    return None

def traverse_tree(node: Node) -> Generator[Node, None, None]:
    """Depth-first traversal generator yielding all AST nodes."""
    yield node
    for child in node.children:
        yield from traverse_tree(child)
