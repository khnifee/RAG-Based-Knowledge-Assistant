import re
import logging
from typing import List, Dict, Union, Optional
from app.services.chunking.base_chunker import BaseChunker

logger = logging.getLogger(__name__)

class SentenceChunker(BaseChunker):
    """
    SentenceChunker splits text into chunks based on a fixed number of sentences,
    with optional overlap between chunks.

    Parameters
    ----------
    chunk_size : int, optional
        Number of sentences per chunk (default is 5).
    overlap : int, optional
        Number of overlapping sentences between chunks (default is 1).
    """

    def __init__(self, chunk_size: int = 5, overlap: int = 1):
        if not isinstance(chunk_size, int) or not isinstance(overlap, int):
            raise TypeError("chunk_size and overlap must be integers.")
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")
        if overlap < 0:
            raise ValueError("overlap cannot be negative.")
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size.")
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        logger.info(f"SentenceChunker initialized with chunk_size={chunk_size}, overlap={overlap}")

    def chunk(self, text: str) -> List[Dict[str, Union[str, dict]]]:
        """
        Splits the input text into chunks of sentences using regex-based sentence boundaries,
        returning each chunk along with metadata.

        Parameters
        ----------
        text : str
            The full text to be chunked.

        Returns
        -------
        List[Dict[str, Union[str, dict]]]
            A list of chunks where each chunk is a dict with keys:
            - "text": the chunk text (str)
            - "metadata": metadata dictionary containing chunk details
        """
        logger.info("Starting sentence-based chunking...")
        if not text.strip():
            logger.warning("Empty or whitespace-only text provided. Returning no chunks.")
            return []

        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        sentences = [s for s in sentences if s]  # Remove empty strings
        logger.debug(f"Extracted {len(sentences)} sentences from input text.")

        chunks = []
        step = self.chunk_size - self.overlap
        for i in range(0, len(sentences), step):
            chunk_sentences = sentences[i:i + self.chunk_size]
            if not chunk_sentences:
                logger.debug(f"Skipping empty chunk at index {i}.")
                continue

            chunk_text = " ".join(chunk_sentences)
            metadata = {
                "chunk_index": i // step,
                "start_sentence": i,
                "end_sentence": i + len(chunk_sentences) - 1,
                "num_sentences": len(chunk_sentences)
            }
            chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })
            logger.debug(f"Created chunk {metadata['chunk_index']} with {metadata['num_sentences']} sentences.")

        logger.info(f"Completed chunking. Total chunks created: {len(chunks)}.")
        return chunks
