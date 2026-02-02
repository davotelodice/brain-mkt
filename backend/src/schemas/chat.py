"""Pydantic schemas for chat system."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    """Create new chat request."""
    title: str | None = Field("New Chat", description="Chat title")


class CreateChatResponse(BaseModel):
    """Create chat response."""
    id: UUID
    title: str
    created_at: datetime


class UpdateChatTitleRequest(BaseModel):
    """Update chat title request."""
    title: str = Field(..., min_length=1, max_length=255)


class SendMessageRequest(BaseModel):
    """Send message request."""
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    model: str | None = Field(None, description="LLM model override (e.g., 'gpt-4o-mini')")
    attachment_content: str | None = Field(
        None,
        max_length=50000,
        description="Contenido del archivo adjunto (texto plano, max 50k chars)"
    )


class Message(BaseModel):
    """Message model."""
    id: UUID
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    metadata: dict[str, str] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSummary(BaseModel):
    """Chat summary (without messages)."""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int | None = None

    class Config:
        from_attributes = True


class ChatWithMessages(BaseModel):
    """Chat with full message history."""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[Message]

    class Config:
        from_attributes = True
