"""Document processor service - Parse, chunk, embed, and store documents."""
from pathlib import Path
from uuid import UUID

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingKnowledgeBase, MarketingUserDocument
from ..services.embedding_service import EmbeddingService
from ..utils.file_parsers import parse_document


class DocumentProcessor:
    """Service for processing user documents into knowledge base."""

    def __init__(self, db: AsyncSession, embedding_service: EmbeddingService):
        """Initialize document processor.

        Args:
            db: Database session
            embedding_service: Service for generating embeddings
        """
        self.db = db
        self.embedding_service = embedding_service
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_document(
        self,
        document_id: UUID,
        file_path: Path,
        file_type: str,
        chat_id: UUID,
        project_id: UUID,
        source_title: str
    ) -> dict[str, int | bool]:
        """Process document: parse, chunk, embed, and store.

        Args:
            document_id: ID of document in marketing_user_documents
            file_path: Path to uploaded file
            file_type: File extension (.txt, .pdf, .docx)
            chat_id: Chat ID where document was uploaded
            project_id: Project ID (CRITICAL for isolation)
            source_title: Document filename

        Returns:
            Processing summary with chunks_count and processed status

        Raises:
            ValueError: If document is empty or parsing fails
        """
        # 1. Parse document
        text = await parse_document(file_path, file_type)

        if not text.strip():
            raise ValueError("Document is empty or could not be parsed")

        # 2. Chunking
        chunks = self.splitter.split_text(text)

        if not chunks:
            raise ValueError("No chunks created from document")

        # 3. Generate embeddings in batch
        embeddings = await self.embedding_service.generate_embeddings_batch(chunks)

        # 4. Save chunks to knowledge_base
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            kb_entry = MarketingKnowledgeBase(
                project_id=project_id,
                chat_id=chat_id,
                content_type='user_document',
                source_title=source_title,
                chunk_text=chunk,
                chunk_index=i,
                metadata={
                    'document_id': str(document_id),
                    'file_type': file_type,
                    'total_chunks': len(chunks),
                },
                embedding=embedding
            )
            self.db.add(kb_entry)

        # 5. Update document metadata
        doc = await self.db.get(MarketingUserDocument, document_id)
        if doc:
            doc.processed = True
            doc.chunks_count = len(chunks)

        await self.db.flush()

        return {
            'chunks_count': len(chunks),
            'processed': True
        }
