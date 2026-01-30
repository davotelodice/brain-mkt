-- ========================================
-- MARKETING SECOND BRAIN - BOOK LEARNING SYSTEM
-- ========================================
-- Fecha: 2026-01-30
-- Migración: 003
-- Propósito: Sistema de aprendizaje progresivo desde libros
-- Tablas nuevas: 2 (marketing_learned_books, marketing_book_concepts)
-- Columnas nuevas: 2 en marketing_knowledge_base
-- ========================================

-- ========================================
-- 1. NUEVA TABLA: marketing_learned_books
-- ========================================
-- Metadata de libros procesados para aprendizaje

CREATE TABLE IF NOT EXISTS marketing_learned_books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    file_path VARCHAR(1000),
    file_type VARCHAR(10),
    processing_status VARCHAR(50) DEFAULT 'pending',
    total_chunks INTEGER,
    processed_chunks INTEGER DEFAULT 0,
    global_summary JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT fk_learned_books_project FOREIGN KEY (project_id) 
        REFERENCES marketing_projects(id) ON DELETE CASCADE,
    CONSTRAINT check_processing_status 
        CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'))
);

COMMENT ON TABLE marketing_learned_books IS 'Libros procesados para aprendizaje progresivo';
COMMENT ON COLUMN marketing_learned_books.processing_status IS 'Estado: pending, processing, completed, failed';
COMMENT ON COLUMN marketing_learned_books.global_summary IS 'Resumen global del libro generado por LLM';

-- Índices para marketing_learned_books
CREATE INDEX IF NOT EXISTS idx_learned_books_project 
    ON marketing_learned_books(project_id);
CREATE INDEX IF NOT EXISTS idx_learned_books_status 
    ON marketing_learned_books(processing_status);

-- ========================================
-- 2. NUEVA TABLA: marketing_book_concepts
-- ========================================
-- Conceptos extraídos y estructurados de libros

CREATE TABLE IF NOT EXISTS marketing_book_concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learned_book_id UUID NOT NULL,
    chunk_index INTEGER NOT NULL,
    main_concepts TEXT[],
    relationships TEXT[],
    key_examples TEXT[],
    technical_terms JSONB,
    condensed_text TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_book_concepts_book FOREIGN KEY (learned_book_id) 
        REFERENCES marketing_learned_books(id) ON DELETE CASCADE
);

COMMENT ON TABLE marketing_book_concepts IS 'Conceptos extraídos de chunks de libros';
COMMENT ON COLUMN marketing_book_concepts.main_concepts IS 'Array de conceptos principales extraídos';
COMMENT ON COLUMN marketing_book_concepts.relationships IS 'Relaciones entre conceptos (ej: "A causa B")';
COMMENT ON COLUMN marketing_book_concepts.technical_terms IS 'Términos técnicos con definiciones en JSON';
COMMENT ON COLUMN marketing_book_concepts.condensed_text IS 'Texto condensado del chunk para embedding';

-- Índices para marketing_book_concepts
CREATE INDEX IF NOT EXISTS idx_book_concepts_book 
    ON marketing_book_concepts(learned_book_id);

-- Índice vectorial para búsqueda semántica de conceptos
-- GOTCHA: Usar ivfflat con lists=100 para balance velocidad/precisión
CREATE INDEX IF NOT EXISTS idx_book_concepts_embedding 
    ON marketing_book_concepts 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ========================================
-- 3. EXTENDER marketing_knowledge_base
-- ========================================
-- Agregar columnas para distinguir tipo de conocimiento

-- Columna para distinguir tipo de conocimiento
ALTER TABLE marketing_knowledge_base 
ADD COLUMN IF NOT EXISTS knowledge_type VARCHAR(50) DEFAULT 'raw_chunk';

COMMENT ON COLUMN marketing_knowledge_base.knowledge_type IS 'Tipo: raw_chunk, extracted_concept, thematic_summary';

-- Columna para relacionar con libro aprendido
ALTER TABLE marketing_knowledge_base 
ADD COLUMN IF NOT EXISTS learned_book_id UUID;

-- FK con ON DELETE CASCADE para limpiar automáticamente
-- NOTA: PostgreSQL no soporta "ADD CONSTRAINT IF NOT EXISTS", usamos DO block
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'fk_knowledge_learned_book' 
        AND table_name = 'marketing_knowledge_base'
    ) THEN
        ALTER TABLE marketing_knowledge_base 
        ADD CONSTRAINT fk_knowledge_learned_book 
            FOREIGN KEY (learned_book_id) 
            REFERENCES marketing_learned_books(id) 
            ON DELETE CASCADE;
    END IF;
END $$;

COMMENT ON COLUMN marketing_knowledge_base.learned_book_id IS 'Referencia al libro de origen (si aplica)';

-- Índices nuevos para marketing_knowledge_base
CREATE INDEX IF NOT EXISTS idx_knowledge_type 
    ON marketing_knowledge_base(knowledge_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_learned_book 
    ON marketing_knowledge_base(learned_book_id);

-- ========================================
-- 4. VERIFICACIÓN
-- ========================================

-- Query para verificar que todo se creó correctamente
DO $$
BEGIN
    -- Verificar tabla marketing_learned_books
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'marketing_learned_books') THEN
        RAISE EXCEPTION 'Tabla marketing_learned_books no fue creada';
    END IF;
    
    -- Verificar tabla marketing_book_concepts
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'marketing_book_concepts') THEN
        RAISE EXCEPTION 'Tabla marketing_book_concepts no fue creada';
    END IF;
    
    -- Verificar columna knowledge_type
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'marketing_knowledge_base' AND column_name = 'knowledge_type') THEN
        RAISE EXCEPTION 'Columna knowledge_type no fue creada';
    END IF;
    
    RAISE NOTICE '✅ Migración 003_book_learning_system completada exitosamente';
END $$;
