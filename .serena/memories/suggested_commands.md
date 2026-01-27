# Comandos Sugeridos para el Proyecto

## 🚀 Setup Inicial

```bash
# Clonar repositorio
git clone <repo-url>
cd brain-mkt

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con credenciales

# Construir servicios Docker
docker compose build

# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Verificar estado
docker compose ps
```

## 📊 Base de Datos (Supabase)

```bash
# Conectar a PostgreSQL
psql $SUPABASE_DB_URL

# Ejecutar migraciones (desde SQL del PRP)
# Ver: PRPs/marketing-brain-system-v3.md
# Sección: "TAREA 1: Configurar Base de Datos en Supabase"

# Verificar tablas creadas
psql $SUPABASE_DB_URL -c "\dt marketing_*"

# Verificar extensión pgvector
psql $SUPABASE_DB_URL -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

## 🐍 Backend (Python + FastAPI)

```bash
# Entrar al contenedor backend
docker compose exec backend bash

# Instalar dependencias (si no están en Docker)
pip install -r requirements.txt

# Iniciar servidor en desarrollo (dentro del contenedor)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Ejecutar migraciones de Alembic
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Ingestar material de entrenamiento
python scripts/ingest_training_data.py \
  --source "contenido/Transcriptions Andrea Estratega/" \
  --content-type video_transcript
```

## ⚛️ Frontend (Next.js 14)

```bash
# Entrar al contenedor frontend
docker compose exec frontend bash

# Instalar dependencias
npm install

# Iniciar desarrollo
npm run dev

# Build para producción
npm run build

# Iniciar producción
npm start
```

## ✅ Validación (3 Niveles)

### Nivel 1: Sintaxis & Estilo

```bash
# Backend (Python)
ruff check backend/src/ --fix
mypy backend/src/

# Frontend (TypeScript)
cd frontend
npx eslint app/ --fix
npx tsc --noEmit
```

### Nivel 2: Tests Unitarios

```bash
# Backend
docker compose exec backend pytest tests/ -v

# Con cobertura
docker compose exec backend pytest tests/ -v --cov=src --cov-report=html

# Test específico
docker compose exec backend pytest tests/test_auth.py -v

# Frontend
cd frontend
npm test
npm test -- --coverage
```

### Nivel 3: Tests de Integración

```bash
# Test completo del flujo
# (Ver sección "Nivel 3: Test de Integración" en PRP)

# 1. Iniciar servicios
docker compose up -d

# 2. Registrar usuario
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","full_name":"Test","project_id":"<uuid>"}'

# 3. Login y obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","project_id":"<uuid>"}' \
  | jq -r '.access_token')

# 4. Crear chat
CHAT_ID=$(curl -X POST http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}' \
  | jq -r '.id')

# 5. Enviar mensaje
curl -X POST http://localhost:8000/api/chats/$CHAT_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Mi negocio es una tienda online de productos eco-friendly"}'

# 6. Acceder al frontend
open http://localhost:3000
```

## 🐛 Debugging

```bash
# Ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f redis

# Reiniciar un servicio
docker compose restart backend

# Reconstruir servicios
docker compose down
docker compose build --no-cache
docker compose up -d

# Limpiar todo (CUIDADO: borra volúmenes)
docker compose down -v
```

## 📚 Acceso a Documentación

```bash
# API Docs (Swagger UI)
open http://localhost:8000/docs

# API Docs (ReDoc)
open http://localhost:8000/redoc

# Frontend
open http://localhost:3000
```

## 🔧 Herramientas de Sistema (Linux)

```bash
# Listar archivos
ls -lah

# Buscar archivos
find . -name "*.py"

# Buscar en contenido
grep -r "pattern" backend/src/

# Git
git status
git add .
git commit -m "mensaje"
git push

# Permisos
chmod +x script.sh

# Procesos
ps aux | grep python
kill -9 <pid>
```

## 📄 Serena MCP (Análisis de Código)

```bash
# Ver estructura de directorio sin leer archivos
get_symbols_overview('backend/src/agents/')

# Buscar símbolo específico
find_symbol('BuyerPersonaAgent/generate_analysis', 'backend/src/agents/buyer_persona_agent.py', True)

# Buscar patrón
search_for_pattern('async def.*chat', 'backend/src/')

# Ver referencias de un símbolo
find_referencing_symbols('ChatService', 'backend/src/services/chat_service.py')
```

## 🎯 Archon MCP (Documentación)

```bash
# Listar fuentes disponibles
rag_get_available_sources()

# Buscar en documentación (ejemplos)
rag_search_knowledge_base("fastapi streaming response", "c889b62860c33a44", 5)
rag_search_knowledge_base("pydantic nested validation", "9d46e91458092424", 5)
rag_search_knowledge_base("langchain agent memory", "e74f94bb9dcb14aa", 10)
rag_search_knowledge_base("supabase pgvector index", "9c5f534e51ee9237", 8)

# Buscar ejemplos de código
rag_search_code_examples("pydantic validator custom", "9d46e91458092424", 3)
```

## 📦 Gestión de Dependencias

```bash
# Backend (Python)
docker compose exec backend pip list
docker compose exec backend pip freeze > requirements.txt

# Frontend (Node)
cd frontend
npm list
npm outdated
npm update
```

## 🏭 Deployment Local

```bash
# Iniciar todo
./scripts/docker-up.sh

# Construir imágenes
./scripts/docker-build.sh

# Ver logs
./scripts/docker-logs.sh

# Parar todo
docker compose down

# Parar y eliminar volúmenes
docker compose down -v
```