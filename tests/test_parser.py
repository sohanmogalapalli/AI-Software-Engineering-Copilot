from backend.parsing.tree_sitter_parser import TreeSitterManager
from backend.parsing.entity_extractor import EntityExtractor
from backend.parsing.import_extractor import ImportExtractor
from backend.parsing.call_extractor import CallExtractor

PYTHON_CODE = '''"""Module docstring."""
import os
from backend.utils import logger

class UserService:
    """Handles user operations."""
    
    @staticmethod
    def get_user(user_id: int):
        """Fetch user by id."""
        logger.info("Fetching user")
        return find_user(user_id)

def standalone_func():
    return True
'''

def test_tree_sitter_python_parsing():
    ts_manager = TreeSitterManager()
    tree = ts_manager.parse(PYTHON_CODE, "python")
    assert tree is not None
    root = tree.root_node
    assert root.type == "module"

    # Test imports
    imports = ImportExtractor.extract_imports(root, PYTHON_CODE, "python")
    assert any("backend.utils" in imp for imp in imports)
    assert any("os" in imp for imp in imports)

    # Test entities
    entities = EntityExtractor.extract_entities(root, PYTHON_CODE, "user_service.py", "python")
    names = [e.name for e in entities]
    assert "UserService" in names
    assert "get_user" in names
    assert "standalone_func" in names

    # Method checks
    get_user_ent = next(e for e in entities if e.name == "get_user")
    assert get_user_ent.entity_type == "method"
    assert get_user_ent.parent_entity == "UserService"
    assert "user_id: int" in get_user_ent.parameters[0]
    assert "@staticmethod" in get_user_ent.decorators
    assert "find_user" in [c.split(".")[-1] for c in get_user_ent.calls]
