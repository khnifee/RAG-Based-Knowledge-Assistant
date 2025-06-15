from abc import ABC, abstractmethod
from typing import List

class BaseEmbedder(ABC):
    """
    Abstract base class for embedding generators.

    This interface defines a standard method `get_embedding` that all embedding implementations 
    (e.g., OpenAIEmbedder, LocalEmbedder) must implement. It ensures consistency across different 
    embedding backends so they can be used interchangeably in the pipeline.

    All implementations must return embeddings as a list of floats, suitable for vector similarity search
    and downstream storage.

    Example usage (via factory or concrete implementation):
        embedder = OpenAIEmbedder()
        embedding = embedder.get_embedding("example text")
    """

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate a vector embedding for the given input text.

        Args:
            text (str): Input string to embed.

        Returns:
            List[float]: A list of floating point numbers representing the embedding vector.
        """
        pass
