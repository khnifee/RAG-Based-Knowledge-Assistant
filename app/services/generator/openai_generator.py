import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional
from app.services.generator.base_generator import BaseGenerator
from app.services.prompt.prompt_manager import PromptManager

# Load environment variables
load_dotenv()

# Module-level logger
logger = logging.getLogger(__name__)

class OpenAIGenerator(BaseGenerator):
    """
    Generator implementation that uses OpenAI's ChatCompletion API.

    This class leverages OpenAI's hosted models (e.g., GPT-4, GPT-3.5) to generate
    conversational responses based on query, context, and optional chat history.

    Attributes
    ----------
    client : OpenAI
        The OpenAI client for interacting with the API.
    model : str
        The OpenAI model to use (e.g., "gpt-4").
    prompt_manager : PromptManager
        Manages prompt templates and context formatting.
    """

    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the generator with the specified OpenAI model.

        Parameters
        ----------
        model : str
            The OpenAI model to use for generating responses. Default is "gpt-4".

        Raises
        ------
        ValueError
            If the OPENAI_API_KEY is not set in the environment.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set.")
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompt_manager = PromptManager()

        logger.info(f"Initialized OpenAIGenerator with model '{self.model}'.")

    def generate_answer(
        self,
        query: str,
        context: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response from the LLM using optional context and chat history.

        Parameters
        ----------
        query : str
            The user query.
        context : Optional[str]
            Fallback or summary context if no history exists.
        chat_history : Optional[List[Dict[str, str]]]
            List of prior chat messages, each in the format:
            {"role": "user" or "assistant", "content": "..."}

        Returns
        -------
        str
            The generated response from the model.
        """
        logger.debug("Generating answer using OpenAIGenerator...")
        logger.debug(f"Query: {query}")
        logger.debug(f"Context present: {bool(context)} | Chat history length: {len(chat_history) if chat_history else 0}")

        messages = chat_history.copy() if chat_history else []

        if context:
            rendered_context = self.prompt_manager.render("rag", context=context)
            messages.insert(0, {"role": "system", "content": rendered_context})

        messages.append({"role": "user", "content": query})

        logger.debug(f"Messages prepared for OpenAI completion (preview): {messages[-2:] if len(messages) > 1 else messages}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            content = response.choices[0].message.content.strip()
            logger.debug(f"Generated response (preview): {content[:300]}")
            return content
        except Exception as e:
            logger.exception("Error occurred during OpenAI completion.")
            raise e
