from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Union


class BaseChunker(ABC):
    """
    Abstract base class for implementing different text chunking strategies.

    All concrete chunker implementations should inherit from this class
    and override the `chunk` method to define their chunking logic.
    """

    @abstractmethod
    def chunk(
        self,
        text: str,
        doc_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Union[str, dict]]]:
        """
        Splits the input text into smaller chunks.

        Parameters
        ----------
        text : str
            The full input text to be chunked.

        doc_metadata : Optional[Dict], optional
            Metadata to associate with each chunk (e.g., source, doc_id), by default None.

        Returns
        -------
        List[Dict[str, Union[str, dict]]]
            A list of chunk dictionaries, each containing:
            - "text": the chunked text
            - "metadata": the chunk-specific metadata (optional)
        """
        pass
