# 🔍 Diagnóstico: Memoria, Contexto y Visualización

**Fecha:** 2026-01-27  
**Tarea relacionada:** Post-TAREA 8

---

## ❌ Problemas Identificados

### 1. **Memoria de Conversación NO se Carga al Iniciar Chat**

**Problema:**
- El método `MemoryManager.load_chat_history()` existe pero **NUNCA se llama**
- Solo se agregan mensajes nuevos con `add_message_to_short_term()`
- Cuando el usuario vuelve a un chat, el agente **no recuerda** mensajes anteriores
- `ConversationBufferWindowMemory` está vacío al inicio

**Código afectado:**
- `backend/src/services/memory_manager.py` - método `load_chat_history()` (línea 164) existe pero no se usa
- `backend/src/api/chat.py` - NO llama a `load_chat_history()` antes de procesar mensajes

**Impacto:**
- El agente no mantiene contexto de conversación
- Cada mensaje se trata como si fuera el primero
- No puede referirse a mensajes anteriores

---

### 2. **Router Agent Detecta TODO como Solicitud de Contenido**

**Problema:**
- El método `_is_content_request()` tiene keywords muy amplias:
  ```python
  content_keywords = [
      'dame', 'genera', 'crea', 'escribe', 'ideas',
      'posts', 'videos', 'scripts', 'contenido',
      'publica', 'redacta', 'hazme', 'necesito'
  ]
  ```
- Cualquier mensaje que contenga estas palabras activa `CONTENT_GENERATION`
- No considera el contexto de la conversación
- No diferencia entre solicitud explícita vs. conversación normal

**Código afectado:**
- `backend/src/agents/router_agent.py` - método `_is_content_request()` (línea 265)

**Impacto:**
- El agente siempre responde con ideas de contenido
- No puede mantener una conversación natural
- No puede responder preguntas o hacer seguimiento

---

### 3. **No Hay Forma de Ver Buyer Persona, Foro, Puntos de Dolor, Customer Journey**

**Problema:**
- No existen endpoints API para obtener/visualizar:
  - Buyer persona completo
  - Forum simulation
  - Pain points
  - Customer journey
- No hay UI en el frontend para mostrar estos datos
- El usuario no sabe si el agente generó estos datos o no
- No puede revisar, editar o descargar el buyer persona

**Código afectado:**
- `backend/src/api/chat.py` - NO hay endpoints `GET /api/chats/{chat_id}/buyer-persona`
- `frontend/` - NO hay componentes para visualizar buyer persona

**Impacto:**
- Usuario no puede verificar qué se generó
- No puede revisar la calidad del buyer persona
- No puede descargar o exportar los datos
- No puede editar o corregir información

---

### 4. **Buyer Persona Agent Solo Guarda en `full_analysis`**

**Problema:**
- El `BuyerPersonaAgent` solo guarda datos en `full_analysis`
- Los otros campos están vacíos:
  - `forum_simulation = {}`
  - `pain_points = {}`
  - `customer_journey = {}`
- Los agentes especializados (Forum Simulator, Pain Points Extractor, Customer Journey Creator) **NO están implementados**

**Código afectado:**
- `backend/src/agents/buyer_persona_agent.py` - línea 98-100:
  ```python
  forum_simulation={},  # TODO: Extract from buyer_persona_data
  pain_points={},  # TODO: Extract from buyer_persona_data
  customer_journey={}  # TODO: Extract from buyer_persona_data
  ```

**Impacto:**
- Solo se genera el buyer persona básico
- No se generan forum simulation, pain points, customer journey
- El sistema está incompleto según el PRP

---

### 5. **RAG vs Contexto Largo: Confusión Conceptual**

**Problema:**
- El usuario quiere que los documentos subidos estén **SIEMPRE en el contexto** del LLM
- Actualmente, los documentos solo se consultan vía RAG cuando se necesita
- El usuario espera que el agente "aprenda" todo lo subido, no solo lo consulte

**Diferencia conceptual:**
- **RAG (actual):** Consulta documentos cuando se necesita (búsqueda semántica)
- **Contexto largo (esperado):** Documentos siempre presentes en el prompt del LLM

**Código afectado:**
- `backend/src/services/memory_manager.py` - método `get_context()` solo hace RAG cuando hay `current_message`
- `backend/src/agents/content_generator_agent.py` - solo usa `relevant_docs` de RAG

**Impacto:**
- El agente no "conoce" los documentos subidos hasta que los busca
- No puede referirse a información de documentos en conversación normal
- El usuario siente que el agente no aprendió lo que subió

---

## ✅ Soluciones Propuestas

### Solución 1: Cargar Historial al Iniciar Chat

**Implementación:**
1. Llamar `load_chat_history()` cuando se abre un chat
2. Cargar últimos 10-20 mensajes desde DB
3. Poblar `ConversationBufferWindowMemory` antes de procesar nuevos mensajes

**Archivos a modificar:**
- `backend/src/api/chat.py` - llamar `load_chat_history()` en endpoints de chat
- `backend/src/api/chat.py` - endpoint `GET /api/chats/{chat_id}` debe cargar historial

---

### Solución 2: Mejorar Detección de Solicitudes de Contenido

**Implementación:**
1. Usar LLM para detectar intención (más preciso que keywords)
2. O mejorar keywords con contexto:
   - Verificar que el mensaje sea una solicitud explícita
   - Considerar el contexto de la conversación
   - No activar si el usuario está respondiendo preguntas

**Archivos a modificar:**
- `backend/src/agents/router_agent.py` - mejorar `_is_content_request()` o usar LLM

---

### Solución 3: Crear Endpoints y UI para Visualizar Datos

**Implementación:**
1. Crear endpoints API:
   - `GET /api/chats/{chat_id}/buyer-persona`
   - `GET /api/chats/{chat_id}/forum-simulation`
   - `GET /api/chats/{chat_id}/pain-points`
   - `GET /api/chats/{chat_id}/customer-journey`
2. Crear componentes frontend:
   - `BuyerPersonaView.tsx`
   - `ForumSimulationView.tsx`
   - `PainPointsView.tsx`
   - `CustomerJourneyView.tsx`

**Archivos a crear:**
- `backend/src/api/buyer_persona.py` - nuevos endpoints
- `frontend/app/components/BuyerPersonaView.tsx`
- `frontend/app/components/ForumSimulationView.tsx`
- `frontend/app/components/PainPointsView.tsx`
- `frontend/app/components/CustomerJourneyView.tsx`

---

### Solución 4: Implementar Agentes Faltantes

**Implementación:**
1. Crear `ForumSimulatorAgent`
2. Crear `PainPointsExtractorAgent`
3. Crear `CustomerJourneyCreatorAgent`
4. Integrar en el flujo del Router Agent

**Archivos a crear:**
- `backend/src/agents/forum_simulator_agent.py`
- `backend/src/agents/pain_points_agent.py`
- `backend/src/agents/customer_journey_agent.py`

---

### Solución 5: Contexto Largo para Documentos Subidos

**Implementación:**
1. Cuando se sube un documento, generar un resumen/extracto
2. Guardar resumen en memoria de largo plazo (no solo embeddings)
3. Incluir resumen de documentos en el prompt del LLM siempre
4. Mantener RAG para búsqueda específica, pero también contexto largo

**Archivos a modificar:**
- `backend/src/services/memory_manager.py` - agregar método `get_document_summaries()`
- `backend/src/agents/content_generator_agent.py` - incluir resúmenes en prompt

---

## 📋 TAREA 8.1 Propuesta

Ver `PRPs/marketing-brain-system-v3.md` - TAREA 8.1 para implementación detallada.
