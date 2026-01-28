-- ========================================
-- 002: Add summary to marketing_user_documents
-- ========================================
-- Ejecutar manualmente en Supabase (VPS) por el usuario.
-- Objetivo: soportar "contexto largo" persistente (resumen) + RAG.

ALTER TABLE IF EXISTS marketing_user_documents
ADD COLUMN IF NOT EXISTS summary TEXT;

COMMENT ON COLUMN marketing_user_documents.summary IS 'Resumen persistente del documento para contexto largo (in-context), además de RAG';

