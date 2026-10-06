from fastapi import FastAPI
from app.core.config import get_settings
from app.graph.client import neo4j_client
from app.llm.groq import groq_client
from app.vectorstore.client import qdrant_client
from app.api.routes import router as query_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(query_router)

@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "services": {
            "groq": groq_client.verify_connection(),
            "neo4j": neo4j_client.verify_connection(),
            "qdrant": qdrant_client.verify_connection(),
        },
    }