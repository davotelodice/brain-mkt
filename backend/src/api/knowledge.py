"""Knowledge API endpoints - Book Learning System."""
import os
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..db.models import MarketingLearnedBook, MarketingUser
from ..middleware.auth import get_current_user
from ..schemas.knowledge import (
    BookProcessingStatus,
    LearnedBookCreate,
    LearnedBookResponse,
)
from ..services.book_learning_service import BookLearningService
from ..services.embedding_service import EmbeddingService
from ..services.llm_service import LLMService

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# Allowed file types for books
ALLOWED_BOOK_TYPES = [".pdf", ".txt", ".docx"]
MAX_BOOK_SIZE = 50 * 1024 * 1024  # 50MB

# Temp storage for uploads
TEMP_PATH = Path(os.getenv("TEMP_PATH", "/tmp/book_uploads"))
TEMP_PATH.mkdir(parents=True, exist_ok=True)


async def _process_book_background(
    db: AsyncSession,
    file_path: str,
    project_id: UUID,
    title: str,
    author: Optional[str] = None,
    book_id: Optional[UUID] = None  # FIX: Pasar book_id existente
) -> None:
    """Background task for book processing.
    
    GOTCHA: Background tasks need fresh service instances.
    FIX: Ahora recibe book_id para reutilizar registro existente.
    """
    llm_service = LLMService()
    embedding_service = EmbeddingService()
    book_service = BookLearningService(db, llm_service, embedding_service)
    
    try:
        await book_service.process_book(
            file_path=file_path,
            project_id=project_id,
            title=title,
            author=author,
            book_id=book_id  # FIX: Pasar book_id
        )
    finally:
        # Cleanup temp file
        try:
            Path(file_path).unlink(missing_ok=True)
        except Exception:
            pass


@router.post("/books/upload", response_model=LearnedBookResponse)
async def upload_book_for_learning(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Book file (.pdf, .txt, .docx)"),
    title: str = Query(..., min_length=1, max_length=500, description="Book title"),
    author: Optional[str] = Query(None, max_length=255, description="Book author"),
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> LearnedBookResponse:
    """Upload a book for progressive learning.
    
    Processing is asynchronous. Use GET /books/{book_id}/status to check progress.
    
    - **file**: Book file (PDF, TXT, or DOCX, max 50MB)
    - **title**: Book title
    - **author**: Optional book author
    """
    # 1. Validate file type
    file_ext = Path(file.filename or "").suffix.lower()
    if file_ext not in ALLOWED_BOOK_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Use: {ALLOWED_BOOK_TYPES}"
        )
    
    # 2. Read and validate size
    content = await file.read()
    if len(content) > MAX_BOOK_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max: {MAX_BOOK_SIZE // (1024*1024)}MB"
        )
    
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    # 3. Create initial record
    learned_book = MarketingLearnedBook(
        project_id=user.project_id,
        title=title,
        author=author,
        file_type=file_ext,
        processing_status="pending"
    )
    db.add(learned_book)
    await db.flush()
    
    # 4. Save temp file
    temp_file_path = TEMP_PATH / f"{learned_book.id}{file_ext}"
    with open(temp_file_path, "wb") as f:
        f.write(content)
    
    learned_book.file_path = str(temp_file_path)
    await db.flush()
    
    # 5. Add background task
    # PATRÓN: FastAPI BackgroundTasks - retorna inmediatamente
    # FIX: Pasar book_id para reutilizar el registro creado
    background_tasks.add_task(
        _process_book_background,
        db=db,
        file_path=str(temp_file_path),
        project_id=user.project_id,
        title=title,
        author=author,
        book_id=learned_book.id  # FIX: Pasar el ID del libro creado
    )
    
    # Update status to processing
    learned_book.processing_status = "processing"
    await db.commit()
    
    return LearnedBookResponse(
        id=learned_book.id,
        title=learned_book.title,
        author=learned_book.author,
        status=learned_book.processing_status,
        total_chunks=learned_book.total_chunks,
        processed_chunks=learned_book.processed_chunks or 0,
        created_at=learned_book.created_at,
        completed_at=learned_book.completed_at
    )


@router.get("/books/{book_id}/status", response_model=BookProcessingStatus)
async def get_book_processing_status(
    book_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BookProcessingStatus:
    """Get book processing status.
    
    Returns current progress including processed/total chunks.
    """
    book = await db.get(MarketingLearnedBook, book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Verify ownership
    if book.project_id != user.project_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return BookProcessingStatus(
        id=book.id,
        status=book.processing_status,
        processed_chunks=book.processed_chunks or 0,
        total_chunks=book.total_chunks,
        completed_at=book.completed_at
    )


@router.get("/books", response_model=list[LearnedBookResponse])
async def list_learned_books(
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100)
) -> list[LearnedBookResponse]:
    """List all learned books for current project."""
    query = select(MarketingLearnedBook).where(
        MarketingLearnedBook.project_id == user.project_id
    )
    
    if status:
        query = query.where(MarketingLearnedBook.processing_status == status)
    
    query = query.order_by(MarketingLearnedBook.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    books = result.scalars().all()
    
    return [
        LearnedBookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            status=book.processing_status,
            total_chunks=book.total_chunks,
            processed_chunks=book.processed_chunks or 0,
            created_at=book.created_at,
            completed_at=book.completed_at
        )
        for book in books
    ]


@router.delete("/books/{book_id}")
async def delete_learned_book(
    book_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Delete a learned book and its concepts.
    
    CASCADE delete removes all associated concepts automatically.
    """
    book = await db.get(MarketingLearnedBook, book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.project_id != user.project_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Delete file if exists
    if book.file_path:
        try:
            Path(book.file_path).unlink(missing_ok=True)
        except Exception:
            pass
    
    await db.delete(book)
    await db.commit()
    
    return {"message": "Book deleted successfully", "id": str(book_id)}
