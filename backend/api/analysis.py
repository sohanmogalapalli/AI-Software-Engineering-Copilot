from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from backend.api.state import app_state
from backend.analysis.dependency_graph import DependencyGraphService
from backend.analysis.call_graph import CallGraphService
from backend.analysis.impact_analysis import ImpactAnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

class ImpactRequest(BaseModel):
    target: str = Field(description="File path or symbol name being modified")
    max_depth: int = Field(default=3, description="Depth of transitive graph traversal")

@router.get("/dependencies")
def get_dependencies_graph():
    if not app_state.index:
        raise HTTPException(status_code=400, detail="Repository not indexed yet.")

    dep_service = DependencyGraphService(app_state.index)
    nodes = []
    for node, data in dep_service.graph.nodes(data=True):
        nodes.append({"id": node, **data})

    edges = []
    for src, dst in dep_service.graph.edges():
        edges.append({"source": src, "target": dst})

    circular = dep_service.find_circular_dependencies()
    central = dep_service.get_central_files(top_k=8)

    return {
        "nodes": nodes,
        "edges": edges,
        "circular_dependencies": circular,
        "central_hubs": [{"file": f, "pagerank": round(r, 4)} for f, r in central]
    }

@router.get("/callers")
def get_symbol_callers(symbol: str = Query(description="Function or method name")):
    if not app_state.index:
        raise HTTPException(status_code=400, detail="Repository not indexed yet.")

    call_service = CallGraphService(app_state.index)
    return {"symbol": symbol, "callers": call_service.get_callers(symbol)}

@router.get("/callees")
def get_symbol_callees(symbol: str = Query(description="Function or method name")):
    if not app_state.index:
        raise HTTPException(status_code=400, detail="Repository not indexed yet.")

    call_service = CallGraphService(app_state.index)
    return {"symbol": symbol, "callees": call_service.get_callees(symbol)}

@router.post("/impact")
def analyze_change_impact(request: ImpactRequest):
    if not app_state.index:
        raise HTTPException(status_code=400, detail="Repository not indexed yet.")

    impact_service = ImpactAnalysisService(app_state.index)
    return impact_service.analyze_impact(request.target, max_depth=request.max_depth)
