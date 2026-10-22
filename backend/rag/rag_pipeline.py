from typing import Any, Dict, Generator, List, Optional
from backend.vectorstore.retriever import HybridRetriever
from backend.rag.query_analyzer import QueryAnalyzer
from backend.rag.context_builder import ContextBuilder
from backend.rag.prompt_builder import PromptBuilder
from backend.analysis.impact_analysis import ImpactAnalysisService
from backend.models.repository_index import RepositoryIndex
from backend.utils.logging import logger

class RAGPipeline:
    def __init__(
        self,
        retriever: HybridRetriever,
        llm_client: Any,
        index: Optional[RepositoryIndex] = None
    ):
        self.retriever = retriever
        self.llm_client = llm_client
        self.index = index
        self.impact_service = ImpactAnalysisService(index) if index else None

    def query(
        self,
        user_query: str,
        top_k: int = 5,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute complete RAG question answering."""
        analysis = QueryAnalyzer.analyze(user_query)
        intent = analysis["primary_intent"]

        # Retrieve relevant code chunks
        retrieved_chunks = self.retriever.retrieve(user_query, top_k=top_k)

        # Structural graph context if relevant
        extra_graph_info = None
        if self.impact_service and analysis["mentioned_symbols"]:
            target_sym = analysis["mentioned_symbols"][0]
            extra_graph_info = self.impact_service.analyze_impact(target_sym, max_depth=2)

        # Build context & prompt
        context_str = ContextBuilder.build_context(retrieved_chunks, extra_graph_info)
        user_prompt = PromptBuilder.build_user_prompt(user_query, context_str, intent)

        # Generate response
        response_text = self.llm_client.generate(
            user_prompt,
            system=PromptBuilder.SYSTEM_PROMPT,
            model=model,
            provider=provider,
            api_key=api_key
        )

        # Prepare citations
        citations = []
        for chunk, score, prov in retrieved_chunks:
            citations.append({
                "file": chunk.relative_path,
                "lines": f"{chunk.start_line}-{chunk.end_line}",
                "entity": chunk.entity_name or "file",
                "type": chunk.entity_type,
                "provenance": prov,
            })

        return {
            "query": user_query,
            "intent": intent,
            "answer": response_text,
            "citations": citations,
            "total_chunks_retrieved": len(retrieved_chunks),
            "graph_context": extra_graph_info,
        }

    def stream_query(
        self,
        user_query: str,
        top_k: int = 5,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Stream RAG answer token-by-token."""
        analysis = QueryAnalyzer.analyze(user_query)
        intent = analysis["primary_intent"]

        retrieved_chunks = self.retriever.retrieve(user_query, top_k=top_k)

        extra_graph_info = None
        if self.impact_service and analysis["mentioned_symbols"]:
            target_sym = analysis["mentioned_symbols"][0]
            extra_graph_info = self.impact_service.analyze_impact(target_sym, max_depth=2)

        context_str = ContextBuilder.build_context(retrieved_chunks, extra_graph_info)
        user_prompt = PromptBuilder.build_user_prompt(user_query, context_str, intent)

        # Send initial metadata event
        citations = [
            {
                "file": c.relative_path,
                "lines": f"{c.start_line}-{c.end_line}",
                "entity": c.entity_name or "file",
                "type": c.entity_type,
            }
            for c, s, p in retrieved_chunks
        ]
        yield {"type": "metadata", "intent": intent, "citations": citations}

        # Stream tokens
        for token in self.llm_client.stream_generate(
            user_prompt,
            system=PromptBuilder.SYSTEM_PROMPT,
            model=model,
            provider=provider,
            api_key=api_key
        ):
            yield {"type": "token", "content": token}

        yield {"type": "done"}
