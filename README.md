# 🧠 Marketing Second Brain System

> Sistema web full-stack de segundo cerebro para estrategia de marketing digital con agente IA, memoria persistente y generación de contenido personalizado

---

## 📌 ¿Qué es esto?

Un sistema inteligente que:

1. **Analiza tu negocio** → Creas tu buyer persona automáticamente
2. **Simula comportamiento** → El agente actúa como tu cliente ideal
3. **Mapea el customer journey** → 3 fases con 20+ preguntas por fase
4. **Genera contenido on-demand** → Ideas de videos, posts, artículos personalizados
5. **Aprende de expertos** → Entrenado con transcripciones de YouTubers + libros de marketing

---

## 🎯 Diferenciadores Clave

| Característica | Descripción |
|----------------|-------------|
| 🤖 **Agente IA Multi-Especializado** | 7 agentes (Router, Buyer Persona, Forum Simulator, Pain Points, Customer Journey, Content Generator, Document Processor) |
| 🧠 **Memoria Triple** | Short-term (10 últimos mensajes), Long-term (DB completa), Semantic (búsqueda vectorial) |
| 📚 **RAG con Conocimiento Experto** | Transcripciones de YouTubers + RAG tradicional |
| 📖 **Aprendizaje Progresivo de Libros** | **🆕** Extrae conceptos estructurados (no solo chunks) de libros de marketing |
| 📄 **Upload de Documentos** | Sube archivos `.txt`, `.pdf`, `.docx` con info de tu negocio |
| ⏸️ **No Genera Automáticamente** | Usuario controla cuándo generar contenido (no spam) |
| 🔒 **Multi-Tenancy Estricto** | Aislamiento total por `project_id` |
| 🚀 **Streaming de Respuestas** | SSE (Server-Sent Events) para respuestas en tiempo real |

---

## 🛠️ Stack Tecnológico

### Frontend
- **Next.js 14** (App Router)
- **TypeScript** + **React 18**
- **TailwindCSS** + **shadcn/ui**
- **Zustand** (estado global)
- **Server-Sent Events** (streaming)

### Backend
- **FastAPI** (Python 3.11+)
- **Pydantic v2** (validación)
- **SQLAlchemy 2.0** + **Alembic** (ORM + migraciones)
- **LangChain** + **LangGraph** (agentes)
- **Anthropic Claude 3.5 Sonnet** (LLM)
- **OpenAI** (embeddings)

### Database
- **Supabase** (PostgreSQL + pgvector)
- **pgvector** (búsqueda vectorial)

### Infrastructure
- **Docker** + **Docker Compose**
- **Redis** (opcional, caché)

---

## 📁 Estructura del Proyecto

```bash
/home/david/brain-mkt/
├── README.md                           # ← Este archivo
├── .env.example                        # Plantilla de variables de entorno
├── docker-compose.yml                  # Orquestación de 4 servicios
│
├── frontend/                           # Next.js 14 App
│   ├── app/
│   │   ├── components/                 # ChatInterface, Sidebar, TracePanel
│   │   ├── page.tsx                    # Página principal
│   │   └── layout.tsx
│   ├── lib/
│   │   └── api-chat.ts                 # Utilidades API (CRUD chats)
│   └── Dockerfile
│
├── backend/                            # FastAPI App
│   ├── src/
│   │   ├── api/                        # Endpoints (auth, chat, documents)
│   │   ├── agents/                     # 7 agentes IA
│   │   │   ├── router_agent.py         # Orquestador principal
│   │   │   ├── content_generator_agent.py  # Generador de ideas
│   │   │   ├── buyer_persona_agent.py
│   │   │   ├── forum_simulator_agent.py
│   │   │   ├── pain_points_agent.py
│   │   │   ├── customer_journey_agent.py
│   │   │   └── document_processor_agent.py
│   │   ├── services/                   # LLM, embeddings, memory
│   │   ├── db/                         # Models SQLAlchemy
│   │   └── schemas/                    # Pydantic schemas
│   ├── scripts/
│   │   └── ingest_training_data.py
│   └── Dockerfile
│
├── mcp-marketing-brain/                # 🆕 MCP Server
│   ├── src/
│   │   └── server.py                   # FastMCP con 3 tools
│   ├── pyproject.toml                  # Dependencias: mcp, httpx, uvicorn
│   └── Dockerfile
│
├── contenido/                          # Material de entrenamiento
│   ├── buyer-plantilla.md
│   ├── prompts-mejorados-v2.md
│   └── Transcriptions Andrea Estratega/
│
├── docs/                               # Documentación técnica
│   ├── gotchas-detallados-y-soluciones.md
│   ├── supabase-self-hosted-setup.md
│   └── qa-plan3-tecnicas-aplicadas.md  # 🆕 QA manual
│
├── PRPs/                               # Product Requirement Prompts
│   └── marketing-brain-system-v3.md
│
└── Context-Engineering-Intro/         # Ejemplos y templates de referencia
```

---

## 🚀 Quick Start

### 1. Clonar Repositorio

```bash
git clone <repo-url>
cd brain-mkt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar plantilla
cp .env.example .env

# Editar con tus credenciales
nano .env

# Variables REQUERIDAS:
# - SUPABASE_URL              # URL de tu instancia Supabase
# - SUPABASE_SERVICE_ROLE_KEY # Service role key (Admin)
# - ANTHROPIC_API_KEY         # API key de Anthropic
# - OPENAI_API_KEY            # API key de OpenAI (embeddings)
# - JWT_SECRET_KEY            # Secret para tokens JWT
```

**📚 Guía**: Ver `docs/supabase-self-hosted-setup.md` si usas Supabase en VPS

### 3. Configurar Base de Datos

```bash
# Conectar a PostgreSQL (Supabase)
psql $SUPABASE_DB_URL

# Ejecutar SQL del PRP (TAREA 1)
# Ver: PRPs/marketing-brain-system-v3.md
# Sección: "TAREA 1: Configurar Base de Datos en Supabase"
```

### 4. Iniciar Servicios con Docker

```bash
# Construir y levantar todos los servicios
docker compose up --build -d

# Verificar que todo está corriendo
docker compose ps

# Esperado: 4 contenedores "Up"
# - marketing-brain-frontend (3000)
# - marketing-brain-backend  (8000)
# - marketing-brain-mcp      (8080)
# - marketing-brain-redis    (6379)
```

### 5. Ingestar Material de Entrenamiento

```bash
# Procesar transcripciones de Andrea Estratega
docker compose exec backend python scripts/ingest_training_data.py \
  --source "contenido/Transcriptions Andrea Estratega/" \
  --content-type video_transcript

# Esperado: ~200-500 chunks procesados
```

### 6. Acceder a la Aplicación

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interfaz de usuario |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger/OpenAPI |
| **MCP Server** | http://localhost:8080/mcp | MCP para Cursor |

---

## 🐳 Docker Architecture

El sistema usa Docker Compose para orquestar 4 servicios:

```yaml
services:
  frontend:        # Next.js 14 (puerto 3000)
  backend:         # FastAPI (puerto 8000)
  mcp-marketing-brain:  # MCP Server (puerto 8080)
  redis:           # Cache (puerto 6379)
```

### Comandos Docker Útiles

```bash
# Iniciar todos los servicios
docker compose up -d

# Ver logs de un servicio específico
docker compose logs -f backend

# Reconstruir un servicio
docker compose up --build -d backend

# Detener todos los servicios
docker compose down

# Limpiar volúmenes (CUIDADO: borra datos)
docker compose down -v
```

### Variables de Entorno Docker

El archivo `docker-compose.yml` configura:

- `NEXT_PUBLIC_API_URL=http://localhost:8000` - URL del backend para el frontend
- `BACKEND_CORS_ORIGINS` - Orígenes permitidos para CORS
- `MCP_TRANSPORT=http` - Transporte HTTP para el MCP server

---

## 🔌 MCP Server (Model Context Protocol)

El proyecto incluye un servidor MCP para integración con Cursor/Claude Desktop.

### Tools Disponibles

| Tool | Descripción |
|------|-------------|
| `mb_list_chats` | Lista todos los chats del proyecto |
| `mb_get_chat_analysis` | Obtiene análisis completo (buyer persona, foro, journey) |
| `mb_generate_content_ideas_stub` | Placeholder para generación de contenido |

### Configuración en Cursor

Para usar el MCP con Cursor, agrega a tu configuración MCP:

```json
{
  "mcpServers": {
    "marketing-brain": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8080/mcp"],
      "env": {}
    }
  }
}
```

### Variables de Entorno MCP

```bash
# En docker-compose.yml o .env
MCP_TRANSPORT=http          # Transporte: stdio | http
MCP_HOST=0.0.0.0           # Host (0.0.0.0 para Docker)
MCP_PORT=8080              # Puerto
BACKEND_API_URL=http://backend:8000  # URL del backend (interno Docker)
```

---

## 📖 Documentación Clave

| Documento | Propósito |
|-----------|-----------|
| **PRPs/marketing-brain-system-v3.md** | PRP completo con 11 tareas detalladas |
| **docs/gotchas-detallados-y-soluciones.md** | 10 problemas técnicos críticos con soluciones validadas |
| **docs/supabase-self-hosted-setup.md** | Guía de instalación de Supabase en VPS |
| **contenido/buyer-plantilla.md** | Plantilla base para buyer persona (11 categorías) |
| **contenido/prompts-mejorados-v2.md** | Prompts con técnicas avanzadas (Chain-of-Thought, Few-Shot) |

---

## 🔍 Componentes Principales

### 🤖 Agentes IA

1. **RouterAgent**: Orquestador principal, detecta intención del usuario
2. **DocumentProcessorAgent**: Procesa archivos subidos (.txt, .pdf, .docx)
3. **BuyerPersonaAgent**: Genera buyer persona completo (11 categorías, 40+ preguntas)
4. **ForumSimulatorAgent**: Simula persona en foro (quejas + soluciones)
5. **PainPointsAgent**: Extrae 10 puntos de dolor
6. **CustomerJourneyAgent**: Crea customer journey (3 fases × 20 preguntas)
7. **ContentGeneratorAgent**: Genera ideas de contenido on-demand

### 🧠 Sistema de Memoria

```python
class MemoryManager:
    """
    Gestión de memoria triple:
    
    1. SHORT-TERM: ConversationBufferWindowMemory (k=10)
       - Últimos 10 mensajes de conversación
       - Para contexto inmediato
    
    2. LONG-TERM: PostgreSQL (marketing_messages, marketing_buyer_personas)
       - Historial completo de chats
       - Buyer personas generados
       - Customer journeys
    
    3. SEMANTIC: pgvector (marketing_knowledge_base)
       - Transcripciones de YouTubers (project_id=NULL)
       - Documentos subidos por usuario (project_id=específico)
       - Búsqueda vectorial con embeddings OpenAI
    """
```

### 📚 Sistema de Aprendizaje Progresivo de Libros

El sistema incluye un pipeline avanzado para aprender de libros y documentos largos. A diferencia de un RAG tradicional que solo guarda chunks de texto, este sistema **extrae conocimiento estructurado**.

#### ¿Por qué tarda en procesar un libro?

| Sistema | Pipeline | Velocidad |
|---------|----------|-----------|
| **RAG tradicional** | Chunk → Embed → Guardar | ⚡ Segundos |
| **Nuestro sistema** | Chunk → **LLM extrae conceptos** → Embed → Guardar | 🐢 Minutos |

Cada chunk del libro pasa por un LLM que extrae:

```
┌─────────────────────────────────────────────────────────────────┐
│                    POR CADA CHUNK SE EXTRAE:                    │
├─────────────────────────────────────────────────────────────────┤
│ main_concepts     │ Conceptos principales (máx 5)               │
│                   │ Ej: ["Hook", "Dream 100", "Traffic Funnel"] │
├───────────────────┼─────────────────────────────────────────────┤
│ relationships     │ Relaciones entre conceptos                  │
│                   │ Ej: ["Hook captura atención → Funnel        │
│                   │      convierte", "Dream 100 genera Warm     │
│                   │      Traffic"]                              │
├───────────────────┼─────────────────────────────────────────────┤
│ key_examples      │ Ejemplos concretos del libro                │
│                   │ Ej: ["Russell contactó 100 influencers      │
│                   │      para su primer lanzamiento"]           │
├───────────────────┼─────────────────────────────────────────────┤
│ technical_terms   │ Términos técnicos con definiciones          │
│                   │ Ej: {"Dream 100": "Lista de 100 personas    │
│                   │      que ya tienen tu audiencia ideal"}     │
├───────────────────┼─────────────────────────────────────────────┤
│ condensed_text    │ Resumen condensado del chunk (máx 2000      │
│                   │ chars) optimizado para embedding            │
└───────────────────┴─────────────────────────────────────────────┘
```

#### ¿Por qué es mejor que RAG tradicional?

| RAG Tradicional | Nuestro Sistema |
|-----------------|-----------------|
| Guarda texto crudo | Guarda **conocimiento estructurado** |
| LLM debe "entender" el chunk | LLM recibe conceptos **pre-digeridos** |
| Busca por similitud de texto | Busca por similitud de **conceptos** |
| Puede ignorar info importante | Conceptos clave ya están extraídos |

#### Flujo de procesamiento de un libro:

```
1. UPLOAD
   Usuario sube PDF/TXT/DOCX en "Libros Aprendidos"
   
2. CHUNKING  
   RecursiveCharacterTextSplitter (1500 chars, 200 overlap)
   
3. EXTRACCIÓN DE CONCEPTOS (por cada chunk)
   LLM extrae: main_concepts, relationships, key_examples, 
              technical_terms, condensed_text
   
4. EMBEDDINGS
   OpenAI text-embedding-3-small genera vector de condensed_text
   
5. ALMACENAMIENTO
   - marketing_learned_books: Metadatos + global_summary
   - marketing_book_concepts: Conceptos por chunk con embeddings
   
6. GLOBAL SUMMARY
   LLM genera resumen ejecutivo del libro completo
```

#### Cómo se aplica en las conversaciones:

```
Usuario pregunta: "Dame ideas de hooks para TikTok"
                           ↓
┌──────────────────────────────────────────────────────────────┐
│ Búsqueda semántica en marketing_book_concepts                │
│ → Encuentra conceptos relevantes por embedding               │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│ Se inyecta en el System Prompt:                              │
│                                                              │
│ ## CONOCIMIENTO APRENDIDO DE LIBROS:                         │
│                                                              │
│ 📚 DE 'Traffic Secrets - Russell Brunson':                   │
│   Conceptos: Hook, Pattern Interrupt, Dream 100              │
│   Resumen: El hook debe capturar atención en 3 segundos...   │
│   Términos: Hook: Primera frase que detiene el scroll        │
│                                                              │
│ 📚 DE 'Expert Secrets':                                      │
│   Conceptos: Story Selling, Origin Story, Epiphany Bridge    │
│   Resumen: Las historias venden mejor que los argumentos...  │
└──────────────────────────────────────────────────────────────┘
                           ↓
              LLM genera respuesta usando ese conocimiento
```

#### Tablas de la base de datos:

```sql
-- Metadatos de libros procesados
CREATE TABLE marketing_learned_books (
    id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    processing_status VARCHAR(50),  -- pending/processing/completed/failed
    total_chunks INTEGER,
    processed_chunks INTEGER,
    global_summary JSONB,           -- Resumen ejecutivo del libro
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Conceptos extraídos por chunk
CREATE TABLE marketing_book_concepts (
    id UUID PRIMARY KEY,
    learned_book_id UUID REFERENCES marketing_learned_books(id),
    chunk_index INTEGER NOT NULL,
    main_concepts TEXT[],           -- Array de conceptos
    relationships TEXT[],           -- Array de relaciones
    key_examples TEXT[],            -- Array de ejemplos
    technical_terms JSONB,          -- {término: definición}
    condensed_text TEXT,            -- Resumen para embedding
    embedding VECTOR(1536),         -- Vector OpenAI
    created_at TIMESTAMP
);
```

#### Tiempo estimado de procesamiento:

| Tamaño del libro | Chunks aprox. | Tiempo estimado |
|------------------|---------------|-----------------|
| 50 páginas | ~50 chunks | 3-5 minutos |
| 200 páginas | ~200 chunks | 10-15 minutos |
| 400+ páginas | ~400+ chunks | 20-30 minutos |

> **Nota**: Cada chunk requiere una llamada al LLM para extraer conceptos. El procesamiento es en batches de 10 chunks para evitar rate limits.

#### Verificar progreso de un libro:

```bash
# Ver estado en la base de datos
docker run --rm postgres:15-alpine psql "$SUPABASE_DB_URL" -c "
SELECT title, processing_status, processed_chunks, total_chunks 
FROM marketing_learned_books 
ORDER BY created_at DESC;
"

# Ver logs de procesamiento
docker logs marketing-brain-backend 2>&1 | grep "\[BOOK\]"
# Output: [BOOK] batch book_id=xxx processed=50/200
```

---

### 📊 Base de Datos

**Tablas principales:**
- `marketing_projects`: Proyectos (multi-tenancy)
- `marketing_users`: Usuarios con autenticación manual (JWT)
- `marketing_chats`: Conversaciones
- `marketing_messages`: Mensajes individuales
- `marketing_buyer_personas`: Buyer personas generados
- `marketing_knowledge_base`: Base de conocimiento vectorial (RAG tradicional)
- `marketing_user_documents`: Documentos subidos
- `marketing_learned_books`: **🆕** Libros procesados (metadatos + resumen global)
- `marketing_book_concepts`: **🆕** Conceptos estructurados extraídos de libros

**Índices críticos:**
- HNSW en `embedding` columns (NO ivfflat con <1000 docs)
- Índices compuestos en `(user_id, project_id)`

---

## 🔐 Seguridad

### Autenticación
- **Manual JWT** (NO Supabase Auth debido a limitaciones de correo)
- Tokens con 7 días de expiración
- Cookies `httpOnly` + `secure` en producción

### Aislamiento Multi-Tenant
```python
# ✅ TODAS las queries incluyen project_id
chats = db.chats.find({
    'user_id': user_id,
    'project_id': project_id  # ← OBLIGATORIO
})

# ❌ NUNCA queries sin project_id
chats = db.chats.find({'user_id': user_id})  # ← PELIGRO
```

### Gotchas de Seguridad

⚠️ **GOTCHA 6**: Service Role Key bypasea RLS

```python
# Supabase Service Role Key NO respeta Row Level Security
# Solución: Validación manual de project_id en backend
```

Ver: `docs/gotchas-detallados-y-soluciones.md` para los 10 gotchas críticos

---

## 🧪 Testing

```bash
# Tests unitarios
docker compose exec backend pytest tests/

# Tests de integración
docker compose exec backend pytest tests/integration/

# Coverage
docker compose exec backend pytest --cov=src tests/
```

---

## 🚨 Troubleshooting

### Docker: "Cannot connect to database"
```bash
# Verificar variables de entorno
docker compose exec backend env | grep SUPABASE

# Ver logs del backend
docker compose logs backend | tail -50
```

### Docker: "Frontend cannot reach backend"
```bash
# Verificar que NEXT_PUBLIC_API_URL apunta a localhost, NO a 'backend'
# El navegador no puede resolver nombres de Docker network

# ✅ Correcto (para el navegador)
NEXT_PUBLIC_API_URL=http://localhost:8000

# ❌ Incorrecto
NEXT_PUBLIC_API_URL=http://backend:8000
```

### Docker: "MCP server not responding"
```bash
# Verificar logs del MCP
docker logs marketing-brain-mcp

# Esperado:
# INFO: Uvicorn running on http://0.0.0.0:8080

# Test endpoint
curl http://localhost:8080/mcp
# Esperado: {"jsonrpc":"2.0","error":{"code":-32600,...}}
```

### "OpenAI rate limit error"
```bash
# Verificar que usas batching en embeddings
# Ver: backend/src/services/embedding_service.py
# Batch size: 50 (reduce a 20 si sigues teniendo problemas)
```

### "pgvector slow queries"
```bash
# Verificar índice HNSW (NO ivfflat con <1000 docs)
psql $SUPABASE_DB_URL -c "\d+ marketing_knowledge_base"

# Esperado: "hnsw" en columna embedding
```

### Agent: "Respuestas truncadas o incompletas"
```bash
# Verificar variables de tracing en .env
AGENT_TRACE=1
AGENT_TRACE_SHOW_PROMPTS=1
SSE_DEBUG=1

# Revisar panel de Trace en el frontend
# (botón "Trace (SSE debug)" en la interfaz)
```

Más soluciones: `docs/gotchas-detallados-y-soluciones.md`

---

## 📈 Roadmap

### ✅ Fase 1 - MVP (Completado)
- [x] Base de datos configurada (PostgreSQL + pgvector)
- [x] Backend con autenticación JWT
- [x] Agente IA con memoria triple
- [x] Frontend básico Next.js

### ✅ Fase 2 - Features Avanzadas (Completado)
- [x] Upload de documentos (.txt, .pdf, .docx)
- [x] Streaming de respuestas (SSE)
- [x] Mejora de prompts (v2.0 con técnicas avanzadas)
- [x] Panel de trazabilidad (debug) en frontend
- [x] Modo consultivo + modo ideas JSON
- [x] Edición y eliminación de chats

### ✅ Fase 3 - Production Ready (Completado)
- [x] MCP custom del proyecto (3 tools read-only)
- [x] Docker + deployment (4 servicios)
- [x] Documentación completa (README actualizado)
- [ ] Testing end-to-end (skeletons pendientes)

### ✅ Fase 4 - Aprendizaje Progresivo (Completado)
- [x] Sistema de procesamiento de libros (PDF, TXT, DOCX)
- [x] Extracción de conceptos estructurados con LLM
- [x] Almacenamiento de main_concepts, relationships, key_examples
- [x] Integración de conocimiento de libros en respuestas del agente
- [x] UI para gestión de libros aprendidos
- [x] Respuestas en Markdown (eliminado formato JSON forzado)

### 🔮 Fase 5 - Futuras Mejoras (Planeado)
- [ ] Cache Redis para training_summary
- [ ] Procesamiento paralelo de chunks (acelerar 4x)
- [ ] Generación de contenido via MCP
- [ ] Dashboard de analytics
- [ ] Exportación de contenido

---

## 🤝 Contribuir

Este es un proyecto personal. Si quieres contribuir:

1. Fork el repo
2. Crea branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Abre Pull Request

---

## 📝 Licencia

MIT License - Ver `LICENSE` para detalles

---

## 🙏 Agradecimientos

- **Anthropic Claude** (LLM)
- **OpenAI** (Embeddings)
- **Supabase** (Database + pgvector)
- **LangChain** (Agents framework)
- **Andrea Estratega** (Transcripciones de YouTube)

---

## 📞 Contacto

**Autor**: David  
**Email**: [tu-email]  
**LinkedIn**: [tu-linkedin]

---

**Última actualización**: 2026-01-31  
**Versión**: 3.0.0 (Progressive Learning System)
