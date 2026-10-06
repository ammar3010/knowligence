import logging
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()

from fastapi import FastAPI

from app.graph.client import neo4j_client
from app.llm.groq import groq_client
from app.vectorstore.client import qdrant_client
from app.api.routes import router as query_router

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Application starting: name=%s version=%s", settings.app_name, settings.app_version)
    try:
        yield
    finally:
        neo4j_client.close()
        qdrant_client.close()
        logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(query_router)

@app.get("/")
def root():
    logger.debug("Root endpoint requested")
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
def health():
    logger.debug("Health check started")
    services = {
        "groq": groq_client.verify_connection(),
        "neo4j": neo4j_client.verify_connection(),
        "qdrant": qdrant_client.verify_connection(),
    }
    logger.info(
        "Health check completed: healthy_services=%d total_services=%d services=%s",
        sum(services.values()),
        len(services),
        services,
    )
    return {
        "status": "healthy",
        "services": services,
    }