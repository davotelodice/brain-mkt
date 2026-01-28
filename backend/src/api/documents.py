"""Documents API endpoints."""
import os
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..db.models import MarketingUser, MarketingUserDocument
from ..middleware.auth import get_current_user
from ..schemas.documents import (
    ALLOWED_FILE_TYPES,
    MAX_FILE_SIZE,
    DocumentMetadata,
    ListDocumentsResponse,
    UploadDocumentResponse,
)
from ..services.chat_service import ChatService
from ..services.document_processor import DocumentProcessor
from ..services.embedding_service import EmbeddingService
from ..services.llm_service import LLMService
from ..utils.file_parsers import parse_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Storage directory
STORAGE_PATH = Path(os.getenv("STORAGE_PATH", "./storage"))
STORAGE_PATH.mkdir(parents=True, exist_ok=True)


@router.post("/upload/{chat_id}", response_model=UploadDocumentResponse)
async def upload_document(
    chat_id: UUID,
    file: UploadFile = File(...),
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UploadDocumentResponse:
    """Upload document to chat.

    Args:
        chat_id: Chat ID
        file: Uploaded file
        user: Current authenticated user
        db: Database session

    Returns:
        Document metadata

    Raises:
        HTTPException: If file type or size invalid, or chat not found
    """
    # 1. Validate chat ownership
    chat_service = ChatService(db)
    await chat_service.get_chat(chat_id, user.id, user.project_id)

    # 2. Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Allowed: {ALLOWED_FILE_TYPES}"
        )

    # 3. Read and validate file size
    content = await file.read()
    file_size = len(content)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    # 4. Save file to storage
    doc_record = MarketingUserDocument(
        chat_id=chat_id,
        project_id=user.project_id,
        user_id=user.id,
        filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        file_path="",  # Will update after saving
        processed=False,
        summary=None
    )
    db.add(doc_record)
    await db.flush()

    # Save to disk
    file_storage_path = STORAGE_PATH / str(user.project_id) / str(chat_id)
    file_storage_path.mkdir(parents=True, exist_ok=True)

    file_full_path = file_storage_path / f"{doc_record.id}{file_ext}"
    with open(file_full_path, 'wb') as f:
        f.write(content)

    # Update path in database
    doc_record.file_path = str(file_full_path)
    await db.flush()

    # 4.1 Generate and persist summary (contexto largo)
    try:
        text = await parse_document(file_full_path, file_ext)
        text = (text or "").strip()
        if text:
            sample = text[:6000]
            llm = LLMService()
            summary = await llm.generate(
                prompt=(
                    "Resume este documento en español, en 6-10 viñetas, "
                    "enfocado a marketing/negocio. Incluye datos, claims, "
                    "audiencia, objeciones y tono si existen.\n\n"
                    f"DOCUMENTO:\n{sample}"
                ),
                max_tokens=400,
                temperature=0.2
            )
            doc_record.summary = summary.strip() if summary else None
            await db.flush()
    except Exception:
        # No bloquear upload si falla el resumen
        pass

    # 5. Process document asynchronously (in background)
    # TODO: Move to background task in production
    embedding_service = EmbeddingService()
    processor = DocumentProcessor(db, embedding_service)

    try:
        await processor.process_document(
            document_id=doc_record.id,
            file_path=file_full_path,
            file_type=file_ext,
            chat_id=chat_id,
            project_id=user.project_id,
            source_title=file.filename
        )
    except Exception as e:
        # Mark as failed but don't block response
        doc_record.processed = False
        await db.flush()
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

    return UploadDocumentResponse(
        id=doc_record.id,
        filename=doc_record.filename,
        file_type=doc_record.file_type,
        file_size=doc_record.file_size,
        processed=doc_record.processed,
        summary=doc_record.summary,
        created_at=doc_record.created_at
    )


@router.get("/chat/{chat_id}", response_model=ListDocumentsResponse)
async def list_documents(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ListDocumentsResponse:
    """List documents in chat.

    Args:
        chat_id: Chat ID
        user: Current authenticated user
        db: Database session

    Returns:
        List of documents with metadata
    """
    # Validate chat ownership
    chat_service = ChatService(db)
    await chat_service.get_chat(chat_id, user.id, user.project_id)

    # Get documents
    query = select(MarketingUserDocument).where(
        MarketingUserDocument.chat_id == chat_id,
        MarketingUserDocument.project_id == user.project_id
    ).order_by(MarketingUserDocument.created_at.desc())

    result = await db.execute(query)
    documents = result.scalars().all()

    return ListDocumentsResponse(
        documents=[
            DocumentMetadata(
                id=doc.id,
                filename=doc.filename,
                file_type=doc.file_type,
                file_size=doc.file_size,
                chunks_count=doc.chunks_count,
                processed=doc.processed,
                summary=doc.summary,
                created_at=doc.created_at
            )
            for doc in documents
        ],
        total=len(documents)
    )


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete document and associated chunks.

    Args:
        document_id: Document ID
        user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If document not found or not owned by user
    """
    # Get document
    query = select(MarketingUserDocument).where(
        MarketingUserDocument.id == document_id,
        MarketingUserDocument.user_id == user.id,
        MarketingUserDocument.project_id == user.project_id
    )
    result = await db.execute(query)
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from storage
    file_path = Path(doc.file_path)
    if file_path.exists():
        file_path.unlink()

    # Delete from database (cascades to knowledge_base chunks)
    await db.delete(doc)
    await db.flush()
