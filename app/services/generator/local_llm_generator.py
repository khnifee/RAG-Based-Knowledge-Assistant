import logging
from typing import List, Dict, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from app.services.generator.base_generator import BaseGenerator
from app.services.prompt.prompt_manager import PromptManager

# Module-level logger
logger = logging.getLogger(__name__)

class LocalGenerator(BaseGenerator):
    """
    Local LLM-based generator for generating answers using a HuggingFace-compatible model.

    This implementation loads a causal language model locally using transformers,
    and performs text generation with an optional RAG-style prompt or chat history.

    Attributes
    ----------
    model_name : str
        Name of the model to be loaded from Hugging Face.
    device : str
        Device used for model inference, either 'cuda' or 'cpu'.
    tokenizer : AutoTokenizer
        Tokenizer for the specified model.
    model : AutoModelForCausalLM
        The language model used for text generation.
    pipeline : transformers.pipeline
        Text generation pipeline using the loaded model and tokenizer.
    prompt_manager : PromptManager
        Utility to render prompts from templates.
    """

    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1", device: Optional[str] = None):
        """
        Initialize the LocalGenerator with a specified model name and device.

        Parameters
        ----------
        model_name : str
            The name or path of the model to load.
        device : Optional[str]
            The device to run the model on. Defaults to 'cuda' if available, else 'cpu'.
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        logger.info(f"Loading model '{self.model_name}' on device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
        )

        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )

        self.prompt_manager = PromptManager()

        logger.info("LocalGenerator initialized successfully.")

    def generate_answer(
        self,
        query: str,
        context: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response from the local LLM using optional context and chat history.

        Parameters
        ----------
        query : str
            The user question or prompt.
        context : Optional[str]
            Additional context (e.g., RAG results) to ground the answer.
        chat_history : Optional[List[Dict[str, str]]]
            Previous messages in the conversation, if any.

        Returns
        -------
        str
            The generated assistant response.
        """
        logger.debug("Generating answer using LocalGenerator...")
        logger.debug(f"Query: {query}")
        logger.debug(f"Context provided: {bool(context)}, Chat history count: {len(chat_history) if chat_history else 0}")

        if context and not chat_history:
            prompt = self.prompt_manager.render("rag", context=context, question=query)
        else:
            prompt = ""
            if chat_history:
                for message in chat_history:
                    role = message["role"]
                    prompt += f"{role.capitalize()}: {message['content']}\n"
            prompt += f"User: {query}\nAssistant:"

        logger.debug(f"Constructed prompt (preview): {prompt[:300]}")

        result = self.pipeline(prompt)[0]["generated_text"]

        if "Assistant:" in result:
            response = result.split("Assistant:")[-1].strip()
        else:
            response = result.strip()

        logger.debug(f"Generated response (preview): {response[:300]}")
        return response
