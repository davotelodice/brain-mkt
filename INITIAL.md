# INITIAL - Sistema de Aprendizaje Progresivo para Marketing Brain

## 📋 INFORMACIÓN DEL PROYECTO

```yaml
nombre: "Marketing Brain - Sistema de Aprendizaje Progresivo desde Libros"
version: "3.0.0 - Knowledge Enhancement Module"
fecha_inicio: "2026-01-30"
tipo_proyecto: "Feature Addition - Knowledge Ingestion System"
proyecto_base: "Marketing Second Brain (EXISTENTE y FUNCIONANDO)"
referencia_base: "@PRPs/marketing-brain-system-v3.md, @INITIAL2.md"
```

---

## 🎯 OBJETIVO PRINCIPAL DE ESTE MÓDULO

**⚠️ CRÍTICO - LEER PRIMERO:**

Este módulo **NO ES UN PROYECTO NUEVO**. Es una **EXTENSIÓN** del sistema Marketing Brain que **YA EXISTE Y FUNCIONA**.

**Lo que YA tenemos funcionando:**
- ✅ Backend FastAPI completo con agentes IA
- ✅ Frontend Next.js 14 con interfaz de chat
- ✅ Base de datos Supabase con pgvector
- ✅ Sistema de memoria triple (short-term, long-term, semantic)
- ✅ RAGService para búsqueda semántica
- ✅ LLMService para interacción con OpenAI/OpenRouter
- ✅ Agentes: RouterAgent, BuyerPersonaAgent, ContentGeneratorAgent, GeneralChatAgent
- ✅ Sistema de documentos: usuarios pueden subir .txt, .pdf, .docx

**Lo que queremos AGREGAR:**
- 🎯 Sistema de "aprendizaje progresivo" para que el agente **comprenda** libros completos
- 🎯 Pipeline que toma un libro → lo divide en chunks → el LLM "aprende" → guarda conceptos clave
- 🎯 Memoria estructurada que almacena conocimiento **destilado** (no texto completo)
- 🎯 Integración perfecta con RAGService existente

---

## 🧠 CONCEPTO: APRENDIZAJE PROGRESIVO (No Almacenamiento Crudo)

### La Diferencia Clave

**❌ Sistema RAG tradicional (lo que NO queremos):**
```
Libro (500 páginas) → Chunks de 1000 tokens → Embeddings → Vector DB
Usuario pregunta → Búsqueda semántica → Retorna chunks crudos → LLM responde
```
**Problema:** El agente no "aprendió" el libro, solo lo tiene almacenado. Cada consulta depende de encontrar el chunk exacto.

**✅ Sistema de Aprendizaje Progresivo (lo que SÍ queremos - HÍBRIDO):**
```
Libro (500 páginas) → 
  Chunks de 1500 tokens con overlap 200 →
  Por cada chunk: LLM extrae conceptos clave (200-300 palabras) →
  Por cada grupo de chunks relacionados: LLM genera resumen temático →
  Resumen global del libro con índice de conceptos →
  
Almacenamiento en 3 capas:
  1. Conceptos extraídos (embeddings) ← búsqueda semántica rápida
  2. Resúmenes temáticos (texto estructurado) ← contexto medio
  3. Índice global de conceptos (JSON) ← navegación rápida

Usuario pregunta → 
  Búsqueda en conceptos extraídos (capa 1) →
  Si necesita más contexto: resúmenes temáticos (capa 2) →
  LLM responde con conocimiento "comprendido"
```

**Beneficio:** El agente "estudió" el libro como lo haría un humano. No memoriza todo, pero entiende los conceptos y puede consultarlos rápidamente.

---

## 🏗️ INTEGRACIÓN CON STACK EXISTENTE

### ⚠️ REGLA DE ORO: APROVECHAR, NO DUPLICAR

**Antes de escribir UNA SOLA LÍNEA de código, el desarrollador DEBE:**

1. **Leer y entender el proyecto existente:**
   ```bash
   # OBLIGATORIO - Usar MCP Serena para análisis
   get_symbols_overview('backend/src/')
   get_symbols_overview('frontend/app/')
   
   # Entender servicios existentes
   find_symbol('RAGService', 'backend/src/services/rag_service.py', True)
   find_symbol('LLMService', 'backend/src/services/llm_service.py', True)
   find_symbol('EmbeddingService', 'backend/src/services/embedding_service.py', True)
   find_symbol('DocumentProcessor', 'backend/src/services/document_processor.py', True)
   
   # Entender estructura de base de datos
   view('backend/src/db/models.py')
   view('backend/db/001_initial_schema.sql')
   view('backend/db/002_add_user_document_summary.sql')
   ```

2. **Identificar qué código REUTILIZAR:**
   - ✅ `RAGService.search_relevant_docs()` → Ya hace búsqueda semántica
   - ✅ `EmbeddingService.generate_embeddings()` → Ya genera embeddings
   - ✅ `LLMService.generate()` → Ya interactúa con LLM
   - ✅ `DocumentProcessor` → Ya tiene parsers para .txt, .pdf, .docx
   - ✅ `RecursiveCharacterTextSplitter` → Ya hace chunking

3. **Identificar qué código EXTENDER (no reemplazar):**
   - 🔧 `marketing_knowledge_base` tabla → Agregar columna `knowledge_type` para diferenciar
   - 🔧 `RAGService` → Agregar método `search_learned_concepts()` especializado
   - 🔧 Crear `BookLearningService` que **usa** servicios existentes

4. **Identificar qué código CREAR (nuevo):**
   - ✨ `backend/src/services/book_learning_service.py` (orquestador del pipeline)
   - ✨ `backend/src/api/knowledge.py` (endpoints para subir/gestionar libros)
   - ✨ Nueva tabla: `marketing_learned_books` (metadata de libros procesados)

---

## 📊 ARQUITECTURA DEL SISTEMA HÍBRIDO (DETALLADA)

### Stack Tecnológico Existente (NO CAMBIAR)

```yaml
Backend: FastAPI (Python 3.11) ✅
ORM: SQLAlchemy 2.0 async ✅
Validación: Pydantic v2 ✅
Base de Datos: Supabase Postgres + pgvector ✅
LLM: OpenAI / OpenRouter (vía LLMService) ✅
Embeddings: OpenAI text-embedding-3-small (vía EmbeddingService) ✅
Frontend: Next.js 14, App Router, TypeScript, Tailwind ✅
```

### Componentes a Integrar (NUEVOS)

#### 1. BookLearningService (Orquestador Principal)

**Ubicación:** `backend/src/services/book_learning_service.py`

**Responsabilidades:**
- Coordinar todo el pipeline de aprendizaje
- **USAR** servicios existentes (DocumentProcessor, LLMService, EmbeddingService, RAGService)
- **NO duplicar** lógica de chunking ni embeddings

**Flujo de procesamiento:**
```python
class BookLearningService:
    def __init__(self, llm_service: LLMService, embedding_service: EmbeddingService):
        self.llm = llm_service
        self.embeddings = embedding_service
        self.chunker = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )
    
    async def process_book(self, file_path: str, project_id: str) -> LearnedBook:
        """
        Pipeline completo de aprendizaje progresivo
        
        IMPORTANTE: Este método orquesta, NO reimplementa.
        Usa servicios existentes para cada paso.
        """
        # 1. Extraer texto (USAR DocumentProcessor existente)
        raw_text = await self._extract_text_from_file(file_path)
        
        # 2. Chunking con overlap (USAR RecursiveCharacterTextSplitter)
        chunks = self.chunker.split_text(raw_text)
        
        # 3. CAPA 1 - Extracción de conceptos por chunk
        chunk_concepts = []
        for i, chunk in enumerate(chunks):
            concepts = await self._extract_concepts_from_chunk(chunk, i)
            chunk_concepts.append(concepts)
        
        # 4. CAPA 2 - Agrupar chunks relacionados y generar resúmenes temáticos
        thematic_summaries = await self._generate_thematic_summaries(
            chunks, chunk_concepts
        )
        
        # 5. CAPA 3 - Resumen global + índice de conceptos
        global_summary = await self._generate_global_summary(
            chunk_concepts, thematic_summaries
        )
        
        # 6. Generar embeddings (USAR EmbeddingService existente)
        concept_embeddings = await self._embed_concepts(chunk_concepts)
        
        # 7. Almacenar en base de datos (NUEVAS tablas + marketing_knowledge_base)
        learned_book = await self._save_learned_book(
            project_id=project_id,
            chunk_concepts=chunk_concepts,
            thematic_summaries=thematic_summaries,
            global_summary=global_summary,
            embeddings=concept_embeddings
        )
        
        return learned_book
    
    async def _extract_concepts_from_chunk(
        self, chunk: str, chunk_index: int
    ) -> ConceptExtraction:
        """
        Usa LLM para extraer conceptos clave de un chunk
        
        IMPORTANTE: Esto NO es un resumen. Es una "destilación" semántica.
        El LLM identifica: conceptos clave, relaciones, ejemplos importantes.
        """
        prompt = f"""
Eres un experto en marketing que está estudiando un libro.
Tu tarea es extraer los conceptos MÁS IMPORTANTES de este fragmento.

NO hagas un resumen. Extrae CONCEPTOS CLAVE que un estudiante debería recordar.

Fragmento del libro (chunk {chunk_index}):
{chunk}

Extrae:
1. Conceptos principales (máximo 5)
2. Relaciones entre conceptos
3. Ejemplos o casos clave mencionados
4. Términos técnicos importantes

Formato de respuesta (JSON):
{{
    "main_concepts": ["concepto1", "concepto2", ...],
    "relationships": ["concepto1 causa concepto2", ...],
    "key_examples": ["ejemplo1", ...],
    "technical_terms": {{"término": "definición", ...}}
}}

Sé CONCISO. Máximo 200-300 palabras en total.
"""
        
        # USAR LLMService existente
        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.3  # Baja temperatura para extracción precisa
        )
        
        return ConceptExtraction.parse_from_llm_response(response)
```

#### 2. Nuevas Tablas en Base de Datos

**⚠️ CRÍTICO:** Estas tablas se **INTEGRAN** con el esquema existente, no lo reemplazan.

**Tabla 1: `marketing_learned_books` (metadata de libros procesados)**

```sql
CREATE TABLE marketing_learned_books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    
    -- Metadata del libro
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    file_path VARCHAR(1000), -- Ruta al archivo original
    file_type VARCHAR(10), -- 'pdf', 'txt', 'docx'
    
    -- Estado del procesamiento
    processing_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    total_chunks INTEGER,
    processed_chunks INTEGER DEFAULT 0,
    
    -- Resumen global del libro
    global_summary JSONB, -- Estructura: {summary: str, key_topics: [], concept_index: {}}
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    -- Índices
    INDEX idx_learned_books_project (project_id),
    INDEX idx_learned_books_status (processing_status)
);
```

**Tabla 2: Extender `marketing_knowledge_base` (AGREGAR columna, no crear tabla nueva)**

```sql
-- MIGRACIÓN: Agregar columna para diferenciar tipos de conocimiento
ALTER TABLE marketing_knowledge_base 
ADD COLUMN knowledge_type VARCHAR(50) DEFAULT 'raw_chunk';

-- Valores posibles de knowledge_type:
-- 'raw_chunk' = chunk tradicional de RAG (existente)
-- 'extracted_concept' = concepto extraído por LLM (NUEVO)
-- 'thematic_summary' = resumen temático (NUEVO)
-- 'user_document' = documento subido por usuario (existente)

-- Agregar columna para enlazar con libro aprendido
ALTER TABLE marketing_knowledge_base 
ADD COLUMN learned_book_id UUID REFERENCES marketing_learned_books(id) ON DELETE CASCADE;

-- Índice para búsquedas por tipo
CREATE INDEX idx_knowledge_type ON marketing_knowledge_base(knowledge_type);
CREATE INDEX idx_learned_book ON marketing_knowledge_base(learned_book_id);
```

**Tabla 3: `marketing_book_concepts` (conceptos extraídos estructurados)**

```sql
CREATE TABLE marketing_book_concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learned_book_id UUID REFERENCES marketing_learned_books(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    
    -- Conceptos extraídos (estructura JSON del LLM)
    main_concepts TEXT[], -- Array de conceptos principales
    relationships TEXT[], -- Array de relaciones entre conceptos
    key_examples TEXT[], -- Array de ejemplos importantes
    technical_terms JSONB, -- {término: definición}
    
    -- Texto resumido del chunk (200-300 palabras)
    condensed_text TEXT,
    
    -- Embedding del concepto condensado
    embedding VECTOR(1536),
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Índices
    INDEX idx_book_concepts_book (learned_book_id),
    INDEX idx_book_concepts_embedding USING ivfflat (embedding vector_cosine_ops)
);
```

#### 3. Endpoints de API (NUEVOS)

**Archivo:** `backend/src/api/knowledge.py`

```python
from fastapi import APIRouter, UploadFile, Depends
from typing import List
from ..services.book_learning_service import BookLearningService
from ..schemas.knowledge import (
    LearnedBookResponse, 
    BookProcessingStatus,
    ConceptSearchRequest,
    ConceptSearchResponse
)

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.post("/books/upload")
async def upload_book_for_learning(
    file: UploadFile,
    project_id: str,
    book_learning_service: BookLearningService = Depends()
):
    """
    Sube un libro para que el agente lo "aprenda"
    
    Proceso:
    1. Valida archivo (.pdf, .txt, .docx)
    2. Guarda temporalmente
    3. Inicia procesamiento asíncrono (background task)
    4. Retorna ID de tarea para seguimiento
    """
    # IMPORTANTE: Reutilizar validaciones existentes de DocumentProcessor
    # NO duplicar código de validación de archivos
    
@router.get("/books/{book_id}/status")
async def get_book_processing_status(
    book_id: str
) -> BookProcessingStatus:
    """
    Consulta el estado del procesamiento de un libro
    
    Retorna:
    - processing_status: 'pending' | 'processing' | 'completed' | 'failed'
    - processed_chunks: X de Y
    - estimated_completion: timestamp (si está procesando)
    """
    
@router.get("/books")
async def list_learned_books(
    project_id: str
) -> List[LearnedBookResponse]:
    """
    Lista todos los libros que el agente ha "aprendido"
    
    Retorna metadata: título, autor, estado, fecha, conceptos clave
    """
    
@router.post("/concepts/search")
async def search_learned_concepts(
    request: ConceptSearchRequest,
    project_id: str
) -> ConceptSearchResponse:
    """
    Búsqueda semántica en conceptos aprendidos
    
    IMPORTANTE: Usa RAGService existente, pero filtra por knowledge_type
    
    Retorna:
    - Conceptos relevantes (no chunks crudos)
    - Resúmenes temáticos relacionados
    - Referencias a libros de origen
    """
    # USAR RAGService.search_relevant_docs() con filtro adicional
    
@router.delete("/books/{book_id}")
async def delete_learned_book(
    book_id: str,
    project_id: str
):
    """
    Elimina un libro aprendido y todos sus conceptos
    
    IMPORTANTE: Eliminar también de marketing_knowledge_base
    """
```

#### 4. Integración con Agentes Existentes

**⚠️ CRÍTICO:** Los agentes existentes **NO se reescriben**, se **EXTIENDEN**.

**Modificación en `ContentGeneratorAgent`:**

```python
# backend/src/agents/content_generator_agent.py

class ContentGeneratorAgent(BaseAgent):
    async def execute(self, user_message: str, chat_id: str) -> str:
        # ... código existente ...
        
        # NUEVO: Además de buscar en documentos y knowledge base tradicional,
        # buscar en conceptos aprendidos
        
        learned_concepts = await self._search_learned_concepts(
            query=user_message,
            project_id=self.project_id,
            limit=5
        )
        
        # Construir prompt con contexto enriquecido
        context = {
            "buyer_persona": buyer_persona,  # Existente
            "customer_journey": customer_journey,  # Existente
            "relevant_docs": relevant_docs,  # Existente
            "learned_concepts": learned_concepts  # NUEVO
        }
        
        # ... resto del código ...
    
    async def _search_learned_concepts(
        self, query: str, project_id: str, limit: int
    ) -> List[ConceptExtraction]:
        """
        NUEVO método que busca en conceptos aprendidos
        
        IMPORTANTE: Usa RAGService existente con filtro knowledge_type
        """
        # NO duplicar código de búsqueda semántica
        # USAR RAGService.search_relevant_docs() con filtro
```

---

## 🔌 MCPs A UTILIZAR

### 1. MCP Serena (⚡ OBLIGATORIO - USAR PRIMERO)

```yaml
Propósito: Análisis simbólico del proyecto existente

ANTES DE CODIFICAR CUALQUIER COSA:
  1. get_symbols_overview('backend/src/services/')
     → Ver qué servicios ya existen
  
  2. find_symbol('RAGService', 'backend/src/services/rag_service.py', True)
     → Leer implementación completa de búsqueda semántica
  
  3. find_symbol('DocumentProcessor', 'backend/src/services/document_processor.py', True)
     → Ver cómo se procesan documentos actualmente
  
  4. search_for_pattern('async def.*embedding', 'backend/src/')
     → Encontrar todas las funciones de embeddings
  
  5. find_referencing_symbols('LLMService', 'services/llm_service.py')
     → Ver dónde se usa LLMService para no duplicar

REGLA: Si Serena encuentra código similar, REUTILIZARLO, NO reescribirlo
```

### 2. MCP Archon (⚡ PRIORITARIO - Documentación)

```yaml
Propósito: Consultar documentación oficial

Usar para:
  - "langchain recursive text splitter overlap"
  - "pydantic v2 nested model validation"
  - "fastapi background tasks async"
  - "supabase pgvector similarity threshold"
  - "openai embeddings batch processing"

Ejemplo:
  rag_search_knowledge_base(
    query="langchain text splitter chunk overlap best practices",
    source_id="src_langchain",
    match_count=5
  )
```

### 3. MCP Custom (Futuro - Fase 2)

```yaml
Propósito: Exponer funcionalidad del sistema

Tools a implementar (después de MVP):
  - analyze_learned_books(project_id)
  - search_concepts(query, book_id)
  - get_book_summary(book_id)
```

---

## 📚 SKILLS A UTILIZAR

### Fase de Análisis del Proyecto Existente

```yaml
Skills:

1. @.cursor/skills/code-comprehension/SKILL.md
   Cuándo: Al inicio, para entender proyecto existente
   Por qué: Evitar duplicación de código
   Activación: "analizar proyecto", "entender arquitectura"

2. @.cursor/skills/architecture/SKILL.md
   Cuándo: Decidir cómo integrar el nuevo módulo
   Por qué: Evaluar trade-offs de diferentes enfoques
   Activación: "decidir integración", "evaluar arquitectura"
```

### Fase de Desarrollo

```yaml
Skills:

3. @.cursor/skills/python-patterns/SKILL.md
   Cuándo: Escribiendo código Python
   Por qué: Mejores prácticas, async patterns
   Activación automática: Proyecto Python detectado

4. @.cursor/skills/clean-code/SKILL.md
   Cuándo: Durante todo el desarrollo
   Por qué: Código conciso, directo, sin duplicación
   Activación automática: Al escribir código

5. @.cursor/skills/rag-implementation/SKILL.md
   Cuándo: Extendiendo RAGService
   Por qué: Chunking optimization, retrieval strategies
   Invocación: @.cursor/skills/rag-implementation/SKILL.md extender RAG

6. @.cursor/skills/agent-memory-systems/SKILL.md
   Cuándo: Integrando con sistema de memoria existente
   Por qué: Entender cómo agregar nueva capa de memoria
   Invocación: @.cursor/skills/agent-memory-systems/SKILL.md integrar memoria
```

### Fase de Testing

```yaml
Skills:

7. @.cursor/skills/testing-patterns/SKILL.md
   Cuándo: Escribiendo tests de integración
   Por qué: Validar que nuevo código funciona con código existente
   Activación automática: Al escribir tests
```

---

## 🚧 FASES DEL PROYECTO

### FASE 0: Análisis del Proyecto Existente (⚡ OBLIGATORIA)

```yaml
Objetivo: Entender completamente el código existente antes de tocar nada

Tareas:

1. Análisis de Servicios Existentes (con Serena):
   - Leer RAGService completo
   - Leer LLMService completo
   - Leer EmbeddingService completo
   - Leer DocumentProcessor completo
   - Identificar funciones reutilizables

2. Análisis de Base de Datos:
   - Leer schema actual (001_initial_schema.sql, 002_*.sql)
   - Entender tabla marketing_knowledge_base
   - Identificar campos que necesitamos agregar

3. Análisis de Agentes:
   - Leer RouterAgent, ContentGeneratorAgent, GeneralChatAgent
   - Identificar puntos de integración
   - Entender flujo de memoria actual

4. Documentar Hallazgos:
   - Crear docs/INTEGRATION_ANALYSIS.md
   - Listar servicios a reutilizar
   - Listar código a extender
   - Listar código nuevo a crear

Criterios de aceptación:
  - [ ] Serena ejecutado en todos los módulos clave
  - [ ] Documento INTEGRATION_ANALYSIS.md creado
  - [ ] Lista clara de "reutilizar vs extender vs crear"
  - [ ] Diagrama de integración dibujado
```

### FASE 1: Migración de Base de Datos

```yaml
Objetivo: Agregar tablas y columnas necesarias SIN romper existentes

Tareas:

1. Crear migración 003_book_learning_system.sql:
   - CREATE TABLE marketing_learned_books
   - ALTER TABLE marketing_knowledge_base ADD COLUMN knowledge_type
   - ALTER TABLE marketing_knowledge_base ADD COLUMN learned_book_id
   - CREATE TABLE marketing_book_concepts
   - Crear índices necesarios

2. Actualizar models.py:
   - Agregar modelo MarketingLearnedBook
   - Agregar modelo MarketingBookConcept
   - Extender modelo MarketingKnowledgeBase (agregar campos nuevos)

3. Validar migración:
   - Ejecutar en DB de desarrollo
   - Verificar que datos existentes no se afectan
   - Verificar que índices se crean correctamente

Archivos a crear:
  - backend/db/003_book_learning_system.sql
  
Archivos a modificar:
  - backend/src/db/models.py (AGREGAR modelos, no modificar existentes)

Skills a usar:
  - @.cursor/skills/database-design/SKILL.md

MCPs a consultar:
  - Archon: "sqlalchemy 2.0 alembic migrations"
  - Serena: Analizar models.py existente antes de modificar

Criterios de aceptación:
  - [ ] Migración ejecutada sin errores
  - [ ] Datos existentes intactos
  - [ ] Nuevos modelos en models.py
  - [ ] Tests de migración pasando
```

### FASE 2: BookLearningService (Pipeline de Aprendizaje)

```yaml
Objetivo: Crear servicio que orquesta aprendizaje progresivo

Tareas:

1. Crear BookLearningService:
   - __init__ con dependencias (LLMService, EmbeddingService, etc.)
   - process_book() método principal
   - _extract_text_from_file() REUTILIZA DocumentProcessor
   - _extract_concepts_from_chunk() usa LLMService
   - _generate_thematic_summaries() usa LLMService
   - _generate_global_summary() usa LLMService
   - _embed_concepts() REUTILIZA EmbeddingService
   - _save_learned_book() guarda en DB

2. Crear schemas Pydantic:
   - ConceptExtraction
   - ThematicSummary
   - LearnedBook
   - BookProcessingStatus

3. Implementar procesamiento por lotes:
   - Procesar chunks en batches de 10 (evitar rate limits)
   - Progress tracking en DB (processed_chunks)
   - Retry logic con exponential backoff

Archivos a crear:
  - backend/src/services/book_learning_service.py
  - backend/src/schemas/knowledge.py

Archivos a REUTILIZAR (no modificar):
  - backend/src/services/llm_service.py
  - backend/src/services/embedding_service.py
  - backend/src/services/document_processor.py

Skills a usar:
  - @.cursor/skills/python-patterns/SKILL.md (automático)
  - @.cursor/skills/clean-code/SKILL.md (automático)

MCPs a consultar:
  - Archon: "langchain recursive character text splitter"
  - Serena: Ver cómo DocumentProcessor parsea archivos

Validación:
  - [ ] BookLearningService instanciable
  - [ ] process_book() ejecuta sin errores (archivo de prueba)
  - [ ] Conceptos extraídos tienen formato correcto
  - [ ] Embeddings generados correctamente
  - [ ] Datos guardados en las 3 tablas nuevas
```

### FASE 3: API Endpoints

```yaml
Objetivo: Exponer funcionalidad vía API REST

Tareas:

1. Crear backend/src/api/knowledge.py:
   - POST /api/knowledge/books/upload
   - GET /api/knowledge/books/{book_id}/status
   - GET /api/knowledge/books (list)
   - POST /api/knowledge/concepts/search
   - DELETE /api/knowledge/books/{book_id}

2. Implementar background tasks:
   - upload endpoint inicia procesamiento en background
   - FastAPI BackgroundTasks para no bloquear request

3. Validaciones:
   - Tipo de archivo (.pdf, .txt, .docx)
   - Tamaño máximo (50MB para libros)
   - project_id del usuario autenticado

4. Registrar router en main.py:
   - app.include_router(knowledge.router)

Archivos a crear:
  - backend/src/api/knowledge.py

Archivos a modificar:
  - backend/src/main.py (include_router)

MCPs a consultar:
  - Archon: "fastapi background tasks async"
  - Serena: Ver cómo están estructurados otros routers (chat.py, documents.py)

Validación:
  - [ ] Endpoints registrados en /docs
  - [ ] upload endpoint acepta archivos
  - [ ] Background task inicia correctamente
  - [ ] Status endpoint retorna progreso
  - [ ] Search endpoint retorna conceptos
```

### FASE 4: Integración con RAGService

```yaml
Objetivo: Extender RAGService para buscar en conceptos aprendidos

Tareas:

1. Extender RAGService:
   - Agregar método search_learned_concepts()
   - Modificar search_relevant_docs() para aceptar knowledge_type filter
   - Mantener compatibilidad con código existente

2. Crear método híbrido:
   - search_with_learned_knowledge(query, project_id)
   - Busca en: conceptos aprendidos + documentos + knowledge base tradicional
   - Combina y rankea resultados

3. Optimizar búsqueda:
   - Usar índice ivfflat eficientemente
   - Threshold de similaridad ajustable
   - Limitar resultados por tipo (5 conceptos + 5 docs + 5 chunks)

Archivos a modificar:
  - backend/src/services/rag_service.py (EXTENDER, no reescribir)

Skills a usar:
  - @.cursor/skills/rag-implementation/SKILL.md

MCPs a consultar:
  - Archon: "supabase pgvector cosine similarity"
  - Serena: Leer RAGService completo antes de modificar

Validación:
  - [ ] search_learned_concepts() funciona
  - [ ] Resultados ordenados por relevancia
  - [ ] Código existente NO roto (tests pasan)
  - [ ] Performance <100ms para búsqueda
```

### FASE 5: Integración con Agentes

```yaml
Objetivo: Que agentes usen conceptos aprendidos en sus respuestas

Tareas:

1. Modificar ContentGeneratorAgent:
   - Agregar método _search_learned_concepts()
   - Incluir conceptos en contexto de prompt
   - Mantener funcionalidad existente intacta

2. Modificar GeneralChatAgent:
   - Usar conceptos aprendidos para respuestas más informadas
   - Similar a ContentGeneratorAgent

3. Probar integración end-to-end:
   - Subir libro de prueba
   - Esperar procesamiento
   - Hacer pregunta al agente
   - Verificar que usa conceptos del libro

Archivos a modificar:
  - backend/src/agents/content_generator_agent.py
  - backend/src/agents/general_chat_agent.py

⚠️ CRÍTICO: NO reescribir agentes, solo AGREGAR método nuevo

Skills a usar:
  - @.cursor/skills/agent-memory-systems/SKILL.md

Validación:
  - [ ] Agentes usan conceptos aprendidos
  - [ ] Respuestas más ricas y contextuales
  - [ ] Funcionalidad existente NO afectada
  - [ ] Tests de agentes pasan
```

### FASE 6: Frontend - UI para Gestión de Libros

```yaml
Objetivo: Permitir al usuario subir/gestionar libros desde UI

Tareas:

1. Crear componente BookUpload:
   - Drag & drop para archivos
   - Validación de tipo (.pdf, .txt, .docx)
   - Progress bar durante procesamiento
   - Feedback de éxito/error

2. Crear página /dashboard/knowledge:
   - Lista de libros aprendidos
   - Tarjetas con: título, autor, estado, conceptos clave
   - Botón para eliminar libro
   - Filtros por estado

3. Crear componente ConceptsViewer:
   - Visualización de conceptos extraídos
   - Búsqueda en conceptos
   - Árbol de conceptos relacionados

4. Integrar en layout existente:
   - Agregar link en sidebar: "Biblioteca de Conocimiento"
   - Mantener consistencia con diseño existente

Componentes a crear:
  - frontend/app/components/BookUpload.tsx
  - frontend/app/dashboard/knowledge/page.tsx
  - frontend/app/components/ConceptsViewer.tsx
  - frontend/app/components/LearnedBookCard.tsx

Archivos a modificar:
  - frontend/app/components/Sidebar.tsx (agregar link)

Skills a usar:
  - @.cursor/skills/nextjs-best-practices/SKILL.md (automático)
  - @.cursor/skills/react-patterns/SKILL.md (automático)
  - @.cursor/skills/frontend-design/SKILL.md

MCPs a consultar:
  - Serena: Ver estructura de componentes existentes (ChatInterface, Sidebar)

Validación:
  - [ ] Usuario puede subir libro
  - [ ] Progress bar funciona
  - [ ] Lista de libros se actualiza
  - [ ] UI consistente con resto del sistema
  - [ ] Responsive en mobile
```

### FASE 7: Testing y Documentación

```yaml
Objetivo: Validar integración completa y documentar

Tareas:

1. Tests de integración:
   - Test: Subir libro → procesar → buscar concepto → obtener respuesta
   - Test: Eliminar libro → verificar cleanup completo
   - Test: Agente sin libros vs con libros (comparar respuestas)

2. Tests unitarios:
   - BookLearningService._extract_concepts_from_chunk()
   - RAGService.search_learned_concepts()
   - Endpoints de API

3. Documentación:
   - docs/BOOK_LEARNING_SYSTEM.md (arquitectura)
   - Actualizar README.md (nueva funcionalidad)
   - Diagramas de flujo

4. Validar performance:
   - Benchmark: procesamiento de libro de 300 páginas
   - Benchmark: búsqueda en 10 libros aprendidos
   - Optimizar si necesario

Archivos a crear:
  - backend/tests/integration/test_book_learning.py
  - backend/tests/unit/test_book_learning_service.py
  - docs/BOOK_LEARNING_SYSTEM.md

Archivos a modificar:
  - README.md

Skills a usar:
  - @.cursor/skills/testing-patterns/SKILL.md
  - @.cursor/skills/systematic-debugging/SKILL.md

Criterios de aceptación:
  - [ ] Coverage >80% en código nuevo
  - [ ] Tests de integración pasan
  - [ ] Documentación completa
  - [ ] Performance aceptable (<5 min para libro de 300 págs)
```

---

## ⚠️ CONSIDERACIONES TÉCNICAS CRÍTICAS

### 🚫 PROHIBICIONES ABSOLUTAS

```yaml
1. DUPLICAR CÓDIGO EXISTENTE:
   ❌ NUNCA: Copiar funciones de RAGService, LLMService, etc.
   ✅ SIEMPRE: Importar y usar servicios existentes
   
   ❌ NUNCA: Crear nueva función de embeddings
   ✅ SIEMPRE: Usar EmbeddingService.generate_embeddings()

2. MODIFICAR TABLAS EXISTENTES SIN MIGRACIÓN:
   ❌ NUNCA: Cambiar columnas de marketing_knowledge_base directamente
   ✅ SIEMPRE: Crear migración SQL numerada (003_*.sql)

3. ROMPER COMPATIBILIDAD:
   ❌ NUNCA: Cambiar firma de métodos existentes
   ✅ SIEMPRE: Agregar métodos nuevos o parámetros opcionales

4. IGNORAR ANÁLISIS PREVIO:
   ❌ NUNCA: Codificar sin haber usado Serena primero
   ✅ SIEMPRE: get_symbols_overview() antes de modificar archivos
```

### 🔐 Seguridad

```yaml
1. Validación de Archivos:
   - Validar MIME type (no solo extensión)
   - Límite de tamaño: 50MB para libros
   - Escanear con antivirus si es posible
   - Sanitizar nombres de archivo

2. Aislamiento por Proyecto:
   - TODOS los queries incluyen WHERE project_id = ?
   - Libros aprendidos son privados por proyecto
   - No mezclar conceptos entre proyectos

3. Rate Limiting:
   - Límite de 5 libros por día por usuario
   - Límite de 100 búsquedas de conceptos por hora
```

### ⚡ Performance

```yaml
1. Procesamiento de Libros:
   - Procesamiento asíncrono (background task)
   - Chunks procesados en batches de 10
   - Progress tracking para UX
   - Timeout de 30 min por libro

2. Búsqueda de Conceptos:
   - Índice ivfflat optimizado
   - Cache en Redis (TTL 1 hora)
   - Límite de 10 conceptos por búsqueda
   - <100ms target latency

3. Embeddings:
   - Batch processing (evitar rate limits)
   - Retry con exponential backoff
   - Cache de embeddings idénticos
```

### 🐛 Gotchas Específicos del Sistema de Aprendizaje

```yaml
1. LLM Context Window:
   GOTCHA: "Chunks muy largos pueden exceder context window"
   SOLUCIÓN: Limitar chunks a 1500 tokens, verificar antes de enviar

2. Extracción de Conceptos:
   GOTCHA: "LLM puede ser inconsistente en formato JSON"
   SOLUCIÓN: Usar Pydantic para parsear y validar, retry si falla

3. Overlap en Chunking:
   GOTCHA: "Sin overlap se pierden conceptos en fronteras"
   SOLUCIÓN: Overlap de 200 tokens, experimentar con 150-300

4. Embedding Similarity Threshold:
   GOTCHA: "Threshold muy bajo retorna conceptos irrelevantes"
   SOLUCIÓN: Experimentar con 0.7-0.8, ajustar según feedback

5. Procesamiento Largo:
   GOTCHA: "Usuario puede cerrar navegador y perder progreso"
   SOLUCIÓN: Background task + polling de status, guardar progreso en DB
```

---

## 🎯 CRITERIOS DE ÉXITO DEL MÓDULO

```yaml
Funcionalidad:
  - [ ] Usuario puede subir libro (.pdf, .txt, .docx)
  - [ ] Sistema procesa libro en background
  - [ ] Usuario ve progreso de procesamiento
  - [ ] Conceptos extraídos correctamente
  - [ ] Agentes usan conceptos en respuestas
  - [ ] Búsqueda de conceptos funcional
  - [ ] Usuario puede eliminar libro
  - [ ] Cleanup completo al eliminar

Integración:
  - [ ] NO duplica código existente
  - [ ] USA servicios existentes (RAG, LLM, Embeddings)
  - [ ] EXTIENDE agentes sin romperlos
  - [ ] Compatibilidad con código existente al 100%
  - [ ] Tests existentes siguen pasando

Calidad:
  - [ ] Coverage >80% en código nuevo
  - [ ] Sin errores de linting (ruff, mypy)
  - [ ] Sin errores de tipos (TypeScript)
  - [ ] Documentación completa

Performance:
  - [ ] Libro de 300 páginas procesado <5 min
  - [ ] Búsqueda de conceptos <100ms
  - [ ] UI responsive durante procesamiento
```

---

## 🚀 EJEMPLO DE USO DEL SISTEMA

```yaml
Escenario: Usuario quiere entrenar agente con "Influence" de Robert Cialdini

Paso 1 - Subir libro:
  Usuario → Dashboard → Biblioteca de Conocimiento → Subir Libro
  Selecciona: "Influence.pdf" (450 páginas)
  Sistema: Inicia procesamiento en background

Paso 2 - Procesamiento (automático):
  Sistema divide en ~300 chunks (1500 tokens cada uno)
  Por cada chunk:
    - LLM extrae conceptos (5 conceptos principales)
    - LLM identifica relaciones entre conceptos
    - LLM extrae ejemplos clave
    - Sistema genera embedding del concepto
  
  Sistema agrupa chunks relacionados:
    - Capítulo 1: Principio de Reciprocidad → Resumen temático
    - Capítulo 2: Principio de Compromiso → Resumen temático
    - ...
  
  Sistema genera resumen global:
    - 6 principios de influencia
    - Índice de conceptos clave
    - Mapa de relaciones

Paso 3 - Uso por el agente:
  Usuario pregunta: "Dame 5 ideas de posts sobre reciprocidad en marketing"
  
  ContentGeneratorAgent:
    1. Busca en buyer_persona (contexto del cliente)
    2. Busca en customer_journey (fase de conciencia)
    3. Busca en conceptos aprendidos: "reciprocidad marketing"
       → Encuentra: Concepto de reciprocidad de Cialdini
       → Encuentra: Ejemplos del libro (muestras gratis, etc.)
    4. Genera ideas basadas en conceptos del libro + contexto del cliente
  
  Resultado:
    "Basándome en el principio de reciprocidad de Cialdini y tu buyer persona:
    
    1. Post: 'Guía gratuita de X' → explicar cómo genera reciprocidad
    2. Post: Video tutorial gratis → activar deseo de retribuir
    3. ...
    
    (Conceptos extraídos de 'Influence' de Robert Cialdini, Cap. 2)"

Valor generado:
  ✅ Agente tiene conocimiento profundo del libro
  ✅ Respuestas basadas en principios validados (no inventados)
  ✅ Cita fuentes (transparencia)
  ✅ Contexto personalizado (libro + buyer persona)
```

---

## 📝 NOTAS FINALES

```yaml
Filosofía de Integración:
  1. "Read first, code later": Usar Serena ANTES de tocar código
  2. "Reuse over rewrite": Si existe, usarlo; si falta, agregarlo
  3. "Extend, don't break": Mantener compatibilidad con código existente
  4. "Test integration, not isolation": Validar que todo funciona junto
  5. "Document for future you": El próximo dev debe entender la integración

Por qué Sistema Híbrido:
  - Combina lo mejor de RAG tradicional (búsqueda rápida) con comprensión profunda
  - Reduce dependencia de encontrar el chunk exacto
  - Permite respuestas más ricas y contextuales
  - El agente "entiende" el material, no solo lo tiene almacenado

Tiempo Estimado:
  - Fase 0 (Análisis): 1-2 días
  - Fase 1 (DB): 1 día
  - Fase 2 (BookLearningService): 3-4 días
  - Fase 3 (API): 2 días
  - Fase 4 (RAG Integration): 2 días
  - Fase 5 (Agents): 2 días
  - Fase 6 (Frontend): 3 días
  - Fase 7 (Testing): 2 días
  - TOTAL: 16-19 días
  - REALISTA: 3-4 semanas

Riesgos y Mitigaciones:
  - Riesgo: Romper código existente
    Mitigación: Tests de regresión exhaustivos
  
  - Riesgo: Performance degradada
    Mitigación: Benchmarks antes/después, optimizar índices
  
  - Riesgo: Extracción inconsistente de conceptos
    Mitigación: Prompts bien diseñados, validación Pydantic, retry logic
  
  - Riesgo: Rate limits de OpenAI
    Mitigación: Batch processing, exponential backoff, considerar tier pagado
```

---

**🎯 Este INITIAL.md está listo para generar un PRP completo que INTEGRE el sistema de aprendizaje progresivo con el proyecto Marketing Brain existente, sin duplicar código y aprovechando toda la infraestructura ya construida.**

**Énfasis clave:**
- ✅ Reutilizar servicios existentes (RAG, LLM, Embeddings)
- ✅ Extender agentes sin romperlos
- ✅ Agregar tablas sin modificar existentes
- ✅ Mantener compatibilidad total
- ✅ Análisis obligatorio con Serena antes de codificar