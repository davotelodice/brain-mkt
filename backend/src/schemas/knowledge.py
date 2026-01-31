"""Pydantic schemas for Book Learning System."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ConceptExtraction(BaseModel):
    """Conceptos extraídos de un chunk de libro."""
    main_concepts: list[str] = Field(default_factory=list, max_length=5)
    relationships: list[str] = Field(default_factory=list)
    key_examples: list[str] = Field(default_factory=list)
    technical_terms: dict[str, str] = Field(default_factory=dict)
    condensed_text: str = Field(default="", max_length=2000)

    @classmethod
    def parse_from_llm_response(cls, response: str) -> "ConceptExtraction":
        """Parse LLM JSON response to ConceptExtraction.
        
        GOTCHA: LLM puede generar JSON inválido, usar fallback.
        """
        import json
        try:
            # Intentar extraer JSON del response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                return cls(**data)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Fallback: usar response como condensed_text
        return cls(
            main_concepts=["Concepto no extraído correctamente"],
            condensed_text=response[:2000] if response else ""
        )


class ThematicSummary(BaseModel):
    """Resumen temático de un grupo de chunks."""
    theme: str
    summary: str
    related_concepts: list[str] = Field(default_factory=list)
    chunk_indices: list[int] = Field(default_factory=list)


class BookProcessingStatus(BaseModel):
    """Estado de procesamiento de un libro."""
    id: UUID
    status: str = Field(validation_alias="processing_status")  # Lee processing_status del ORM
    processed_chunks: int
    total_chunks: Optional[int] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class LearnedBookResponse(BaseModel):
    """Respuesta con información de libro procesado."""
    id: UUID
    title: str
    author: Optional[str] = None
    status: str = Field(validation_alias="processing_status")  # Lee processing_status del ORM
    total_chunks: Optional[int] = None
    processed_chunks: int = 0
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class LearnedBookCreate(BaseModel):
    """Request para subir libro."""
    title: str = Field(..., min_length=1, max_length=500)
    author: Optional[str] = Field(None, max_length=255)


class ConceptSearchResult(BaseModel):
    """Resultado de búsqueda de conceptos."""
    id: UUID
    book_title: str
    chunk_index: int
    main_concepts: list[str]
    condensed_text: str
    similarity_score: float
