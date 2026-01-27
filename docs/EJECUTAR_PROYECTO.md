# 🚀 Guía de Ejecución - Marketing Second Brain

Instrucciones para ejecutar el proyecto completo (Backend + Frontend).

## 📋 Pre-requisitos

- ✅ Python 3.11+
- ✅ Node.js 18+
- ✅ PostgreSQL con pgvector (Supabase o local)
- ✅ Variables de entorno configuradas (`.env`)

---

## 🎯 Inicio Rápido (Desarrollo)

### Terminal 1: Backend (FastAPI)

```bash
cd backend
python run.py

# Esperado:
# INFO:     Uvicorn running on http://localhost:8000
# INFO:     Application startup complete.
```

### Terminal 2: Frontend (Next.js)

```bash
cd frontend
npm run dev

# Esperado:
# ✓ Ready in 1.5s
# ○ Local:        http://localhost:3000
# ✓ Compiled in 500ms (Turbopack)
```

### Terminal 3: Verificar Health

```bash
# Backend health
curl http://localhost:8000/health
# Esperado: {"status":"healthy"}

# Frontend (debería redirigir a /login)
curl -L http://localhost:3000
```

---

## 🧪 Testing de Autenticación

### Opción 1: Navegador

1. Abre `http://localhost:3000`
2. Deberías ser redirigido a `/login`
3. Click en "¿No tienes cuenta? Regístrate"
4. Registra usuario:
   - Email: `tu@email.com`
   - Password: `TuPassword123` (mín 8, 1 mayúscula, 1 número)
   - Full Name: `Tu Nombre`
   - Project ID: `a0000000-0000-0000-0000-000000000001` (Test Project)
5. Login con las mismas credenciales
6. Deberías ver el dashboard principal

### Opción 2: Script Automatizado

```bash
# Asegúrate que backend y frontend estén corriendo
./frontend/test-auth-flow.sh

# Esperado:
# ✅ Backend corriendo
# ✅ Frontend corriendo
# ✅ Registro exitoso
# ✅ Login exitoso (token recibido)
# ✅ Cookie 'auth_token' seteada
# ✅ Logout exitoso
```

---

## 🔧 Comandos Útiles

### Backend

```bash
cd backend

# Ejecutar tests
pytest

# Ejecutar tests con coverage
pytest --cov=src --cov-report=html

# Lint
ruff check src/ --fix

# Type check
mypy src/ --config-file=mypy.ini

# Ingestar datos de entrenamiento (RAG)
python scripts/ingest_training_data.py

# Test búsqueda semántica
python scripts/test_semantic_search.py

# Test streaming SSE
./scripts/test_streaming_endpoint.sh
```

### Frontend

```bash
cd frontend

# Build para producción
npm run build

# Lint
npm run lint

# Test auth flow
./test-auth-flow.sh
```

---

## 🌐 URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI (automático) |
| **Health Check** | http://localhost:8000/health | Status del backend |
| **Frontend** | http://localhost:3000 | Next.js App |
| **Login** | http://localhost:3000/login | Página de login |
| **Register** | http://localhost:3000/register | Página de registro |

---

## 🔐 Flujo de Autenticación (Cookies httpOnly)

```
User → Frontend /login
         ↓
    POST /api/auth/login (email, password)
         ↓
    Backend valida credenciales
         ↓
    Backend setea cookie: auth_token (httpOnly)
         ↓
    Frontend redirect a /
         ↓
    Next.js middleware lee cookie
         ↓
    Acceso permitido a rutas privadas
```

---

## 📊 Estado Actual del Proyecto

```
✅ TAREA 0-6: Base de datos, Backend API, Agentes IA, RAG, Streaming
✅ TAREA 7: Frontend Auth (Actual)
⏳ TAREA 8: Frontend Chat Interface
⏳ TAREA 9-11: MCP, Docker, Testing Completo
```

---

## ⚠️ Troubleshooting

### Backend no inicia

```bash
# Verificar variables de entorno
cat .env | grep -E "SUPABASE_DB_URL|JWT_SECRET_KEY|OPENAI_API_KEY"

# Verificar conexión a base de datos
psql $SUPABASE_DB_URL -c "SELECT 1"
```

### Frontend no inicia

```bash
# Re-instalar dependencias
cd frontend
rm -rf node_modules package-lock.json
npm install

# Limpiar caché de Next.js
rm -rf .next
npm run dev
```

### Cookies no funcionan

1. Verifica CORS en `backend/src/main.py`:
   ```python
   ALLOWED_ORIGINS = ["http://localhost:3000"]
   ```

2. Verifica que frontend usa `credentials: 'include'` en fetch

3. Verifica cookie en DevTools:
   - Chrome → Application → Cookies → http://localhost:3000
   - Debería ver `auth_token` con HttpOnly = ✓

---

## 🚢 Deployment (Futuro - TAREA 10)

- **Backend:** Docker container en VPS/Cloud
- **Frontend:** Vercel (deployment automático desde GitHub)
- **Base de datos:** Supabase (PostgreSQL con pgvector)

---

Para más información, ver documentación específica:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Streaming API: `backend/docs/STREAMING_API.md`
- Tareas pendientes: `docs/TAREAS_PENDIENTES_Y_GOTCHAS.md`
