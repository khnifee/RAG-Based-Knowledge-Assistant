from abc import ABC, abstractmethod
from typing import List, Dict

class BaseReranker(ABC):
    @abstractmethod
    def rerank(self, query: str, documents: List[Dict]) -> List[Dict]:
        """
        Rerank a list of documents based on the query.

        Args:
            query (str): The input user query.
            documents (List[Dict]): Each dict must contain a "text" field.

        Returns:
            List[Dict]: Same structure, sorted by relevance (descending).
        """
        pass
