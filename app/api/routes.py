import logging
from time import perf_counter

from fastapi import APIRouter

from app.models.response import GraphRAGResponse, QueryRequest
from app.workflows.graph import graph

router = APIRouter(prefix="/api/v1", tags=["query"])
logger = logging.getLogger(__name__)


@router.post("/query", response_model=GraphRAGResponse)
def query(request: QueryRequest) -> GraphRAGResponse:
    started_at = perf_counter()
    logger.info("Query request started: history_messages=%d", len(request.chat_history))
    try:
        result = graph.invoke(
            {
                "query": request.query,
                "chat_history": request.chat_history,
            }
        )
    except Exception:
        logger.exception("Query request failed")
        raise

    logger.info(
        "Query request completed: sources=%d graph_paths=%d duration_ms=%.1f",
        len(result.get("sources", [])),
        len(result.get("graph_paths", [])),
        (perf_counter() - started_at) * 1000,
    )

    return GraphRAGResponse(
        answer=result["answer"],
        entities=result.get("entities", []),
        sources=result.get("sources", []),
        graph_paths=result.get("graph_paths", []),
    )