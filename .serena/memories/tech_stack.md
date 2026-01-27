# Stack Tecnológico

## Frontend

- **Next.js 14** (App Router)
- **TypeScript** + **React 18**
- **TailwindCSS** + **shadcn/ui**
- **Zustand** (estado global)
- **Server-Sent Events** (streaming de respuestas)

## Backend

- **FastAPI** (Python 3.11+)
- **Pydantic v2** (validación)
- **SQLAlchemy 2.0** + **Alembic** (ORM + migraciones)
- **LangChain** + **LangGraph** (agentes IA)
- **Anthropic Claude 3.5 Sonnet** (LLM principal)
- **OpenAI** (embeddings: text-embedding-3-large)

## Base de Datos

- **Supabase** (PostgreSQL + pgvector)
- **pgvector** (búsqueda vectorial con embeddings)
- **8 tablas** con prefijo `marketing_`:
  1. marketing_projects
  2. marketing_users
  3. marketing_chats
  4. marketing_messages
  5. marketing_buyer_personas
  6. marketing_knowledge_base
  7. marketing_user_documents
  8. marketing_password_reset_tokens

## Infraestructura

- **Docker** + **Docker Compose**
- **Redis** (caché y queue)
- **3 servicios**:
  - frontend (puerto 3000)
  - backend (puerto 8000)
  - redis (puerto 6379)

## APIs Externas

- **Anthropic API** (Claude para agente)
- **OpenAI API** (embeddings)
- **Supabase** (database + storage)

## Lenguajes y Herramientas

- **Python 3.11+** (backend)
- **TypeScript** (frontend)
- **SQL** (PostgreSQL/Supabase)
- **Docker** (contenerización)
- **Git** (control de versiones)

## MCPs Utilizados

- **Archon MCP**: Consultar documentación oficial (Pydantic, FastAPI, LangChain, Supabase, Next.js, React, TypeScript, shadcn/ui)
- **Serena MCP**: Análisis simbólico de código (ESTE MCP)
- **Custom MCP** (a crear): marketing-brain-mcp con herramientas específicas del proyecto