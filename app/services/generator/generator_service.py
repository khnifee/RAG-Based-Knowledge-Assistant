import logging
from typing import List, Dict, Optional
from app.services.generator.base_generator import BaseGenerator

# Module-level logger
logger = logging.getLogger(__name__)

class GeneratorService:
    """
    High-level service that delegates text generation to a selected LLM provider.

    This service abstracts the underlying generator implementation (e.g., OpenAI, Anthropic)
    and provides a consistent interface to generate answers based on a query and optional context.

    Attributes
    ----------
    generator : BaseGenerator
        The underlying LLM-based generator implementation.
    """

    def __init__(self, generator: BaseGenerator):
        """
        Initialize the generator service with a provided BaseGenerator instance.

        Parameters
        ----------
        generator : BaseGenerator
            An implementation of the BaseGenerator interface for generating answers.
        """
        self.generator = generator
        logger.info(f"Initialized GeneratorService with generator: {generator.__class__.__name__}")

    def generate_answer(
        self,
        query: str,
        context: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate an answer using the provided query, optional context, and chat history.

        Parameters
        ----------
        query : str
            The user query to be answered.
        context : Optional[str]
            Supplementary text used to ground the model's answer.
        chat_history : Optional[List[Dict[str, str]]]
            List of prior user-assistant messages to preserve context in a conversation.

        Returns
        -------
        str
            A generated answer string from the LLM.
        """
        logger.debug(f"Generating answer for query: '{query[:50]}...' (context provided: {bool(context)}, chat history: {len(chat_history) if chat_history else 0} messages)")
        
        answer = self.generator.generate_answer(
            query=query,
            context=context,
            chat_history=chat_history
        )

        logger.debug(f"Generated answer: '{answer[:75]}...'")
        return answer
