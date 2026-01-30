# PRP: Sistema de Aprendizaje Progresivo desde Libros

## 📋 METADATA

```yaml
nombre: "Book Learning System"
version: "3.0.0"
fecha: "2026-01-30"
descripcion: "Sistema de aprendizaje progresivo que permite al agente 'estudiar' libros completos"
tipo: "Feature Addition"
proyecto_base: "Marketing Second Brain (EXISTENTE)"
score_confianza: "9/10"
```

---

## 🎯 OBJETIVO

Agregar un sistema de "aprendizaje progresivo" al proyecto Marketing Brain existente que permita:
1. Subir libros completos (.pdf, .txt, .docx)
2. Procesarlos con LLM para extraer conceptos clave (no almacenamiento crudo)
3. Almacenar conocimiento estructurado en 3 capas
4. Integrar con agentes existentes para respuestas más ricas

**⚠️ CRÍTICO**: Este módulo **EXTIENDE** el sistema existente, **NO LO REEMPLAZA**.

---

## 🚨 FUNCIONALIDAD EXISTENTE - NO DUPLICAR

### YA EXISTE en LLMService (NO recrear):
```yaml
generate_with_messages(messages: list):
  Líneas: 141-197
  Estado: ✅ YA IMPLEMENTADO
  Uso: Para llamadas con historial

stream_with_messages(messages: list):
  Líneas: 199-255
  Estado: ✅ YA IMPLEMENTADO
  Uso: Para streaming con historial
```

### YA EXISTE en MemoryManager (REUTILIZAR):
```yaml
format_messages_from_memory():
  Líneas: 142-199
  Estado: ✅ YA IMPLEMENTADO
  Uso: Convierte historial a formato OpenAI messages[]

get_training_summary():
  Líneas: 201-296
  Estado: ✅ YA IMPLEMENTADO
  ⭐ PATRÓN A SEGUIR para conceptos aprendidos
  
get_context():
  Líneas: 52-121
  Estado: ✅ YA IMPLEMENTADO
  Acción: EXTENDER para incluir conceptos aprendidos
```

### NO EXISTE y NO SE CREARÁ:
```yaml
GeneralChatAgent:
  Estado: ❌ NO EXISTE
  Razón: Estrategia cambió (ver PRP marketing-brain-conversational-agent-v3.md)
  Decisión: NO crear - mejorar ContentGeneratorAgent en su lugar
```

---

## 🔍 ANÁLISIS DEL PROYECTO EXISTENTE (Con MCP Serena)

### Servicios a REUTILIZAR (No duplicar)

```yaml
RAGService (backend/src/services/rag_service.py):
  Líneas: 14-351
  Métodos disponibles:
    - search_relevant_docs() → Búsqueda semántica híbrida
    - _vector_search() → Búsqueda vectorial directa
    - _rerank_with_llm() → Reranking con LLM
    - search_by_chat() → Búsqueda por chat_id
  Variables:
    - db, embedding_service, llm_service
  
  USO: Extender con search_learned_concepts(), NO reescribir

LLMService (backend/src/services/llm_service.py):
  Líneas: 15-255
  Métodos disponibles:
    - generate(prompt, temperature) → Generación simple
    - stream() → Streaming de respuesta
    - generate_with_messages() → Con historial (✅ YA EXISTE)
    - stream_with_messages() → Streaming con historial (✅ YA EXISTE)
  
  USO: Usar generate() para extracción de conceptos
  ⚠️ NO recrear generate_with_messages - YA EXISTE

MemoryManager (backend/src/services/memory_manager.py):
  Líneas: 17-421
  Métodos disponibles:
    - get_context() → Contexto completo para agentes (EXTENDER)
    - format_messages_from_memory() → Convierte historial a messages[] (✅ YA EXISTE)
    - get_training_summary() → Resumen de transcripciones (⭐ PATRÓN A SEGUIR)
    - load_chat_history() → Carga historial de BD
    - ensure_chat_loaded() → Verifica carga
  
  USO: 
    - SEGUIR PATRÓN de get_training_summary() para conceptos
    - EXTENDER get_context() para incluir conceptos aprendidos
    - NO duplicar lógica de historial

EmbeddingService (backend/src/services/embedding_service.py):
  Líneas: 6-59
  Métodos disponibles:
    - generate_embedding(text) → Embedding individual
    - generate_embeddings_batch(texts) → Batch processing
  Variables:
    - batch_size (para rate limiting)
  
  USO: Usar generate_embeddings_batch() para conceptos

DocumentProcessor (backend/src/services/document_processor.py):
  Líneas: 12-100
  Métodos disponibles:
    - process_document() → Parsea .txt, .pdf, .docx
  Variables:
    - splitter (RecursiveCharacterTextSplitter)
  
  USO: Reutilizar lógica de parsing, NO duplicar
```

### Modelos de BD Existentes

```yaml
Tablas con prefijo marketing_:
  - MarketingProject
  - MarketingUser
  - MarketingChat
  - MarketingMessage
  - MarketingBuyerPersona
  - MarketingKnowledgeBase ← EXTENDER con columnas nuevas
  - MarketingUserDocument
  - MarketingPasswordResetToken

Migraciones existentes:
  - 001_initial_schema.sql
  - 002_add_user_document_summary.sql
  
SIGUIENTE: 003_book_learning_system.sql
```

### Comandos Serena para Verificación

```bash
# Antes de codificar, ejecutar:
get_symbols_overview('backend/src/services/rag_service.py')
find_symbol('RAGService/search_relevant_docs', 'backend/src/services/rag_service.py', True)
find_symbol('DocumentProcessor/process_document', 'backend/src/services/document_processor.py', True)
get_symbols_overview('backend/src/db/models.py')
```

---

## 📚 DOCUMENTACIÓN CONSULTADA (MCP Archon)

### Fuentes Disponibles

```yaml
LangChain (source_id: e74f94bb9dcb14aa):
  - Text splitters: https://docs.langchain.com/oss/python/integrations/splitters/index.md
  - RAG patterns: https://docs.langchain.com/oss/python/langchain/rag.md
  Query usada: "langchain text splitter recursive character chunking overlap"

FastAPI (source_id: c889b62860c33a44):
  - Background tasks: https://fastapi.tiangolo.com/tutorial/background-tasks
  - Async patterns: https://fastapi.tiangolo.com/async
  Query usada: "FastAPI background tasks async processing"

Supabase (source_id: 9c5f534e51ee9237):
  - pgvector: https://supabase.com/llms/guides.txt
  Query usada: "pgvector similarity search embeddings"

Pydantic (source_id: 9d46e91458092424):
  - Validación de JSON desde LLM
  Query: "pydantic model validation json parsing"
```

---

## 📖 SKILLS A UTILIZAR

### Por Fase del Proyecto

```yaml
FASE 0 - Análisis:
  - MCP Serena: OBLIGATORIO antes de cualquier código
  - Skill: architecture (decisiones de integración)

FASE 1 - Base de Datos:
  - MCP Serena: Ver models.py existente
  - Skill: database-design (migraciones)

FASE 2 - BookLearningService:
  - MCP Archon: "langchain text splitter" (source: e74f94bb9dcb14aa)
  - Skill: python-patterns (automático)
  - Skill: clean-code (automático)
  - Skill: rag-implementation (extender RAG)

FASE 3 - API Endpoints:
  - MCP Archon: "FastAPI background tasks" (source: c889b62860c33a44)
  - MCP Serena: Ver estructura de chat.py, documents.py
  - Skill: api-patterns

FASE 4 - Integración RAG:
  - MCP Archon: "pgvector similarity" (source: 9c5f534e51ee9237)
  - MCP Serena: Leer RAGService completo antes de modificar
  - Skill: rag-implementation

FASE 5 - Agentes:
  - MCP Serena: Ver ContentGeneratorAgent, GeneralChatAgent
  - Skill: agent-memory-systems

FASE 6 - Frontend:
  - MCP Serena: Ver Sidebar.tsx, ChatInterface.tsx
  - Skill: react-patterns (automático)
  - Skill: nextjs-best-practices (automático)

FASE 7 - Testing:
  - Skill: testing-patterns
  - Skill: verification-before-completion
```

---

## 🏗️ TAREAS

### TAREA 0: Verificación del Entorno y Análisis (⚡ OBLIGATORIA)

**Herramientas:**
- 🔧 MCP Serena: Análisis simbólico completo
- 📚 Skill: architecture

**Objetivo:** Confirmar que todo el código existente está entendido antes de escribir una línea.

**Pasos:**

1. **Activar proyecto en Serena:**
   ```bash
   activate_project("brain-mkt")
   ```

2. **Analizar servicios existentes:**
   ```bash
   # Ver todos los servicios
   get_symbols_overview('backend/src/services/rag_service.py')
   get_symbols_overview('backend/src/services/llm_service.py')
   get_symbols_overview('backend/src/services/embedding_service.py')
   get_symbols_overview('backend/src/services/document_processor.py')
   get_symbols_overview('backend/src/services/memory_manager.py')
   
   # Leer métodos clave
   find_symbol('RAGService/search_relevant_docs', 'backend/src/services/rag_service.py', True)
   find_symbol('EmbeddingService/generate_embeddings_batch', 'backend/src/services/embedding_service.py', True)
   
   # ⭐ CRÍTICO: Ver patrón a seguir
   find_symbol('MemoryManager/get_training_summary', 'backend/src/services/memory_manager.py', True)
   find_symbol('MemoryManager/get_context', 'backend/src/services/memory_manager.py', True)
   ```

3. **Analizar agentes existentes:**
   ```bash
   get_symbols_overview('backend/src/agents/content_generator_agent.py')
   # ⚠️ NO existe general_chat_agent.py - NO intentar analizar
   ```

4. **Analizar base de datos:**
   ```bash
   get_symbols_overview('backend/src/db/models.py')
   # Ver tabla marketing_knowledge_base específicamente
   find_symbol('MarketingKnowledgeBase', 'backend/src/db/models.py', True)
   ```

5. **Documentar hallazgos:**
   - Crear `docs/INTEGRATION_ANALYSIS.md` con:
     - Servicios a reutilizar
     - Código a extender
     - Código nuevo a crear

**Criterios de aceptación:**
- [ ] Serena activado en proyecto brain-mkt
- [ ] Todos los servicios analizados (incluyendo MemoryManager)
- [ ] Patrón get_training_summary() entendido y documentado
- [ ] Verificado que generate_with_messages() YA EXISTE
- [ ] Verificado que GeneralChatAgent NO existe
- [ ] INTEGRATION_ANALYSIS.md creado/actualizado
- [ ] Lista clara de "reutilizar vs extender vs crear"

---

### TAREA 1: Migración de Base de Datos

**Herramientas:**
- 🔧 MCP Serena: Ver models.py existente
- ⚡ MCP Archon: `rag_search_knowledge_base(query="sqlalchemy 2.0 relationship", source_id="...")`
- 📚 Skill: database-design

**Objetivo:** Agregar tablas y columnas necesarias SIN romper existentes.

**Pasos:**

1. **Crear migración 003:**
   ```sql
   -- backend/db/003_book_learning_system.sql
   
   -- TABLA 1: Metadata de libros procesados
   CREATE TABLE marketing_learned_books (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       project_id UUID REFERENCES marketing_projects(id) NOT NULL,
       title VARCHAR(500) NOT NULL,
       author VARCHAR(255),
       file_path VARCHAR(1000),
       file_type VARCHAR(10),
       processing_status VARCHAR(50) DEFAULT 'pending',
       total_chunks INTEGER,
       processed_chunks INTEGER DEFAULT 0,
       global_summary JSONB,
       created_at TIMESTAMP DEFAULT NOW(),
       completed_at TIMESTAMP
   );
   
   CREATE INDEX idx_learned_books_project ON marketing_learned_books(project_id);
   CREATE INDEX idx_learned_books_status ON marketing_learned_books(processing_status);
   
   -- EXTENDER tabla existente (NO crear nueva)
   ALTER TABLE marketing_knowledge_base 
   ADD COLUMN IF NOT EXISTS knowledge_type VARCHAR(50) DEFAULT 'raw_chunk';
   
   ALTER TABLE marketing_knowledge_base 
   ADD COLUMN IF NOT EXISTS learned_book_id UUID REFERENCES marketing_learned_books(id) ON DELETE CASCADE;
   
   CREATE INDEX IF NOT EXISTS idx_knowledge_type ON marketing_knowledge_base(knowledge_type);
   CREATE INDEX IF NOT EXISTS idx_learned_book ON marketing_knowledge_base(learned_book_id);
   
   -- TABLA 2: Conceptos extraídos estructurados
   CREATE TABLE marketing_book_concepts (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       learned_book_id UUID REFERENCES marketing_learned_books(id) ON DELETE CASCADE,
       chunk_index INTEGER NOT NULL,
       main_concepts TEXT[],
       relationships TEXT[],
       key_examples TEXT[],
       technical_terms JSONB,
       condensed_text TEXT,
       embedding VECTOR(1536),
       created_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_book_concepts_book ON marketing_book_concepts(learned_book_id);
   CREATE INDEX idx_book_concepts_embedding ON marketing_book_concepts 
       USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
   ```

2. **Actualizar models.py:**
   - Usar Serena para ver estructura actual:
     ```bash
     find_symbol('MarketingKnowledgeBase', 'backend/src/db/models.py', True)
     ```
   - Agregar modelos (NO modificar existentes):
     - `MarketingLearnedBook`
     - `MarketingBookConcept`
   - Extender `MarketingKnowledgeBase` con campos nuevos

3. **Ejecutar migración:**
   ```bash
   # En Supabase SQL Editor o psql
   \i backend/db/003_book_learning_system.sql
   ```

**Archivos a crear:**
- `backend/db/003_book_learning_system.sql`

**Archivos a modificar:**
- `backend/src/db/models.py` (AGREGAR modelos, no modificar existentes)

**Criterios de aceptación:**
- [ ] Migración ejecutada sin errores
- [ ] Datos existentes intactos (verificar con SELECT)
- [ ] Nuevos modelos en models.py
- [ ] Relaciones funcionando (test manual)

**Pseudocódigo:**

```python
# backend/src/db/models.py - AGREGAR (no modificar existente)

# GOTCHA: Usar Optional para campos que pueden ser NULL
# PATRÓN: Seguir estructura de modelos existentes (ver MarketingChat)

class MarketingLearnedBook(Base):
    __tablename__ = "marketing_learned_books"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("marketing_projects.id"), nullable=False)
    title = Column(String(500), nullable=False)
    author = Column(String(255))
    file_path = Column(String(1000))
    file_type = Column(String(10))
    processing_status = Column(String(50), default="pending")
    total_chunks = Column(Integer)
    processed_chunks = Column(Integer, default=0)
    global_summary = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    project = relationship("MarketingProject", back_populates="learned_books")
    concepts = relationship("MarketingBookConcept", back_populates="book", cascade="all, delete-orphan")

class MarketingBookConcept(Base):
    __tablename__ = "marketing_book_concepts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learned_book_id = Column(UUID(as_uuid=True), ForeignKey("marketing_learned_books.id", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    main_concepts = Column(ARRAY(String))
    relationships = Column(ARRAY(String))
    key_examples = Column(ARRAY(String))
    technical_terms = Column(JSONB)
    condensed_text = Column(Text)
    # GOTCHA: pgvector requiere Vector type de pgvector extension
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    book = relationship("MarketingLearnedBook", back_populates="concepts")
```

---

### TAREA 2: BookLearningService (Pipeline de Aprendizaje)

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('DocumentProcessor/process_document', '...', True)`
- ⚡ MCP Archon: `rag_search_knowledge_base(query="langchain recursive text splitter", source_id="e74f94bb9dcb14aa")`
- 📚 Skills: python-patterns, clean-code, rag-implementation

**Objetivo:** Crear servicio que orquesta aprendizaje progresivo REUTILIZANDO servicios existentes.

**Pasos:**

1. **Analizar DocumentProcessor primero:**
   ```bash
   find_symbol('DocumentProcessor/process_document', 'backend/src/services/document_processor.py', True)
   # Ver cómo hace chunking actual
   ```

2. **Crear BookLearningService:**
   - Inyectar dependencias existentes (LLMService, EmbeddingService)
   - Reutilizar RecursiveCharacterTextSplitter del DocumentProcessor
   - Implementar extracción de conceptos con LLM
   - Implementar agrupación temática
   - Implementar resumen global

3. **Crear schemas Pydantic:**
   - ConceptExtraction (main_concepts, relationships, key_examples, technical_terms)
   - ThematicSummary
   - LearnedBookResponse
   - BookProcessingStatus

**Archivos a crear:**
- `backend/src/services/book_learning_service.py`
- `backend/src/schemas/knowledge.py`

**Archivos a REUTILIZAR (NO modificar):**
- `backend/src/services/llm_service.py`
- `backend/src/services/embedding_service.py`
- `backend/src/services/document_processor.py`

**Criterios de aceptación:**
- [ ] BookLearningService instanciable
- [ ] USA LLMService.generate() (no reimplementa)
- [ ] USA EmbeddingService.generate_embeddings_batch() (no reimplementa)
- [ ] process_book() ejecuta sin errores
- [ ] Conceptos extraídos tienen formato correcto
- [ ] Datos guardados en las 3 tablas

**Pseudocódigo:**

```python
# backend/src/services/book_learning_service.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services.llm_service import LLMService
from ..services.embedding_service import EmbeddingService
from ..schemas.knowledge import ConceptExtraction, LearnedBook

class BookLearningService:
    """
    Orquesta el pipeline de aprendizaje progresivo.
    
    CRÍTICO: Este servicio ORQUESTA, no reimplementa.
    Usa servicios existentes para cada operación.
    """
    
    def __init__(
        self, 
        db: AsyncSession,
        llm_service: LLMService,  # REUTILIZAR
        embedding_service: EmbeddingService  # REUTILIZAR
    ):
        self.db = db
        self.llm = llm_service
        self.embeddings = embedding_service
        # PATRÓN: Usar mismo splitter que DocumentProcessor
        self.chunker = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    async def process_book(
        self, 
        file_path: str, 
        project_id: str,
        title: str,
        author: Optional[str] = None
    ) -> LearnedBook:
        """
        Pipeline completo de aprendizaje progresivo.
        
        GOTCHA: Procesar en batches de 10 chunks para evitar rate limits.
        GOTCHA: Guardar progreso en DB para recuperación ante fallos.
        """
        # 1. Crear registro inicial
        learned_book = MarketingLearnedBook(
            project_id=project_id,
            title=title,
            author=author,
            file_path=file_path,
            processing_status="processing"
        )
        self.db.add(learned_book)
        await self.db.commit()
        
        try:
            # 2. Extraer texto (REUTILIZAR lógica existente)
            raw_text = await self._extract_text(file_path)
            
            # 3. Chunking con overlap
            chunks = self.chunker.split_text(raw_text)
            learned_book.total_chunks = len(chunks)
            await self.db.commit()
            
            # 4. CAPA 1: Extracción de conceptos por chunk
            chunk_concepts = []
            for batch_start in range(0, len(chunks), 10):
                batch = chunks[batch_start:batch_start + 10]
                for i, chunk in enumerate(batch):
                    concepts = await self._extract_concepts_from_chunk(
                        chunk, batch_start + i
                    )
                    chunk_concepts.append(concepts)
                    learned_book.processed_chunks = batch_start + i + 1
                    await self.db.commit()
            
            # 5. CAPA 2: Resúmenes temáticos
            thematic_summaries = await self._generate_thematic_summaries(
                chunks, chunk_concepts
            )
            
            # 6. CAPA 3: Resumen global
            global_summary = await self._generate_global_summary(
                chunk_concepts, thematic_summaries
            )
            learned_book.global_summary = global_summary
            
            # 7. Generar embeddings (USAR servicio existente)
            concept_texts = [c.condensed_text for c in chunk_concepts]
            embeddings = await self.embeddings.generate_embeddings_batch(concept_texts)
            
            # 8. Guardar conceptos con embeddings
            await self._save_concepts(learned_book.id, chunk_concepts, embeddings)
            
            # 9. Marcar como completado
            learned_book.processing_status = "completed"
            learned_book.completed_at = datetime.utcnow()
            await self.db.commit()
            
            return learned_book
            
        except Exception as e:
            learned_book.processing_status = "failed"
            await self.db.commit()
            raise
    
    async def _extract_concepts_from_chunk(
        self, chunk: str, chunk_index: int
    ) -> ConceptExtraction:
        """
        Usa LLM para extraer conceptos clave.
        
        CRÍTICO: Esto NO es un resumen. Es una destilación semántica.
        """
        prompt = f"""
Eres un experto en marketing que está estudiando un libro.
Tu tarea es extraer los conceptos MÁS IMPORTANTES de este fragmento.

NO hagas un resumen. Extrae CONCEPTOS CLAVE que un estudiante debería recordar.

Fragmento (chunk {chunk_index}):
{chunk}

Extrae en formato JSON:
{{
    "main_concepts": ["concepto1", "concepto2", ...],
    "relationships": ["concepto1 causa concepto2", ...],
    "key_examples": ["ejemplo1", ...],
    "technical_terms": {{"término": "definición", ...}},
    "condensed_text": "Resumen de 200-300 palabras con los puntos clave"
}}

Sé CONCISO. Máximo 5 conceptos principales.
"""
        
        # USAR LLMService existente
        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.3  # Baja para extracción precisa
        )
        
        # GOTCHA: LLM puede fallar en formato JSON
        # Usar Pydantic para validar y retry si falla
        return ConceptExtraction.parse_from_llm_response(response)
```

---

### TAREA 3: API Endpoints

**Herramientas:**
- 🔧 MCP Serena: Ver estructura de `chat.py`, `documents.py`
- ⚡ MCP Archon: `rag_search_knowledge_base(query="FastAPI background tasks", source_id="c889b62860c33a44")`
- 📚 Skill: api-patterns

**Objetivo:** Exponer funcionalidad vía API REST.

**Pasos:**

1. **Analizar routers existentes:**
   ```bash
   get_symbols_overview('backend/src/api/chat.py')
   get_symbols_overview('backend/src/api/documents.py')
   # Ver patrón de dependencias
   ```

2. **Crear router de knowledge:**
   - POST /api/knowledge/books/upload (con background task)
   - GET /api/knowledge/books/{book_id}/status
   - GET /api/knowledge/books
   - POST /api/knowledge/concepts/search
   - DELETE /api/knowledge/books/{book_id}

3. **Registrar en main.py:**
   ```python
   from .api import knowledge
   app.include_router(knowledge.router)
   ```

**Archivos a crear:**
- `backend/src/api/knowledge.py`

**Archivos a modificar:**
- `backend/src/main.py` (include_router)

**Criterios de aceptación:**
- [ ] Endpoints registrados en /docs (Swagger)
- [ ] Upload acepta .pdf, .txt, .docx
- [ ] Background task inicia correctamente
- [ ] Status endpoint retorna progreso real
- [ ] Search retorna conceptos relevantes

**Pseudocódigo:**

```python
# backend/src/api/knowledge.py

from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks
from ..services.book_learning_service import BookLearningService
from ..middleware.auth import get_current_user

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# PATRÓN: Ver cómo documents.py maneja uploads
# GOTCHA: Usar BackgroundTasks para procesamiento largo

@router.post("/books/upload")
async def upload_book_for_learning(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    title: str,
    author: Optional[str] = None,
    current_user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sube un libro para aprendizaje.
    Procesamiento es asíncrono (background task).
    """
    # Validar tipo de archivo
    allowed_types = [".pdf", ".txt", ".docx"]
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_types:
        raise HTTPException(400, f"Tipo no permitido. Usar: {allowed_types}")
    
    # Validar tamaño (50MB max para libros)
    MAX_SIZE = 50 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "Archivo muy grande. Máximo 50MB.")
    
    # Guardar temporalmente
    temp_path = f"/tmp/{uuid.uuid4()}{ext}"
    with open(temp_path, "wb") as f:
        f.write(contents)
    
    # Crear servicio con dependencias
    llm_service = LLMService()
    embedding_service = EmbeddingService()
    book_service = BookLearningService(db, llm_service, embedding_service)
    
    # Iniciar procesamiento en background
    # GOTCHA: background_tasks NO espera, retorna inmediatamente
    background_tasks.add_task(
        book_service.process_book,
        file_path=temp_path,
        project_id=str(current_user.default_project_id),
        title=title,
        author=author
    )
    
    return {"message": "Procesamiento iniciado", "status": "processing"}

@router.get("/books/{book_id}/status")
async def get_book_status(
    book_id: str,
    current_user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BookProcessingStatus:
    """Retorna estado de procesamiento."""
    book = await db.get(MarketingLearnedBook, book_id)
    if not book:
        raise HTTPException(404, "Libro no encontrado")
    
    return BookProcessingStatus(
        status=book.processing_status,
        processed_chunks=book.processed_chunks,
        total_chunks=book.total_chunks,
        completed_at=book.completed_at
    )
```

---

### TAREA 4: Integración con RAGService

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('RAGService/search_relevant_docs', '...', True)`
- ⚡ MCP Archon: `rag_search_knowledge_base(query="pgvector cosine similarity", source_id="9c5f534e51ee9237")`
- 📚 Skill: rag-implementation

**Objetivo:** Extender RAGService para buscar en conceptos aprendidos.

**Pasos:**

1. **Leer RAGService completo:**
   ```bash
   find_symbol('RAGService', 'backend/src/services/rag_service.py', True, depth=1)
   find_symbol('RAGService/search_relevant_docs', '...', True)
   ```

2. **Agregar método search_learned_concepts():**
   - NO modificar métodos existentes
   - Agregar método nuevo que filtra por knowledge_type
   - Mantener compatibilidad total

3. **Agregar método híbrido search_with_learned_knowledge():**
   - Busca en: conceptos + documentos + knowledge base
   - Combina y rankea resultados

**Archivos a modificar:**
- `backend/src/services/rag_service.py` (AGREGAR métodos, no modificar existentes)

**Criterios de aceptación:**
- [ ] search_learned_concepts() funciona
- [ ] Métodos existentes NO modificados (diff mínimo)
- [ ] Tests existentes siguen pasando
- [ ] Performance <100ms

**Pseudocódigo:**

```python
# backend/src/services/rag_service.py - AGREGAR (no modificar existente)

class RAGService:
    # ... métodos existentes NO TOCAR ...
    
    async def search_learned_concepts(
        self,
        query: str,
        project_id: str,
        limit: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[ConceptSearchResult]:
        """
        Busca en conceptos aprendidos de libros.
        
        CRÍTICO: Este método es NUEVO, no modifica search_relevant_docs()
        """
        # Generar embedding de la query
        query_embedding = await self.embedding_service.generate_embedding(query)
        
        # GOTCHA: Filtrar por knowledge_type = 'extracted_concept'
        # Y por project_id para aislamiento
        results = await self.db.execute(
            select(MarketingBookConcept)
            .join(MarketingLearnedBook)
            .where(
                MarketingLearnedBook.project_id == project_id,
                # Usar operador de similaridad de pgvector
                MarketingBookConcept.embedding.cosine_distance(query_embedding) < (1 - similarity_threshold)
            )
            .order_by(MarketingBookConcept.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        
        return [ConceptSearchResult.from_orm(r) for r in results.scalars()]
    
    async def search_with_learned_knowledge(
        self,
        query: str,
        project_id: str,
        limit_per_type: int = 5
    ) -> HybridSearchResult:
        """
        Búsqueda híbrida: conceptos + documentos + knowledge base.
        
        Retorna resultados combinados y rankeados.
        """
        # 1. Buscar en conceptos aprendidos
        concepts = await self.search_learned_concepts(
            query, project_id, limit=limit_per_type
        )
        
        # 2. Buscar en documentos de usuario (método existente)
        docs = await self.search_relevant_docs(
            query, project_id, limit=limit_per_type
        )
        
        # 3. Buscar en knowledge base tradicional
        # REUTILIZAR método existente con filtro
        kb_results = await self._vector_search(
            query, project_id, limit=limit_per_type
        )
        
        return HybridSearchResult(
            concepts=concepts,
            documents=docs,
            knowledge_base=kb_results
        )
```

---

### TAREA 5: Integración con Agentes

**Herramientas:**
- 🔧 MCP Serena: Ver ContentGeneratorAgent y MemoryManager
- 📚 Skill: agent-memory-systems

**Objetivo:** Que ContentGeneratorAgent use conceptos aprendidos en respuestas.

**⚠️ IMPORTANTE:** 
- `GeneralChatAgent` NO EXISTE y no se creará (ver PRP marketing-brain-conversational-agent-v3.md)
- Solo modificar `ContentGeneratorAgent`
- SEGUIR PATRÓN de `MemoryManager.get_training_summary()` para inyectar conceptos

**Pasos:**

1. **Analizar agente y patrón existente:**
   ```bash
   get_symbols_overview('backend/src/agents/content_generator_agent.py')
   find_symbol('ContentGeneratorAgent/execute', '...', True)
   find_symbol('MemoryManager/get_training_summary', 'backend/src/services/memory_manager.py', True)
   ```

2. **Extender MemoryManager.get_context():**
   - Agregar llamada a `RAGService.search_learned_concepts()`
   - Incluir conceptos en contexto retornado
   - SEGUIR PATRÓN de cómo se incluye `training_summary`

3. **Modificar ContentGeneratorAgent._build_system_prompt():**
   - Incluir conceptos aprendidos del contexto
   - Agregar sección "CONOCIMIENTO APRENDIDO DE LIBROS"
   - Mantener secciones existentes (training_summary, buyer_persona, etc.)

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` (extender get_context)
- `backend/src/agents/content_generator_agent.py` (usar conceptos en prompt)

**⚠️ CRÍTICO:** 
- NO crear GeneralChatAgent
- NO reescribir agentes, solo AGREGAR funcionalidad
- SEGUIR PATRÓN existente de get_training_summary()

**Criterios de aceptación:**
- [ ] MemoryManager.get_context() incluye conceptos aprendidos
- [ ] ContentGeneratorAgent usa conceptos en system prompt
- [ ] Respuestas incluyen conocimiento de libros procesados
- [ ] Funcionalidad existente NO afectada
- [ ] Tests de agentes pasan

---

### TAREA 6: Frontend - UI para Gestión de Libros

**Herramientas:**
- 🔧 MCP Serena: Ver Sidebar.tsx, ChatInterface.tsx
- 📚 Skills: react-patterns, nextjs-best-practices

**Objetivo:** Permitir al usuario subir/gestionar libros desde UI.

**Pasos:**

1. **Analizar componentes existentes:**
   ```bash
   get_symbols_overview('frontend/app/components/Sidebar.tsx')
   get_symbols_overview('frontend/app/components/DocumentUpload.tsx')
   ```

2. **Crear componentes:**
   - BookUpload.tsx (drag & drop)
   - LearnedBookCard.tsx (tarjeta con info)
   - ConceptsViewer.tsx (visualización)

3. **Crear página:**
   - `/dashboard/knowledge/page.tsx`

4. **Integrar en Sidebar:**
   - Agregar link "Biblioteca de Conocimiento"

**Componentes a crear:**
- `frontend/app/components/BookUpload.tsx`
- `frontend/app/components/LearnedBookCard.tsx`
- `frontend/app/components/ConceptsViewer.tsx`
- `frontend/app/dashboard/knowledge/page.tsx`

**Archivos a modificar:**
- `frontend/app/components/Sidebar.tsx`
- `frontend/lib/api-chat.ts` (agregar funciones de knowledge)

**Criterios de aceptación:**
- [ ] Usuario puede subir libro
- [ ] Progress bar durante procesamiento
- [ ] Lista de libros actualizable
- [ ] UI consistente con diseño existente
- [ ] Responsive en mobile

---

### TAREA 7: Testing y Documentación

**Herramientas:**
- 📚 Skills: testing-patterns, verification-before-completion

**Objetivo:** Validar integración completa y documentar.

**Pasos:**

1. **Tests de integración:**
   - Test flujo completo: subir → procesar → buscar → responder
   - Test eliminación y cleanup

2. **Tests unitarios:**
   - BookLearningService._extract_concepts_from_chunk()
   - RAGService.search_learned_concepts()
   - Endpoints de API

3. **Documentación:**
   - `docs/BOOK_LEARNING_SYSTEM.md`
   - Actualizar README.md

**Archivos a crear:**
- `backend/tests/integration/test_book_learning.py`
- `backend/tests/unit/test_book_learning_service.py`
- `docs/BOOK_LEARNING_SYSTEM.md`

**Criterios de aceptación:**
- [ ] Coverage >80% en código nuevo
- [ ] Tests de integración pasan
- [ ] Documentación completa

**Comandos de validación:**

```bash
# Nivel 1: Sintaxis y estilo
cd backend && ruff check src/ --fix && mypy src/

# Nivel 2: Tests unitarios
pytest tests/unit/test_book_learning_service.py -v

# Nivel 3: Tests de integración
pytest tests/integration/test_book_learning.py -v

# Nivel 4: Coverage
pytest --cov=src/services/book_learning_service --cov-report=term-missing
```

---

## ⚠️ GOTCHAS CRÍTICOS

```yaml
1. LLM Context Window:
   PROBLEMA: "Chunks muy largos exceden context window"
   SOLUCIÓN: "Limitar chunks a 1500 tokens, verificar antes de enviar"
   
2. JSON Parsing:
   PROBLEMA: "LLM puede generar JSON inválido"
   SOLUCIÓN: "Usar Pydantic para validar, retry con temperatura 0.1 si falla"
   
3. Rate Limits:
   PROBLEMA: "OpenAI rate limits en embeddings batch"
   SOLUCIÓN: "Procesar en batches de 10, exponential backoff"
   
4. Overlap en Chunking:
   PROBLEMA: "Sin overlap se pierden conceptos en fronteras"
   SOLUCIÓN: "Overlap de 200 tokens"
   
5. Background Tasks:
   PROBLEMA: "Si servidor reinicia, proceso se pierde"
   SOLUCIÓN: "Guardar progreso en DB, implementar recuperación"
   
6. Similarity Threshold:
   PROBLEMA: "Threshold muy bajo retorna conceptos irrelevantes"
   SOLUCIÓN: "Usar 0.7-0.8, ajustar según feedback"

7. ⚠️ DUPLICACIÓN DE CÓDIGO:
   PROBLEMA: "Recrear métodos que ya existen"
   SOLUCIÓN: "VERIFICAR antes de crear: generate_with_messages(), format_messages_from_memory() YA EXISTEN"
   
8. ⚠️ AGENTE INEXISTENTE:
   PROBLEMA: "Intentar modificar GeneralChatAgent que no existe"
   SOLUCIÓN: "Solo modificar ContentGeneratorAgent. GeneralChatAgent NO existe ni se creará"
   
9. ⚠️ PATRÓN NO SEGUIDO:
   PROBLEMA: "Crear nueva lógica para conceptos sin seguir patrón existente"
   SOLUCIÓN: "SEGUIR PATRÓN de MemoryManager.get_training_summary() para inyectar conceptos"
```

---

## 📊 SCORE DE CONFIANZA: 9/10

```yaml
Justificación:
  ✅ Archon consultado exhaustivamente (3 fuentes relevantes)
  ✅ Serena usado para análisis completo de servicios
  ✅ Skills identificadas por fase
  ✅ Estructura de tareas completa con comandos
  ✅ Validación en 3+ niveles
  ✅ Gotchas documentados
  ✅ Pseudocódigo con patrones del proyecto
  
  ⚠️ -1 punto: Frontend puede requerir ajustes de diseño no previstos
```

---

## 🎯 RESUMEN EJECUTIVO

| Tarea | Archivos a Crear | Archivos a Modificar | Prioridad |
|-------|------------------|----------------------|-----------|
| T0: Análisis | docs/INTEGRATION_ANALYSIS.md | - | ⚡ CRÍTICA |
| T1: DB | db/003_*.sql | db/models.py | Alta |
| T2: Service | services/book_learning_service.py, schemas/knowledge.py | - | Alta |
| T3: API | api/knowledge.py | main.py | Alta |
| T4: RAG | - | services/rag_service.py | Media |
| T5: Agents | - | memory_manager.py, content_generator_agent.py | Media |
| T6: Frontend | 4 componentes, 1 página | Sidebar.tsx, api-chat.ts | Media |
| T7: Tests | tests/*.py, docs/*.md | README.md | Baja |

**⚠️ ADVERTENCIAS CRÍTICAS:**
- `LLMService.generate_with_messages()` YA EXISTE - NO recrear
- `MemoryManager.get_training_summary()` es PATRÓN A SEGUIR
- `GeneralChatAgent` NO existe y NO se creará - solo modificar ContentGeneratorAgent

**Principio guía:** REUTILIZAR > EXTENDER > CREAR

---

**🚀 Este PRP está listo para implementación one-pass. El desarrollador tiene todo el contexto necesario para ejecutar sin preguntas adicionales.**
