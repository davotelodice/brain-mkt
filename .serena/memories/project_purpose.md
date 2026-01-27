# Propósito del Proyecto

## Marketing Second Brain System

**Sistema web full-stack de segundo cerebro para estrategia de marketing digital**

### Qué hace:

1. **Analiza tu negocio** → Crea buyer persona automáticamente
2. **Simula comportamiento** → El agente actúa como tu cliente ideal en foros
3. **Mapea el customer journey** → 3 fases (awareness, consideration, purchase) con 20+ preguntas por fase
4. **Procesa documentos** → Usuario sube .txt, .pdf, .docx con info de su negocio
5. **Genera contenido on-demand** → Ideas de videos, posts, artículos personalizados
6. **Aprende de expertos** → Entrenado con transcripciones de YouTubers + libros de marketing

### Diferenciadores Clave:

- 🤖 **7 Agentes IA Especializados**: Router, Document Processor, Buyer Persona, Forum Simulator, Pain Points, Customer Journey, Content Generator
- 🧠 **Memoria Triple**: Short-term (10 últimos mensajes), Long-term (DB), Semantic (pgvector)
- 📚 **RAG con Conocimiento Experto**: Transcripciones de YouTubers + libros de marketing
- 📄 **Upload de Documentos**: Soporta .txt, .pdf, .docx
- ⏸️ **No Genera Automáticamente**: Usuario controla cuándo generar contenido (no spam)
- 🔒 **Multi-Tenancy Estricto**: Aislamiento total por `project_id`
- 🚀 **Streaming de Respuestas**: SSE (Server-Sent Events) para respuestas en tiempo real

### Flujo Principal:

**FASE 1 - ANÁLISIS INICIAL (Automático):**
1. Usuario crea nuevo chat
2. Agente hace 4-5 preguntas iniciales
3. [OPCIONAL] Usuario sube documentos
4. Agente procesa documentos
5. Agente genera buyer persona completo (35+ preguntas)
6. Agente simula foro y extrae pain points
7. Agente genera customer journey
8. Agente ENTREGA documento y ESPERA

**FASE 2 - GENERACIÓN DE CONTENIDO (On-Demand):**
1. Usuario pide contenido específico
2. Agente consulta: buyer persona + CJ + documentos + knowledge base
3. Agente GENERA respuesta personalizada
4. Ciclo continúa según peticiones

**IMPORTANTE**: El agente NO genera contenido automáticamente, solo cuando el usuario lo solicita.