from backend.rag.query_analyzer import QueryAnalyzer
from backend.rag.prompt_builder import PromptBuilder
from backend.rag.context_builder import ContextBuilder

def test_query_analyzer():
    res1 = QueryAnalyzer.analyze("Why is the login function throwing an exception?")
    assert res1["primary_intent"] == "DEBUG"

    res2 = QueryAnalyzer.analyze("Where is the JWT token created?")
    assert res2["primary_intent"] == "SEARCH"

    res3 = QueryAnalyzer.analyze("What will break if I change `UserService`?")
    assert res3["primary_intent"] == "IMPACT"
    assert "UserService" in res3["mentioned_symbols"]

def test_prompt_builder():
    prompt = PromptBuilder.build_user_prompt("Where is auth?", "context here", "SEARCH")
    assert "context here" in prompt
    assert "Where is auth?" in prompt
    assert "Identify the exact files" in prompt
