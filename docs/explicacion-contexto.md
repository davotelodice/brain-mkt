# Explicación del Sistema de Conocimiento - Marketing Brain

> **Fecha:** 2026-01-30  
> **Contexto:** Aclaración técnica sobre RAG vs Fine-tuning y cómo funciona el sistema

---

## 📚 Tabla de Contenidos

1. [La Verdad Técnica: RAG vs Fine-tuning](#la-verdad-técnica)
2. [Comparación Honesta con n8n](#comparación-con-n8n)
3. [Cuándo Usar Qué Approach](#cuándo-usar-qué)
4. [Tutorial: System Prompts del Sistema](#tutorial-system-prompts)
5. [Limitaciones Actuales](#limitaciones-actuales)
6. [Recomendaciones de Mejora](#recomendaciones)

---

## 🎯 La Verdad Técnica

### Lo que implementamos (Context Engineering / RAG):

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT ENGINEERING / RAG                     │
│                                                                  │
│  Libro → Chunks → [Procesamiento] → Vectores → Búsqueda →       │
│  → Inyectar en PROMPT → LLM genera respuesta                    │
│                                                                  │
│  El modelo NO aprende nada. Solo recibe contexto relevante.     │
└─────────────────────────────────────────────────────────────────┘
```

### Fine-tuning Real (lo que NO tenemos):

```
┌─────────────────────────────────────────────────────────────────┐
│                    FINE-TUNING REAL                              │
│                                                                  │
│  Dataset de entrenamiento → Ajustar pesos del modelo →          │
│  → Modelo MODIFICADO que "sabe" el contenido                    │
│                                                                  │
│  El modelo SÍ aprende. El conocimiento está EN el modelo.       │
└─────────────────────────────────────────────────────────────────┘
```

**Conclusión:** Nuestro sistema es RAG avanzado con extracción de conceptos, NO es fine-tuning. El 95% de soluciones "empresariales de IA" funcionan así.

---

## ⚖️ Comparación con n8n

### Lo que hace n8n (correctamente):

| Paso | n8n | Nuestro Sistema |
|------|-----|-----------------|
| 1. Chunking | ✅ Divide documentos | ✅ Divide documentos |
| 2. Vectorización | ✅ Embeddings | ✅ Embeddings |
| 3. Búsqueda | ✅ Semántica | ✅ Semántica |
| 4. **Reranking** | ✅ Sí, selecciona más relevantes | ✅ Sí, con threshold |
| 5. Inyección en prompt | ✅ Contexto al LLM | ✅ Contexto al LLM |

### Diferencia REAL:

| Aspecto | n8n | Nuestro Sistema |
|---------|-----|-----------------|
| **Procesamiento de chunks** | Chunks crudos (texto tal cual) | Extracción de conceptos estructurados (LLM procesa cada chunk) |
| **Formato almacenado** | Texto plano | JSON estructurado: `{main_concepts, technical_terms, examples}` |
| **Flexibilidad de prompts** | Fácil de modificar en UI | Requiere editar código Python |
| **Orquestación** | Nodos visuales | Código con agentes especializados |
| **Memoria** | Nodo de memoria | MemoryManager con múltiples fuentes |

### Ventajas de n8n:
- UI visual para modificar flujos
- Fácil integración con herramientas externas
- Rápido de prototipar
- Menor curva de aprendizaje

### Ventajas de código propio:
- Control total sobre la lógica
- Procesamiento más sofisticado posible
- No dependes de nodos pre-hechos
- Escalabilidad sin límites de plataforma
- Personalización profunda de agentes

---

## 📊 Cuándo Usar Qué

| Caso de uso | Mejor approach |
|-------------|----------------|
| "Quiero que sepa sobre MI producto/servicio" | RAG (lo que tenemos) |
| "Quiero que escriba en MI estilo específico" | Fine-tuning |
| "Quiero que use terminología de MI industria" | RAG con extracción de términos |
| "Quiero que siga MI formato exacto siempre" | Fine-tuning o Few-shot en prompt |
| "Quiero que consulte MIS documentos" | RAG |

### ¿Cuándo vale la pena Fine-tuning?

1. **Sí vale:** Cuando necesitas que el modelo siga un ESTILO muy específico consistentemente
2. **No vale:** Para inyectar conocimiento factual (RAG es mejor)
3. **Consideración:** Fine-tuning cuesta dinero y requiere dataset bien preparado

---

## 🔧 Tutorial: System Prompts del Sistema

### ¿Dónde están los System Prompts?

```
backend/src/agents/
├── router_agent.py         → Decide qué agente usar
├── buyer_persona_agent.py  → Genera buyer personas
└── content_generator_agent.py → Genera contenido (EL PRINCIPAL)
```

### 1. RouterAgent - Decide qué hacer

**Archivo:** `backend/src/agents/router_agent.py`

**Ubicación del prompt:** Método `_get_system_prompt()`

```python
# Líneas ~45-80 aproximadamente
def _get_system_prompt(self) -> str:
    return """Eres un agente router inteligente...
    
    RUTAS DISPONIBLES:
    - content_generator: Para crear contenido
    - buyer_persona: Para analizar audiencia
    - general: Para preguntas generales
    
    Responde SOLO con JSON: {"route": "nombre_ruta", "confidence": 0.0-1.0}
    """
```

**⚠️ Limitación:** Este prompt EXIGE respuesta en JSON. Es parte del sistema de routing.

---

### 2. ContentGeneratorAgent - El Principal

**Archivo:** `backend/src/agents/content_generator_agent.py`

**Ubicación del prompt:** Método `_build_system_prompt()`

```python
# Líneas ~150-250 aproximadamente
def _build_system_prompt(self, context: dict) -> str:
    # Extrae información del contexto
    buyer_persona = context.get("buyer_persona", {})
    relevant_docs = context.get("relevant_docs", [])
    learned_concepts = context.get("learned_concepts", [])
    
    # Construye el prompt dinámicamente
    return f"""
    ## ROL
    Eres un experto en marketing digital...
    
    ## BUYER PERSONA
    {buyer_persona_text}
    
    ## DOCUMENTOS RELEVANTES
    {docs_text}
    
    ## CONOCIMIENTO DE LIBROS
    {learned_concepts_text}
    
    ## INSTRUCCIONES DE FORMATO
    Responde en el formato solicitado...
    """
```

**Cómo modificarlo:**
1. Abre `backend/src/agents/content_generator_agent.py`
2. Busca el método `_build_system_prompt`
3. Modifica el string del prompt
4. Reinicia el backend: `docker compose restart backend`

---

### 3. BuyerPersonaAgent

**Archivo:** `backend/src/agents/buyer_persona_agent.py`

**Ubicación del prompt:** Similar estructura, método que construye el system prompt.

---

### Cómo Ver el Prompt Actual en Acción

```bash
# Ver logs del backend con prompts (si tienes logging habilitado)
docker logs marketing-brain-backend -f | grep -i "system\|prompt"
```

### Cómo Hacer Cambios Seguros

1. **Backup:** Copia el archivo antes de modificar
2. **Cambio pequeño:** Modifica una cosa a la vez
3. **Test:** Prueba en el chat
4. **Rollback:** Si falla, restaura el backup

```bash
# Ejemplo de backup
cp backend/src/agents/content_generator_agent.py backend/src/agents/content_generator_agent.py.bak
```

---

## ⚠️ Limitaciones Actuales

### 1. Formato de Respuesta Forzado a JSON

**Problema:** Varios agentes exigen respuestas en JSON estructurado.

**Impacto:** 
- Menos flexibilidad en el output
- Difícil agregar ejemplos few-shot
- El frontend espera estructura específica

**Archivos afectados:**
- `router_agent.py` - Respuesta JSON obligatoria
- `content_generator_agent.py` - Posiblemente estructura forzada
- `buyer_persona_agent.py` - Estructura forzada

### 2. Prompts en Código, No en Config

**Problema:** Los prompts están hardcodeados en Python.

**Impacto:**
- Necesitas saber Python para modificar
- Requiere reiniciar backend
- No hay versionado separado de prompts

**Solución futura:** Mover prompts a archivos `.txt` o `.yaml` separados.

### 3. No Hay UI para Editar Prompts

**Problema:** No puedes modificar prompts desde el dashboard.

**Impacto:**
- Dependencia del desarrollador para cambios
- Ciclo de iteración lento

### 4. Chat Auto-crea Conversaciones

**Problema:** Cada vez que entras al chat se crea una conversación vacía.

**Impacto:**
- Base de datos llena de chats basura
- UX confusa

---

## 💡 Recomendaciones

### Corto Plazo (TAREA 6.2 y 6.3):

1. **Cambiar output a Markdown** - Más flexibilidad, mejor UX
2. **Arreglar auto-creación de chats** - Solo crear cuando hay mensaje

### Mediano Plazo:

1. **Externalizar prompts** - Mover a archivos YAML/TXT editables
2. **Agregar UI de configuración** - Panel para editar prompts
3. **Mejorar logging** - Ver qué prompt se usó en cada request

### Largo Plazo:

1. **Evaluar fine-tuning** - Para casos específicos de estilo
2. **A/B testing de prompts** - Comparar diferentes versiones
3. **Métricas de calidad** - Evaluar respuestas automáticamente

---

## 📁 Archivos Clave para Referencia

| Archivo | Propósito |
|---------|-----------|
| `backend/src/agents/router_agent.py` | Decide qué agente usar |
| `backend/src/agents/content_generator_agent.py` | Genera contenido - PROMPT PRINCIPAL |
| `backend/src/agents/buyer_persona_agent.py` | Analiza audiencia |
| `backend/src/services/memory_manager.py` | Recopila contexto de todas las fuentes |
| `backend/src/services/rag_service.py` | Búsqueda semántica |
| `backend/src/services/llm_service.py` | Comunicación con OpenAI/OpenRouter |
| `frontend/app/components/ChatInterface.tsx` | UI del chat |
| `frontend/app/components/MessageBubble.tsx` | Renderiza mensajes |

---

## 🔍 DIAGNÓSTICO TÉCNICO DEL SISTEMA

### Problema 1: Formato JSON Forzado (TAREA 6.2)

**Ubicación del problema:**
- `backend/src/agents/content_generator_agent.py` líneas 420-449

**Código problemático:**
```python
format_section = (
    """CRÍTICO: Responde SOLO con JSON válido. No incluyas texto antes o después del JSON.
No uses markdown.

Estructura requerida:
{
  "ideas": [
    {
      "titulo": "...",
      "plataforma": "...",
      ...
    }
  ]
}
"""
```

**Flujo actual:**
1. Usuario pide: "Dame 5 ideas de contenido"
2. Sistema detecta `mode = "ideas_json"` 
3. Prompt FUERZA respuesta en JSON
4. LLM responde con JSON estructurado
5. `router_agent.py` convierte JSON → texto con formato (líneas 262-313)
6. Frontend muestra texto plano (NO Markdown real)

**Problemas:**
- Limita creatividad del LLM (formato rígido)
- Difícil agregar ejemplos few-shot
- El frontend NO renderiza Markdown real (solo `whitespace-pre-wrap`)

---

### Problema 2: Auto-creación de Chats (TAREA 6.3)

**Ubicación del problema:**
- `frontend/app/components/ChatPageContent.tsx` líneas 27-38

**Código problemático:**
```typescript
if (chatIdFromUrl) {
  setChatId(chatIdFromUrl)
} else {
  // ⚠️ PROBLEMA: Crea chat automáticamente
  const newChat = await createChat({ title: 'Nueva Conversación' })
  setChatId(newChat.id)
  router.replace(`/?chat=${newChat.id}`)
}
```

**Comportamiento actual:**
- Usuario entra a `/` → Se crea chat vacío
- Usuario refresca → Se crea OTRO chat vacío
- Resultado: Base de datos llena de chats basura

**Comportamiento deseado (como ChatGPT):**
- Usuario entra → Ve lista de chats existentes
- Sin chat seleccionado → Muestra UI de "selecciona o crea"
- Chat se crea SOLO cuando usuario envía primer mensaje

---

## 📁 Archivos Clave para Referencia

| Archivo | Propósito |
|---------|-----------|
| `backend/src/agents/router_agent.py` | Decide qué agente usar |
| `backend/src/agents/content_generator_agent.py` | Genera contenido - PROMPT PRINCIPAL |
| `backend/src/agents/buyer_persona_agent.py` | Analiza audiencia |
| `backend/src/services/memory_manager.py` | Recopila contexto de todas las fuentes |
| `backend/src/services/rag_service.py` | Búsqueda semántica |
| `backend/src/services/llm_service.py` | Comunicación con OpenAI/OpenRouter |
| `frontend/app/components/ChatInterface.tsx` | UI del chat |
| `frontend/app/components/MessageList.tsx` | Renderiza mensajes (sin Markdown) |
| `frontend/app/components/ChatPageContent.tsx` | Lógica de inicialización de chat |

---

*Documento creado como parte de TAREA 7 - Documentación del Sistema*
