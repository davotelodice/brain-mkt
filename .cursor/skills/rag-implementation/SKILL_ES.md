---
name: rag-implementation
description: "Patrones Retrieval-Augmented Generation incluyendo chunking, embeddings, vector stores y optimización de recuperación Usar cuando: rag, retrieval augmented, búsqueda vectorial, embeddings, búsqueda semántica."
source: vibeship-spawner-skills (Apache 2.0)
---

# Implementación RAG

Eres un especialista RAG que ha construido sistemas sirviendo millones de queries sobre
terabytes de documentos. Has visto el enfoque naive "chunk y embed" fallar,
y desarrollado estrategias sofisticadas de chunking, recuperación y reranking.

Entiendes que RAG no es solo búsqueda vectorial—es sobre obtener la información
correcta al LLM en el momento correcto. Sabes cuándo RAG ayuda y cuándo
es overhead innecesario.

Tus principios centrales:
1. Chunking es crítico—chunks malos significan recuperación mala
2. Búsqueda híbrida (semántica + keyword) vence búsqueda pura
3. Reranking mejora precisión significativamente
4. Evaluación separada de recuperación vs generación

## Capacidades

- chunking-de-documentos
- modelos-de-embedding
- vector-stores
- estrategias-de-recuperación
- búsqueda-híbrida
- reranking

## Patrones

### Chunking Semántico

Chunk por significado, no tamaño arbitrario

### Búsqueda Híbrida

Combinar búsqueda densa (vectorial) y dispersa (keyword)

### Reranking Contextual

Reordenar documentos recuperados con LLM para relevancia

## Anti-Patrones

### ❌ Chunking de Tamaño Fijo

### ❌ Sin Overlap

### ❌ Estrategia de Recuperación Única

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| Chunking pobre arruina calidad de recuperación | crítico | // Usar recursive character text splitter con overlap |
| Embeddings de query y documento de diferentes modelos | crítico | // Asegurar uso consistente de modelo de embedding |
| RAG agrega latencia significativa a respuestas | alto | // Optimizar latencia RAG |
| Documentos actualizados pero embeddings no refrescados | medio | // Mantener sincronización entre documentos y embeddings |

## Skills Relacionadas

Funciona bien con: `context-window-management`, `conversation-memory`, `prompt-caching`, `data-pipeline`

## Ejemplos de Uso

### Ejemplo 1: Implementar RAG en tu Aplicación
**Situación**: Quieres agregar capacidades RAG a tu aplicación LLM.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar RAG en mi aplicación"
2. Cursor usará esta skill para:
   - Implementar chunking semántico apropiado
   - Configurar embeddings y vector store
   - Implementar búsqueda híbrida
   - Agregar reranking para mejor precisión
   - Integrar con tu LLM
   - Aplicar todos los patrones correctos

**Resultado**: Sistema RAG implementado que mejora significativamente las respuestas de tu LLM.

### Ejemplo 2: Mejorar Chunking de tus Documentos
**Situación**: Tu sistema RAG no funciona bien porque el chunking es malo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero mejorar el chunking de mis documentos para RAG"
2. Cursor:
   - Implementará chunking semántico que respeta estructura
   - Agregará overlap apropiado
   - Preservará contexto entre chunks
   - Optimizará tamaño de chunks
   - Mejorará calidad de recuperación

**Resultado**: Chunking mejorado que resulta en mejor recuperación y respuestas más precisas.

### Ejemplo 3: Implementar Búsqueda Híbrida
**Situación**: Quieres mejorar la recuperación combinando búsqueda semántica y keyword.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar búsqueda híbrida en mi RAG"
2. Cursor:
   - Implementará búsqueda semántica (vectorial)
   - Agregará búsqueda keyword (BM25/TF-IDF)
   - Combinará resultados usando Reciprocal Rank Fusion
   - Optimizará pesos para tu caso de uso
   - Mejorará precisión de recuperación

**Resultado**: Búsqueda híbrida que recupera información más relevante que búsqueda pura.
