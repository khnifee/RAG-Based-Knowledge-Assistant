import logging
from typing import Optional, List, Dict, Union
from app.services.embedding.embedding_service import EmbeddingService
from app.services.storage.storage_service import StorageService
from app.db.vector.vector_store_service import VectorStoreService
from app.services.generator.generator_service import GeneratorService
from app.services.reranking.reranking_service import RerankingService
from app.db.models import Conversation, Message
from datetime import datetime

logger = logging.getLogger(__name__)

class RagService:
    """
    Core service that handles Retrieval-Augmented Generation workflow.

    Responsibilities:
    - Generate embeddings for the query
    - Run vector search using embeddings
    - Retrieve or create conversation
    - Store user and assistant messages
    - Generate answer using generator with context and chat history
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        storage_service: StorageService,
        vector_store_service: VectorStoreService,
        generator_service: GeneratorService,
        reranking_service: RerankingService
    ):
        self.embedding_service = embedding_service
        self.storage_service = storage_service
        self.vector_store_service = vector_store_service
        self.generator_service = generator_service
        self.reranking_service = reranking_service
        logger.info("Initialized RagService with all dependent services")

    def chat(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        knowledge_base_id: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.0
    ) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
        """
        Handles a chat query and returns an AI-generated response along with context chunks.

        Args:
            query (str): The user query.
            conversation_id (Optional[str]): Existing conversation ID.
            knowledge_base_id (Optional[str]): Used if creating a new conversation.
            top_k (int): Number of context chunks to retrieve.
            min_score (float): Minimum similarity threshold for retrieved chunks.

        Returns:
            Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]: Generated answer and context.
        """

        logger.info(f"Received chat query: '{query}' for conversation_id: {conversation_id} and knowledge_base_id: {knowledge_base_id}")

        # 1. Embed the query
        query_embedding = self.embedding_service.get_embedding(query)
        logger.debug(f"Generated query embedding of length {len(query_embedding)}")

        # 2. Run vector search
        context_chunks = self.vector_store_service.query(
            query_embedding=query_embedding,
            top_k=top_k,
            knowledge_base_id=knowledge_base_id if knowledge_base_id else None,
            min_score=min_score,
        )
        logger.info(f"Retrieved {len(context_chunks)} context chunks from vector search")

        # Optional reranking (not implemented here, but logged for awareness)
        # context_chunks = self.reranking_service.rerank(query, context_chunks)
        # logger.info("Reranked context chunks")

        # Prepare context as plain string
        context_text = "\n".join([chunk["text"] for chunk in context_chunks])
        logger.debug(f"Prepared context text of length {len(context_text)} characters")

        # 3. Retrieve or create conversation
        if conversation_id:
            conversation = self.storage_service.get_conversation_by_id(conversation_id)
            if not conversation:
                logger.error(f"Conversation with ID {conversation_id} not found")
                raise ValueError(f"Conversation with ID {conversation_id} not found.")
            logger.info(f"Loaded conversation with ID {conversation_id}")
        else:
            conversation = Conversation(knowledge_base_id=knowledge_base_id)
            self.storage_service.create_conversation(conversation)
            conversation_id = conversation.id
            logger.info(f"Created new conversation with ID {conversation_id}")

        # 4. Build chat history for LLM API
        history_messages = None
        if conversation.messages:
            history_messages = [{"role": msg.role, "content": msg.content} for msg in conversation.messages]
            logger.debug(f"Loaded chat history with {len(history_messages)} messages")

        # 5. Generate answer using LLM
        answer = self.generator_service.generate_answer(
            query=query,
            context=context_text,
            chat_history=history_messages
        )
        logger.info(f"Generated answer of length {len(answer)} characters")

        # 6. Store user and assistant messages
        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=query,
            created_at=datetime.utcnow()
        )
        self.storage_service.add_message(user_msg)
        logger.info(f"Stored user message for conversation ID {conversation_id}")

        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            created_at=datetime.utcnow()
        )
        self.storage_service.add_message(assistant_msg)
        logger.info(f"Stored assistant message for conversation ID {conversation_id}")

        return {
            "conversation_id": conversation_id,
            "answer": answer,
            "context_chunks": context_chunks
        }
