# Marketing Second Brain - Backend

Backend API para el sistema Marketing Second Brain.

## Stack Tecnológico

- **Framework**: FastAPI 0.109+
- **Python**: 3.11+
- **Database**: PostgreSQL 15+ con pgvector
- **ORM**: SQLAlchemy 2.0 (async)
- **Autenticación**: JWT manual (sin Supabase Auth)
- **AI**: LangChain + LangGraph (futuro)
- **Cache**: Redis

## Estructura del Proyecto

```
backend/
├── src/
│   ├── api/          # Endpoints REST
│   ├── agents/       # Agentes IA (futuro)
│   ├── db/           # Database models y conexión
│   ├── services/     # Lógica de negocio (futuro)
│   ├── schemas/      # Pydantic schemas
│   ├── middleware/   # Middleware (auth, etc.)
│   └── utils/        # Utilidades (password, jwt)
├── tests/            # Tests unitarios e integración
├── scripts/          # Scripts de utilidad
├── pyproject.toml    # Configuración del proyecto
└── run.py            # Ejecutar servidor
```

## Instalación

```bash
# Instalar dependencias
pip install -e .

# Para desarrollo
pip install -e ".[dev]"
```

## Variables de Entorno

Copiar `.env.example` del root del proyecto y configurar:

```bash
# Database
SUPABASE_DB_URL=postgresql://...

# JWT
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# OpenAI (para embeddings)
OPENAI_API_KEY=...

# Backend
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
BACKEND_CORS_ORIGINS=http://localhost:3000
```

## Ejecutar

```bash
# Desarrollo (con hot reload)
python run.py

# Producción
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Autenticación

- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Login y obtener JWT
- `POST /api/auth/request-password-reset` - Solicitar reset de password
- `POST /api/auth/reset-password` - Resetear password con token

### Health

- `GET /` - Root endpoint
- `GET /health` - Health check

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Solo unitarios
pytest tests/unit/

# Solo integración
pytest tests/integration/
```

## Linting y Type Checking

```bash
# Linting con ruff
ruff check src/ --fix

# Type checking con mypy
mypy src/
```

## Estructura de Base de Datos

8 tablas con prefijo `marketing_`:

1. `marketing_projects` - Proyectos (multi-tenancy)
2. `marketing_users` - Usuarios
3. `marketing_chats` - Chats
4. `marketing_messages` - Mensajes
5. `marketing_buyer_personas` - Buyer personas
6. `marketing_knowledge_base` - Base de conocimiento RAG
7. `marketing_user_documents` - Documentos subidos
8. `marketing_password_reset_tokens` - Tokens de reset

## Próximos Pasos

- [ ] TAREA 3: Sistema de Chat Básico (CRUD)
- [ ] TAREA 4: Agentes IA con Memoria
- [ ] TAREA 5: Entrenamiento RAG
- [ ] TAREA 6: API Streaming (SSE)

## Documentación API

Una vez el servidor esté corriendo, visita:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
