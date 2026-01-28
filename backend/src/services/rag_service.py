"""RAG Service - Hybrid search with reranking using pgvector."""

import logging
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .embedding_service import EmbeddingService
from .llm_service import LLMService

logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG service with hybrid search and reranking capabilities.

    Features (TAREA 5):
    - Vector similarity search (semantic)
    - Metadata filtering (content_type, source, date)
    - LLM-based reranking for improved relevance

    Simple version (TAREA 4) still available via rerank=False.
    """

    def __init__(
        self,
        db: AsyncSession,
        embedding_service: EmbeddingService,
        llm_service: LLMService | None = None
    ):
        """
        Initialize RAG service.

        Args:
            db: Async database session
            embedding_service: Service for generating embeddings
            llm_service: Optional LLM service for reranking (TAREA 5)
        """
        self.db = db
        self.embedding_service = embedding_service
        self.llm_service = llm_service

    async def search_relevant_docs(
        self,
        query: str,
        project_id: UUID,
        chat_id: UUID | None = None,
        limit: int = 5,
        rerank: bool = False,
        metadata_filters: dict | None = None
    ) -> list[dict]:
        """
        Search for relevant documents using semantic similarity.

        TAREA 5 Improvements:
        - Metadata filtering (content_type, source)
        - LLM-based reranking for better relevance

        Args:
            query: User query to search for
            project_id: Project ID for filtering
            chat_id: Optional chat ID for additional filtering
            limit: Maximum number of results to return
            rerank: If True, use LLM to rerank results (TAREA 5)
            metadata_filters: Optional filters {"content_type": "youtube", "source": "Andrea"}

        Returns:
            List of relevant document chunks with metadata:
            [
                {
                    "content": "...",
                    "source_title": "...",
                    "content_type": "user_document | youtube | book",
                    "similarity": 0.85,
                    "rerank_score": 0.92  # If rerank=True
                },
                ...
            ]
        """
        logger.info(
            "[RAG] query_len=%s project_id=%s chat_id=%s limit=%s rerank=%s filters=%s",
            len(query or ""),
            str(project_id),
            str(chat_id) if chat_id else "None",
            limit,
            rerank,
            metadata_filters or {},
        )
        # 1. Get initial results (fetch 3x for reranking)
        initial_limit = limit * 3 if rerank else limit
        initial_results = await self._vector_search(
            query=query,
            project_id=project_id,
            chat_id=chat_id,
            limit=initial_limit
        )

        # 2. Apply metadata filters if provided
        if metadata_filters:
            initial_results = self._filter_by_metadata(initial_results, metadata_filters)

        # 3. Rerank with LLM if requested
        if rerank and self.llm_service and len(initial_results) > 0:
            reranked_results = await self._rerank_with_llm(query, initial_results)
            logger.info(
                "[RAG] reranked_count=%s top_types=%s top_sim=%s",
                len(reranked_results[:limit]),
                [d.get("content_type") for d in reranked_results[: min(limit, 3)]],
                [round(float(d.get("similarity", 0.0)), 3) for d in reranked_results[: min(limit, 3)]],
            )
            return reranked_results[:limit]

        logger.info(
            "[RAG] result_count=%s top_types=%s top_sim=%s",
            len(initial_results[:limit]),
            [d.get("content_type") for d in initial_results[: min(limit, 3)]],
            [round(float(d.get("similarity", 0.0)), 3) for d in initial_results[: min(limit, 3)]],
        )
        return initial_results[:limit]

    async def _vector_search(
        self,
        query: str,
        project_id: UUID,
        chat_id: UUID | None,
        limit: int
    ) -> list[dict]:
        """
        Internal vector similarity search.

        Args:
            query: User query
            project_id: Project ID for filtering
            chat_id: Optional chat ID for filtering
            limit: Maximum results

        Returns:
            List of document chunks with similarity scores
        """
        # 1. Generate embedding for query
        query_embedding = await self.embedding_service.generate_embedding(query)

        # 2. Vector similarity search
        # Note: Convert embedding to pgvector string format: '[0.1, 0.2, ...]'
        embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

        sql = text("""
            SELECT
                chunk_text as content,
                source_title,
                content_type,
                metadata,
                1 - (embedding <=> CAST(:query_embedding AS vector)) as similarity
            FROM marketing_knowledge_base
            WHERE project_id = :project_id OR project_id IS NULL
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :limit
        """)

        result = await self.db.execute(
            sql,
            {
                "query_embedding": embedding_str,
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
                "metadata": dict(row.metadata) if row.metadata else {},
                "similarity": float(row.similarity)
            }
            for row in rows
        ]

    def _filter_by_metadata(
        self,
        results: list[dict],
        metadata_filters: dict
    ) -> list[dict]:
        """
        Filter results by metadata fields.

        Args:
            results: List of document chunks
            metadata_filters: Filters to apply {"content_type": "youtube", "source": "Andrea"}

        Returns:
            Filtered list of documents
        """
        filtered = []
        for doc in results:
            matches = True

            # Check content_type filter
            if "content_type" in metadata_filters:
                if doc.get("content_type") != metadata_filters["content_type"]:
                    matches = False

            # Check nested metadata filters
            doc_metadata = doc.get("metadata", {})
            for key, value in metadata_filters.items():
                if key != "content_type":  # Already checked above
                    if doc_metadata.get(key) != value:
                        matches = False
                        break

            if matches:
                filtered.append(doc)

        return filtered

    async def _rerank_with_llm(
        self,
        query: str,
        results: list[dict]
    ) -> list[dict]:
        """
        Rerank results using LLM for improved relevance.

        Args:
            query: Original user query
            results: List of candidate documents

        Returns:
            Reranked list of documents with rerank_score
        """
        if not self.llm_service or len(results) == 0:
            return results

        # Build reranking prompt
        docs_text = "\n\n".join([
            f"[{i+1}] {doc['content'][:500]}..."
            for i, doc in enumerate(results)
        ])

        prompt = f"""Given the user query and candidate documents, rank them by relevance.
Return ONLY a comma-separated list of numbers (1-{len(results)}) in order of relevance.

Query: "{query}"

Documents:
{docs_text}

Ranking (most relevant first):"""

        try:
            # Get LLM ranking
            response = await self.llm_service.generate(
                prompt=prompt,
                system="You are a relevance ranking expert. Return only numbers.",
                max_tokens=100,
                temperature=0.0
            )

            # Parse ranking (e.g., "3,1,5,2,4")
            ranking = [int(x.strip()) - 1 for x in response.strip().split(",") if x.strip().isdigit()]

            # Reorder results
            reranked = []
            for rank_idx, doc_idx in enumerate(ranking):
                if 0 <= doc_idx < len(results):
                    doc = results[doc_idx].copy()
                    doc["rerank_score"] = 1.0 - (rank_idx / len(ranking))
                    reranked.append(doc)

            # Add any missing docs at the end
            added_indices = set(ranking)
            for i, doc in enumerate(results):
                if i not in added_indices:
                    doc_copy = doc.copy()
                    doc_copy["rerank_score"] = 0.0
                    reranked.append(doc_copy)

            return reranked

        except Exception as e:
            # If reranking fails, return original order
            print(f"⚠️ Reranking failed: {e}")
            return results

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

        # Convert to string format for pgvector
        embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

        # 2. Search with chat_id filter
        sql = text("""
            SELECT
                chunk_text as content,
                source_title,
                content_type,
                metadata,
                1 - (embedding <=> CAST(:query_embedding AS vector)) as similarity
            FROM marketing_knowledge_base
            WHERE project_id = :project_id
              AND chat_id = :chat_id
              AND content_type = 'user_document'
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :limit
        """)

        result = await self.db.execute(
            sql,
            {
                "query_embedding": embedding_str,
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
