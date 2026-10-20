import re
from typing import List, Optional
from tree_sitter import Node
from backend.models.code_entity import CodeEntity
from backend.parsing.ast_traversal import get_node_text, traverse_tree
from backend.parsing.call_extractor import CallExtractor

class EntityExtractor:
    @staticmethod
    def extract_entities(root_node: Optional[Node], source_code: str, file_path: str, language: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []

        if root_node:
            if language == "python":
                entities.extend(EntityExtractor._extract_python_entities(root_node, source_code, file_path))
            elif language in ("javascript", "typescript"):
                entities.extend(EntityExtractor._extract_js_entities(root_node, source_code, file_path))
            elif language == "go":
                entities.extend(EntityExtractor._extract_go_entities(root_node, source_code, file_path))
            elif language == "rust":
                entities.extend(EntityExtractor._extract_rust_entities(root_node, source_code, file_path))
            elif language in ("java", "kotlin"):
                entities.extend(EntityExtractor._extract_java_entities(root_node, source_code, file_path))
            elif language in ("c", "cpp"):
                entities.extend(EntityExtractor._extract_cpp_entities(root_node, source_code, file_path))
            elif language in ("c_sharp", "csharp"):
                entities.extend(EntityExtractor._extract_csharp_entities(root_node, source_code, file_path))
            elif language == "php":
                entities.extend(EntityExtractor._extract_php_entities(root_node, source_code, file_path))

        # Universal fallback: if AST returned nothing or language has no AST grammar
        if not entities:
            entities.extend(EntityExtractor._extract_generic_entities(source_code, file_path, language))

        return entities

    # ================= PYTHON =================
    @staticmethod
    def _extract_python_docstring(body_node: Optional[Node], source_code: str) -> Optional[str]:
        if not body_node:
            return None
        for child in body_node.children:
            if child.type == "expression_statement":
                for expr_child in child.children:
                    if expr_child.type == "string":
                        raw_str = get_node_text(expr_child, source_code)
                        return raw_str.strip('"""').strip("'''").strip('"').strip("'").strip()
        return None

    @staticmethod
    def _extract_python_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []

        def visit(node: Node, current_class: Optional[str] = None):
            if node.type == "class_definition":
                name_node = node.child_by_field_name("name")
                body_node = node.child_by_field_name("body")
                class_name = get_node_text(name_node, source_code) if name_node else "AnonymousClass"
                docstring = EntityExtractor._extract_python_docstring(body_node, source_code)
                target_node = node.parent if node.parent and node.parent.type == "decorated_definition" else node

                decorators = []
                if node.parent and node.parent.type == "decorated_definition":
                    for c in node.parent.children:
                        if c.type == "decorator":
                            decorators.append(get_node_text(c, source_code).strip())

                entities.append(CodeEntity(
                    name=class_name,
                    entity_type="class",
                    file_path=file_path,
                    start_line=target_node.start_point.row + 1,
                    end_line=target_node.end_point.row + 1,
                    source=get_node_text(target_node, source_code),
                    docstring=docstring,
                    decorators=decorators,
                    calls=CallExtractor.extract_calls(node, source_code, "python")
                ))

                if body_node:
                    for child in body_node.children:
                        visit(child, current_class=class_name)
                return

            if node.type == "function_definition":
                name_node = node.child_by_field_name("name")
                body_node = node.child_by_field_name("body")
                params_node = node.child_by_field_name("parameters")
                func_name = get_node_text(name_node, source_code) if name_node else "anonymous"
                target_node = node.parent if node.parent and node.parent.type == "decorated_definition" else node

                decorators = []
                if node.parent and node.parent.type == "decorated_definition":
                    for c in node.parent.children:
                        if c.type == "decorator":
                            decorators.append(get_node_text(c, source_code).strip())

                parameters = []
                if params_node:
                    for c in params_node.children:
                        if c.type not in (",", "(", ")"):
                            p_txt = get_node_text(c, source_code).strip()
                            if p_txt:
                                parameters.append(p_txt)

                entities.append(CodeEntity(
                    name=func_name,
                    entity_type="method" if current_class else "function",
                    file_path=file_path,
                    start_line=target_node.start_point.row + 1,
                    end_line=target_node.end_point.row + 1,
                    source=get_node_text(target_node, source_code),
                    docstring=EntityExtractor._extract_python_docstring(body_node, source_code),
                    parent_entity=current_class,
                    parameters=parameters,
                    decorators=decorators,
                    calls=CallExtractor.extract_calls(node, source_code, "python")
                ))
                return

            for child in node.children:
                visit(child, current_class)

        visit(root_node)
        return entities

    # ================= JAVASCRIPT & TYPESCRIPT =================
    @staticmethod
    def _extract_js_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []

        def visit(node: Node, current_class: Optional[str] = None):
            if node.type in ("class_declaration", "class"):
                name_node = node.child_by_field_name("name")
                class_name = get_node_text(name_node, source_code) if name_node else "AnonymousClass"
                entities.append(CodeEntity(
                    name=class_name,
                    entity_type="class",
                    file_path=file_path,
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    source=get_node_text(node, source_code),
                    calls=CallExtractor.extract_calls(node, source_code, "javascript")
                ))
                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        visit(child, current_class=class_name)
                return

            if node.type in ("function_declaration", "method_definition", "function"):
                name_node = node.child_by_field_name("name")
                func_name = get_node_text(name_node, source_code) if name_node else "anonymous"
                entities.append(CodeEntity(
                    name=func_name,
                    entity_type="method" if current_class else "function",
                    file_path=file_path,
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    source=get_node_text(node, source_code),
                    parent_entity=current_class,
                    calls=CallExtractor.extract_calls(node, source_code, "javascript")
                ))
                return

            for child in node.children:
                visit(child, current_class)

        visit(root_node)
        return entities

    # ================= GO =================
    @staticmethod
    def _extract_go_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="function",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code),
                        calls=CallExtractor.extract_calls(node, source_code, "go")
                    ))
            elif node.type == "method_declaration":
                name_node = node.child_by_field_name("name")
                receiver_node = node.child_by_field_name("receiver")
                receiver_name = get_node_text(receiver_node, source_code) if receiver_node else None
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="method",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code),
                        parent_entity=receiver_name,
                        calls=CallExtractor.extract_calls(node, source_code, "go")
                    ))
            elif node.type == "type_spec":
                name_node = node.child_by_field_name("name")
                type_node = node.child_by_field_name("type")
                if name_node and type_node and type_node.type in ("struct_type", "interface_type"):
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
        return entities

    # ================= RUST =================
    @staticmethod
    def _extract_rust_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type == "function_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    parent_impl = None
                    if node.parent and node.parent.parent and node.parent.parent.type == "impl_item":
                        type_node = node.parent.parent.child_by_field_name("type")
                        if type_node:
                            parent_impl = get_node_text(type_node, source_code)

                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="method" if parent_impl else "function",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code),
                        parent_entity=parent_impl,
                        calls=CallExtractor.extract_calls(node, source_code, "rust")
                    ))
            elif node.type in ("struct_item", "enum_item", "trait_item"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
        return entities

    # ================= JAVA & KOTLIN =================
    @staticmethod
    def _extract_java_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type in ("class_declaration", "interface_declaration", "record_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
            elif node.type in ("method_declaration", "function_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    parent_class = None
                    curr = node.parent
                    while curr:
                        if curr.type in ("class_declaration", "interface_declaration"):
                            p_name = curr.child_by_field_name("name")
                            if p_name:
                                parent_class = get_node_text(p_name, source_code)
                            break
                        curr = curr.parent

                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="method" if parent_class else "function",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code),
                        parent_entity=parent_class,
                        calls=CallExtractor.extract_calls(node, source_code, "java")
                    ))
        return entities

    # ================= C & C++ =================
    @staticmethod
    def _extract_cpp_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type in ("class_specifier", "struct_specifier"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
            elif node.type == "function_definition":
                declarator = node.child_by_field_name("declarator")
                func_name = "func"
                if declarator:
                    func_name = get_node_text(declarator, source_code).split("(")[0].strip()
                entities.append(CodeEntity(
                    name=func_name,
                    entity_type="function",
                    file_path=file_path,
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    source=get_node_text(node, source_code),
                    calls=CallExtractor.extract_calls(node, source_code, "cpp")
                ))
        return entities

    # ================= C# =================
    @staticmethod
    def _extract_csharp_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type in ("class_declaration", "struct_declaration", "interface_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
            elif node.type == "method_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="method",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code),
                        calls=CallExtractor.extract_calls(node, source_code, "c_sharp")
                    ))
        return entities

    # ================= PHP =================
    @staticmethod
    def _extract_php_entities(root_node: Node, source_code: str, file_path: str) -> List[CodeEntity]:
        entities: List[CodeEntity] = []
        for node in traverse_tree(root_node):
            if node.type in ("class_declaration", "interface_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="class",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
            elif node.type in ("method_declaration", "function_definition"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entities.append(CodeEntity(
                        name=get_node_text(name_node, source_code),
                        entity_type="method" if node.type == "method_declaration" else "function",
                        file_path=file_path,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=get_node_text(node, source_code)
                    ))
        return entities

    # ================= UNIVERSAL HEURISTIC FALLBACK (ANY LANGUAGE) =================
    @staticmethod
    def _extract_generic_entities(source_code: str, file_path: str, language: str) -> List[CodeEntity]:
        """
        Universal heuristic regex & signature extractor that parses classes and functions
        from Ruby, Swift, Dart, Scala, Lua, Perl, Shell, SQL, Julia, Elixir, etc.
        """
        entities: List[CodeEntity] = []
        lines = source_code.splitlines()

        class_pattern = re.compile(r"^\s*(?:class|struct|interface|type|module|trait|enum)\s+([a-zA-Z0-9_]+)", re.MULTILINE)
        func_pattern = re.compile(r"^\s*(?:def|func|fn|function|sub|procedure|fun|task)\s+([a-zA-Z0-9_]+)", re.MULTILINE)

        for idx, line in enumerate(lines, start=1):
            c_match = class_pattern.search(line)
            if c_match:
                name = c_match.group(1)
                end = min(len(lines), idx + 30)
                entities.append(CodeEntity(
                    name=name,
                    entity_type="class",
                    file_path=file_path,
                    start_line=idx,
                    end_line=end,
                    source="\n".join(lines[idx - 1:end])
                ))
                continue

            f_match = func_pattern.search(line)
            if f_match:
                name = f_match.group(1)
                end = min(len(lines), idx + 25)
                entities.append(CodeEntity(
                    name=name,
                    entity_type="function",
                    file_path=file_path,
                    start_line=idx,
                    end_line=end,
                    source="\n".join(lines[idx - 1:end])
                ))

        return entities
