# INITIAL - Marketing Second Brain System

## 📋 INFORMACIÓN DEL PROYECTO

```yaml
nombre: "Marketing Second Brain - Sistema de Estrategia de Contenido con IA"
version: "1.0.0"
fecha_inicio: "2026-01-26"
entorno_inicial: "Local (Docker) → VPS (Portainer después)"
tipo_proyecto: "Full-stack Web Application con AI Agent"
```

---

## 🎯 FEATURE PRINCIPAL

### Sistema de Segundo Cerebro de Marketing con Agente IA

**Descripción General:**

Sistema web que funciona como un "segundo cerebro" para estrategia de marketing digital. Permite a los usuarios crear estrategias de contenido basadas en:

1. **Análisis profundo de Buyer Persona** (mediante cuestionario y plantilla completa)
2. **Simulación de comportamiento real** (buyer persona actuando en foro de internet)
3. **Customer Journey detallado** (3 fases de conciencia con 20 preguntas por fase)
4. **Generación de contenido de valor** (posts, videos, ideas) basado en conocimiento entrenado

**Flujo del Usuario:**

```mermaid
FASE 1 - ANÁLISIS INICIAL:
Usuario → Registro/Login → Dashboard Chat → Nuevo Chat →
→ Agente hace 4-5 preguntas iniciales →
→ Usuario responde preguntas →
→ [OPCIONAL] Usuario sube documentos (.txt, .pdf, .docx) sobre su negocio →
→ Agente procesa documentos subidos →
→ Agente completa Buyer Persona (plantilla completa) →
→ Agente simula persona en foro (quejas + soluciones) →
→ Agente extrae 10 puntos de dolor →
→ Agente genera Customer Journey (3 fases × 20 preguntas) →
→ Agente ENTREGA documento completo al usuario →
→ Agente GUARDA TODO en memoria (3 tipos) →
→ ⏸️ AGENTE ESPERA PETICIONES DEL USUARIO

FASE 2 - GENERACIÓN DE CONTENIDO (ON-DEMAND):
Usuario pide: "Dame 5 ideas de videos para fase de conciencia" →
→ Agente consulta memoria (buyer + CJ) →
→ Agente busca en knowledge_base (YouTubers + libros) →
→ Agente busca en documentos subidos del usuario →
→ Agente GENERA respuesta personalizada →
→ Usuario recibe ideas accionables →
→ Usuario pide: "Escríbeme el script del video 3" →
→ Agente GENERA script basado en contexto →
→ ... ciclo continúa según peticiones del usuario

IMPORTANTE: El agente NO genera contenido automáticamente.
            Solo responde cuando el usuario lo solicita.
            Mantiene contexto de conversación + memoria persistente.
```

**Valor Diferencial:**

- ✅ **No es un chatbot genérico**: Está entrenado específicamente en creación de contenido de redes sociales
- ✅ **Contexto persistente**: Recuerda el buyer persona, puntos de dolor, customer journey + documentos del usuario
- ✅ **Entrenamiento con material real**: Transcripciones de YouTubers exitosos + libros de marketing
- ✅ **Salida accionable**: Genera contenido listo para usar, no solo teoría
- ✅ **On-demand**: Solo genera cuando el usuario lo pide, no automáticamente
- ✅ **Ingesta de documentos**: Usuario sube .txt, .pdf, .docx con info de su negocio

---

## 🏗️ STACK TECNOLÓGICO

### Frontend

```yaml
Framework: Next.js 14 (App Router)
Lenguaje: TypeScript
UI Framework: TailwindCSS + shadcn/ui (componentes modernos)
Estado Global: Zustand o React Context (para chat y sesión)
Real-time: WebSocket o Server-Sent Events (para streaming de respuestas IA)

Estructura:
  app/
    (auth)/
      - login/
      - register/
      - recover-password/
    dashboard/
      - page.tsx (chat interface)
      - layout.tsx (sidebar con lista de chats)
    api/
      - chat/route.ts (proxy a backend Python)
      - auth/route.ts (manejo de sesión)

Componentes Clave:
  - ChatInterface: Mensajes + input + streaming
  - ChatSidebar: Lista de conversaciones + edición de título
  - AuthGuard: Protección de rutas
  - BuyerPersonaViewer: Vista del documento generado
  - DocumentUploader: Subida de .txt, .pdf, .docx
  - DocumentsList: Lista de documentos subidos por el usuario
```

### Backend - Agente IA

```yaml
Framework: FastAPI (Python 3.11+)
Validación: Pydantic v2 (usar Archon para documentación oficial)
ORM: SQLAlchemy 2.0 + Alembic (migraciones)
IA Framework: LangChain + LangGraph (para agente con memoria)
LLM: Anthropic Claude 3.5 Sonnet o OpenAI GPT-4 Turbo
Embeddings: OpenAI text-embedding-3-large o similar
Vector Store: Supabase pgvector (mismo DB)

Arquitectura del Agente:
  1. Router Agent: Decide qué herramienta usar según petición del usuario
  2. Document Processor: Procesa documentos subidos (.txt, .pdf, .docx)
  3. Buyer Persona Specialist: Genera análisis completo
  4. Forum Simulator: Simula comportamiento en foro
  5. Customer Journey Creator: Genera las 3 fases
  6. Content Generator: Crea posts/videos SOLO cuando usuario lo pide
  7. Memory Manager: Gestiona 3 tipos de memoria + documentos subidos

FLUJO CRÍTICO:
  - Agente genera análisis → ENTREGA al usuario → GUARDA en memoria
  - Agente ESPERA a que usuario haga peticiones específicas
  - Agente RESPONDE basándose en: memoria + entrenamiento + docs subidos

Memoria del Agente (CRÍTICO):
  
  Tipo 1 - Short-term Memory (Ventana de contexto):
    - Últimas 10-15 interacciones del chat actual
    - Buffer de conversación con resumen automático
    - Implementar con ConversationBufferWindowMemory (LangChain)
  
  Tipo 2 - Long-term Memory (Base de datos):
    - Buyer persona completo (JSON en Supabase)
    - Customer journey (JSON en Supabase)
    - Puntos de dolor y soluciones (JSON)
    - Documentos subidos por el usuario (metadata + path)
    - Metadatos: proyecto_id, chat_id, created_at
  
  Tipo 3 - Semantic Memory (Vector Store):
    - Embeddings del buyer persona
    - Embeddings del customer journey
    - Embeddings de transcripciones de entrenamiento (global)
    - Embeddings de libros de marketing (global)
    - Embeddings de documentos subidos por usuario (por chat)
    - Búsqueda semántica con pgvector en Supabase
    - k=10 documentos más relevantes por consulta
  
  IMPORTANTE: Cuando usuario pide contenido, el agente busca en:
    1. Buyer persona del chat actual (long-term)
    2. Customer journey del chat actual (long-term)
    3. Documentos subidos del chat actual (semantic)
    4. Knowledge base global (semantic: YouTubers + libros)
    5. Conversación reciente (short-term)

Entrenamiento del Agente (In-Context Learning):
  
  Fase 1 - Preparación de Datos:
    - Transcripciones de videos → chunks de 1000 tokens
    - Libros de marketing → chunks de 1000 tokens
    - Generar embeddings con OpenAI
    - Almacenar en tabla 'knowledge_base' con pgvector
  
  Fase 2 - Retrieval-Augmented Generation (RAG):
    - Usuario consulta: "Dame 5 ideas de videos para fase de conciencia"
    - Sistema busca en vector store: buyer_persona + customer_journey
    - Sistema busca en knowledge_base: "ideas videos marketing"
    - Sistema inyecta top-10 chunks relevantes en prompt
    - Claude genera respuesta basada en contexto enriquecido
  
  Fase 3 - Fine-tuning Simulado (Long Context):
    - Usar ventana de contexto de 200k tokens de Claude
    - Inyectar transcripciones completas como "system knowledge"
    - Mantener consistencia en respuestas largas

Estructura Backend:
  src/
    api/
      - auth.py (registro, login, recuperar contraseña)
      - chat.py (endpoints de chat + streaming)
      - buyer_persona.py (generación de análisis)
    agents/
      - router_agent.py (orquestador principal)
      - buyer_persona_agent.py (especialista)
      - content_generator_agent.py (creador)
      - memory_manager.py (gestor de memoria)
    db/
      - models.py (SQLAlchemy models)
      - supabase_client.py (conexión)
    services/
      - llm_service.py (wrapper de Claude/OpenAI)
      - embedding_service.py (generación de embeddings)
      - vector_search.py (búsqueda semántica)
    schemas/
      - auth.py (Pydantic schemas)
      - chat.py
      - buyer_persona.py
    utils/
      - validation.py
      - formatting.py
```

### Base de Datos - Supabase

```yaml
Proveedor: Supabase (PostgreSQL + pgvector)
Ubicación: VPS del usuario
Extensiones Requeridas:
  - pgvector (para embeddings)
  - uuid-ossp (para IDs)

Esquema de Tablas (⚠️ PREFIJO: marketing_):

1. marketing_projects (identificador de proyecto):
   - id: UUID PRIMARY KEY
   - name: VARCHAR(255)
   - owner_user_id: UUID REFERENCES marketing_users(id)
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   
   ÍNDICE: owner_user_id
   PROPÓSITO: Aislar datos entre proyectos

2. marketing_users:
   - id: UUID PRIMARY KEY
   - email: VARCHAR UNIQUE NOT NULL
   - password_hash: VARCHAR NOT NULL
   - full_name: VARCHAR
   - project_id: UUID REFERENCES marketing_projects(id)
   - created_at: TIMESTAMP
   - last_login: TIMESTAMP
   
   ÍNDICE: (email, project_id), project_id
   CONSTRAINT: UNIQUE (email, project_id)
   NOTA: Autenticación manual (sin Supabase Auth por restricción de emails)

3. marketing_chats:
   - id: UUID PRIMARY KEY
   - user_id: UUID REFERENCES marketing_users(id)
   - project_id: UUID REFERENCES marketing_projects(id)
   - title: VARCHAR (editable)
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   
   ÍNDICE: (user_id, project_id), created_at DESC
   RLS: WHERE user_id = auth.uid() AND project_id = current_project()

4. marketing_messages:
   - id: UUID PRIMARY KEY
   - chat_id: UUID REFERENCES marketing_chats(id) ON DELETE CASCADE
   - project_id: UUID REFERENCES marketing_projects(id)
   - role: VARCHAR ('user' | 'assistant' | 'system')
   - content: TEXT
   - metadata: JSONB (buyer_persona_step, stage, etc.)
   - created_at: TIMESTAMP
   
   ÍNDICE: (chat_id, created_at), project_id
   RLS: WHERE chat_id IN (SELECT id FROM marketing_chats WHERE user_id = auth.uid())

5. marketing_buyer_personas:
   - id: UUID PRIMARY KEY
   - chat_id: UUID REFERENCES marketing_chats(id)
   - project_id: UUID REFERENCES marketing_projects(id)
   - initial_questions: JSONB (4-5 respuestas del usuario)
   - full_analysis: JSONB (plantilla completa respondida)
   - forum_simulation: JSONB (quejas + soluciones)
   - pain_points: JSONB (array de 10 puntos)
   - customer_journey: JSONB (3 fases × 20 preguntas)
   - created_at: TIMESTAMP
   - embedding: VECTOR(1536) (para búsqueda semántica)
   
   ÍNDICE: chat_id, project_id, embedding (ivfflat)
   RLS: WHERE chat_id IN (SELECT id FROM marketing_chats WHERE user_id = auth.uid())

6. marketing_knowledge_base (material de entrenamiento + documentos del usuario):
   - id: UUID PRIMARY KEY
   - project_id: UUID REFERENCES marketing_projects(id) NULL (NULL = global)
   - chat_id: UUID REFERENCES marketing_chats(id) NULL (NULL = global)
   - content_type: VARCHAR ('video_transcript' | 'book' | 'article' | 'user_document')
   - source_title: VARCHAR
   - chunk_text: TEXT
   - chunk_index: INTEGER
   - metadata: JSONB (autor, fecha, tema, file_type, etc.)
   - embedding: VECTOR(1536)
   - created_at: TIMESTAMP
   
   ÍNDICE: embedding (ivfflat), content_type, project_id, chat_id
   NOTA: 
     - project_id NULL + chat_id NULL = conocimiento global (YouTubers + libros)
     - project_id NOT NULL + chat_id NOT NULL = documentos subidos por usuario

7. marketing_user_documents (metadata de archivos subidos):
   - id: UUID PRIMARY KEY
   - chat_id: UUID REFERENCES marketing_chats(id) ON DELETE CASCADE
   - project_id: UUID REFERENCES marketing_projects(id)
   - user_id: UUID REFERENCES marketing_users(id)
   - filename: VARCHAR
   - file_type: VARCHAR ('.txt' | '.pdf' | '.docx')
   - file_size: INTEGER (bytes)
   - file_path: VARCHAR (ruta en storage)
   - chunks_count: INTEGER (cuántos chunks en marketing_knowledge_base)
   - processed: BOOLEAN DEFAULT FALSE
   - created_at: TIMESTAMP
   
   ÍNDICE: (chat_id, user_id), project_id
   RLS: WHERE user_id = auth.uid() AND project_id = current_project()
   
   PROPÓSITO: Tracking de documentos que usuario ha subido

8. marketing_password_reset_tokens (sin emails, usar link mágico):
   - id: UUID PRIMARY KEY
   - user_id: UUID REFERENCES users(id)
   - project_id: UUID REFERENCES projects(id)
   - token: VARCHAR UNIQUE
   - expires_at: TIMESTAMP
   - used: BOOLEAN DEFAULT FALSE
   
   ÍNDICE: token, (user_id, used)
   EXPIRA: 1 hora

Funciones de Base de Datos:

-- Búsqueda semántica optimizada (incluye documentos del usuario)
CREATE OR REPLACE FUNCTION marketing_match_documents(
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT,
  filter_project_id UUID,
  filter_chat_id UUID DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  content_type VARCHAR,
  source_title VARCHAR,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    kb.id,
    kb.chunk_text,
    kb.content_type,
    kb.source_title,
    1 - (kb.embedding <=> query_embedding) AS similarity
  FROM marketing_knowledge_base kb
  WHERE 
    (
      -- Conocimiento global (YouTubers + libros)
      (kb.project_id IS NULL AND kb.chat_id IS NULL)
      
      OR
      
      -- Documentos del usuario en este chat específico
      (kb.project_id = filter_project_id AND kb.chat_id = filter_chat_id)
    )
    AND 1 - (kb.embedding <=> query_embedding) > match_threshold
  ORDER BY kb.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

### Infraestructura

```yaml
Desarrollo Local:
  - Docker Compose con 3 servicios:
    * frontend: Next.js (puerto 3000)
    * backend: FastAPI (puerto 8000)
    * redis: Cache y queue (puerto 6379)
  - Supabase remoto (VPS del usuario)
  - Volúmenes para persistencia

Producción (Futuro - Portainer en VPS):
  - Misma estructura Docker Compose
  - Nginx reverse proxy
  - SSL con Let's Encrypt
  - Logs centralizados

docker-compose.yml:
  version: '3.8'
  services:
    frontend:
      build: ./frontend
      ports: ["3000:3000"]
      environment:
        - NEXT_PUBLIC_API_URL=http://backend:8000
      depends_on: [backend]
    
    backend:
      build: ./backend
      ports: ["8000:8000"]
      environment:
        - SUPABASE_URL=${SUPABASE_URL}
        - SUPABASE_KEY=${SUPABASE_KEY}
        - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
        - OPENAI_API_KEY=${OPENAI_API_KEY}
      volumes:
        - ./backend/src:/app/src
        - ./training_data:/app/training_data
      depends_on: [redis]
    
    redis:
      image: redis:7-alpine
      ports: ["6379:6379"]
      volumes:
        - redis_data:/data

  volumes:
    redis_data:
```

---

## 🔌 MCPs A UTILIZAR

### 1. MCP Archon (⚡ PRIORITARIO - Documentación)

```yaml
Propósito: Consultar documentación oficial durante todo el desarrollo

Cuándo usar:
  - Desarrollo con Pydantic (modelos, validación)
  - Desarrollo con FastAPI (endpoints, dependency injection)
  - Integración de Python + Next.js
  - Uso de LangChain y agentes
  - Configuración de pgvector en Supabase
  - Implementación de RAG

Flujo de uso:
  1. rag_get_available_sources() → obtener lista
  2. Identificar source_id de: Pydantic, FastAPI, LangChain, Supabase
  3. Por cada duda técnica:
     rag_search_knowledge_base(
       query="keywords específicos",
       source_id="src_xxx",
       match_count=5-10
     )
  4. Para ejemplos de código:
     rag_search_code_examples(
       query="tipo de implementación",
       source_id="src_xxx",
       match_count=3-5
     )

Ejemplo de uso durante desarrollo:
  - "Cómo validar campos anidados en Pydantic v2"
    → rag_search_knowledge_base("nested validation pydantic v2", src_pydantic, 5)
  
  - "Streaming response con FastAPI"
    → rag_search_code_examples("streaming response fastapi", src_fastapi, 3)
  
  - "Implementar agente con memoria en LangChain"
    → rag_search_knowledge_base("agent memory langchain", src_langchain, 10)
```

### 2. MCP Serena (⚡ OBLIGATORIO - Análisis de Código)

```yaml
Propósito: Análisis simbólico de código sin leer archivos completos

Cuándo usar:
  - Antes de modificar código existente
  - Para entender estructura de módulos
  - Para encontrar definiciones de funciones/clases
  - Para ver dónde se usa un símbolo (impacto de cambios)

Comandos clave:
  1. get_symbols_overview('backend/src/agents/')
     → Ver estructura de agentes sin leer archivos
  
  2. find_symbol('BuyerPersonaAgent/generate_analysis', 'agents/buyer_persona_agent.py', True)
     → Leer solo el método específico
  
  3. search_for_pattern('async def.*chat', 'backend/src/')
     → Buscar funciones de chat
  
  4. find_referencing_symbols('ChatService', 'services/chat_service.py')
     → Ver dónde se usa ChatService

CRÍTICO: NUNCA leer archivos completos sin antes usar get_symbols_overview()
```

### 3. MCP Custom del Proyecto (🔧 A CREAR)

```yaml
Nombre: "marketing-brain-mcp"
Propósito: Interfaz para operaciones específicas del sistema

Tools a implementar:

1. analyze_buyer_persona:
   descripción: "Analiza un buyer persona y retorna insights"
   parámetros:
     - chat_id: UUID
     - project_id: UUID
   retorna:
     - pain_points: array
     - opportunities: array
     - content_suggestions: array

2. generate_content_ideas:
   descripción: "Genera ideas de contenido basadas en customer journey"
   parámetros:
     - chat_id: UUID
     - phase: "awareness" | "consideration" | "purchase"
     - content_type: "video" | "post" | "article"
     - count: integer (default 5)
   retorna:
     - ideas: array[{title, description, hook, cta}]

3. search_knowledge_base:
   descripción: "Busca en material de entrenamiento"
   parámetros:
     - query: string
     - content_type: string (opcional)
     - limit: integer (default 10)
   retorna:
     - results: array[{source, text, relevance}]

4. export_strategy_document:
   descripción: "Exporta documento PDF con buyer persona + customer journey"
   parámetros:
     - chat_id: UUID
     - format: "pdf" | "docx"
   retorna:
     - file_url: string

Implementación:
  - Carpeta: /mcp-server/
  - Tecnología: Python + FastMCP
  - Conexión: HTTP a backend FastAPI
  - Skill de referencia: @.cursor/skills/mcp-builder/SKILL.md
```

---

## 📚 SKILLS A UTILIZAR (Por Fase)

### FASE 1: Planificación y Arquitectura

```yaml
Skills:

1. @.cursor/skills/brainstorming/SKILL.md
   Cuándo: Al iniciar el proyecto, antes de codificar
   Por qué: Explorar requisitos y decisiones arquitectónicas
   Activación: Mencionar "nueva feature", "crear proyecto"

2. @.cursor/skills/architecture/SKILL.md
   Cuándo: Decidir estructura de agentes y flujo de datos
   Por qué: Evaluar trade-offs (LangChain vs implementación custom, memoria, etc.)
   Activación: Mencionar "decidir arquitectura", "evaluar opciones"

3. @.cursor/skills/planning-with-files/SKILL.md
   Cuándo: Este proyecto es complejo (>50 tareas estimadas)
   Por qué: Crear task_plan.md, findings.md, progress.md
   Activación: Mencionar "tarea compleja", "proyecto grande"

4. @.cursor/skills/agent-memory-systems/SKILL.md
   Cuándo: Diseñar sistema de memoria del agente
   Por qué: Entender tipos de memoria (short-term, long-term, semantic)
   Invocación: @.cursor/skills/agent-memory-systems/SKILL.md diseñar memoria
```

### FASE 2: Desarrollo Backend (Python + FastAPI)

```yaml
Skills:

1. @.cursor/skills/python-patterns/SKILL.md
   Cuándo: Escribiendo código Python
   Por qué: Mejores prácticas de Python, async patterns, type hints
   Activación automática: Proyecto Python detectado

2. @.cursor/skills/clean-code/SKILL.md
   Cuándo: Durante todo el desarrollo
   Por qué: Código conciso, directo, sin sobre-ingeniería
   Activación automática: Al escribir código

3. @.cursor/skills/agent-tool-builder/SKILL.md
   Cuándo: Creando herramientas (tools) para el agente
   Por qué: JSON Schema correcto, descripciones útiles para LLM
   Invocación: @.cursor/skills/agent-tool-builder/SKILL.md crear tool

4. @.cursor/skills/rag-implementation/SKILL.md
   Cuándo: Implementando búsqueda semántica (RAG)
   Por qué: Chunking, embeddings, vector stores, retrieval optimization
   Invocación: @.cursor/skills/rag-implementation/SKILL.md implementar RAG

5. @.cursor/skills/autonomous-agents/SKILL.md
   Cuándo: Implementando agentes con LangChain
   Por qué: Agent loops (ReAct), goal decomposition, self-correction
   Invocación: @.cursor/skills/autonomous-agents/SKILL.md diseñar agente
```

### FASE 3: Desarrollo Frontend (Next.js 14)

```yaml
Skills:

1. @.cursor/skills/nextjs-best-practices/SKILL.md
   Cuándo: Desarrollando con Next.js
   Por qué: Server Components, data fetching, routing patterns
   Activación automática: Proyecto Next.js detectado

2. @.cursor/skills/react-patterns/SKILL.md
   Cuándo: Creando componentes de UI
   Por qué: Hooks, composition, performance, TypeScript
   Activación automática: Al escribir JSX/TSX

3. @.cursor/skills/tailwind-patterns/SKILL.md
   Cuándo: Estilizando componentes
   Por qué: CSS-first configuration, design tokens
   Activación automática: Proyecto con Tailwind

4. @.cursor/skills/frontend-design/SKILL.md
   Cuándo: Diseñando interfaz de chat y dashboard
   Por qué: UI/UX de calidad, evitar estética genérica de IA
   Invocación: @.cursor/skills/frontend-design/SKILL.md diseñar chat UI
```

### FASE 4: Base de Datos y Autenticación

```yaml
Skills:

1. @.cursor/skills/database-design/SKILL.md
   Cuándo: Diseñando esquema de Supabase
   Por qué: Schema design, indexing strategy, RLS
   Invocación: @.cursor/skills/database-design/SKILL.md diseñar schema

2. @.cursor/skills/postgres-best-practices/SKILL.md
   Cuándo: Optimizando queries y usando pgvector
   Por qué: Performance optimization (Supabase = Postgres)
   Invocación: @.cursor/skills/postgres-best-practices/SKILL.md optimizar queries

3. @.cursor/skills/nextjs-supabase-auth/SKILL.md
   Cuándo: Implementando autenticación
   Por qué: Integración Next.js + Supabase (pero sin Supabase Auth por restricción)
   Nota: Leer skill pero adaptar para autenticación manual
```

### FASE 5: Testing y Validación

```yaml
Skills:

1. @.cursor/skills/test-driven-development/SKILL.md
   Cuándo: Antes de implementar features críticas
   Por qué: RED-GREEN-REFACTOR, escribir tests primero
   Activación: Mencionar "escribir tests primero", "TDD"

2. @.cursor/skills/testing-patterns/SKILL.md
   Cuándo: Escribiendo tests
   Por qué: Jest patterns, factory functions, mocking
   Activación automática: Al escribir tests

3. @.cursor/skills/systematic-debugging/SKILL.md
   Cuándo: Encontrando bugs o comportamiento inesperado
   Por qué: Debugging estructurado antes de proponer fixes
   Activación: Mencionar "bug", "error", "no funciona"
```

### FASE 6: Deployment y Producción

```yaml
Skills:

1. @.cursor/skills/docker-expert/SKILL.md
   Cuándo: Creando Dockerfile y docker-compose
   Por qué: Multi-stage builds, optimización, security
   Invocación: @.cursor/skills/docker-expert/SKILL.md optimizar docker

2. @.cursor/skills/deployment-procedures/SKILL.md
   Cuándo: Preparando deployment a Portainer
   Por qué: Safe deployment workflows, rollback strategies
   Invocación: @.cursor/skills/deployment-procedures/SKILL.md preparar deploy
```

### FASE 7: Creación del MCP Custom

```yaml
Skills:

1. @.cursor/skills/mcp-builder/SKILL.md
   Cuándo: Creando el MCP del proyecto
   Por qué: Guía para crear MCP servers de calidad
   Invocación: @.cursor/skills/mcp-builder/SKILL.md crear MCP marketing-brain
```

---

## 📖 DOCUMENTACIÓN Y RECURSOS

### Ejemplos de Referencia (LEER PRIMERO)

```yaml
Ubicación: /Context-Engineering-Intro/examples/

Propósito: Ejemplos de proyectos similares para entender patrones

Estado: Variable (puede estar vacía o contener múltiples ejemplos)

Cuándo leer:
  - ANTES de diseñar arquitectura
  - ANTES de tomar decisiones técnicas
  - Para entender cómo otros resolvieron problemas similares

Cómo leer:
  Opción A - Con Serena (RECOMENDADO si hay código):
    1. get_symbols_overview('Context-Engineering-Intro/examples/')
    2. Identificar archivos relevantes
    3. find_symbol() para leer partes específicas
  
  Opción B - Lectura directa (si son archivos pequeños):
    1. Listar archivos en carpeta
    2. Leer archivos relevantes
    3. Extraer patrones y decisiones

Qué buscar:
  - Estructura de carpetas
  - Patrones de arquitectura
  - Decisiones técnicas (por qué X en vez de Y)
  - Configuraciones importantes
  - Gotchas y soluciones

IMPORTANTE: Si carpeta está vacía, continuar sin ejemplos
```

### Documentación Oficial (vía Archon MCP)

```yaml
PRIORITARIO - Consultar Archon SIEMPRE antes de web search:

1. Python:
   - source: "Python Official Docs"
   - topics: async/await, type hints, decorators
   - query ejemplo: "python async context manager"

2. Pydantic v2:
   - source: "Pydantic v2 Docs"
   - topics: validation, models, field validators
   - query ejemplo: "pydantic nested model validation"

3. FastAPI:
   - source: "FastAPI Docs"
   - topics: dependency injection, streaming, WebSocket
   - query ejemplo: "fastapi streaming response sse"

4. LangChain:
   - source: "LangChain Docs"
   - topics: agents, memory, tools, chains
   - query ejemplo: "langchain agent with memory"

5. LangGraph:
   - source: "LangGraph Docs"
   - topics: stateful agents, checkpoints, cycles
   - query ejemplo: "langgraph agent with state"

6. Supabase:
   - source: "Supabase Docs"
   - topics: pgvector, RLS, auth, realtime
   - query ejemplo: "supabase pgvector similarity search"

7. Next.js 14:
   - source: "Next.js Docs"
   - topics: App Router, Server Components, streaming
   - query ejemplo: "nextjs 14 server component data fetching"
```

### Material de Entrenamiento del Agente

```yaml
A proporcionar por el usuario:

1. Transcripciones de videos de YouTubers:
   - Formato: .txt o .json
   - Estructura: {title, author, date, transcript}
   - Ubicación: /training_data/videos/
   - Procesamiento: Chunking de 1000 tokens + embeddings

2. Libros de marketing y creación de contenido:
   - Formato: .pdf o .txt
   - Temas: copywriting, content strategy, social media
   - Ubicación: /training_data/books/
   - Procesamiento: Extracción de texto + chunking + embeddings

Proceso de ingesta:
  1. Script: backend/scripts/ingest_training_data.py
  2. Leer archivos de /training_data/
  3. Chunking con RecursiveCharacterTextSplitter (1000 tokens, overlap 200)
  4. Generar embeddings con OpenAI
  5. Almacenar en tabla knowledge_base con project_id NULL (global)
  6. Crear índice ivfflat en columna embedding
```

### Plantillas de Referencia

```yaml
1. Buyer Persona Template:
   - Archivo: @buyer-plantilla.md
   - Secciones: 11 categorías con 35+ preguntas
   - Uso: El agente debe responder TODAS las preguntas
   - Almacenamiento: buyer_personas.full_analysis (JSONB)

2. Preguntas Iniciales (a definir):
   Pregunta 1: "¿Cuál es tu negocio o proyecto?"
   Pregunta 2: "¿Quién es tu cliente ideal? (edad, ocupación, ubicación)"
   Pregunta 3: "¿Qué problema principal resuelves para ellos?"
   Pregunta 4: "¿Qué resultado desean alcanzar tus clientes?"
   Pregunta 5: "¿Tienes competencia directa? ¿Quiénes?"
   
   Almacenamiento: buyer_personas.initial_questions (JSONB)

3. Simulación de Foro:
   - Formato: array de {queja: string, solucion_deseada: string}
   - Cantidad: 5-7 quejas relevantes
   - Almacenamiento: buyer_personas.forum_simulation (JSONB)

4. Puntos de Dolor:
   - Formato: array de strings (10 puntos)
   - Almacenamiento: buyer_personas.pain_points (JSONB)

5. Customer Journey:
   Estructura:
     {
       awareness: {
         questions: ["¿Qué busca en Google?", ...] (20 preguntas),
         mindset: "Descripción de mentalidad",
         content_types: ["blog posts", "videos educativos"]
       },
       consideration: {
         questions: ["¿Qué comparaciones hace?", ...] (20 preguntas),
         mindset: "Descripción de mentalidad",
         content_types: ["comparativas", "demos"]
       },
       purchase: {
         questions: ["¿Qué lo convence de comprar?", ...] (20 preguntas),
         mindset: "Descripción de mentalidad",
         content_types: ["testimonios", "casos de éxito"]
       }
     }
   Almacenamiento: buyer_personas.customer_journey (JSONB)
```

---

## 🚧 FASES DEL PROYECTO

### Fase 0: Configuración Inicial (OBLIGATORIA)

```yaml
Objetivo: Preparar entorno y verificar MCPs

Tareas:
  1. Instalar MCP Serena en Cursor
     - Verificar con: get_symbols_overview('.')
  
  2. Verificar MCP Archon
     - Ejecutar: rag_get_available_sources()
     - Confirmar: Pydantic, FastAPI, LangChain disponibles
  
  3. Crear estructura de proyecto
     - Carpeta: marketing-brain/
     - Subcarpetas: frontend/, backend/, mcp-server/, training_data/
  
  4. Configurar variables de entorno
     - .env.local (frontend)
     - .env (backend)
     - Incluir: SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY

Criterios de aceptación:
  - [ ] Serena funcional
  - [ ] Archon accesible
  - [ ] Estructura de proyecto creada
  - [ ] Variables de entorno configuradas
```

### Fase 1: Base de Datos (Supabase)

```yaml
Objetivo: Configurar Supabase con todas las tablas e índices

Tareas:
  1. Habilitar extensión pgvector
     - SQL: CREATE EXTENSION IF NOT EXISTS vector;
  
  2. Crear todas las 8 tablas con prefijo marketing_:
     - marketing_projects
     - marketing_users
     - marketing_chats
     - marketing_messages
     - marketing_buyer_personas
     - marketing_knowledge_base
     - marketing_user_documents
     - marketing_password_reset_tokens
     - Usar schema detallado de sección "Base de Datos"
     - Incluir todos los índices
     - Configurar RLS (Row Level Security)
  
  3. Crear función marketing_match_documents para búsqueda semántica
     - Función SQL proporcionada en sección anterior
  
  4. Crear proyecto de prueba
     - INSERT INTO marketing_projects VALUES (uuid_generate_v4(), 'Test Project', NULL, NOW(), NOW())

Archivos a crear:
  - backend/db/migrations/001_initial_schema.sql (con prefijo marketing_)
  - backend/db/migrations/002_create_match_function.sql (función marketing_match_documents)
  - backend/db/seed_data.sql (datos de prueba)

Validación:
  - Ejecutar: SELECT * FROM marketing_match_documents('[0.1, 0.2, ...]', 0.7, 10, <project_id>)
  - Debe retornar resultados sin error
```

### Fase 2: Backend - Setup y Autenticación

```yaml
Objetivo: Configurar FastAPI y sistema de autenticación manual

Tareas:
  1. Setup FastAPI con estructura modular
     - Consultar Archon: "fastapi project structure best practices"
  
  2. Configurar SQLAlchemy + Alembic
     - Models para todas las tablas
     - Consultar Archon: "sqlalchemy 2.0 async sessions"
  
  3. Implementar autenticación manual (sin Supabase Auth)
     - POST /api/auth/register
     - POST /api/auth/login (retorna JWT)
     - POST /api/auth/request-password-reset (genera token único)
     - POST /api/auth/reset-password (valida token + cambia contraseña)
     - Middleware de autenticación JWT
  
  4. Gestión de sesiones
     - JWT con expiración de 7 días
     - Refresh token en Redis

Archivos a crear:
  - backend/src/api/auth.py
  - backend/src/schemas/auth.py (Pydantic)
  - backend/src/db/models.py
  - backend/src/middleware/auth.py
  - backend/src/utils/jwt.py
  - backend/src/utils/password.py (bcrypt)

Skills a usar:
  - @.cursor/skills/python-patterns/SKILL.md (automático)
  - @.cursor/skills/clean-code/SKILL.md (automático)

MCPs a consultar:
  - Archon: "pydantic v2 email validator"
  - Archon: "fastapi jwt authentication"
  - Serena: Analizar estructura antes de modificar

Validación (Nivel 1-3):
  - [ ] ruff check backend/src/ --fix
  - [ ] mypy backend/src/
  - [ ] pytest tests/test_auth.py -v
  - [ ] curl -X POST http://localhost:8000/api/auth/register (manual)
```

### Fase 3: Backend - Sistema de Chat Básico

```yaml
Objetivo: CRUD de chats + mensajes (sin IA todavía)

Tareas:
  1. Endpoints de gestión de chats
     - GET /api/chats (listar chats del usuario)
     - POST /api/chats (crear nuevo chat)
     - PATCH /api/chats/{id} (editar título)
     - DELETE /api/chats/{id}
  
  2. Endpoints de mensajes
     - GET /api/chats/{id}/messages (obtener historial)
     - POST /api/chats/{id}/messages (enviar mensaje)
  
  3. Filtrado por project_id
     - Todos los queries deben incluir WHERE project_id = ?
     - Middleware para inyectar project_id desde JWT

Archivos a crear:
  - backend/src/api/chat.py
  - backend/src/schemas/chat.py
  - backend/src/services/chat_service.py

Validación:
  - [ ] Tests con pytest
  - [ ] Verificar aislamiento entre proyectos (crear 2 proyectos de prueba)
```

### Fase 3.5: Backend - Procesamiento de Documentos del Usuario

```yaml
Objetivo: Permitir subida y procesamiento de .txt, .pdf, .docx

Tareas:
  1. Endpoint de subida de documentos
     - POST /api/chats/{id}/upload-document
     - Validar tipo de archivo (.txt, .pdf, .docx)
     - Validar tamaño máximo (10MB)
     - Guardar en storage (local o Supabase Storage)
  
  2. Procesador de documentos
     - Para .txt: Leer directamente
     - Para .pdf: Usar PyPDF2 o pdfplumber
     - Para .docx: Usar python-docx
     - Extraer texto plano
  
  3. Chunking y embedding
     - Dividir documento en chunks de 1000 tokens
     - Generar embeddings con OpenAI
     - Guardar en marketing_knowledge_base con:
       * project_id = usuario.project_id
       * chat_id = chat_id actual
       * content_type = 'user_document'
       * source_title = nombre del archivo
  
  4. Metadata en tabla marketing_user_documents
     - Guardar info del archivo
     - Marcar processed = TRUE al terminar
     - chunks_count = cantidad de chunks generados
  
  5. Endpoint para listar documentos
     - GET /api/chats/{id}/documents
     - Retornar lista con metadata
  
  6. Endpoint para eliminar documento
     - DELETE /api/documents/{id}
     - Eliminar chunks de marketing_knowledge_base
     - Eliminar metadata de marketing_user_documents
     - Eliminar archivo de storage

Archivos a crear:
  - backend/src/api/documents.py
  - backend/src/schemas/documents.py
  - backend/src/services/document_processor.py
  - backend/src/utils/file_parsers.py (txt, pdf, docx)

Skills a usar:
  - @.cursor/skills/python-patterns/SKILL.md (automático)

MCPs a consultar:
  - Archon: "python pdf parsing pypdf2"
  - Archon: "python docx reading"
  - Archon: "langchain text splitter"

Validación:
  - [ ] Subir archivo .txt y verificar chunks en DB
  - [ ] Subir archivo .pdf y verificar extracción de texto
  - [ ] Subir archivo .docx y verificar extracción
  - [ ] Hacer búsqueda semántica y obtener chunks del documento
  - [ ] Eliminar documento y verificar cleanup completo
```

### Fase 4: Backend - Agente IA con Memoria (NÚCLEO)

```yaml
Objetivo: Implementar agente con LangChain/LangGraph + 3 tipos de memoria

IMPORTANTE: Este agente NO genera contenido automáticamente.
            Solo genera cuando el usuario lo solicita explícitamente.

Tareas:
  1. Setup de LLM service
     - Wrapper para Claude 3.5 Sonnet (Anthropic)
     - Configurar streaming
     - Consultar Archon: "langchain anthropic streaming"
  
  2. Implementar 3 tipos de memoria:
     
     a) Short-term (ventana de contexto):
        - ConversationBufferWindowMemory (últimas 10 msgs)
        - Implementar resumen automático cuando >10 msgs
     
     b) Long-term (Supabase):
        - Guardar buyer_persona completo en tabla
        - Guardar customer_journey
        - Recuperar al cargar chat
     
     c) Semantic (pgvector):
        - Embeddings del buyer_persona
        - Embeddings del customer_journey
        - Función de búsqueda: get_relevant_context(query, k=10)
  
  3. Crear agentes especializados:
     
     Agent 1 - Document Processor (NUEVO):
       - Input: Documento subido por usuario
       - Proceso:
         1. Parsear documento (.txt, .pdf, .docx)
         2. Hacer chunking
         3. Generar embeddings
         4. Guardar en marketing_knowledge_base con chat_id
       - Output: Confirmación de procesamiento
     
     Agent 2 - Buyer Persona Specialist:
       - Input: 4-5 respuestas del usuario + documentos subidos (opcional)
       - Proceso:
         1. Cargar plantilla @buyer-plantilla.md
         2. Buscar info en documentos subidos si existen
         3. Responder todas las 35+ preguntas
         4. Guardar en buyer_personas.full_analysis
         5. Generar embedding y guardar
       - Output: JSON completo + documento formateado para el usuario
       - ⏸️ ENTREGA documento y ESPERA a que usuario pida más cosas
     
     Agent 3 - Forum Simulator:
       - Input: buyer_persona.full_analysis
       - Proceso:
         1. Simular persona en foro
         2. Generar 5-7 {queja, solucion_deseada}
         3. Guardar en buyer_personas.forum_simulation
       - Output: JSON de quejas + documento formateado
     
     Agent 4 - Pain Points Extractor:
       - Input: full_analysis + forum_simulation
       - Proceso:
         1. Extraer 10 puntos de dolor
         2. Guardar en buyer_personas.pain_points
       - Output: Lista de 10 puntos + documento formateado
     
     Agent 5 - Customer Journey Creator:
       - Input: full_analysis + pain_points
       - Proceso:
         1. Generar 3 fases (awareness, consideration, purchase)
         2. 20 preguntas por fase sobre búsquedas + mentalidad
         3. Guardar en buyer_personas.customer_journey
       - Output: JSON estructurado + documento formateado
       - ⏸️ ENTREGA documento completo y ESPERA peticiones
     
     Agent 6 - Router/Orchestrator:
       - Decide qué agente ejecutar según:
         * Estado del chat (¿ya tiene buyer persona?)
         * Tipo de petición del usuario
       - Flujo INICIAL: Document Processor → Specialist → Forum → Pain Points → CJ
       - Flujo POSTERIOR: Detecta petición → ejecuta Content Generator
       - CRÍTICO: NO ejecuta Content Generator hasta que usuario lo pida
     
     Agent 7 - Content Generator (ON-DEMAND):
       - ⚠️ SOLO SE EJECUTA cuando usuario hace petición explícita
       - Input: Petición del usuario (ej: "5 ideas de videos para awareness")
       - Proceso:
         1. Buscar buyer_persona del chat (long-term en marketing_buyer_personas)
         2. Buscar customer_journey del chat (long-term en marketing_buyer_personas)
         3. Buscar en documentos subidos del chat (semantic search en marketing_knowledge_base)
         4. Buscar en knowledge base global (YouTubers + libros en marketing_knowledge_base)
         5. Inyectar top-10 chunks relevantes en prompt
         6. Claude genera respuesta personalizada
       - Output: Contenido específico solicitado
       - Ejemplos de peticiones:
         * "Dame 5 ideas de videos para fase de conciencia"
         * "Escribe el script del video sobre [tema]"
         * "Crea 10 posts de Instagram para fase de consideración"
         * "Dame hooks para captar atención en TikTok"
  
  4. Memory Manager
     - Clase: AgentMemoryManager
     - Métodos:
       * get_short_term_context(chat_id) → últimos 10 msgs
       * get_long_term_context(chat_id) → buyer_persona + CJ
       * get_semantic_context(chat_id, query, k) → búsqueda vectorial
       * save_to_long_term(chat_id, data) → persistir en DB

Archivos a crear:
  - backend/src/agents/router_agent.py
  - backend/src/agents/document_processor_agent.py (NUEVO)
  - backend/src/agents/buyer_persona_agent.py
  - backend/src/agents/forum_simulator_agent.py
  - backend/src/agents/pain_points_agent.py
  - backend/src/agents/customer_journey_agent.py
  - backend/src/agents/content_generator_agent.py (on-demand)
  - backend/src/agents/memory_manager.py
  - backend/src/services/llm_service.py
  - backend/src/services/embedding_service.py
  - backend/src/services/vector_search.py

Skills a usar:
  - @.cursor/skills/agent-memory-systems/SKILL.md (diseñar memoria)
  - @.cursor/skills/autonomous-agents/SKILL.md (implementar agentes)
  - @.cursor/skills/rag-implementation/SKILL.md (búsqueda semántica)

MCPs a consultar:
  - Archon: "langchain agent with memory"
  - Archon: "langgraph stateful agent"
  - Archon: "langchain tools custom"

Validación:
  - [ ] Crear chat de prueba
  - [ ] (Opcional) Subir documento con info del negocio
  - [ ] Responder 5 preguntas iniciales
  - [ ] Verificar que se generó buyer_persona completo
  - [ ] Verificar que agente ENTREGÓ documento y ESPERÓ
  - [ ] Verificar que se guardó en DB con embedding
  - [ ] Hacer petición: "Dame 3 ideas de posts"
  - [ ] Verificar que agente buscó en: buyer + CJ + docs subidos + knowledge base
  - [ ] Verificar que respuesta es personalizada al negocio del usuario
```

### Fase 5: Backend - Entrenamiento del Agente (In-Context Learning)

```yaml
Objetivo: Ingerir material de entrenamiento y configurar RAG

Tareas:
  1. Script de ingesta de datos
     - Procesar archivos de /training_data/videos/*.txt
     - Procesar archivos de /training_data/books/*.pdf
     - Chunking: 1000 tokens, overlap 200
     - Generar embeddings con OpenAI
     - Insertar en knowledge_base con project_id NULL
  
  2. Crear índice vectorial optimizado
     - CREATE INDEX ON knowledge_base USING ivfflat (embedding vector_cosine_ops)
     - Configurar lists = n_rows / 1000
  
  3. Implementar búsqueda en knowledge_base
     - Función: search_training_material(query, content_type, k)
     - Usar match_documents de Supabase
  
  4. Integrar en agente de contenido
     - Agent 6 - Content Generator:
       * Input: customer_journey + user_query (ej: "5 ideas de videos fase awareness")
       * Proceso:
         1. Buscar en buyer_persona (contexto del cliente)
         2. Buscar en knowledge_base (técnicas de YouTubers)
         3. Inyectar top-10 chunks en prompt
         4. Claude genera ideas basadas en contexto real
       * Output: Ideas accionables de contenido

Archivos a crear:
  - backend/scripts/ingest_training_data.py
  - backend/src/agents/content_generator_agent.py

Skills a usar:
  - @.cursor/skills/rag-implementation/SKILL.md (chunking, retrieval)

MCPs a consultar:
  - Archon: "langchain document loader pdf"
  - Archon: "langchain text splitter recursive"
  - Archon: "supabase pgvector performance"

Validación:
  - [ ] Ingerir 1 transcripción de prueba
  - [ ] Verificar embedding generado
  - [ ] Hacer búsqueda: "técnicas de hook para videos"
  - [ ] Obtener chunks relevantes
  - [ ] Generar ideas de contenido y verificar calidad
```

### Fase 6: Backend - API de Chat con Streaming

```yaml
Objetivo: Integrar agente con API y streaming de respuestas

Tareas:
  1. Endpoint de chat con streaming
     - POST /api/chats/{id}/stream
     - Server-Sent Events (SSE) para streaming
     - Consultar Archon: "fastapi sse streaming"
  
  2. Orquestación de agentes
     - Router detecta si:
       * Es primer mensaje → ejecutar Agent 1 (preguntas iniciales)
       * Son respuestas a preguntas → ejecutar Agent 1-4 (análisis completo)
       * Es consulta de contenido → ejecutar Agent 6 (generador)
  
  3. Gestión de estado
     - Estado del chat en Redis (qué agentes ya ejecutaron)
     - Persistir resultados en DB
  
  4. Formateo de respuestas
     - JSON estructurado cuando es análisis
     - Markdown cuando es contenido
     - Incluir metadata en mensajes

Archivos a modificar:
  - backend/src/api/chat.py (añadir /stream endpoint)

Validación:
  - [ ] Tests de integración end-to-end
  - [ ] Verificar streaming funciona
  - [ ] Medir latencia (<3s para primera respuesta)
```

### Fase 7: Frontend - Autenticación y Layout

```yaml
Objetivo: Páginas de auth + layout del dashboard

Tareas:
  1. Páginas de autenticación
     - /login (formulario + validación)
     - /register (formulario + validación)
     - /recover-password (solicitar token)
     - /reset-password/[token] (cambiar contraseña)
  
  2. Layout del dashboard
     - Sidebar con lista de chats
     - Área principal de chat
     - Header con usuario + logout
  
  3. Estado global
     - Zustand store para: user, currentChat, chats[]
     - Persistir token en localStorage
  
  4. Protección de rutas
     - Middleware en /dashboard/*
     - Redirect a /login si no autenticado

Componentes a crear:
  - app/(auth)/login/page.tsx
  - app/(auth)/register/page.tsx
  - app/(auth)/recover-password/page.tsx
  - app/(auth)/reset-password/[token]/page.tsx
  - app/dashboard/layout.tsx
  - components/auth/LoginForm.tsx
  - components/auth/RegisterForm.tsx
  - components/dashboard/ChatSidebar.tsx
  - components/dashboard/ChatHeader.tsx
  - stores/authStore.ts
  - stores/chatStore.ts

Skills a usar:
  - @.cursor/skills/nextjs-best-practices/SKILL.md (automático)
  - @.cursor/skills/react-patterns/SKILL.md (automático)
  - @.cursor/skills/frontend-design/SKILL.md (diseño UI)

Validación:
  - [ ] Flujo de registro completo
  - [ ] Flujo de login completo
  - [ ] Flujo de recuperar contraseña
  - [ ] Protección de rutas funciona
  - [ ] UI responsive en mobile y desktop
```

### Fase 8: Frontend - Interfaz de Chat con Streaming

```yaml
Objetivo: Chat funcional con streaming de respuestas del agente

Tareas:
  1. Componente de chat
     - Lista de mensajes con scroll automático
     - Input de texto con envío (Enter)
     - Indicador de "escribiendo..."
     - Formato de mensajes (user vs assistant)
  
  2. Integración con SSE
     - EventSource para recibir streaming
     - Actualizar mensaje del assistant chunk por chunk
     - Manejo de errores de conexión
  
  3. Gestión de chats
     - Crear nuevo chat
     - Listar chats en sidebar
     - Editar título de chat (inline edit)
     - Eliminar chat (con confirmación)
     - Seleccionar chat (cargar mensajes)
  
  4. Visualización de análisis
     - Componente especial para mostrar:
       * Buyer Persona completo (acordeón por sección)
       * Simulación de foro (lista de quejas)
       * Puntos de dolor (lista numerada)
       * Customer Journey (tabs por fase)
     - Botón "Exportar PDF" (llamar a MCP cuando exista)

Componentes a crear:
  - components/chat/ChatInterface.tsx
  - components/chat/MessageList.tsx
  - components/chat/MessageItem.tsx
  - components/chat/ChatInput.tsx
  - components/chat/DocumentUploader.tsx (NUEVO)
  - components/chat/DocumentsList.tsx (NUEVO)
  - components/chat/BuyerPersonaView.tsx
  - components/chat/CustomerJourneyView.tsx
  - components/chat/StreamingIndicator.tsx
  - hooks/useStreamingChat.ts
  - hooks/useChats.ts
  - hooks/useDocuments.ts (NUEVO)

Skills a usar:
  - @.cursor/skills/react-patterns/SKILL.md (hooks, composition)
  - @.cursor/skills/tailwind-patterns/SKILL.md (estilo)

MCPs a consultar:
  - Archon: "nextjs sse event source"
  - Archon: "react streaming updates"

Validación:
  - [ ] Subir documento .txt y ver en lista
  - [ ] Subir documento .pdf y esperar procesamiento
  - [ ] Ver indicador "procesando" mientras se procesa
  - [ ] Eliminar documento y verificar desaparece
  - [ ] Enviar mensaje y recibir respuesta streaming
  - [ ] Crear nuevo chat
  - [ ] Editar título de chat
  - [ ] Eliminar chat
  - [ ] Visualizar buyer persona generado
  - [ ] Pedir ideas de contenido y verificar respuesta personalizada
  - [ ] UI fluida sin lags
```

### Fase 9: MCP Custom del Proyecto

```yaml
Objetivo: Crear MCP "marketing-brain-mcp" con tools específicos

Tareas:
  1. Setup del MCP server
     - Carpeta: /mcp-server/
     - Framework: Python + FastMCP
     - Consultar skill: @.cursor/skills/mcp-builder/SKILL.md
  
  2. Implementar 4 tools:
     - analyze_buyer_persona
     - generate_content_ideas
     - search_knowledge_base
     - export_strategy_document
  
  3. Conectar con backend FastAPI
     - HTTP requests a endpoints
     - Autenticación con API key interna
  
  4. Configurar en Cursor
     - Añadir a settings de MCP
     - Probar invocación desde Cursor

Archivos a crear:
  - mcp-server/server.py
  - mcp-server/tools/analyze_buyer_persona.py
  - mcp-server/tools/generate_content_ideas.py
  - mcp-server/tools/search_knowledge_base.py
  - mcp-server/tools/export_strategy.py
  - mcp-server/README.md

Skills a usar:
  - @.cursor/skills/mcp-builder/SKILL.md (crear MCP)

Validación:
  - [ ] MCP instalado en Cursor
  - [ ] Invocar tool desde Cursor y obtener respuesta
  - [ ] Verificar que tools consultan backend correctamente
```

### Fase 10: Docker y Deployment Local

```yaml
Objetivo: Dockerizar aplicación y probar en local

Tareas:
  1. Dockerfiles
     - frontend/Dockerfile (multi-stage)
     - backend/Dockerfile (multi-stage)
  
  2. docker-compose.yml
     - 3 servicios: frontend, backend, redis
     - Volúmenes para persistencia
     - Networks para comunicación
  
  3. Scripts de deployment
     - scripts/docker-build.sh
     - scripts/docker-up.sh
     - scripts/docker-logs.sh
  
  4. Prueba end-to-end
     - docker-compose up -d
     - Acceder a http://localhost:3000
     - Probar flujo completo

Skills a usar:
  - @.cursor/skills/docker-expert/SKILL.md (optimizar Dockerfiles)

Validación:
  - [ ] docker-compose up exitoso
  - [ ] Frontend accesible en puerto 3000
  - [ ] Backend responde en puerto 8000
  - [ ] Redis funcional
  - [ ] Volúmenes persisten datos
  - [ ] Logs sin errores críticos
```

### Fase 11: Testing End-to-End y Documentación

```yaml
Objetivo: Tests completos y documentación del proyecto

Tareas:
  1. Tests backend
     - Tests unitarios (pytest)
     - Tests de integración (API)
     - Coverage >80%
  
  2. Tests frontend
     - Tests de componentes (Jest + React Testing Library)
     - Tests e2e (Playwright)
  
  3. Documentación
     - README.md del proyecto
     - API documentation (OpenAPI/Swagger)
     - Guía de deployment
     - Guía de uso del MCP

Archivos a crear:
  - README.md
  - docs/API.md
  - docs/DEPLOYMENT.md
  - docs/MCP_GUIDE.md

Skills a usar:
  - @.cursor/skills/test-driven-development/SKILL.md
  - @.cursor/skills/testing-patterns/SKILL.md

Validación:
  - [ ] pytest tests/ -v --cov (>80% coverage)
  - [ ] npm test (frontend tests passing)
  - [ ] playwright test (e2e tests passing)
  - [ ] Documentación completa y clara
```

---

## ⚠️ CONSIDERACIONES TÉCNICAS CRÍTICAS

### 🚫 PROHIBICIONES ABSOLUTAS

```yaml
1. HARDCODEAR DATOS:
   ❌ NUNCA: const API_URL = "http://localhost:8000"
   ✅ SIEMPRE: const API_URL = process.env.NEXT_PUBLIC_API_URL
   
   ❌ NUNCA: project_id = "123e4567-e89b-12d3-a456-426614174000"
   ✅ SIEMPRE: project_id = user.project_id (desde JWT/DB)

2. LEER ARCHIVOS COMPLETOS SIN SERENA:
   ❌ NUNCA: Abrir archivo y leer todo
   ✅ SIEMPRE: get_symbols_overview() primero

3. BUSCAR EN WEB SIN CONSULTAR ARCHON:
   ❌ NUNCA: Buscar "fastapi streaming" en Google
   ✅ SIEMPRE: rag_search_knowledge_base("fastapi streaming", src_fastapi, 5)

4. MEZCLAR DATOS ENTRE PROYECTOS:
   ❌ NUNCA: SELECT * FROM chats WHERE user_id = ?
   ✅ SIEMPRE: SELECT * FROM chats WHERE user_id = ? AND project_id = ?
```

### 🔐 Seguridad

```yaml
1. Autenticación:
   - JWT con HS256 (clave secreta en .env)
   - Password hashing con bcrypt (cost factor 12)
   - Rate limiting en endpoints de auth (5 intentos/minuto)
   - CORS configurado solo para frontend origin

2. Upload de Archivos:
   - Validar MIME type (no solo extensión)
   - Escanear archivos con antivirus si es posible
   - Límite de tamaño: 10MB por archivo
   - Sanitizar nombres de archivo
   - Almacenar fuera de webroot
   - No ejecutar archivos subidos

3. Base de Datos:
   - Row Level Security (RLS) habilitado
   - Prepared statements (SQLAlchemy previene SQL injection)
   - Índices en columnas filtradas (project_id, user_id)

4. API Keys:
   - ANTHROPIC_API_KEY: Nunca exponer al frontend
   - OPENAI_API_KEY: Solo en backend
   - SUPABASE_KEY: Service role key (nunca anon key)

5. Validación de Input:
   - Pydantic en TODOS los endpoints
   - Sanitizar input antes de embeddings
   - Límite de 5000 caracteres por mensaje
```

### ⚡ Performance

```yaml
1. Base de Datos:
   - Usar índices ivfflat para pgvector (búsquedas <50ms)
   - Connection pooling: min=5, max=20
   - Lazy loading para relaciones grandes

2. LLM:
   - Streaming obligatorio (no esperar respuesta completa)
   - Timeout de 30s por request
   - Cache de embeddings en Redis (TTL 1 hora)
   - Batch de embeddings (procesar 50 chunks a la vez)

3. Frontend:
   - Lazy load de chats (paginación de 20)
   - Virtual scrolling en lista de mensajes (react-window)
   - Code splitting por ruta
   - Imágenes optimizadas con next/image

4. Docker:
   - Multi-stage builds (reducir tamaño de imagen)
   - .dockerignore (excluir node_modules, .git, etc.)
   - Health checks en docker-compose
```

### 🐛 Gotchas y Trampas Comunes

```yaml
1. Supabase pgvector:
   GOTCHA: "ivfflat index requiere >1000 rows para ser efectivo"
   SOLUCIÓN: Usar al menos 1000 chunks en knowledge_base, o usar hnsw index

2. LangChain Memory:
   GOTCHA: "ConversationBufferMemory crece indefinidamente"
   SOLUCIÓN: Usar ConversationBufferWindowMemory con k=10 + resumen

3. Next.js 14 Server Components:
   GOTCHA: "No puedes usar useState en Server Components"
   SOLUCIÓN: Marcar 'use client' en componentes interactivos

4. FastAPI Streaming:
   GOTCHA: "StreamingResponse no funciona con middlewares que leen body"
   SOLUCIÓN: Excluir /stream endpoints de body-reading middleware

5. Docker Volumes en Windows:
   GOTCHA: "Permisos incorrectos en volúmenes montados"
   SOLUCIÓN: Usar named volumes en vez de bind mounts

6. Embeddings de OpenAI:
   GOTCHA: "Rate limit de 3000 RPM en tier free"
   SOLUCIÓN: Batch de embeddings + retry con exponential backoff

7. JWT en Next.js:
   GOTCHA: "localStorage no accesible en Server Components"
   SOLUCIÓN: Usar cookies httpOnly para JWT, leer en middleware

8. Supabase RLS:
   GOTCHA: "RLS policies no aplican con service role key"
   SOLUCIÓN: Validar project_id manualmente en backend

9. LangChain Tools:
   GOTCHA: "Descripciones vagas causan que LLM use tool incorrecto"
   SOLUCIÓN: Descripciones específicas con ejemplos en docstring

10. pgvector Cosine Distance:
    GOTCHA: "1 - cosine_distance no es similarity score 0-1"
    SOLUCIÓN: Normalizar embeddings antes de insertar
```

### 📊 Monitoreo y Logs

```yaml
1. Backend:
   - Logging estructurado con loguru
   - Niveles: DEBUG (dev), INFO (prod)
   - Logs incluyen: request_id, user_id, project_id, timestamp

2. Frontend:
   - Sentry para errores en producción
   - Console logs solo en desarrollo
   - Analytics de uso (opcional)

3. Docker:
   - Logs centralizados con docker-compose logs
   - Rotación de logs (max-size: 10m, max-file: 3)

4. Métricas:
   - Tiempo de respuesta de LLM
   - Tokens consumidos por request
   - Latencia de búsqueda vectorial
   - Tasa de error por endpoint
```

---

## 🎯 CRITERIOS DE ÉXITO DEL PROYECTO

```yaml
Funcionalidad:
  - [ ] Usuario puede registrarse, login, recuperar contraseña
  - [ ] Usuario puede crear/editar/eliminar chats
  - [ ] Usuario puede subir documentos (.txt, .pdf, .docx)
  - [ ] Usuario puede eliminar documentos subidos
  - [ ] Agente responde 4-5 preguntas iniciales
  - [ ] Agente procesa documentos subidos y extrae información
  - [ ] Agente genera buyer persona completo (35+ preguntas)
  - [ ] Agente simula foro y extrae 10 puntos de dolor
  - [ ] Agente genera customer journey (3 fases × 20 preguntas)
  - [ ] Agente ENTREGA análisis completo y ESPERA peticiones
  - [ ] Sistema recuerda contexto (memoria funcional + docs subidos)
  - [ ] Usuario puede pedir ideas de contenido específicas
  - [ ] Agente genera contenido SOLO cuando se le pide
  - [ ] Agente usa: buyer + CJ + docs subidos + entrenamiento
  - [ ] Streaming de respuestas funcional (<3s primera palabra)
  - [ ] Datos aislados por project_id (sin mezcla entre proyectos)

Calidad:
  - [ ] Código sin hardcoding de datos
  - [ ] Tests con >80% coverage
  - [ ] Sin errores de linting (ruff, mypy)
  - [ ] Sin errores de tipos (TypeScript)
  - [ ] Documentación completa
  - [ ] Docker funcionando en local

Performance:
  - [ ] Búsqueda vectorial <100ms
  - [ ] Streaming LLM <3s primera respuesta
  - [ ] Frontend carga <2s (Lighthouse >90)
  - [ ] API responde <200ms (endpoints simples)

Seguridad:
  - [ ] JWT implementado correctamente
  - [ ] Passwords hasheados con bcrypt
  - [ ] RLS habilitado en Supabase
  - [ ] API keys no expuestas
  - [ ] Validación de input en todos los endpoints
```

---

## 🚀 PRÓXIMOS PASOS (Post-MVP)

```yaml
Deployment a VPS con Portainer:
  - Configurar Portainer en VPS
  - Subir docker-compose.yml
  - Configurar Nginx reverse proxy
  - Habilitar SSL con Let's Encrypt
  - Configurar dominio

Features Adicionales:
  - Exportar PDF de análisis (tool del MCP)
  - Compartir chats con otros usuarios
  - Templates de contenido predefinidos
  - Análisis de competencia automatizado
  - Calendario de contenido sugerido
  - Integración con redes sociales (auto-publicar)

Optimizaciones:
  - Cache de análisis frecuentes
  - Fine-tuning de modelo (si presupuesto lo permite)
  - Mejora de prompts basada en feedback
  - A/B testing de diferentes estrategias de agente
```

---

## 📝 NOTAS FINALES

```yaml
Filosofía del Proyecto:
  1. "Context is king": Memoria y RAG son críticos para calidad
  2. "Streaming always": Nunca bloquear esperando respuesta completa
  3. "Isolation matters": project_id en TODAS las queries
  4. "No hardcoding": Todo desde DB o env vars
  5. "Serena first": Análisis simbólico antes de leer archivos
  6. "Archon priority": Documentación oficial siempre primero

Stack Justification:
  - Next.js 14: SSR + streaming, App Router moderno
  - FastAPI: Async nativo, Pydantic integrado, rápido
  - Pydantic: Validación robusta, tipos claros
  - LangChain: Ecosystem maduro para agentes
  - Supabase: Postgres + pgvector en un solo lugar
  - Claude 3.5: Mejor para tareas complejas, context largo
  - Docker: Reproducibilidad, fácil deployment

Tiempo Estimado:
  - Setup inicial: 1-2 días
  - Backend (Fases 1-6): 10-15 días
  - Frontend (Fases 7-8): 5-7 días
  - MCP + Testing (Fases 9-11): 3-5 días
  - TOTAL: 19-29 días (desarrollo intensivo)
  - REALISTA: 4-6 semanas (con contingencias)

Costos Estimados (Mensual):
  - Anthropic API (Claude): $50-200 (según uso)
  - OpenAI API (embeddings): $20-50
  - Supabase (si hosted): $0-25 (tier gratuito hasta límite)
  - VPS (Portainer): $10-20
  - TOTAL: ~$100-300/mes

Prioridades de Desarrollo:
  1. Base de datos + autenticación (fundación)
  2. Agente con memoria (núcleo del valor)
  3. Chat con streaming (experiencia)
  4. Entrenamiento del agente (diferenciación)
  5. Frontend pulido (usabilidad)
  6. MCP + deployment (productización)
```

---

**🎯 Con este INITIAL.md detallado, estamos listos para generar el PRP completo usando `generate-prp-v3-es.md`**

**El PRP resultante tendrá:**
- ✅ Estructura de 11 fases bien definidas
- ✅ Skills integradas por fase
- ✅ MCPs con comandos específicos
- ✅ Consideraciones técnicas detalladas
- ✅ Validación en 3 niveles por tarea
- ✅ Todo lo necesario para implementación exitosa

**Este documento es 10x más completo que el INITIAL.md de ejemplo, incluyendo arquitectura técnica, decisiones de stack, gotchas, y todo el flujo del agente con memoria.**
