"""SQLAlchemy models for all marketing_* tables."""
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    ARRAY,
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
from sqlalchemy.orm import relationship

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
    
    # Columnas nuevas para Book Learning System (migración 003)
    knowledge_type = Column(String(50), default='raw_chunk')  # raw_chunk, extracted_concept, thematic_summary
    learned_book_id = Column(UUID(as_uuid=True), ForeignKey('marketing_learned_books.id', ondelete='CASCADE'))


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


# ========================================
# BOOK LEARNING SYSTEM - Migración 003
# ========================================

class MarketingLearnedBook(Base):
    """Learned books table - metadata de libros procesados para aprendizaje."""
    __tablename__ = 'marketing_learned_books'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(500), nullable=False)
    author = Column(String(255))
    file_path = Column(String(1000))
    file_type = Column(String(10))
    processing_status = Column(
        String(50),
        CheckConstraint("processing_status IN ('pending', 'processing', 'completed', 'failed')"),
        default='pending'
    )
    total_chunks = Column(Integer)
    processed_chunks = Column(Integer, default=0)
    global_summary = Column(JSONB)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP)

    # Relationships
    project = relationship("MarketingProject", backref="learned_books")
    concepts = relationship("MarketingBookConcept", back_populates="book", cascade="all, delete-orphan")


class MarketingBookConcept(Base):
    """Book concepts table - conceptos extraídos de chunks de libros."""
    __tablename__ = 'marketing_book_concepts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learned_book_id = Column(UUID(as_uuid=True), ForeignKey('marketing_learned_books.id', ondelete='CASCADE'), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    main_concepts = Column(ARRAY(String))  # Array de conceptos principales
    relationships = Column(ARRAY(String))  # Relaciones entre conceptos
    key_examples = Column(ARRAY(String))   # Ejemplos clave
    technical_terms = Column(JSONB)        # Términos técnicos con definiciones
    condensed_text = Column(Text)          # Texto condensado para embedding
    embedding = Column(Vector(1536))       # Vector embedding del concepto
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    book = relationship("MarketingLearnedBook", back_populates="concepts")
