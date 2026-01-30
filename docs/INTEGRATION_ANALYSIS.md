# Análisis de Integración: Book Learning System

**Fecha:** 2026-01-30  
**Versión:** 1.0  
**Objetivo:** Documentar servicios a REUTILIZAR, EXTENDER y CREAR para el sistema de aprendizaje desde libros.

---

## 🎯 Principio Guía

```
REUTILIZAR > EXTENDER > CREAR
```

Minimizar código nuevo. Aprovechar infraestructura existente.

---

## 📊 Análisis de Servicios Existentes

### 1. RAGService (EXTENDER)

**Ubicación:** `backend/src/services/rag_service.py`  
**Líneas:** 14-351 (337 líneas)

| Método | Líneas | Acción | Justificación |
|--------|--------|--------|---------------|
| `__init__` | 26-42 | REUTILIZAR | Ya inyecta db, embedding_service, llm_service |
| `search_relevant_docs` | 44-120 | REUTILIZAR | Búsqueda semántica híbrida funcionando |
| `_vector_search` | 122-182 | REUTILIZAR | Búsqueda vectorial base |
| `_filter_by_metadata` | 184-219 | REUTILIZAR | Filtrado existente |
| `_rerank_with_llm` | 221-288 | REUTILIZAR | Reranking inteligente |
| `search_by_chat` | 290-351 | REUTILIZAR | Por chat_id |

**Métodos a AGREGAR (no modificar existentes):**
- `search_learned_concepts()` → Busca en conceptos extraídos
- `search_with_learned_knowledge()` → Búsqueda híbrida (conceptos + docs + KB)

**Variables existentes a usar:**
- `self.db` → AsyncSession
- `self.embedding_service` → EmbeddingService
- `self.llm_service` → LLMService

---

### 2. LLMService (REUTILIZAR SIN MODIFICAR)

**Ubicación:** `backend/src/services/llm_service.py`  
**Líneas:** 15-255 (240 líneas)

| Método | Líneas | Uso en BookLearningService |
|--------|--------|---------------------------|
| `generate(prompt, temperature)` | 45-91 | ✅ Extracción de conceptos |
| `stream()` | 93-139 | ❌ No necesario |
| `generate_with_messages()` | 141-197 | ❌ No necesario |
| `stream_with_messages()` | 199-255 | ❌ No necesario |

**Uso específico:**
```python
response = await self.llm.generate(
    prompt=concept_extraction_prompt,
    temperature=0.3  # Baja para extracción precisa
)
```

---

### 3. EmbeddingService (REUTILIZAR SIN MODIFICAR)

**Ubicación:** `backend/src/services/embedding_service.py`  
**Líneas:** 6-59 (53 líneas)

| Método | Líneas | Uso en BookLearningService |
|--------|--------|---------------------------|
| `generate_embedding(text)` | 18-31 | ✅ Query para búsqueda |
| `generate_embeddings_batch(texts)` | 33-59 | ✅ Batch de conceptos |

**Uso específico:**
```python
# Para embeddings de conceptos extraídos
embeddings = await self.embeddings.generate_embeddings_batch(
    [c.condensed_text for c in chunk_concepts]
)
```

**Variable importante:**
- `self.batch_size` → Ya maneja rate limiting

---

### 4. DocumentProcessor (REUTILIZAR PARCIALMENTE)

**Ubicación:** `backend/src/services/document_processor.py`  
**Líneas:** 12-100 (88 líneas)

| Componente | Acción | Justificación |
|------------|--------|---------------|
| `process_document()` | ESTUDIAR | Ver cómo parsea archivos |
| `self.splitter` | REUTILIZAR PATRÓN | RecursiveCharacterTextSplitter |

**Configuración de splitter a replicar:**
```python
self.splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Ajustar para libros
    chunk_overlap=200,  # Overlap para no perder contexto
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

---

## 📊 Análisis de Agentes Existentes

### 1. ContentGeneratorAgent (EXTENDER)

**Ubicación:** `backend/src/agents/content_generator_agent.py`  
**Líneas:** 15-588 (573 líneas)

| Método | Líneas | Acción |
|--------|--------|--------|
| `execute()` | 27-214 | MODIFICAR (agregar búsqueda de conceptos) |
| `_build_system_prompt()` | 275-468 | ESTUDIAR (para incluir conceptos) |
| Otros métodos | - | NO TOCAR |

**Modificación requerida en `execute()`:**
```python
# AGREGAR al contexto:
learned_concepts = await self._search_learned_concepts(query, project_id)
# Incluir en prompt junto con buyer_persona, customer_journey, etc.
```

### 2. RouterAgent (NO MODIFICAR)

**Ubicación:** `backend/src/agents/router_agent.py`
- No requiere cambios para Book Learning System

---

## 📊 Análisis de MemoryManager (CRÍTICO - Patrón a Seguir)

**Ubicación:** `backend/src/services/memory_manager.py`  
**Líneas:** 17-421 (404 líneas)

### Métodos Existentes (11 métodos)

| Método | Líneas | Propósito | Relevancia para Book Learning |
|--------|--------|-----------|------------------------------|
| `__init__` | 28-45 | Inicializa db, rag_service, llm_service | Patrón de inyección |
| `_get_short_term` | 47-50 | Obtiene memoria corto plazo | - |
| `get_context` | 52-121 | Contexto completo para agentes | **EXTENDER** para incluir conceptos |
| `add_message_to_short_term` | 123-140 | Añade mensaje a memoria | - |
| `format_messages_from_memory` | 142-199 | Convierte historial a messages[] | REUTILIZAR |
| `get_training_summary` | 201-296 | **Resumen de transcripciones** | **PATRÓN A SEGUIR** |
| `_get_buyer_persona_row` | 298-320 | Obtiene buyer persona | - |
| `_count_user_documents` | 322-347 | Cuenta documentos | - |
| `_get_document_summaries` | 349-371 | Resúmenes de docs | - |
| `load_chat_history` | 373-416 | Carga historial de BD | - |
| `ensure_chat_loaded` | 418-421 | Verifica carga | - |

### ⭐ PATRÓN CLAVE: `get_training_summary()` (líneas 201-296)

Este método es el **modelo a seguir** para el sistema de conceptos aprendidos:

```python
# Patrón existente en MemoryManager.get_training_summary():
# 1. Buscar chunks relevantes con RAG
# 2. Combinar chunks
# 3. Generar resumen con LLM
# 4. Cachear resultado
# 5. Retornar para inyectar en prompt
```

**Para BookLearningService:**
- Seguir mismo patrón pero con conceptos extraídos
- Crear `get_learned_concepts_summary()` similar
- Inyectar en `get_context()` junto con training_summary

### Variables Importantes

```python
self.db: AsyncSession
self.rag_service: RAGService  # Ya disponible
self.llm_service: LLMService  # Ya disponible
self._training_summary_cache: dict  # Patrón de caché a seguir
```

---

## 📊 Análisis de Base de Datos

### Tablas Existentes (8 tablas)

| Tabla | Acción | Notas |
|-------|--------|-------|
| `marketing_projects` | REUTILIZAR | FK para learned_books |
| `marketing_users` | REUTILIZAR | - |
| `marketing_chats` | REUTILIZAR | - |
| `marketing_messages` | REUTILIZAR | - |
| `marketing_buyer_persona` | REUTILIZAR | - |
| `marketing_knowledge_base` | EXTENDER | Agregar 2 columnas |
| `marketing_user_documents` | REUTILIZAR | - |
| `marketing_password_reset_tokens` | REUTILIZAR | - |

### MarketingKnowledgeBase - Columnas Actuales

```python
# Líneas 86-103 de backend/src/db/models.py
id: UUID
project_id: UUID (FK)
chat_id: UUID (FK)
content_type: String(50)  # CHECK: 'video_transcript', 'book', 'user_document'
source_title: String(500)
chunk_text: Text
chunk_index: Integer
metadata_: JSONB
embedding: Vector(1536)
created_at: TIMESTAMP
```

### Columnas a AGREGAR (Migración 003)

```sql
-- NO modificar existentes, solo agregar
ALTER TABLE marketing_knowledge_base 
ADD COLUMN IF NOT EXISTS knowledge_type VARCHAR(50) DEFAULT 'raw_chunk';
-- Valores: 'raw_chunk', 'extracted_concept', 'thematic_summary'

ALTER TABLE marketing_knowledge_base 
ADD COLUMN IF NOT EXISTS learned_book_id UUID REFERENCES marketing_learned_books(id) ON DELETE CASCADE;
```

### Migraciones Existentes

1. `001_initial_schema.sql` → Estructura base
2. `002_add_user_document_summary.sql` → Columna summary

### Nueva Migración

3. `003_book_learning_system.sql` → Tablas y columnas para Book Learning

---

## 🆕 Código Nuevo a Crear

### Servicios

| Archivo | Propósito | Dependencias |
|---------|-----------|--------------|
| `backend/src/services/book_learning_service.py` | Orquestador del pipeline | LLMService, EmbeddingService, DB |

### Schemas

| Archivo | Contenido |
|---------|-----------|
| `backend/src/schemas/knowledge.py` | ConceptExtraction, ThematicSummary, LearnedBookResponse, BookProcessingStatus |

### API

| Archivo | Endpoints |
|---------|-----------|
| `backend/src/api/knowledge.py` | POST/GET/DELETE /api/knowledge/* |

### Modelos

| Modelo | Tabla |
|--------|-------|
| `MarketingLearnedBook` | marketing_learned_books |
| `MarketingBookConcept` | marketing_book_concepts |

### Frontend

| Archivo | Componente |
|---------|------------|
| `frontend/app/components/BookUpload.tsx` | Drag & drop |
| `frontend/app/components/LearnedBookCard.tsx` | Tarjeta de libro |
| `frontend/app/components/ConceptsViewer.tsx` | Visualización |
| `frontend/app/dashboard/knowledge/page.tsx` | Página principal |

---

## ⚠️ IMPORTANTE: Funcionalidad YA EXISTENTE (NO DUPLICAR)

### LLMService - Métodos que YA existen:

| Método | Líneas | Estado |
|--------|--------|--------|
| `generate(prompt, temperature)` | 45-91 | ✅ EXISTE |
| `stream()` | 93-139 | ✅ EXISTE |
| `generate_with_messages(messages)` | 141-197 | ✅ EXISTE |
| `stream_with_messages(messages)` | 199-255 | ✅ EXISTE |

**⚠️ NO crear estos métodos, ya existen.**

### MemoryManager - Métodos que YA existen:

| Método | Líneas | Estado |
|--------|--------|--------|
| `format_messages_from_memory()` | 142-199 | ✅ EXISTE |
| `get_training_summary()` | 201-296 | ✅ EXISTE (patrón a seguir) |
| `get_context()` | 52-121 | ✅ EXISTE (extender, no reemplazar) |

**⚠️ USAR estos métodos existentes. Para conceptos, EXTENDER `get_context()`.**

---

## 📋 Trade-off Analysis (ADR)

### ADR-001: Extender vs Crear Nueva Tabla para Conceptos

**Contexto:** ¿Agregar columnas a `marketing_knowledge_base` o crear tabla nueva?

**Opciones:**
1. Agregar columnas a tabla existente
2. Crear `marketing_book_concepts` separada

**Decisión:** **Opción 2 - Tabla separada**

**Justificación:**
- Conceptos tienen estructura diferente (arrays, JSONB específico)
- Evita alterar funcionamiento existente de RAG
- Permite búsqueda especializada sin afectar queries actuales
- Principio: "Extend, don't modify"

**Trade-off:**
- (+) Aislamiento, no rompe existente
- (+) Flexibilidad de schema
- (-) Más JOINs en búsqueda híbrida
- (-) Mantenimiento de 2 tablas con embeddings

### ADR-002: Background Tasks vs Job Queue

**Contexto:** ¿Cómo procesar libros largos?

**Opciones:**
1. FastAPI BackgroundTasks (simple)
2. Redis + Celery/BullMQ (robusto)

**Decisión:** **Opción 1 - BackgroundTasks**

**Justificación:**
- MVP: simplicidad primero
- Proyecto ya tiene patrón establecido
- Se puede migrar a cola después si necesario

**Trade-off:**
- (+) Simple, sin dependencias nuevas
- (-) Si servidor reinicia, proceso se pierde
- Mitigación: Guardar progreso en DB

---

## ✅ Checklist de Verificación

- [x] Serena activado en proyecto brain-mkt
- [x] RAGService analizado (6 métodos, 3 variables)
- [x] LLMService analizado (4 métodos)
- [x] EmbeddingService analizado (2 métodos)
- [x] DocumentProcessor analizado (1 método, 3 variables)
- [x] ContentGeneratorAgent analizado (6 métodos)
- [x] GeneralChatAgent verificado (NO EXISTE)
- [x] MarketingKnowledgeBase analizado (10 columnas)
- [x] Migraciones existentes verificadas (2)
- [x] Trade-offs documentados (2 ADRs)
- [x] Lista clara de REUTILIZAR vs EXTENDER vs CREAR

---

## 🎯 Resumen Ejecutivo

| Categoría | Cantidad | Archivos |
|-----------|----------|----------|
| REUTILIZAR | 5 servicios | llm_service (4 métodos), embedding_service, document_processor, memory_manager (patrón get_training_summary), modelos existentes |
| EXTENDER | 3 archivos | rag_service.py (agregar search_learned_concepts), memory_manager.py (extender get_context), content_generator_agent.py |
| CREAR | 9 archivos | 1 servicio, 1 schema, 1 API, 2 modelos, 4 componentes frontend |

**⚠️ CRÍTICO:** 
- `LLMService.generate_with_messages()` YA EXISTE - NO recrear
- `MemoryManager.get_training_summary()` es PATRÓN A SEGUIR para conceptos
- `ContentGeneratorAgent` es el ÚNICO agente a modificar (GeneralChatAgent NO existe ni se creará)

**Principio cumplido:** Mínimo código nuevo, máxima reutilización.
