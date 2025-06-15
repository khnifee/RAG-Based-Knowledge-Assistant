import logging
from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

class WordChunker:
    """
    WordChunker splits text into chunks based on a fixed number of words,
    with optional overlap between consecutive chunks.

    Each chunk is returned along with detailed metadata, including 
    chunk position info and optionally document-level metadata.

    Parameters
    ----------
    chunk_size : int, optional
        Number of words per chunk (default is 150).
    overlap : int, optional
        Number of overlapping words between chunks (default is 30).

    Methods
    -------
    chunk(text: str, doc_metadata: Optional[Dict] = None) -> List[Dict]
        Splits the input text into chunks and returns a list of dictionaries,
        each containing the chunk text and associated metadata.
    """

    def __init__(self, chunk_size: int = 150, overlap: int = 30):
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size.")
        self.chunk_size = chunk_size
        self.overlap = overlap
        logger.info(f"WordChunker initialized with chunk_size={chunk_size}, overlap={overlap}")

    def chunk(self, text: str, doc_metadata: Optional[Dict] = None) -> List[Dict[str, Union[str, dict]]]:
        """
        Splits the input text into word-based chunks with optional overlap,
        returning each chunk along with metadata.

        Parameters
        ----------
        text : str
            The input text to be chunked.
        doc_metadata : dict, optional
            Optional dictionary of metadata related to the whole document.
            These metadata entries will be merged into each chunk's metadata.

        Returns
        -------
        List[Dict]
            A list where each element is a dictionary with keys:
                - "text": the chunk text (str)
                - "metadata": a dictionary containing:
                    - chunk_index (int): Index of the chunk (0-based)
                    - start_word (int): Start word index of the chunk in the document
                    - end_word (int): End word index of the chunk in the document
                    - word_count (int): Number of words in the chunk
                    - char_count (int): Number of characters in the chunk
                    - any keys from doc_metadata, if provided
        """
        logger.info("Starting word-based chunking...")

        words = text.split()
        total_words = len(words)

        if total_words == 0:
            logger.warning("No words found in input text. Returning no chunks.")
            return []

        logger.debug(f"Total words in input text: {total_words}")

        chunks_with_metadata = []
        step = self.chunk_size - self.overlap

        for i, start_idx in enumerate(range(0, total_words, step)):
            chunk_words = words[start_idx: start_idx + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            metadata = {
                "chunk_index": i,
                "start_word": start_idx,
                "end_word": min(start_idx + self.chunk_size - 1, total_words - 1),
                "word_count": len(chunk_words),
                "char_count": len(chunk_text),
            }

            if doc_metadata:
                metadata.update(doc_metadata)

            chunks_with_metadata.append({
                "text": chunk_text,
                "metadata": metadata
            })

            logger.debug(f"Created chunk {i} with {len(chunk_words)} words.")

            if start_idx + self.chunk_size >= total_words:
                break

        logger.info(f"Completed chunking. Total chunks created: {len(chunks_with_metadata)}.")
        return chunks_with_metadata
