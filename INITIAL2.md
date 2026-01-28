# INITIAL2 - Marketing Second Brain System (Continuación y Mejoras)

## 📋 INFORMACIÓN DEL PROYECTO

```yaml
nombre: "Marketing Second Brain - Sistema de Estrategia de Contenido con IA"
version: "2.0.0"
fecha_inicio: "2026-01-26"
fecha_actualizacion: "2026-01-27"
estado_actual: "TAREAS 0-8.1 completadas, TAREAS 8.2-11 pendientes"
referencia_prp: "@PRPs/marketing-brain-system-v3.md"
tipo_proyecto: "Full-stack Web Application con AI Agent Conversacional Entrenado"
```

---

## 🎯 OBJETIVO DE ESTE PRP

**Continuar y mejorar** el sistema existente (documentado en `@PRPs/marketing-brain-system-v3.md`) con:

1. **TAREA 8.3**: Arreglar sistema conversacional (agente general + ContentGenerator que respeta intención)
2. **TAREA 9**: MCP Custom del Proyecto
3. **TAREA 10**: Docker + Deployment
4. **TAREA 11**: Testing End-to-End + Documentación Final

**⚠️ CRÍTICO**: Este PRP **NO** reemplaza el anterior, sino que **continúa** desde donde quedó. Todo lo implementado en TAREAS 0-8.1 está funcionando y debe **aprovecharse** sin duplicar código.

**⚠️ IMPORTANTE**: El sistema actual usa **RAG (Retrieval-Augmented Generation)** para entrenar el agente con transcripciones de YouTube y libros de marketing. El objetivo futuro es implementar **fine-tuning real** del modelo (no contexto largo), pero eso está fuera del scope de este PRP.

---

## 📊 ESTADO ACTUAL DEL PROYECTO (Lo que YA funciona)

### Backend (FastAPI + Python 3.11)

**✅ Completado (TAREAS 0-8.1):**

1. **Base de Datos (Supabase + pgvector)**:
   - 8 tablas con prefijo `marketing_` creadas
   - Extensión `pgvector` habilitada
   - Función `marketing_match_documents()` para búsqueda semántica
   - Índices HNSW para embeddings
   - **Migración 002**: Columna `summary` en `marketing_user_documents` (ejecutada manualmente)

2. **Autenticación Manual**:
   - `POST /api/auth/register` (con validación de password strength)
   - `POST /api/auth/login` (JWT en httpOnly cookies)
   - `POST /api/auth/logout` (limpia cookie)
   - Middleware `get_current_user` lee cookie `auth_token` + fallback a Bearer header
   - **NO usa Supabase Auth** (restricción de emails)

3. **Sistema de Chat**:
   - `GET /api/chats` (listar chats del usuario)
   - `POST /api/chats` (crear chat)
   - `PATCH /api/chats/{chat_id}/title` (editar título) ✅ **YA IMPLEMENTADO**
   - `DELETE /api/chats/{chat_id}` (eliminar chat) ✅ **YA IMPLEMENTADO**
   - `GET /api/chats/{chat_id}/messages` (historial)
   - `POST /api/chats/{chat_id}/messages` (mensaje no-streaming)
   - `POST /api/chats/{chat_id}/stream` (SSE streaming)
   
   **Nota:** La funcionalidad de editar y eliminar chats ya está implementada en el backend. Solo falta integrarla en el frontend (ver TAREA 8.3).

4. **Procesamiento de Documentos**:
   - `POST /api/documents/upload/{chat_id}` (sube .txt, .pdf, .docx)
   - `GET /api/documents/chat/{chat_id}` (lista documentos)
   - `DELETE /api/documents/{document_id}` (elimina documento)
   - Parsers para .txt, .pdf, .docx
   - Chunking con `RecursiveCharacterTextSplitter`
   - Embeddings con OpenAI `text-embedding-3-small`
   - **Resúmenes persistentes** (contexto largo) generados al subir

5. **Sistema de Memoria Triple**:
   - **Short-term**: `ConversationBufferWindowMemory` **por chat_id** (no global)
   - **Long-term**: `MarketingBuyerPersona` (full_analysis, forum_simulation, pain_points, customer_journey)
   - **Semantic**: `RAGService` con búsqueda híbrida (vector + keyword + reranking)
   - `MemoryManager` carga historial desde DB al iniciar chat
   - `document_summaries` incluidos en contexto largo

6. **Agentes IA**:
   - `RouterAgent`: Routing rule-based (BUYER_PERSONA, CONTENT_GENERATION, WAITING)
   - `BuyerPersonaAgent`: ✅ **YA GENERA COMPLETO** (plantilla completa + foro + pain points + customer journey automáticamente)
   - `ContentGeneratorAgent`: Genera ideas de contenido (pendiente: respetar intención específica del usuario)
   - `BaseAgent`: Clase base con acceso a `llm` y `memory`

7. **Entrenamiento del Agente (RAG)**:
   - ✅ **9 transcripciones de YouTube de Andrea Estratega** ya ingeridas en `marketing_knowledge_base` (project_id=NULL, chat_id=NULL)
   - ✅ Script `ingest_training_data.py` procesa transcripciones → chunks → embeddings → DB
   - ✅ `RAGService` busca en knowledge base global al generar contenido
   - ✅ El agente está **entrenado** con técnicas virales de creación de contenido (vía RAG)
   - ⚠️ **Futuro**: Fine-tuning real del modelo (no contexto largo) - fuera del scope actual

8. **Endpoints de Visualización**:
   - `GET /api/chats/{chat_id}/buyer-persona` (JSON completo)
   - `GET /api/chats/{chat_id}/analysis` (resumen con flags)

9. **Streaming (SSE)**:
   - `RouterAgent.process_stream()` genera chunks JSON
   - Middleware respeta endpoints `/stream` (no lee body)

**Archivos Backend (existentes y funcionando):**
- `backend/src/api/auth.py`
- `backend/src/api/chat.py`
- `backend/src/api/documents.py`
- `backend/src/api/analysis.py` ✅ (nuevo en TAREA 8.1)
- `backend/src/agents/router_agent.py`
- `backend/src/agents/buyer_persona_agent.py` ✅ (YA genera foro + pain points + CJ automáticamente)
- `backend/src/agents/content_generator_agent.py`
- `backend/src/agents/base_agent.py`
- `backend/src/services/memory_manager.py`
- `backend/src/services/llm_service.py` (OpenAI/OpenRouter configurable)
- `backend/src/services/rag_service.py` (búsqueda híbrida con reranking)
- `backend/src/services/embedding_service.py`
- `backend/src/services/document_processor.py`
- `backend/src/services/chat_service.py`
- `backend/src/schemas/analysis.py` ✅ (nuevo en TAREA 8.1)
- `backend/src/db/models.py`
- `backend/db/001_initial_schema.sql`
- `backend/db/002_add_user_document_summary.sql` ✅ (nuevo en TAREA 8.1)
- `backend/scripts/ingest_training_data.py` ✅ (ya ejecutado, transcripciones ingeridas)

### Frontend (Next.js 14 + TypeScript + Tailwind)

**✅ Completado (TAREAS 7-8.1):**

1. **Autenticación**:
   - `/login` (Client Component)
   - `/register` (Client Component)
   - Middleware protege rutas privadas
   - Cookies httpOnly para JWT

2. **Layout Base**:
   - Root layout con Inter font
   - Suspense boundaries para `useSearchParams`
   - `ChatPageContent` (Client Component) encapsula lógica de chat

3. **Interfaz de Chat**:
   - `ChatInterface.tsx`: Mensajes + input + streaming SSE
   - `MessageList.tsx`: Lista con auto-scroll
   - `DocumentUpload.tsx`: Subida de archivos con feedback
   - `Sidebar.tsx`: Lista de chats + crear nuevo + logout
   - `AnalysisPanel.tsx`: Visualización de buyer persona/analysis ✅ (nuevo en TAREA 8.1)

4. **API Clients**:
   - `lib/api.ts`: Auth (login, register, logout)
   - `lib/api-chat.ts`: Chat (listChats, getChat, getMessages, createChat, streamMessage, uploadDocument)
   - `lib/api-analysis.ts`: Analysis (getChatAnalysis) ✅ (nuevo en TAREA 8.1)

**Archivos Frontend (existentes y funcionando):**
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`
- `frontend/app/login/page.tsx`
- `frontend/app/register/page.tsx`
- `frontend/middleware.ts`
- `frontend/app/components/ChatInterface.tsx`
- `frontend/app/components/MessageList.tsx`
- `frontend/app/components/DocumentUpload.tsx`
- `frontend/app/components/Sidebar.tsx`
- `frontend/app/components/ChatPageContent.tsx`
- `frontend/app/components/AnalysisPanel.tsx` ✅ (nuevo en TAREA 8.1)
- `frontend/lib/types.ts`
- `frontend/lib/api.ts`
- `frontend/lib/api-chat.ts`
- `frontend/lib/api-analysis.ts` ✅ (nuevo en TAREA 8.1)

**Pendiente en Frontend:**
- ⚠️ Editar nombre de chat (backend listo, falta UI en `Sidebar.tsx`)
- ⚠️ Eliminar chat (backend listo, falta UI en `Sidebar.tsx`)

---

## 🚨 PROBLEMA IDENTIFICADO (A resolver en este PRP)

### Problema: Sistema NO es Conversacional

**Síntoma:**
- Cualquier mensaje del usuario (incluso "dame 2 ideas") termina generando 10 ideas de reels
- No respeta intención específica (cantidad, tipo de contenido, formato)
- No puede mantener conversación general (preguntas, análisis, estrategias, planes de marketing)

**Causa Raíz:**
- `RouterAgent` solo tiene 2 estados "inteligentes": `BUYER_PERSONA` y `CONTENT_GENERATION`
- `_is_content_request()` es demasiado estricto pero luego TODO cae en `CONTENT_GENERATION`
- No hay agente de "conversación general" que responda preguntas/estrategias sin generar contenido
- `ContentGeneratorAgent` tiene prompt hardcodeado "Genera mínimo 5 ideas (ideal 7-10)" que ignora la intención del usuario

**Solución Propuesta (TAREA 8.3):**
- Agregar estado `GENERAL_CHAT` para conversación normal
- Crear `GeneralChatAgent` para preguntas/estrategias/planes (no generación de contenido)
- Mejorar `ContentGeneratorAgent` para parsear intención (count, tipo, formato) y respetarla
- Usar LLM para clasificación de intención (más preciso que keywords)

---

## 🏗️ STACK TECNOLÓGICO (Sin cambios, aprovechar existente)

### Frontend
```yaml
Framework: Next.js 14 (App Router) ✅
Lenguaje: TypeScript ✅
UI Framework: TailwindCSS ✅
Estado: React hooks (useState, useEffect) ✅
Real-time: Server-Sent Events (SSE) ✅
```

### Backend
```yaml
Framework: FastAPI (Python 3.11+) ✅
Validación: Pydantic v2 ✅
ORM: SQLAlchemy 2.0 async ✅
IA Framework: LangChain (memoria) ✅
LLM: OpenAI / OpenRouter (configurable) ✅
Embeddings: OpenAI text-embedding-3-small ✅
Vector Store: Supabase pgvector ✅
Entrenamiento: RAG (Retrieval-Augmented Generation) ✅
```

### Base de Datos
```yaml
Proveedor: Supabase (PostgreSQL + pgvector) ✅
Ubicación: VPS del usuario ✅
8 tablas con prefijo marketing_ ✅
Función marketing_match_documents() ✅
```

---

## 🔌 MCPs A UTILIZAR (Igual que PRP original)

### 1. MCP Archon (⚡ PRIORITARIO)
- Consultar documentación oficial durante desarrollo
- Especialmente para: LangGraph, agentes conversacionales, intent classification, fine-tuning patterns

### 2. MCP Serena (⚡ OBLIGATORIO)
- Análisis simbólico antes de modificar código
- Localizar símbolos exactos, ver impacto de cambios
- **CRÍTICO**: Usar SIEMPRE antes de crear código nuevo para evitar duplicación

### 3. MCP Custom (TAREA 9)
- Crear MCP "marketing-brain" con tools del proyecto

---

## 📚 SKILLS A UTILIZAR

**Skills activadas por defecto:**
- `python-patterns` (automático)
- `clean-code` (automático)

**Skills específicas para agentes conversacionales:**
- `autonomous-agents` (patrones de agentes, routing, loops)
- `ai-agents-architect` (diseño de agentes, tool use, planning)
- `agent-memory-systems` (arquitectura de memoria)
- `conversation-memory` (memoria persistente de conversaciones)
- `langgraph` (orquestación de agentes con estado)
- `llm-app-patterns` (patrones de apps LLM, RAG, streaming)

**Skills específicas para fine-tuning (futuro, fuera del scope actual):**
- `rag-engineer` (RAG avanzado, puede incluir técnicas de fine-tuning)
- `rag-implementation` (implementación de RAG)
- `prompt-engineer` (ingeniería de prompts, puede incluir técnicas de fine-tuning)
- `context-window-management` (gestión de contexto largo, alternativo a fine-tuning)

**Nota:** Fine-tuning real del modelo requiere investigación adicional y está fuera del scope de este PRP. El sistema actual usa RAG que funciona bien, pero el objetivo futuro es implementar fine-tuning.

---

## 🎯 TAREAS PENDIENTES (Este PRP)

### TAREA 8.3: Sistema Conversacional General + ContentGenerator Mejorado

**Referencia PRP Original:** Basado en diagnóstico `docs/DIAGNOSTICO_MEMORIA_Y_CONTEXTO.md`

**Estado:** Pendiente (sistema actual solo genera contenido, no conversa)

**Objetivo:**
Hacer el sistema verdaderamente conversacional:
- Agregar agente de "conversación general" para preguntas/estrategias/planes
- Mejorar `ContentGeneratorAgent` para respetar intención específica (count, tipo, formato)
- Integrar edición/eliminación de chats en frontend

**Herramientas a utilizar:**
- 🔧 MCP Serena: analizar `RouterAgent.route()` y `ContentGeneratorAgent.execute()` ANTES de modificar
  - Comando: `find_symbol('RouterAgent/route', 'backend/src/agents/router_agent.py', True)`
  - Comando: `find_symbol('ContentGeneratorAgent/execute', 'backend/src/agents/content_generator_agent.py', True)`
  - Comando: `get_symbols_overview('backend/src/agents/')` para ver estructura completa
- ⚡ MCP Archon: patrones de intent classification con LLM, LangGraph routing
  - Comando: `rag_search_knowledge_base(query="intent classification LLM agent routing", match_count=5)`
  - Comando: `rag_search_knowledge_base(query="LangGraph conversational agent general chat vs content generation", match_count=5)`
- 📚 Skills:
  - **autonomous-agents** (routing inteligente, agent loops)
  - **ai-agents-architect** (diseño de agentes conversacionales)
  - **conversation-memory** (conversación natural)
  - **langgraph** (orquestación de agentes con estado)
  - **llm-app-patterns** (patrones de apps LLM)
  - python-patterns (automático)
  - clean-code (automático)

**Pasos a seguir:**

1. **Investigar código existente con Serena:**
   - Ver estructura completa de `RouterAgent` y `ContentGeneratorAgent`
   - Identificar dónde se puede agregar `GENERAL_CHAT` sin romper lógica existente
   - Verificar que no exista código similar ya implementado

2. **Agregar estado `GENERAL_CHAT` en RouterAgent:**
   - Modificar `AgentState` enum (en `backend/src/agents/router_agent.py` o donde esté definido)
   - Lógica: Si hay buyer persona Y NO es petición explícita de contenido → `GENERAL_CHAT`
   - Mejorar `_is_content_request()` para ser más preciso (usar regex más estricto)

3. **Crear `GeneralChatAgent`:**
   - Nuevo archivo: `backend/src/agents/general_chat_agent.py`
   - Hereda de `BaseAgent`
   - `execute()`: Responde preguntas/estrategias usando buyer persona + CJ + docs como contexto
   - NO genera ideas de contenido, solo conversa/analiza/planifica
   - Usa mismo contexto que `ContentGeneratorAgent` pero con prompt diferente

4. **Mejorar `ContentGeneratorAgent`:**
   - Parsear intención del mensaje:
     - Extraer `count` (número de ideas solicitadas) usando regex o LLM
     - Extraer `tipo` (reels, posts, videos, scripts, guiones, planes)
     - Extraer `formato` (ideas, script completo, plan, etc.)
   - Ajustar prompt para respetar estos parámetros
   - Recortar salida al `count` solicitado (red de seguridad)
   - Eliminar hardcodeo "Genera mínimo 5 ideas (ideal 7-10)"

5. **Integrar en RouterAgent:**
   - `route()` ahora puede retornar `GENERAL_CHAT`
   - `process_stream()` maneja `GENERAL_CHAT` → llama `GeneralChatAgent`

6. **Integrar en endpoints:**
   - `POST /api/chats/{chat_id}/stream` → ejecuta `GeneralChatAgent` si estado es `GENERAL_CHAT`
   - `POST /api/chats/{chat_id}/messages` → igual

7. **Integrar edición/eliminación de chats en Frontend:**
   - Modificar `Sidebar.tsx` para permitir editar título (inline edit o modal)
   - Agregar botón de eliminar con confirmación
   - Usar `PATCH /api/chats/{chat_id}/title` y `DELETE /api/chats/{chat_id}` (ya existen)
   - Actualizar `lib/api-chat.ts` con funciones `updateChatTitle()` y `deleteChat()` si no existen
   - Verificar con Serena que no existan estas funciones antes de crearlas

**Archivos a crear:**
- `backend/src/agents/general_chat_agent.py`

**Archivos a modificar:**
- `backend/src/agents/router_agent.py` (agregar `GENERAL_CHAT`, mejorar routing)
- `backend/src/agents/content_generator_agent.py` (parsear intención, respetar count)
- `backend/src/api/chat.py` (manejar `GENERAL_CHAT`)
- `frontend/app/components/Sidebar.tsx` (editar/eliminar chats) ⚠️ **NUEVO**
- `frontend/lib/api-chat.ts` (agregar `updateChatTitle`, `deleteChat` si no existen) ⚠️ **NUEVO**

**Criterios de aceptación:**
- [ ] "dame 2 ideas" → genera exactamente 2 ideas (no 10)
- [ ] "desarrolla un plan de marketing" → `GeneralChatAgent` responde (no ContentGenerator)
- [ ] "escribe un guion para..." → ContentGenerator genera guion (no ideas)
- [ ] Conversación fluida sin siempre generar contenido
- [ ] Usuario puede editar nombre de chat desde UI
- [ ] Usuario puede eliminar chat desde UI con confirmación

---

### TAREA 9: MCP Custom del Proyecto

**Referencia PRP Original:** `@PRPs/marketing-brain-system-v3.md` - TAREA 9 (líneas 4948-5024)

**Estado:** Pendiente

**Objetivo:**
Crear MCP "marketing-brain-mcp" que expone tools del sistema para Cursor.

**Herramientas a utilizar:**
- ⚡ MCP Archon: MCP Protocol, FastMCP patterns
  - Comando: `rag_search_knowledge_base(query="MCP server python custom tools FastMCP", match_count=5)`
- 🔧 MCP Serena: Analizar estructura de MCPs existentes
  - Comando: `get_symbols_overview('Context-Engineering-Intro/examples/mcp-server/')`
- 📚 Skills:
  - **mcp-builder** (construcción de MCPs)
  - **agent-tool-builder** (diseño de tools)
  - python-patterns (automático)
  - clean-code (automático)

**Pasos a seguir:**

1. **Crear estructura:**
   ```bash
   mkdir -p mcp-marketing-brain/src
   cd mcp-marketing-brain
   touch pyproject.toml README.md
   ```

2. **Implementar servidor MCP (FastMCP):**
   - `mcp-marketing-brain/src/server.py`
   - Tools:
     - `get_buyer_persona(chat_id: str)`
     - `list_chats(project_id: str)`
     - `generate_content_ideas(chat_id: str, phase: str, content_type: str, count: int)`
     - `search_knowledge_base(query: str, limit: int)`

3. **Conectar con backend FastAPI:**
   - HTTP requests a endpoints existentes
   - Autenticación con API key interna

4. **Registrar en Cursor:**
   - Configurar en `~/.cursor/mcp-config.json`

**Archivos a crear:**
- `mcp-marketing-brain/src/server.py`
- `mcp-marketing-brain/pyproject.toml`
- `mcp-marketing-brain/README.md`

**Criterios de aceptación:**
- [ ] MCP server funciona en Cursor
- [ ] Tools expuestas funcionan
- [ ] Cursor puede invocar tools desde chat

---

### TAREA 10: Docker + Deployment

**Referencia PRP Original:** `@PRPs/marketing-brain-system-v3.md` - TAREA 10 (líneas 5027-5144)

**Estado:** Pendiente

**Objetivo:**
Dockerizar aplicación completa para desarrollo local y producción.

**Herramientas a utilizar:**
- ⚡ MCP Archon: Docker best practices, multi-stage builds
  - Comando: `rag_search_knowledge_base(query="docker compose multi-container production", match_count=5)`
- 📚 Skills:
  - **docker-expert** (containerización, optimización)
  - **deployment-procedures** (estrategias de deployment)
  - clean-code (automático)

**Pasos a seguir:**

1. **Crear Dockerfiles:**
   - `backend/Dockerfile` (multi-stage, Python 3.11-slim)
   - `frontend/Dockerfile` (multi-stage, Node 20-alpine)

2. **Crear docker-compose.yml:**
   - 3 servicios: frontend, backend, redis
   - Named volumes (GOTCHA 8: evitar bind mounts en Windows)
   - Variables de entorno desde `.env`

3. **Scripts de deployment:**
   - `scripts/docker-build.sh`
   - `scripts/docker-up.sh`
   - `scripts/docker-logs.sh`

**Archivos a crear:**
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `scripts/docker-build.sh`
- `scripts/docker-up.sh`

**Criterios de aceptación:**
- [ ] `docker compose up` inicia todos los servicios
- [ ] Frontend accesible en :3000
- [ ] Backend accesible en :8000
- [ ] Named volumes persisten datos
- [ ] Sin problemas de permisos (GOTCHA 8)

---

### TAREA 11: Testing End-to-End + Documentación Final

**Referencia PRP Original:** `@PRPs/marketing-brain-system-v3.md` - TAREA 11 (líneas 5147-5218)

**Estado:** Pendiente

**Objetivo:**
Suite completa de tests + documentación final.

**Herramientas a utilizar:**
- ⚡ MCP Archon: Pytest patterns, testing best practices
  - Comando: `rag_search_code_examples(query="pytest async fixtures", match_count=3)`
- 📚 Skills:
  - **testing-patterns** (unit, integration, E2E)
  - **verification-before-completion** (validación exhaustiva)
  - python-patterns (automático)

**Pasos a seguir:**

1. **Tests E2E:**
   - `backend/tests/integration/test_full_flow.py`
   - Flujo completo: registro → chat → buyer persona → contenido

2. **Actualizar README.md:**
   - Quick start
   - Troubleshooting
   - Ejemplos de uso

3. **Documentación API:**
   - Verificar `/docs` de FastAPI
   - Documentar endpoints principales

**Archivos a crear:**
- `backend/tests/integration/test_full_flow.py`
- `README.md` (actualizar)

**Criterios de aceptación:**
- [ ] Tests E2E pasan al 100%
- [ ] Coverage >80%
- [ ] README completo
- [ ] Sistema funciona end-to-end

---

## 🚧 CONSIDERACIONES TÉCNICAS CRÍTICAS

### ⚠️ Evitar Duplicación de Código

**Reglas estrictas:**
- ❌ NO crear funciones que ya existen (usar `ChatService`, `MemoryManager`, etc.)
- ❌ NO cambiar nombres de parámetros existentes
- ❌ NO crear nuevos agentes si la lógica cabe en agentes existentes
- ✅ SIEMPRE usar Serena antes de crear código nuevo
- ✅ SIEMPRE verificar con `grep` si existe función similar

**Ejemplos de código existente a aprovechar:**
- `ChatService.update_chat_title()` ✅ (ya existe)
- `ChatService.delete_chat()` ✅ (ya existe)
- `MemoryManager.get_context()` ✅ (ya incluye todo lo necesario)
- `RAGService.search_relevant_docs()` ✅ (ya funciona)
- `BuyerPersonaAgent` ✅ (YA genera foro + pain points + CJ automáticamente)

### 🔐 Seguridad (Sin cambios)

- JWT en httpOnly cookies ✅
- Passwords con bcrypt ✅
- Validación Pydantic en todos los endpoints ✅
- Aislamiento por `project_id` ✅

### ⚡ Performance (Sin cambios)

- Búsqueda vectorial con HNSW ✅
- Streaming SSE ✅
- Connection pooling ✅

### 🎓 Entrenamiento del Agente

**Estado Actual:**
- ✅ **RAG (Retrieval-Augmented Generation)**: Transcripciones de YouTube ya ingeridas en `marketing_knowledge_base`
- ✅ El agente está **entrenado** con técnicas virales de creación de contenido (vía RAG)
- ✅ `ContentGeneratorAgent` busca en knowledge base global al generar contenido

**Futuro (Fuera del scope de este PRP):**
- ⚠️ **Fine-tuning real**: Entrenar el modelo LLM con las transcripciones (no contexto largo)
- ⚠️ Requiere investigación adicional sobre:
  - Librerías de fine-tuning (OpenAI fine-tuning API, LangGraph fine-tuning, etc.)
  - Preparación de datos para fine-tuning
  - Costos y limitaciones
  - Evaluación del modelo fine-tuneado

**Nota:** El sistema actual con RAG funciona bien, pero el objetivo futuro es implementar fine-tuning real del modelo para mejor consistencia y menor costo en el largo plazo.

---

## 📖 RECURSOS DEL PROYECTO (Aprovechar existentes)

### Plantillas y Prompts

1. **Buyer Persona Template:**
   - Archivo: `contenido/buyer-plantilla.md` ✅ (existe, YA se usa completo en BuyerPersonaAgent)
   - Secciones: 11 categorías con 40+ preguntas
   - Ejemplos: Caso "Ana" (usar como guía, no copiar)

2. **Prompts de Foro y CJ:**
   - Archivo: `contenido/promts_borradores.md` ✅ (existe)
   - Foro: Líneas 16-18 (YA implementado en BuyerPersonaAgent)
   - CJ: Líneas 22-30 (YA implementado en BuyerPersonaAgent)

### Material de Entrenamiento

- ✅ **9 transcripciones de YouTube de Andrea Estratega**: Ya ingeridas en `marketing_knowledge_base` (project_id NULL)
- ✅ Script `ingest_training_data.py` ya ejecutado
- ✅ El agente está **entrenado** con estas técnicas (vía RAG)

---

## 🎯 CRITERIOS DE ÉXITO (Actualizados)

**Funcionalidad:**
- [x] Usuario puede registrarse, login, logout ✅
- [x] Usuario puede crear chats ✅
- [x] Usuario puede subir documentos ✅
- [x] Sistema recuerda contexto de conversación ✅
- [x] Streaming funcional ✅
- [x] Buyer persona usa plantilla completa ✅ (YA implementado)
- [x] Foro + pain points + CJ generados automáticamente ✅ (YA implementado)
- [ ] Sistema conversacional (preguntas/estrategias sin generar contenido) (TAREA 8.3)
- [ ] ContentGenerator respeta intención (count, tipo, formato) (TAREA 8.3)
- [ ] Usuario puede editar/eliminar chats desde UI (TAREA 8.3)
- [ ] MCP custom funcional (TAREA 9)
- [ ] Docker funcionando (TAREA 10)
- [ ] Tests >80% coverage (TAREA 11)

**Calidad:**
- [x] Sin errores de linting ✅
- [x] Sin errores de tipos ✅
- [ ] Tests >80% coverage (TAREA 11)
- [ ] Documentación completa (TAREA 11)

---

## 📝 NOTAS FINALES

**Filosofía:**
1. **Aprovechar código existente**: No duplicar, extender
2. **Serena primero**: Análisis simbólico antes de modificar
3. **Archon siempre**: Documentación oficial antes de implementar
4. **Coherencia de parámetros**: No cambiar nombres existentes
5. **Backend y frontend funcionan**: Mejorar, no rehacer
6. **Agente entrenado**: El sistema usa RAG con transcripciones de YouTube (entrenamiento contextual)
7. **Fine-tuning futuro**: Objetivo es implementar fine-tuning real del modelo (no contexto largo), pero está fuera del scope actual

**Referencias:**
- PRP Original: `@PRPs/marketing-brain-system-v3.md`
- Diagnóstico: `docs/DIAGNOSTICO_MEMORIA_Y_CONTEXTO.md`
- Tareas y Gotchas: `docs/TAREAS_PENDIENTES_Y_GOTCHAS.md`

**Ejemplos de Referencia:**
- `/home/david/brain-mkt/Context-Engineering-Intro/examples/basic_chat_agent/agent.py` (PydanticAI patterns)
- `/home/david/brain-mkt/Context-Engineering-Intro/examples/main_agent_reference/` (multi-agent patterns)

---

**🎯 Este INITIAL2.md continúa el proyecto desde TAREA 8.3, aprovechando todo lo implementado en TAREAS 0-8.1, y resuelve el problema conversacional identificado. El sistema ya está entrenado con RAG y el buyer persona ya genera todo automáticamente.**
