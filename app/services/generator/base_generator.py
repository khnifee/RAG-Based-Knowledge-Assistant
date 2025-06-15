from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseGenerator(ABC):
    @abstractmethod
    def generate_answer(self, query: str, context: Optional[str] = None, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generates an answer based on the input query and context."""
        pass
