-- ========================================
-- MARKETING SECOND BRAIN - INITIAL SCHEMA
-- ========================================
-- Fecha: 2026-01-27
-- Base de datos: PostgreSQL 15+ con pgvector
-- Total: 8 tablas con prefijo marketing_
-- ========================================

-- ========================================
-- 1. EXTENSIONES
-- ========================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ========================================
-- 2. TABLAS
-- ========================================

-- Tabla 1: marketing_projects
CREATE TABLE IF NOT EXISTS marketing_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    owner_user_id UUID,  -- FK se añade después de crear marketing_users
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE marketing_projects IS 'Proyectos de marketing (multi-tenancy)';
COMMENT ON COLUMN marketing_projects.owner_user_id IS 'Usuario propietario del proyecto (opcional)';

-- Tabla 2: marketing_users
CREATE TABLE IF NOT EXISTS marketing_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    project_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT fk_users_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE,
    CONSTRAINT unique_email_per_project UNIQUE (email, project_id)
);

COMMENT ON TABLE marketing_users IS 'Usuarios del sistema (autenticación manual, sin Supabase Auth)';
COMMENT ON CONSTRAINT unique_email_per_project ON marketing_users IS 'Un email puede existir en múltiples proyectos';

-- Tabla 3: marketing_chats
CREATE TABLE IF NOT EXISTS marketing_chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    project_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_chats_user FOREIGN KEY (user_id) 
        REFERENCES marketing_users(id) ON DELETE CASCADE,
    CONSTRAINT fk_chats_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_chats IS 'Conversaciones de chat (1 chat = 1 buyer persona)';

-- Tabla 4: marketing_messages
CREATE TABLE IF NOT EXISTS marketing_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL,
    project_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_messages_chat FOREIGN KEY (chat_id) 
        REFERENCES marketing_chats(id) ON DELETE CASCADE,
    CONSTRAINT fk_messages_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_messages IS 'Mensajes de chat (user, assistant, system)';
COMMENT ON COLUMN marketing_messages.metadata IS 'Metadata adicional (ej: tokens_used, model_used)';

-- Tabla 5: marketing_buyer_personas
CREATE TABLE IF NOT EXISTS marketing_buyer_personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL,
    project_id UUID NOT NULL,
    initial_questions JSONB NOT NULL,  -- 4-5 respuestas iniciales
    full_analysis JSONB NOT NULL,      -- 35+ preguntas expandidas
    forum_simulation JSONB NOT NULL,   -- Array de {complaint, desired_solution}
    pain_points JSONB NOT NULL,        -- Array de 10 pain points
    customer_journey JSONB NOT NULL,   -- {awareness, consideration, purchase}
    embedding VECTOR(1536),             -- Embedding del análisis completo
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_personas_chat FOREIGN KEY (chat_id) 
        REFERENCES marketing_chats(id) ON DELETE CASCADE,
    CONSTRAINT fk_personas_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE,
    CONSTRAINT unique_persona_per_chat UNIQUE (chat_id)
);

COMMENT ON TABLE marketing_buyer_personas IS 'Buyer personas completos generados por el agente';
COMMENT ON COLUMN marketing_buyer_personas.embedding IS 'Embedding del full_analysis para búsqueda semántica';

-- Tabla 6: marketing_knowledge_base
CREATE TABLE IF NOT EXISTS marketing_knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID,  -- NULL = conocimiento global (YouTubers + libros)
    chat_id UUID,     -- NULL = conocimiento global
    content_type VARCHAR(50) NOT NULL CHECK (content_type IN ('video_transcript', 'book', 'user_document')),
    source_title VARCHAR(500) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints (FKs opcionales porque project_id y chat_id pueden ser NULL)
    CONSTRAINT fk_kb_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE,
    CONSTRAINT fk_kb_chat FOREIGN KEY (chat_id) 
        REFERENCES marketing_chats(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_knowledge_base IS 'Base de conocimiento RAG (global + documentos de usuario)';
COMMENT ON COLUMN marketing_knowledge_base.project_id IS 'NULL = conocimiento global (YouTubers + libros)';
COMMENT ON COLUMN marketing_knowledge_base.chat_id IS 'NULL = conocimiento global, NOT NULL = documento de usuario';

-- Tabla 7: marketing_user_documents
CREATE TABLE IF NOT EXISTS marketing_user_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL,
    project_id UUID NOT NULL,
    user_id UUID NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL CHECK (file_type IN ('.txt', '.pdf', '.docx')),
    file_size INTEGER NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    chunks_count INTEGER NOT NULL DEFAULT 0,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_docs_chat FOREIGN KEY (chat_id) 
        REFERENCES marketing_chats(id) ON DELETE CASCADE,
    CONSTRAINT fk_docs_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE,
    CONSTRAINT fk_docs_user FOREIGN KEY (user_id) 
        REFERENCES marketing_users(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_user_documents IS 'Tracking de documentos subidos por usuarios (.txt, .pdf, .docx)';
COMMENT ON COLUMN marketing_user_documents.processed IS 'TRUE cuando chunks están en marketing_knowledge_base';

-- Tabla 8: marketing_password_reset_tokens
CREATE TABLE IF NOT EXISTS marketing_password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    project_id UUID NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_reset_user FOREIGN KEY (user_id) 
        REFERENCES marketing_users(id) ON DELETE CASCADE,
    CONSTRAINT fk_reset_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_password_reset_tokens IS 'Tokens para recuperación de contraseña (expiran en 1 hora)';

-- ========================================
-- 3. FOREIGN KEY CIRCULAR (marketing_projects.owner_user_id)
-- ========================================

ALTER TABLE marketing_projects
ADD CONSTRAINT fk_projects_owner 
FOREIGN KEY (owner_user_id) 
REFERENCES marketing_users(id) ON DELETE SET NULL;

-- ========================================
-- 4. ÍNDICES
-- ========================================

-- marketing_users
CREATE INDEX IF NOT EXISTS idx_users_email_project 
ON marketing_users(email, project_id);

CREATE INDEX IF NOT EXISTS idx_users_project 
ON marketing_users(project_id);

-- marketing_chats
CREATE INDEX IF NOT EXISTS idx_chats_user_project 
ON marketing_chats(user_id, project_id);

CREATE INDEX IF NOT EXISTS idx_chats_created_at 
ON marketing_chats(created_at DESC);

-- marketing_messages
CREATE INDEX IF NOT EXISTS idx_messages_chat 
ON marketing_messages(chat_id, created_at);

CREATE INDEX IF NOT EXISTS idx_messages_project 
ON marketing_messages(project_id);

-- marketing_buyer_personas
CREATE INDEX IF NOT EXISTS idx_personas_chat 
ON marketing_buyer_personas(chat_id);

CREATE INDEX IF NOT EXISTS idx_personas_project 
ON marketing_buyer_personas(project_id);

-- ÍNDICE VECTORIAL HNSW para embedding (GOTCHA 1: usar HNSW en vez de IVFFlat)
CREATE INDEX IF NOT EXISTS idx_personas_embedding_hnsw 
ON marketing_buyer_personas 
USING hnsw (embedding vector_cosine_ops);

COMMENT ON INDEX idx_personas_embedding_hnsw IS 'HNSW index para búsqueda vectorial (mejor que IVFFlat para datasets pequeños)';

-- marketing_knowledge_base
CREATE INDEX IF NOT EXISTS idx_kb_content_type 
ON marketing_knowledge_base(content_type);

CREATE INDEX IF NOT EXISTS idx_kb_project_chat 
ON marketing_knowledge_base(project_id, chat_id);

-- ÍNDICE VECTORIAL HNSW para embedding (GOTCHA 1)
CREATE INDEX IF NOT EXISTS idx_kb_embedding_hnsw 
ON marketing_knowledge_base 
USING hnsw (embedding vector_cosine_ops);

COMMENT ON INDEX idx_kb_embedding_hnsw IS 'HNSW index para búsqueda vectorial RAG';

-- marketing_user_documents
CREATE INDEX IF NOT EXISTS idx_docs_chat_user 
ON marketing_user_documents(chat_id, user_id);

CREATE INDEX IF NOT EXISTS idx_docs_project 
ON marketing_user_documents(project_id);

CREATE INDEX IF NOT EXISTS idx_docs_processed 
ON marketing_user_documents(processed) WHERE processed = FALSE;

-- marketing_password_reset_tokens
CREATE INDEX IF NOT EXISTS idx_reset_token 
ON marketing_password_reset_tokens(token) WHERE used = FALSE;

CREATE INDEX IF NOT EXISTS idx_reset_user_used 
ON marketing_password_reset_tokens(user_id, used);

-- ========================================
-- 5. FUNCIÓN DE BÚSQUEDA VECTORIAL
-- ========================================

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
        kb.chunk_text AS content,
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

COMMENT ON FUNCTION marketing_match_documents IS 'Búsqueda semántica en knowledge base (global + documentos de usuario)';

-- ========================================
-- 6. ROW LEVEL SECURITY (RLS)
-- ========================================

-- NOTA: Deshabilitado por ahora porque usamos autenticación manual (sin Supabase Auth)
-- Las políticas RLS requieren auth.uid() que solo está disponible con Supabase Auth
-- En su lugar, filtramos por project_id en las queries del backend

-- Si en el futuro migramos a Supabase Auth, descomentar:
/*
ALTER TABLE marketing_chats ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only see their own chats"
ON marketing_chats
FOR SELECT
USING (user_id = auth.uid() AND project_id = current_setting('app.current_project_id')::UUID);

-- Repetir para todas las tablas relevantes
*/

-- ========================================
-- 7. TRIGGERS (updated_at automático)
-- ========================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para marketing_projects
CREATE TRIGGER update_projects_updated_at
BEFORE UPDATE ON marketing_projects
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para marketing_chats
CREATE TRIGGER update_chats_updated_at
BEFORE UPDATE ON marketing_chats
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 8. PROYECTO DE PRUEBA
-- ========================================

INSERT INTO marketing_projects (id, name, created_at, updated_at)
VALUES (
    'a0000000-0000-0000-0000-000000000001'::UUID,
    'Test Project',
    NOW(),
    NOW()
)
ON CONFLICT (id) DO NOTHING;

COMMENT ON TABLE marketing_projects IS 'Proyecto de prueba creado con ID fijo para development';

-- ========================================
-- 9. RESUMEN
-- ========================================

-- Verificar que todas las tablas fueron creadas
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'marketing_%';
    
    RAISE NOTICE 'Total de tablas marketing_*: %', table_count;
    
    IF table_count <> 8 THEN
        RAISE WARNING 'Se esperaban 8 tablas, pero se crearon %', table_count;
    ELSE
        RAISE NOTICE '✅ Todas las tablas fueron creadas correctamente';
    END IF;
END $$;

-- Listar tablas creadas
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns 
     WHERE table_name = t.table_name) AS column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_name LIKE 'marketing_%'
ORDER BY table_name;
