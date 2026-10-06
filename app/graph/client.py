import logging

from neo4j import Driver, GraphDatabase

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class Neo4jClient:
    def __init__(self) -> None:
        settings = get_settings()

        self.driver: Driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
        )

    def verify_connection(self) -> bool:
        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            logger.exception("Neo4j connectivity check failed")
            return False

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ):
        try:
            with self.driver.session() as session:
                result = session.run(
                    query,
                    parameters or {},
                )

                records = result.data()
                logger.debug("Neo4j query completed: rows=%d", len(records))
                return records
        except Exception:
            logger.exception("Neo4j query execution failed")
            raise

    def close(self) -> None:
        self.driver.close()
        logger.info("Neo4j driver closed")


neo4j_client = Neo4jClient()