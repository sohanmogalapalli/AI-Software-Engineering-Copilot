from typing import Dict, List, Set, Any
from backend.models.repository_index import RepositoryIndex
from backend.analysis.dependency_graph import DependencyGraphService
from backend.analysis.call_graph import CallGraphService

class ImpactAnalysisService:
    def __init__(self, index: RepositoryIndex):
        self.index = index
        self.dep_service = DependencyGraphService(index)
        self.call_service = CallGraphService(index)

    def analyze_impact(self, target: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Analyze the change blast radius for a target file or symbol.
        target can be a file path (e.g. "backend/auth.py") or symbol (e.g. "authenticate_user").
        """
        # Determine if target is a file or symbol
        is_file = any(target in f or f in target for f in self.index.files.keys())
        
        affected_files: Set[str] = set()
        affected_callers: List[Dict[str, str]] = []
        direct_dependents: List[str] = []
        transitive_dependents: Set[str] = set()

        if is_file:
            # Find the closest matching file key
            matched_file = None
            for f in self.index.files.keys():
                if target == f or target.endswith(f) or f.endswith(target):
                    matched_file = f
                    break
            
            if matched_file:
                direct_dependents = self.dep_service.get_dependents(matched_file)
                transitive_dependents = self.dep_service.get_transitive_dependents(matched_file, max_depth=max_depth)
                affected_files.update(direct_dependents)
                affected_files.update(transitive_dependents)
                affected_files.add(matched_file)
        else:
            # Target is a symbol
            affected_callers = self.call_service.get_callers(target)
            for caller in affected_callers:
                if caller.get("file"):
                    affected_files.add(caller["file"])

        # Identify relevant test files
        suggested_tests: List[str] = []
        for file in self.index.files.keys():
            if "test" in file.lower():
                if file in affected_files or any(aff.split("/")[-1].split(".")[0] in file for aff in affected_files):
                    suggested_tests.append(file)

        # Risk scoring
        impact_count = len(affected_files) + len(affected_callers)
        if impact_count == 0:
            risk_level = "LOW"
            explanation = "Minimal impact detected. No direct dependents or external callers found."
        elif impact_count <= 2:
            risk_level = "LOW"
            explanation = "Low impact. Only isolated dependents or callers identified."
        elif impact_count <= 5:
            risk_level = "MEDIUM"
            explanation = "Medium impact. Several downstream modules or callers depend on this component."
        elif impact_count <= 10:
            risk_level = "HIGH"
            explanation = "High impact. Multiple core modules and external callers may be affected."
        else:
            risk_level = "CRITICAL"
            explanation = "Critical blast radius. This component is a major architecture hub with wide downstream effects."

        return {
            "target": target,
            "is_file": is_file,
            "risk_level": risk_level,
            "explanation": explanation,
            "blast_radius_score": impact_count,
            "direct_dependents": direct_dependents,
            "transitive_dependents": list(transitive_dependents),
            "affected_callers": affected_callers,
            "all_affected_files": sorted(list(affected_files)),
            "suggested_tests": sorted(list(set(suggested_tests))),
        }
