from neo4j import Driver, GraphDatabase

from app.core.config import get_settings


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
            return False

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ):
        with self.driver.session() as session:
            result = session.run(
                query,
                parameters or {},
            )

            return result.data()

    def close(self) -> None:
        self.driver.close()


neo4j_client = Neo4jClient()