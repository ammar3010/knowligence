from abc import ABC, abstractmethod

from app.models.documents import Document


class BaseDocumentLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> Document:
        """
        Load a source and convert it into a normalized Document.
        """
        raise NotImplementedError