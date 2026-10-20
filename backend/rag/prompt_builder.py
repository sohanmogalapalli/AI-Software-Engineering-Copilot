import re

class PromptBuilder:
    SYSTEM_PROMPT = """You are an expert AI Software Engineering Copilot specializing in large-scale codebase understanding, debugging, architectural analysis, and change impact reasoning.

Follow these strict rules:
1. Base your answer strictly on the provided repository code context and structural relationships.
2. ALWAYS cite exact file paths and line numbers when referencing code (e.g., `NeuroVault-main/backend/app/main.py:10-45`).
3. NEVER fabricate or hallucinate generic descriptions (e.g., never claim an AI memory platform is a simple user management app). Read the actual project documents and code provided.
4. If the user asks for a project overview or to 'tell me full about the project', provide a comprehensive breakdown covering:
   - What the platform/project actually is
   - Core architecture & technology stack (backend, frontend, database, AI components)
   - Key features, algorithms, or mechanics
   - Major files and module organization
5. If the provided context is insufficient to answer the question with certainty, clearly state what information is missing.
6. Be direct, crisp, and concise. Avoid conversational filler, disclaimers, or excessive boilerplate so your response is fast and immediately actionable.
"""

    @staticmethod
    def build_user_prompt(query: str, context: str, intent: str = "GENERAL") -> str:
        intent_instruction = ""
        q_lower = query.lower()
        if any(w in q_lower for w in ["tell me", "about the project", "overview", "what is this", "what does this do"]):
            intent_instruction = "Provide a comprehensive, deep-dive architectural and functional overview of this project based on its documentation, tech stack, and code."
        elif intent == "DEBUG":
            intent_instruction = "Diagnose the root cause of the error or bug based on the code logic and explain the exact fix."
        elif intent == "EXPLAIN":
            intent_instruction = "Explain the architecture, design patterns, control flow, and purpose of the code."
        elif intent == "SEARCH":
            intent_instruction = "Identify the exact files, classes, and functions responsible and explain how they connect."
        elif intent == "IMPACT":
            intent_instruction = "Analyze downstream consequences, breaking changes, and files that require testing."

        return f"""{context}

---
USER QUESTION: {query}
SPECIAL INSTRUCTION: {intent_instruction}

Answer thoroughly and ground every claim in the repository context:"""
