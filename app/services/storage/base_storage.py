from abc import ABC, abstractmethod
from typing import List, Any, Union, Dict, Optional
from app.db.models import Conversation, Message


class BaseStorage(ABC):
    """
    Abstract base class for document, chunk, and chat storage backends.

    This interface defines the required methods any storage backend must implement
    to be compatible with the RAG pipeline. It ensures that documents, chunks, embeddings,
    and chat-related entities like conversations and messages can be persisted consistently.
    """

    @abstractmethod
    def store_document(self, name: str, document_metadata: dict, path: str) -> Any:
        """
        Store metadata about the original document in the storage backend.

        Args:
            name (str): The name of the document.
            document_metadata (dict): Additional metadata for the document.
            path (str): The path to the document on the local filesystem or cloud.

        Returns:
            Any: A storage-specific object representing the stored document.
        """
        pass

    @abstractmethod
    def store_chunks(self, document_id: int, chunks: List[Dict[str, Union[str, dict]]], embeddings: List[List[float]]) -> None:
        """
        Store the chunked text and their corresponding vector embeddings.

        Args:
            document_id (int): The unique identifier of the stored document.
            chunks (List[Dict]): A list of text chunks and optional metadata.
            embeddings (List[List[float]]): Vector embeddings corresponding to each chunk.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """
        Retrieve a conversation by its ID.

        Args:
            conversation_id (str): Unique identifier of the conversation.

        Returns:
            Optional[Conversation]: The conversation instance if found, else None.
        """
        pass

    @abstractmethod
    def create_conversation(self, conversation: Conversation) -> None:
        """
        Persist a new conversation.

        Args:
            conversation (Conversation): The conversation object to store.
        """
        pass

    @abstractmethod
    def add_message(self, message: Message) -> None:
        """
        Persist a new chat message.

        Args:
            message (Message): The message object to store.
        """
        pass

    @abstractmethod
    def get_messages_by_conversation(self, conversation_id: str) -> List[Message]:
        """
        Retrieve all messages in a conversation, ordered by creation time.

        Args:
            conversation_id (str): Unique identifier of the conversation.

        Returns:
            List[Message]: List of messages in the conversation.
        """
        pass
