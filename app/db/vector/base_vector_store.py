from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union

class BaseVectorStore(ABC):
    """
    Abstract base class for vector store implementations.

    This class defines the contract for storing and querying document chunks 
    with their associated vector embeddings.
    """

    @abstractmethod
    def store_chunks(
        self,
        document_id: int,
        chunks: List[Union[str, Dict[str, Any]]],
        embeddings: List[List[float]],
    ) -> None:
        """
        Stores a list of text chunks and their corresponding vector embeddings.

        Args:
            document_id (int): The ID of the document the chunks belong to.
            chunks (List[Union[str, Dict[str, Any]]]): A list of text chunks or dictionaries 
                with 'text' and optional 'metadata'.
            embeddings (List[List[float]]): A list of vector embeddings corresponding to the chunks.

        Returns:
            None
        """
        pass

    @abstractmethod
    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        knowledge_base_id: Optional[str] = None,
        filters: Optional[Dict[str, Union[str, int]]] = None,
        min_score: float = 0.0,
        query_text: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Queries the vector store for the most relevant chunks based on a query embedding.

        Args:
            query_embedding (List[float]): The embedding vector of the query.
            top_k (int, optional): The maximum number of top results to return. Defaults to 5.
            knowledge_base_id (Optional[str], optional): Optional filter to restrict search to a specific knowledge base.
            filters (Optional[Dict[str, Union[str, int]]], optional): Optional metadata filters for more granular search.
            min_score (float, optional): Minimum similarity score threshold. Defaults to 0.0.
            query_text (Optional[str], optional): Optional keyword-based query text for hybrid strategies.

        Returns:
            List[Dict[str, Any]]: A list of matched chunks with associated metadata and similarity scores.
        """
        pass
