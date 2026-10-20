import hashlib
from typing import List, Optional
from backend.models.chunk import CodeChunk
from backend.models.code_file import CodeFile
from backend.models.repository_index import RepositoryIndex
from backend.utils.logging import logger

MAX_CHUNK_LINES = 120

class ContextEnrichedChunker:
    """
    Produces context-enriched, hierarchical code chunks.
    Prepend breadcrumbs (file path, scope, signatures, imports) to preserve
    semantic context for embedding models and LLMs.
    """
    
    @staticmethod
    def chunk_repository(index: RepositoryIndex) -> List[CodeChunk]:
        all_chunks: List[CodeChunk] = []
        for rel_path, code_file in index.files.items():
            file_chunks = ContextEnrichedChunker.chunk_file(code_file)
            all_chunks.extend(file_chunks)
        logger.info(f"Generated {len(all_chunks)} context-enriched chunks from {len(index.files)} files.")
        return all_chunks

    @staticmethod
    def chunk_file(code_file: CodeFile) -> List[CodeChunk]:
        chunks: List[CodeChunk] = []

        # 1. Module Overview Chunk
        classes_summary = [c.name for c in code_file.classes]
        funcs_summary = [f.name for f in code_file.functions if not f.parent_entity]
        
        overview_lines = [
            f"# File: {code_file.relative_path}",
            f"# Language: {code_file.language}",
            f"# Lines: 1-{code_file.line_count}",
            f"# Defined Classes: {', '.join(classes_summary) if classes_summary else 'None'}",
            f"# Defined Functions: {', '.join(funcs_summary) if funcs_summary else 'None'}",
            f"# Imported Modules: {', '.join(code_file.imports[:10]) if code_file.imports else 'None'}",
        ]
        enriched_overview = "\n".join(overview_lines)

        chunk_id = hashlib.sha256(f"{code_file.relative_path}:overview".encode()).hexdigest()[:16]
        chunks.append(CodeChunk(
            chunk_id=chunk_id,
            file_path=code_file.path,
            relative_path=code_file.relative_path,
            language=code_file.language,
            entity_name=None,
            entity_type="module_overview",
            start_line=1,
            end_line=min(code_file.line_count, 40),
            content=enriched_overview,
            enriched_content=enriched_overview,
            docstring=None,
            imports=code_file.imports,
            calls=code_file.all_calls
        ))

        # 2. Entity Chunks (Classes, Functions, Methods)
        for entity in code_file.entities:
            header_lines = [
                f"# File: {code_file.relative_path}",
                f"# Symbol: {entity.qualified_name} ({entity.entity_type})",
                f"# Lines: {entity.start_line}-{entity.end_line}",
            ]
            if entity.parent_entity:
                header_lines.append(f"# Class Scope: {entity.parent_entity}")
            if entity.decorators:
                header_lines.append(f"# Decorators: {', '.join(entity.decorators)}")
            if entity.docstring:
                clean_doc = entity.docstring.replace("\n", " ").strip()
                header_lines.append(f"# Docstring: {clean_doc[:200]}")
            if code_file.imports:
                header_lines.append(f"# Context Imports: {', '.join(code_file.imports[:6])}")

            header_text = "\n".join(header_lines)

            # If the entity is excessively large, break it into windowed sub-chunks
            source_lines = entity.source.splitlines()
            if len(source_lines) > MAX_CHUNK_LINES:
                stride = MAX_CHUNK_LINES - 20
                for start_idx in range(0, len(source_lines), stride):
                    end_idx = min(start_idx + MAX_CHUNK_LINES, len(source_lines))
                    sub_source = "\n".join(source_lines[start_idx:end_idx])
                    actual_start = entity.start_line + start_idx
                    actual_end = entity.start_line + end_idx - 1

                    sub_header = f"{header_text}\n# Part: lines {actual_start}-{actual_end}"
                    enriched_sub = f"{sub_header}\n\n{sub_source}"
                    
                    sub_id = hashlib.sha256(f"{code_file.relative_path}:{entity.qualified_name}:{actual_start}".encode()).hexdigest()[:16]
                    chunks.append(CodeChunk(
                        chunk_id=sub_id,
                        file_path=code_file.path,
                        relative_path=code_file.relative_path,
                        language=code_file.language,
                        entity_name=entity.name,
                        entity_type=entity.entity_type,
                        start_line=actual_start,
                        end_line=actual_end,
                        content=sub_source,
                        enriched_content=enriched_sub,
                        docstring=entity.docstring,
                        imports=code_file.imports,
                        calls=entity.calls
                    ))
            else:
                enriched_text = f"{header_text}\n\n{entity.source}"
                cid = hashlib.sha256(f"{code_file.relative_path}:{entity.qualified_name}:{entity.start_line}".encode()).hexdigest()[:16]
                chunks.append(CodeChunk(
                    chunk_id=cid,
                    file_path=code_file.path,
                    relative_path=code_file.relative_path,
                    language=code_file.language,
                    entity_name=entity.name,
                    entity_type=entity.entity_type,
                    start_line=entity.start_line,
                    end_line=entity.end_line,
                    content=entity.source,
                    enriched_content=enriched_text,
                    docstring=entity.docstring,
                    imports=code_file.imports,
                    calls=entity.calls
                ))

        return chunks
