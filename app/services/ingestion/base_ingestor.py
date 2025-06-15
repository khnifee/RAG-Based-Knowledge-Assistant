"""
Base Ingestor Interface

Defines the abstract interface for all document ingestors.
Each ingestor should implement the `load_documents` method
that returns document names and their extracted content.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseIngestor(ABC):
    """
    Abstract base class for document ingestors.
    
    All custom ingestors (e.g., PDFIngestor, TXTIngestor) should inherit from this class
    and implement the `load_documents` method.
    """

    @abstractmethod
    def load_documents(self) -> List[Tuple[str, str]]:
        """
        Load and extract documents from a given source.

        Returns:
            List[Tuple[str, str]]: A list of (document_name, document_text) tuples.
        """
        pass
