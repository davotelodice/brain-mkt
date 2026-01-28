name: "Marketing Second Brain System - PRP v3"
version: "3.0-ES"
descripcion: |
  Sistema web full-stack de segundo cerebro para estrategia de marketing digital.
  Incluye agente IA con memoria persistente (short-term, long-term, semantic),
  generación de buyer personas, simulación de comportamiento, customer journey,
  y creación de contenido on-demand basado en entrenamiento con YouTubers + libros.

---

## 🎯 Objetivo

Construir un sistema web completo ("Marketing Second Brain") que funcione como asistente IA para estrategia de marketing digital, con las siguientes capacidades principales:

1. **Análisis Profundo de Buyer Persona**: Cuestionario inicial + plantilla completa de 35+ preguntas
2. **Simulación de Comportamiento**: Buyer persona actuando en foro de internet (quejas + soluciones)
3. **Customer Journey Detallado**: 3 fases de conciencia con 20 preguntas cada una
4. **Ingesta de Documentos**: Usuario sube archivos (.txt, .pdf, .docx) con info de su negocio
5. **Generación de Contenido On-Demand**: Posts, videos, scripts SOLO cuando usuario lo solicita
6. **Sistema de Memoria Triple**: Short-term (ventana), Long-term (DB), Semantic (vector store)
7. **Entrenamiento Contextual**: RAG con transcripciones de YouTubers + libros de marketing

**Estado Final Deseado:**
- Frontend (Next.js 14) con interfaz de chat responsive y moderna
- Backend (FastAPI + Python) con agente IA usando LangChain/LangGraph
- Base de datos (Supabase + pgvector) con aislamiento por `project_id`
- Sistema de autenticación manual (sin Supabase Auth por restricción)
- Docker Compose para desarrollo local
- Documentos procesados y embeddings generados
- Agente que ENTREGA análisis completo y ESPERA peticiones del usuario
- Tests con >80% coverage

---

## 💡 Por Qué

### Valor de Negocio
- **Diferenciación**: No es un chatbot genérico - está entrenado específicamente en creación de contenido
- **Contexto Persistente**: Recuerda buyer persona, puntos de dolor, customer journey, y documentos del usuario
- **Salida Accionable**: Genera contenido listo para usar, no solo teoría
- **ROI Claro**: Ahorra horas de investigación y redacción de contenido

### Impacto en el Usuario
- Estrategia de marketing personalizada en minutos
- Ideas de contenido basadas en comportamiento real del público objetivo
- Capacidad de incorporar info del negocio mediante documentos
- Generación de contenido bajo demanda (no automática, controlada por usuario)

### Integración
- Primera versión standalone, futuro: integración con redes sociales
- Fundamento para features adicionales: calendario de contenido, análisis de competencia

### Problemas que Resuelve
- **Para marketers**: Falta de insights profundos sobre su audiencia
- **Para creadores de contenido**: No saber qué contenido crear para cada fase del customer journey
- **Para emprendedores**: Dificultad para crear estrategia de contenido consistente
- **Para consultores**: Necesidad de herramienta para acelerar análisis de clientes

---

## 📋 Qué

### Comportamiento Visible para el Usuario

#### FASE 1 - ANÁLISIS INICIAL (Automático):
1. Usuario se registra / inicia sesión
2. Usuario crea nuevo chat desde dashboard
3. Agente hace 4-5 preguntas iniciales sobre el negocio
4. **[NUEVO]** Usuario OPCIONALMENTE sube documentos (.txt, .pdf, .docx) con info del negocio
5. **[NUEVO]** Agente procesa documentos y extrae información relevante
6. Agente completa Buyer Persona automáticamente (plantilla de 35+ preguntas)
7. Agente simula persona en foro (quejas + soluciones propuestas)
8. Agente extrae 10 puntos de dolor principales
9. Agente genera Customer Journey (3 fases × 20 preguntas cada una)
10. Agente ENTREGA documento completo al usuario (formato markdown estructurado)
11. Agente GUARDA todo en memoria (3 tipos: short-term, long-term, semantic + docs)
12. ⏸️ **AGENTE ESPERA PETICIONES DEL USUARIO** (no genera contenido automáticamente)

> ✅ **Estado actual (enero 2026, ya implementado / verificado):**
> - **Tarea 9 (Customer Journey)**: ya existe en `backend/src/agents/buyer_persona_agent.py` (`BuyerPersonaAgent/_generate_customer_journey`) y se persiste en DB como `buyer_persona.customer_journey`. En UI se visualiza en `frontend/app/components/AnalysisPanel.tsx` (bloque “Ver customer journey (JSON)”).  
>   - **Nota de coherencia**: hoy generamos \(por fase\) **10 `busquedas` + 10 `preguntas_cabeza`** (=20 items). Si la intención del PRP era “20 preguntas *solo* en `preguntas_cabeza`”, hay que aclararlo aquí para no “romper” lo que ya funciona.
> - **Tarea 10 (Documento completo en Markdown)**: **no está implementada** como “export/entrega de documento completo”. Actualmente se muestran JSONs (buyer persona/foro/dolor/journey) en el panel de análisis, pero no hay “documento markdown estructurado” descargable/compartible.
> - **Tarea 11 (Guardar todo en memoria)**: ya está **parcialmente cumplida**:
>   - **Long-term**: buyer persona + foro + pain points + customer journey quedan en DB (modelo `BuyerPersona`).
>   - **Short-term**: conversación reciente se mantiene (buffer) y se persiste en mensajes (DB).
>   - **Semantic + docs**: RAG funciona y se usa en generación; documentos del usuario entran al retrieval; además existe “training summary” inyectado en prompt (con trazabilidad).
>   - **Pendiente recomendado (sin romper nada)**: cuando se implemente Tarea 10, guardar también ese **Markdown final** como documento “snapshot” (para recuperación semántica y auditoría).

#### FASE 2 - GENERACIÓN DE CONTENIDO (On-Demand):
1. Usuario pide contenido específico (ej: "Dame 5 ideas de videos para fase de conciencia")
2. Agente consulta:
   - Buyer persona del chat actual (long-term)
   - Customer journey del chat actual (long-term)
   - Documentos subidos por el usuario (semantic search)
   - Knowledge base global (YouTubers + libros, semantic search)
   - Conversación reciente (short-term)
3. Agente GENERA respuesta personalizada basada en contexto completo
4. Usuario recibe ideas accionables
5. Usuario puede pedir refinamientos o scripts completos
6. Ciclo continúa según peticiones

### Requisitos Técnicos

#### Frontend (Next.js 14 + TypeScript + TailwindCSS + shadcn/ui):
- App Router con Server Components
- Páginas de autenticación: login, register, recover-password, reset-password/[token]
- Dashboard con sidebar de chats + área principal de chat
- Interfaz de chat con streaming de respuestas (SSE)
- **[NUEVO]** Componente de subida de documentos (drag & drop o selector)
- **[NUEVO]** Lista de documentos subidos con estado de procesamiento
- Visualización especial para buyer persona, forum simulation, customer journey
- Estado global con Zustand (user, currentChat, chats[], documents[])
- Protección de rutas con middleware
- Responsive (mobile + desktop)

#### Backend (FastAPI + Python 3.11+):
- Estructura modular: api/, agents/, db/, services/, schemas/, utils/
- Autenticación manual con JWT (sin Supabase Auth)
- Recuperación de contraseña con tokens únicos (sin emails, link mágico)
- CRUD de chats y mensajes
- **[NUEVO]** Upload de documentos con validación (.txt, .pdf, .docx, max 10MB)
- **[NUEVO]** Procesamiento de documentos (parsers para cada formato)
- **[NUEVO]** Chunking y embedding de documentos subidos
- Sistema de agentes con LangChain/LangGraph:
  - **Router Agent**: Orquestador principal
  - **Document Processor Agent**: Procesa archivos subidos (**NUEVO**)
  - **Buyer Persona Specialist**: Genera análisis completo + busca en docs
  - **Forum Simulator**: Simula comportamiento en foro
  - **Pain Points Extractor**: Extrae 10 puntos principales
  - **Customer Journey Creator**: 3 fases × 20 preguntas
  - **Content Generator**: SOLO cuando usuario lo solicita
  - **Memory Manager**: Gestiona 3 tipos de memoria
- Streaming de respuestas con Server-Sent Events (SSE)
- Sistema de memoria triple (short/long/semantic)
- RAG con embeddings de OpenAI
- Búsqueda vectorial con pgvector

#### Base de Datos (Supabase + PostgreSQL + pgvector):
- **8 tablas** con prefijo `marketing_`:
  1. `marketing_projects` (identificador de proyecto)
  2. `marketing_users` (autenticación manual, NO Supabase Auth)
  3. `marketing_chats` (conversaciones con RLS)
  4. `marketing_messages` (historial con metadata)
  5. `marketing_buyer_personas` (análisis completo + embeddings)
  6. `marketing_knowledge_base` (entrenamiento global + **docs de usuario**)
  7. **`marketing_user_documents`** (metadata de archivos subidos) **[NUEVO]**
  8. `marketing_password_reset_tokens` (recuperación sin email)
- Extensión pgvector para embeddings (VECTOR(1536))
- Función `marketing_match_documents` para búsqueda semántica
- Row Level Security (RLS) configurado
- Índices ivfflat para búsqueda vectorial rápida
- **CRÍTICO**: Aislamiento total por `project_id` (sin mezcla entre proyectos)

#### Infraestructura (Docker + Docker Compose):
- 3 servicios: frontend (puerto 3000), backend (puerto 8000), redis (puerto 6379)
- Volúmenes para persistencia de datos
- Supabase remoto (VPS del usuario)
- Variables de entorno desde .env
- Scripts de deployment: docker-build.sh, docker-up.sh

### Criterios de Éxito

**Funcionalidad:**
- [ ] Usuario puede registrarse, login, recuperar contraseña
- [ ] Usuario puede crear/editar/eliminar chats
- [ ] Usuario puede subir documentos (.txt, .pdf, .docx) en un chat
- [ ] Usuario puede ver lista de documentos subidos con estado de procesamiento
- [ ] Usuario puede eliminar documentos subidos
- [ ] Agente responde 4-5 preguntas iniciales
- [ ] Agente procesa documentos subidos y extrae información
- [ ] Agente genera buyer persona completo (35+ preguntas) usando docs si existen
- [ ] Agente simula foro y extrae 10 puntos de dolor
- [ ] Agente genera customer journey (3 fases × 20 preguntas)
- [ ] Agente ENTREGA análisis y ESPERA peticiones
- [ ] Sistema recuerda contexto (memoria funcional + documentos subidos)
- [ ] Usuario puede pedir ideas de contenido específicas
- [ ] Agente genera contenido SOLO cuando se le pide
- [ ] Agente usa: buyer + CJ + docs subidos + entrenamiento global
- [ ] Streaming de respuestas funcional (<3s primera palabra)
- [ ] Datos aislados por `project_id` (sin mezcla entre proyectos)

**Calidad:**
- [ ] Código sin hardcoding de datos
- [ ] Tests con >80% coverage
- [ ] Sin errores de linting (ruff, mypy)
- [ ] Sin errores de tipos (TypeScript)
- [ ] Documentación completa (README, API docs)
- [ ] Docker funcionando en local

**Performance:**
- [ ] Búsqueda vectorial <100ms
- [ ] Streaming LLM <3s primera respuesta
- [ ] Frontend carga <2s (Lighthouse >90)
- [ ] API responde <200ms (endpoints simples)

**Seguridad:**
- [ ] JWT implementado correctamente
- [ ] Passwords hasheados con bcrypt
- [ ] RLS habilitado en Supabase
- [ ] API keys no expuestas
- [ ] Validación de input en todos los endpoints
- [ ] Archivos subidos validados (tipo MIME, tamaño, sanitización de nombres)

---

## 🧰 Skills del Proyecto a Utilizar

### 📝 FASE DE PLANIFICACIÓN

**Skill: planning-with-files**
- **Cuándo**: Este proyecto es complejo (11 fases, ~30+ tareas)
- **Por qué**: Crear task_plan.md, findings.md y progress.md para seguimiento estructurado
- **Activación**: Comenzar FASE 0 antes de cualquier implementación

**Skill: brainstorming**
- **Cuándo**: ANTES de implementar cada feature crítica (agentes, memoria, auth)
- **Por qué**: Explorar requisitos y decisiones arquitectónicas
- **Crítico**: OBLIGATORIO antes de implementar agentes IA

**Skill: architecture**
- **Cuándo**: Decidir estructura de agentes y flujo de datos entre ellos
- **Por qué**: Evaluar trade-offs (LangChain vs custom, tipo de memoria, embedding strategy)
- **Aplicación**: FASE 4 (Agente IA con Memoria)

**Skill: agent-memory-systems**
- **Cuándo**: Diseñar sistema de memoria del agente (3 tipos)
- **Por qué**: Entender patrones de short-term, long-term y semantic memory
- **Aplicación**: FASE 4 (implementación de memoria)

**Skill: rag-implementation**
- **Cuándo**: Implementando búsqueda semántica y entrenamiento del agente
- **Por qué**: Chunking, embeddings, vector stores, retrieval optimization
- **Aplicación**: FASE 5 (entrenamiento) y FASE 3.5 (documentos de usuario)

### 💻 FASE DE DESARROLLO

**MCP: Serena** ⚡ CRÍTICO - INSTALAR PRIMERO
- **Cuándo**: TAREA 0 - Primera acción en todo proyecto
- **Por qué**: Análisis simbólico de código, ediciones quirúrgicas
- **Herramientas principales**:
  - `get_symbols_overview`: Ver estructura sin leer archivos completos
  - `find_symbol`: Buscar símbolos específicos
  - `search_for_pattern`: Búsqueda rápida cuando ubicación desconocida
  - `replace_symbol_body`: Edición quirúrgica de funciones/clases
- **Aplicación**: TODAS las fases de desarrollo

**Skill: clean-code**
- **Cuándo**: Escribiendo o revisando código (siempre)
- **Por qué**: Código conciso, directo, sin sobre-ingeniería
- **Aplicación**: Backend + Frontend

**Skill: python-patterns**
- **Cuándo**: Desarrollando backend en Python
- **Por qué**: Async patterns, type hints, estructura modular
- **Aplicación**: FASES 2-6 (backend)

**Skill: react-patterns**
- **Cuándo**: Desarrollando componentes de UI
- **Por qué**: Hooks, composition, performance, TypeScript best practices
- **Aplicación**: FASES 7-8 (frontend)

**Skill: nextjs-best-practices**
- **Cuándo**: Trabajando con Next.js App Router
- **Por qué**: Server Components, data fetching, routing patterns
- **Aplicación**: FASES 7-8 (frontend)

**Skill: autonomous-agents**
- **Cuándo**: Implementando agentes con LangChain/LangGraph
- **Por qué**: Agent loops (ReAct), goal decomposition, self-correction
- **Aplicación**: FASE 4 (núcleo del sistema)

### 📚 FASE DE DOCUMENTACIÓN

**MCP: Archon** 🎯 PRIORIDAD MÁXIMA
- **Cuándo**: SIEMPRE - Consultar ANTES que URLs externas
- **Por qué**: Base de datos RAG con documentación oficial verificada
- **Documentación disponible**:
  - Python (varios libros + PEPs)
  - Pydantic v2 (docs completas + ejemplos) - source_id: `9d46e91458092424`
  - FastAPI (tutorial + API reference) - source_id: `c889b62860c33a44`
  - LangChain + LangGraph - source_id: `e74f94bb9dcb14aa`
  - Supabase (docs + pgvector) - source_id: `9c5f534e51ee9237`
  - Next.js 14 - source_id: `77b8a4a07d5230b5`
  - React - source_id: `a931698c21fb8f24`
  - TypeScript - source_id: `d7c76d077e634ab3`
  - shadcn/ui - source_id: `bf102fe8a697ed7c`
- **Herramientas**:
  - `rag_get_available_sources()`: Listar todas las fuentes
  - `rag_search_knowledge_base(query, source_id, match_count)`: Buscar docs
  - `rag_search_code_examples(query, source_id, match_count)`: Buscar ejemplos

**Skill: documentation-templates**
- **Cuándo**: Crear README.md, API.md, DEPLOYMENT.md
- **Por qué**: Templates estructurados para documentación clara
- **Aplicación**: FASE 11 (documentación final)

### 🧪 FASE DE TESTING

**Skill: test-driven-development**
- **Cuándo**: ANTES de implementar features críticas (agentes, auth, memoria)
- **Por qué**: Tests primero aseguran calidad desde el inicio
- **Aplicación**: FASES 2-6 (backend)

**Skill: testing-patterns**
- **Cuándo**: Escribiendo tests unitarios y de integración
- **Por qué**: Jest patterns, factory functions, mocking strategies
- **Aplicación**: FASE 11 (testing completo)

### ✅ FASE DE VALIDACIÓN

**Skill: lint-and-validate**
- **Cuándo**: Después de CADA modificación de código
- **Por qué**: QA automático, linting, análisis estático
- **Aplicación**: TODAS las fases (validación continua)

**Skill: verification-before-completion**
- **Cuándo**: Antes de declarar completitud de cada tarea
- **Por qué**: Requiere evidencia ejecutable de comandos
- **Aplicación**: Final de cada tarea

**Skill: systematic-debugging**
- **Cuándo**: Bugs, test failures, comportamiento inesperado
- **Por qué**: Análisis sistemático ANTES de proponer fixes
- **Aplicación**: Cuando aparezcan errores

### 🚀 FASE DE DEPLOYMENT

**Skill: docker-expert**
- **Cuándo**: Creando Dockerfile y docker-compose.yml
- **Por qué**: Multi-stage builds, optimización, seguridad
- **Aplicación**: FASE 10 (Docker y deployment local)

**Skill: deployment-procedures**
- **Cuándo**: Preparando deployment a Portainer (futuro)
- **Por qué**: Safe deployment workflows, rollback strategies
- **Aplicación**: Post-MVP (deployment a VPS)

---

## 🔌 Guía de MCPs

### MCP Archon 🎯 (USAR SIEMPRE PRIMERO)

**Contexto del Proyecto:**
Este proyecto usa tecnologías con documentación completa en Archon:
- Backend: FastAPI + Pydantic v2 + LangChain/LangGraph
- Frontend: Next.js 14 + React + TypeScript + shadcn/ui
- Database: Supabase + pgvector
- Python: Async patterns, type hints, decorators

**Flujo de trabajo estándar:**

```yaml
Paso 1 - Listar fuentes disponibles (PRIMERO):
  comando: rag_get_available_sources()
  resultado: |
    Lista completa con source_id de cada documentación:
    - Pydantic v2: 9d46e91458092424
    - FastAPI: c889b62860c33a44
    - LangChain: e74f94bb9dcb14aa
    - Supabase: 9c5f534e51ee9237
    - Next.js 14: 77b8a4a07d5230b5
    - React: a931698c21fb8f24
    - TypeScript: d7c76d077e634ab3
    - shadcn/ui: bf102fe8a697ed7c

Paso 2 - Buscar documentación específica:
  comando: |
    rag_search_knowledge_base(
        query="keywords cortos 2-5 palabras",
        source_id="src_xxx",
        match_count=5
    )
  ejemplos_buenos:
    - "pydantic nested model validation"
    - "fastapi streaming response sse"
    - "langchain agent memory conversation"
    - "supabase pgvector similarity search"
    - "nextjs 14 server component"
  ejemplos_malos:
    - "cómo implementar validación de modelos anidados en Pydantic v2"
    - "crear respuesta de streaming con FastAPI usando Server-Sent Events"

Paso 3 - Buscar ejemplos de código:
  comando: |
    rag_search_code_examples(
        query="pydantic validator custom",
        source_id="9d46e91458092424",
        match_count=3
    )
  cuándo: "Después de entender conceptos, necesitas ver implementaciones"
```

**Queries Recomendadas por Fase:**

```yaml
FASE 1 (Base de Datos):
  - query: "supabase pgvector create index"
    source_id: "9c5f534e51ee9237"
  - query: "postgres vector similarity search"
    source_id: "9c5f534e51ee9237"

FASE 2 (Backend Setup):
  - query: "fastapi project structure async"
    source_id: "c889b62860c33a44"
  - query: "pydantic v2 model validation"
    source_id: "9d46e91458092424"

FASE 3.5 (Upload de Documentos):
  - query: "fastapi file upload validation"
    source_id: "c889b62860c33a44"
  - query: "python pdf parsing text extraction"
    (buscar en libros de Python disponibles)

FASE 4 (Agente IA con Memoria):
  - query: "langchain agent memory conversation"
    source_id: "e74f94bb9dcb14aa"
  - query: "langgraph stateful agent"
    source_id: "e74f94bb9dcb14aa"
  - query: "langchain tools custom"
    source_id: "e74f94bb9dcb14aa"

FASE 5 (Entrenamiento RAG):
  - query: "langchain document loader pdf"
    source_id: "e74f94bb9dcb14aa"
  - query: "langchain text splitter recursive"
    source_id: "e74f94bb9dcb14aa"

FASE 6 (API Streaming):
  - query: "fastapi sse streaming"
    source_id: "c889b62860c33a44"
  - query: "fastapi server sent events"
    source_id: "c889b62860c33a44"

FASE 7 (Frontend Auth):
  - query: "nextjs 14 middleware authentication"
    source_id: "77b8a4a07d5230b5"
  - query: "react zustand persist"
    source_id: "a931698c21fb8f24"

FASE 8 (Frontend Chat):
  - query: "nextjs sse event source"
    source_id: "77b8a4a07d5230b5"
  - query: "react streaming updates"
    source_id: "a931698c21fb8f24"
```

### MCP Serena ⚡ (INSTALAR PRIMERO)

**Filosofía de Uso:**
- ❌ **PROHIBIDO**: Leer archivos completos sin razón
- ✅ **OBLIGATORIO**: `get_symbols_overview` ANTES de leer
- ✅ **PREFERIDO**: `find_symbol` para símbolos específicos
- ✅ **RECOMENDADO**: Ediciones simbólicas (`replace_symbol_body`)

**Herramientas Principales y Cuándo Usar:**

```yaml
get_symbols_overview(relative_path):
  propósito: "Ver estructura de archivos sin leer contenido completo"
  cuándo_usar:
    - Antes de modificar cualquier archivo existente
    - Para entender organización de un módulo
    - Para decidir dónde añadir código nuevo
  ejemplo: |
    get_symbols_overview('backend/src/agents/')
    # Retorna: lista de clases, funciones, métodos (sin bodies)

find_symbol(name_path, relative_path, include_body):
  propósito: "Buscar y leer símbolo específico (clase, función, método)"
  cuándo_usar:
    - Sabes el nombre del símbolo que necesitas modificar
    - Quieres leer implementación específica
  ejemplos: |
    # Leer método específico de clase
    find_symbol('BuyerPersonaAgent/generate_analysis', 
                'backend/src/agents/buyer_persona_agent.py', 
                include_body=True)
    
    # Ver estructura de clase sin bodies
    find_symbol('ChatService', 
                'backend/src/services/chat_service.py', 
                include_body=False)

search_for_pattern(pattern, relative_path):
  propósito: "Búsqueda rápida cuando no sabes ubicación exacta"
  cuándo_usar:
    - Buscas un patrón de código en el proyecto
    - No estás seguro en qué archivo está
  ejemplo: |
    search_for_pattern('async def.*authenticate', 'backend/src/')
    # Encuentra todas las funciones async con 'authenticate'

find_referencing_symbols(name_path, relative_path):
  propósito: "Ver dónde se usa un símbolo (impacto de cambios)"
  cuándo_usar:
    - Antes de modificar una función/clase
    - Para entender dependencias
  ejemplo: |
    find_referencing_symbols('UserModel', 'backend/src/db/models.py')
    # Retorna snippets de código donde se referencia UserModel

replace_symbol_body(name_path, relative_path, new_body):
  propósito: "Reemplazar implementación completa de función/clase"
  cuándo_usar:
    - Cambios grandes en un símbolo específico
    - Refactoring de método completo
  ejemplo: |
    replace_symbol_body(
        'ChatService/create_chat',
        'backend/src/services/chat_service.py',
        'async def create_chat(self, user_id, title): ...'
    )
```

**Patrones de Uso Comunes:**

```yaml
PATRÓN 1 - Modificar archivo existente:
  paso_1: get_symbols_overview('path/to/file.py')
  paso_2: "Identificar símbolo a modificar"
  paso_3: find_symbol('Class/method', 'path/to/file.py', True)
  paso_4: "Analizar implementación"
  paso_5: replace_symbol_body(...) o edición manual

PATRÓN 2 - Añadir código nuevo:
  paso_1: get_symbols_overview('path/to/file.py')
  paso_2: "Ver último símbolo del archivo"
  paso_3: "Usar insert_after_symbol para añadir nueva función/clase"

PATRÓN 3 - Entender dependencias:
  paso_1: find_symbol('ClassName', 'path/to/file.py', False)
  paso_2: find_referencing_symbols('ClassName', 'path/to/file.py')
  paso_3: "Analizar impacto de cambios propuestos"

PATRÓN 4 - Buscar implementación desconocida:
  paso_1: search_for_pattern('async def process_document', 'backend/')
  paso_2: "Identificar archivo correcto en resultados"
  paso_3: get_symbols_overview('archivo_encontrado.py')
  paso_4: find_symbol(...) para leer implementación
```

**Integración con INITIAL.md:**

El INITIAL.md menciona estos patrones existentes que deberías buscar:
- Patrón de agentes con dependencies (ver ejemplos)
- Patrón de tools con decoradores
- Patrón de Pydantic models con Field descriptions
- Patrón de endpoints FastAPI con dependency injection

Usar Serena para encontrarlos:
```bash
search_for_pattern('@research_agent.tool', 'Context-Engineering-Intro/examples/')
search_for_pattern('class.*BaseModel', 'Context-Engineering-Intro/examples/')
```

---

## 📦 Todo el Contexto Necesario

### Documentación & Referencias

**Prioridad de Consulta:**

```yaml
NIVEL 1 - MCP Archon (PRIORITARIO):
  acción: |
    # 1. Obtener fuentes disponibles
    rag_get_available_sources()
    
    # 2. Identificar source_id relevante
    # Ejemplo para FastAPI:
    source_id = "c889b62860c33a44"
    
    # 3. Buscar documentación específica
    rag_search_knowledge_base(
        query="fastapi streaming response",
        source_id="c889b62860c33a44",
        match_count=5
    )
  
  fuentes_disponibles:
    pydantic: "9d46e91458092424"
    fastapi: "c889b62860c33a44"
    langchain: "e74f94bb9dcb14aa"
    supabase: "9c5f534e51ee9237"
    nextjs: "77b8a4a07d5230b5"
    react: "a931698c21fb8f24"
    typescript: "d7c76d077e634ab3"
    shadcn_ui: "bf102fe8a697ed7c"
  
  por_qué: "Documentación oficial verificada y actualizada"

NIVEL 2 - Ejemplos del Proyecto con Serena:
  ubicación: "Context-Engineering-Intro/examples/"
  
  ejemplos_relevantes:
    - main_agent_reference/:
        - research_agent.py: "Patrón de agente con pydantic-ai y tools"
        - models.py: "Modelos Pydantic con Field descriptions"
        - providers.py: "Configuración de LLM models"
    
    - mcp-server/:
        - src/index.ts: "MCP server con auth"
        - src/tools/: "Tool registration pattern"
        - CLAUDE.md: "Estándares de implementación"
  
  acción: |
    # Ver estructura de ejemplo
    get_symbols_overview('Context-Engineering-Intro/examples/main_agent_reference/research_agent.py')
    
    # Leer patrón específico
    find_symbol('research_agent', 'Context-Engineering-Intro/examples/main_agent_reference/research_agent.py', True)
  
  por_qué: "Patrones probados del proyecto específico"

NIVEL 3 - Archivos del Proyecto (cuando existan):
  acción: |
    # ANTES de modificar cualquier archivo:
    get_symbols_overview('backend/src/agents/buyer_persona_agent.py')
    
    # Leer símbolo específico:
    find_symbol('BuyerPersonaAgent/generate', 'backend/src/agents/buyer_persona_agent.py', True)
    
    # Ver referencias:
    find_referencing_symbols('BuyerPersonaAgent', 'backend/src/agents/buyer_persona_agent.py')
  
  por_qué: "Entender código existente sin leer archivos completos"

NIVEL 4 - URLs Externos (ÚLTIMO RECURSO):
  cuándo_usar: "Solo si Archon no tiene la información"
  
  ejemplos_válidos:
    - url: "https://docs.anthropic.com/claude/reference"
      por_qué: "API específica de Claude 3.5 Sonnet"
      sección: "Streaming responses"
    
    - url: "https://python.langchain.com/docs/modules/agents/agent_types/"
      por_qué: "Tipos de agentes específicos no cubiertos en Archon"
      sección: "ReAct agent pattern"
  
  nota: "Archon tiene cobertura completa de Python, Pydantic, FastAPI, LangChain, Supabase, Next.js"
```

### Insights de Ejemplos de Referencia

**Patrón 1: Agentes con Dependencies (de `research_agent.py`):**

```python
# PATRÓN: Usar @dataclass para dependencies
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class ResearchAgentDependencies:
    """Dependencies - solo configuración, no instancias de tools"""
    brave_api_key: str
    gmail_credentials_path: str
    session_id: Optional[str] = None

# PATRÓN: Inicializar agente con deps_type
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)

# PATRÓN: Tools reciben contexto con dependencies
@research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    # Acceder a dependencies via ctx.deps
    api_key = ctx.deps.brave_api_key
    results = await search_web_tool(api_key=api_key, query=query)
    return results
```

**Aplicación al Proyecto:**
- Usar patrón similar para BuyerPersonaAgent, ContentGeneratorAgent
- Dependencies incluirán: supabase_url, anthropic_api_key, project_id
- Tools accederán a DB y LLM via dependencies

**Patrón 2: Modelos Pydantic con Validación (de `models.py`):**

```python
# PATRÓN: Usar Field para descripciones detalladas
from pydantic import BaseModel, Field
from typing import List, Optional

class ResearchQuery(BaseModel):
    """Model for research query requests."""
    query: str = Field(..., description="Research topic to investigate")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results")
    include_summary: bool = Field(True, description="Whether to include AI summary")

class BraveSearchResult(BaseModel):
    """Model for individual search results."""
    title: str = Field(..., description="Title of result")
    url: str = Field(..., description="URL of result")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Example Result",
                "url": "https://example.com",
                "score": 0.95
            }
        }
```

**Aplicación al Proyecto:**
- Crear schemas Pydantic para: BuyerPersona, CustomerJourney, ContentIdea, UserDocument
- Incluir Field descriptions detalladas (ayuda al LLM)
- Añadir ejemplos en Config (documentación automática)

**Patrón 3: MCP Tool Registration (de `mcp-server/`):**

```typescript
// PATRÓN: Registro centralizado de tools
// src/tools/register-tools.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // Registro por dominio/feature
  registerDatabaseTools(server, env, props);
  registerAnalyticsTools(server, env, props);
  // ... más tools
}

// PATRÓN: Cada feature tiene su propio módulo de tools
// examples/database-tools.ts
export function registerDatabaseTools(server: McpServer, env: Env, props: Props) {
  // Tool disponible para todos
  server.tool("listTables", "Get all tables", ListTablesSchema, async () => {
    // Implementation
  });
  
  // Tool solo para usuarios privilegiados
  if (ALLOWED_USERNAMES.has(props.login)) {
    server.tool("executeDatabase", "Execute SQL", ExecuteSchema, async ({ sql }) => {
      // Implementation
    });
  }
}
```

**Aplicación al Proyecto:**
- Crear MCP custom para el proyecto (FASE 9)
- Tools: analyze_buyer_persona, generate_content_ideas, search_knowledge_base
- Implementar permisos por usuario si necesario

### Árbol del Codebase Actual

```bash
# Estado inicial del proyecto (a crear)
/home/david/brain-mkt/
├── README.md (TO CREATE)
├── .gitignore (TO CREATE)
├── docker-compose.yml (TO CREATE)
│
├── frontend/ (TO CREATE)
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── .env.local
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   ├── recover-password/page.tsx
│   │   │   └── reset-password/[token]/page.tsx
│   │   ├── dashboard/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── api/
│   │       ├── chat/route.ts
│   │       └── auth/route.ts
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── DocumentUploader.tsx (NEW)
│   │   │   ├── DocumentsList.tsx (NEW)
│   │   │   └── BuyerPersonaView.tsx
│   │   └── dashboard/
│   │       ├── ChatSidebar.tsx
│   │       └── ChatHeader.tsx
│   └── stores/
│       ├── authStore.ts
│       └── chatStore.ts
│
├── backend/ (TO CREATE)
│   ├── pyproject.toml
│   ├── .env
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── buyer_persona.py
│   │   │   └── documents.py (NEW)
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── router_agent.py
│   │   │   ├── document_processor_agent.py (NEW)
│   │   │   ├── buyer_persona_agent.py
│   │   │   ├── forum_simulator_agent.py
│   │   │   ├── pain_points_agent.py
│   │   │   ├── customer_journey_agent.py
│   │   │   ├── content_generator_agent.py
│   │   │   └── memory_manager.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── supabase_client.py
│   │   │   └── migrations/
│   │   │       ├── 001_initial_schema.sql
│   │   │       └── 002_create_match_function.sql
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_search.py
│   │   │   ├── document_processor.py (NEW)
│   │   │   └── chat_service.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── buyer_persona.py
│   │   │   └── documents.py (NEW)
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validation.py
│   │       ├── formatting.py
│   │       ├── jwt.py
│   │       ├── password.py
│   │       └── file_parsers.py (NEW - txt, pdf, docx)
│   ├── scripts/
│   │   └── ingest_training_data.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_chat.py
│       ├── test_agents.py
│       ├── test_documents.py (NEW)
│       └── fixtures/
│
├── mcp-server/ (TO CREATE - FASE 9)
│   ├── server.py
│   ├── tools/
│   │   ├── analyze_buyer_persona.py
│   │   ├── generate_content_ideas.py
│   │   ├── search_knowledge_base.py
│   │   └── export_strategy.py
│   └── README.md
│
├── training_data/ (TO PROVIDE BY USER)
│   ├── videos/ (transcripciones .txt)
│   └── books/ (libros .pdf)
│
└── Context-Engineering-Intro/ (EXISTING)
    ├── examples/ (reference patterns)
    ├── PRPs/ (este archivo)
    └── validation/
```

### Árbol del Codebase Deseado (Post-Implementación)

```bash
# Estado final esperado (todas las fases completadas)
/home/david/brain-mkt/
├── README.md ✅
├── docker-compose.yml ✅
├── .dockerignore ✅
├── .gitignore ✅
│
├── frontend/ ✅ (3000 puerto)
│   ├── Dockerfile ✅
│   ├── [todos los archivos de estructura inicial] ✅
│   └── [componentes completamente funcionales] ✅
│
├── backend/ ✅ (8000 puerto)
│   ├── Dockerfile ✅
│   ├── [todos los archivos de estructura inicial] ✅
│   ├── [agentes implementados y funcionando] ✅
│   ├── [tests >80% coverage] ✅
│   └── storage/ (archivos subidos por usuarios)
│       └── documents/ (organizados por project_id/chat_id/)
│
├── mcp-server/ ✅
│   ├── [MCP funcional con 4 tools] ✅
│   └── [documentación de uso] ✅
│
├── training_data/ ✅
│   ├── videos/ (con archivos .txt proporcionados)
│   └── books/ (con archivos .pdf proporcionados)
│
├── docs/ ✅
│   ├── API.md ✅
│   ├── DEPLOYMENT.md ✅
│   └── MCP_GUIDE.md ✅
│
└── scripts/
    ├── docker-build.sh ✅
    ├── docker-up.sh ✅
    └── docker-logs.sh ✅
```

### Gotchas Conocidos y Críticos

**🔴 NIVEL CRÍTICO - Pueden romper el sistema:**

```python
# GOTCHA 1: Supabase pgvector requiere >1000 rows para índice ivfflat
# Problema: Índice ivfflat no es efectivo con <1000 documentos
# Solución: Usar hnsw index o asegurar >1000 chunks en knowledge_base
CREATE INDEX ON marketing_knowledge_base 
USING hnsw (embedding vector_cosine_ops); -- Mejor para pocos documentos

# GOTCHA 2: LangChain ConversationBufferMemory crece indefinidamente
# Problema: Memoria crece sin límite, consume tokens
# Solución: Usar ConversationBufferWindowMemory con k=10
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=10, return_messages=True)

# GOTCHA 3: FastAPI StreamingResponse + middleware que lee body
# ⚠️ INTEGRADO EN: TAREA 6 - API de Chat con Streaming (cuando se detalle)
# Problema: Middleware que lee request body rompe streaming
# Solución: Excluir /stream endpoints del middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # ✅ Detectar endpoints de streaming ANTES de leer body
    if "/stream" in request.url.path or "/sse" in request.url.path:
        return await call_next(request)  # Skip middleware
    
    # Para endpoints normales, procesar como siempre
    body = await request.body()
    # ... resto del middleware

# GOTCHA 4: Next.js Server Components + useState
# ⚠️ INTEGRADO EN: TAREA 8 - Frontend Chat Interface (cuando se detalle)
# Problema: No puedes usar useState en Server Components
# Solución: Marcar componentes interactivos con 'use client'
'use client'  // ✅ Al inicio del archivo
import { useState } from 'react'

# Patrón recomendado:
# - app/page.tsx → Server Component (fetch datos, layout)
# - app/components/ChatInterface.tsx → 'use client' (useState, eventos)

# GOTCHA 5: Embeddings de OpenAI rate limit (3000 RPM en tier free)
# Problema: Al procesar muchos chunks, se alcanza límite
# Solución: Batch de embeddings + retry con exponential backoff
async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    batch_size = 50
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = await openai.Embedding.create(input=batch, model="text-embedding-3-large")
            results.extend([e['embedding'] for e in response['data']])
        except RateLimitError:
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
            retry_count += 1
    return results

# GOTCHA 6: Supabase RLS no aplica con service role key
# Problema: Service role key bypasea RLS policies
# Solución: Validar project_id manualmente en backend
async def get_chats(user_id: UUID, project_id: UUID):
    # Validar project_id manualmente, no confiar solo en RLS
    user = await db.users.find_one({'id': user_id})
    if user.project_id != project_id:
        raise PermissionError("User not in this project")
    return await db.chats.find({'user_id': user_id, 'project_id': project_id})

# GOTCHA 7: LangChain Tools - Descripciones vagas causan mal uso
# Problema: LLM usa tool incorrecto si descripción es vaga
# Solución: Descripciones específicas con ejemplos en docstring
@agent.tool
async def generate_content_ideas(
    ctx: RunContext,
    phase: str,
    content_type: str,
    count: int = 5
) -> List[Dict]:
    """
    Generate content ideas for a specific customer journey phase.
    
    Use this tool when user explicitly asks for content ideas.
    Examples: "Dame 5 ideas de videos", "Crea ideas de posts"
    
    Args:
        phase: One of: "awareness", "consideration", "purchase"
        content_type: One of: "video", "post", "article"
        count: Number of ideas to generate (default 5)
    
    DO NOT use this tool for analyzing buyer persona or creating customer journey.
    """
    ...

# GOTCHA 8: Docker volumes en Windows - Permisos incorrectos
# Problema: Bind mounts tienen permisos raros en Windows
# Solución: Usar named volumes en vez de bind mounts
# BAD:
volumes:
  - ./backend:/app  # Bind mount - problemas en Windows
# GOOD:
volumes:
  - backend_data:/app  # Named volume - funciona en todos lados

# GOTCHA 9: pgvector cosine distance no es similarity 0-1
# Problema: 1 - cosine_distance no devuelve score normalizado
# Solución: Normalizar embeddings antes de insertar
def normalize_embedding(embedding: List[float]) -> List[float]:
    norm = np.linalg.norm(embedding)
    return [x / norm for x in embedding]

# GOTCHA 10: JWT en localStorage + Server Components
# ⚠️ INTEGRADO EN: TAREA 7 - Frontend Auth + TAREA 8 - Chat Interface (cuando se detallen)
# Problema: localStorage no accesible en Server Components de Next.js
# Solución: Usar cookies httpOnly y leer en middleware
// ❌ NO HACER: localStorage.setItem('token', jwt)
// ✅ HACER: cookies httpOnly

// Backend: Setear cookie en response de /login
response.set_cookie(
    key="auth_token",
    value=jwt_token,
    httponly=True,  # ← No accesible desde JavaScript
    secure=True,  # Solo HTTPS en production
    samesite="lax",
    max_age=604800  # 7 días
)

// Frontend: middleware.ts lee cookie automáticamente
export async function middleware(request: NextRequest) {
    const token = request.cookies.get('auth_token')?.value
    if (!token) {
        return NextResponse.redirect(new URL('/login', request.url))
    }
    // Validar JWT antes de permitir acceso
    // ...
}
```

**🟡 NIVEL ADVERTENCIA - Pueden causar problemas de performance:**

```python
# WARNING 1: No usar .all() en queries grandes
# BAD:
all_messages = await db.messages.find().all()  # Puede ser millones
# GOOD:
messages = await db.messages.find({'chat_id': chat_id}).limit(100).all()

# WARNING 2: No generar embeddings síncronamente
# BAD:
for chunk in chunks:
    embedding = openai.Embedding.create(input=chunk['text'])  # Síncrono
# GOOD:
embeddings = await generate_embeddings_batch([c['text'] for c in chunks])

# WARNING 3: No hacer queries N+1 en loops
# BAD:
for chat_id in chat_ids:
    messages = await db.messages.find({'chat_id': chat_id})  # N queries
# GOOD:
messages = await db.messages.find({'chat_id': {'$in': chat_ids}})  # 1 query

# WARNING 4: No procesar archivos grandes en memoria
# BAD:
content = file.read()  # Todo el archivo en RAM
# GOOD:
async for chunk in file.stream():
    await process_chunk(chunk)  # Stream processing
```

### Validación de Restricciones Críticas

```yaml
RESTRICCIÓN 1: Supabase Auth NO disponible
  razón: "Limitación en correos electrónicos"
  solución: "Implementar autenticación manual con JWT"
  impacto:
    - Crear tabla marketing_users con password_hash
    - Implementar endpoints de auth manualmente
    - Usar bcrypt para passwords
    - JWT para sesiones
  validación: |
    # Verificar que NO se use Supabase Auth
    grep -r "supabase.auth" backend/src/
    # Esperado: Sin resultados

RESTRICCIÓN 2: Aislamiento total por project_id
  razón: "Multi-tenancy estricto"
  solución: "Incluir project_id en TODAS las queries"
  impacto:
    - WHERE project_id = ? en TODAS las queries
    - RLS policies con project_id
    - Middleware para inyectar project_id desde JWT
  validación: |
    # Verificar que todas las queries incluyen project_id
    grep -r "SELECT.*FROM marketing_" backend/src/ | grep -v "project_id"
    # Esperado: Sin resultados (todas incluyen project_id)

RESTRICCIÓN 3: Agente NO genera automáticamente
  razón: "Usuario controla cuándo generar contenido"
  solución: "Content Generator solo se ejecuta con petición explícita"
  impacto:
    - Router agent detecta petición de contenido
    - Content Generator NO se ejecuta en análisis inicial
    - Usuario debe pedir explícitamente
  validación: |
    # Verificar que Content Generator no se ejecuta automáticamente
    grep -A10 "class RouterAgent" backend/src/agents/router_agent.py
    # Debe haber lógica de detección de petición de contenido

RESTRICCIÓN 4: Upload máximo 10MB por archivo
  razón: "Evitar sobrecarga de servidor y procesamiento lento"
  solución: "Validar tamaño antes de aceptar archivo"
  impacto:
    - Validación en frontend (pre-upload)
    - Validación en backend (endpoint)
  validación: |
    # Verificar límite en backend
    grep "MAX_FILE_SIZE" backend/src/api/documents.py
    # Esperado: MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

---

## 🏗️ Blueprint de Implementación

### Modelos de Datos y Estructura

#### SQLAlchemy Models (backend/src/db/models.py):

```python
from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class MarketingProject(Base):
    __tablename__ = 'marketing_projects'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id'), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class MarketingUser(Base):
    __tablename__ = 'marketing_users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_login = Column(TIMESTAMP)
    
    # ÍNDICE COMPUESTO: (email, project_id)
    # CONSTRAINT: UNIQUE (email, project_id)

class MarketingChat(Base):
    __tablename__ = 'marketing_chats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    title = Column(String(255), default="New Chat", nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # ÍNDICE: (user_id, project_id), created_at DESC
    # RLS: WHERE user_id = auth.uid() AND project_id = current_project()

class MarketingMessage(Base):
    __tablename__ = 'marketing_messages'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    metadata = Column(JSONB, default={})
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # ÍNDICE: (chat_id, created_at), project_id

class MarketingBuyerPersona(Base):
    __tablename__ = 'marketing_buyer_personas'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    initial_questions = Column(JSONB, nullable=False)  # 4-5 respuestas
    full_analysis = Column(JSONB, nullable=False)  # 35+ preguntas
    forum_simulation = Column(JSONB, nullable=False)  # Array de {queja, solucion}
    pain_points = Column(JSONB, nullable=False)  # Array de strings (10 puntos)
    customer_journey = Column(JSONB, nullable=False)  # {awareness, consideration, purchase}
    embedding = Column(Vector(1536))  # Embedding del análisis completo
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # ÍNDICE: chat_id, project_id, embedding (ivfflat o hnsw)

class MarketingKnowledgeBase(Base):
    __tablename__ = 'marketing_knowledge_base'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=True)  # NULL = global
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id'), nullable=True)  # NULL = global
    content_type = Column(String(50), nullable=False)  # 'video_transcript' | 'book' | 'user_document'
    source_title = Column(String(500), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    metadata = Column(JSONB, default={})
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # ÍNDICE: embedding (ivfflat o hnsw), content_type, project_id, chat_id
    # NOTA:
    #  - project_id NULL + chat_id NULL = conocimiento global (YouTubers + libros)
    #  - project_id NOT NULL + chat_id NOT NULL = documentos subidos por usuario

class MarketingUserDocument(Base):
    __tablename__ = 'marketing_user_documents'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('marketing_chats.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id'), nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(10), nullable=False)  # '.txt' | '.pdf' | '.docx'
    file_size = Column(Integer, nullable=False)  # bytes
    file_path = Column(String(1000), nullable=False)  # ruta en storage
    chunks_count = Column(Integer, default=0, nullable=False)
    processed = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # ÍNDICE: (chat_id, user_id), project_id
    # PROPÓSITO: Tracking de documentos subidos por el usuario

class MarketingPasswordResetToken(Base):
    __tablename__ = 'marketing_password_reset_tokens'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('marketing_users.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('marketing_projects.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    
    # ÍNDICE: token, (user_id, used)
    # EXPIRA: 1 hora
```

#### Pydantic Schemas (backend/src/schemas/):

**auth.py:**
```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from uuid import UUID

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    full_name: Optional[str] = Field(None, description="User full name")
    project_id: UUID = Field(..., description="Project to join")
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    project_id: UUID

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict  # {id, email, full_name, project_id}

class RequestPasswordResetRequest(BaseModel):
    email: EmailStr
    project_id: UUID

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
```

**chat.py:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class CreateChatRequest(BaseModel):
    title: Optional[str] = Field("New Chat", description="Chat title")

class CreateChatResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime

class SendMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)

class Message(BaseModel):
    id: UUID
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    metadata: Dict[str, Any] = {}
    created_at: datetime

class ChatSummary(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = None
```

**documents.py (NUEVO):**
```python
from pydantic import BaseModel, Field, field_validator
from typing import List
from uuid import UUID
from datetime import datetime

class UploadDocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    file_size: int
    processed: bool = False
    created_at: datetime

class DocumentMetadata(BaseModel):
    id: UUID
    filename: str
    file_type: str
    file_size: int
    chunks_count: int
    processed: bool
    created_at: datetime

class ListDocumentsResponse(BaseModel):
    documents: List[DocumentMetadata]
    total: int

# Validación de archivo
ALLOWED_FILE_TYPES = {'.txt', '.pdf', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@field_validator('file_type')
def validate_file_type(cls, v):
    if v not in ALLOWED_FILE_TYPES:
        raise ValueError(f'File type must be one of {ALLOWED_FILE_TYPES}')
    return v
```

**buyer_persona.py:**
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from uuid import UUID

class InitialQuestions(BaseModel):
    q1_business: str
    q2_ideal_customer: str
    q3_main_problem: str
    q4_desired_outcome: str
    q5_competition: str

class ForumSimulation(BaseModel):
    complaint: str
    desired_solution: str

class CustomerJourneyPhase(BaseModel):
    questions: List[str] = Field(..., min_items=20, max_items=20)
    mindset: str
    content_types: List[str]

class CustomerJourney(BaseModel):
    awareness: CustomerJourneyPhase
    consideration: CustomerJourneyPhase
    purchase: CustomerJourneyPhase

class BuyerPersonaAnalysis(BaseModel):
    initial_questions: InitialQuestions
    full_analysis: Dict[str, Any]  # 35+ preguntas estructuradas
    forum_simulation: List[ForumSimulation]
    pain_points: List[str] = Field(..., min_items=10, max_items=10)
    customer_journey: CustomerJourney
```

#### Arquitectura de Agentes (LangChain + LangGraph):

```python
# backend/src/agents/router_agent.py
from langchain.agents import Agent
from langchain.memory import ConversationBufferWindowMemory
from enum import Enum

class AgentState(str, Enum):
    INITIAL = "initial"
    DOCUMENT_PROCESSING = "document_processing"
    BUYER_PERSONA = "buyer_persona"
    FORUM_SIMULATION = "forum_simulation"
    PAIN_POINTS = "pain_points"
    CUSTOMER_JOURNEY = "customer_journey"
    WAITING = "waiting"
    CONTENT_GENERATION = "content_generation"

class RouterAgent:
    """
    Orquestador principal que decide qué agente ejecutar.
    
    Flujo:
    1. Detecta estado del chat (¿ya tiene buyer persona?)
    2. Detecta tipo de petición del usuario
    3. Ejecuta agente correspondiente
    
    CRÍTICO: Content Generator SOLO se ejecuta con petición explícita
    """
    def __init__(self, memory_manager, llm_service):
        self.memory_manager = memory_manager
        self.llm = llm_service
        self.memory = ConversationBufferWindowMemory(k=10)
    
    async def route(self, chat_id: UUID, user_message: str) -> AgentState:
        # 1. Obtener contexto del chat
        chat_context = await self.memory_manager.get_long_term_context(chat_id)
        
        # 2. Decidir estado
        if not chat_context.get('buyer_persona'):
            if not chat_context.get('documents_uploaded'):
                return AgentState.BUYER_PERSONA
            else:
                return AgentState.DOCUMENT_PROCESSING
        
        # 3. Detectar petición de contenido
        if self._is_content_request(user_message):
            return AgentState.CONTENT_GENERATION
        
        # 4. Por defecto, esperar
        return AgentState.WAITING
    
    def _is_content_request(self, message: str) -> bool:
        """
        Detecta si usuario solicita generación de contenido.
        
        Keywords: dame, genera, crea, escribe, ideas, posts, videos, scripts
        """
        keywords = ['dame', 'genera', 'crea', 'escribe', 'ideas', 'posts', 'videos', 'scripts']
        return any(kw in message.lower() for kw in keywords)
```

---

## 🎯 Recursos Clave del Proyecto (¡CRÍTICOS!)

**Estos 3 recursos son la BASE de conocimiento que hace único a este sistema:**

### RECURSO 1: Plantilla de Buyer Persona 📋

```yaml
Ubicación: contenido/buyer-plantilla.md

Propósito:
  "Estructura base completa que el agente DEBE seguir al crear análisis de buyer persona"

Contenido:
  - 11 categorías organizadas
  - ~40 preguntas específicas y detalladas
  - Ejemplo real completo: "Ana" (enfermera, 35 años, Barcelona, preparando EIR)
  
Estructura de las 11 Categorías:
  1. Aspectos Demográficos (5 preguntas): nombre, edad, estudios, ingresos, ubicación, estado civil
  2. Hogar y Familia (3 preguntas): integrantes, ocio, responsabilidades
  3. Trabajo (3 preguntas): dónde trabaja, retos laborales, vida laboral vs personal
  4. Comportamiento (2 preguntas): relaciones, expresiones y lenguaje del grupo social
  5. Problema (2 preguntas): qué dolor activa búsqueda, cómo tu producto lo soluciona
  6. Búsqueda de la Solución (3 preguntas): dónde busca, cómo te encuentra, reacción a comerciales
  7. Objeciones y Barreras (2 preguntas): barreras para no comprar, excusas que usa
  8. Miedos e Inseguridades (2 preguntas): qué odia encontrar, experiencias negativas previas
  9. Comparación con Competencia (5 preguntas): factores de comparación, diferencias, mejor/peor, por qué elige
  10. Tu Producto o Servicio (4 preguntas): beneficios percibidos/no percibidos, complementarios, dudas postventa

Ejemplo Completo del Caso "Ana":
  - Enfermera de 35 años en Barcelona
  - Contratos temporales en sanidad pública
  - Salario: ~35.000€/año
  - Problema: Inestabilidad laboral genera ansiedad
  - Solución buscada: Preparar examen EIR para plaza fija
  - Lenguaje específico: "EIRsilente", "rEIRsilente"
  - Objeciones: Empresa nueva sin estadísticas de aprobados
  - Miedos: Dejar teléfono para conseguir info, llamadas insistentes

Uso en el Código:
  archivo: backend/src/agents/buyer_persona_agent.py
  
  implementación: |
    class BuyerPersonaAgent:
        def __init__(self):
            # Cargar plantilla base al inicializar
            with open('contenido/buyer-plantilla.md', 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            
            # Extraer estructura de preguntas para validación
            self.required_categories = [
                'Aspectos Demográficos',
                'Hogar y Familia',
                'Trabajo',
                # ... todas las 11 categorías
            ]
        
        def validate_analysis(self, analysis: Dict) -> bool:
            """Verificar que análisis incluye todas las categorías."""
            for category in self.required_categories:
                if category not in analysis:
                    return False
            return True
  
  en_prompt_del_agente: |
    # Inyectar estructura completa de la plantilla
    system_prompt = f"""
    {self.template_content}
    
    Responde TODAS las preguntas de la plantilla usando:
    - Respuestas iniciales del usuario
    - Documentos subidos (si existen)
    - Inferencia lógica basada en contexto
    """

Valor para el Sistema:
  - Define nivel de detalle esperado del análisis
  - Asegura consistencia en todos los buyer personas generados
  - Proporciona ejemplo real de calidad esperada
  - Cubre aspectos que otros análisis omiten (lenguaje del grupo, miedos específicos)
```

---

### RECURSO 2: Prompts Base del Agente (Borradores a Mejorar) 💬

```yaml
Ubicación: contenido/promts_borradores.md

Propósito:
  "Prompts iniciales que el agente usará como BASE y MEJORARÁ dinámicamente"

Contenido: 3 prompts clave del sistema

PROMPT 1 - Generación de Buyer Persona:
  contexto: |
    "Eres un experto en marketing digital con amplios conocimientos en mercadología, 
    el contexto de la situación es el siguiente, estas por comenzar una campaña 
    publicitaria en ADS con un plan de contenidos orgánico para una empresa..."
  
  input_requerido:
    - Lo que ofrece la empresa: [descripción del producto/servicio]
    - Público objetivo: [descripción del cliente ideal]
    - Tipo de negocio: [B2B o B2P]
  
  instrucciones_clave:
    - "Debes ignorar las respuestas de cada pregunta [de la plantilla], solo úsalas como guía"
    - "Responde todas las preguntas de manera completa y eficiente"
    - "Datos se usarán para campañas en Meta ADS y estrategia de content marketing"
    - "Respuestas basadas en la REALIDAD del público (no manipular para favorecer)"
    - "Con datos reales podremos dar soluciones reales"
    - "Establece un paso a paso: analiza primero documento, luego enfócate en necesidad real"
  
  mejoras_a_aplicar:
    - Añadir sección de "DOCUMENTOS DEL USUARIO" si existen
    - Enriquecer con técnicas de investigación de mercado
    - Personalizar según tipo de negocio específico
    - Inyectar contexto de transcripciones (técnicas de marketing)

PROMPT 2 - Simulación de Foro:
  contexto: |
    "Basándonos en el buyer persona que me acabas de responder, quiero que ahora 
    tomes el papel de esa persona e imagines que estás en un foro de internet..."
  
  escenario:
    - Foro de internet donde personas se quejan/recomiendan servicios
    - El agente ACTÚA COMO el buyer persona
    - Genera quejas de problemas al contratar servicios similares
    - Después de cada queja: solución deseada
  
  output_esperado:
    parte_1: "Array de {queja, solucion_deseada} (5-7 posts)"
    parte_2: "Lista de 10 puntos de dolor del personaje"
    detalles: "Todo lo que piensa y siente ANTES de comprar, criterios, comportamientos"
  
  mejoras_a_aplicar:
    - Enriquecer con contexto de documentos del usuario
    - Usar lenguaje específico del buyer persona
    - Añadir ejemplos de quejas reales (si documentos lo proporcionan)

PROMPT 3 - Customer Journey:
  contexto: |
    "Quiero que actúes como un experto en content marketing y basándote en 
    la documentación que te acabo de adjunta de mi buyer personas y de su papel 
    en un foro..."
  
  input_base:
    - Buyer persona completo
    - Simulación de foro con puntos de dolor
  
  output_requerido:
    - Customer Journey con 3 fases de conciencia EXTENDIDAS
  
  definiciones_de_fases:
    conciencia: |
      "Todo lo que el cliente hace hasta tomar conciencia de su necesidad.
      El consumidor está investigando opciones SIN intención comercial."
    
    consideracion: |
      "Tienen 2-3 opciones, pasan a investigación de cada una en profundidad.
      Puede tener presente algún interés comercial."
    
    compra: |
      "El cliente decide comprar, sobre la base de sus investigaciones."
  
  formato_de_salida:
    - CJ con mínimo 10 preguntas por cada fase
    - "Qué busca mi cliente ideal en internet" (10 preguntas)
    - "Qué quiere saber, qué pasa por su cabeza" (10 preguntas)
    - "Debes ser EXTENSO y conocer muy bien a quien le daremos este contenido"
  
  mejoras_a_aplicar:
    - Usar buyer persona + foro para ser específico
    - Consultar knowledge base (transcripciones) para tipos de contenido efectivos
    - Personalizar según fase del embudo de marketing

Uso en el Código:
  ubicación: backend/src/agents/
  
  archivos_afectados:
    - buyer_persona_agent.py: Usa PROMPT 1 (mejorado)
    - forum_simulator_agent.py: Usa PROMPT 2 (mejorado)
    - customer_journey_agent.py: Usa PROMPT 3 (mejorado)
  
  patrón_de_mejora: |
    class BuyerPersonaAgent:
        def __init__(self):
            # 1. Cargar prompt base desde archivo
            with open('contenido/promts_borradores.md', 'r') as f:
                prompts_raw = f.read()
            
            # 2. Extraer prompt específico (parsear markdown)
            self.base_prompt_buyer_persona = self._extract_prompt(prompts_raw, "Promt de buyer persona")
            
            # 3. Mejorar dinámicamente según contexto
            self.enhanced_prompt = self._enhance_prompt(
                base=self.base_prompt_buyer_persona,
                template=template_content,
                user_context=user_info,
                documents_context=docs_summary
            )
        
        def _enhance_prompt(self, base, template, user_context, documents_context):
            """
            Mejora el prompt base con:
            - Plantilla completa (contenido/buyer-plantilla.md)
            - Contexto del usuario
            - Información de documentos subidos
            - Técnicas de las transcripciones
            """
            return f"""
            {base}
            
            PLANTILLA COMPLETA A SEGUIR:
            {template}
            
            INFORMACIÓN ADICIONAL DEL NEGOCIO:
            {documents_context}
            
            TÉCNICAS DE MARKETING A APLICAR:
            {marketing_techniques_from_knowledge_base}
            """

Estado Actual:
  - ✅ Prompts base definidos y claros
  - ⚠️ Requieren mejora dinámica con contexto
  - ⚠️ Deben integrarse con plantilla completa
  - ⚠️ Deben enriquecerse con transcripciones

Siguiente Paso:
  "Al implementar BuyerPersonaAgent (TAREA 4), cargar estos prompts y mejorarlos"
```

---

### RECURSO 3: Material de Entrenamiento - Transcripciones de Andrea Estratega 🎓

```yaml
Ubicación: contenido/Transcriptions Andrea Estratega/

Propósito:
  "Entrenar al agente en técnicas REALES de creación de contenido viral para redes sociales"

Contenido: 9 transcripciones de videos de YouTube:

1. "6 Carruseles en Instagram que te harán viral en 2025 (y su estructura).txt"
   Temas: Formatos de carruseles virales, estructura replicable
   Aplicación: Cuando usuario pide ideas de carruseles para Instagram

2. "Cómo hacer 7 guiones virales en menos de 30 min CON UNA ESTRUCTURA copia y pega.txt"
   Temas: Templates de guiones rápidos, estructura copia-pega
   Aplicación: Cuando usuario pide scripts de videos

3. "Domina el Storytelling de tu Rubro en 19 minutos (nunca lo olvidarás).txt"
   Temas: Storytelling aplicado, narrativa persuasiva por sector
   Aplicación: Cuando usuario pide contenido narrativo

4. "El secreto detrás de los videos que no puedes dejar de ver (usan 1 solo formato).txt"
   Temas: Formatos adictivos, retención de atención, psicología del engagement
   Aplicación: Cuando usuario pide videos con alta retención

5. "El sistema IA que Crea contenido para Redes sociales Todos los días (100% automático).txt"
   Temas: Automatización de contenido, sistemas IA, workflows
   Aplicación: Cuando usuario pregunta por automatización

6. "El Top Embudo de Redes sociales Explicado en 16 Minutos  Contenido de Valor.txt"
   Temas: Top of funnel, contenido de valor, awareness phase
   Aplicación: Cuando usuario pide contenido para fase de conciencia

7. "Estudié +50 formatos de video, te reveló los 5 MÁS VIRALES.txt"
   Temas: Análisis de formatos virales, tendencias probadas
   Aplicación: Cuando usuario pide formatos con mayor viralidad

8. "La forma más RÁPIDA de crecer tu Instagram y Tiktok en 2026 (5 estrategias).txt"
   Temas: Crecimiento orgánico 2026, estrategias actualizadas
   Aplicación: Cuando usuario pide estrategia de crecimiento

9. "Todo lo que el CEO de Instagram dijo para 2026 (revela los secretos para crecer).txt"
   Temas: Algoritmo de Instagram oficial, tendencias 2026, secretos del CEO
   Aplicación: Cuando usuario pregunta por algoritmo o tendencias 2026

Procesamiento Técnico:
  
  script: backend/scripts/ingest_training_data.py
  
  pasos:
    1. Leer cada archivo .txt de la carpeta
    2. Chunking con RecursiveCharacterTextSplitter:
       - chunk_size: 1000 tokens
       - chunk_overlap: 200 tokens
    3. Generar embeddings con OpenAI text-embedding-3-large
    4. Insertar en marketing_knowledge_base:
       configuración:
         - project_id: NULL (conocimiento GLOBAL, no de un proyecto específico)
         - chat_id: NULL (conocimiento GLOBAL, no de un chat específico)
         - content_type: 'video_transcript'
         - source_title: nombre del archivo (ej: "6 Carruseles en Instagram...")
         - chunk_text: texto del chunk
         - chunk_index: índice del chunk en el documento
         - metadata: {"autor": "Andrea Estratega", "tema": "content_marketing", "año": "2025-2026"}
         - embedding: vector de 1536 dimensiones
  
  comando_de_ingesta: |
    python backend/scripts/ingest_training_data.py \
      --source "contenido/Transcriptions Andrea Estratega/" \
      --content-type video_transcript \
      --metadata '{"autor":"Andrea Estratega","tema":"content_marketing"}'
  
  verificación: |
    # Verificar chunks en DB
    SELECT 
      COUNT(*) as total_chunks,
      source_title,
      COUNT(DISTINCT chunk_index) as chunks_per_doc
    FROM marketing_knowledge_base
    WHERE content_type = 'video_transcript'
      AND metadata->>'autor' = 'Andrea Estratega'
    GROUP BY source_title;
    
    # Esperado: 
    # - 9 documentos (uno por archivo)
    # - ~200-500 chunks totales (dependiendo de longitud)
    # - ~20-60 chunks por documento promedio

Uso en el Agente (ContentGeneratorAgent):
  
  flujo_de_búsqueda: |
    # Cuando usuario pide: "Dame 5 ideas de videos para fase de conciencia"
    
    1. Construir query de búsqueda:
       query = "ideas videos contenido fase conciencia awareness engagement"
    
    2. Generar embedding del query:
       query_embedding = await embedding_service.generate_embedding(query)
    
    3. Buscar en knowledge_base:
       results = await vector_search.search(
           query_embedding=query_embedding,
           project_id=user.project_id,  # Incluirá también docs del usuario
           chat_id=chat_id,
           match_count=10
       )
       # Retorna:
       # - Chunks de transcripciones de Andrea (project_id NULL)
       # - Chunks de documentos del usuario (project_id, chat_id específicos)
    
    4. Filtrar transcripciones:
       transcription_chunks = [r for r in results if r['content_type'] == 'video_transcript']
    
    5. Inyectar en prompt:
       context = "\n\n".join([
           f"TÉCNICA DE ANDREA ESTRATEGA ({chunk['source_title']}):\n{chunk['content']}"
           for chunk in transcription_chunks[:5]
       ])
       
       prompt = f"""
       BUYER PERSONA DEL USUARIO:
       {buyer_persona}
       
       CUSTOMER JOURNEY (Fase Conciencia):
       {customer_journey['awareness']}
       
       TÉCNICAS DE CREACIÓN DE CONTENIDO:
       {context}
       
       Genera 5 ideas de videos para fase de conciencia combinando:
       - El perfil específico del buyer persona
       - Las técnicas virales de las transcripciones
       - El comportamiento del customer journey
       """

Valor Diferencial:
  - "Este es el conocimiento que diferencia al agente de ChatGPT genérico"
  - "Técnicas probadas de creación de contenido viral"
  - "Contexto específico de redes sociales 2025-2026"
  - "Estrategias basadas en algoritmos reales de Instagram/TikTok"
  - "Material de Andrea Estratega (experta reconocida)"

CRÍTICO - Sin estas transcripciones:
  - El agente sería un chatbot genérico
  - Respuestas serían teóricas, no prácticas
  - No tendría técnicas actualizadas de 2026
  - No conocería formatos virales probados
```

---

### RECURSO 4: Integración de los 3 Recursos en el Flujo del Agente

```yaml
Flujo Completo de Uso:

ETAPA 1 - Análisis Inicial:
  input_usuario:
    - 4-5 respuestas a preguntas iniciales
    - (Opcional) Documentos subidos (.txt, .pdf, .docx)
  
  proceso_agente:
    1. Cargar RECURSO 2 (Prompt 1 de buyer persona)
    2. Mejorar prompt con:
       - Respuestas del usuario
       - Info de documentos subidos (si existen)
    3. Usar RECURSO 1 (Plantilla completa) como estructura
    4. Generar análisis completo
    5. Validar que cubre las 11 categorías
  
  output:
    - Buyer persona completo en JSON (almacenar en DB)
    - Documento formateado para el usuario (markdown)

ETAPA 2 - Simulación y Extracción:
  proceso_agente:
    1. Cargar RECURSO 2 (Prompt 2 de foro)
    2. Usar buyer persona generado
    3. Simular comportamiento en foro
    4. Extraer 10 puntos de dolor
  
  output:
    - Forum simulation en JSON
    - Pain points en array de 10 strings

ETAPA 3 - Customer Journey:
  proceso_agente:
    1. Cargar RECURSO 2 (Prompt 3 de CJ)
    2. Usar buyer persona + puntos de dolor
    3. Consultar RECURSO 3 (transcripciones) para tipos de contenido efectivos por fase
    4. Generar 3 fases con mínimo 10 preguntas cada una
  
  output:
    - Customer Journey en JSON (3 fases)
    - Documento completo formateado

ETAPA 4 - Generación de Contenido (On-Demand):
  trigger: "Usuario hace petición explícita"
  
  ejemplo_petición: "Dame 5 ideas de videos para fase de conciencia"
  
  proceso_agente:
    1. Recuperar de DB:
       - RECURSO 1 (buyer persona del chat)
       - Customer Journey (fase awareness)
    
    2. Buscar en RECURSO 3 (knowledge base):
       query: "ideas videos contenido conciencia viral"
       resultado: Top-10 chunks de transcripciones relevantes
    
    3. Combinar contextos:
       - Perfil del buyer persona (necesidades, lenguaje, problemas)
       - Fase del customer journey (qué busca, qué piensa)
       - Técnicas de transcripciones (formatos virales, hooks, estructuras)
    
    4. Generar contenido personalizado:
       - 5 ideas de videos
       - Cada idea con: título, hook, estructura, CTA
       - Adaptado específicamente al buyer persona
       - Usando técnicas probadas de Andrea Estratega

Código de Integración (en ContentGeneratorAgent):
  
  método_principal: |
    async def generate_content_ideas(
        self,
        chat_id: UUID,
        project_id: UUID,
        phase: str,  # 'awareness' | 'consideration' | 'purchase'
        content_type: str,  # 'video' | 'post' | 'article'
        count: int = 5
    ) -> List[Dict]:
        # 1. Recuperar contexto de largo plazo
        buyer_persona = await self.memory.get_long_term_context(chat_id, project_id)
        
        # 2. Buscar técnicas en transcripciones (RECURSO 3)
        search_query = f"{content_type} {phase} viral técnicas"
        techniques = await self.memory.get_semantic_context(
            query=search_query,
            project_id=project_id,
            chat_id=chat_id,
            k=10
        )
        
        # Filtrar solo transcripciones
        andrea_techniques = [
            t for t in techniques 
            if t['content_type'] == 'video_transcript'
        ]
        
        # 3. Construir prompt enriquecido
        prompt = self._build_enhanced_prompt(
            buyer_persona=buyer_persona,
            phase=phase,
            techniques=andrea_techniques[:5],
            count=count
        )
        
        # 4. Generar con Claude
        response = await self.llm.generate(prompt)
        
        return response

Valor de la Integración:
  - Buyer persona específico del usuario (RECURSO 1)
  + Prompts optimizados y mejorados (RECURSO 2)
  + Técnicas probadas de contenido viral (RECURSO 3)
  = Contenido ULTRA-PERSONALIZADO y ACCIONABLE
```

---

## 📝 Lista de Tareas Detalladas

### TAREA 0: Instalar y Configurar MCP Serena (⚡ OBLIGATORIO)

**Herramientas a utilizar:**
- ⚡ MCP Archon: Documentación de MCPs
  - Importancia: "Consultar instalación de MCPs en Cursor"
  - Comando: `rag_search_knowledge_base(query="MCP installation", match_count=3)`

- 🔧 MCP Serena: Onboarding del proyecto
  - Importancia: "Activar para análisis simbólico de código"

- 📚 Skill environment-setup-guide: Setup correcto
  - Importancia: "Guía de configuración de entorno"

**Objetivo:**
Instalar y verificar que Serena está activo para análisis simbólico del código sin leer archivos completos.

**Pasos a seguir:**
1. Verificar que Serena está en configuración de Cursor (`~/.cursor/mcp-config.json`)
2. Activar Serena en el proyecto actual
3. Ejecutar onboarding si es necesario
4. Probar con `get_symbols_overview('Context-Engineering-Intro/examples/')`

**Criterios de aceptación:**
- [ ] Serena activo y respondiendo comandos
- [ ] Puede ejecutar `get_symbols_overview`
- [ ] Onboarding completado si era necesario

---

### TAREA 1: Configurar Base de Datos en Supabase

**Herramientas a utilizar:**
- ⚡ MCP Archon: Documentación de Supabase + pgvector
  - Importancia: "Necesitamos docs oficiales sobre pgvector y RLS en Supabase"
  - Comando: `rag_search_knowledge_base(query="supabase pgvector create index", source_id="9c5f534e51ee9237", match_count=8)`
  - Comando: `rag_search_knowledge_base(query="supabase row level security", source_id="9c5f534e51ee9237", match_count=5)`

- 🔧 MCP Serena: Análisis de estructura de ejemplo (si existe migration de referencia)
  - Comando: `get_symbols_overview('Context-Engineering-Intro/examples/mcp-server/src/database/')`

- 📚 Skill postgres-best-practices: Optimización de queries
  - Importancia: "Patrones de performance para Postgres"

**Objetivo:**
Configurar Supabase con todas las tablas, extensiones, índices y funciones necesarias para el proyecto.

**Pasos a seguir:**

1. **Habilitar extensión pgvector:**
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```

2. **Crear 8 tablas con prefijo `marketing_`:**
   - Usar esquema definido en sección "Modelos de Datos"
   - **CRÍTICO**: Incluir `project_id` en TODAS las tablas
   - Crear índices según especificado
   - Configurar RLS (Row Level Security) en todas las tablas

3. **Crear función `marketing_match_documents` para búsqueda vectorial:**
   ```sql
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

4. **Crear proyecto de prueba:**
   ```sql
   INSERT INTO marketing_projects (id, name, created_at, updated_at)
   VALUES (uuid_generate_v4(), 'Test Project', NOW(), NOW());
   ```

5. **Configurar políticas RLS:**
   ```sql
   -- Ejemplo para marketing_chats
   ALTER TABLE marketing_chats ENABLE ROW LEVEL SECURITY;
   
   CREATE POLICY "Users can only see their own chats"
   ON marketing_chats
   FOR SELECT
   USING (user_id = auth.uid() AND project_id = current_project());
   
   -- Repetir para todas las tablas
   ```

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 1 - pgvector index**: Usar HNSW en vez de ivfflat porque:
- IVFFlat requiere >1000 documentos para ser efectivo
- HNSW funciona bien con cualquier cantidad de datos
- Performance superior en general (validado por Supabase docs)

**SQL para índices vectoriales (usar HNSW):**
```sql
-- ✅ CORRECTO: HNSW index (funciona con <1000 docs)
CREATE INDEX idx_knowledge_base_embedding_hnsw 
ON marketing_knowledge_base 
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX idx_buyer_personas_embedding_hnsw 
ON marketing_buyer_personas 
USING hnsw (embedding vector_cosine_ops);

-- ❌ NO USAR: ivfflat (solo efectivo con >1000 docs)
-- CREATE INDEX ... USING ivfflat ...
```

**Criterios de aceptación:**
- [ ] Extensiones pgvector y uuid-ossp habilitadas
- [ ] 8 tablas creadas con prefijo `marketing_`
- [ ] ✅ Índices HNSW creados (NO ivfflat) para embeddings
- [ ] Función `marketing_match_documents` funcional
- [ ] Proyecto de prueba creado exitosamente
- [ ] RLS configurado en todas las tablas
- [ ] Test: `SELECT * FROM marketing_match_documents('[0.1, 0.2, ...]', 0.7, 10, <project_id>)` retorna sin error

**Archivos a crear:**
- `backend/db/migrations/001_initial_schema.sql` (tablas + índices)
- `backend/db/migrations/002_create_match_function.sql` (función vectorial)
- `backend/db/migrations/003_configure_rls.sql` (políticas RLS)
- `backend/db/seed_data.sql` (proyecto de prueba)

**Comandos de validación:**
```bash
# Ejecutar desde psql o Supabase SQL Editor
psql $DATABASE_URL -f backend/db/migrations/001_initial_schema.sql
psql $DATABASE_URL -f backend/db/migrations/002_create_match_function.sql
psql $DATABASE_URL -f backend/db/migrations/003_configure_rls.sql

# Verificar tablas creadas
psql $DATABASE_URL -c "\dt marketing_*"

# Verificar función
psql $DATABASE_URL -c "SELECT routine_name FROM information_schema.routines WHERE routine_name LIKE 'marketing_%';"
```

---

### TAREA 2: Setup Backend con FastAPI + Autenticación Manual

**Herramientas a utilizar:**
- ⚡ MCP Archon: FastAPI + Pydantic
  - Comando: `rag_search_knowledge_base(query="fastapi project structure async", source_id="c889b62860c33a44", match_count=5)`
  - Comando: `rag_search_knowledge_base(query="pydantic v2 model validation", source_id="9d46e91458092424", match_count=5)`
  - Comando: `rag_search_code_examples(query="fastapi jwt authentication", source_id="c889b62860c33a44", match_count=3)`

- 🔧 MCP Serena: Analizar estructura de ejemplo de agente
  - Comando: `get_symbols_overview('Context-Engineering-Intro/examples/main_agent_reference/research_agent.py')`

- 📚 Skills:
  - python-patterns (automático)
  - clean-code (automático)

**Objetivo:**
Configurar FastAPI con estructura modular, SQLAlchemy + Alembic, y sistema de autenticación manual con JWT.

**Pasos a seguir:**

1. **Consultar Archon sobre estructura de proyecto FastAPI:**
   - Ejecutar comandos de Archon listados arriba
   - Tomar notas sobre mejores prácticas

2. **Crear estructura de carpetas:**
   ```bash
   mkdir -p backend/src/{api,agents,db,services,schemas,utils}
   mkdir -p backend/tests/{unit,integration,fixtures}
   mkdir -p backend/scripts
   touch backend/pyproject.toml backend/.env backend/README.md
   ```

3. **Configurar pyproject.toml con dependencias:**
   ```toml
   [project]
   name = "marketing-brain-backend"
   version = "0.1.0"
   dependencies = [
       "fastapi>=0.109.0",
       "uvicorn[standard]>=0.27.0",
       "pydantic>=2.5.0",
       "pydantic-settings>=2.1.0",
       "sqlalchemy>=2.0.25",
       "alembic>=1.13.0",
       "asyncpg>=0.29.0",
       "langchain>=0.1.0",
       "langgraph>=0.0.20",
       "anthropic>=0.18.0",
       "openai>=1.12.0",
       "pgvector>=0.2.4",
       "bcrypt>=4.1.2",
       "pyjwt>=2.8.0",
       "python-multipart>=0.0.9",
       "redis>=5.0.1",
       "pypdf2>=3.0.1",
       "python-docx>=1.1.0",
   ]
   ```

4. **Implementar modelos SQLAlchemy:**
   - Crear `backend/src/db/models.py` con modelos de sección "Modelos de Datos"
   - Usar async patterns con SQLAlchemy 2.0

5. **Implementar schemas Pydantic:**
   - `backend/src/schemas/auth.py` (RegisterRequest, LoginRequest, etc.)
   - Usar Field descriptions detalladas
   - Agregar validadores custom

6. **Implementar autenticación manual:**
   
   **`backend/src/api/auth.py`:**
   ```python
   from fastapi import APIRouter, HTTPException, Depends
   from ..schemas.auth import RegisterRequest, LoginRequest, LoginResponse
   from ..utils.password import hash_password, verify_password
   from ..utils.jwt import create_access_token
   
   router = APIRouter(prefix="/api/auth", tags=["auth"])
   
   @router.post("/register")
   async def register(request: RegisterRequest):
       # 1. Verificar que email no existe en proyecto
       # 2. Hash password con bcrypt
       # 3. Crear usuario en DB
       # 4. Retornar user info (sin password)
       pass
   
   @router.post("/login", response_model=LoginResponse)
   async def login(request: LoginRequest):
       # 1. Buscar usuario por email + project_id
       # 2. Verificar password
       # 3. Generar JWT con user_id, email, project_id
       # 4. Retornar token + user info
       pass
   
   @router.post("/request-password-reset")
   async def request_password_reset(request: RequestPasswordResetRequest):
       # 1. Buscar usuario
       # 2. Generar token único (UUID)
       # 3. Guardar en marketing_password_reset_tokens (expires_at = 1 hora)
       # 4. Retornar token (en producción: enviar link mágico)
       pass
   
   @router.post("/reset-password")
   async def reset_password(request: ResetPasswordRequest):
       # 1. Validar token (existe, no usado, no expirado)
       # 2. Hash nuevo password
       # 3. Actualizar password de usuario
       # 4. Marcar token como usado
       pass
   ```
   
   **`backend/src/utils/password.py`:**
   ```python
   import bcrypt
   
   def hash_password(password: str) -> str:
       salt = bcrypt.gensalt(rounds=12)
       return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
   
   def verify_password(password: str, hashed: str) -> bool:
       return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
   ```
   
   **`backend/src/utils/jwt.py`:**
   ```python
   import jwt
   from datetime import datetime, timedelta
   from typing import Dict
   import os
   
   SECRET_KEY = os.getenv('JWT_SECRET_KEY')
   ALGORITHM = "HS256"
   
   def create_access_token(data: Dict, expires_delta: timedelta = timedelta(days=7)) -> str:
       to_encode = data.copy()
       expire = datetime.utcnow() + expires_delta
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   
   def decode_access_token(token: str) -> Dict:
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           return payload
       except jwt.ExpiredSignatureError:
           raise HTTPException(status_code=401, detail="Token expired")
       except jwt.JWTError:
           raise HTTPException(status_code=401, detail="Invalid token")
   ```

7. **Implementar middleware de autenticación:**
   
   **⚠️ GOTCHA CRÍTICO APLICADO:**
   **GOTCHA 6 - Supabase RLS bypass**: Service role key NO respeta RLS policies.
   - Solución: Validación manual de project_id en TODAS las queries
   - Middleware inyecta project_id desde JWT en request.state
   - NUNCA confiar solo en RLS para aislamiento multi-tenant
   
   **`backend/src/middleware/auth.py`:**
   ```python
   from fastapi import Request, HTTPException
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   from ..utils.jwt import decode_access_token
   
   security = HTTPBearer()
   
   async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
       token = credentials.credentials
       payload = decode_access_token(token)
       return payload  # {user_id, email, project_id}
   
   async def inject_project_id(request: Request, call_next):
       """
       ⚠️ CRÍTICO PARA GOTCHA 6
       
       Middleware que inyecta project_id desde JWT en request.state
       para asegurar aislamiento multi-tenant.
       
       Supabase Service Role Key bypasea RLS, por lo que DEBEMOS
       validar project_id manualmente en TODAS las queries.
       """
       public_paths = ["/api/auth/", "/health", "/docs", "/openapi.json"]
       
       if not any(path in request.url.path for path in public_paths):
           # Extraer token de header Authorization
           auth_header = request.headers.get("Authorization")
           if not auth_header or not auth_header.startswith("Bearer "):
               raise HTTPException(status_code=401, detail="Missing or invalid token")
           
           token = auth_header.split(" ")[1]
           payload = decode_access_token(token)
           
           # ✅ Inyectar en request.state (disponible en todos los endpoints)
           request.state.user_id = payload['user_id']
           request.state.project_id = payload['project_id']  # ← CRÍTICO
           request.state.email = payload['email']
       
       response = await call_next(request)
       return response
   ```
   
   **Ejemplo de uso en endpoint (SIEMPRE incluir project_id):**
   ```python
   @router.get("/api/chats")
   async def get_user_chats(request: Request):
       user_id = request.state.user_id
       project_id = request.state.project_id  # Del JWT, NO del input del usuario
       
       # ✅ CORRECTO: Query con project_id explícito
       chats = await db.query(
           "SELECT * FROM marketing_chats WHERE user_id = $1 AND project_id = $2",
           user_id, project_id
       )
       
       # ❌ INCORRECTO: Query sin project_id
       # chats = await db.query("SELECT * FROM marketing_chats WHERE user_id = $1", user_id)
       
       return {"chats": chats}
   ```

8. **Configurar main.py:**
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   from .api import auth
   from .middleware.auth import inject_project_id
   
   app = FastAPI(title="Marketing Brain API", version="1.0.0")
   
   # CORS
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   
   # Custom middleware
   app.middleware("http")(inject_project_id)
   
   # Routers
   app.include_router(auth.router)
   
   @app.get("/health")
   async def health():
       return {"status": "ok"}
   ```

**Criterios de aceptación:**
- [ ] Estructura de carpetas creada
- [ ] pyproject.toml con todas las dependencias
- [ ] Modelos SQLAlchemy creados (8 tablas)
- [ ] Schemas Pydantic creados (auth)
- [ ] Endpoints de auth implementados:
  - [ ] POST /api/auth/register
  - [ ] POST /api/auth/login
  - [ ] POST /api/auth/request-password-reset
  - [ ] POST /api/auth/reset-password
- [ ] Utils de password y JWT funcionan
- [ ] Middleware de autenticación inyecta project_id
- [ ] Sin errores de linting: `ruff check backend/src/`
- [ ] Sin errores de tipos: `mypy backend/src/`

**Archivos a crear:**
- `backend/pyproject.toml`
- `backend/src/main.py`
- `backend/src/db/models.py`
- `backend/src/schemas/auth.py`
- `backend/src/api/auth.py`
- `backend/src/utils/password.py`
- `backend/src/utils/jwt.py`
- `backend/src/middleware/auth.py`

**Comandos de validación:**
```bash
# Linting
ruff check backend/src/ --fix

# Type checking
mypy backend/src/

# Tests de auth
pytest backend/tests/test_auth.py -v

# Test manual (con servidor corriendo)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","full_name":"Test User","project_id":"<uuid>"}'
```

---

### TAREA 3: Sistema de Chat Básico (sin IA todavía)

**Herramientas a utilizar:**
- ⚡ MCP Archon: FastAPI + SQLAlchemy async
  - Comando: `rag_search_knowledge_base(query="fastapi dependency injection", source_id="c889b62860c33a44", match_count=5)`
  - Comando: `rag_search_code_examples(query="sqlalchemy async session", source_id="9c5f534e51ee9237", match_count=3)`

- 🔧 MCP Serena: Analizar implementación de auth de TAREA 2
  - Comando: `get_symbols_overview('backend/src/api/auth.py')`
  - Comando: `find_symbol('get_current_user', 'backend/src/middleware/auth.py', True)`

- 📚 Skills: clean-code, python-patterns

**Objetivo:**
Implementar CRUD de chats y mensajes (sin IA todavía), con filtrado estricto por `project_id`.

**Pasos a seguir:**

1. **Crear schemas para chat:**
   
   **`backend/src/schemas/chat.py`:**
   - Usar esquema de sección "Pydantic Schemas"
   - CreateChatRequest, CreateChatResponse, SendMessageRequest, Message, ChatSummary

2. **Implementar servicio de chat:**
   
   **`backend/src/services/chat_service.py`:**
   ```python
   from sqlalchemy.ext.asyncio import AsyncSession
   from uuid import UUID
   from ..db.models import MarketingChat, MarketingMessage
   from ..schemas.chat import CreateChatRequest, Message
   
   class ChatService:
       def __init__(self, db: AsyncSession):
           self.db = db
       
       async def create_chat(self, user_id: UUID, project_id: UUID, title: str = "New Chat"):
           """
           Crear nuevo chat.
           
           CRÍTICO: Incluir project_id para aislamiento.
           """
           chat = MarketingChat(
               user_id=user_id,
               project_id=project_id,
               title=title
           )
           self.db.add(chat)
           await self.db.commit()
           await self.db.refresh(chat)
           return chat
       
       async def list_chats(self, user_id: UUID, project_id: UUID):
           """
           Listar chats del usuario.
           
           CRÍTICO: Filtrar por project_id.
           """
           query = select(MarketingChat).where(
               MarketingChat.user_id == user_id,
               MarketingChat.project_id == project_id
           ).order_by(MarketingChat.created_at.desc())
           
           result = await self.db.execute(query)
           return result.scalars().all()
       
       async def get_chat(self, chat_id: UUID, user_id: UUID, project_id: UUID):
           """
           Obtener chat específico.
           
           CRÍTICO: Validar que pertenece al usuario y proyecto.
           """
           query = select(MarketingChat).where(
               MarketingChat.id == chat_id,
               MarketingChat.user_id == user_id,
               MarketingChat.project_id == project_id
           )
           result = await self.db.execute(query)
           chat = result.scalar_one_or_none()
           if not chat:
               raise HTTPException(404, "Chat not found")
           return chat
       
       async def update_chat_title(self, chat_id: UUID, user_id: UUID, project_id: UUID, new_title: str):
           chat = await self.get_chat(chat_id, user_id, project_id)
           chat.title = new_title
           await self.db.commit()
           return chat
       
       async def delete_chat(self, chat_id: UUID, user_id: UUID, project_id: UUID):
           chat = await self.get_chat(chat_id, user_id, project_id)
           await self.db.delete(chat)
           await self.db.commit()
       
       async def get_messages(self, chat_id: UUID, user_id: UUID, project_id: UUID):
           """
           Obtener mensajes del chat.
           
           CRÍTICO: Validar que chat pertenece al usuario y proyecto.
           """
           # Primero validar acceso al chat
           await self.get_chat(chat_id, user_id, project_id)
           
           query = select(MarketingMessage).where(
               MarketingMessage.chat_id == chat_id
           ).order_by(MarketingMessage.created_at.asc())
           
           result = await self.db.execute(query)
           return result.scalars().all()
       
       async def create_message(self, chat_id: UUID, user_id: UUID, project_id: UUID, role: str, content: str):
           # Validar acceso
           await self.get_chat(chat_id, user_id, project_id)
           
           message = MarketingMessage(
               chat_id=chat_id,
               project_id=project_id,
               role=role,
               content=content
           )
           self.db.add(message)
           await self.db.commit()
           await self.db.refresh(message)
           return message
   ```

3. **Implementar endpoints de chat:**
   
   **`backend/src/api/chat.py`:**
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from uuid import UUID
   from ..schemas.chat import *
   from ..services.chat_service import ChatService
   from ..middleware.auth import get_current_user
   
   router = APIRouter(prefix="/api/chats", tags=["chat"])
   
   @router.get("/")
   async def list_chats(current_user: dict = Depends(get_current_user)):
       service = ChatService(db)
       chats = await service.list_chats(
           user_id=current_user['user_id'],
           project_id=current_user['project_id']
       )
       return {"chats": [ChatSummary.model_validate(c) for c in chats]}
   
   @router.post("/", response_model=CreateChatResponse)
   async def create_chat(
       request: CreateChatRequest,
       current_user: dict = Depends(get_current_user)
   ):
       service = ChatService(db)
       chat = await service.create_chat(
           user_id=current_user['user_id'],
           project_id=current_user['project_id'],
           title=request.title
       )
       return CreateChatResponse.model_validate(chat)
   
   @router.patch("/{chat_id}")
   async def update_chat(
       chat_id: UUID,
       title: str,
       current_user: dict = Depends(get_current_user)
   ):
       service = ChatService(db)
       chat = await service.update_chat_title(
           chat_id, current_user['user_id'], current_user['project_id'], title
       )
       return {"success": True, "chat": chat}
   
   @router.delete("/{chat_id}")
   async def delete_chat(
       chat_id: UUID,
       current_user: dict = Depends(get_current_user)
   ):
       service = ChatService(db)
       await service.delete_chat(chat_id, current_user['user_id'], current_user['project_id'])
       return {"success": True}
   
   @router.get("/{chat_id}/messages")
   async def get_messages(
       chat_id: UUID,
       current_user: dict = Depends(get_current_user)
   ):
       service = ChatService(db)
       messages = await service.get_messages(chat_id, current_user['user_id'], current_user['project_id'])
       return {"messages": [Message.model_validate(m) for m in messages]}
   
   @router.post("/{chat_id}/messages")
   async def send_message(
       chat_id: UUID,
       request: SendMessageRequest,
       current_user: dict = Depends(get_current_user)
   ):
       service = ChatService(db)
       
       # 1. Guardar mensaje del usuario
       user_msg = await service.create_message(
           chat_id, current_user['user_id'], current_user['project_id'],
           role="user", content=request.content
       )
       
       # 2. (Por ahora) Respuesta dummy del asistente
       assistant_msg = await service.create_message(
           chat_id, current_user['user_id'], current_user['project_id'],
           role="assistant", content="Echo: " + request.content
       )
       
       return {"user_message": Message.model_validate(user_msg), "assistant_message": Message.model_validate(assistant_msg)}
   ```

4. **Registrar router en main.py:**
   ```python
   from .api import auth, chat
   
   app.include_router(auth.router)
   app.include_router(chat.router)
   ```

**Criterios de aceptación:**
- [ ] ChatService implementado con métodos CRUD
- [ ] Todos los métodos filtran por `project_id`
- [ ] Endpoints funcionan:
  - [ ] GET /api/chats (listar)
  - [ ] POST /api/chats (crear)
  - [ ] PATCH /api/chats/{id} (editar título)
  - [ ] DELETE /api/chats/{id}
  - [ ] GET /api/chats/{id}/messages
  - [ ] POST /api/chats/{id}/messages
- [ ] Tests con pytest
- [ ] Verificar aislamiento entre proyectos (crear 2 proyectos de prueba)
- [ ] Sin errores de linting/tipos

**Archivos a crear:**
- `backend/src/schemas/chat.py`
- `backend/src/services/chat_service.py`
- `backend/src/api/chat.py`
- `backend/tests/test_chat.py`

**Comandos de validación:**
```bash
# Tests
pytest backend/tests/test_chat.py -v

# Test manual (servidor corriendo + token JWT)
curl -X POST http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}'

curl -X GET http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN"
```

---

### TAREA 3.5: Procesamiento de Documentos del Usuario (NUEVO)

**Herramientas a utilizar:**
- ⚡ MCP Archon: FastAPI file upload + Python parsers
  - Comando: `rag_search_knowledge_base(query="fastapi file upload validation", source_id="c889b62860c33a44", match_count=5)`
  - Comando: `rag_search_knowledge_base(query="python pdf parsing text extraction", match_count=5)`
  - Comando: `rag_search_knowledge_base(query="langchain text splitter", source_id="e74f94bb9dcb14aa", match_count=5)`

- 🔧 MCP Serena: Analizar servicio de chat de TAREA 3
  - Comando: `get_symbols_overview('backend/src/services/chat_service.py')`

- 📚 Skills:
  - python-patterns
  - clean-code

**Objetivo:**
Permitir que usuarios suban archivos (.txt, .pdf, .docx) con información de su negocio, procesarlos, hacer chunking, generar embeddings y almacenarlos en `marketing_knowledge_base` con `project_id` y `chat_id` para búsqueda semántica posterior.

**Pasos a seguir:**

1. **Consultar Archon sobre parsers y chunking:**
   - Ejecutar comandos de Archon listados arriba
   - Entender estrategias de chunking (RecursiveCharacterTextSplitter)

2. **Crear schemas para documentos:**
   
   **`backend/src/schemas/documents.py`:**
   - Usar esquema de sección "Pydantic Schemas"

3. **Implementar parsers de archivos:**
   
   **`backend/src/utils/file_parsers.py`:**
   ```python
   from pathlib import Path
   import PyPDF2
   import docx
   
   async def parse_txt(file_path: Path) -> str:
       """Parse .txt file and return content."""
       with open(file_path, 'r', encoding='utf-8') as f:
           return f.read()
   
   async def parse_pdf(file_path: Path) -> str:
       """Parse .pdf file and extract text."""
       text = []
       with open(file_path, 'rb') as f:
           reader = PyPDF2.PdfReader(f)
           for page in reader.pages:
               text.append(page.extract_text())
       return "\n".join(text)
   
   async def parse_docx(file_path: Path) -> str:
       """Parse .docx file and extract text."""
       doc = docx.Document(file_path)
       return "\n".join([para.text for para in doc.paragraphs])
   
   async def parse_document(file_path: Path, file_type: str) -> str:
       """Route to appropriate parser based on file type."""
       parsers = {
           '.txt': parse_txt,
           '.pdf': parse_pdf,
           '.docx': parse_docx,
       }
       parser = parsers.get(file_type)
       if not parser:
           raise ValueError(f"Unsupported file type: {file_type}")
       return await parser(file_path)
   ```

4. **Implementar servicio de procesamiento de documentos:**
   
   **`backend/src/services/document_processor.py`:**
   ```python
   from pathlib import Path
   from uuid import UUID
   from langchain.text_splitter import RecursiveCharacterTextSplitter
   from ..utils.file_parsers import parse_document
   from ..services.embedding_service import EmbeddingService
   from ..db.models import MarketingKnowledgeBase, MarketingUserDocument
   
   class DocumentProcessor:
       def __init__(self, db, embedding_service: EmbeddingService):
           self.db = db
           self.embedding_service = embedding_service
           self.splitter = RecursiveCharacterTextSplitter(
               chunk_size=1000,
               chunk_overlap=200,
               length_function=len,
           )
       
       async def process_document(
           self,
           document_id: UUID,
           file_path: Path,
           file_type: str,
           chat_id: UUID,
           project_id: UUID,
           source_title: str
       ):
           """
           Procesar documento: parsear, chunking, embeddings, guardar en DB.
           
           Pasos:
           1. Parsear documento según tipo
           2. Hacer chunking (1000 tokens, overlap 200)
           3. Generar embeddings con OpenAI
           4. Guardar chunks en marketing_knowledge_base con:
              - project_id = usuario.project_id
              - chat_id = chat_id actual
              - content_type = 'user_document'
           5. Actualizar marketing_user_documents (processed=True, chunks_count)
           """
           # 1. Parsear
           text = await parse_document(file_path, file_type)
           
           if not text.strip():
               raise ValueError("Document is empty or could not be parsed")
           
           # 2. Chunking
           chunks = self.splitter.split_text(text)
           
           # 3. Generar embeddings
           embeddings = await self.embedding_service.generate_embeddings_batch(chunks)
           
           # 4. Guardar en knowledge_base
           for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
               kb_entry = MarketingKnowledgeBase(
                   project_id=project_id,
                   chat_id=chat_id,
                   content_type='user_document',
                   source_title=source_title,
                   chunk_text=chunk,
                   chunk_index=i,
                   metadata={
                       'document_id': str(document_id),
                       'file_type': file_type,
                       'total_chunks': len(chunks),
                   },
                   embedding=embedding
               )
               self.db.add(kb_entry)
           
           # 5. Actualizar metadata del documento
           doc = await self.db.get(MarketingUserDocument, document_id)
           doc.processed = True
           doc.chunks_count = len(chunks)
           
           await self.db.commit()
           
           return {
               'chunks_count': len(chunks),
               'success': True
           }
   ```

5. **Implementar endpoints de documentos:**
   
   **`backend/src/api/documents.py`:**
   ```python
   from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
   from pathlib import Path
   from uuid import UUID, uuid4
   import os
   from ..schemas.documents import *
   from ..services.document_processor import DocumentProcessor
   from ..middleware.auth import get_current_user
   
   router = APIRouter(prefix="/api/chats/{chat_id}/documents", tags=["documents"])
   
   STORAGE_PATH = Path("backend/storage/documents")
   STORAGE_PATH.mkdir(parents=True, exist_ok=True)
   
   @router.post("/upload", response_model=UploadDocumentResponse)
   async def upload_document(
       chat_id: UUID,
       file: UploadFile = File(...),
       background_tasks: BackgroundTasks,
       current_user: dict = Depends(get_current_user)
   ):
       """
       Subir documento y procesarlo en background.
       
       Validaciones:
       - Tipo de archivo: .txt, .pdf, .docx
       - Tamaño máximo: 10MB
       - Sanitización de nombre de archivo
       """
       # 1. Validaciones
       file_type = Path(file.filename).suffix.lower()
       if file_type not in ALLOWED_FILE_TYPES:
           raise HTTPException(400, f"File type not allowed. Allowed: {ALLOWED_FILE_TYPES}")
       
       file_size = 0
       content = bytearray()
       async for chunk in file.stream():
           file_size += len(chunk)
           if file_size > MAX_FILE_SIZE:
               raise HTTPException(400, f"File too large. Max: {MAX_FILE_SIZE / 1024 / 1024}MB")
           content.extend(chunk)
       
       # 2. Sanitizar nombre
       safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ")
       
       # 3. Guardar en storage
       document_id = uuid4()
       file_path = STORAGE_PATH / str(current_user['project_id']) / str(chat_id) / f"{document_id}{file_type}"
       file_path.parent.mkdir(parents=True, exist_ok=True)
       
       with open(file_path, 'wb') as f:
           f.write(content)
       
       # 4. Crear entrada en DB
       doc = MarketingUserDocument(
           id=document_id,
           chat_id=chat_id,
           project_id=current_user['project_id'],
           user_id=current_user['user_id'],
           filename=safe_filename,
           file_type=file_type,
           file_size=file_size,
           file_path=str(file_path),
           processed=False
       )
       db.add(doc)
       await db.commit()
       
       # 5. Procesar en background
       background_tasks.add_task(
           document_processor.process_document,
           document_id, file_path, file_type, chat_id,
           current_user['project_id'], safe_filename
       )
       
       return UploadDocumentResponse.model_validate(doc)
   
   @router.get("/", response_model=ListDocumentsResponse)
   async def list_documents(
       chat_id: UUID,
       current_user: dict = Depends(get_current_user)
   ):
       """Listar documentos subidos en este chat."""
       query = select(MarketingUserDocument).where(
           MarketingUserDocument.chat_id == chat_id,
           MarketingUserDocument.project_id == current_user['project_id']
       ).order_by(MarketingUserDocument.created_at.desc())
       
       result = await db.execute(query)
       docs = result.scalars().all()
       
       return ListDocumentsResponse(
           documents=[DocumentMetadata.model_validate(d) for d in docs],
           total=len(docs)
       )
   
   @router.delete("/{document_id}")
   async def delete_document(
       chat_id: UUID,
       document_id: UUID,
       current_user: dict = Depends(get_current_user)
   ):
       """
       Eliminar documento y sus chunks.
       
       Pasos:
       1. Eliminar chunks de marketing_knowledge_base
       2. Eliminar metadata de marketing_user_documents
       3. Eliminar archivo físico
       """
       # 1. Obtener documento
       doc = await db.get(MarketingUserDocument, document_id)
       if not doc or doc.project_id != current_user['project_id']:
           raise HTTPException(404, "Document not found")
       
       # 2. Eliminar chunks
       await db.execute(
           delete(MarketingKnowledgeBase).where(
               MarketingKnowledgeBase.project_id == current_user['project_id'],
               MarketingKnowledgeBase.chat_id == chat_id,
               MarketingKnowledgeBase.metadata['document_id'].astext == str(document_id)
           )
       )
       
       # 3. Eliminar metadata
       await db.delete(doc)
       await db.commit()
       
       # 4. Eliminar archivo físico
       try:
           Path(doc.file_path).unlink()
       except FileNotFoundError:
           pass  # Archivo ya no existe
       
       return {"success": True}
   ```

6. **Registrar router en main.py:**
   ```python
   from .api import auth, chat, documents
   
   app.include_router(auth.router)
   app.include_router(chat.router)
   app.include_router(documents.router)
   ```

**Criterios de aceptación:**
- [ ] Parsers implementados para .txt, .pdf, .docx
- [ ] DocumentProcessor hace chunking correcto (1000 tokens, overlap 200)
- [ ] Embeddings generados correctamente con OpenAI
- [ ] Chunks guardados en `marketing_knowledge_base` con `project_id` y `chat_id`
- [ ] Metadata en `marketing_user_documents` actualizada
- [ ] Endpoints funcionan:
  - [ ] POST /api/chats/{id}/documents/upload
  - [ ] GET /api/chats/{id}/documents
  - [ ] DELETE /api/chats/{id}/documents/{doc_id}
- [ ] Validaciones funcionan (tipo, tamaño)
- [ ] Procesamiento en background no bloquea respuesta
- [ ] Tests:
  - [ ] Subir archivo .txt y verificar chunks en DB
  - [ ] Subir archivo .pdf y verificar extracción
  - [ ] Subir archivo .docx y verificar extracción
  - [ ] Buscar chunks del documento en vector store
  - [ ] Eliminar documento y verificar cleanup completo

**Archivos a crear:**
- `backend/src/schemas/documents.py`
- `backend/src/utils/file_parsers.py`
- `backend/src/services/document_processor.py`
- `backend/src/api/documents.py`
- `backend/tests/test_documents.py`

**Comandos de validación:**
```bash
# Tests
pytest backend/tests/test_documents.py -v

# Test manual (con archivo test.txt)
curl -X POST http://localhost:8000/api/chats/<chat_id>/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.txt"

# Verificar chunks en DB
psql $DATABASE_URL -c "SELECT COUNT(*) FROM marketing_knowledge_base WHERE content_type='user_document' AND chat_id='<chat_id>';"
```

---

### TAREA 4: Agente IA con Memoria (NÚCLEO DEL SISTEMA)

**Herramientas a utilizar:**
- ⚡ MCP Archon: LangChain + Memoria + Agentes
  - Comando: `rag_search_knowledge_base(query="langchain agent memory conversation", source_id="e74f94bb9dcb14aa", match_count=8)`
  - Comando: `rag_search_knowledge_base(query="langgraph stateful agent", source_id="e74f94bb9dcb14aa", match_count=5)`
  - Comando: `rag_search_code_examples(query="langchain tools custom", source_id="e74f94bb9dcb14aa", match_count=5)`

- 🔧 MCP Serena: Analizar patrón de agente de ejemplo
  - Comando: `find_symbol('research_agent', 'Context-Engineering-Intro/examples/main_agent_reference/research_agent.py', True)`
  - Comando: `find_symbol('ResearchAgentDependencies', 'Context-Engineering-Intro/examples/main_agent_reference/research_agent.py', True)`

- 📚 Skills:
  - **agent-memory-systems** (diseño de sistema de memoria multi-nivel)
  - **autonomous-agents** (patrones de agentes autónomos y orquestación)
  - **rag-implementation** (chunking, embeddings, búsqueda semántica)
  - **prompt-engineering** (técnicas avanzadas de prompting para agentes)
  - **ai-agents-architect** (arquitectura de sistemas multi-agente)
  - **context-window-management** (gestión eficiente de contexto LLM)
  - **llm-app-patterns** (patrones de producción para apps LLM)
  - python-patterns (automático)
  - clean-code (automático)
  - brainstorming (ANTES de implementar - OBLIGATORIO)

**⚠️ IMPORTANTE: Esta tarea es el NÚCLEO del sistema. El agente NO genera contenido automáticamente. Solo genera cuando el usuario lo solicita explícitamente.**

**Objetivo:**
Implementar el sistema de agentes IA con 3 tipos de memoria (short-term, long-term, semantic) que:
1. Genera análisis completo de buyer persona
2. Procesa documentos subidos por el usuario
3. Extrae insights
4. ENTREGA documento completo
5. ESPERA peticiones del usuario
6. Genera contenido SOLO cuando se le pide

**📋 DISEÑO VALIDADO:** 
Este task implementa las decisiones documentadas en: `docs/plans/2026-01-27-agentes-memoria-design.md`

**Decisiones clave aplicadas:**
- ✅ **DECISIÓN 1:** LangGraph (state machine) para Router Agent
- ✅ **DECISIÓN 2:** MemoryManager centralizado (combina 3 tipos de memoria)
- ✅ **DECISIÓN 3:** Rule-based routing (sin LLM extra, más rápido)
- ✅ **DECISIÓN 4:** LLM configurable (OpenAI/OpenRouter vía variable de entorno)
- ✅ **DECISIÓN 5:** Implementación incremental (Fase 1: Router + Buyer Persona)
- ✅ **DECISIÓN 6:** Búsqueda semántica simple (mejorar en TAREA 5)
- ✅ **DECISIÓN 7:** Retry con exponential backoff (manejo robusto de errores)
- ✅ **DECISIÓN 8:** Prompt único con plantilla completa (40+ preguntas, NO saltarse ninguna)

**Archivos a crear en esta TAREA:**
```
backend/src/agents/
├── base_agent.py              # Clase base compartida
├── router_agent.py            # Orquestador (LangGraph state machine)
└── buyer_persona_agent.py     # Genera buyer persona (40+ preguntas)

backend/src/services/
├── memory_manager.py          # MemoryManager centralizado
├── llm_service.py             # LLM configurable (OpenAI/OpenRouter)
└── rag_service.py             # Búsqueda semántica simple
```

**Pasos a seguir:**

1. **[OBLIGATORIO] Ejecutar Skill brainstorming ANTES de implementar:**
   ```
   @.cursor/skills/brainstorming/SKILL.md explorar diseño de sistema de agentes
   ```
   - ✅ **COMPLETADO**: Ver `docs/plans/2026-01-27-agentes-memoria-design.md`
   - ✅ Arquitectura: LangGraph seleccionado
   - ✅ Memoria: MemoryManager centralizado
   - ✅ LLM: Configurable (OpenAI/OpenRouter)

2. **Consultar Archon sobre agentes y memoria:**
   - Ejecutar comandos listados arriba
   - Leer sobre ConversationBufferWindowMemory
   - Estudiar ReAct agent pattern

3. **Analizar patrón de agente de ejemplo con Serena:**
   ```python
   # Ver estructura de research_agent.py
   get_symbols_overview('Context-Engineering-Intro/examples/main_agent_reference/research_agent.py')
   
   # Leer implementación completa
   find_symbol('research_agent', '...', include_body=True)
   ```

4. **Implementar servicios base:**
   
   **`backend/src/services/llm_service.py`:**
   ```python
   from anthropic import AsyncAnthropic
   from typing import AsyncIterator
   
   class LLMService:
       def __init__(self, api_key: str):
           self.client = AsyncAnthropic(api_key=api_key)
           self.model = "claude-3-5-sonnet-20241022"
       
       async def generate(self, prompt: str, system: str = "") -> str:
           """Generación síncrona (para análisis)."""
           response = await self.client.messages.create(
               model=self.model,
               max_tokens=4096,
               system=system,
               messages=[{"role": "user", "content": prompt}]
           )
           return response.content[0].text
       
       async def stream(self, prompt: str, system: str = "") -> AsyncIterator[str]:
           """Streaming (para chat en tiempo real)."""
           async with self.client.messages.stream(
               model=self.model,
               max_tokens=4096,
               system=system,
               messages=[{"role": "user", "content": prompt}]
           ) as stream:
               async for text in stream.text_stream:
                   yield text
   ```
   
   **`backend/src/services/embedding_service.py`:**
   ```python
   from openai import AsyncOpenAI
   from typing import List
   import asyncio
   
   class EmbeddingService:
       def __init__(self, api_key: str):
           self.client = AsyncOpenAI(api_key=api_key)
           self.model = "text-embedding-3-large"
           self.dimension = 1536
       
       async def generate_embedding(self, text: str) -> List[float]:
           """Generar embedding para un texto."""
           response = await self.client.embeddings.create(
               model=self.model,
               input=text
           )
           return response.data[0].embedding
       
       async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
           """
           ⚠️ GOTCHA CRÍTICO APLICADO:
           **GOTCHA 5 - OpenAI Rate Limits**
           
           Problema: OpenAI tier free tiene límite de 3000 RPM (requests per minute).
           Si procesas 5000 chunks con requests individuales → rate limit error.
           
           Solución implementada:
           - Batch de 50 textos por request (reduce 5000 requests a 100)
           - Exponential backoff si hay rate limit (espera 2^n segundos)
           - Pequeña pausa entre batches (0.5s) para evitar burst
           
           Resultado: 5000 chunks procesados en ~2 minutos sin errores vs timeout instantáneo
           """
           batch_size = 50  # ✅ OpenAI permite hasta 2048 inputs por request
           results = []
           max_retries = 5
           
           for i in range(0, len(texts), batch_size):
               batch = texts[i:i+batch_size]
               retry_count = 0
               
               while retry_count < max_retries:
                   try:
                       response = await self.client.embeddings.create(
                           model=self.model,
                           input=batch
                       )
                       results.extend([e.embedding for e in response.data])
                       break  # Éxito, salir del retry loop
                       
                   except Exception as e:
                       if "rate_limit" in str(e).lower():
                           wait_time = 2 ** retry_count  # Exponential backoff
                           print(f"⚠️ Rate limit. Retry {retry_count+1}/{max_retries} en {wait_time}s")
                           await asyncio.sleep(wait_time)
                           retry_count += 1
                           
                           if retry_count == max_retries:
                               raise Exception(f"Max retries alcanzado para batch {i//batch_size + 1}")
                       else:
                           raise
               
               # Pequeña pausa entre batches para evitar burst
               await asyncio.sleep(0.5)
           
           return results
   ```
   
   **`backend/src/services/vector_search.py`:**
   ```python
   from typing import List, Dict, Optional
   from uuid import UUID
   
   class VectorSearchService:
       def __init__(self, db):
           self.db = db
       
       async def search(
           self,
           query_embedding: List[float],
           project_id: UUID,
           chat_id: Optional[UUID] = None,
           match_threshold: float = 0.7,
           match_count: int = 10
       ) -> List[Dict]:
           """
           Buscar documentos similares usando función de Supabase.
           
           Busca en:
           - Conocimiento global (project_id NULL, chat_id NULL)
           - Documentos del usuario (project_id, chat_id específicos)
           """
           query = f"""
           SELECT * FROM marketing_match_documents(
               ARRAY{query_embedding}::vector,
               {match_threshold},
               {match_count},
               '{project_id}'::uuid,
               {f"'{chat_id}'::uuid" if chat_id else 'NULL'}
           )
           """
           result = await self.db.execute(query)
           return [dict(row) for row in result]
   ```

5. **Implementar Memory Manager:**
   
   **⚠️ GOTCHA CRÍTICO APLICADO:**
   **GOTCHA 2 - LangChain ConversationBufferMemory crece indefinidamente**
   
   Problema: `ConversationBufferMemory` sin límite guarda TODOS los mensajes.
   - Después de 100+ mensajes: miles de tokens por request
   - Latencia alta (prompt enorme)
   - Costo $$$
   - Puede exceder límite de contexto
   
   Solución implementada:
   - Usar `ConversationBufferWindowMemory(k=10)` con límite explícito
   - Solo mantiene últimos 10 turnos de conversación
   - Guardar todos los mensajes en DB (long-term) pero solo cargar últimos 10
   
   **`backend/src/agents/memory_manager.py`:**
   ```python
   from langchain.memory import ConversationBufferWindowMemory  # ✅ Window, NO Buffer
   from typing import Dict, List, Optional
   from uuid import UUID
   
   class AgentMemoryManager:
       """
       Gestiona 3 tipos de memoria:
       1. Short-term: Ventana de conversación (últimas 10 interacciones) ← GOTCHA 2
       2. Long-term: Buyer persona + Customer Journey en DB
       3. Semantic: Embeddings para búsqueda vectorial
       """
       def __init__(self, db, embedding_service, vector_search):
           self.db = db
           self.embedding_service = embedding_service
           self.vector_search = vector_search
           
           # ✅ CORRECTO: ConversationBufferWindowMemory con límite k=10
           self.short_term = ConversationBufferWindowMemory(
               k=10,  # Solo últimos 10 turnos (user + assistant = 1 turno)
               return_messages=True,
               memory_key="chat_history"
           )
           
           # ❌ INCORRECTO: ConversationBufferMemory sin límite
           # from langchain.memory import ConversationBufferMemory
           # self.short_term = ConversationBufferMemory()  # ← Crece indefinidamente!
           
           # Short-term memory (por chat_id)
           self.short_term_memories = {}
       
       def get_short_term_memory(self, chat_id: UUID) -> ConversationBufferWindowMemory:
           """
           Obtener memoria de ventana para un chat.
           
           GOTCHA: ConversationBufferMemory crece indefinidamente.
           Solución: Usar BufferWindowMemory con k=10.
           """
           if chat_id not in self.short_term_memories:
               self.short_term_memories[chat_id] = ConversationBufferWindowMemory(
                   k=10,
                   return_messages=True,
                   memory_key="chat_history"
               )
           return self.short_term_memories[chat_id]
       
       async def get_long_term_context(self, chat_id: UUID, project_id: UUID) -> Dict:
           """
           Recuperar contexto de largo plazo desde DB.
           
           Retorna:
           - buyer_persona: Análisis completo
           - customer_journey: 3 fases
           - documents_uploaded: Lista de documentos del usuario
           """
           # Buscar buyer persona
           query = select(MarketingBuyerPersona).where(
               MarketingBuyerPersona.chat_id == chat_id,
               MarketingBuyerPersona.project_id == project_id
           )
           result = await self.db.execute(query)
           buyer_persona = result.scalar_one_or_none()
           
           # Buscar documentos subidos
           query = select(MarketingUserDocument).where(
               MarketingUserDocument.chat_id == chat_id,
               MarketingUserDocument.project_id == project_id,
               MarketingUserDocument.processed == True
           )
           result = await self.db.execute(query)
           documents = result.scalars().all()
           
           return {
               'buyer_persona': buyer_persona.full_analysis if buyer_persona else None,
               'customer_journey': buyer_persona.customer_journey if buyer_persona else None,
               'pain_points': buyer_persona.pain_points if buyer_persona else None,
               'documents_uploaded': [{'id': str(d.id), 'filename': d.filename} for d in documents]
           }
       
       async def get_semantic_context(
           self,
           query: str,
           project_id: UUID,
           chat_id: UUID,
           k: int = 10
       ) -> List[Dict]:
           """
           Búsqueda semántica en knowledge_base.
           
           Busca en:
           1. Documentos del usuario (chat_id específico)
           2. Conocimiento global (YouTubers + libros)
           """
           # Generar embedding del query
           query_embedding = await self.embedding_service.generate_embedding(query)
           
           # Buscar en vector store
           results = await self.vector_search.search(
               query_embedding=query_embedding,
               project_id=project_id,
               chat_id=chat_id,
               match_count=k
           )
           
           return results
       
       async def save_to_long_term(
           self,
           chat_id: UUID,
           project_id: UUID,
           data: Dict
       ):
           """
           Guardar análisis en memoria de largo plazo.
           
           También genera embedding del análisis completo.
           """
           # Generar embedding del análisis
           full_text = str(data.get('full_analysis', ''))
           embedding = await self.embedding_service.generate_embedding(full_text)
           
           # Guardar en DB
           buyer_persona = MarketingBuyerPersona(
               chat_id=chat_id,
               project_id=project_id,
               initial_questions=data['initial_questions'],
               full_analysis=data['full_analysis'],
               forum_simulation=data['forum_simulation'],
               pain_points=data['pain_points'],
               customer_journey=data['customer_journey'],
               embedding=embedding
           )
           self.db.add(buyer_persona)
           await self.db.commit()
   ```

6. **Implementar agentes especializados:**
   
   **`backend/src/agents/buyer_persona_agent.py`:**
   ```python
   from typing import Dict, List
   from uuid import UUID
   
   # CRÍTICO: Cargar plantilla desde archivo real del proyecto
   # Ubicación: contenido/buyer-plantilla.md
   
   BUYER_PERSONA_TEMPLATE = """
   Eres un experto en marketing digital con amplios conocimientos en mercadología.
   
   CONTEXTO DE TU TAREA:
   Estás desarrollando un buyer persona detallado para una campaña publicitaria en ADS 
   y un plan de contenidos orgánico.
   
   INFORMACIÓN DEL NEGOCIO:
   - Empresa ofrece: {business_offering}
   - Público objetivo: {target_audience}
   - Tipo de negocio: {business_type}  # B2B o B2P
   
   DOCUMENTOS ADICIONALES DEL USUARIO:
   {context_from_documents}
   
   TU MISIÓN:
   Desarrollar un buyer persona completo respondiendo a las preguntas de la plantilla base.
   
   IMPORTANTE:
   - Responde TODAS las preguntas de manera completa y eficiente
   - Los datos se usarán para campañas en Meta ADS y estrategia de content marketing
   - Las respuestas deben basarse en la REALIDAD del público (no manipular para favorecer al negocio)
   - Con datos reales podremos dar soluciones reales
   - Establece un paso a paso: analiza primero, luego enfócate en necesidades reales
   
   PLANTILLA A COMPLETAR (11 categorías, ~40 preguntas):
   
   ## 1. ASPECTOS DEMOGRÁFICOS
   1. ¿Cuál es su nombre y edad?
   2. ¿Qué estudios tiene?
   3. ¿Cuánto cobra bruto al año?
   4. ¿En dónde vive?
   5. ¿Cuál es su estado civil?
   
   ## 2. HOGAR Y FAMILIA
   1. ¿Quiénes son los integrantes de su unidad familiar?
   2. ¿Cuáles son sus principales actividades de ocio?
   3. ¿Cuáles son sus principales responsabilidades en el hogar?
   
   ## 3. TRABAJO
   1. ¿Dónde trabaja y qué cargo tiene?
   2. ¿Cuáles son sus retos laborales?
   3. ¿Cómo influye su vida laboral en la personal y viceversa?
   
   ## 4. COMPORTAMIENTO
   1. ¿Cómo es la relación con su pareja, familia y amigos?
   2. ¿Qué expresiones y lenguaje utiliza su grupo social?
   
   ## 5. PROBLEMA
   1. ¿Qué problema o dolor activa la búsqueda de una solución?
   2. ¿Cómo tu producto o servicio soluciona ese problema o dolor?
   
   ## 6. BÚSQUEDA DE LA SOLUCIÓN
   1. ¿Dónde busca soluciones a su problema o dolor?
   2. ¿Cómo encuentra tu empresa?
   3. ¿Cómo reacciona ante las propuestas comerciales?
   
   ## 7. OBJECIONES Y BARRERAS
   1. ¿Cuáles son las barreras internas o externas por las que no compra?
   2. ¿Cuáles son las alternativas o excusas que utiliza para no comprar?
   
   ## 8. MIEDOS E INSEGURIDADES
   1. ¿Qué odia encontrar cuando busca información sobre el producto?
   2. ¿Qué experiencias negativas ha tenido hasta la fecha?
   
   ## 9. COMPARACIÓN CON LA COMPETENCIA
   1. ¿Qué factores compara antes de la contratación o compra?
   2. ¿Cuáles son las diferencias de tu producto con la competencia?
   3. ¿En qué es mejor tu producto o servicio?
   4. ¿En qué es peor?
   5. ¿Por qué elige tu producto o servicio?
   
   ## 10. TU PRODUCTO O SERVICIO
   1. ¿Qué prestaciones o beneficios son percibidos sobre tu producto?
   2. ¿Qué prestaciones o beneficios NO son percibidos?
   3. ¿Cuáles son los productos o servicios complementarios?
   4. ¿Cuáles son las dudas y quejas más habituales de postventa?
   
   EJEMPLO DE REFERENCIA (NO COPIAR, SOLO GUÍA DE FORMATO):
   Ver: contenido/buyer-plantilla.md - Caso de "Ana" (enfermera)
   
   FORMATO DE SALIDA:
   Responde en JSON estructurado con todas las categorías y respuestas completas.
   """
   
   FORUM_SIMULATION_PROMPT = """
   Basándote en el buyer persona que acabas de crear, ahora TOMA EL PAPEL de esa persona.
   
   ESCENARIO:
   Estás en un foro de internet donde las personas se reúnen a quejarse o recomendar 
   este tipo de servicios.
   
   TU TAREA:
   1. Comienza a quejarte de los problemas que tienen las personas al contratar servicios similares
   2. Después de cada queja, da una solución o lo que te gustaría que ocurriese
   
   FORMATO:
   {
     "forum_posts": [
       {
         "queja": "descripción de la queja específica",
         "solucion_deseada": "lo que me gustaría que pasara"
       },
       // ... 5-7 posts
     ],
     "pain_points": [
       "punto de dolor 1",
       "punto de dolor 2",
       // ... total 10 puntos
     ]
   }
   
   LUEGO: Dame una lista de 10 PUNTOS DE DOLOR de ese personaje (buyer persona):
   - Todo lo que piensa y siente ANTES de realizar la compra
   - Criterios que evalúa
   - Comportamientos que tiene
   
   IMPORTANTE: Sé específico y realista. Usa el lenguaje del buyer persona.
   """
   
   CUSTOMER_JOURNEY_PROMPT = """
   Actúa como un experto en content marketing.
   
   CONTEXTO:
   Basándote en:
   - El buyer persona completo
   - Su papel en el foro (quejas y puntos de dolor)
   
   TU TAREA:
   Crear el Customer Journey para la estrategia de contenidos con las 3 fases de conciencia EXTENDIDAS.
   
   DEFINICIONES:
   
   1. CONCIENCIA:
      - Todo lo que el cliente hace hasta tomar conciencia de su necesidad
      - Investigando opciones SIN intención comercial
      - Preguntas: "¿Qué síntomas tengo?", "¿Por qué me pasa esto?"
   
   2. CONSIDERACIÓN:
      - Tiene 2-3 opciones identificadas
      - Investigación en profundidad de cada opción
      - PUEDE tener algún interés comercial
      - Preguntas: "¿Cuál es mejor?", "¿Qué diferencias hay?"
   
   3. COMPRA:
      - El cliente decide comprar
      - Basado en sus investigaciones previas
      - Preguntas: "¿Dónde compro?", "¿Cuándo es el mejor momento?"
   
   FORMATO DE SALIDA:
   {
     "awareness": {
       "mindset": "descripción de mentalidad en esta fase",
       "content_types": ["tipo 1", "tipo 2", ...],
       "busquedas_google": [
         "búsqueda 1", "búsqueda 2", ...
         // mínimo 10, ideal 20
       ],
       "preguntas_cabeza": [
         "pregunta 1", "pregunta 2", ...
         // mínimo 10, ideal 20
       ]
     },
     "consideration": {
       // misma estructura
     },
     "purchase": {
       // misma estructura
     }
   }
   
   IMPORTANTE:
   - Dame un MÍNIMO de 10 preguntas por cada fase (ideal 20)
   - Divide en: qué busca en internet + qué pasa por su cabeza
   - Sé EXTENSO y conoce muy bien a quien le daremos este contenido
   - Usa el conocimiento del buyer persona + foro para ser específico
   """
   
   class BuyerPersonaAgent:
       def __init__(self, llm_service, memory_manager):
           self.llm = llm_service
           self.memory = memory_manager
       
       async def generate_analysis(
           self,
           chat_id: UUID,
           project_id: UUID,
           initial_questions: Dict,
           use_documents: bool = True
       ) -> Dict:
           """
           Generar análisis completo de buyer persona.
           
           Pasos:
           1. Buscar en documentos del usuario si existen
           2. Crear prompt con plantilla + contexto
           3. Generar análisis con Claude
           4. Estructurar respuesta
           """
           # 1. Buscar contexto en documentos del usuario
           context_from_docs = ""
           if use_documents:
               docs_context = await self.memory.get_semantic_context(
                   query="información del negocio empresa productos servicios",
                   project_id=project_id,
                   chat_id=chat_id,
                   k=5
               )
               if docs_context:
                   context_from_docs = "\n\nINFORMACIÓN EXTRAÍDA DE DOCUMENTOS:\n" + \
                       "\n".join([f"- {d['content'][:500]}..." for d in docs_context])
           
           # 2. Crear prompt
           prompt = f"""
           RESPUESTAS INICIALES DEL USUARIO:
           1. Negocio: {initial_questions.get('q1_business')}
           2. Cliente ideal: {initial_questions.get('q2_ideal_customer')}
           3. Problema principal: {initial_questions.get('q3_main_problem')}
           4. Resultado deseado: {initial_questions.get('q4_desired_outcome')}
           5. Competencia: {initial_questions.get('q5_competition')}
           
           {context_from_docs}
           
           Con esta información, completa el análisis de buyer persona usando la plantilla.
           Responde en formato JSON estructurado.
           """
           
           # 3. Generar análisis
           response = await self.llm.generate(
               prompt=prompt,
               system=BUYER_PERSONA_TEMPLATE.format(context_from_documents=context_from_docs)
           )
           
           # 4. Parsear y retornar (asumiendo respuesta JSON)
           import json
           full_analysis = json.loads(response)
           
           return full_analysis
   ```
   
   **(Continúa con ForumSimulatorAgent, PainPointsAgent, CustomerJourneyAgent, ContentGeneratorAgent siguiendo patrones similares...)**

7. **Implementar Router Agent (orquestador):**
   
   **`backend/src/agents/router_agent.py`:**
   - Usar código de sección "Arquitectura de Agentes" del PRP
   - Implementar detección de estado
   - Implementar detección de petición de contenido
   - Orquestar flujo completo

**Criterios de aceptación:**
- [ ] LLMService implementado (generate + stream)
- [ ] EmbeddingService con batch processing y rate limiting
- [ ] VectorSearchService usando función de Supabase
- [ ] Memory Manager con 3 tipos de memoria
- [ ] BuyerPersonaAgent genera análisis completo (puede usar docs del usuario)
- [ ] ForumSimulatorAgent simula foro
- [ ] PainPointsAgent extrae 10 puntos
- [ ] CustomerJourneyAgent genera 3 fases × 20 preguntas
- [ ] ContentGeneratorAgent genera SOLO cuando se le pide
- [ ] RouterAgent orquesta flujo correcto
- [ ] Tests >80% coverage
- [ ] Agente ENTREGA análisis y ESPERA (no genera automáticamente)
- [ ] Sistema de memoria funcional
- [ ] Búsqueda semántica incluye documentos del usuario

**Archivos a crear:**
- `backend/src/services/llm_service.py`
- `backend/src/services/embedding_service.py`
- `backend/src/services/vector_search.py`
- `backend/src/agents/memory_manager.py`
- `backend/src/agents/buyer_persona_agent.py`
- `backend/src/agents/forum_simulator_agent.py`
- `backend/src/agents/pain_points_agent.py`
- `backend/src/agents/customer_journey_agent.py`
- `backend/src/agents/content_generator_agent.py`
- `backend/src/agents/router_agent.py`
- `backend/tests/test_agents.py`
- `backend/tests/test_memory.py`

**Comandos de validación:**
```bash
# Tests unitarios de agentes
pytest backend/tests/test_agents.py -v

# Tests de memoria
pytest backend/tests/test_memory.py -v

# Test de integración end-to-end
pytest backend/tests/integration/test_full_flow.py -v

# Verificar que agente usa documentos del usuario
# (crear chat, subir documento, generar buyer persona, verificar que usa info del doc)
```

---

### TAREA 5: Entrenamiento del Agente con Material de YouTube

**Herramientas a utilizar:**
- ⚡ MCP Archon: Chunking strategies y document processing
  - Comando: `rag_search_knowledge_base(query="document chunking embedding strategies", match_count=5)`
  - Comando: `rag_search_code_examples(query="python pdf text extraction", match_count=3)`

- 🔧 MCP Serena: Analizar estructura de scripts existentes
  - Comando: `find_file('ingest', 'backend/scripts/')`

- 📚 Skills:
  - **rag-implementation** (estrategias de chunking y embedding)
  - **context-window-management** (optimización de tokens)
  - python-patterns (automático)
  - clean-code (automático)

**Objetivo:**
Procesar las 9 transcripciones de YouTube de Andrea Estratega y cargarlas en `marketing_knowledge_base` como conocimiento global (project_id=NULL, chat_id=NULL) para que el ContentGeneratorAgent pueda usar estas técnicas al generar contenido.

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 5 - OpenAI Rate Limits**: Ya implementado en EmbeddingService.generate_embeddings_batch() de TAREA 4.

**📋 MEJORAS DE DISEÑO (desde TAREA 4):**
Esta tarea implementa mejoras documentadas en: `docs/plans/2026-01-27-agentes-memoria-design.md`

**Decisión aplicada:**
- ✅ **DECISIÓN 6:** Migración de búsqueda semántica simple → híbrida con reranking
  - **TAREA 4:** Implementó búsqueda vectorial simple (suficiente para MVP)
  - **TAREA 5:** Agregar filtrado por metadata + reranking con LLM
  - **Beneficios:** Mejor precisión, considera tipo de documento, reranking mejora relevancia

**Mejoras a implementar en `backend/src/services/rag_service.py`:**
```python
async def search_relevant_docs(
    chat_id: UUID,
    query: str,
    limit: int = 5,
    rerank: bool = True,
    metadata_filters: dict = None
) -> List[dict]:
    # 1. Búsqueda vectorial (traer 3x resultados para reranking)
    initial_results = await self._vector_search(query, limit * 3)
    
    # 2. Filtrar por metadata (tipo, fecha, fuente)
    filtered = self._filter_by_metadata(initial_results, metadata_filters)
    
    # 3. Reranking con LLM (opcional, mejora relevancia)
    if rerank:
        reranked = await self._rerank_with_llm(query, filtered)
        return reranked[:limit]
    
    return filtered[:limit]
```

**Pasos a seguir:**

1. **Consultar Archon sobre estrategias de chunking:**
   - Ejecutar comandos listados arriba
   - Decidir tamaño de chunk (recomendado: 500-1000 tokens con overlap de 100)

2. **Crear script de ingesta de datos:**
   
   **`backend/scripts/ingest_training_data.py`:**
   ```python
   import asyncio
   import os
   from pathlib import Path
   from typing import List, Dict
   from uuid import UUID
   import sys
   
   # Añadir src al path
   sys.path.append(str(Path(__file__).parent.parent / 'src'))
   
   from services.embedding_service import EmbeddingService
   from db.database import get_db_connection
   
   CHUNK_SIZE = 800  # tokens (~3000 caracteres)
   CHUNK_OVERLAP = 100  # tokens
   
   def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
       """Divide texto en chunks con overlap."""
       words = text.split()
       chunks = []
       
       for i in range(0, len(words), chunk_size - overlap):
           chunk = ' '.join(words[i:i + chunk_size])
           if chunk:
               chunks.append(chunk)
       
       return chunks
   
   async def ingest_youtube_transcripts(source_dir: str):
       """Procesa transcripciones de YouTube y las sube a knowledge_base."""
       
       # 1. Inicializar servicios
       embedding_service = EmbeddingService(api_key=os.getenv('OPENAI_API_KEY'))
       db = await get_db_connection()
       
       # 2. Cargar archivos .txt
       transcript_dir = Path(source_dir)
       transcript_files = list(transcript_dir.glob('*.txt'))
       
       print(f"📁 Encontrados {len(transcript_files)} archivos de transcripciones")
       
       all_chunks = []
       
       # 3. Procesar cada archivo
       for file_path in transcript_files:
           with open(file_path, 'r', encoding='utf-8') as f:
               content = f.read()
           
           # Dividir en chunks
           chunks = chunk_text(content)
           
           for idx, chunk_text in enumerate(chunks):
               all_chunks.append({
                   'source_title': file_path.stem,  # Nombre del video
                   'chunk_text': chunk_text,
                   'chunk_index': idx,
                   'content_type': 'video_transcript'
               })
           
           print(f"  ✅ {file_path.name}: {len(chunks)} chunks")
       
       print(f"\n📊 Total: {len(all_chunks)} chunks a procesar")
       
       # 4. Generar embeddings en batch (GOTCHA 5 manejado aquí)
       print("\n🔄 Generando embeddings (puede tomar 2-5 minutos)...")
       texts = [chunk['chunk_text'] for chunk in all_chunks]
       embeddings = await embedding_service.generate_embeddings_batch(texts)
       
       print(f"✅ {len(embeddings)} embeddings generados")
       
       # 5. Insertar en base de datos
       print("\n💾 Insertando en marketing_knowledge_base...")
       
       for chunk, embedding in zip(all_chunks, embeddings):
           await db.execute(
               """
               INSERT INTO marketing_knowledge_base 
               (project_id, chat_id, content_type, source_title, chunk_text, chunk_index, embedding, metadata)
               VALUES (NULL, NULL, $1, $2, $3, $4, $5, $6)
               """,
               chunk['content_type'],
               chunk['source_title'],
               chunk['chunk_text'],
               chunk['chunk_index'],
               embedding,
               {'source': 'youtube', 'author': 'Andrea Estratega'}
           )
       
       print(f"✅ {len(all_chunks)} chunks insertados en knowledge_base")
       
       await db.close()
   
   if __name__ == "__main__":
       source = "contenido/Transcriptions Andrea Estratega/"
       asyncio.run(ingest_youtube_transcripts(source))
   ```

3. **Ejecutar script de ingesta:**
   ```bash
   cd backend
   python scripts/ingest_training_data.py
   ```
   
   Esperado:
   ```
   📁 Encontrados 9 archivos de transcripciones
     ✅ 6 Carruseles en Instagram que te harán viral en 2025 (y su estructura).txt: 45 chunks
     ✅ Cómo hacer 7 guiones virales en menos de 30 min CON UNA ESTRUCTURA copia y pega.txt: 38 chunks
     ... (7 más)
   
   📊 Total: ~300-400 chunks a procesar
   
   🔄 Generando embeddings (puede tomar 2-5 minutos)...
   ✅ Batch 1: 50 embeddings
   ✅ Batch 2: 50 embeddings
   ... (6-8 batches más)
   ✅ 350 embeddings generados
   
   💾 Insertando en marketing_knowledge_base...
   ✅ 350 chunks insertados
   ```

4. **Verificar que datos están en la base:**
   ```sql
   -- Conectar a Supabase
   psql postgresql://postgres:b12f16dbcd20ef9b7097bea120576816@213.199.39.112:5432/postgres
   
   -- Verificar chunks insertados
   SELECT content_type, COUNT(*) 
   FROM marketing_knowledge_base 
   WHERE content_type = 'video_transcript'
   GROUP BY content_type;
   
   -- Esperado: video_transcript | 300-400
   
   -- Verificar títulos de videos
   SELECT DISTINCT source_title 
   FROM marketing_knowledge_base 
   WHERE content_type = 'video_transcript';
   
   -- Esperado: 9 títulos de videos
   ```

5. **Probar búsqueda semántica:**
   ```python
   # Test: Buscar técnicas de contenido viral
   async def test_semantic_search():
       embedding_service = EmbeddingService()
       vector_search = VectorSearchService(db)
       
       # Generar embedding de query
       query = "técnicas para crear carruseles virales en Instagram"
       query_embedding = await embedding_service.generate_embedding(query)
       
       # Buscar chunks similares
       results = await vector_search.search(
           query_embedding=query_embedding,
           project_id=None,  # Búsqueda global
           chat_id=None,
           match_threshold=0.7,
           match_count=5
       )
       
       print(f"✅ Encontrados {len(results)} chunks relevantes:")
       for r in results:
           print(f"  - {r['source_title']}: {r['similarity']:.2f}")
   ```

**Criterios de aceptación:**
- [ ] Script `ingest_training_data.py` ejecuta sin errores
- [ ] 300-400 chunks insertados en `marketing_knowledge_base`
- [ ] Todos con `project_id=NULL` y `chat_id=NULL` (conocimiento global)
- [ ] Embeddings generados sin rate limit errors
- [ ] Query SQL retorna 9 source_title distintos
- [ ] Búsqueda semántica retorna chunks relevantes con similarity >0.7
- [ ] Índice HNSW funciona correctamente (queries <100ms)

**Archivos a crear:**
- `backend/scripts/ingest_training_data.py`

---

### TAREA 6: API de Chat con Streaming (SSE)

**Herramientas a utilizar:**
- ⚡ MCP Archon: FastAPI Streaming + SSE
  - Comando: `rag_search_knowledge_base(query="fastapi streaming server sent events", source_id="c889b62860c33a44", match_count=5)`
  - Comando: `rag_search_code_examples(query="fastapi StreamingResponse async", source_id="c889b62860c33a44", match_count=3)`

- 🔧 MCP Serena: Analizar RouterAgent si existe
  - Comando: `get_symbols_overview('backend/src/agents/router_agent.py')`

- 📚 Skills:
  - **api-patterns** (diseño de APIs streaming)
  - **autonomous-agents** (orquestación de flujos multi-agente)
  - **llm-app-patterns** (streaming, RAG, y producción)
  - python-patterns (automático)
  - clean-code (automático)

**Objetivo:**
Implementar endpoint de chat que hace streaming de respuestas en tiempo real usando SSE (Server-Sent Events) y orquesta el flujo de agentes.

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 3 - FastAPI Streaming + Middleware**

Problema: Middleware que lee `request.body()` rompe streaming.
Solución: Excluir endpoints `/stream` y `/sse` del middleware de logging.

**Implementación en `backend/src/main.py`:**
```python
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # ✅ Lista de paths que usan streaming
    streaming_paths = ["/api/chat/stream", "/api/sse"]
    
    if any(path in request.url.path for path in streaming_paths):
        # ✅ NO leer body, pasar directamente
        return await call_next(request)
    
    # Para endpoints normales, procesar
    try:
        body = await request.body()
        logger.info(f"Request to {request.url.path}: {body[:100]}")
    except:
        pass
    
    response = await call_next(request)
    return response
```

**Pasos a seguir:**

1. **Modificar `main.py` con middleware que respeta streaming:**
   - Ver código arriba (GOTCHA 3)

2. **Implementar endpoint de streaming:**
   
   **`backend/src/api/chat.py`:**
   ```python
   from fastapi import APIRouter, Request, HTTPException
   from fastapi.responses import StreamingResponse
   from ..agents.router_agent import RouterAgent
   from ..schemas.chat import ChatRequest
   from uuid import UUID
   
   router = APIRouter(prefix="/api/chat", tags=["chat"])
   
   @router.post("/stream")
   async def stream_chat(request: Request, chat_request: ChatRequest):
       """
       Endpoint de chat con streaming SSE.
       
       ⚠️ GOTCHA 3: Este endpoint está EXCLUIDO del middleware de logging
       para que el streaming funcione correctamente.
       """
       # Extraer user_id y project_id del middleware (GOTCHA 6)
       user_id = request.state.user_id
       project_id = request.state.project_id
       
       # Inicializar router agent
       router_agent = RouterAgent(
           db=db,
           llm_service=llm_service,
           memory_manager=memory_manager
       )
       
       async def generate_sse():
           """Genera eventos SSE (Server-Sent Events)."""
           try:
               # Procesar mensaje con agente
               async for chunk in router_agent.process_stream(
                   chat_id=chat_request.chat_id,
                   project_id=project_id,
                   user_id=user_id,
                   message=chat_request.message
               ):
                   # Formato SSE: "data: {contenido}\n\n"
                   yield f"data: {chunk}\n\n"
               
               # Señal de fin
               yield "data: [DONE]\n\n"
               
           except Exception as e:
               # Error en streaming
               yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
       
       return StreamingResponse(
           generate_sse(),
           media_type="text/event-stream",
           headers={
               "Cache-Control": "no-cache",
               "Connection": "keep-alive",
               "X-Accel-Buffering": "no"  # Nginx buffering off
           }
       )
   
   @router.post("/message")
   async def send_message(request: Request, chat_request: ChatRequest):
       """
       Endpoint sin streaming (espera respuesta completa).
       Útil para análisis completos (buyer persona, customer journey).
       """
       user_id = request.state.user_id
       project_id = request.state.project_id
       
       router_agent = RouterAgent(db, llm_service, memory_manager)
       
       # Procesar sin streaming
       result = await router_agent.process(
           chat_id=chat_request.chat_id,
           project_id=project_id,
           user_id=user_id,
           message=chat_request.message
       )
       
       return {"response": result}
   ```

3. **Implementar RouterAgent.process_stream():**
   
   **`backend/src/agents/router_agent.py`:**
   ```python
   from typing import AsyncIterator
   
   class RouterAgent:
       # ... (código de TAREA 4)
       
       async def process_stream(
           self,
           chat_id: UUID,
           project_id: UUID,
           user_id: UUID,
           message: str
       ) -> AsyncIterator[str]:
           """
           Procesa mensaje y hace streaming de respuesta.
           
           Flujo:
           1. Detectar intención
           2. Ejecutar agente apropiado con streaming
           3. Guardar en memoria
           """
           # 1. Guardar mensaje del usuario
           await self.memory.save_to_long_term(chat_id, project_id, 'user', message)
           
           # 2. Detectar estado/intención
           state = await self.detect_state(chat_id, project_id, message)
           
           # 3. Ejecutar agente apropiado
           if state == AgentState.CONTENT_GENERATION:
               # Streaming de generación de contenido
               async for chunk in self.content_generator.generate_stream(
                   chat_id, project_id, message
               ):
                   yield chunk
           
           elif state == AgentState.BUYER_PERSONA:
               # Análisis completo (sin streaming, pero enviar progreso)
               yield "Analizando buyer persona...\n"
               result = await self.buyer_persona_agent.generate_analysis(...)
               yield f"Análisis completo: {result}\n"
           
           # ... (otros estados)
       
       async def process(self, chat_id, project_id, user_id, message) -> Dict:
           """Versión sin streaming (retorna resultado completo)."""
           # Similar a process_stream pero sin yield
           pass
   ```

**Criterios de aceptación:**
- [ ] Middleware NO lee body en endpoints de streaming (GOTCHA 3)
- [ ] Endpoint `/api/chat/stream` retorna SSE correctamente
- [ ] Endpoint `/api/chat/message` retorna JSON completo
- [ ] RouterAgent orquesta agentes correctamente
- [ ] Mensajes se guardan en `marketing_messages`
- [ ] Test con curl: `curl -N http://localhost:8000/api/chat/stream` retorna chunks
- [ ] Frontend puede consumir stream sin bloqueos

**Archivos a crear/modificar:**
- `backend/src/api/chat.py` (nuevo)
- `backend/src/main.py` (modificar middleware)
- `backend/src/agents/router_agent.py` (añadir process_stream)

**Comandos de validación:**
```bash
# Test streaming con curl
curl -N http://localhost:8000/api/chat/stream \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"...","message":"Hola"}' \
  --no-buffer

# Esperado: Chunks en tiempo real
data: Hola
data: ,
data:  ¿cómo
data:  puedo
data:  ayudarte?
data: [DONE]
```

---

### TAREA 7: Frontend - Auth y Layout Base

**Herramientas a utilizar:**
- ⚡ MCP Archon: Next.js 14 App Router + Auth patterns
  - Comando: `rag_search_knowledge_base(query="nextjs app router authentication middleware", source_id="77b8a4a07d5230b5", match_count=5)`
  - Comando: `rag_search_code_examples(query="nextjs cookies httponly", source_id="77b8a4a07d5230b5", match_count=3)`

- 🔧 MCP Serena: Analizar componentes de ejemplo
  - Comando: `find_file('layout.tsx', 'Context-Engineering-Intro/examples/')`

- 📚 Skills:
  - **nextjs-best-practices** (App Router, Server Components, middleware)
  - **react-patterns** (hooks, composición, performance)
  - **tailwind-patterns** (sistema de diseño, tokens)
  - **clean-code** (código limpio y mantenible)

**Objetivo:**
Crear estructura base del frontend con autenticación, layout, y navegación usando Next.js 14 App Router, toma en cuenta que mas adelant el proyecto se desplegara en vercel.

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 10 - JWT en localStorage + Server Components**

Problema: `localStorage` no es accesible en Server Components.
Solución: Usar cookies httpOnly + middleware de Next.js.

**Backend setea cookie (modificar en TAREA 2):**
```python
# backend/src/api/auth.py - Modificar endpoint login
from fastapi import Response

@router.post("/login")
async def login(request: LoginRequest, response: Response):
    # ... validar usuario ...
    
    # Generar JWT
    token = create_access_token({
        'user_id': str(user.id),
        'email': user.email,
        'project_id': str(user.project_id)
    })
    
    # ✅ Setear cookie httpOnly (GOTCHA 10)
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,  # No accesible desde JavaScript
        secure=True,  # Solo HTTPS en production
        samesite="lax",
        max_age=604800  # 7 días
    )
    
    return {"user": {"id": user.id, "email": user.email}}
```

**Pasos a seguir:**

1. **Crear proyecto Next.js 14:**
   ```bash
   npx create-next-app@14 frontend --typescript --tailwind --app --src-dir=false
   cd frontend
   npm install zustand @tanstack/react-query
   ```

2. **Crear middleware de autenticación:**
   
   **`frontend/middleware.ts`:**
   ```typescript
   import { NextResponse } from 'next/server'
   import type { NextRequest } from 'next/server'
   
   export function middleware(request: NextRequest) {
     // ✅ Leer cookie httpOnly (GOTCHA 10)
     const token = request.cookies.get('auth_token')?.value
     
     // Rutas públicas
     const publicPaths = ['/login', '/register', '/reset-password']
     const isPublicPath = publicPaths.some(path => request.nextUrl.pathname.startsWith(path))
     
     // Si no hay token y la ruta es privada → redirect a login
     if (!token && !isPublicPath) {
       return NextResponse.redirect(new URL('/login', request.url))
     }
     
     // Si hay token y está en página de login → redirect a /
     if (token && isPublicPath) {
       return NextResponse.redirect(new URL('/', request.url))
     }
     
     return NextResponse.next()
   }
   
   export const config = {
     matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
   }
   ```

3. **Crear layout base:**
   
   **`frontend/app/layout.tsx`:**
   ```typescript
   import type { Metadata } from 'next'
   import { Inter } from 'next/font/google'
   import './globals.css'
   
   const inter = Inter({ subsets: ['latin'] })
   
   export const metadata: Metadata = {
     title: 'Marketing Second Brain',
     description: 'Sistema IA para estrategia de contenido',
   }
   
   export default function RootLayout({
     children,
   }: {
     children: React.ReactNode
   }) {
     return (
       <html lang="es">
         <body className={inter.className}>{children}</body>
       </html>
     )
   }
   ```

4. **Crear páginas de autenticación:**
   
   **`frontend/app/login/page.tsx`:**
   ```typescript
   'use client'  // ✅ GOTCHA 4: Marcar como client component
   
   import { useState } from 'react'
   import { useRouter } from 'next/navigation'
   
   export default function LoginPage() {
     const [email, setEmail] = useState('')
     const [password, setPassword] = useState('')
     const [loading, setLoading] = useState(false)
     const router = useRouter()
     
     const handleLogin = async (e: React.FormEvent) => {
       e.preventDefault()
       setLoading(true)
       
       try {
         const response = await fetch('http://localhost:8000/api/auth/login', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ email, password }),
           credentials: 'include'  // ✅ Importante para cookies
         })
         
         if (response.ok) {
           // Cookie ya seteada por backend
           router.push('/')
         } else {
           alert('Login failed')
         }
       } finally {
         setLoading(false)
       }
     }
     
     return (
       <div className="min-h-screen flex items-center justify-center">
         <form onSubmit={handleLogin} className="space-y-4">
           <input
             type="email"
             value={email}
             onChange={(e) => setEmail(e.target.value)}
             placeholder="Email"
             className="border p-2"
           />
           <input
             type="password"
             value={password}
             onChange={(e) => setPassword(e.target.value)}
             placeholder="Password"
             className="border p-2"
           />
           <button type="submit" disabled={loading}>
             {loading ? 'Loading...' : 'Login'}
           </button>
         </form>
       </div>
     )
   }
   ```

**Criterios de aceptación:**
- [ ] Middleware de Next.js protege rutas privadas
- [ ] Cookies httpOnly funcionan (NO localStorage)
- [ ] Login exitoso setea cookie y redirige a /
- [ ] Logout limpia cookie y redirige a /login
- [ ] Layout base con navegación
- [ ] Rutas públicas (/login, /register) accesibles sin auth
- [ ] Rutas privadas (/) redirigen a /login si no hay token

**Archivos a crear:**
- `frontend/middleware.ts`
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`
- `frontend/app/login/page.tsx`
- `frontend/app/register/page.tsx`

---

### TAREA 8: Frontend - Chat Interface con Streaming

**Herramientas a utilizar:**
- ⚡ MCP Archon: React hooks + SSE en cliente
  - Comando: `rag_search_knowledge_base(query="react server sent events streaming", source_id="a931698c21fb8f24", match_count=5)`
  - Comando: `rag_search_code_examples(query="nextjs client component useState", source_id="77b8a4a07d5230b5", match_count=3)`

- 📚 Skills:
  - **react-ui-patterns** (loading states, error handling, async data)
  - **frontend-design** (UI moderna y distintiva)
  - **nextjs-best-practices** (client vs server components)
  - **context-window-management** (gestión de mensajes largos)
  - react-patterns (automático)
  - clean-code (automático)

**Objetivo:**
Implementar interfaz de chat que consume el endpoint de streaming y muestra respuestas en tiempo real.

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 4 - Next.js Server Components + useState**

Problema: `useState` NO funciona en Server Components (default en App Router).
Solución: Directiva `'use client'` al inicio de componentes interactivos.

**Pasos a seguir:**

1. **Crear componente de chat (Client Component):**
   
   **`frontend/app/components/ChatInterface.tsx`:**
   ```typescript
   'use client'  // ✅ GOTCHA 4: Marcar como client component
   
   import { useState, useEffect, useRef } from 'react'
   
   interface Message {
     role: 'user' | 'assistant'
     content: string
   }
   
   export function ChatInterface({ chatId }: { chatId: string }) {
     const [messages, setMessages] = useState<Message[]>([])
     const [input, setInput] = useState('')
     const [isStreaming, setIsStreaming] = useState(false)
     const messagesEndRef = useRef<HTMLDivElement>(null)
     
     const scrollToBottom = () => {
       messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
     }
     
     useEffect(() => {
       scrollToBottom()
     }, [messages])
     
     const handleSend = async () => {
       if (!input.trim() || isStreaming) return
       
       const userMessage = input
       setInput('')
       
       // Añadir mensaje del usuario
       setMessages(prev => [...prev, { role: 'user', content: userMessage }])
       
       // Iniciar streaming
       setIsStreaming(true)
       let assistantMessage = ''
       
       try {
         const response = await fetch('http://localhost:8000/api/chat/stream', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           credentials: 'include',  // Cookies
           body: JSON.stringify({ chat_id: chatId, message: userMessage })
         })
         
         const reader = response.body?.getReader()
         const decoder = new TextDecoder()
         
         while (true) {
           const { done, value } = await reader!.read()
           if (done) break
           
           const chunk = decoder.decode(value)
           const lines = chunk.split('\n')
           
           for (const line of lines) {
             if (line.startsWith('data: ')) {
               const data = line.slice(6)
               
               if (data === '[DONE]') {
                 // Fin del streaming
                 break
               }
               
               // Añadir chunk a mensaje del asistente
               assistantMessage += data
               
               // Actualizar UI en tiempo real
               setMessages(prev => {
                 const newMessages = [...prev]
                 const lastMsg = newMessages[newMessages.length - 1]
                 
                 if (lastMsg?.role === 'assistant') {
                   lastMsg.content = assistantMessage
                 } else {
                   newMessages.push({ role: 'assistant', content: assistantMessage })
                 }
                 
                 return newMessages
               })
             }
           }
         }
       } catch (error) {
         console.error('Streaming error:', error)
       } finally {
         setIsStreaming(false)
       }
     }
     
     return (
       <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
         {/* Lista de mensajes */}
         <div className="flex-1 overflow-y-auto space-y-4 mb-4">
           {messages.map((msg, idx) => (
             <div
               key={idx}
               className={`p-4 rounded-lg ${
                 msg.role === 'user' 
                   ? 'bg-blue-100 ml-auto max-w-[80%]' 
                   : 'bg-gray-100 mr-auto max-w-[80%]'
               }`}
             >
               {msg.content}
             </div>
           ))}
           <div ref={messagesEndRef} />
         </div>
         
         {/* Input box */}
         <div className="flex gap-2">
           <input
             type="text"
             value={input}
             onChange={(e) => setInput(e.target.value)}
             onKeyPress={(e) => e.key === 'Enter' && handleSend()}
             placeholder="Escribe tu mensaje..."
             disabled={isStreaming}
             className="flex-1 border rounded-lg p-3"
           />
           <button
             onClick={handleSend}
             disabled={isStreaming || !input.trim()}
             className="bg-blue-500 text-white px-6 rounded-lg disabled:opacity-50"
           >
             {isStreaming ? 'Enviando...' : 'Enviar'}
           </button>
         </div>
       </div>
     )
   }
   ```

2. **Crear página principal (Server Component wrapper):**
   
   **`frontend/app/page.tsx`:**
   ```typescript
   // ✅ Server Component por defecto (NO necesita 'use client')
   import { ChatInterface } from './components/ChatInterface'
   
   export default async function HomePage() {
     // ✅ Aquí podrías hacer fetch de datos iniciales si fuera necesario
     // const chats = await fetchChats()  // Server-side fetch
     
     return (
       <main>
         <h1 className="text-2xl font-bold p-4">Marketing Second Brain</h1>
         {/* Client Component maneja interactividad */}
         <ChatInterface chatId="default-chat-id" />
       </main>
     )
   }
   ```

**Criterios de aceptación:**
- [ ] Middleware protege rutas privadas
- [ ] Login funciona y setea cookie httpOnly (GOTCHA 10)
- [ ] ChatInterface es Client Component ('use client')
- [ ] HomePage es Server Component (sin 'use client')
- [ ] Streaming funciona en tiempo real
- [ ] Sin errores de hidratación en consola
- [ ] UI responsiva (mobile + desktop)

**Archivos a crear:**
- `frontend/app/components/ChatInterface.tsx`
- `frontend/app/components/Sidebar.tsx`
- `frontend/app/components/MessageList.tsx`
- `frontend/app/page.tsx`

---

### TAREA 8.1: Memoria de Conversación, Contexto Largo y Visualización de Datos

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar implementación actual de memoria
- ⚡ MCP Archon: Documentación de LangChain memory patterns
- 📚 Skills:
  - **conversation-memory** (memoria persistente de conversaciones)
  - **context-window-management** (gestión de contexto largo)
  - **agent-memory-systems** (arquitectura de memoria)
  - **frontend-design** (UI para visualización)
  - python-patterns (automático)
  - clean-code (automático)

**Uso obligatorio de herramientas (en CADA PASO):**
- **Serena (obligatorio)**: antes de cambiar código, ubicar símbolos/llamadas reales (memoria, routing, endpoints) y confirmar dónde se integra.
- **Archon (obligatorio)**: antes de decidir el patrón, consultar documentación/patrones actuales (LangChain memory, context-window, retrieval) y documentar “por qué” la decisión.

**⚠️ PROBLEMAS IDENTIFICADOS (Ver `docs/DIAGNOSTICO_MEMORIA_Y_CONTEXTO.md`):**

1. **Memoria de conversación NO se carga**: El agente no recuerda mensajes anteriores
2. **Router detecta TODO como contenido**: Keywords muy amplias activan siempre CONTENT_GENERATION
3. **No hay forma de ver buyer persona**: No hay endpoints/UI para visualizar datos generados
4. **Agentes faltantes**: Forum Simulator, Pain Points, Customer Journey no implementados
5. **RAG vs Contexto Largo**: Documentos solo se consultan, no están siempre en contexto

**Objetivo:**
Corregir sistema de memoria, mejorar detección de intenciones, crear visualización de datos, e implementar contexto largo para documentos.

**Pasos a seguir:**

#### PASO 1: Cargar Historial de Conversación

**Problema:** `load_chat_history()` existe pero nunca se llama.

**Uso de herramientas (PASO 1):**
- 🔧 Serena: localizar dónde se instancia `MemoryManager` y dónde se atienden `GET /api/chats/{chat_id}`, `POST /messages`, `POST /stream` para insertar la carga de historial sin romper SSE.
- ⚡ Archon: validar patrón recomendado para memoria por conversación (por `chat_id`) y ventana \(k\), incluyendo `return_messages`.

**Solución:**
1. Modificar `GET /api/chats/{chat_id}` para cargar historial al abrir chat
2. Modificar `POST /api/chats/{chat_id}/messages` para cargar historial antes de procesar
3. Modificar `POST /api/chats/{chat_id}/stream` para cargar historial antes de streaming

**Archivos a modificar:**
- `backend/src/api/chat.py` - agregar llamadas a `memory_manager.load_chat_history()`

**Criterios:**
- [ ] Al abrir un chat, se cargan últimos 20 mensajes
- [ ] `ConversationBufferWindowMemory` está poblado antes de procesar nuevos mensajes
- [ ] El agente puede referirse a mensajes anteriores

---

#### PASO 2: Mejorar Detección de Solicitudes de Contenido

**Problema:** Keywords muy amplias detectan cualquier mensaje como solicitud de contenido.

**Uso de herramientas (PASO 2):**
- 🔧 Serena: localizar `_is_content_request` y su uso en `route()` + ejemplos de mensajes que se clasifican mal.
- ⚡ Archon: consultar patrones de intent detection (reglas + guardrails) y cuándo conviene LLM vs reglas.

**Hallazgos (PASO 2):**
- **Serena**: `RouterAgent/_is_content_request` usa `any(keyword in message_lower ...)` con keywords demasiado amplias (incluye `"necesito"`), lo que dispara `CONTENT_GENERATION` en mensajes no-petición.
- **Archon**: para MVP, preferir **reglas estrictas** con guardrails (word boundaries + combinación “verbo de solicitud” + “objeto de contenido”) antes que keywords sueltas; dejar LLM intent-detection como opción posterior si siguen falsos positivos.

**Solución:**
1. Usar LLM para detectar intención (más preciso)
2. O mejorar keywords con contexto:
   - Verificar que sea solicitud explícita (no pregunta)
   - Considerar contexto de conversación
   - No activar si usuario está respondiendo preguntas del agente

**Archivos a modificar:**
- `backend/src/agents/router_agent.py` - mejorar `_is_content_request()` o usar LLM

**Criterios:**
- [ ] Solo activa CONTENT_GENERATION con solicitudes explícitas
- [ ] Puede mantener conversación normal sin generar contenido
- [ ] Considera contexto de mensajes anteriores

---

#### PASO 3: Crear Endpoints API para Visualizar Datos

**Problema:** No hay forma de ver buyer persona, foro, puntos de dolor, customer journey.

**Uso de herramientas (PASO 3):**
- 🔧 Serena: localizar modelos/relaciones (`MarketingBuyerPersona`, `MarketingChat`) y patrones existentes de endpoints/auth.
- ⚡ Archon: consultar diseño de APIs REST para “read-only views” + autorización por `project_id`.

**Hallazgos (PASO 3):**
- **Serena**: el backend actualmente incluye routers en `backend/src/main.py` (`auth`, `chat`, `documents`). Los endpoints siguen patrón `APIRouter(prefix="/api/...", tags=[...])` y usan `Depends(get_current_user)` para aislar por `project_id`.
- **Archon**: para “read-only views” conviene endpoints dedicados por recurso (ej. `/api/chats/{chat_id}/analysis`) y respuestas JSON estables; si una sección aún no existe (forum/pain_points/journey), devolverla vacía pero explícita (sin 404) para que UI pueda mostrar “pendiente”.

**Solución:**
1. Crear nuevos endpoints:
   - `GET /api/chats/{chat_id}/buyer-persona` - Obtener buyer persona completo
   - `GET /api/chats/{chat_id}/forum-simulation` - Obtener simulación de foro
   - `GET /api/chats/{chat_id}/pain-points` - Obtener puntos de dolor
   - `GET /api/chats/{chat_id}/customer-journey` - Obtener customer journey
   - `GET /api/chats/{chat_id}/analysis` - Obtener todo el análisis (resumen)

2. Crear schemas de respuesta:
   - `backend/src/schemas/buyer_persona.py` - Schemas para respuestas

**Archivos a crear:**
- `backend/src/api/buyer_persona.py` - Nuevos endpoints
- `backend/src/schemas/buyer_persona.py` - Schemas de respuesta

**Criterios:**
- [ ] Endpoints retornan datos en formato JSON estructurado
- [ ] Manejo de errores si no existe buyer persona
- [ ] Validación de permisos (solo usuario del proyecto)

---

#### PASO 4: Crear Componentes Frontend para Visualización

**Problema:** No hay UI para ver los datos generados.

**Uso de herramientas (PASO 4):**
- 🔧 Serena: localizar componentes actuales (`ChatInterface`, layout) y dónde insertar “panel de análisis” sin romper SSR/Suspense.
- ⚡ Archon: revisar patrones UI para estados (loading/error/empty) y manejo de context window (mostrar “resumen” vs “JSON raw”).

**Solución:**
1. Crear componentes React:
   - `BuyerPersonaView.tsx` - Visualizar buyer persona completo
   - `ForumSimulationView.tsx` - Visualizar simulación de foro
   - `PainPointsView.tsx` - Visualizar puntos de dolor
   - `CustomerJourneyView.tsx` - Visualizar customer journey
   - `AnalysisSummaryView.tsx` - Vista resumen de todo el análisis

2. Crear API client:
   - `frontend/lib/api-analysis.ts` - Cliente para endpoints de análisis

3. Integrar en ChatInterface:
   - Agregar botón/tab para ver análisis
   - Mostrar estado de generación (completo, parcial, pendiente)

**Archivos a crear:**
- `frontend/app/components/BuyerPersonaView.tsx`
- `frontend/app/components/ForumSimulationView.tsx`
- `frontend/app/components/PainPointsView.tsx`
- `frontend/app/components/CustomerJourneyView.tsx`
- `frontend/app/components/AnalysisSummaryView.tsx`
- `frontend/lib/api-analysis.ts`

**Criterios:**
- [ ] UI muestra buyer persona de forma legible y organizada
- [ ] UI muestra foro, puntos de dolor, customer journey si existen
- [ ] UI indica qué partes están completas y cuáles pendientes
- [ ] Diseño consistente con el resto de la aplicación

---

#### PASO 5: Implementar Contexto Largo para Documentos

**Problema:** Documentos solo se consultan vía RAG, no están siempre en contexto.

**Uso de herramientas (PASO 5):**
- 🔧 Serena: confirmar si existe columna/estructura para “summary” de documentos y dónde se procesa upload.
- ⚡ Archon: validar patrón “long-term doc summaries + RAG” (resumen persistente + retrieval puntual) y límites de tokens.

**Hallazgos (PASO 5):**
- **Serena**: `marketing_user_documents` actualmente NO tiene columna `summary` (solo tracking: filename/file_path/chunks_count/processed). Por tanto, “resúmenes persistentes” requieren **migración** (SQL) o alternativa (guardar resumen en `metadata` de KB / tabla nueva).
- **Archon**: patrón recomendado para “contexto largo de docs” en producción suele ser **resumen persistente + RAG** (no meter todos los docs crudos al prompt). Implica: generar resumen al subir, guardar, e inyectar resúmenes + top-k retrieval en prompts.

**Solución:**
1. Cuando se sube un documento:
   - Generar resumen/extracto con LLM
   - Guardar resumen en tabla `marketing_user_documents.summary`
   - Mantener embeddings para RAG

**Implementación (PASO 5):**
- Crear migración: `backend/db/002_add_user_document_summary.sql` (ejecución manual en Supabase).
- Backend:
  - `MarketingUserDocument.summary` (nullable) + exponer `summary` en schemas de documentos.
  - En `POST /api/documents/upload/{chat_id}` generar `summary` (sin bloquear si falla) y persistir.
  - `MemoryManager.get_context()` incluir `document_summaries` para inyectar en prompts como “contexto largo”.
  - `ContentGeneratorAgent` incluye `document_summaries` + RAG (top-k) en el prompt.

2. En `MemoryManager.get_context()`:
   - Incluir resúmenes de documentos del chat en contexto largo
   - Mantener RAG para búsqueda específica

3. En prompts de agentes:
   - Incluir resúmenes de documentos siempre (no solo cuando se busca)

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - agregar `get_document_summaries()`
- `backend/src/api/documents.py` - generar resumen al subir documento
- `backend/src/agents/content_generator_agent.py` - incluir resúmenes en prompt

**Criterios:**
- [ ] Documentos subidos tienen resumen generado
- [ ] Resúmenes se incluyen en contexto largo del LLM
- [ ] El agente puede referirse a información de documentos sin buscar
- [ ] RAG sigue funcionando para búsqueda específica

---

### TAREA 8.2: Buyer Persona Extendido (Plantilla + Foro + Customer Journey)

**Herramientas a utilizar:**
- 🔧 MCP Serena: localizar y editar `backend/src/agents/buyer_persona_agent.py`
- ⚡ MCP Archon: revisar patrones de prompts largos y respuestas JSON robustas
- 📚 Skills:
  - **conversation-memory**, **agent-memory-systems**
  - **python-patterns**, **clean-code**

**Objetivo:**
Completar el análisis del buyer persona generando automáticamente:
- `full_analysis` basado en la plantilla completa `contenido/buyer-plantilla.md`
- `forum_simulation` con posts de foro y soluciones deseadas
- `pain_points` con 10 puntos de dolor claros
- `customer_journey` con 3 fases (awareness, consideration, purchase) y listas de búsquedas/preguntas.

**Pasos a seguir:**

1. **Usar plantilla completa desde disco**
   - Leer `contenido/buyer-plantilla.md` desde el backend (ruta relativa al root del proyecto).
   - Actualizar `_build_buyer_persona_prompt()` de `BuyerPersonaAgent` para:
     - Inyectar el contenido completo del markdown en el prompt.
     - Indicar explícitamente que debe usar solo las PREGUNTAS como guía y **no** copiar las respuestas de ejemplo (caso Ana).
     - Exigir salida en **JSON válido**, estructurado por secciones (títulos de la plantilla como claves de primer nivel).

2. **Generar foro + puntos de dolor automáticamente**
   - Añadir método interno `BuyerPersonaAgent._generate_forum_and_pain_points(buyer_persona_data)`.
   - Basarse en el prompt de foro definido en `contenido/promts_borradores.md` (sección “Promt para simulacion en foro de buyer persona”).
   - El LLM debe devolver JSON con estructura:
     ```json
     {
       "posts": [{ "queja": "...", "solucion_deseada": "..." }],
       "pain_points": { "items": ["Punto 1", "...", "Punto 10"] }
     }
     ```
   - Guardar:
     - `forum_simulation = { "posts": [...] }`
     - `pain_points = { "items": [...] }`

3. **Generar customer journey (CJ) automáticamente**
   - Añadir método interno `BuyerPersonaAgent._generate_customer_journey(buyer_persona_data, forum_simulation, pain_points)`.
   - Basarse en el prompt “Prompt costumer journey” de `contenido/promts_borradores.md`.
   - El LLM debe devolver JSON con estructura:
     ```json
     {
       "awareness": { "busquedas": [...], "preguntas_cabeza": [...] },
       "consideration": { "busquedas": [...], "preguntas_cabeza": [...] },
       "purchase": { "busquedas": [...], "preguntas_cabeza": [...] }
     }
     ```
   - Guardar el resultado en `customer_journey`.

4. **Integración en el flujo actual**
   - Dentro de `BuyerPersonaAgent.execute()`:
     - Después de generar y persistir `full_analysis`, llamar secuencialmente a:
       - `_generate_forum_and_pain_points(...)`
       - `_generate_customer_journey(...)`
     - Actualizar el registro de `MarketingBuyerPersona` recién creado con:
       - `forum_simulation`, `pain_points`, `customer_journey`
       - `await db.commit()` al final de la secuencia.
   - No modificar:
     - `RouterAgent`
     - `MemoryManager`
     - endpoints existentes de análisis (`/api/chats/{chat_id}/analysis`, `/buyer-persona`).

**Archivos a modificar:**
- `backend/src/agents/buyer_persona_agent.py`

**Criterios de aceptación:**
- [ ] Primer buyer persona generado para un chat rellena:
  - `full_analysis`
  - `forum_simulation.posts` (≥1 post con `queja` + `solucion_deseada`)
  - `pain_points.items` (exactamente 10 ítems)
  - `customer_journey.awareness/consideration/purchase` con ≥10 `busquedas` y ≥10 `preguntas_cabeza` cada una.
- [ ] `GET /api/chats/{chat_id}/analysis` refleja `has_forum_simulation=true`, `has_pain_points=true`, `has_customer_journey=true` tras el primer análisis.
- [ ] El panel de análisis actual muestra la nueva información sin romper el flujo de TAREA 8.1.

---

#### PASO 6: Implementar Agentes Faltantes (Opcional - Futuro)

**Nota:** Estos agentes están fuera del scope de TAREA 8.1, pero se documentan para futuro.

**Agentes a implementar:**
1. `ForumSimulatorAgent` - Simula comportamiento en foro
2. `PainPointsExtractorAgent` - Extrae puntos de dolor
3. `CustomerJourneyCreatorAgent` - Crea customer journey

**Archivos a crear (futuro):**
- `backend/src/agents/forum_simulator_agent.py`
- `backend/src/agents/pain_points_agent.py`
- `backend/src/agents/customer_journey_agent.py`

---

**Criterios de aceptación generales:**
- [ ] El agente mantiene contexto de conversación (recuerda mensajes anteriores)
- [ ] El agente solo genera contenido cuando se solicita explícitamente
- [ ] Usuario puede ver buyer persona generado en UI
- [ ] Usuario puede ver foro, puntos de dolor, customer journey (si existen)
- [ ] Documentos subidos están siempre en contexto largo del agente
- [ ] Conversación fluida y natural, no solo generación de contenido

**Archivos a crear:**
- `backend/src/api/buyer_persona.py`
- `backend/src/schemas/buyer_persona.py`
- `frontend/app/components/BuyerPersonaView.tsx`
- `frontend/app/components/ForumSimulationView.tsx`
- `frontend/app/components/PainPointsView.tsx`
- `frontend/app/components/CustomerJourneyView.tsx`
- `frontend/app/components/AnalysisSummaryView.tsx`
- `frontend/lib/api-analysis.ts`
- `docs/DIAGNOSTICO_MEMORIA_Y_CONTEXTO.md` ✅ (ya creado)

**Archivos a modificar:**
- `backend/src/api/chat.py` - cargar historial
- `backend/src/agents/router_agent.py` - mejorar detección de contenido
- `backend/src/services/memory_manager.py` - contexto largo de documentos
- `backend/src/api/documents.py` - generar resúmenes
- `backend/src/agents/content_generator_agent.py` - incluir resúmenes

---

### TAREA 9: MCP Custom del Proyecto

**Herramientas a utilizar:**
- ⚡ MCP Archon: MCP Protocol y server creation
  - Comando: `rag_search_knowledge_base(query="MCP server python custom tools", match_count=5)`

- 🔧 MCP Serena: Analizar estructura de MCPs existentes
  - Comando: `get_symbols_overview('/home/david/.cursor/projects/home-david-brain-mkt/mcps/user-archon/')`

- 📚 Skills:
  - **mcp-builder** (construcción de MCPs custom)
  - **agent-tool-builder** (diseño de herramientas para agentes)
  - python-patterns (automático)
  - clean-code (automático)

**Objetivo:**
Crear MCP custom que expone herramientas del proyecto para que Cursor pueda interactuar con el sistema.

**Pasos a seguir:**

1. **Crear estructura del MCP:**
   ```bash
   mkdir -p mcp-marketing-brain/src
   cd mcp-marketing-brain
   touch pyproject.toml README.md
   ```

2. **Implementar servidor MCP:**
   
   **`mcp-marketing-brain/src/server.py`:**
   ```python
   from mcp.server import Server
   from mcp.types import Tool, TextContent
   import asyncio
   
   app = Server("marketing-brain")
   
   @app.tool()
   async def get_buyer_persona(chat_id: str) -> str:
       """Obtiene buyer persona generado para un chat."""
       # Conectar a BD y obtener buyer persona
       pass
   
   @app.tool()
   async def list_chats(project_id: str) -> str:
       """Lista todos los chats de un proyecto."""
       pass
   
   @app.tool()
   async def generate_content_ideas(phase: str, content_type: str, count: int = 5) -> str:
       """Genera ideas de contenido basadas en buyer persona."""
       pass
   ```

3. **Registrar en Cursor:**
   ```json
   // ~/.cursor/mcp-config.json
   {
     "mcpServers": {
       "marketing-brain": {
         "command": "python",
         "args": ["-m", "mcp_marketing_brain"],
         "cwd": "/home/david/brain-mkt/mcp-marketing-brain"
       }
     }
   }
   ```

**Criterios de aceptación:**
- [ ] MCP server funciona en Cursor
- [ ] Tools expuestas: get_buyer_persona, list_chats, generate_content_ideas
- [ ] Cursor puede llamar tools desde chat

**Archivos a crear:**
- `mcp-marketing-brain/src/server.py`
- `mcp-marketing-brain/pyproject.toml`

---

### TAREA 9.1: Edición y Eliminación Segura de Chats

**Herramientas a utilizar:**
- 🔧 MCP Serena: inspección de flujo de chats
  - `search_for_pattern("class ChatService", "backend/src")`
  - `search_for_pattern("Sidebar(", "frontend/app/components")`
- 📚 Skills:
  - **senior-fullstack**, **senior-architect**
  - clean-code (automático)

**Objetivo:**
Permitir **renombrar** y **eliminar** chats desde el sidebar, asegurando que:
- Al eliminar un chat:
  - Se elimina el registro en `marketing_chats`
  - Se eliminan en cascada SOLO los datos ligados a ese chat:
    - mensajes (`marketing_messages`)
    - buyer persona + foro + pain points + customer journey (`marketing_buyer_personas`)
    - documentos y chunks asociados (`marketing_user_documents`, `marketing_knowledge_base`)
- El frontend refresca la lista sin romper la sesión actual.

**Notas de coherencia (estado actual):**
- Backend ya tiene:
  - `ChatService.update_chat_title(...)`
  - `ChatService.delete_chat(...)` con `ondelete='CASCADE'` en:
    - `MarketingMessage.chat_id`
    - `MarketingBuyerPersona.chat_id`
    - `MarketingKnowledgeBase.chat_id`
    - `MarketingUserDocument.chat_id`
  - Endpoints expuestos en `backend/src/api/chat.py`:
    - `PATCH /api/chats/{chat_id}/title`
    - `DELETE /api/chats/{chat_id}`
- Frontend:
  - `Sidebar.tsx` ya lista y crea chats, pero **aún no expone** renombrar / eliminar.

**Pasos a seguir (sin romper lo existente):**

1. **Frontend – API client:**
   - Añadir en `frontend/lib/api-chat.ts`:
     - `updateChatTitle(chatId: string, title: string): Promise<ChatSummary>`
       - PATCH ` /api/chats/{chat_id}/title` con body `{ title }`
     - `deleteChat(chatId: string): Promise<void>`
       - DELETE `/api/chats/{chat_id}`

2. **Frontend – Sidebar UI:**
   - En `Sidebar.tsx`:
     - Añadir acciones por chat:
       - Renombrar: prompt simple (`window.prompt`) y llamada a `updateChatTitle`.
       - Eliminar: `window.confirm` y llamada a `deleteChat`.
     - Actualizar estado `chats` en memoria sin recargar toda la página.
     - Si se elimina el chat activo:
       - Seleccionar el siguiente chat disponible (o limpiar selección) y actualizar URL (`/?chat=...`).

3. **Validación:**
   - Crear >2 chats, cambiar nombres y borrar uno:
     - Confirmar que desaparece del sidebar.
     - Confirmar en DB (via SQL o tests) que:
       - El chat NO existe.
       - Buyer persona + foro + pain points + journey de ese chat NO existen.
       - Documentos y chunks con ese `chat_id` NO existen.

**Criterios de aceptación:**
- [ ] Desde el sidebar se puede renombrar un chat sin perder mensajes.
- [ ] Desde el sidebar se puede eliminar un chat y:
  - Desaparece de la lista.
  - Si era el chat activo, se selecciona otro o se deja sin selección.
- [ ] En base de datos no quedan registros huérfanos asociados a ese `chat_id`.

---

### TAREA 10: Docker + Deployment

**Herramientas a utilizar:**
- ⚡ MCP Archon: Docker best practices
  - Comando: `rag_search_knowledge_base(query="docker compose multi-container production", match_count=5)`

- 📚 Skills:
  - **docker-expert** (containerización, optimización, seguridad)
  - **deployment-procedures** (estrategias de deployment)
  - **server-management** (gestión de procesos y recursos)
  - clean-code (automático)

**⚠️ GOTCHA CRÍTICO APLICADO:**
**GOTCHA 8 - Docker volumes en Windows**

Problema: Bind mounts (`./backend:/app`) tienen permisos raros en Windows/WSL.
Solución: Usar named volumes para persistencia.

**Objetivo:**
Crear configuración de Docker para desarrollo y producción.

**Pasos a seguir:**

1. **Crear Dockerfile del backend:**
   
   **`backend/Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY pyproject.toml ./
   RUN pip install --no-cache-dir -e .
   
   COPY . .
   
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
   ```

2. **Crear Dockerfile del frontend:**
   
   **`frontend/Dockerfile`:**
   ```dockerfile
   FROM node:20-alpine
   
   WORKDIR /app
   
   COPY package*.json ./
   RUN npm install
   
   COPY . .
   
   CMD ["npm", "run", "dev"]
   ```

3. **Crear docker-compose.yml:**
   
   **`docker-compose.yml`:**
   ```yaml
   version: '3.8'
   
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - SUPABASE_URL=${SUPABASE_URL}
         - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
         - SUPABASE_DB_URL=${SUPABASE_DB_URL}
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
         - JWT_SECRET_KEY=${JWT_SECRET_KEY}
       volumes:
         # ✅ GOTCHA 8: Named volume en vez de bind mount
         - backend_storage:/app/storage
         # Para desarrollo: bind mount solo para código
         - ./backend/src:/app/src:ro
       depends_on:
         - redis
     
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://localhost:8000/api
       volumes:
         - ./frontend/app:/app/app:ro
         - ./frontend/components:/app/components:ro
       depends_on:
         - backend
     
     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
       volumes:
         # ✅ GOTCHA 8: Named volume
         - redis_data:/data
   
   volumes:
     backend_storage:  # ✅ Named volume (funciona en Windows/Linux/Mac)
     redis_data:
   ```

**Criterios de aceptación:**
- [ ] `docker compose up` inicia todos los servicios
- [ ] Backend accesible en :8000
- [ ] Frontend accesible en :3000
- [ ] Named volumes persisten datos correctamente
- [ ] Sin problemas de permisos en Windows/WSL (GOTCHA 8)

**Archivos a crear:**
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

---

### TAREA 11: Documentación Final (tests E2E parciales / futura iteración)

**Herramientas a utilizar:**
- ⚡ MCP Archon: Pytest patterns
  - Comando: `rag_search_code_examples(query="pytest async fixtures", match_count=3)`

- 📚 Skills:
  - **testing-patterns** (unit, integration, E2E)
  - **verification-before-completion** (validación exhaustiva)
  - **systematic-debugging** (debugging metódico)
  - **test-driven-development** (TDD cuando aplique)
  - python-patterns (automático)
  - clean-code (automático)

**Objetivo (ajustado):**
- En esta iteración: **documentación final del proyecto** (README, uso, gotchas, trazas).
- Dejar **plantilla y esqueletos** de tests E2E listos, sin exigir cobertura completa ahora.

**Pasos a seguir:**

1. **Tests end-to-end del flujo completo:**
   
   **`backend/tests/integration/test_full_flow.py`:**
   ```python
   import pytest
   
   @pytest.mark.asyncio
   async def test_complete_buyer_persona_flow():
       """Test del flujo completo: registro → chat → buyer persona."""
       
       # 1. Registrar usuario
       # 2. Login
       # 3. Crear chat
       # 4. Enviar mensaje con info del negocio
       # 5. Verificar que genera buyer persona completo
       # 6. Verificar que NO genera contenido automáticamente
       
       pass
   
   @pytest.mark.asyncio
   async def test_document_upload_and_usage():
       """Test: documento subido se usa en análisis."""
       
       # 1. Login
       # 2. Subir documento con info del negocio
       # 3. Generar buyer persona
       # 4. Verificar que análisis menciona info del documento
       
       pass
   ```

2. **Actualizar README.md con instrucciones finales:**
   - Quick start completo
   - Troubleshooting
   - Ejemplos de uso

3. **Crear documentación de API:**
   ```bash
   # FastAPI genera docs automáticas
   # Verificar en: http://localhost:8000/docs
   ```

**Criterios de aceptación (ajustados):**
- [ ] README completo y actualizado (incluye:
  - Setup backend/frontend
  - Variables de entorno
  - Flujo buyer persona → análisis → contenido
  - Uso del panel Trace y flags de salud (`has_history`, `rag_used`, `training_injected`, `tecnicas_aplicadas_count`)
- [ ] Referencia rápida de endpoints clave (auth, chats, stream, documentos, análisis)
- [ ] Esqueletos de tests E2E creados (`backend/tests/integration/test_full_flow.py`) pero sin requerir 100% coverage en esta fase
- [ ] Checklist de validación manual actualizado (sección “Checklist de Validación Final”)

**Archivos a crear:**
- `backend/tests/integration/test_full_flow.py`
- `README.md` (actualizar)

---

## 🔄 Bucle de Validación

### Nivel 1: Sintaxis & Estilo
```bash
# Ejecutar PRIMERO - arreglar errores antes de proceder
ruff check backend/src/ --fix
mypy backend/src/

# Frontend
npx eslint frontend/app/ --fix
npx tsc --noEmit

# Esperado: Sin errores. Si hay errores, LEER y ARREGLAR
```

### Nivel 2: Tests Unitarios
```python
# Backend: CREAR tests siguiendo patrones
def test_buyer_persona_agent_generates_complete_analysis():
    """BuyerPersonaAgent retorna análisis completo con 35+ campos."""
    agent = BuyerPersonaAgent(llm, memory)
    result = await agent.generate_analysis(chat_id, project_id, initial_questions)
    
    assert 'full_analysis' in result
    assert len(result['full_analysis']) >= 35
    assert 'demographics' in result['full_analysis']

def test_content_generator_not_called_automatically():
    """ContentGenerator NO se ejecuta sin petición explícita."""
    router = RouterAgent(memory, llm)
    state = await router.route(chat_id, "Hola, tengo un negocio de X")
    
    assert state != AgentState.CONTENT_GENERATION
    assert state in [AgentState.BUYER_PERSONA, AgentState.WAITING]

def test_document_processor_includes_in_search():
    """Documentos subidos aparecen en búsqueda semántica."""
    # Subir documento
    doc_id = await upload_document(chat_id, file)
    await process_document(doc_id)
    
    # Buscar
    results = await vector_search.search(query, project_id, chat_id)
    
    # Verificar que incluye chunks del documento
    assert any(r['content_type'] == 'user_document' for r in results)
```

```bash
# Ejecutar e iterar hasta que pasen:
pytest backend/tests/ -v --cov=backend/src --cov-report=html

# Frontend:
npm test -- --coverage
```

### Nivel 3: Test de Integración
```bash
# 1. Iniciar servicios
docker-compose up -d

# 2. Test del flujo completo
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","full_name":"Test","project_id":"<uuid>"}'

# Obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","project_id":"<uuid>"}' \
  | jq -r '.access_token')

# Crear chat
CHAT_ID=$(curl -X POST http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}' \
  | jq -r '.id')

# Subir documento
curl -X POST http://localhost:8000/api/chats/$CHAT_ID/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_business_info.txt"

# Esperar procesamiento (background task)
sleep 5

# Enviar mensaje para iniciar análisis
curl -X POST http://localhost:8000/api/chats/$CHAT_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Mi negocio es una tienda online de productos eco-friendly"}'

# Verificar que agente respondió con análisis
# Verificar que análisis incluye info del documento subido

# 3. Test frontend
open http://localhost:3000
# Manual: Login, crear chat, subir doc, chat con agente, pedir ideas de contenido
```

---

## ✅ Checklist de Validación Final

**Funcionalidad Completa:**
- [ ] Autenticación: register, login, recover password
- [ ] Chats: crear, listar, editar, eliminar
- [ ] Documentos: subir (.txt, .pdf, .docx), listar, eliminar
- [ ] Procesamiento: documentos se procesan en background
- [ ] Agente: genera buyer persona completo (con docs si existen)
- [ ] Agente: simula foro y extrae pain points
- [ ] Agente: genera customer journey (3 fases × 20 preguntas)
- [ ] Agente: ENTREGA análisis y ESPERA (no genera automáticamente)
- [ ] Memoria: funciona (short/long/semantic)
- [ ] Contenido on-demand: genera SOLO cuando usuario pide
- [ ] Búsqueda semántica: incluye docs del usuario + knowledge base global
- [ ] Streaming: respuestas en tiempo real (<3s primera palabra)
- [ ] Aislamiento: datos por project_id (sin mezcla)

**Calidad de Código:**
- [ ] Sin errores de linting: `ruff check backend/src/`
- [ ] Sin errores de tipos: `mypy backend/src/`
- [ ] Sin errores TypeScript: `npx tsc --noEmit`
- [ ] Tests >80% coverage: `pytest --cov`
- [ ] Documentación: README.md, API.md completos

**Performance:**
- [ ] Búsqueda vectorial <100ms
- [ ] Streaming LLM <3s primera respuesta
- [ ] Frontend carga <2s (Lighthouse >90)
- [ ] API <200ms (endpoints simples)

**Seguridad:**
- [ ] JWT implementado correctamente
- [ ] Passwords con bcrypt (cost 12)
- [ ] RLS habilitado en Supabase
- [ ] API keys no expuestas
- [ ] Validación de input en todos los endpoints
- [ ] Archivos: validación MIME, tamaño, sanitización

**Docker:**
- [ ] docker-compose up funciona sin errores
- [ ] Frontend accesible en :3000
- [ ] Backend accesible en :8000
- [ ] Redis funcional
- [ ] Volúmenes persisten datos
- [ ] Logs sin errores críticos

---

## ❌ Anti-Patrones a Evitar

**Código:**
- ❌ No crear patrones cuando existentes funcionan
- ❌ No saltar validación porque "debería funcionar"
- ❌ No ignorar tests fallidos
- ❌ No usar sync en contexto async
- ❌ No hardcodear valores (usar env vars)
- ❌ No usar catch-all exceptions
- ❌ No leer archivos completos sin Serena primero
- ❌ No buscar en web sin Archon primero

**Arquitectura:**
- ❌ No hacer que ContentGenerator se ejecute automáticamente
- ❌ No mezclar datos entre proyectos (siempre filtrar por project_id)
- ❌ No usar Supabase Auth (implementar manual)
- ❌ No generar embeddings síncronamente
- ❌ No hacer queries N+1 en loops

**Base de Datos:**
- ❌ No crear índice ivfflat con <1000 rows (usar hnsw)
- ❌ No usar service role key confiando en RLS (validar project_id manualmente)
- ❌ No olvidar normalizar embeddings antes de insertar

**Agentes:**
- ❌ No usar descripciones vagas en tools (ser específico)
- ❌ No asumir que ConversationBufferMemory es suficiente (usar WindowMemory)
- ❌ No olvidar buscar en documentos del usuario cuando genera contenido

---

## 📊 Score de Confianza

**Evaluar este PRP en escala 1-10:**

**Criterios Actuales:**
- ✅ Archon consultado exhaustivamente (Pydantic, FastAPI, LangChain, Supabase)
- ✅ Source IDs específicos incluidos
- ✅ Queries de ejemplo proporcionadas
- ✅ Serena: TAREA 0 obligatoria incluida
- ✅ Comandos específicos de Serena en cada tarea
- ✅ Skills identificadas por fase con justificación
- ✅ Gotchas críticos documentados (10 GOTCHAS + 4 WARNINGS)
- ✅ Modelos completos (SQLAlchemy + Pydantic)
- ✅ Estructura de tareas con herramientas, pasos, criterios
- ✅ Validación en 3 niveles (sintaxis, tests, integración)
- ✅ Anti-patrones específicos del proyecto
- ✅ Ejemplos de código con contexto del proyecto
- ✅ Comandos de validación ejecutables

**Score Estimado: 9/10**

**Razones:**
- Contexto extremadamente completo
- MCPs integrados estratégicamente
- Skills activadas en momentos correctos
- Tareas 0-3.5 con detalle quirúrgico
- Patrón de desarrollo claro
- Gotchas de producción documentados
- Sistema de memoria bien diseñado
- Flujo de documentos del usuario integrado
- Aislamiento multi-tenant correcto

**Única debilidad:** Tareas 4-11 necesitan completarse con mismo nivel de detalle que 0-3.5 (esto se hará en siguiente iteración o durante ejecución).

**Implementación one-pass:** ✅ ALTA PROBABILIDAD

---

## 🎯 Próximos Pasos

1. **Ejecutar PRP:**
   ```bash
   # Abrir archivo PRP en Cursor
   code PRPs/marketing-brain-system-v3.md
   
   # Comenzar por TAREA 0 (instalar Serena)
   # Luego proceder secuencialmente
   ```

2. **Durante Ejecución:**
   - Consultar Archon con queries proporcionadas
   - Usar Serena ANTES de leer archivos
   - Activar Skills en momentos indicados
   - Ejecutar validación después de cada tarea
   - Iterar si tests fallan (leer error, entender, arreglar, re-ejecutar)

3. **Al Completar:**
   - Verificar checklist final
   - Ejecutar tests de integración completos
   - Documentar cualquier decisión arquitectónica tomada
   - Actualizar README.md con setup instructions

4. **Post-MVP:**
   - Deployment a VPS con Portainer
   - Features adicionales (exportar PDF, calendario de contenido)
   - Optimizaciones de performance
   - Fine-tuning de prompts basado en feedback

---

## 📚 Referencias y Recursos

**Archon Source IDs:**
- Pydantic v2: `9d46e91458092424`
- FastAPI: `c889b62860c33a44`
- LangChain: `e74f94bb9dcb14aa`
- Supabase: `9c5f534e51ee9237`
- Next.js 14: `77b8a4a07d5230b5`
- React: `a931698c21fb8f24`
- TypeScript: `d7c76d077e634ab3`
- shadcn/ui: `bf102fe8a697ed7c`

**Ejemplos del Proyecto:**
- `Context-Engineering-Intro/examples/main_agent_reference/`: Patrón de agentes con dependencies
- `Context-Engineering-Intro/examples/mcp-server/`: MCP server con auth y tools

**Skills Críticas:**
- Planificación: `planning-with-files`, `brainstorming`, `architecture`
- Desarrollo: `clean-code`, `python-patterns`, `react-patterns`
- Agentes: `agent-memory-systems`, `autonomous-agents`, `rag-implementation`
- Validación: `lint-and-validate`, `verification-before-completion`, `systematic-debugging`

---

**🚀 ESTE PRP ESTÁ LISTO PARA EJECUCIÓN**

**Recuerda:**
- TAREA 0 es OBLIGATORIA (instalar Serena)
- Consultar Archon ANTES que web
- Usar Serena ANTES de leer archivos
- Activar Skills en momentos correctos
- Validar después de cada tarea
- Iterar hasta que tests pasen

**¡Éxito en la implementación! 🎉**

