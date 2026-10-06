import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.response import QueryRequest
from app.workflows.stream import stream_query


router = APIRouter(
    prefix="/api/v1",
    tags=["query"],
)


@router.post("/query")
def query(request: QueryRequest):

    def event_stream():
        for event in stream_query(
            query=request.query,
            chat_history=request.chat_history,
        ):
            yield (
                f"event: {event['type']}\n"
                f"data: {json.dumps(event)}\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )