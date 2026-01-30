"""Book Learning Service - Pipeline de aprendizaje progresivo desde libros."""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingBookConcept, MarketingLearnedBook
from ..schemas.knowledge import ConceptExtraction
from ..services.embedding_service import EmbeddingService
from ..services.llm_service import LLMService
from ..utils.file_parsers import parse_document

logger = logging.getLogger(__name__)


class BookLearningService:
    """
    Orquesta el pipeline de aprendizaje progresivo desde libros.
    
    CRÍTICO: Este servicio ORQUESTA, no reimplementa.
    Usa servicios existentes (LLMService, EmbeddingService) para cada operación.
    
    Pipeline:
    1. Parsear documento → texto
    2. Chunking con overlap → chunks
    3. Extraer conceptos por chunk (LLM) → ConceptExtraction
    4. Generar resumen global (LLM)
    5. Generar embeddings (batch)
    6. Guardar en BD
    """

    def __init__(
        self,
        db: AsyncSession,
        llm_service: LLMService,
        embedding_service: EmbeddingService
    ):
        """Initialize book learning service.
        
        Args:
            db: Database session
            llm_service: Service for LLM calls (REUTILIZAR)
            embedding_service: Service for embeddings (REUTILIZAR)
        """
        self.db = db
        self.llm = llm_service
        self.embeddings = embedding_service
        # PATRÓN: Usar mismo estilo que DocumentProcessor
        self.chunker = RecursiveCharacterTextSplitter(
            chunk_size=1500,  # Más grande para libros (mejor contexto)
            chunk_overlap=200,  # CRÍTICO: overlap para no perder conceptos
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    async def process_book(
        self,
        file_path: str,
        project_id: UUID,
        title: str,
        author: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> MarketingLearnedBook:
        """
        Pipeline completo de aprendizaje progresivo.
        
        GOTCHA: Procesar en batches de 10 chunks para evitar rate limits.
        GOTCHA: Guardar progreso en DB para recuperación ante fallos.
        
        Args:
            file_path: Path al archivo temporal
            project_id: Project ID (aislamiento)
            title: Título del libro
            author: Autor (opcional)
            file_type: Tipo de archivo (.pdf, .txt, .docx)
            
        Returns:
            MarketingLearnedBook con estado final
        """
        # Detectar file_type si no se proporciona
        if not file_type:
            file_type = Path(file_path).suffix.lower()
        
        # 1. Crear registro inicial
        learned_book = MarketingLearnedBook(
            project_id=project_id,
            title=title,
            author=author,
            file_path=file_path,
            file_type=file_type,
            processing_status="processing"
        )
        self.db.add(learned_book)
        await self.db.flush()  # Obtener ID
        
        logger.info(
            "[BOOK] start book_id=%s title=%s",
            str(learned_book.id), title
        )
        
        try:
            # 2. Extraer texto
            raw_text = await self._extract_text(file_path, file_type)
            
            if not raw_text.strip():
                raise ValueError("Document is empty or could not be parsed")
            
            # 3. Chunking
            chunks = self.chunker.split_text(raw_text)
            learned_book.total_chunks = len(chunks)
            await self.db.flush()
            
            logger.info(
                "[BOOK] chunks book_id=%s total=%s",
                str(learned_book.id), len(chunks)
            )
            
            # 4. CAPA 1: Extraer conceptos por chunk (en batches)
            chunk_concepts: list[ConceptExtraction] = []
            batch_size = 10
            
            for batch_start in range(0, len(chunks), batch_size):
                batch_end = min(batch_start + batch_size, len(chunks))
                batch = chunks[batch_start:batch_end]
                
                for i, chunk in enumerate(batch):
                    chunk_index = batch_start + i
                    concepts = await self._extract_concepts_from_chunk(chunk, chunk_index)
                    chunk_concepts.append(concepts)
                    
                    # Actualizar progreso
                    learned_book.processed_chunks = chunk_index + 1
                    await self.db.flush()
                
                logger.info(
                    "[BOOK] batch book_id=%s processed=%s/%s",
                    str(learned_book.id), batch_end, len(chunks)
                )
            
            # 5. CAPA 2: Generar resumen global
            global_summary = await self._generate_global_summary(chunk_concepts, title)
            learned_book.global_summary = {"summary": global_summary}
            
            # 6. Generar embeddings para conceptos
            concept_texts = [c.condensed_text for c in chunk_concepts if c.condensed_text]
            embeddings = await self.embeddings.generate_embeddings_batch(concept_texts)
            
            # 7. Guardar conceptos en BD
            await self._save_concepts(learned_book.id, chunk_concepts, embeddings)
            
            # 8. Marcar como completado
            learned_book.processing_status = "completed"
            learned_book.completed_at = datetime.utcnow()
            await self.db.flush()
            
            logger.info(
                "[BOOK] completed book_id=%s concepts=%s",
                str(learned_book.id), len(chunk_concepts)
            )
            
            return learned_book
            
        except Exception as e:
            logger.error(
                "[BOOK] failed book_id=%s error=%s",
                str(learned_book.id), str(e)
            )
            learned_book.processing_status = "failed"
            await self.db.flush()
            raise

    async def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from document file.
        
        REUTILIZA: parse_document de utils.file_parsers
        """
        return await parse_document(Path(file_path), file_type)

    async def _extract_concepts_from_chunk(
        self,
        chunk: str,
        chunk_index: int
    ) -> ConceptExtraction:
        """
        Usa LLM para extraer conceptos clave de un chunk.
        
        CRÍTICO: Esto NO es un resumen. Es una destilación semántica.
        """
        prompt = f"""Eres un experto analizando libros de marketing y negocios.
Tu tarea es extraer los conceptos MÁS IMPORTANTES de este fragmento.

NO hagas un resumen genérico. Extrae CONCEPTOS CLAVE que un estudiante debería recordar.

Fragmento (chunk {chunk_index}):
---
{chunk}
---

Extrae en formato JSON (SOLO JSON, sin explicaciones):
{{
    "main_concepts": ["concepto1", "concepto2", ...],
    "relationships": ["concepto1 causa concepto2", ...],
    "key_examples": ["ejemplo concreto 1", ...],
    "technical_terms": {{"término": "definición breve", ...}},
    "condensed_text": "Resumen de 200-300 palabras con los puntos clave del fragmento"
}}

REGLAS:
- Máximo 5 conceptos principales
- Ejemplos deben ser específicos, no genéricos
- condensed_text debe capturar la esencia del fragmento
- Si no hay conceptos claros, extraer ideas principales"""

        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.3  # Baja para extracción precisa
        )
        
        return ConceptExtraction.parse_from_llm_response(response)

    async def _generate_global_summary(
        self,
        concepts: list[ConceptExtraction],
        book_title: str
    ) -> str:
        """
        Genera resumen global del libro basado en conceptos extraídos.
        
        PATRÓN: Similar a MemoryManager.get_training_summary()
        """
        # Combinar conceptos principales
        all_concepts = []
        for c in concepts[:30]:  # Limitar para no exceder contexto
            all_concepts.extend(c.main_concepts[:3])
        
        unique_concepts = list(set(all_concepts))[:20]
        
        prompt = f"""Analiza estos conceptos extraídos del libro "{book_title}":

CONCEPTOS PRINCIPALES:
{chr(10).join(f"- {c}" for c in unique_concepts)}

Genera un resumen ejecutivo del libro (máximo 500 palabras) que:
1. Identifique el TEMA CENTRAL del libro
2. Liste los 3-5 CONCEPTOS CLAVE más importantes
3. Describa las RELACIONES entre conceptos
4. Incluya APLICACIONES PRÁCTICAS

Formato: Texto claro y estructurado, listo para usar como referencia rápida."""

        summary = await self.llm.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=700
        )
        
        return summary

    async def _save_concepts(
        self,
        book_id: UUID,
        concepts: list[ConceptExtraction],
        embeddings: list[list[float]]
    ) -> None:
        """Save extracted concepts to database."""
        for i, (concept, embedding) in enumerate(zip(concepts, embeddings)):
            db_concept = MarketingBookConcept(
                learned_book_id=book_id,
                chunk_index=i,
                main_concepts=concept.main_concepts,
                relationships=concept.relationships,
                key_examples=concept.key_examples,
                technical_terms=concept.technical_terms,
                condensed_text=concept.condensed_text,
                embedding=embedding
            )
            self.db.add(db_concept)
        
        await self.db.flush()

    async def get_book_status(self, book_id: UUID) -> Optional[MarketingLearnedBook]:
        """Get book processing status."""
        return await self.db.get(MarketingLearnedBook, book_id)
