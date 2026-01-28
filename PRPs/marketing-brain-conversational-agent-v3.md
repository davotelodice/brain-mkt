name: "Marketing Brain - Agente Conversacional y Entrenamiento"
version: "3.2-ES"
descripcion: |
  PRP enfocado en hacer el agente conversacional con contexto persistente
  y entrenamiento efectivo con transcripciones de Andrea Estratega.
  NO duplica funcionalidades ya implementadas (Buyer Persona, Customer Journey, Forum).

fecha_creacion: "2026-01-28"
ultima_actualizacion: "2026-01-28"
autor: "Claude Code (con Serena + Archon)"

---

## 🎯 Problema Principal Identificado

**El agente NO es conversacional:**
- No mantiene contexto de la conversación
- No recuerda mensajes anteriores
- No puede sostener diálogos naturales
- Las transcripciones están en la knowledge base pero no se usan efectivamente

**Lo que YA funciona (NO tocar):**
- ✅ Buyer Persona Agent (genera análisis completo)
- ✅ Customer Journey (3 fases × 20 preguntas)
- ✅ Forum Simulator (quejas + soluciones)
- ✅ Pain Points (10 puntos de dolor)
- ✅ Base de datos completa (8 tablas con prefijo marketing_)
- ✅ RAG Service (búsqueda semántica)
- ✅ Memory Manager (3 tipos de memoria)

**Lo que FALTA:**
- ❌ Conversación con contexto persistente
- ❌ Entrenamiento efectivo con transcripciones
- ❌ Sistema de mensajes en formato conversacional para LLM

---

## 📚 Contexto y Documentación

### Análisis del Código Actual (Serena)

**Estado Actual Verificado:**

**Backend (`backend/src/`):**
- ✅ `agents/router_agent.py` - Router con estados
- ✅ `agents/buyer_persona_agent.py` - Genera buyer persona + forum + CJ
- ✅ `agents/content_generator_agent.py` - Genera contenido on-demand
- ✅ `services/memory_manager.py` - MemoryManager con ConversationBufferWindowMemory(k=10)
- ✅ `services/llm_service.py` - LLMService con generate() y stream()
- ✅ `services/rag_service.py` - Búsqueda semántica
- ✅ `api/chat.py` - Endpoints de chat con streaming

**Problema Identificado (verificado con Serena):**

1. **LLMService NO acepta messages array:**
   - `generate(prompt: str, system: str)` - Solo string, no historial
   - `stream(prompt: str, system: str)` - Solo string, no historial
   - **Solución:** Añadir `generate_with_messages(messages: list)` y `stream_with_messages(messages: list)`

2. **MemoryManager tiene historial pero NO se convierte a messages:**
   - `ConversationBufferWindowMemory.load_memory_variables({})` retorna `{"history": "Human: ...\nAI: ..."}`
   - **Solución:** Crear helper `format_messages_from_memory()` que convierte a formato OpenAI

3. **Historial se carga pero NO se inyecta:**
   - `ensure_chat_loaded()` se llama en `/stream` y `/messages` (líneas 270, 378)
   - Pero el historial NO se pasa al LLM
   - **Solución:** Usar `format_messages_from_memory()` antes de llamar LLM

4. **Transcripciones solo se buscan vía RAG, no como entrenamiento:**
   - `_build_content_prompt()` busca transcripciones vía RAG (línea 119: `if doc.get('content_type') == 'video_transcript'`)
   - Solo aparecen si la búsqueda las encuentra
   - **Solución:** Inyectar resumen de técnicas SIEMPRE en system prompt (cacheado)

**Comandos Serena Ejecutados (YA VERIFICADO):**
```python
# ✅ YA EJECUTADO:
find_symbol('ContentGeneratorAgent/_build_content_prompt', 'backend/src/agents/content_generator_agent.py', include_body=True)
# Resultado: Prompt se construye con técnicas vía RAG, pero NO usa historial de conversación

find_symbol('MemoryManager/get_context', 'backend/src/services/memory_manager.py', include_body=True)
# Resultado: Retorna context dict con recent_chat, buyer_persona, relevant_docs, etc.

find_symbol('LLMService/generate', 'backend/src/services/llm_service.py', include_body=True)
# Resultado: Solo acepta prompt string, NO messages array
```

**Hallazgos Clave:**
- `_build_content_prompt()` construye prompt con técnicas vía RAG (línea 119-120)
- `LLMService.generate()` solo acepta `prompt: str`, no `messages: list`
- `ensure_chat_loaded()` se llama pero historial NO se usa en llamadas al LLM

### Documentación Consultada (Archon)

**Source IDs Disponibles:**
- `e74f94bb9dcb14aa` - LangChain Documentation (1M palabras, incluye LangGraph)
- `c889b62860c33a44` - FastAPI Documentation

**Queries Ejecutadas:**

1. **LangGraph Conversation Memory:**
   ```yaml
   query: "langgraph conversation state checkpoint memory"
   source_id: "e74f94bb9dcb14aa"
   resultados:
     - LangGraph add-memory.md: Checkpointers para estado persistente
     - InMemorySaver y AsyncMongoDBSaver para checkpoints
     - thread_id para mantener conversaciones separadas
     - MessagesState para manejo de mensajes
   ```

2. **LangChain Conversation Memory:**
   ```yaml
   query: "conversation memory langchain buffer window"
   source_id: "e74f94bb9dcb14aa"
   resultados:
     - ConversationBufferWindowMemory con k=10
     - load_memory_variables() para obtener historial
     - return_messages=True para formato de mensajes
   ```

**Decisión Técnica:**
- **Opción A (Recomendada)**: Mejorar LLMService para aceptar `messages` array y usar historial de ConversationBufferWindowMemory
- **Opción B (Futuro)**: Migrar a LangGraph con checkpoints para conversaciones stateful más robustas

**Por ahora: Opción A** (más simple, menos cambios, funciona con stack actual)

---

## 🎓 Skills Disponibles y Cuándo Usarlas

**Skills identificadas del `skills_index.json` que mejoran la ejecución:**

### Skills de Desarrollo y Calidad
- **python-patterns** (automático): Patrones Python, async, type hints - usar siempre
- **clean-code** (automático): Código conciso, sin over-engineering - usar siempre
- **lint-and-validate**: Validación automática después de cada cambio - usar después de cada modificación
- **test-driven-development** / **tdd-workflow**: TDD red-green-refactor - usar si se crean tests nuevos
- **test-fixing**: Arreglar tests fallidos sistemáticamente - usar cuando tests fallen
- **systematic-debugging**: Debugging metódico paso a paso - usar ANTES de proponer fixes si hay errores
- **verification-before-completion**: Validar ANTES de marcar como completo - usar antes de completar cada tarea
- **code-review-checklist**: Checklist completo de revisión - usar antes de completar cada tarea
- **requesting-code-review**: Solicitar code review - usar al finalizar todas las tareas

### Skills de Agentes y Memoria
- **conversation-memory**: Patrones de memoria persistente para conversaciones LLM
- **agent-memory-systems**: Arquitectura de memoria multi-nivel (short-term, long-term, semantic)
- **llm-app-patterns**: Patrones de producción para apps LLM (RAG, agentes, observabilidad)
- **langgraph**: Framework para agentes stateful (alternativa futura si messages array no es suficiente)
- **langfuse**: Observabilidad LLM - tracing, evaluación, debugging (opcional pero útil)

### Skills de Prompts y RAG
- **prompt-engineering**: Guía experta de prompt engineering - usar para optimizar prompts
- **prompt-engineer**: Diseño efectivo de prompts para apps LLM - usar para mejorar prompts
- **prompt-caching**: Cachear prompts para reducir costos - usar para cachear resumen de técnicas
- **rag-implementation**: Estrategias de chunking, embeddings, búsqueda semántica
- **rag-engineer**: Expert en RAG systems - usar para validar búsqueda de técnicas
- **context-window-management**: Gestión de contexto largo - usar para optimizar tamaño de prompts

### Skills de Planificación y Ejecución
- **plan-writing**: Planificación estructurada con dependencias - usar al inicio de cada tarea
- **executing-plans**: Ejecutar plan con checkpoints - usar si se crea plan detallado
- **brainstorming**: Explorar diseño antes de implementar - usar ANTES de crear código nuevo (OBLIGATORIO según skill)

**Nota:** Las skills se activan automáticamente cuando detectan keywords relevantes, pero es mejor mencionarlas explícitamente en cada tarea para asegurar su uso.

**⚠️ IMPORTANTE:** La skill **brainstorming** indica que DEBE usarse antes de cualquier trabajo creativo. Considerar usar al inicio de TAREA 3 (Entrenamiento) para explorar estrategias de in-context learning.

---

## 🚨 Gotchas Críticos Identificados

```yaml
1. LLMService NO acepta messages array:
   PROBLEMA: Solo acepta prompt string, no puede usar historial
   SOLUCIÓN: Añadir método generate_with_messages(messages: list)
   UBICACIÓN: backend/src/services/llm_service.py

2. Historial NO se inyecta en prompts:
   PROBLEMA: ConversationBufferWindowMemory existe pero no se usa
   SOLUCIÓN: Inyectar historial en formato messages[] antes de llamar LLM
   UBICACIÓN: backend/src/agents/content_generator_agent.py

3. Transcripciones NO se usan como "entrenamiento":
   PROBLEMA: Están en knowledge_base pero solo se buscan vía RAG
   SOLUCIÓN: Inyectar resumen de técnicas en system prompt siempre
   UBICACIÓN: backend/src/agents/content_generator_agent.py

4. Fine-tuning NO es necesario:
   DECISIÓN: Usar in-context learning (transcripciones en system prompt)
   RAZÓN: Fine-tuning requiere dataset estructurado y es costoso
   ALTERNATIVA: LangGraph con checkpoints para estado conversacional
```

---

## 📋 Tareas de Implementación

### TAREA 1: Mejorar LLMService para Aceptar Messages Array

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar LLMService actual
  - Importancia: "Ver estructura exacta antes de modificar"
  - Comando: `find_symbol('LLMService', 'backend/src/services/llm_service.py', include_body=True)`
- ⚡ MCP Archon: OpenAI/OpenRouter messages format
  - Importancia: "Formato correcto de messages array"
  - Comando: `rag_search_knowledge_base(query="openai chat completions messages array format", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills:
  - **python-patterns** (automático): Patrones Python, async, type hints
  - **clean-code** (automático): Código conciso, sin over-engineering
  - **llm-app-patterns**: Validar que implementación sigue best practices de apps LLM
  - **systematic-debugging**: Si hay errores, usar ANTES de proponer fixes - debugging metódico paso a paso
  - **verification-before-completion**: ANTES de marcar como completo - ejecutar tests y validar output
  - **test-driven-development**: Si se crean tests nuevos, considerar TDD - escribir tests primero
  - **lint-and-validate**: Después de cada cambio - validación automática

**Objetivo:** Añadir método `generate_with_messages()` y `stream_with_messages()` que acepten array de mensajes en formato OpenAI

**Pasos a seguir:**
1. Analizar `LLMService` con Serena
2. Añadir métodos nuevos (NO modificar los existentes para backward compatibility)
3. Formato messages: `[{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, ...]`
4. Soporte para historial de conversación

**Criterios de aceptación:**
- [ ] `generate_with_messages(messages: list)` funciona
- [ ] `stream_with_messages(messages: list)` funciona
- [ ] Métodos existentes siguen funcionando (backward compatible)
- [ ] Tests unitarios pasan

**Archivos a modificar:**
- `backend/src/services/llm_service.py` - Añadir métodos nuevos

**Pseudocódigo:**
```python
# PATRÓN: Mantener métodos existentes + añadir nuevos
class LLMService:
    # Métodos existentes (NO tocar)
    async def generate(self, prompt: str, system: str = "", ...):
        ...
    
    # NUEVO: Método con messages array
    async def generate_with_messages(
        self,
        messages: list[dict[str, str]],  # [{"role": "user", "content": "..."}, ...]
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text with full conversation history.
        
        Args:
            messages: List of message dicts with "role" and "content"
            Format: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, ...]
        
        Returns:
            Generated text
        """
        # CRÍTICO: Validar formato de messages
        # GOTCHA: OpenAI requiere roles: system, user, assistant
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # ✅ Pasar directamente
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    async def stream_with_messages(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream with full conversation history."""
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

---

### TAREA 2: Inyectar Historial de Conversación en Agentes

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar cómo se usa MemoryManager
  - Importancia: "Ver cómo obtener historial y formatearlo"
  - Comando: `find_symbol('MemoryManager/get_context', 'backend/src/services/memory_manager.py', include_body=True)`
  - Comando: `find_symbol('ContentGeneratorAgent/execute', 'backend/src/agents/content_generator_agent.py', include_body=True)`
- ⚡ MCP Archon: LangChain memory format conversion
  - Importancia: "Cómo convertir ConversationBufferWindowMemory a messages array"
  - Comando: `rag_search_knowledge_base(query="langchain memory load_memory_variables messages format", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills:
  - **conversation-memory**: Patrones de memoria persistente para conversaciones LLM - usar para diseñar formato de messages
  - **agent-memory-systems**: Arquitectura de memoria multi-nivel - usar para entender cómo combinar short-term + long-term
  - **llm-app-patterns**: Patrones de producción para apps LLM - usar para validar que la implementación sigue best practices
  - **systematic-debugging**: Si hay problemas con formato de messages - debugging metódico
  - **verification-before-completion**: Validar que historial se inyecta correctamente antes de completar

**Objetivo:** Modificar agentes para que usen historial de conversación en formato messages[] al llamar al LLM

**Pasos a seguir:**
1. Analizar `MemoryManager.get_context()` con Serena
2. Ver cómo `ConversationBufferWindowMemory.load_memory_variables({})` retorna el historial
3. Crear función helper `_format_messages_from_memory()` que convierte historial a formato OpenAI
4. Modificar `ContentGeneratorAgent` para usar `generate_with_messages()` con historial
5. Modificar `BuyerPersonaAgent` si es necesario

**Criterios de aceptación:**
- [ ] Historial se convierte correctamente a formato messages[]
- [ ] Agentes usan historial en llamadas al LLM
- [ ] El agente puede referirse a mensajes anteriores
- [ ] Conversación fluida y natural

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - Añadir método helper
- `backend/src/agents/content_generator_agent.py` - Usar historial
- `backend/src/agents/buyer_persona_agent.py` - Usar historial si aplica

**Pseudocódigo:**
```python
# PATRÓN: Helper para convertir memoria a messages array
class MemoryManager:
    def _format_messages_from_memory(
        self,
        chat_id: UUID,
        system_prompt: str = "",
        current_user_message: str = ""
    ) -> list[dict[str, str]]:
        """
        Convert ConversationBufferWindowMemory to OpenAI messages format.
        
        Returns:
            [{"role": "system", "content": "..."}, 
             {"role": "user", "content": "..."}, 
             {"role": "assistant", "content": "..."}, ...]
        """
        messages = []
        
        # 1. System prompt primero
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 2. Obtener historial de ConversationBufferWindowMemory
        memory = self._get_short_term(chat_id)
        history_dict = memory.load_memory_variables({})
        
        # 3. Parsear historial (formato: "Human: ...\nAI: ...\nHuman: ...")
        history_text = history_dict.get("history", "")
        
        if history_text:
            # Dividir por líneas y parsear
            lines = history_text.strip().split("\n")
            for line in lines:
                if line.startswith("Human:"):
                    content = line.replace("Human:", "").strip()
                    if content:
                        messages.append({"role": "user", "content": content})
                elif line.startswith("AI:"):
                    content = line.replace("AI:", "").strip()
                    if content:
                        messages.append({"role": "assistant", "content": content})
        
        # 4. Añadir mensaje actual del usuario
        if current_user_message:
            messages.append({"role": "user", "content": current_user_message})
        
        return messages

# En ContentGeneratorAgent:
class ContentGeneratorAgent(BaseAgent):
    async def execute(...):
        # 1. Get context (buyer persona, docs, etc.)
        context = await self._get_context(chat_id, project_id, user_message)
        
        # 2. Formatear mensajes con historial
        messages = self.memory._format_messages_from_memory(
            chat_id=chat_id,
            system_prompt=self._build_system_prompt(context),
            current_user_message=user_message
        )
        
        # 3. Llamar LLM con historial completo
        response = await self.llm.generate_with_messages(
            messages=messages,
            max_tokens=4000,
            temperature=0.8
        )
        
        # 4. Parsear y retornar
        ...
```

---

### TAREA 3: Entrenamiento con Transcripciones (In-Context Learning)

**Herramientas a utilizar:**
- 🔧 MCP Serena: Verificar script de ingesta
  - Importancia: "Confirmar que transcripciones están en knowledge_base"
  - Comando: `find_symbol('ingest', 'backend/scripts/ingest_training_data.py', include_body=True)`
- ⚡ MCP Archon: In-context learning patterns
  - Importancia: "Cómo inyectar conocimiento de entrenamiento en system prompt"
  - Comando: `rag_search_knowledge_base(query="in-context learning system prompt training data", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills:
  - **brainstorming** (OBLIGATORIO): Explorar estrategias de in-context learning ANTES de implementar
  - **rag-implementation**: Estrategias de chunking, embeddings, búsqueda semántica - usar para optimizar búsqueda de chunks representativos
  - **rag-engineer**: Expert en RAG systems - usar para validar que la búsqueda de técnicas es efectiva
  - **context-window-management**: Gestión de contexto largo - usar para optimizar tamaño del resumen (no exceder tokens)
  - **prompt-caching**: Cachear resumen de técnicas - usar para reducir costos (cachear en Redis con TTL 24h)
  - **prompt-engineer**: Diseño efectivo de prompts - usar para mejorar el prompt que genera el resumen de técnicas
  - **prompt-engineering**: Guía experta de prompt engineering - usar para optimizar estructura del prompt
  - **llm-app-patterns**: Patrones de producción - usar para validar que in-context learning está bien implementado

**Objetivo:** Inyectar técnicas de las transcripciones de Andrea Estratega en el system prompt del ContentGeneratorAgent para que el agente "esté entrenado" con ese conocimiento

**Pasos a seguir:**
1. **[OBLIGATORIO] Usar skill brainstorming:** Explorar estrategias de in-context learning antes de implementar
2. Verificar que transcripciones están en `marketing_knowledge_base` con `content_type='video_transcript'`
3. Crear método `_get_training_summary()` que obtiene resumen de técnicas principales
4. Inyectar resumen en system prompt del ContentGeneratorAgent
5. Cachear resumen en Redis para no buscarlo cada vez (usar skill prompt-caching)

**Criterios de aceptación:**
- [ ] System prompt incluye técnicas de transcripciones
- [ ] El agente genera contenido usando técnicas de Andrea Estratega
- [ ] Resumen se cachea para performance
- [ ] Tests verifican que técnicas aparecen en respuestas

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - Añadir `_get_training_summary()`
- `backend/src/agents/content_generator_agent.py` - Inyectar en system prompt

**Pseudocódigo:**
```python
# PATRÓN: In-context learning con resumen de técnicas
class MemoryManager:
    async def get_training_summary(
        self,
        project_id: UUID,
        cache_key: str = "training_summary"
    ) -> str:
        """
        Obtener resumen de técnicas de las transcripciones de Andrea Estratega.
        
        Estrategia:
        1. Buscar chunks más representativos de técnicas virales
        2. Generar resumen con LLM (una vez, cachear)
        3. Inyectar en system prompt siempre
        
        Returns:
            Resumen de técnicas en formato texto
        """
        # 1. Buscar chunks representativos (no todos, solo los mejores)
        training_chunks = await self.rag_service.search_relevant_docs(
            query="técnicas virales contenido Instagram TikTok hooks estructuras",
            project_id=None,  # Global knowledge
            chat_id=None,
            limit=15,  # Top 15 chunks más relevantes
            metadata_filters={"content_type": "video_transcript"}
        )
        
        # 2. Combinar chunks en texto
        techniques_text = "\n\n".join([
            f"TÉCNICA {i+1} (de {chunk['source_title']}):\n{chunk['content']}"
            for i, chunk in enumerate(training_chunks)
        ])
        
        # 3. Generar resumen estructurado (cachear en Redis)
        # Si ya existe en cache, retornar cache
        # Si no, generar con LLM y cachear
        
        summary_prompt = f"""
        Resume las técnicas principales de creación de contenido viral
        de estas transcripciones de videos de marketing:
        
        {techniques_text}
        
        Crea un resumen estructurado con:
        - Técnicas de hooks (primeros 3 segundos)
        - Estructuras de contenido que funcionan
        - Formatos virales probados
        - CTAs efectivos
        
        Formato: Texto claro y conciso, listo para usar en system prompt.
        """
        
        # Generar resumen (una vez, cachear)
        summary = await self.llm_service.generate(
            prompt=summary_prompt,
            system="Eres un experto en resumir técnicas de marketing",
            max_tokens=2000,
            temperature=0.3  # Baja temperatura para resumen fiel
        )
        
        # Cachear en Redis (TTL 24 horas)
        # await redis.setex(cache_key, 86400, summary)
        
        return summary

# En ContentGeneratorAgent:
class ContentGeneratorAgent(BaseAgent):
    def _build_system_prompt(self, context: dict) -> str:
        """Build system prompt with training data."""
        
        # 1. Obtener resumen de técnicas (cacheado)
        training_summary = await self.memory.get_training_summary(context['project_id'])
        
        # 2. Combinar con instrucciones base
        system = f"""
        Eres un experto en marketing digital especializado en crear contenido viral
        para redes sociales (TikTok, Instagram, YouTube).
        
        ## TÉCNICAS DE ENTRENAMIENTO (de Andrea Estratega):
        {training_summary}
        
        ## TU ESTILO:
        - Usa estas técnicas probadas en tu contenido
        - Adapta técnicas al buyer persona específico
        - Sé específico y accionable
        - Genera contenido listo para usar
        """
        
        return system
```

---

### TAREA 4: Verificar y Mejorar Carga de Historial

**Herramientas a utilizar:**
- 🔧 MCP Serena: Verificar dónde se carga historial
  - Importancia: "Confirmar que load_chat_history se llama correctamente"
  - Comando: `grep('load_chat_history|ensure_chat_loaded', 'backend/src/api/chat.py')`
  - Comando: `find_symbol('stream_message', 'backend/src/api/chat.py', include_body=True)`
- 📚 Skills:
  - **conversation-memory**: Patrones de memoria persistente - usar para validar que carga de historial sigue best practices
  - **systematic-debugging**: Si hay problemas con carga de historial - debugging metódico
  - **verification-before-completion**: Validar que historial se carga correctamente antes de completar

**Objetivo:** Asegurar que el historial se carga ANTES de procesar cada mensaje

**Pasos a seguir:**
1. Verificar que `ensure_chat_loaded()` se llama en endpoints de chat
2. Verificar que se llama ANTES de procesar mensaje
3. Asegurar que historial se añade a memoria corto plazo correctamente

**Criterios de aceptación:**
- [ ] Historial se carga al abrir chat
- [ ] Historial se carga antes de procesar cada mensaje
- [ ] ConversationBufferWindowMemory está poblado
- [ ] El agente puede referirse a mensajes anteriores

**Archivos a modificar:**
- `backend/src/api/chat.py` - Verificar llamadas a `ensure_chat_loaded()`

---

### TAREA 5: Mejorar System Prompt con Contexto Completo

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar prompts actuales
  - Importancia: "Ver cómo se construyen los prompts"
  - Comando: `find_symbol('ContentGeneratorAgent/_build_content_prompt', 'backend/src/agents/content_generator_agent.py', include_body=True)`
- 📚 Skills:
  - **prompt-engineering**: Guía experta de prompt engineering - usar para optimizar estructura y formato del system prompt
  - **prompt-engineer**: Diseño efectivo de prompts para apps LLM - usar para mejorar prompts con técnicas avanzadas
  - **context-window-management**: Gestión de contexto largo - usar para optimizar tamaño del prompt (no exceder límite)
  - **prompt-caching**: Cachear partes estáticas del prompt - usar para reducir tokens en cada llamada
  - **llm-app-patterns**: Patrones de producción - usar para validar que el prompt sigue best practices de apps LLM

**Objetivo:** Mejorar system prompt para incluir siempre:
- Técnicas de entrenamiento (transcripciones)
- Buyer persona del chat
- Customer journey del chat
- Resúmenes de documentos subidos

**Pasos a seguir:**
1. Analizar `_build_content_prompt()` actual
2. Mover información estática a system prompt
3. Inyectar técnicas de entrenamiento siempre
4. Optimizar para no exceder límite de tokens

**Criterios de aceptación:**
- [ ] System prompt incluye técnicas de entrenamiento
- [ ] System prompt incluye buyer persona y CJ
- [ ] Prompt no excede límite de tokens
- [ ] El agente genera contenido usando técnicas aprendidas

**Archivos a modificar:**
- `backend/src/agents/content_generator_agent.py` - Mejorar `_build_content_prompt()`

---

## ✅ Gates de Validación

**Skills a usar en validación:**
- **lint-and-validate**: Validación automática después de cada cambio
- **test-fixing**: Arreglar tests fallidos sistemáticamente
- **verification-before-completion**: Validar ANTES de marcar como completo
- **code-review-checklist**: Revisar código antes de completar
- **requesting-code-review**: Solicitar code review al finalizar todas las tareas

### Nivel 1: Sintaxis
```bash
ruff check backend/src/ --fix
mypy backend/src/
```
**Skill: lint-and-validate** - Ejecutar automáticamente después de cada cambio

### Nivel 2: Tests
```bash
pytest backend/tests/test_memory.py -v
pytest backend/tests/test_agents.py::test_content_generator_uses_history -v
```
**Skills:**
- **test-fixing**: Si tests fallan, usar para arreglar sistemáticamente
- **test-driven-development**: Si se crean tests nuevos, considerar TDD

### Nivel 3: Integración
```bash
# Test conversacional:
# 1. Crear chat
# 2. Mensaje 1: "Hola, mi negocio es..."
# 3. Mensaje 2: "¿Qué más necesitas saber?"
# 4. Verificar que agente recuerda mensaje 1
```
**Skill: verification-before-completion** - Validar que todo funciona antes de completar

---

## 🔍 Análisis Detallado del Problema

### Problema 1: LLMService NO Usa Historial

**Código Actual (verificado con Serena):**
```python
# backend/src/services/llm_service.py
async def generate(self, prompt: str, system: str = "", ...):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})  # ❌ Solo mensaje actual
    # ...
```

**Problema:** Solo envía el mensaje actual, NO el historial.

**Solución:** Añadir `generate_with_messages(messages: list)` que acepta historial completo.

---

### Problema 2: MemoryManager NO Convierte Historial a Messages

**Código Actual (verificado con Serena):**
```python
# backend/src/services/memory_manager.py
recent_messages = self._get_short_term(chat_id).load_memory_variables({})
# Retorna: {"history": "Human: ...\nAI: ...\nHuman: ..."}
```

**Problema:** Historial está en formato texto, NO en formato messages[] para OpenAI.

**Solución:** Crear helper `_format_messages_from_memory()` que convierte a formato OpenAI.

---

### Problema 3: Transcripciones Solo se Buscan, No se Inyectan

**Código Actual (verificado con Serena):**
```python
# backend/src/agents/content_generator_agent.py
relevant_docs = context['relevant_docs']  # Solo cuando se busca vía RAG
# Se inyectan en prompt, pero NO en system prompt como "entrenamiento"
```

**Problema:** Las transcripciones solo aparecen cuando se buscan específicamente, no como conocimiento base.

**Solución:** Inyectar resumen de técnicas en system prompt siempre (cacheado).

---

## 🎯 Decisión: Fine-tuning vs In-Context Learning

**Fine-tuning:**
- ❌ Requiere dataset estructurado (pregunta-respuesta)
- ❌ Costoso ($$$)
- ❌ Tiempo de entrenamiento
- ❌ Modelo específico (no funciona con cualquier LLM)

**In-Context Learning (Recomendado):**
- ✅ Funciona con cualquier LLM
- ✅ Sin costo adicional
- ✅ Fácil de actualizar (solo cambiar system prompt)
- ✅ Funciona con stack actual

**Decisión:** Usar **In-Context Learning** inyectando técnicas en system prompt.

**Alternativa Futura:** LangGraph con checkpoints para conversaciones más robustas (si in-context learning no es suficiente).

---

## 📋 Tareas Detalladas

### TAREA 1: Mejorar LLMService para Aceptar Messages Array

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar LLMService actual
  - Comando: `find_symbol('LLMService', 'backend/src/services/llm_service.py', include_body=True)`
- ⚡ MCP Archon: OpenAI messages format
  - Comando: `rag_search_knowledge_base(query="openai chat completions messages format roles", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills: python-patterns, clean-code

**Objetivo:** Añadir métodos `generate_with_messages()` y `stream_with_messages()` sin romper código existente

**Pasos a seguir:**
1. Analizar `LLMService` completo con Serena
2. Añadir métodos nuevos (backward compatible)
3. Validar formato de messages (roles: system, user, assistant)
4. Tests unitarios

**Archivos a modificar:**
- `backend/src/services/llm_service.py`

**Pseudocódigo:**
```python
# PATRÓN: Añadir métodos nuevos, NO modificar existentes
class LLMService:
    # ✅ Métodos existentes (mantener para backward compatibility)
    async def generate(self, prompt: str, system: str = "", ...):
        # Código existente - NO TOCAR
        ...    
    # ✅ NUEVO: Método con messages array
    async def generate_with_messages(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Generate with full conversation history.
        
        Args:
            messages: [{"role": "system|user|assistant", "content": "..."}, ...]
        
        Returns:
            Generated text
        """
        # CRÍTICO: Validar formato
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"Invalid message format: {msg}")
            if msg["role"] not in ["system", "user", "assistant"]:
                raise ValueError(f"Invalid role: {msg['role']}")
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    async def stream_with_messages(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream with full conversation history."""
        # Misma validación que generate_with_messages
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

**Comandos de validación:**
```bash
pytest backend/tests/test_llm_service.py -v
# Test: generate_with_messages con historial de 5 mensajes
```

---

### TAREA 2: Convertir Historial a Messages Array

**Herramientas a utilizar:**
- 🔧 MCP Serena: Ver formato exacto de ConversationBufferWindowMemory
  - Comando: `find_symbol('MemoryManager/_get_short_term', 'backend/src/services/memory_manager.py', include_body=True)`
  - Comando: `grep('load_memory_variables', 'backend/src/services/memory_manager.py')`
- ⚡ MCP Archon: LangChain memory format
  - Comando: `rag_search_knowledge_base(query="langchain ConversationBufferWindowMemory load_memory_variables format", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills: conversation-memory

**Objetivo:** Crear helper que convierte `ConversationBufferWindowMemory` a formato messages[] de OpenAI

**Pasos a seguir:**
1. Verificar formato exacto que retorna `load_memory_variables({})`
2. Crear método `_format_messages_from_memory()` en MemoryManager
3. Probar conversión con historial real

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - Añadir método helper

**Pseudocódigo (basado en código real analizado):**
```python
# PATRÓN: Helper para convertir ConversationBufferWindowMemory a messages array
# VERIFICADO: load_memory_variables({}) retorna {"history": "Human: ...\nAI: ..."}
class MemoryManager:
    def format_messages_from_memory(
        self,
        chat_id: UUID,
        system_prompt: str = "",
        current_user_message: str = ""
    ) -> list[dict[str, str]]:
        """
        Convert ConversationBufferWindowMemory to OpenAI messages format.
        
        VERIFICADO: load_memory_variables({}) retorna {"history": "Human: ...\nAI: ..."}
        
        Returns:
            [{"role": "system", "content": "..."}, 
             {"role": "user", "content": "..."}, 
             {"role": "assistant", "content": "..."}, ...]
        """
        messages = []
        
        # 1. System prompt primero
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 2. Obtener historial (VERIFICADO: retorna {"history": "Human: ...\nAI: ..."})
        memory = self._get_short_term(chat_id)
        history_dict = memory.load_memory_variables({})
        history_text = history_dict.get("history", "")
        
        # 3. Parsear formato "Human: ...\nAI: ..."
        if history_text and isinstance(history_text, str):
            lines = history_text.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("Human:"):
                    content = line.replace("Human:", "").strip()
                    if content:
                        messages.append({"role": "user", "content": content})
                elif line.startswith("AI:"):
                    content = line.replace("AI:", "").strip()
                    if content:
                        messages.append({"role": "assistant", "content": content})
        
        # 4. Añadir mensaje actual
        if current_user_message:
            messages.append({"role": "user", "content": current_user_message})
        
        return messages
```

**Comandos de validación:**
```python
# Test manual:
memory = MemoryManager(db, rag_service)
# Añadir algunos mensajes
await memory.add_message_to_short_term(chat_id, "user", "Hola")
await memory.add_message_to_short_term(chat_id, "assistant", "Hola, ¿cómo puedo ayudarte?")
await memory.add_message_to_short_term(chat_id, "user", "Mi negocio es...")

# Convertir a messages
messages = memory.format_messages_from_memory(chat_id, "Eres un asistente", "¿Qué más?")
# Verificar formato: [{"role": "system", ...}, {"role": "user", "content": "Hola"}, ...]
```

---

### TAREA 3: Inyectar Transcripciones en System Prompt

**Herramientas a utilizar:**
- 🔧 MCP Serena: Verificar que transcripciones están en DB
  - Comando: `grep('video_transcript', 'backend/src')`
  - Comando: `read_file('backend/scripts/ingest_training_data.py')` (verificar que funciona)
- ⚡ MCP Archon: In-context learning best practices
  - Comando: `rag_search_knowledge_base(query="system prompt training data in-context learning", source_id="e74f94bb9dcb14aa", match_count=3)`
- 📚 Skills: rag-implementation, context-window-management

**Objetivo:** Obtener resumen de técnicas de transcripciones e inyectarlo SIEMPRE en system prompt

**Pasos a seguir:**
1. Verificar que script `ingest_training_data.py` se ejecutó y hay datos en DB
2. Crear método `get_training_summary()` en MemoryManager
3. Buscar top-15 chunks más representativos de técnicas
4. Generar resumen estructurado (cachear en Redis)
5. Inyectar en system prompt del ContentGeneratorAgent

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - Añadir `get_training_summary()`
- `backend/src/agents/content_generator_agent.py` - Usar en `_build_content_prompt()`

**Pseudocódigo:**
```python
# PATRÓN: In-context learning con resumen cacheado
class MemoryManager:
    async def get_training_summary(self, project_id: UUID) -> str:
        """
        Obtener resumen de técnicas de transcripciones (cacheado).
        
        Estrategia:
        1. Buscar chunks más representativos (una vez)
        2. Generar resumen con LLM (una vez, cachear 24h)
        3. Retornar resumen para inyectar en system prompt
        """
        cache_key = f"training_summary_{project_id}"
        
        # 1. Verificar cache (Redis)
        # cached = await redis.get(cache_key)
        # if cached:
        #     return cached
        
        # 2. Buscar chunks representativos de técnicas
        training_chunks = await self.rag_service.search_relevant_docs(
            query="técnicas virales hooks estructuras contenido Instagram TikTok",
            project_id=None,  # Global knowledge
            chat_id=None,
            limit=15,
            metadata_filters={"content_type": "video_transcript"},
            rerank=True  # Mejor relevancia
        )
        
        if not training_chunks:
            return "No hay transcripciones de entrenamiento disponibles aún."
        
        # 3. Combinar chunks
        techniques_text = "\n\n---\n\n".join([
            f"**TÉCNICA {i+1}** (de: {chunk['source_title']}):\n{chunk['content'][:800]}"
            for i, chunk in enumerate(training_chunks)
        ])
        
        # 4. Generar resumen estructurado
        summary_prompt = f"""
        Resume las técnicas principales de creación de contenido viral
        de estas transcripciones de videos de marketing de Andrea Estratega:
        
        {techniques_text}
        
        Crea un resumen estructurado y conciso (máximo 1500 palabras) con:
        
        1. TÉCNICAS DE HOOKS (primeros 3 segundos):
           - Ejemplos específicos
           - Patrones que funcionan
        
        2. ESTRUCTURAS DE CONTENIDO:
           - Formatos probados
           - Orden de elementos
        
        3. TÉCNICAS VIRALES:
           - Qué hace que un contenido se vuelva viral
           - Elementos clave
        
        4. CTAs EFECTIVOS:
           - Cómo cerrar contenido para acción
        
        Formato: Texto claro, listo para usar en system prompt de un LLM.
        Sé específico con ejemplos reales de las transcripciones.
        """
        
        summary = await self.llm_service.generate(
            prompt=summary_prompt,
            system="Eres un experto en resumir técnicas de marketing de forma estructurada.",
            max_tokens=2000,
            temperature=0.3  # Baja para resumen fiel
        )
        
        # 5. Cachear (24 horas)
        # await redis.setex(cache_key, 86400, summary)
        
        return summary

# En ContentGeneratorAgent:
class ContentGeneratorAgent(BaseAgent):
    async def _build_system_prompt(self, context: dict) -> str:
        """Build system prompt with training data siempre."""
        
        # 1. Obtener resumen de técnicas (cacheado, rápido)
        training_summary = await self.memory.get_training_summary(context['project_id'])
        
        # 2. Combinar con buyer persona y CJ
        buyer_text = json.dumps(context.get('buyer_persona', {}), ensure_ascii=False, indent=2) if context.get('buyer_persona') else "No disponible aún"
        cj_text = json.dumps(context.get('customer_journey', {}), ensure_ascii=False, indent=2) if context.get('customer_journey') else "No disponible aún"
        
        system = f"""
        Eres un experto en marketing digital especializado en crear contenido viral
        para redes sociales (TikTok, Instagram, YouTube).
        
        ## TÉCNICAS DE ENTRENAMIENTO (de Andrea Estratega - experta en contenido viral):
        {training_summary}
        
        ## BUYER PERSONA DEL CLIENTE:
        {buyer_text}
        
        ## CUSTOMER JOURNEY:
        {cj_text}
        
        ## TU ESTILO:
        - Usa las técnicas probadas de arriba en TODO tu contenido
        - Adapta técnicas al buyer persona específico (lenguaje, problemas, mentalidad)
        - Considera la fase del customer journey (awareness/consideration/purchase)
        - Sé específico y accionable (no genérico)
        - Genera contenido listo para usar (hooks, estructuras, CTAs)
        - Mantén conversación natural, recuerda contexto de mensajes anteriores
        """
        
        return system
```

**Comandos de validación:**
```bash
# Verificar que hay transcripciones en DB
psql $SUPABASE_URL -c "SELECT COUNT(*) FROM marketing_knowledge_base WHERE content_type='video_transcript';"

# Debe retornar > 0 (idealmente 300-400 chunks de 9 videos)
```

---

### TAREA 4: Modificar ContentGeneratorAgent para Usar Historial

**Herramientas a utilizar:**
- 🔧 MCP Serena: Analizar ContentGeneratorAgent completo
  - Comando: `find_symbol('ContentGeneratorAgent/execute', 'backend/src/agents/content_generator_agent.py', include_body=True)`
  - Comando: `find_symbol('ContentGeneratorAgent/_build_content_prompt', 'backend/src/agents/content_generator_agent.py', include_body=True)`
- 📚 Skills: conversation-memory, agent-memory-systems

**Objetivo:** Modificar ContentGeneratorAgent para usar `generate_with_messages()` con historial completo

**Pasos a seguir:**
1. Analizar `ContentGeneratorAgent.execute()` completo
2. Modificar para usar `format_messages_from_memory()`
3. Cambiar de `llm.generate()` a `llm.generate_with_messages()`
4. Asegurar que system prompt incluye técnicas de entrenamiento

**Archivos a modificar:**
- `backend/src/agents/content_generator_agent.py`

**Pseudocódigo:**
```python
# PATRÓN: Usar historial completo en lugar de solo prompt
class ContentGeneratorAgent(BaseAgent):
    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        # 1. Get context (buyer persona, docs, etc.)
        context = await self._get_context(chat_id, project_id, user_message)
        
        if not context['has_buyer_persona']:
            return {"success": False, "message": "Primero genera buyer persona"}
        
        # 2. Build system prompt con técnicas de entrenamiento
        system_prompt = await self._build_system_prompt(context)
        
        # 3. Formatear mensajes con historial completo
        messages = self.memory.format_messages_from_memory(
            chat_id=chat_id,
            system_prompt=system_prompt,
            current_user_message=user_message
        )
        
        # 4. Generar contenido con historial
        response = await self.llm.generate_with_messages(
            messages=messages,
            max_tokens=4000,
            temperature=0.8
        )
        
        # 5. Parsear y retornar
        content_ideas = self._parse_content_response(response)
        
        return {
            "success": True,
            "content_ideas": content_ideas,
            "message": f"✅ Generé {len(content_ideas)} ideas personalizadas."
        }
    
    async def _build_system_prompt(self, context: dict) -> str:
        """Build system prompt with training data."""
        # Obtener resumen de técnicas (cacheado)
        training_summary = await self.memory.get_training_summary(context['project_id'])
        
        # Combinar con buyer persona y CJ
        buyer_text = json.dumps(context.get('buyer_persona', {}), ensure_ascii=False, indent=2) if context.get('buyer_persona') else "No disponible"
        cj_text = json.dumps(context.get('customer_journey', {}), ensure_ascii=False, indent=2) if context.get('customer_journey') else "No disponible"
        
        return f"""
        Eres un experto en marketing digital especializado en contenido viral.
        
        ## TÉCNICAS DE ENTRENAMIENTO:
        {training_summary}
        
        ## BUYER PERSONA:
        {buyer_text}
        
        ## CUSTOMER JOURNEY:
        {cj_text}
        
        Genera contenido usando estas técnicas, adaptado al buyer persona.
        """
```

---

### TAREA 5: Verificar Carga de Historial en Endpoints

**Herramientas a utilizar:**
- 🔧 MCP Serena: Verificar endpoints de chat
  - Comando: `find_symbol('stream_message', 'backend/src/api/chat.py', include_body=True)`
  - Comando: `find_symbol('send_message', 'backend/src/api/chat.py', include_body=True)`
- 📚 Skills:
  - **conversation-memory**: Patrones de memoria persistente - usar para validar que carga sigue best practices
  - **systematic-debugging**: Si hay problemas con carga - debugging metódico
  - **verification-before-completion**: Validar que historial se carga correctamente antes de completar

**Objetivo:** Asegurar que `ensure_chat_loaded()` se llama ANTES de procesar cada mensaje

**Pasos a seguir:**
1. Verificar que `ensure_chat_loaded()` se llama en `/stream` y `/messages`
2. Verificar que se llama ANTES de `router_agent.process_stream()`
3. Asegurar que historial se añade a memoria después de cada mensaje

**Archivos a modificar:**
- `backend/src/api/chat.py` - Verificar orden de llamadas

**Pseudocódigo:**
```python
# PATRÓN: Cargar historial ANTES de procesar
@router.post("/{chat_id}/stream")
async def stream_message(...):
    # 1. Guardar mensaje del usuario
    await chat_service.create_message(...)
    
    # 2. ✅ CARGAR HISTORIAL ANTES de procesar
    await memory_manager.ensure_chat_loaded(chat_id=chat_id, project_id=user.project_id, limit=20)
    
    # 3. Añadir mensaje actual a memoria corto plazo
    await memory_manager.add_message_to_short_term(chat_id, "user", request.content)
    
    # 4. Procesar con agente (que ahora usará historial)
    async for chunk in router_agent.process_stream(...):
        yield chunk
    
    # 5. Guardar respuesta y añadir a memoria
    await memory_manager.add_message_to_short_term(chat_id, "assistant", final_content)
```

---

## ✅ Validación Final

**Test Conversacional:**
```python
# 1. Crear chat
chat_id = create_chat()

# 2. Mensaje 1
send_message(chat_id, "Hola, mi negocio es una tienda online de productos eco-friendly")

# 3. Mensaje 2 (debe recordar mensaje 1)
send_message(chat_id, "¿Qué más necesitas saber sobre mi negocio?")

# Verificar que respuesta menciona "tienda online" o "productos eco-friendly"
# (prueba que recuerda contexto)
```

**Test de Entrenamiento:**
```python
# 1. Verificar transcripciones en DB
# 2. Generar contenido
# 3. Verificar que respuesta menciona técnicas específicas de las transcripciones
# (ej: "hook de los primeros 3 segundos", "estructura de carrusel", etc.)
```

---

## 📚 Skills Adicionales Recomendadas

**Skills que mejoran la ejecución pero no son obligatorias:**

1. **langgraph** (Alternativa Futura):
   - **Para qué:** Si in-context learning no es suficiente, migrar a LangGraph con checkpoints
   - **Cuándo usar:** Después de validar que Opción A (messages array) funciona pero necesita más robustez
   - **Beneficio:** Conversaciones stateful más robustas, checkpoints persistentes

2. **langfuse** (Observabilidad - Opcional):
   - **Para qué:** Tracing y evaluación de llamadas LLM, debugging de prompts
   - **Cuándo usar:** Si hay problemas con calidad de respuestas o costos altos
   - **Beneficio:** Ver exactamente qué prompts se envían, cuántos tokens, calidad de respuestas

3. **plan-writing** (Planificación):
   - **Para qué:** Planificación estructurada antes de implementar
   - **Cuándo usar:** Al inicio de cada tarea para desglosar en pasos
   - **Beneficio:** Plan claro con dependencias y criterios de verificación

4. **executing-plans** (Ejecución con Checkpoints):
   - **Para qué:** Ejecutar plan con checkpoints de revisión
   - **Cuándo usar:** Si se crea un plan detallado con plan-writing
   - **Beneficio:** Ejecución controlada con puntos de revisión

5. **code-review-checklist** (Revisión):
   - **Para qué:** Checklist completo de revisión de código
   - **Cuándo usar:** Antes de completar cada tarea
   - **Beneficio:** Asegurar calidad, seguridad, performance, mantenibilidad

6. **requesting-code-review** (Solicitar Review):
   - **Para qué:** Solicitar code review al finalizar todas las tareas
   - **Cuándo usar:** Al completar todas las tareas del PRP
   - **Beneficio:** Validación externa antes de merge

---

## 📊 Score de Confianza: 9.5/10

**Razones:**
- ✅ Serena usado correctamente (proyecto brain-mkt activado)
- ✅ Archon consultado para documentación
- ✅ NO duplica funcionalidades existentes
- ✅ Enfocado en problema real (conversación + entrenamiento)
- ✅ Pseudocódigo basado en código real analizado
- ✅ Comandos Serena específicos incluidos
- ✅ Skills relevantes identificadas y explicadas
- ✅ Skills añadidas en cada tarea con justificación
- ⚠️ Necesita pruebas reales para validar efectividad

---

**PRP Listo para Implementación - Enfocado en Problema Real con Skills Optimizadas**

