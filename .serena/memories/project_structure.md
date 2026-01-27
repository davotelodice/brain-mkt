# Estructura del Proyecto

## Vista General

```
/home/david/brain-mkt/
├── README.md                           # Documentación principal
├── INITIAL.md                          # Especificación inicial detallada
├── RESUMEN-EJECUTIVO.md                # Resumen del proyecto
├── .env.example                        # Plantilla de variables de entorno
├── .cursor/                            # Configuración de Cursor IDE
├── docker-compose.yml                  # Orquestación de servicios
├──
├── frontend/                           # Aplicación Next.js 14
├── backend/                            # API FastAPI
├── contenido/                          # Material de entrenamiento
├── docs/                               # Documentación técnica
├── PRPs/                               # Product Requirement Prompts
└── Context-Engineering-Intro/         # Ejemplos y templates de referencia
```

## Frontend (Next.js 14)

```
frontend/
├── app/                                # App Router (Next.js 14)
│   ├── (auth)/                         # Grupo de rutas de autenticación
│   │   ├── login/
│   │   ├── register/
│   │   ├── recover-password/
│   │   └── reset-password/[token]/
│   ├── dashboard/                      # Dashboard principal
│   │   ├── page.tsx                    # Chat interface
│   │   └── layout.tsx                  # Sidebar + header
│   ├── api/                            # API routes (proxy)
│   │   ├── chat/route.ts
│   │   └── auth/route.ts
│   ├── layout.tsx                      # Root layout
│   └── page.tsx                        # Landing page
├── components/                         # Componentes React
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── dashboard/
│   │   ├── ChatSidebar.tsx
│   │   └── ChatHeader.tsx
│   └── chat/
│       ├── ChatInterface.tsx
│       ├── MessageList.tsx
│       ├── MessageItem.tsx
│       ├── ChatInput.tsx
│       ├── DocumentUploader.tsx
│       ├── DocumentsList.tsx
│       ├── BuyerPersonaView.tsx
│       └── CustomerJourneyView.tsx
├── lib/                                # Utilidades
│   ├── api.ts                          # Cliente API
│   └── utils.ts                        # Helpers
├── stores/                             # Zustand stores
│   ├── authStore.ts
│   └── chatStore.ts
├── hooks/                              # Custom hooks
│   ├── useStreamingChat.ts
│   ├── useChats.ts
│   └── useDocuments.ts
├── public/                             # Assets estáticos
├── styles/                             # Estilos globales
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── Dockerfile
```

## Backend (FastAPI + Python)

```
backend/
├── src/
│   ├── main.py                         # Punto de entrada FastAPI
│   ├── api/                            # Endpoints REST
│   │   ├── __init__.py
│   │   ├── auth.py                     # Registro, login, recover password
│   │   ├── chat.py                     # CRUD de chats + mensajes
│   │   ├── documents.py                 # Upload + procesamiento de docs
│   │   └── buyer_persona.py            # Endpoints de análisis
│   ├── agents/                         # Agentes IA (LangChain)
│   │   ├── __init__.py
│   │   ├── router_agent.py             # Orquestador principal
│   │   ├── document_processor_agent.py # Procesa archivos subidos
│   │   ├── buyer_persona_agent.py      # Genera buyer persona completo
│   │   ├── forum_simulator_agent.py    # Simula comportamiento en foro
│   │   ├── pain_points_agent.py        # Extrae puntos de dolor
│   │   ├── customer_journey_agent.py   # Genera customer journey
│   │   ├── content_generator_agent.py  # Genera contenido on-demand
│   │   └── memory_manager.py           # Gestiona 3 tipos de memoria
│   ├── services/                       # Servicios de negocio
│   │   ├── __init__.py
│   │   ├── llm_service.py              # Wrapper Claude/OpenAI
│   │   ├── embedding_service.py        # Generación de embeddings
│   │   ├── vector_search.py            # Búsqueda semántica
│   │   ├── chat_service.py             # Lógica de chats
│   │   └── document_service.py         # Lógica de documentos
│   ├── db/                             # Base de datos
│   │   ├── __init__.py
│   │   ├── models.py                   # SQLAlchemy models (8 tablas)
│   │   ├── database.py                 # Conexión y sesión
│   │   ├── migrations/                 # Alembic migrations
│   │   └── seed_data.sql               # Datos de prueba
│   ├── schemas/                        # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py                     # UserCreate, UserLogin, etc.
│   │   ├── chat.py                     # ChatCreate, MessageCreate, etc.
│   │   ├── documents.py                 # DocumentUpload, etc.
│   │   └── buyer_persona.py            # BuyerPersonaResponse, etc.
│   ├── middleware/                     # Middleware de FastAPI
│   │   ├── __init__.py
│   │   ├── auth.py                     # JWT validation
│   │   └── cors.py                     # CORS config
│   └── utils/                          # Utilidades
│       ├── __init__.py
│       ├── jwt.py                      # JWT encoding/decoding
│       ├── password.py                 # Bcrypt hashing
│       ├── validation.py               # Validadores custom
│       └── file_parsers.py             # Parsers .txt, .pdf, .docx
├── scripts/
│   ├── ingest_training_data.py         # Procesar transcripciones
│   └── seed_database.py                # Popular DB con datos de prueba
├── tests/                              # Tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_chat.py
│   ├── test_documents.py
│   ├── test_agents.py
│   └── integration/
│       └── test_full_flow.py
├── requirements.txt
├── pyproject.toml                     # Configuración ruff, mypy
├── alembic.ini
└── Dockerfile
```

## Contenido (Material de Entrenamiento)

```
contenido/
├── buyer-plantilla.md                 # Plantilla de buyer persona (11 categorías)
├── promts_borradores.md               # Prompts v1.0 (originales)
├── prompts-mejorados-v2.md            # Prompts v2.0 (con técnicas avanzadas)
└── Transcriptions Andrea Estratega/  # Transcripciones de YouTube
    ├── video_1.txt
    ├── video_2.txt
    └── ...
```

## Docs (Documentación Técnica)

```
docs/
├── gotchas-detallados-y-soluciones.md      # 10 gotchas críticos con soluciones
├── supabase-self-hosted-setup.md           # Guía instalación Supabase en VPS
└── architecture.md                         # Arquitectura del sistema (TBD)
```

## PRPs (Product Requirement Prompts)

```
PRPs/
└── marketing-brain-system-v3.md    # PRP completo del proyecto (11 fases)
```

## Context-Engineering-Intro (Ejemplos)

```
Context-Engineering-Intro/
├── examples/                      # Ejemplos de referencia
│   ├── main_agent_reference/
│   │   ├── research_agent.py      # Patrón de agente con pydantic-ai
│   │   ├── models.py              # Modelos Pydantic
│   │   └── providers.py           # Configuración LLM
│   └── mcp-server/
│       ├── src/index.ts           # MCP server con auth
│       ├── src/tools/             # Tool registration pattern
│       └── CLAUDE.md              # Estándares de implementación
├── PRPs/                          # Templates de PRPs
└── validation/                    # Scripts de validación
```

## Docker

```
.
├── docker-compose.yml             # Orquestación de 3 servicios
├── frontend/Dockerfile
└── backend/Dockerfile
```

## Servicios Docker

1. **frontend** (puerto 3000)
   - Next.js 14 con hot reload
   - Conecta a backend en puerto 8000

2. **backend** (puerto 8000)
   - FastAPI con hot reload
   - Conecta a Supabase (remoto)
   - Usa Redis para caché

3. **redis** (puerto 6379)
   - Caché y queue
   - Volúmen persistente

## Archivos de Configuración

```
.
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore
├── .cursor/                       # Configuración de Cursor IDE
│   ├── rules/                     # Reglas de Cursor
│   └── skills/                    # Skills de Cursor
└── .serena/                       # Configuración de Serena MCP
    └── memories/                  # Memorias de Serena (este archivo)
```

## Convenciones de Naming

### Tablas de BD:
- Prefijo: `marketing_`
- Ejemplo: `marketing_chats`, `marketing_users`

### Archivos Python:
- snake_case: `buyer_persona_agent.py`
- Models: PascalCase dentro del archivo

### Archivos TypeScript:
- PascalCase para componentes: `ChatInterface.tsx`
- camelCase para hooks: `useStreamingChat.ts`
- camelCase para utilities: `api.ts`

### Variables de Entorno:
- UPPER_SNAKE_CASE: `SUPABASE_URL`, `ANTHROPIC_API_KEY`
- Prefijo `NEXT_PUBLIC_` para variables de frontend

## Archivos Importantes a Conocer

1. **PRPs/marketing-brain-system-v3.md** - PRP completo con 11 tareas
2. **docs/gotchas-detallados-y-soluciones.md** - 10 problemas críticos
3. **contenido/buyer-plantilla.md** - Plantilla de buyer persona
4. **contenido/prompts-mejorados-v2.md** - Prompts con técnicas avanzadas
5. **README.md** - Documentación principal del proyecto
6. **INITIAL.md** - Especificación técnica completa