import logging
from typing import List, Dict, Union, Optional
from app.services.chunking.base_chunker import BaseChunker

logger = logging.getLogger(__name__)

class ChunkingService:
    """
    A high-level service to chunk text using the injected BaseChunker strategy.
    """

    def __init__(self, chunker: BaseChunker):
        """
        Initialize with a specific chunker strategy.

        Parameters
        ----------
        chunker : BaseChunker
            The chunker strategy to use.
        """
        self.chunker = chunker
        logger.info(f"ChunkingService initialized with chunker: {self.chunker.__class__.__name__}")

    def chunk_text(self, text: str, doc_metadata: Optional[Dict] = None) -> List[Dict[str, Union[str, dict]]]:
        """
        Chunk the input text using the configured strategy.

        Parameters
        ----------
        text : str
            The text to chunk.
        doc_metadata : Optional[Dict], optional
            Optional metadata to include in each chunk.

        Returns
        -------
        List[Dict[str, Union[str, dict]]]
            The chunked result.
        """
        logger.info("Starting text chunking process...")
        logger.debug(f"Text length: {len(text)} characters")
        if doc_metadata:
            logger.debug(f"Document metadata provided: {doc_metadata}")

        chunks = self.chunker.chunk(text, doc_metadata=doc_metadata)

        logger.info(f"Text chunking complete. Generated {len(chunks)} chunks.")
        return chunks
