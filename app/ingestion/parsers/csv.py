from pathlib import Path

import pandas as pd

from app.ingestion.loader import BaseDocumentLoader
from app.models.documents import Document, DocumentType
from app.utilities.ids import generate_id


class CSVDocumentLoader(BaseDocumentLoader):

    def load(self, source: str) -> Document:
        path = Path(source)

        dataframe = pd.read_csv(path)

        content = dataframe.to_csv(
            index=False
        )

        return Document(
            id=generate_id("doc"),
            title=path.stem,
            source=str(path.absolute()),
            source_type=DocumentType.CSV,
            content=content,
            metadata={
                "filename": path.name,
                "extension": path.suffix,
                "rows": len(dataframe),
                "columns": list(dataframe.columns),
            },
        )