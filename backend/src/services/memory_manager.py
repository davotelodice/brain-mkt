"""Memory Manager - Centralized access to triple memory system."""

from uuid import UUID

from langchain.memory import ConversationBufferWindowMemory
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingBuyerPersona, MarketingMessage
from .rag_service import RAGService


class MemoryManager:
    """
    Centralized memory manager combining three types of memory:

    1. Short-term: ConversationBufferWindowMemory (last 10 messages)
    2. Long-term: PostgreSQL (buyer personas, customer journeys)
    3. Semantic: pgvector RAG (knowledge base documents)

    All agents access memory through this single interface.
    """

    def __init__(self, db: AsyncSession, rag_service: RAGService):
        """
        Initialize memory manager.

        Args:
            db: Async database session
            rag_service: RAG service for semantic search
        """
        self.db = db
        self.rag_service = rag_service

        # Short-term memory MUST be per chat_id (avoid cross-chat leakage)
        self._short_term_by_chat: dict[UUID, ConversationBufferWindowMemory] = {}
        self._loaded_chats: set[UUID] = set()

    def _get_short_term(self, chat_id: UUID) -> ConversationBufferWindowMemory:
        if chat_id not in self._short_term_by_chat:
            self._short_term_by_chat[chat_id] = ConversationBufferWindowMemory(k=10)
        return self._short_term_by_chat[chat_id]

    async def get_context(
        self,
        chat_id: UUID,
        project_id: UUID,
        current_message: str | None = None
    ) -> dict:
        """
        Get complete context combining all three memory types.

        Args:
            chat_id: Chat ID
            project_id: Project ID for filtering
            current_message: Optional current user message for RAG query

        Returns:
            Combined context dictionary:
            {
                "recent_chat": [...],  # Last 10 messages
                "buyer_persona": {...},  # Buyer persona if exists
                "customer_journey": {...},  # Customer journey if exists
                "relevant_docs": [...],  # Semantic search results
                "has_buyer_persona": bool,
                "documents_count": int
            }
        """
        # Ensure short-term memory is loaded for this chat
        await self.ensure_chat_loaded(chat_id=chat_id, project_id=project_id, limit=20)

        # 1. Short-term: Get recent messages from buffer
        recent_messages = self._get_short_term(chat_id).load_memory_variables({})

        # 2. Long-term: Get buyer persona
        buyer_persona = await self._get_buyer_persona(chat_id, project_id)

        # 3. Long-term: Count documents uploaded to this chat
        documents_count = await self._count_user_documents(chat_id, project_id)
        document_summaries = await self._get_document_summaries(chat_id, project_id)

        # 4. Semantic: Get relevant documents via RAG
        relevant_docs = []
        if current_message:
            relevant_docs = await self.rag_service.search_relevant_docs(
                query=current_message,
                project_id=project_id,
                chat_id=chat_id,
                limit=5
            )

        return {
            "recent_chat": recent_messages,
            "buyer_persona": buyer_persona,
            "relevant_docs": relevant_docs,
            "has_buyer_persona": buyer_persona is not None,
            "documents_count": documents_count,
            "document_summaries": document_summaries,
        }

    async def add_message_to_short_term(
        self,
        chat_id: UUID,
        role: str,
        content: str
    ) -> None:
        """
        Add message to short-term memory buffer.

        Args:
            role: Message role (user | assistant)
            content: Message content
        """
        mem = self._get_short_term(chat_id)
        if role == "user":
            mem.chat_memory.add_user_message(content)
        elif role == "assistant":
            mem.chat_memory.add_ai_message(content)

    async def _get_buyer_persona(
        self,
        chat_id: UUID,
        project_id: UUID
    ) -> dict | None:
        """
        Get buyer persona for chat if exists.

        Args:
            chat_id: Chat ID
            project_id: Project ID for validation

        Returns:
            Buyer persona data or None
        """
        result = await self.db.execute(
            select(MarketingBuyerPersona).where(
                MarketingBuyerPersona.chat_id == chat_id,
                MarketingBuyerPersona.project_id == project_id
            )
        )

        persona = result.scalar_one_or_none()

        if persona:
            # Return full_analysis (contains complete buyer persona JSON)
            return persona.full_analysis if persona.full_analysis else {}

        return None

    async def _count_user_documents(
        self,
        chat_id: UUID,
        project_id: UUID
    ) -> int:
        """
        Count documents uploaded to this chat.

        Args:
            chat_id: Chat ID
            project_id: Project ID for validation

        Returns:
            Number of documents
        """
        from ..db.models import MarketingUserDocument

        result = await self.db.execute(
            select(MarketingUserDocument).where(
                MarketingUserDocument.chat_id == chat_id,
                MarketingUserDocument.project_id == project_id
            )
        )

        docs = result.scalars().all()
        return len(docs)

    async def _get_document_summaries(self, chat_id: UUID, project_id: UUID) -> list[dict]:
        """
        Get persisted summaries for uploaded documents in this chat.

        Returns:
            [{ "document_id": "...", "filename": "...", "summary": "..." }, ...]
        """
        from ..db.models import MarketingUserDocument

        result = await self.db.execute(
            select(MarketingUserDocument).where(
                MarketingUserDocument.chat_id == chat_id,
                MarketingUserDocument.project_id == project_id,
            )
        )
        docs = result.scalars().all()
        out: list[dict] = []
        for d in docs:
            if getattr(d, "summary", None):
                out.append(
                    {"document_id": str(d.id), "filename": d.filename, "summary": d.summary}
                )
        return out

    async def load_chat_history(
        self,
        chat_id: UUID,
        project_id: UUID,
        limit: int = 10
    ) -> None:
        """
        Load chat history into short-term memory from database.

        This should be called when initializing a conversation.

        Args:
            chat_id: Chat ID
            project_id: Project ID for validation
            limit: Number of recent messages to load (default: 10)
        """
        # Reset memory for this chat before loading
        self._short_term_by_chat[chat_id] = ConversationBufferWindowMemory(k=10)

        # Get last N messages from database
        result = await self.db.execute(
            select(MarketingMessage)
            .where(
                MarketingMessage.chat_id == chat_id,
                MarketingMessage.project_id == project_id
            )
            .order_by(MarketingMessage.created_at.desc())
            .limit(limit)
        )

        messages = result.scalars().all()

        # Add to short-term memory (reverse order: oldest first)
        for message in reversed(messages):
            await self.add_message_to_short_term(
                chat_id=chat_id,
                role=message.role,
                content=message.content
            )

        self._loaded_chats.add(chat_id)

    async def ensure_chat_loaded(self, chat_id: UUID, project_id: UUID, limit: int = 20) -> None:
        if chat_id in self._loaded_chats:
            return
        await self.load_chat_history(chat_id=chat_id, project_id=project_id, limit=limit)
