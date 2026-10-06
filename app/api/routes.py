from fastapi import APIRouter

from app.models.response import GraphRAGResponse, QueryRequest
from app.workflows.graph import graph

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post("/query", response_model=GraphRAGResponse)
def query(request: QueryRequest) -> GraphRAGResponse:
    result = graph.invoke(
        {
            "query": request.query,
            "chat_history": request.chat_history,
        }
    )

    return GraphRAGResponse(
        answer=result["answer"],
        entities=result.get("entities", []),
        sources=result.get("sources", []),
        graph_paths=result.get("graph_paths", []),
    )