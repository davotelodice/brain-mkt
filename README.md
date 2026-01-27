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
| 📚 **RAG con Conocimiento Experto** | Base de datos con transcripciones de YouTubers y libros de marketing |
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
├── docker-compose.yml                  # Orquestación de servicios
│
├── frontend/                           # Next.js 14 App
│   ├── app/                            # App Router
│   ├── components/                     # Componentes React
│   ├── lib/                            # Utilidades
│   └── Dockerfile
│
├── backend/                            # FastAPI App
│   ├── src/
│   │   ├── api/                        # Endpoints (auth, chat, documents)
│   │   ├── agents/                     # Agentes IA (router, buyer_persona, etc.)
│   │   ├── services/                   # LLM, embeddings, vector search
│   │   ├── db/                         # Models, migrations
│   │   ├── schemas/                    # Pydantic schemas
│   │   └── utils/                      # JWT, password, file parsers
│   ├── scripts/
│   │   └── ingest_training_data.py     # Procesar transcripciones
│   ├── tests/                          # Tests unitarios + integración
│   └── Dockerfile
│
├── contenido/                          # Material de entrenamiento
│   ├── buyer-plantilla.md              # Plantilla de buyer persona (11 categorías)
│   ├── promts_borradores.md            # Prompts v1.0 (originales)
│   ├── prompts-mejorados-v2.md         # Prompts v2.0 (con técnicas avanzadas)
│   └── Transcriptions Andrea Estratega/  # 9 transcripciones de YouTube
│
├── docs/                               # Documentación técnica
│   ├── gotchas-detallados-y-soluciones.md      # 10 gotchas críticos
│   ├── supabase-self-hosted-setup.md           # Guía de instalación Supabase
│   └── architecture.md                         # Arquitectura del sistema (TBD)
│
├── PRPs/                               # Product Requirement Prompts
│   └── marketing-brain-system-v3.md    # PRP completo del proyecto
│
└── Context-Engineering-Intro/         # Ejemplos y templates de referencia
    ├── examples/
    ├── PRPs/
    └── validation/
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

# Asegúrate de tener:
# - SUPABASE_URL
# - SUPABASE_SERVICE_ROLE_KEY
# - ANTHROPIC_API_KEY
# - OPENAI_API_KEY
# - JWT_SECRET_KEY (ya generada en .env.example)
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
# Construir imágenes
docker compose build

# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Verificar que todo está corriendo
docker compose ps
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

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

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

### 📊 Base de Datos

**Tablas principales:**
- `marketing_projects`: Proyectos (multi-tenancy)
- `marketing_users`: Usuarios con autenticación manual (JWT)
- `marketing_chats`: Conversaciones
- `marketing_messages`: Mensajes individuales
- `marketing_buyer_personas`: Buyer personas generados
- `marketing_knowledge_base`: Base de conocimiento vectorial
- `marketing_user_documents`: Documentos subidos

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

### "Cannot connect to database"
```bash
# Verificar que Supabase está corriendo
docker compose ps | grep supabase

# Ver logs
docker compose logs backend
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

Más soluciones: `docs/gotchas-detallados-y-soluciones.md`

---

## 📈 Roadmap

### ✅ Fase 1 - MVP (Completado)
- [ ] Base de datos configurada
- [ ] Backend con autenticación
- [ ] Agente IA con memoria
- [ ] Frontend básico

### 🔄 Fase 2 - Features Avanzadas (En progreso)
- [ ] Upload de documentos
- [ ] Streaming de respuestas
- [ ] Mejora de prompts (v2.0 con técnicas avanzadas)

### 🚀 Fase 3 - Production Ready (Planeado)
- [ ] MCP custom del proyecto
- [ ] Docker + deployment
- [ ] Testing end-to-end
- [ ] Documentación completa

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

**Última actualización**: 2026-01-26  
**Versión**: 1.0.0 (MVP)
