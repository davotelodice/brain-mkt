# 🚀 Guía de Instalación: Supabase Self-Hosted en VPS

> **Proyecto**: Marketing Second Brain System  
> **Fecha**: 2026-01-26  
> **Para**: Usuario con Supabase self-hosted en VPS

---

## 📋 Requisitos Previos

- ✅ VPS con Ubuntu 20.04+ (o Debian 10+)
- ✅ Mínimo 4GB RAM, 2 CPU cores, 40GB almacenamiento
- ✅ Docker y Docker Compose instalados
- ✅ Dominio o IP pública accesible
- ✅ Acceso root o sudo

---

## 1. 🐳 Instalar Docker y Docker Compose (si no lo tienes)

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Añadir repo de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verificar instalación
docker --version
docker compose version

# Añadir usuario al grupo docker (opcional, para no usar sudo)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 2. 📦 Descargar Supabase Self-Hosted

```bash
# Ir al directorio home
cd ~

# Clonar repo oficial de Supabase
git clone --depth 1 https://github.com/supabase/supabase.git

# Ir al directorio de Docker
cd supabase/docker

# Ver archivos
ls -la
# Esperado:
# - docker-compose.yml
# - .env.example
# - volumes/
```

---

## 3. ⚙️ Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar configuración
nano .env
```

### Configuración Mínima Necesaria:

```bash
# ========================================
# SUPABASE SELF-HOSTED - CONFIGURACIÓN
# ========================================

# 1. PostgreSQL Database
POSTGRES_PASSWORD=tu-password-seguro-aqui  # ⚠️ CAMBIAR
POSTGRES_PORT=5432
POSTGRES_DB=postgres

# 2. API URLs (reemplazar IP con tu VPS)
SUPABASE_PUBLIC_URL=http://TU-VPS-IP:8000
API_EXTERNAL_URL=http://TU-VPS-IP:8000

# 3. JWT Secret (para autenticación interna de Supabase)
# Generar con: openssl rand -base64 32
JWT_SECRET=tu-jwt-secret-aqui  # ⚠️ CAMBIAR

# 4. Service Role Key (para backend)
# Generar con: openssl rand -base64 32
SERVICE_ROLE_KEY=tu-service-role-key-aqui  # ⚠️ CAMBIAR

# 5. Anon Key (para frontend - NO USAR en nuestro caso)
ANON_KEY=tu-anon-key-aqui  # ⚠️ CAMBIAR

# 6. Dashboard Auth (para acceder a Supabase Studio)
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=tu-password-dashboard  # ⚠️ CAMBIAR

# 7. SMTP (opcional, para emails)
SMTP_ADMIN_EMAIL=tu-email@ejemplo.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASS=tu-password-smtp
SMTP_SENDER_NAME=Marketing Brain

# 8. Storage
STORAGE_BACKEND=file  # file | s3
```

### Generar Claves Seguras:

```bash
# Generar POSTGRES_PASSWORD
openssl rand -base64 32

# Generar JWT_SECRET
openssl rand -base64 32

# Generar SERVICE_ROLE_KEY
openssl rand -base64 32

# Generar ANON_KEY
openssl rand -base64 32
```

---

## 4. 🚀 Iniciar Supabase

```bash
# Asegurarse de estar en supabase/docker/
cd ~/supabase/docker

# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Verificar que todos los contenedores están corriendo
docker compose ps

# Esperado (todos "Up"):
# - supabase-db (PostgreSQL)
# - supabase-studio (Dashboard)
# - supabase-auth (GoTrue)
# - supabase-rest (PostgREST)
# - supabase-realtime
# - supabase-storage
# - supabase-meta
# - supabase-imgproxy
# - supabase-kong (API Gateway)
```

---

## 5. 🔌 Habilitar pgvector en PostgreSQL

```bash
# Conectar a PostgreSQL
docker exec -it supabase-db psql -U postgres

# Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

# Verificar
SELECT * FROM pg_extension WHERE extname = 'vector';

# Esperado:
#  extname | extowner | extnamespace | extrelocatable | extversion 
# ---------+----------+--------------+----------------+------------
#  vector  | ...      | ...          | f              | 0.5.1

# Salir
\q
```

---

## 6. 🌐 Verificar Acceso

```bash
# Verificar que servicios están accesibles
curl http://localhost:8000/rest/v1/

# Esperado: {"message":"success"}

# Acceder a Supabase Studio (Dashboard)
# http://TU-VPS-IP:3000
# Credenciales: DASHBOARD_USERNAME / DASHBOARD_PASSWORD del .env
```

---

## 7. 🔐 Obtener Credenciales para el Proyecto

Una vez Supabase esté corriendo:

```bash
# 1. SUPABASE_URL
echo "SUPABASE_URL=http://$(curl -s ifconfig.me):8000"

# 2. SUPABASE_SERVICE_ROLE_KEY
# Obtener del .env
grep SERVICE_ROLE_KEY ~/supabase/docker/.env

# 3. SUPABASE_DB_URL
echo "SUPABASE_DB_URL=postgresql://postgres:$(grep POSTGRES_PASSWORD ~/supabase/docker/.env | cut -d'=' -f2)@$(curl -s ifconfig.me):5432/postgres"
```

### Añadir a `/home/david/brain-mkt/.env`:

```bash
# Copiar valores obtenidos arriba
SUPABASE_URL=http://TU-VPS-IP:8000
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key-del-env
SUPABASE_DB_URL=postgresql://postgres:tu-password@TU-VPS-IP:5432/postgres
```

---

## 8. 🔥 Configurar Firewall (Seguridad)

```bash
# Habilitar UFW (Uncomplicated Firewall)
sudo ufw enable

# Permitir SSH (¡IMPORTANTE! No te bloquees)
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Permitir puertos de Supabase
sudo ufw allow 8000/tcp  # API Gateway (Kong)
sudo ufw allow 5432/tcp  # PostgreSQL
sudo ufw allow 3000/tcp  # Supabase Studio (opcional, solo para admin)

# Verificar reglas
sudo ufw status

# Esperado:
# Status: active
# To                         Action      From
# --                         ------      ----
# 22/tcp                     ALLOW       Anywhere
# 8000/tcp                   ALLOW       Anywhere
# 5432/tcp                   ALLOW       Anywhere
# 3000/tcp                   ALLOW       Anywhere
```

**⚠️ IMPORTANTE DE SEGURIDAD:**
```bash
# Si Supabase Studio (puerto 3000) es solo para admin:
# Cerrar puerto 3000 después de configuración inicial
sudo ufw deny 3000/tcp

# O permitir solo desde tu IP
sudo ufw allow from TU-IP-LOCAL to any port 3000
```

---

## 9. 📊 Crear Tablas del Proyecto

```bash
# Conectar a PostgreSQL
docker exec -it supabase-db psql -U postgres

# O desde tu máquina local (si puerto 5432 está abierto)
psql postgresql://postgres:tu-password@TU-VPS-IP:5432/postgres
```

### SQL a ejecutar (desde TAREA 1 del PRP):

```sql
-- 1. Habilitar pgvector (ya hecho en paso 5)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear tablas del proyecto
-- (Copiar SQL completo desde PRPs/marketing-brain-system-v3.md TAREA 1)

CREATE TABLE marketing_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_user_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    UNIQUE(email, project_id)
);

CREATE TABLE marketing_chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES marketing_users(id) NOT NULL,
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    title VARCHAR(255) DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID REFERENCES marketing_chats(id) ON DELETE CASCADE NOT NULL,
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_buyer_personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID REFERENCES marketing_chats(id) NOT NULL,
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    initial_questions JSONB NOT NULL,
    full_analysis JSONB NOT NULL,
    forum_simulation JSONB NOT NULL,
    pain_points JSONB NOT NULL,
    customer_journey JSONB NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES marketing_projects(id),
    chat_id UUID REFERENCES marketing_chats(id),
    content_type VARCHAR(50) NOT NULL,
    source_title VARCHAR(500) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_user_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID REFERENCES marketing_chats(id) ON DELETE CASCADE NOT NULL,
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    user_id UUID REFERENCES marketing_users(id) NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    chunks_count INTEGER DEFAULT 0,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE marketing_password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES marketing_users(id) NOT NULL,
    project_id UUID REFERENCES marketing_projects(id) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE
);

-- 3. Crear índices
CREATE INDEX idx_users_email_project ON marketing_users(email, project_id);
CREATE INDEX idx_chats_user_project ON marketing_chats(user_id, project_id);
CREATE INDEX idx_chats_created ON marketing_chats(created_at DESC);
CREATE INDEX idx_messages_chat_created ON marketing_messages(chat_id, created_at);
CREATE INDEX idx_messages_project ON marketing_messages(project_id);
CREATE INDEX idx_buyer_personas_chat ON marketing_buyer_personas(chat_id);
CREATE INDEX idx_buyer_personas_project ON marketing_buyer_personas(project_id);
CREATE INDEX idx_buyer_personas_embedding ON marketing_buyer_personas USING hnsw(embedding vector_cosine_ops);
CREATE INDEX idx_knowledge_base_content_type ON marketing_knowledge_base(content_type);
CREATE INDEX idx_knowledge_base_project_chat ON marketing_knowledge_base(project_id, chat_id);
CREATE INDEX idx_knowledge_base_embedding_hnsw ON marketing_knowledge_base USING hnsw(embedding vector_cosine_ops);
CREATE INDEX idx_user_documents_chat ON marketing_user_documents(chat_id);
CREATE INDEX idx_user_documents_user_project ON marketing_user_documents(user_id, project_id);

-- 4. Crear función de búsqueda vectorial
CREATE OR REPLACE FUNCTION marketing_match_documents(
    query_embedding vector(1536),
    match_project_id UUID,
    match_chat_id UUID,
    match_count INT,
    match_threshold FLOAT
)
RETURNS TABLE(
    id UUID,
    content_type VARCHAR,
    source_title VARCHAR,
    chunk_text TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.id,
        kb.content_type,
        kb.source_title,
        kb.chunk_text,
        kb.metadata,
        1 - (kb.embedding <=> query_embedding) AS similarity
    FROM marketing_knowledge_base kb
    WHERE
        (kb.project_id = match_project_id OR kb.project_id IS NULL)
        AND (kb.chat_id = match_chat_id OR kb.chat_id IS NULL)
        AND 1 - (kb.embedding <=> query_embedding) > match_threshold
    ORDER BY kb.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 5. Crear políticas RLS (opcional, ya que usamos service role key)
-- Nota: Service role key bypasea RLS, pero las creamos por consistencia
ALTER TABLE marketing_chats ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_buyer_personas ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_user_documents ENABLE ROW LEVEL SECURITY;

-- ✅ LISTO! Base de datos configurada
```

---

## 10. 🔍 Verificar Configuración

```bash
# 1. Verificar tablas creadas
docker exec -it supabase-db psql -U postgres -c "\dt"

# Esperado: Ver todas las tablas marketing_*

# 2. Verificar extensión pgvector
docker exec -it supabase-db psql -U postgres -c "SELECT * FROM pg_extension WHERE extname='vector';"

# Esperado: Ver registro de pgvector

# 3. Verificar índices HNSW
docker exec -it supabase-db psql -U postgres -c "\d+ marketing_knowledge_base"

# Esperado: Ver índice HNSW en columna embedding

# 4. Probar función de búsqueda
docker exec -it supabase-db psql -U postgres -c "SELECT marketing_match_documents(NULL, NULL, NULL, 1, 0.5);"

# Esperado: Función existe (aunque retorna vacío por NULL)
```

---

## 11. 🔄 Comandos Útiles de Administración

```bash
# Ver logs de Supabase
cd ~/supabase/docker
docker compose logs -f

# Reiniciar servicios
docker compose restart

# Detener Supabase
docker compose down

# Detener y BORRAR datos (⚠️ CUIDADO)
docker compose down -v

# Backup de la base de datos
docker exec -it supabase-db pg_dump -U postgres postgres > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i supabase-db psql -U postgres postgres < backup_20260126.sql

# Actualizar Supabase a nueva versión
cd ~/supabase/docker
git pull origin master
docker compose pull
docker compose up -d
```

---

## 12. 🚨 Solución de Problemas Comunes

### Problema: "Cannot connect to PostgreSQL"
```bash
# Verificar que el contenedor está corriendo
docker compose ps | grep supabase-db

# Ver logs de PostgreSQL
docker compose logs supabase-db

# Reiniciar contenedor
docker compose restart supabase-db
```

### Problema: "pgvector not found"
```bash
# Reinstalar pgvector
docker exec -it supabase-db psql -U postgres -c "DROP EXTENSION IF EXISTS vector CASCADE;"
docker exec -it supabase-db psql -U postgres -c "CREATE EXTENSION vector;"
```

### Problema: "Out of memory"
```bash
# Ver uso de recursos
docker stats

# Aumentar memoria de PostgreSQL
nano ~/supabase/docker/.env
# Añadir: POSTGRES_SHARED_BUFFERS=512MB
# Añadir: POSTGRES_EFFECTIVE_CACHE_SIZE=2GB

# Reiniciar
docker compose restart
```

### Problema: "Connection refused from external IP"
```bash
# Verificar firewall
sudo ufw status

# Verificar que puertos están escuchando
sudo netstat -tulpn | grep -E '8000|5432'

# Verificar configuración de Docker
docker compose ps
```

---

## 13. ✅ Checklist Final

- [ ] Supabase corriendo en VPS
- [ ] pgvector habilitado
- [ ] Todas las tablas creadas
- [ ] Índices HNSW configurados
- [ ] Función `marketing_match_documents` creada
- [ ] Firewall configurado
- [ ] Credenciales guardadas en `.env`
- [ ] Backup automático configurado (opcional)
- [ ] Monitoreo configurado (opcional)

---

## 14. 📚 Referencias

- [Supabase Self-Hosting Guide](https://supabase.com/docs/guides/self-hosting)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Última actualización**: 2026-01-26  
**Mantenido por**: AI Agent + Usuario
