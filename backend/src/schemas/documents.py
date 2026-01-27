"""Pydantic schemas for document processing."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    """Upload document response."""
    id: UUID
    filename: str
    file_type: str
    file_size: int
    processed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentMetadata(BaseModel):
    """Document metadata."""
    id: UUID
    filename: str
    file_type: str
    file_size: int
    chunks_count: int
    processed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ListDocumentsResponse(BaseModel):
    """List documents response."""
    documents: list[DocumentMetadata]
    total: int


class ProcessDocumentResponse(BaseModel):
    """Document processing response."""
    document_id: UUID
    chunks_count: int
    processed: bool
    message: str


# Constants
ALLOWED_FILE_TYPES = {'.txt', '.pdf', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
