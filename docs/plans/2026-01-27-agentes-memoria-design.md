# Diseño: Sistema de Agentes IA con Triple Memoria

**Fecha:** 2026-01-27  
**Autor:** Sistema de IA  
**Estado:** En validación  
**Versión:** 1.0

---

## 📋 Resumen Ejecutivo

Este documento define la arquitectura e implementación del sistema de agentes IA con triple memoria para el Marketing Second Brain System. El diseño fue validado mediante proceso de brainstorming colaborativo, considerando trade-offs de rendimiento, costo y complejidad.

### Decisiones Clave Tomadas

1. **Framework de Agentes:** LangGraph (state machine)
2. **Gestión de Memoria:** MemoryManager centralizado
3. **Routing:** Rule-based (sin LLM extra)
4. **LLM Provider:** Configurable (OpenAI/OpenRouter)
5. **Estrategia de Implementación:** Incremental (MVP → completo)
6. **Búsqueda Semántica:** Simple (TAREA 4) → Híbrida (TAREA 5)
7. **Manejo de Errores:** Retry con exponential backoff
8. **Generación de Buyer Persona:** Prompt único con plantilla completa

---

## 🎯 Objetivos del Sistema

### Funcionales
- ✅ Router Agent que decide qué agente ejecutar según contexto
- ✅ Buyer Persona Agent genera análisis completo (40+ preguntas)
- ✅ Sistema de triple memoria (short/long/semantic)
- ✅ Búsqueda semántica en knowledge base
- ✅ NO generar contenido automáticamente (solo bajo petición explícita)

### No Funcionales
- ⚡ Latencia < 3s para routing
- 💰 Costo optimizado (evitar LLM calls innecesarias)
- 🔒 Aislamiento estricto por project_id
- 🛡️ Manejo robusto de errores (retry + logging)

---

## 🏗️ Arquitectura General

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│                  /api/chat/{chat_id}/message                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Router Agent                             │
│              (LangGraph State Machine)                       │
│  Rule-based routing: ¿buyer_persona? ¿docs? ¿content_req?   │
└──────────────────┬──────────────┬────────────────────────────┘
                   │              │
        ┌──────────┘              └──────────┐
        ▼                                    ▼
┌─────────────────┐                  ┌─────────────────┐
│ Buyer Persona   │                  │ Content         │
│ Agent           │                  │ Generator Agent │
│ (40+ questions) │                  │ (on-demand)     │
└────────┬────────┘                  └─────────────────┘
         │
         │ usa
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Memory Manager                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Short-term   │  │ Long-term    │  │ Semantic     │      │
│  │ (últimos 10  │  │ (PostgreSQL) │  │ (pgvector    │      │
│  │  mensajes)   │  │              │  │  RAG)        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │
         │ usa
         ▼
┌─────────────────────────────────────────────────────────────┐
│                     LLM Service                              │
│  Provider: Configurable (OpenAI / OpenRouter)               │
│  Model: gpt-4o / claude-3.5-sonnet (via OpenRouter)         │
│  Retry: 3 intentos con exponential backoff                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 DECISIÓN 1: Framework de Agentes - LangGraph

### Contexto
El sistema necesita un framework para orquestar múltiples agentes con estados bien definidos (INITIAL, BUYER_PERSONA, WAITING, CONTENT_GENERATION, etc.).

### Opciones Evaluadas

**A. LangGraph (✅ SELECCIONADA)**
- Graph-based state machine
- Checkpointing integrado
- Visualización de flujos
- Producción probada (LinkedIn, Uber)

**B. LangChain tradicional**
- Agent with tools
- Más simple
- Menos control sobre flujo

**C. Custom (sin framework)**
- Control total
- Más código manual

### Decisión Final: **LangGraph**

**Razones:**
1. El PRP define estados explícitos → state machine es natural
2. Built-in checkpointing para debugging
3. Escalable para agregar más agentes
4. Comunidad activa y documentación

**Trade-offs Aceptados:**
- ➖ Curva de aprendizaje mayor que LangChain puro
- ➕ Mejor control y debugging

**Impacto:**
- TAREA 4: Implementar Router Agent como LangGraph state machine
- Archivos: `backend/src/agents/router_agent.py`

---

## 📦 DECISIÓN 2: Gestión de Memoria - MemoryManager Centralizado

### Contexto
El sistema tiene 3 tipos de memoria que deben trabajar juntos. Cada agente necesita acceso consistente.

### Opciones Evaluadas

**A. MemoryManager centralizado (✅ SELECCIONADA)**
```python
class MemoryManager:
    def __init__(self):
        self.short_term = ConversationBufferWindowMemory(k=10)
        self.db_session = AsyncSession
        self.retriever = VectorStoreRetriever
    
    async def get_context(self, chat_id: UUID) -> dict:
        # Combina las 3 memorias
        return {
            "recent_chat": [...],
            "buyer_persona": {...},
            "relevant_docs": [...]
        }
```

**B. Memoria descentralizada**
- Cada agente accede directamente a lo que necesita

### Decisión Final: **MemoryManager centralizado**

**Razones:**
1. DRY: Lógica de memoria en un solo lugar
2. Optimización: Podemos agregar caché fácilmente
3. Testing: Más fácil mockear
4. Consistencia: Todos los agentes ven el mismo contexto

**Trade-offs Aceptados:**
- ➖ Una clase más
- ➕ Código más mantenible

**Impacto:**
- TAREA 4: Implementar `backend/src/services/memory_manager.py`
- Todos los agentes usan la misma interfaz

---

## 📦 DECISIÓN 3: Routing Strategy - Rule-based

### Contexto
El Router Agent debe decidir qué agente ejecutar según el estado del chat y el mensaje del usuario.

### Opciones Evaluadas

**A. LLM-based routing**
- El LLM decide qué agente ejecutar
- Más inteligente pero más lento/caro

**B. Rule-based routing (✅ SELECCIONADA)**
```python
async def route(self, chat_id: UUID, user_message: str) -> AgentState:
    context = await self.memory_manager.get_context(chat_id)
    
    # Reglas fijas
    if not context.get('buyer_persona'):
        return AgentState.BUYER_PERSONA
    
    if self._has_pending_documents(context):
        return AgentState.DOCUMENT_PROCESSING
    
    if self._is_content_request(user_message):
        return AgentState.CONTENT_GENERATION
    
    return AgentState.WAITING
```

### Decisión Final: **Rule-based**

**Razones:**
1. Más rápido: Sin latencia de LLM extra
2. Más barato: Sin costo de API extra
3. Más predecible: Sabemos exactamente qué hará
4. Suficiente: Las reglas son claras y simples

**Trade-offs Aceptados:**
- ➖ Menos flexible (solo reglas fijas)
- ➕ Más confiable y rápido

**Migración Futura:**
Si en TAREA 5+ necesitamos más inteligencia, podemos migrar a LLM-based manteniendo la interfaz.

**Impacto:**
- TAREA 4: Implementar routing con if/else en `router_agent.py`

---

## 📦 DECISIÓN 4: LLM Provider - Configurable

### Contexto
El usuario **NO** tiene API key de Anthropic, solo OpenAI y OpenRouter.

### Opciones Evaluadas

**A. Solo OpenAI**
- Simple
- Sin redundancia

**B. OpenAI + OpenRouter fallback**
- Redundancia
- Más complejo

**C. Configurable por variable de entorno (✅ SELECCIONADA)**
```python
class LLMService:
    def __init__(self):
        provider = os.getenv("LLM_PROVIDER", "openai")
        
        if provider == "openai":
            self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4o"
        else:  # openrouter
            self.client = AsyncOpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = "anthropic/claude-3.5-sonnet"
```

### Decisión Final: **Configurable**

**Razones:**
1. Máxima flexibilidad: Cambiar provider sin tocar código
2. Testing: Probar con diferentes modelos fácilmente
3. Producción: Si un provider falla, cambiar en .env

**Configuración en .env:**
```bash
LLM_PROVIDER=openai  # o "openrouter"
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
```

**Impacto:**
- TAREA 4: Implementar `backend/src/services/llm_service.py`

---

## 📦 DECISIÓN 5: Implementación Incremental

### Contexto
El sistema tiene 7 agentes especializados. ¿Todos a la vez o incremental?

### Opciones Evaluadas

**A. Todos los agentes desde el principio**
- Sistema completo día 1
- Difícil debuggear

**B. Incremental (✅ SELECCIONADA)**

**Fase 1 (TAREA 4 - MVP):**
```
backend/src/agents/
├── base_agent.py            # Clase base compartida
├── router_agent.py          # Orquestador
└── buyer_persona_agent.py   # Agente más crítico
```

**Fase 2 (TAREA 5-6 - Expansión):**
```
Agregar:
├── pain_points_agent.py
├── journey_agent.py
└── content_generator.py
```

**Fase 3 (Futuro - Avanzados):**
```
Agregar:
├── forum_simulator.py
└── document_processor_agent.py
```

### Decisión Final: **Incremental (Opción B)**

**Razones:**
1. Validación paso a paso
2. Más fácil debuggear
3. MVP viable: Router + Buyer Persona ya es funcional
4. Menos riesgo

**Impacto:**
- TAREA 4: Solo 3 archivos (base, router, buyer_persona)
- TAREA 5: Agregar 3 agentes más

---

## 📦 DECISIÓN 6: Búsqueda Semántica (RAG) - Progresiva

### Contexto
El sistema necesita buscar información relevante usando embeddings.

### Estrategia Progresiva (✅ SELECCIONADA)

**TAREA 4 (MVP): Búsqueda simple**
```python
async def search_relevant_docs(
    chat_id: UUID, 
    query: str, 
    limit: int = 5
) -> List[str]:
    # 1. Generar embedding
    query_embedding = await embedding_service.generate_embedding(query)
    
    # 2. Buscar usando función de Supabase
    result = await db.execute(
        select(marketing_match_documents(
            query_embedding=query_embedding,
            match_count=limit,
            filter_project_id=project_id
        ))
    )
    
    return [doc.content for doc in result]
```

**TAREA 5 (RAG Training): Búsqueda híbrida + reranking**
- Agregar filtrado por metadata
- Agregar reranking con LLM
- Optimizar para YouTubers + libros

### Decisión Final: **Progresiva**

**Razones:**
1. No optimizar prematuramente
2. TAREA 4 enfocada en agentes
3. TAREA 5 enfocada en RAG avanzado

**Impacto:**
- TAREA 4: Implementar búsqueda simple en `memory_manager.py`
- TAREA 5: Mejorar con metadata + reranking

---

## 📦 DECISIÓN 7: Manejo de Errores - Retry con Exponential Backoff

### Contexto
Las APIs de LLM pueden fallar (timeout, rate limit, errores transitorios).

### Opción Seleccionada (✅)

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError))
)
async def generate(self, prompt: str) -> str:
    return await self.client.chat.completions.create(...)
```

### Decisión Final: **Retry con exponential backoff**

**Razones:**
1. Más robusto: APIs fallan temporalmente
2. Mejor UX: Usuario no ve errores transitorios
3. Estándar: Todas las apps de producción lo usan

**Configuración:**
- Máximo 3 intentos
- Espera: 2s, 4s, 8s (exponencial)
- Solo para errores recuperables

**Impacto:**
- TAREA 4: Agregar decorator `@retry` en `llm_service.py`
- Dependencia: `tenacity` (ya en pyproject.toml)

---

## 📦 DECISIÓN 8: Generación de Buyer Persona - Prompt Único

### Contexto
El Buyer Persona Agent debe generar 40+ preguntas organizadas en 11 categorías.

### Opciones Evaluadas

**A. Prompt único con plantilla completa (✅ SELECCIONADA)**
```python
async def generate_buyer_persona(self, chat_id: UUID) -> dict:
    # 1. Cargar plantilla completa (11 categorías, 40+ preguntas)
    template = await self._load_buyer_persona_template()
    
    # 2. Obtener contexto (documentos del usuario)
    context = await self.memory_manager.get_context(chat_id)
    relevant_docs = context['relevant_docs']
    
    # 3. Prompt completo
    prompt = f"""
    Eres un experto en marketing que crea buyer personas ULTRA DETALLADAS.
    
    Documentos del usuario:
    {relevant_docs}
    
    Genera un buyer persona siguiendo esta estructura COMPLETA:
    {template}
    
    INSTRUCCIONES CRÍTICAS:
    - Debes responder TODAS las 40+ preguntas (no puedes saltarte ninguna)
    - Usa información REAL de los documentos proporcionados
    - Si falta información, infiere basado en contexto lógico
    - Sigue el formato del ejemplo "Ana" (enfermera, 35 años, Barcelona)
    - Respuesta en formato JSON estructurado
    
    EJEMPLO DE RESPUESTA ESPERADA (caso "Ana"):
    {{
      "nombre": "Ana",
      "edad": 35,
      "profesion": "Enfermera",
      "ubicacion": "Barcelona",
      ...
    }}
    """
    
    response = await self.llm.generate(prompt, max_tokens=8000)
    return json.loads(response)
```

**B. Prompt en fases (11 llamadas)**
- Más controlable pero más lento

### Decisión Final: **Prompt único (Opción A)**

**Razones:**
1. Más rápido: 1 llamada vs 11 llamadas
2. Más coherente: Todo el persona es consistente
3. GPT-4 maneja 8k tokens bien

**Requisitos Críticos:**
- ✅ Debe responder TODAS las preguntas (no saltarse ninguna)
- ✅ Incluir respuestas de ejemplo (caso "Ana" del PRP)
- ✅ Formato JSON estructurado

**Plantilla de Buyer Persona:**
```markdown
# Plantilla de Buyer Persona (11 categorías)

1. Aspectos Demográficos (5 preguntas)
   - Nombre
   - Edad
   - Nivel de estudios
   - Ingresos aproximados
   - Ubicación
   - Estado civil

2. Hogar y Familia (3 preguntas)
   - ¿Cuántas personas viven en su hogar?
   - ¿Qué hace en su tiempo libre?
   - ¿Qué responsabilidades tiene?

3. Trabajo (3 preguntas)
   - ¿Dónde trabaja?
   - ¿Cuáles son sus mayores retos laborales?
   - ¿Cómo es su vida laboral vs personal?

[... 8 categorías más con 30+ preguntas ...]

## Ejemplo Completo: "Ana"
{
  "nombre": "Ana",
  "edad": 35,
  "profesion": "Enfermera",
  "ubicacion": "Barcelona",
  "salario": "35000",
  "problema": "Inestabilidad laboral genera ansiedad",
  "solucion_buscada": "Preparar examen EIR para plaza fija",
  ...
}
```

**Impacto:**
- TAREA 4: Implementar en `buyer_persona_agent.py`
- TAREA 4: Cargar plantilla desde `contenido/buyer-plantilla.md`

---

## 🔧 Estructura de Archivos (TAREA 4)

```
backend/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Clase base compartida
│   │   ├── router_agent.py            # Orquestador (LangGraph)
│   │   └── buyer_persona_agent.py     # Genera buyer persona (40+ preguntas)
│   │
│   ├── services/
│   │   ├── memory_manager.py          # MemoryManager centralizado
│   │   ├── llm_service.py             # LLM configurable (OpenAI/OpenRouter)
│   │   └── rag_service.py             # Búsqueda semántica (simple)
│   │
│   └── api/
│       └── chat.py                     # Ya existe, agregar endpoint streaming
│
├── tests/
│   ├── test_agents.py                  # Tests de agentes
│   └── test_memory.py                  # Tests de memoria
│
└── contenido/
    └── buyer-plantilla.md              # Plantilla con 11 categorías

pyproject.toml:
  - Agregar: langgraph, tenacity
```

---

## 🧪 Plan de Testing (TAREA 4)

### Tests Unitarios

**1. Test de Router Agent**
```python
async def test_router_no_buyer_persona():
    """Si no hay buyer persona, debe rutear a BUYER_PERSONA"""
    router = RouterAgent(memory_manager, llm_service)
    
    # Mock: chat sin buyer persona
    memory_manager.get_context = AsyncMock(return_value={
        'buyer_persona': None,
        'documents_uploaded': True
    })
    
    state = await router.route(chat_id, "Hola")
    assert state == AgentState.BUYER_PERSONA
```

**2. Test de MemoryManager**
```python
async def test_memory_manager_combines_three_types():
    """MemoryManager debe combinar short/long/semantic"""
    mm = MemoryManager(db, retriever, short_term)
    
    context = await mm.get_context(chat_id)
    
    assert 'recent_chat' in context
    assert 'buyer_persona' in context
    assert 'relevant_docs' in context
```

**3. Test de LLM Service**
```python
async def test_llm_retry_on_rate_limit():
    """LLM debe reintentar en rate limit"""
    llm = LLMService()
    
    # Mock: falla 2 veces, éxito en intento 3
    with patch('openai.AsyncOpenAI.chat.completions.create') as mock:
        mock.side_effect = [
            RateLimitError("Rate limit"),
            RateLimitError("Rate limit"),
            MagicMock(choices=[MagicMock(message=MagicMock(content="OK"))])
        ]
        
        result = await llm.generate("test")
        assert result == "OK"
        assert mock.call_count == 3
```

### Tests de Integración

**4. Test de flujo completo**
```python
async def test_buyer_persona_generation_flow():
    """Test end-to-end: mensaje → routing → buyer persona"""
    # 1. Usuario envía mensaje
    response = await client.post(
        f"/api/chats/{chat_id}/messages",
        json={"content": "Quiero crear mi buyer persona"}
    )
    
    # 2. Sistema debe ejecutar Buyer Persona Agent
    assert response.status_code == 200
    
    # 3. Debe guardar buyer persona en DB
    persona = await db.get(MarketingBuyerPersona, filter_by={'chat_id': chat_id})
    assert persona is not None
    assert len(persona.data) > 0  # JSON con 40+ preguntas
```

---

## 📊 Métricas de Éxito (TAREA 4)

### Funcionales
- ✅ Router Agent decide correctamente en 100% de casos básicos
- ✅ Buyer Persona Agent genera 40+ preguntas completas
- ✅ Sistema NO genera contenido automáticamente
- ✅ MemoryManager combina 3 tipos de memoria

### No Funcionales
- ⚡ Latencia de routing < 500ms
- ⚡ Latencia de generación de buyer persona < 10s
- 🔒 Aislamiento 100% por project_id
- 🛡️ Retry exitoso en 95% de errores transitorios
- 📊 Coverage de tests > 80%

---

## 🚀 Secuencia de Implementación (TAREA 4)

### Paso 1: Servicios Base (Fundación)
1. `backend/src/services/llm_service.py` - LLM configurable + retry
2. `backend/src/services/memory_manager.py` - MemoryManager centralizado
3. `backend/src/services/rag_service.py` - Búsqueda semántica simple

### Paso 2: Agentes (Core)
4. `backend/src/agents/base_agent.py` - Clase base
5. `backend/src/agents/router_agent.py` - Router con LangGraph
6. `backend/src/agents/buyer_persona_agent.py` - Generador de buyer persona

### Paso 3: Integración API
7. Actualizar `backend/src/api/chat.py` - Integrar router en endpoint
8. Agregar endpoint streaming (preparación para TAREA 6)

### Paso 4: Testing
9. `backend/tests/test_agents.py` - Tests unitarios de agentes
10. `backend/tests/test_memory.py` - Tests de memoria
11. Tests de integración end-to-end

### Paso 5: Validación
12. Ejecutar linters (ruff, mypy)
13. Ejecutar tests (pytest con coverage > 80%)
14. Pruebas manuales de flujos críticos

---

## 🔗 Referencias al PRP

Este diseño implementa las siguientes secciones del PRP:

### TAREA 4: Agente IA con Memoria (NÚCLEO DEL SISTEMA)
- **Sección:** "Arquitectura de Agentes (LangChain + LangGraph)"
- **Líneas:** 1416-1476 del PRP
- **Decisiones aplicadas:**
  - DECISIÓN 1: LangGraph para state machine
  - DECISIÓN 2: MemoryManager centralizado
  - DECISIÓN 3: Rule-based routing
  - DECISIÓN 4: LLM configurable
  - DECISIÓN 5: Implementación incremental (Fase 1)
  - DECISIÓN 7: Retry con exponential backoff
  - DECISIÓN 8: Prompt único para buyer persona

### TAREA 5: Entrenamiento RAG (YouTubers + libros de marketing)
- **Sección:** "Entrenamiento con YouTubers de Marketing"
- **Decisiones aplicadas:**
  - DECISIÓN 6: Migrar de búsqueda simple → híbrida + reranking

---

## 📝 Notas de Implementación

### Prioridades
1. **Corrección** > Performance (primero que funcione)
2. **Testing** > Features (tests antes de agregar complejidad)
3. **Simplicidad** > Optimización prematura

### Gotchas Conocidos
- ⚠️ Mypy puede reportar errores con LangChain (ignorar con mypy.ini)
- ⚠️ LangGraph requiere checkpointer para persistencia (implementar en TAREA 6)
- ⚠️ OpenAI rate limits: usar batching en embeddings (ya implementado en TAREA 3)

### Deuda Técnica Aceptada (para resolver después)
- [ ] Caché de contexto en MemoryManager (TAREA 6)
- [ ] Reranking con LLM en RAG (TAREA 5)
- [ ] Monitoring de costos por agente (futuro)
- [ ] A/B testing de prompts (futuro)

---

## ✅ Criterios de Aceptación (TAREA 4)

### Funcionales
- [ ] Router Agent rutea correctamente según estado del chat
- [ ] Buyer Persona Agent genera 40+ preguntas completas
- [ ] MemoryManager combina 3 tipos de memoria
- [ ] Sistema NO genera contenido sin petición explícita
- [ ] Aislamiento estricto por project_id

### Técnicos
- [ ] Tests unitarios > 80% coverage
- [ ] Ruff check pasa sin errores
- [ ] Mypy pasa (con excepciones en mypy.ini)
- [ ] Tests de integración end-to-end pasan

### Performance
- [ ] Routing < 500ms
- [ ] Generación buyer persona < 10s
- [ ] Retry exitoso en errores transitorios

---

## 🎯 Próximos Pasos

1. **Validar este diseño** con el usuario
2. **Actualizar PRP** con referencias a este documento
3. **Implementar** siguiendo la secuencia definida
4. **Testing continuo** durante implementación
5. **Documentar** en `docs/TAREAS_PENDIENTES_Y_GOTCHAS.md`

---

## 📚 Anexos

### A. Ejemplo de Prompt Completo para Buyer Persona

```python
BUYER_PERSONA_PROMPT = """
Eres un experto en marketing digital especializado en crear buyer personas ULTRA DETALLADAS.

Tu trabajo es analizar los documentos del usuario y generar un buyer persona completo siguiendo la plantilla de 11 categorías con 40+ preguntas.

## Documentos del Usuario:
{relevant_docs}

## Plantilla de Buyer Persona:

### 1. Aspectos Demográficos (5 preguntas)
- Nombre (inventa uno realista)
- Edad
- Nivel de estudios
- Ingresos aproximados
- Ubicación geográfica
- Estado civil

### 2. Hogar y Familia (3 preguntas)
- ¿Cuántas personas viven en su hogar?
- ¿Qué hace en su tiempo libre?
- ¿Qué responsabilidades familiares tiene?

### 3. Trabajo (3 preguntas)
- ¿Dónde trabaja? (industria, tipo de empresa)
- ¿Cuáles son sus mayores retos laborales?
- ¿Cómo equilibra vida laboral vs personal?

### 4. Comportamiento (2 preguntas)
- ¿Cómo son sus relaciones interpersonales?
- ¿Qué expresiones y lenguaje usa su grupo social?

### 5. Problema (2 preguntas)
- ¿Qué dolor o necesidad activa su búsqueda de solución?
- ¿Cómo tu producto/servicio soluciona ese problema?

### 6. Búsqueda de la Solución (3 preguntas)
- ¿Dónde busca información? (redes sociales, Google, amigos)
- ¿Cómo te encuentra?
- ¿Cómo reacciona a mensajes comerciales?

### 7. Objeciones y Barreras (2 preguntas)
- ¿Qué barreras le impiden comprar?
- ¿Qué excusas usa para no decidirse?

### 8. Miedos e Inseguridades (2 preguntas)
- ¿Qué odia encontrar en productos similares?
- ¿Qué experiencias negativas previas ha tenido?

### 9. Comparación con Competencia (5 preguntas)
- ¿Qué factores compara entre diferentes opciones?
- ¿Qué diferencias encuentra entre competidores?
- ¿Qué hace mejor la competencia?
- ¿Qué haces mejor tú?
- ¿Por qué te elige a ti finalmente?

### 10. Tu Producto o Servicio (4 preguntas)
- ¿Qué beneficios percibe claramente?
- ¿Qué beneficios NO percibe (pero existen)?
- ¿Qué productos complementarios podría necesitar?
- ¿Qué dudas tiene post-compra?

### 11. Información Adicional Relevante
- Cualquier dato específico del contexto que sea relevante

## INSTRUCCIONES CRÍTICAS:

1. **COMPLETO**: Debes responder TODAS las preguntas. No puedes saltarte ninguna.
2. **REALISTA**: Basa tus respuestas en la información de los documentos.
3. **COHERENTE**: Todas las respuestas deben ser coherentes entre sí.
4. **ESPECÍFICO**: Usa detalles concretos, no generalidades.
5. **FORMATO**: Respuesta en JSON estructurado.

## EJEMPLO DE RESPUESTA (caso "Ana" - Enfermera preparando EIR):

{
  "aspectos_demograficos": {
    "nombre": "Ana",
    "edad": 35,
    "nivel_estudios": "Grado en Enfermería",
    "ingresos": "35000",
    "ubicacion": "Barcelona",
    "estado_civil": "Soltera"
  },
  "hogar_familia": {
    "integrantes_hogar": "Vive sola, visita a padres los fines de semana",
    "tiempo_libre": "Lee, hace yoga, sale con amigas enfermeras",
    "responsabilidades": "Cuidar de su madre (diabética), pagar alquiler"
  },
  "trabajo": {
    "donde_trabaja": "Hospital público en Barcelona (contratos temporales)",
    "retos_laborales": "Inestabilidad laboral, turnos rotatorios agotadores, falta de plaza fija",
    "vida_laboral_personal": "Difícil planificar vida personal con turnos cambiantes"
  },
  "comportamiento": {
    "relaciones": "Grupo cercano de compañeras enfermeras, activa en foros de EIR",
    "lenguaje": "Usa términos como 'EIRsilente', 'rEIRsilente', 'temario mil hojas'"
  },
  "problema": {
    "dolor": "Ansiedad por inestabilidad laboral, cansancio de turnos, quiere plaza fija",
    "solucion": "Preparar examen EIR para conseguir especialidad y plaza fija mejor pagada"
  },
  "busqueda_solucion": {
    "donde_busca": "Grupos de Facebook de EIR, foros, Instagram de academias",
    "como_te_encuentra": "Anuncios en Facebook/Instagram, recomendaciones de amigas",
    "reaccion_comercial": "Escéptica de promesas, busca estadísticas de aprobados"
  },
  "objeciones": {
    "barreras": "Precio alto de academias, miedo a fracasar, falta de tiempo por turnos",
    "excusas": "'Empiezo el mes que viene', 'Este año solo investigo', 'Muy caro'"
  },
  "miedos": {
    "que_odia": "Academias con material desactualizado, sin soporte personalizado",
    "experiencias_negativas": "Compró curso online barato que nadie actualizaba"
  },
  "comparacion_competencia": {
    "factores_comparacion": "Precio, tasa de aprobados, flexibilidad horaria, material actualizado",
    "diferencias": "Algunas academias muy caras pero prestigiosas, otras baratas pero básicas",
    "mejor_competencia": "Academia X tiene años de trayectoria y estadísticas públicas",
    "mejor_tu": "Flexibilidad total online, soporte 24/7, grupo de WhatsApp activo",
    "por_que_te_elige": "Puede estudiar en turnos nocturnos, precio intermedio, comunidad activa"
  },
  "tu_producto": {
    "beneficios_percibidos": "Flexibilidad horaria, material actualizado, comunidad de apoyo",
    "beneficios_no_percibidos": "Networking con otras enfermeras especialistas, orientación laboral post-EIR",
    "productos_complementarios": "Simulacros de examen, masterclasses con especialistas",
    "dudas_post_compra": "'¿El temario es realmente completo?', '¿Y si no apruebo?'"
  },
  "info_adicional": "Prefiere formato digital, activa en Instagram, confía en testimonios reales"
}

## TU RESPUESTA:

Genera el buyer persona completo en formato JSON siguiendo la estructura del ejemplo.
"""
```

---

**Fin del Documento de Diseño**

Este documento será la guía de implementación para TAREA 4. Cualquier duda o cambio debe documentarse aquí.
