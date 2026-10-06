import hashlib
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.graph.repository import GraphRepository
from app.ingestion.service import IngestionService
from app.models.documents import DocumentType
from app.models.ingestion import DocumentInfo, IngestResponse
from app.vectorstore.client import qdrant_client


router = APIRouter(
    prefix="/api/v1",
    tags=["ingestion"],
)

ingestion_service = IngestionService()
graph_repository = GraphRepository()


ALLOWED_EXTENSIONS = {
    ".pdf": DocumentType.PDF,
    ".txt": DocumentType.TEXT,
    ".md": DocumentType.MARKDOWN,
    ".csv": DocumentType.CSV,
}


@router.post(
    "/ingest",
    response_model=IngestResponse,
)
async def ingest_file(
    file: UploadFile = File(...),
):
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported types: PDF, TXT, MD, CSV."
            ),
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    document_id = hashlib.sha256(content).hexdigest()
    document_type = ALLOWED_EXTENSIONS[extension]

    document, chunks = ingestion_service.load_and_chunk_file(
        content=content,
        filename=filename,
        document_id=document_id,
        document_type=document_type,
    )

    chunk_count = ingestion_service.ingest(
        document=document,
        chunks=chunks,
    )

    return IngestResponse(
        document_id=document.id,
        filename=filename,
        source_type=document_type.value,
        chunks_indexed=chunk_count,
        message="Document successfully ingested.",
    )


@router.get(
    "/documents",
    response_model=list[DocumentInfo],
)
def list_documents():
    return graph_repository.list_documents()


@router.delete(
    "/documents/{document_id}",
)
def delete_document(document_id: str):
    graph_repository.delete_document(document_id)
    qdrant_client.delete_document(document_id)

    return {
        "document_id": document_id,
        "message": "Document deleted.",
    }