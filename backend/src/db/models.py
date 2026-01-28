"""SQLAlchemy models for all marketing_* tables."""
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class MarketingProject(Base):
    """Projects table (multi-tenancy)."""
    __tablename__ = 'marketing_projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class MarketingUser(Base):
    """Users table (manual authentication)."""
    __tablename__ = 'marketing_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_login = Column(TIMESTAMP)


class MarketingChat(Base):
    """Chats table."""
    __tablename__ = 'marketing_chats'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), default="New Chat", nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class MarketingMessage(Base):
    """Messages table."""
    __tablename__ = 'marketing_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    role = Column(String(20), CheckConstraint("role IN ('user', 'assistant', 'system')"), nullable=False)
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSONB, default={})  # Renamed to avoid SQLAlchemy reserved name
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class MarketingBuyerPersona(Base):
    """Buyer personas table."""
    __tablename__ = 'marketing_buyer_personas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    initial_questions = Column(JSONB, nullable=False)
    full_analysis = Column(JSONB, nullable=False)
    forum_simulation = Column(JSONB, nullable=False)
    pain_points = Column(JSONB, nullable=False)
    customer_journey = Column(JSONB, nullable=False)
    embedding = Column(Vector(1536))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class MarketingKnowledgeBase(Base):
    """Knowledge base table (global + user documents)."""
    __tablename__ = 'marketing_knowledge_base'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'))
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'))
    content_type = Column(
        String(50),
        CheckConstraint("content_type IN ('video_transcript', 'book', 'user_document')"),
        nullable=False
    )
    source_title = Column(String(500), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    metadata_ = Column("metadata", JSONB, default={})  # Renamed to avoid SQLAlchemy reserved name
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class MarketingUserDocument(Base):
    """User documents table (tracking uploaded files)."""
    __tablename__ = 'marketing_user_documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(10), CheckConstraint("file_type IN ('.txt', '.pdf', '.docx')"), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(1000), nullable=False)
    summary = Column(Text)  # Nullable; requires DB migration 002_add_user_document_summary.sql
    chunks_count = Column(Integer, default=0, nullable=False)
    processed = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class MarketingPasswordResetToken(Base):
    """Password reset tokens table."""
    __tablename__ = 'marketing_password_reset_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
