import re
from typing import List, Optional
from tree_sitter import Node
from backend.parsing.ast_traversal import get_node_text, traverse_tree

class ImportExtractor:
    @staticmethod
    def extract_imports(root_node: Optional[Node], source_code: str, language: str) -> List[str]:
        imports: List[str] = []
        if root_node:
            if language == "python":
                imports.extend(ImportExtractor._extract_python_imports(root_node, source_code))
            elif language in ("javascript", "typescript"):
                imports.extend(ImportExtractor._extract_js_imports(root_node, source_code))
            elif language == "go":
                imports.extend(ImportExtractor._extract_go_imports(root_node, source_code))
            elif language == "rust":
                imports.extend(ImportExtractor._extract_rust_imports(root_node, source_code))
            elif language in ("java", "kotlin"):
                imports.extend(ImportExtractor._extract_java_imports(root_node, source_code))
            elif language in ("c", "cpp"):
                imports.extend(ImportExtractor._extract_cpp_includes(root_node, source_code))
            elif language in ("c_sharp", "csharp"):
                imports.extend(ImportExtractor._extract_csharp_usings(root_node, source_code))

        # If AST extraction returned empty or language has no AST parser, use regex fallback
        if not imports:
            imports.extend(ImportExtractor._extract_generic_imports(source_code))

        return sorted(list(set(imports)))

    @staticmethod
    def _extract_python_imports(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type == "import_statement":
                for child in node.children:
                    if child.type == "dotted_name":
                        results.append(get_node_text(child, source_code))
                    elif child.type == "aliased_import":
                        name_node = child.child_by_field_name("name")
                        if name_node:
                            results.append(get_node_text(name_node, source_code))
            elif node.type == "import_from_statement":
                module_node = node.child_by_field_name("module_name")
                module_name = get_node_text(module_node, source_code) if module_node else ""
                for child in node.children:
                    if child.type == "dotted_name" and child != module_node:
                        sym = get_node_text(child, source_code)
                        results.append(f"{module_name}.{sym}" if module_name else sym)
                    elif child.type == "aliased_import":
                        name_node = child.child_by_field_name("name")
                        if name_node:
                            sym = get_node_text(name_node, source_code)
                            results.append(f"{module_name}.{sym}" if module_name else sym)
        return results

    @staticmethod
    def _extract_js_imports(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type == "import_statement":
                source_node = node.child_by_field_name("source")
                if source_node:
                    results.append(get_node_text(source_node, source_code).strip("'\"`"))
            elif node.type == "call_expression":
                func_node = node.child_by_field_name("function")
                if func_node and get_node_text(func_node, source_code) == "require":
                    args = node.child_by_field_name("arguments")
                    if args and len(args.children) > 1:
                        results.append(get_node_text(args.children[1], source_code).strip("'\"`"))
        return results

    @staticmethod
    def _extract_go_imports(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type in ("import_spec", "interpreted_string_literal"):
                if node.parent and node.parent.type in ("import_spec", "import_declaration"):
                    results.append(get_node_text(node, source_code).strip('"'))
        return results

    @staticmethod
    def _extract_rust_imports(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type == "use_declaration":
                text = get_node_text(node, source_code).replace("use ", "").replace(";", "").strip()
                if text:
                    results.append(text)
        return results

    @staticmethod
    def _extract_java_imports(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type == "import_declaration":
                text = get_node_text(node, source_code).replace("import ", "").replace(";", "").strip()
                if text:
                    results.append(text)
        return results

    @staticmethod
    def _extract_cpp_includes(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if "include" in node.type or node.type == "preproc_include":
                path_node = node.child_by_field_name("path")
                if path_node:
                    results.append(get_node_text(path_node, source_code).strip('<>"'))
                else:
                    text = get_node_text(node, source_code).replace("#include", "").strip('<>" \r\n')
                    if text:
                        results.append(text)
        return results

    @staticmethod
    def _extract_csharp_usings(root_node: Node, source_code: str) -> List[str]:
        results: List[str] = []
        for node in traverse_tree(root_node):
            if node.type == "using_directive":
                text = get_node_text(node, source_code).replace("using ", "").replace(";", "").strip()
                if text:
                    results.append(text)
        return results

    @staticmethod
    def _extract_generic_imports(source_code: str) -> List[str]:
        """Regex fallback for any programming language."""
        results = []
        patterns = [
            r'^\s*(?:import|using|include|require|from)\s+([a-zA-Z0-9_\.\/"\<\>]+)',
            r'#include\s*[<"]([^>"]+)[>"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'use\s+([a-zA-Z0-9_:\\]+);',
        ]
        for pat in patterns:
            for match in re.finditer(pat, source_code, re.MULTILINE):
                clean = match.group(1).strip(';"\'')
                if clean and len(clean) > 1 and clean not in results:
                    results.append(clean)
        return results
