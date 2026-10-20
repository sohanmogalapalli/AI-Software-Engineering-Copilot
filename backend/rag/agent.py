import json
import re
from typing import Any, Dict, List, Optional
from pathlib import Path

from backend.models.repository_index import RepositoryIndex
from backend.vectorstore.retriever import HybridRetriever
from backend.analysis.call_graph import CallGraphService
from backend.analysis.dependency_graph import DependencyGraphService
from backend.analysis.impact_analysis import ImpactAnalysisService
from backend.llm.ollama_client import OllamaClient
from backend.utils.file_utils import read_file_content
from backend.utils.logging import logger

class CopilotAgent:
    """
    Autonomous multi-step ReAct agent that inspects code, follows function calls,
    checks dependencies, and solves complex codebase queries with repository grounding.
    """
    def __init__(
        self,
        retriever: HybridRetriever,
        llm_client: OllamaClient,
        index: RepositoryIndex
    ):
        self.retriever = retriever
        self.llm_client = llm_client
        self.index = index
        self.call_service = CallGraphService(index)
        self.dep_service = DependencyGraphService(index)
        self.impact_service = ImpactAnalysisService(index)

    def execute_tool(self, tool_name: str, argument: str) -> str:
        """Execute one of the registered agent tools."""
        clean_arg = argument.strip("'\" \t\r\n")
        try:
            if tool_name == "search_code":
                chunks = self.retriever.retrieve(clean_arg, top_k=5)
                if not chunks:
                    return "No matching code found."
                res = []
                for c, s, prov in chunks:
                    res.append(f"File `{c.relative_path}` ({c.start_line}-{c.end_line}) [{c.entity_type} {c.entity_name}]:\n{c.content[:1000]}")
                return "\n---\n".join(res)

            elif tool_name == "get_symbol_callers":
                callers = self.call_service.get_callers(clean_arg)
                if not callers:
                    return f"No callers found for '{clean_arg}'."
                return json.dumps(callers[:8], indent=2)

            elif tool_name == "get_dependencies":
                deps = self.dep_service.get_dependencies(clean_arg)
                return f"Dependencies of `{clean_arg}`: {', '.join(deps) if deps else 'None'}"

            elif tool_name == "get_impact":
                impact = self.impact_service.analyze_impact(clean_arg)
                return f"Risk Level: {impact['risk_level']}. Blast radius score: {impact['blast_radius_score']}. Affected files: {', '.join(impact['all_affected_files'])}"

            elif tool_name == "read_file":
                parts = clean_arg.split(":")
                file_rel = parts[0]
                full_path = Path(self.index.repository_path) / file_rel
                content = read_file_content(full_path)
                if not content:
                    # Try matching relative to repository
                    for f in self.index.files.keys():
                        if file_rel in f:
                            content = read_file_content(Path(self.index.repository_path) / f)
                            break
                if not content:
                    return f"Could not read `{file_rel}`"

                lines = content.splitlines()
                if len(parts) > 1 and "-" in parts[1]:
                    s, e = map(int, parts[1].split("-"))
                    return "\n".join(lines[max(0, s-1):e])
                return "\n".join(lines[:120])

            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Tool execution error: {e}"

    def run(self, user_query: str, max_steps: int = 3) -> Dict[str, Any]:
        """Run grounded multi-step reasoning loop."""
        tools_desc = """Available Tools:
1. search_code[query] - Searches codebase using hybrid search.
2. get_symbol_callers[symbol_name] - Finds functions calling this symbol.
3. get_dependencies[file_path] - Finds files imported by this file.
4. get_impact[file_or_symbol] - Calculates change blast radius.
5. read_file[file_path:start-end] - Reads specific file lines (e.g. backend/main.py:1-50).
"""
        agent_system = f"""You are an expert AI Software Engineering Agent analyzing the repository '{self.index.name}'.
Answer the user's question thoroughly and ground your reasoning in the actual repository files, architecture, and code.

CRITICAL RULES:
1. NEVER guess or invent a generic story (e.g. claiming it is a simple user management app when it is an enterprise AI memory platform).
2. Base your explanation strictly on the provided repository observations and tool results.
3. If the user asks for a project overview ('tell me full about the project', 'what does this do'), explain the real project purpose, database/backend architecture, key features, and major components.
4. When stating your final answer, prefix it with 'Final Answer:' and include exact file references.

{tools_desc}

Format for steps:
Thought: What specific files or concepts do I need to inspect next?
Action: tool_name[argument]
Observation: (tool output will appear here)
Final Answer: Complete, detailed, grounded response.
"""
        # Step 0: Seed with ground-truth repository retrieval
        initial_chunks = self.retriever.retrieve(user_query, top_k=6)
        initial_obs = []
        for c, s, prov in initial_chunks:
            initial_obs.append(f"File `{c.relative_path}` ({c.start_line}-{c.end_line}) [{c.entity_type} {c.entity_name}]:\n{c.content[:1000]}")
        initial_context = "\n---\n".join(initial_obs)

        conversation_history = (
            f"User Question: {user_query}\n\n"
            f"Initial Ground-Truth Repository Context:\n{initial_context}\n"
        )
        steps_log = [{"step": 1, "action": "Initial Repository Retrieval", "observation": f"Retrieved {len(initial_chunks)} relevant code & documentation chunks"}]

        for step in range(max_steps):
            prompt = f"{conversation_history}\nThought:"
            step_output = self.llm_client.generate(prompt, system=agent_system, temperature=0.1)

            # Check if agent produced Final Answer
            if "Final Answer:" in step_output:
                final_answer = step_output.split("Final Answer:")[-1].strip()
                steps_log.append({"step": step + 2, "thought": step_output, "action": "Synthesize Grounded Answer"})
                return {
                    "query": user_query,
                    "final_answer": final_answer,
                    "steps": steps_log
                }

            # Check for Action: tool_name[arg]
            match = re.search(r"Action:\s*([a-zA-Z_]+)\[(.*?)\]", step_output, re.DOTALL)
            if match:
                tool_name = match.group(1).strip()
                tool_arg = match.group(2).strip()
                observation = self.execute_tool(tool_name, tool_arg)

                steps_log.append({
                    "step": step + 2,
                    "thought": step_output,
                    "tool": tool_name,
                    "argument": tool_arg,
                    "observation": observation[:500]
                })

                conversation_history += f"\nThought: {step_output}\nObservation: {observation}\n"
            else:
                # If no tool call, finalize answer
                steps_log.append({"step": step + 2, "thought": "Final Analysis", "action": "Final Answer"})
                return {
                    "query": user_query,
                    "final_answer": step_output,
                    "steps": steps_log
                }

        # If loop reached max steps, synthesize final answer
        summary_prompt = f"{conversation_history}\nBased on all real observations above, produce your comprehensive Final Answer:\nFinal Answer:"
        final_answer = self.llm_client.generate(summary_prompt, system=agent_system, temperature=0.1)
        return {
            "query": user_query,
            "final_answer": final_answer,
            "steps": steps_log
        }
