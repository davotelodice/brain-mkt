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
| 📖 **Aprendizaje Progresivo de Libros** | Extrae conceptos estructurados (no solo chunks) de libros de marketing |
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
- **OpenAI GPT-4o** (LLM + embeddings)

### Database
- **Supabase** (PostgreSQL + pgvector)
- **pgvector** (búsqueda vectorial)

### Infrastructure
- **Docker** + **Docker Compose**
- **Redis** (opcional, caché)

---

## 📁 Estructura del Proyecto

```bash
brain-mkt/
├── README.md                           # ← Este archivo
├── .env.example                        # Plantilla de variables de entorno
├── docker-compose.yml                  # Orquestación de servicios
│
├── frontend/                           # Next.js 14 App
│   ├── app/
│   │   ├── components/                 # ChatInterface, Sidebar, TracePanel
│   │   ├── page.tsx                    # Página principal
│   │   └── layout.tsx
│   ├── lib/
│   │   └── api-chat.ts                 # Utilidades API
│   └── Dockerfile
│
├── backend/                            # FastAPI App
│   ├── src/
│   │   ├── api/                        # Endpoints (auth, chat, documents, knowledge)
│   │   ├── agents/                     # 7 agentes IA
│   │   ├── services/                   # LLM, embeddings, memory, book_learning
│   │   ├── db/                         # Models SQLAlchemy
│   │   └── schemas/                    # Pydantic schemas
│   ├── db/                             # SQL migrations
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_user_document_summary.sql
│   │   └── 003_book_learning_system.sql
│   └── Dockerfile
│
├── mcp-marketing-brain/                # MCP Server para Cursor
│   ├── src/server.py
│   └── Dockerfile
│
├── contenido/                          # Material de entrenamiento
│   └── Transcriptions Andrea Estratega/
│
└── docs/                               # Documentación técnica
```

---

## 🚀 Quick Start

### 1. Clonar Repositorio

```bash
git clone https://github.com/davotelodice/brain-mkt.git
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
# - OPENAI_API_KEY            # API key de OpenAI (LLM + embeddings)
# - JWT_SECRET_KEY            # Secret para tokens JWT
```

### 3. Configurar Base de Datos en Supabase

Ejecuta los 3 archivos SQL en orden en el **SQL Editor de Supabase**:

```bash
# Opción A: Desde el SQL Editor de Supabase Dashboard
# 1. Ve a tu proyecto en https://supabase.com/dashboard
# 2. Abre SQL Editor
# 3. Copia y ejecuta cada archivo en orden:

# Archivo 1: backend/db/001_initial_schema.sql
# Archivo 2: backend/db/002_add_user_document_summary.sql  
# Archivo 3: backend/db/003_book_learning_system.sql

# Opción B: Desde terminal con psql
psql "$SUPABASE_DB_URL" -f backend/db/001_initial_schema.sql
psql "$SUPABASE_DB_URL" -f backend/db/002_add_user_document_summary.sql
psql "$SUPABASE_DB_URL" -f backend/db/003_book_learning_system.sql
```

> **Nota**: Si usas Supabase self-hosted, ver `docs/supabase-self-hosted-setup.md`

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

### 5. Acceder a la Aplicación

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interfaz de usuario |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger/OpenAPI |
| **MCP Server** | http://localhost:8080/mcp | MCP para Cursor |

---

## 🐳 Docker Commands

```bash
# Iniciar todos los servicios
docker compose up -d

# Ver logs de un servicio específico
docker compose logs -f backend

# Reconstruir un servicio
docker compose up --build -d backend

# Detener todos los servicios
docker compose down
```

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

---

## 📖 Sistema de Aprendizaje Progresivo de Libros

El sistema extrae **conocimiento estructurado** de libros, no solo chunks de texto.

### ¿Qué extrae por cada chunk?

- **main_concepts**: Conceptos principales (máx 5)
- **relationships**: Relaciones entre conceptos
- **key_examples**: Ejemplos concretos del libro
- **technical_terms**: Términos técnicos con definiciones
- **condensed_text**: Resumen optimizado para embedding

### Tiempo de procesamiento

| Tamaño del libro | Chunks aprox. | Tiempo estimado |
|------------------|---------------|-----------------|
| 50 páginas | ~50 chunks | 3-5 minutos |
| 200 páginas | ~200 chunks | 10-15 minutos |
| 400+ páginas | ~400+ chunks | 20-30 minutos |

### Ver progreso de procesamiento

```bash
docker logs marketing-brain-backend 2>&1 | grep "\[BOOK\]"
# Output: [BOOK] parallel_batch book_id=xxx processed=50/200 success=10
```

---

## 📝 Licencia

MIT License

---

## 🙏 Agradecimientos

- **OpenAI** (LLM + Embeddings)
- **Supabase** (Database + pgvector)
- **LangChain** (Agents framework)

---

**Última actualización**: 2026-02-01  
**Versión**: 3.1.0
