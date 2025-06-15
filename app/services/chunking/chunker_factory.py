import logging
from app.services.chunking.word_chunker import WordChunker
from app.services.chunking.sentence_chunker import SentenceChunker

logger = logging.getLogger(__name__)

def get_chunker(strategy: str, **kwargs):
    """
    Factory function to return a chunking strategy instance based on the input strategy.

    Parameters
    ----------
    strategy : str
        The chunking strategy to use. Supported values are:
        - "word": Uses WordChunker to split text by a fixed number of words
        - "sentence": Uses SentenceChunker to split text by sentences

    **kwargs : dict
        Optional keyword arguments passed to the chunker constructor.
        For example: chunk_size, overlap, etc.

    Returns
    -------
    BaseChunker
        An instance of the selected chunking strategy class.

    Raises
    ------
    ValueError
        If the given strategy is not supported.
    """
    strategy = strategy.lower()
    logger.info(f"Initializing chunker strategy: {strategy}")

    if strategy == "word":
        chunker = WordChunker(**kwargs)
        logger.info(f"WordChunker initialized with params: {kwargs}")
        return chunker

    elif strategy == "sentence":
        chunker = SentenceChunker(**kwargs)
        logger.info(f"SentenceChunker initialized with params: {kwargs}")
        return chunker

    else:
        logger.error(f"Unsupported chunking strategy received: {strategy}")
        raise ValueError(f"Unsupported chunking strategy: {strategy}")
