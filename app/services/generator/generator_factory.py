import logging
from app.services.generator.base_generator import BaseGenerator
from app.services.generator.openai_generator import OpenAIGenerator
from app.services.generator.local_llm_generator import LocalGenerator

# Module-level logger
logger = logging.getLogger(__name__)

def get_generator(provider: str, **kwargs) -> BaseGenerator:
    """
    Factory function to initialize the appropriate LLM generator.

    This function returns an instance of a generator class that implements
    the BaseGenerator interface, based on the provided provider name.

    Parameters
    ----------
    provider : str
        The name of the provider to use ("openai" or "local").
    **kwargs : dict
        Additional keyword arguments passed to the generator constructor.
        For example, model configuration or API keys.

    Returns
    -------
    BaseGenerator
        An instance of a class implementing BaseGenerator for the selected provider.

    Raises
    ------
    ValueError
        If the specified provider is not supported.
    """
    provider = provider.lower()

    if provider == "openai":
        logger.info("Initializing OpenAIGenerator with provided kwargs.")
        return OpenAIGenerator(**kwargs)

    elif provider == "local":
        logger.info("Initializing LocalGenerator.")
        return LocalGenerator()

    else:
        logger.error(f"Unsupported generator backend requested: {provider}")
        raise ValueError(f"Unsupported generator backend: {provider}")
