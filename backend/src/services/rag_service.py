"""RAG Service - Simple semantic search using pgvector."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .embedding_service import EmbeddingService


class RAGService:
    """
    Simple RAG service for semantic search in knowledge base.

    Uses marketing_match_documents function from Supabase for vector similarity.
    This is the MVP version (TAREA 4).
    TAREA 5 will add metadata filtering + reranking.
    """

    def __init__(self, db: AsyncSession, embedding_service: EmbeddingService):
        """
        Initialize RAG service.

        Args:
            db: Async database session
            embedding_service: Service for generating embeddings
        """
        self.db = db
        self.embedding_service = embedding_service

    async def search_relevant_docs(
        self,
        query: str,
        project_id: UUID,
        chat_id: UUID | None = None,
        limit: int = 5
    ) -> list[dict]:
        """
        Search for relevant documents using semantic similarity.

        Args:
            query: User query to search for
            project_id: Project ID for filtering
            chat_id: Optional chat ID for additional filtering
            limit: Maximum number of results to return

        Returns:
            List of relevant document chunks with metadata:
            [
                {
                    "content": "...",
                    "source_title": "...",
                    "content_type": "user_document | youtube | book",
                    "similarity": 0.85
                },
                ...
            ]
        """
        # 1. Generate embedding for query
        query_embedding = await self.embedding_service.generate_embedding(query)

        # 2. Call marketing_match_documents function
        # Note: This function is defined in 001_initial_schema.sql
        sql = text("""
            SELECT
                chunk_text as content,
                source_title,
                content_type,
                metadata,
                1 - (embedding <=> :query_embedding::vector) as similarity
            FROM marketing_knowledge_base
            WHERE project_id = :project_id OR project_id IS NULL
            ORDER BY embedding <=> :query_embedding::vector
            LIMIT :limit
        """)

        result = await self.db.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "project_id": str(project_id),
                "limit": limit
            }
        )

        rows = result.fetchall()

        # 3. Format results
        return [
            {
                "content": row.content,
                "source_title": row.source_title,
                "content_type": row.content_type,
                "similarity": float(row.similarity)
            }
            for row in rows
        ]

    async def search_by_chat(
        self,
        query: str,
        chat_id: UUID,
        project_id: UUID,
        limit: int = 5
    ) -> list[dict]:
        """
        Search documents specifically uploaded to a chat.

        Args:
            query: User query
            chat_id: Chat ID to filter by
            project_id: Project ID for validation
            limit: Maximum results

        Returns:
            List of relevant document chunks from this chat
        """
        # 1. Generate embedding
        query_embedding = await self.embedding_service.generate_embedding(query)

        # 2. Search with chat_id filter
        sql = text("""
            SELECT
                chunk_text as content,
                source_title,
                content_type,
                metadata,
                1 - (embedding <=> :query_embedding::vector) as similarity
            FROM marketing_knowledge_base
            WHERE project_id = :project_id
              AND chat_id = :chat_id
              AND content_type = 'user_document'
            ORDER BY embedding <=> :query_embedding::vector
            LIMIT :limit
        """)

        result = await self.db.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "project_id": str(project_id),
                "chat_id": str(chat_id),
                "limit": limit
            }
        )

        rows = result.fetchall()

        return [
            {
                "content": row.content,
                "source_title": row.source_title,
                "content_type": row.content_type,
                "similarity": float(row.similarity)
            }
            for row in rows
        ]
