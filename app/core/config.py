from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    app_name: str = "GraphRAG Knowledge Intelligence"
    app_version: str = "0.1.0"
    debug: bool = True

    # Groq
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    groq_extraction_model: str = "qwen/qwen3.8-27b"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "knowledge_chunks"

    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Retrieval
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()