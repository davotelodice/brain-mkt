"""Memory Manager - Centralized access to triple memory system."""

import logging
import time
from uuid import UUID

from langchain.memory import ConversationBufferWindowMemory
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingBuyerPersona, MarketingMessage
from .llm_service import LLMService
from .rag_service import RAGService

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Centralized memory manager combining three types of memory:

    1. Short-term: ConversationBufferWindowMemory (last 10 messages)
    2. Long-term: PostgreSQL (buyer personas, customer journeys)
    3. Semantic: pgvector RAG (knowledge base documents)

    All agents access memory through this single interface.
    """

    def __init__(self, db: AsyncSession, rag_service: RAGService, llm_service: LLMService | None = None):
        """
        Initialize memory manager.

        Args:
            db: Async database session
            rag_service: RAG service for semantic search
            llm_service: Optional LLM service for generating training summaries
        """
        self.db = db
        self.rag_service = rag_service
        self.llm_service = llm_service

        # Short-term memory MUST be per chat_id (avoid cross-chat leakage)
        self._short_term_by_chat: dict[UUID, ConversationBufferWindowMemory] = {}
        self._loaded_chats: set[UUID] = set()
        # Cache (in-memory) for training summaries (TTL seconds)
        self._training_summary_cache: dict[str, tuple[str, float]] = {}

    def _get_short_term(self, chat_id: UUID) -> ConversationBufferWindowMemory:
        if chat_id not in self._short_term_by_chat:
            self._short_term_by_chat[chat_id] = ConversationBufferWindowMemory(k=10)
        return self._short_term_by_chat[chat_id]

    async def get_context(
        self,
        chat_id: UUID,
        project_id: UUID,
        current_message: str | None = None,
    ) -> dict:
        """
        Get complete context combining all memory types (short, long, semantic).

        Args:
            chat_id: Chat ID
            project_id: Project ID for filtering
            current_message: Optional current user message for RAG query

        Returns:
            Combined context dictionary:
            {
                "recent_chat": [...],
                "buyer_persona": {...} | None,
                "forum_simulation": {...} | None,
                "pain_points": {...} | None,
                "customer_journey": {...} | None,
                "relevant_docs": [...],
                "has_buyer_persona": bool,
                "documents_count": int,
                "document_summaries": [...],
            }
        """
        # Ensure short-term memory is loaded for this chat
        await self.ensure_chat_loaded(chat_id=chat_id, project_id=project_id, limit=20)

        # 1. Short-term: Get recent messages from buffer
        recent_messages = self._get_short_term(chat_id).load_memory_variables({})

        # 2. Long-term: Get buyer persona + análisis extendido (foro, pain points, CJ)
        buyer_persona_row = await self._get_buyer_persona_row(chat_id, project_id)
        buyer_persona = buyer_persona_row.full_analysis if buyer_persona_row else None
        forum_simulation = (
            buyer_persona_row.forum_simulation if buyer_persona_row else None
        )
        pain_points = buyer_persona_row.pain_points if buyer_persona_row else None
        customer_journey = (
            buyer_persona_row.customer_journey if buyer_persona_row else None
        )

        # 3. Long-term: Count documents uploaded to this chat
        documents_count = await self._count_user_documents(chat_id, project_id)
        document_summaries = await self._get_document_summaries(chat_id, project_id)

        # 4. Semantic: Get relevant documents via RAG
        relevant_docs: list[dict] = []
        if current_message:
            relevant_docs = await self.rag_service.search_relevant_docs(
                query=current_message,
                project_id=project_id,
                chat_id=chat_id,
                limit=5,
            )

        return {
            "recent_chat": recent_messages,
            "buyer_persona": buyer_persona,
            "forum_simulation": forum_simulation,
            "pain_points": pain_points,
            "customer_journey": customer_journey,
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

    def format_messages_from_memory(
        self,
        chat_id: UUID,
        system_prompt: str = "",
        current_user_message: str = ""
    ) -> list[dict[str, str]]:
        """
        Convert ConversationBufferWindowMemory to OpenAI messages format.

        VERIFICADO: load_memory_variables({}) retorna {"history": "Human: ...\\nAI: ..."}

        Args:
            chat_id: Chat ID
            system_prompt: Optional system prompt to prepend
            current_user_message: Optional current user message to append

        Returns:
            List of message dicts in OpenAI format:
            [{"role": "system", "content": "..."},
             {"role": "user", "content": "..."},
             {"role": "assistant", "content": "..."}, ...]
        """
        messages: list[dict[str, str]] = []

        # 1. System prompt primero (si se proporciona)
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 2. Obtener historial de ConversationBufferWindowMemory
        memory = self._get_short_term(chat_id)
        history_dict = memory.load_memory_variables({})
        history_text = history_dict.get("history", "")

        # 3. Parsear formato "Human: ...\\nAI: ..."
        if history_text and isinstance(history_text, str):
            lines = history_text.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("Human:"):
                    content = line.replace("Human:", "").strip()
                    if content:
                        messages.append({"role": "user", "content": content})
                elif line.startswith("AI:"):
                    content = line.replace("AI:", "").strip()
                    if content:
                        messages.append({"role": "assistant", "content": content})

        # 4. Añadir mensaje actual del usuario (si se proporciona)
        if current_user_message:
            messages.append({"role": "user", "content": current_user_message})

        logger.info(
            "[MEM] chat_id=%s history_chars=%s messages_out=%s",
            str(chat_id),
            len(history_text or ""),
            len(messages),
        )
        return messages

    async def get_training_summary(self, project_id: UUID) -> str:
        """
        Obtener resumen de técnicas de las transcripciones de Andrea Estratega (cacheado).

        Estrategia:
        1. Buscar chunks más representativos de técnicas virales
        2. Generar resumen estructurado con LLM (una vez, cachear 24h)
        3. Retornar resumen para inyectar en system prompt

        Args:
            project_id: Project ID (para cache key, aunque transcripciones son globales)

        Returns:
            Resumen de técnicas en formato texto listo para system prompt
        """
        if not self.llm_service:
            return "No hay LLM service disponible para generar resumen de técnicas."

        cache_ttl = int(time.time()) + 86400
        cache_key = f"training_summary:{project_id}"
        cached = self._training_summary_cache.get(cache_key)
        if cached and cached[1] > time.time():
            logger.info("[TRAIN] cache_hit=1 project_id=%s", str(project_id))
            return cached[0]
        logger.info("[TRAIN] cache_hit=0 project_id=%s", str(project_id))

        # 1. Buscar chunks representativos de técnicas virales
        # Nota: Usamos project_id para la búsqueda aunque las transcripciones son globales
        # RAGService filtrará por metadata_filters para obtener solo video_transcript
        training_chunks = await self.rag_service.search_relevant_docs(
            query="técnicas virales hooks estructuras contenido Instagram TikTok",
            project_id=project_id,  # Usar project_id aunque transcripciones sean globales
            chat_id=None,
            limit=15,  # Top 15 chunks más relevantes
            metadata_filters={"content_type": "video_transcript"},
            rerank=True  # Mejor relevancia
        )

        if not training_chunks:
            return "No hay transcripciones de entrenamiento disponibles aún."

        # 2. Combinar chunks en texto
        techniques_text = "\n\n---\n\n".join([
            f"**TÉCNICA {i+1}** (de: {chunk.get('source_title', 'Desconocido')}):\n{chunk.get('content', '')[:800]}"
            for i, chunk in enumerate(training_chunks)
        ])

        # 3. Generar resumen estructurado
        summary_prompt = f"""
        Resume las técnicas principales de creación de contenido viral
        de estas transcripciones de videos de marketing de Andrea Estratega:

        {techniques_text}

        Crea un resumen estructurado y conciso (máximo 1500 palabras) con:

        1. TÉCNICAS DE HOOKS (primeros 3 segundos):
           - Ejemplos específicos
           - Patrones que funcionan

        2. ESTRUCTURAS DE CONTENIDO:
           - Formatos probados
           - Orden de elementos

        3. TÉCNICAS VIRALES:
           - Qué hace que un contenido se vuelva viral
           - Elementos clave

        4. CTAs EFECTIVOS:
           - Cómo cerrar contenido para acción

        Formato: Texto claro, listo para usar en system prompt de un LLM.
        Sé específico con ejemplos reales de las transcripciones.
        """

        summary = await self.llm_service.generate(
            prompt=summary_prompt,
            system="Eres un experto en resumir técnicas de marketing de forma estructurada y concisa.",
            max_tokens=1500,  # Reducido para evitar prompts muy largos
            temperature=0.3  # Baja temperatura para resumen fiel
        )

        # Truncar si es demasiado largo (máximo ~2000 caracteres ≈ 500 tokens)
        if len(summary) > 2000:
            summary = summary[:2000] + "..."

        logger.info(
            "[TRAIN] project_id=%s chunks=%s summary_chars=%s",
            str(project_id),
            len(training_chunks),
            len(summary or ""),
        )
        # Cache in-memory (TTL 24h)
        self._training_summary_cache[cache_key] = (summary, float(cache_ttl))

        return summary

    async def _get_buyer_persona_row(
        self,
        chat_id: UUID,
        project_id: UUID
    ):
        """
        Get MarketingBuyerPersona row for chat if exists.

        Args:
            chat_id: Chat ID
            project_id: Project ID for validation

        Returns:
            ORM row or None
        """
        result = await self.db.execute(
            select(MarketingBuyerPersona).where(
                MarketingBuyerPersona.chat_id == chat_id,
                MarketingBuyerPersona.project_id == project_id
            )
        )

        return result.scalar_one_or_none()

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
            # Validate that role and content are not None (mypy type checking)
            if message.role is None or message.content is None:
                continue
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
