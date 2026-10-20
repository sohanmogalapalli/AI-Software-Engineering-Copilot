import re
from typing import Dict, Any

class QueryAnalyzer:
    INTENT_KEYWORDS = {
        "DEBUG": ["error", "bug", "crash", "exception", "traceback", "fail", "broken", "fix", "why is", "500", "401", "404"],
        "EXPLAIN": ["explain", "understand", "what does", "how does", "walkthrough", "overview", "describe"],
        "SEARCH": ["where is", "find", "locate", "which file", "search for", "how to find"],
        "DEPENDENCY": ["depend", "import", "require", "who imports", "relationship", "downstream"],
        "IMPACT": ["impact", "what breaks", "blast radius", "change", "modify", "affect", "side effect"],
    }

    @staticmethod
    def analyze(query: str) -> Dict[str, Any]:
        """Classify user query and extract key symbols and intents."""
        q_lower = query.lower()
        matched_intents = []

        for intent, kws in QueryAnalyzer.INTENT_KEYWORDS.items():
            if any(kw in q_lower for kw in kws):
                matched_intents.append(intent)

        primary_intent = matched_intents[0] if matched_intents else "GENERAL"

        # Extract possible symbols or paths mentioned in quotes or backticks
        mentioned_symbols = re.findall(r"[`'\"]([a-zA-Z0-9_\.\/\-]+)[`'\"]", query)

        return {
            "query": query,
            "primary_intent": primary_intent,
            "all_intents": matched_intents,
            "mentioned_symbols": mentioned_symbols,
        }
