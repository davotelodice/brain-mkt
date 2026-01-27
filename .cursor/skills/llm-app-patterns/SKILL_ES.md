---
name: llm-app-patterns
description: "Patrones listos para producción para construir aplicaciones LLM. Cubre pipelines RAG, arquitecturas de agentes, prompt IDEs y monitoreo LLMOps. Usar al diseñar aplicaciones IA, implementar RAG, construir agentes o configurar observabilidad LLM."
---

# 🤖 Patrones de Aplicaciones LLM

> Patrones listos para producción para construir aplicaciones LLM, inspirados en [Dify](https://github.com/langgenius/dify) y mejores prácticas de la industria.

## Cuándo Usar Esta Skill

Usar esta skill cuando:

- Diseñar aplicaciones habilitadas por LLM
- Implementar RAG (Retrieval-Augmented Generation)
- Construir agentes IA con herramientas
- Configurar monitoreo LLMOps
- Elegir entre arquitecturas de agentes

---

## 1. Arquitectura de Pipeline RAG

### Resumen

RAG (Retrieval-Augmented Generation) fundamenta respuestas LLM en tus datos.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Ingest    │────▶│   Retrieve  │────▶│   Generate  │
│  Documents  │     │   Context   │     │   Response  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
 ┌─────────┐       ┌───────────┐       ┌───────────┐
 │ Chunking│       │  Vector   │       │    LLM    │
 │Embedding│       │  Search   │       │  + Context│
 └─────────┘       └───────────┘       └───────────┘
```

### 1.1 Ingestión de Documentos

Estrategias de chunking:
- Fixed-size: Chunks de tamaño fijo (simple pero puede romper contexto)
- Semantic: Chunking semántico (preserva significado)
- Recursive: División recursiva (prueba múltiples separadores)
- Document-aware: Consciente de documento (respeta estructura)

### 1.2 Embedding y Almacenamiento

Opciones de base de datos vectorial:
- Pinecone: Producción, servicio gestionado, billones de vectores
- Weaviate: Self-hosted, multi-modal, millones de vectores
- ChromaDB: Desarrollo, prototipado, miles de vectores
- pgvector: Infraestructura Postgres existente, millones de vectores

### 1.3 Estrategias de Recuperación

- Búsqueda semántica básica
- Búsqueda híbrida (semántica + keyword)
- Recuperación multi-query
- Compresión contextual

### 1.4 Generación con Contexto

Template de prompt RAG que incluye contexto recuperado antes de generar respuesta.

---

## 2. Arquitecturas de Agentes

### 2.1 Patrón ReAct (Reasoning + Acting)

Loop de razonamiento y acción para agentes con herramientas.

### 2.2 Agentes con Planificación

Agentes que planifican antes de ejecutar.

---

## Ejemplos de Uso

### Ejemplo 1: Diseñar una Aplicación LLM Completa
**Situación**: Quieres construir una aplicación completa habilitada por LLM.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero diseñar una aplicación LLM completa"
2. Cursor usará esta skill para:
   - Diseñar pipeline RAG si es necesario
   - Elegir arquitectura de agente apropiada
   - Configurar monitoreo LLMOps
   - Implementar todos los patrones correctos
   - Aplicar mejores prácticas de producción

**Resultado**: Una aplicación LLM bien diseñada lista para producción.

### Ejemplo 2: Implementar Pipeline RAG Completo
**Situación**: Quieres implementar un pipeline RAG completo para tu aplicación.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar un pipeline RAG completo"
2. Cursor:
   - Configurará ingestión de documentos
   - Implementará chunking apropiado
   - Configurará embeddings y vector store
   - Implementará estrategias de recuperación
   - Integrará generación con contexto

**Resultado**: Pipeline RAG completo que mejora significativamente las respuestas de tu LLM.

### Ejemplo 3: Configurar Monitoreo LLMOps
**Situación**: Quieres monitorear y mejorar tu aplicación LLM en producción.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar monitoreo LLMOps para mi app"
2. Cursor:
   - Configurará tracing de LLM
   - Implementará gestión de prompts
   - Configurará evaluación y scoring
   - Agregará tracking de costos
   - Aplicará todas las mejores prácticas

**Resultado**: Sistema de monitoreo completo que te ayuda a mejorar tu aplicación LLM.
