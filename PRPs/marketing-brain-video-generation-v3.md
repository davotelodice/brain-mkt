# PRP v3 - Marketing Brain: Extensión de Generación de Videos con IA (LTX-2)

```yaml
name: "marketing-brain-video-generation-extension"
version: "3.0-ES"
descripcion: |
  PRP para implementar la extensión de generación de videos con fal.ai LTX-2
  sobre el sistema Marketing Brain existente. Incluye entrenamiento de LoRA,
  agentes Cinematography y VideoProduction, servicios fal.ai/storage/FFmpeg,
  APIs REST, migración DB y frontend Estudio de Videos (LoRAs, Producir, Galería).
```

---

## Principios

1. **Contexto es Rey**: API fal.ai **solo** en `docs/documentacion-api-fal-ltx2.md` (fuente única y más actualizada PARA FAL AI). Resto (FastAPI, Supabase, Next.js…) en Archon.
2. **Análisis simbólico**: Usar Serena (get_symbols_overview, find_symbol) antes de leer archivos completos.
3. **No tocar lo que funciona**: Agentes y APIs existentes se mantienen; solo se añaden módulos nuevos.
4. **Validación en 3 niveles**: Lint → Tests unitarios → Integración.

---

## 🎯 Objetivo

Extender Marketing Brain con un **módulo de video con IA** que permita:

- Entrenar LoRAs personalizados (fal.ai LTX-2 Video Trainer) con dataset de videos del usuario.
- Generar videos de la persona hablando a cámara en bloques de ~20 s con continuidad visual.
- Gestionar LoRAs, proyectos de video y galería desde un nuevo “Estudio de Videos” en el dashboard.

**Estado final deseado:** Usuario sube dataset → entrena LoRA → escribe/pega guion → sistema genera video en bloques (ContentGeneratorAgent + CinematographyAgent + fal.ai LTX) → usuario ve/descarga desde Galería.

---

## 💡 Por Qué

- **Valor**: Videos de la persona para redes sin grabar cada vez; reutilización de guiones del chat.
- **Integración**: Aprovecha ContentGeneratorAgent, RAG, memoria y chat ya existentes.
- **Resuelve**: Producción de video repetitiva y costosa; unifica guion + generación en un flujo.

---

## 📋 Qué (alcance técnico)

- **Backend**: FalAIService, LoRATrainingService, VideoGenerationService, VideoProcessingService (FFmpeg), StorageService; CinematographyAgent y VideoProductionAgent; 4 tablas nuevas (marketing_loras, marketing_video_projects, marketing_video_blocks, marketing_video_renders); APIs: `/api/loras`, `/api/video-projects`, `/api/video-renders`, `/api/storage`.
- **Frontend**: Sección “Estudio de Videos” con Mis LoRAs, Producir Video, Galería; componentes de upload, progreso, preview y descarga.
- **Documentación**: API fal.ai **exclusivamente** en `docs/documentacion-api-fal-ltx2.md` (fuente única actualizada); resto en Archon.

### Criterios de Éxito

- [ ] Usuario puede entrenar un LoRA (upload dataset → polling → LoRA listo).
- [ ] Usuario puede crear proyecto de video desde guion y generar video en bloques.
- [ ] Video final se renderiza (FFmpeg), se guarda y se puede descargar desde Galería.
- [ ] Tests automatizados (unit + integración) y lint pasan.

---

## 🧰 Skills y MCPs por Fase

### Planificación
- **brainstorming**: Antes de implementar nuevas features (obligatorio).
- **architecture**: Decisiones de diseño (agentes, servicios, APIs).
- **writing-plans** / **planning-with-files**: Desglose de tareas multi-paso.

### Desarrollo
- **Serena** (obligatorio): get_symbols_overview, find_symbol, search_for_pattern; no leer archivos completos sin necesidad.
- **Archon**: rag_get_available_sources(); rag_search_knowledge_base(query corto, source_id); rag_search_code_examples si aplica.
- **clean-code**, **python-patterns**, **backend-dev-guidelines**: Backend FastAPI/Python.
- **nextjs-best-practices**, **frontend-dev-guidelines**: Frontend Next.js.

### Documentación
- **documentation-templates**: README, API docs.
- **API fal.ai**: **solo** `docs/documentacion-api-fal-ltx2.md` (fuente única y más actualizada para LTX-2/ltx-video). Para FastAPI, Supabase, Next.js, etc. usar Archon.

### Testing y validación
- **test-driven-development**: Antes de implementación.
- **test-fixing**: Cuando fallen tests.
- **lint-and-validate**: Tras cada cambio.
- **verification-before-completion**: Evidencia de comandos antes de dar por terminado.

---

## 📦 Contexto Necesario

### Documentación

**API fal.ai (LTX-2 trainer + ltx-video) – fuente única:**
- **Usar siempre y solo:** `docs/documentacion-api-fal-ltx2.md`
- Es la fuente **más actualizada** para esta API; no depender de Archon ni de URLs externas para firma de endpoints, parámetros, schemas ni ejemplos Python.
- Incluye: input/output schema, parámetros (number_of_frames, rank, etc.), restricción frames % 8 == 1, ejemplos cURL y Python, respuesta (lora_file, video, etc.).

**Resto del stack (FastAPI, Supabase, Next.js, Pydantic, etc.):**
- **Usar Archon** como fuente prioritaria:
  - `rag_get_available_sources()` → obtener source_id de FastAPI, Supabase, Next.js, etc.
  - `rag_search_knowledge_base(query="...", source_id="...", match_count=5)`
  - `rag_search_code_examples(query="...", source_id="...", match_count=3)` cuando haga falta.  

### Análisis de codebase (Serena)

```yaml
# Estructura de agentes (patrón a seguir)
get_symbols_overview('backend/src/agents/base_agent.py')
get_symbols_overview('backend/src/agents/content_generator_agent.py')
find_symbol('BaseAgent', 'backend/src/agents/base_agent.py', depth=1, include_body=False)
find_symbol('ContentGeneratorAgent', 'backend/src/agents/content_generator_agent.py', depth=1, include_body=False)

# APIs existentes (patrón de routers)
get_symbols_overview('backend/src/api/chat.py')
# Patrón: router = APIRouter(prefix="/api/...", tags=[...]); @router.post/get/delete
# main.py: app.include_router(chat.router), etc.

# Dónde registrar nuevo router
# backend/src/main.py líneas 78-82 (include_router)
```

**Archivos clave a referenciar:**
- `backend/src/agents/base_agent.py`: BaseAgent (execute, _get_context).
- `backend/src/agents/content_generator_agent.py`: ContentGeneratorAgent (execute, _build_system_prompt).
- `backend/src/api/chat.py`: router, stream_message, send_message, get_agent_system.
- `backend/src/main.py`: include_router para auth, chat, analysis, documents, knowledge.

### Gotchas conocidos

**CRÍTICO (fal.ai LTX-2):**
- `number_of_frames` debe cumplir **frames % 8 == 1**.
- Valores válidos: `1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89, 97, 105, 113, 121`.
- Usar **FalAIService.validate_frame_count(num_frames)** antes de cualquier llamada a la API.

**GOTCHA (fal_client):**
- **Entrenamiento** (async/largo): `fal_client.submit` → endpoint **fal-ai/ltx2-video-trainer**.
- **Generación**: `fal_client.subscribe` → endpoint **fal-ai/ltx-video**.
- No intercambiar submit/subscribe ni los endpoints.

**PATRÓN (agentes):**
- Agentes nuevos heredan **BaseAgent** y reciben `llm_service` (y opcionalmente `rag_service`).
- No modificar BaseAgent ni ContentGeneratorAgent; solo extender.

**PATRÓN (servicios async con fal):**
- Llamadas a `fal_client` son bloqueantes: usar **asyncio.to_thread()** para no bloquear el event loop de FastAPI.

**Proyecto (stack y convenciones):**
- SQLAlchemy 2.0, Pydantic v2, FastAPI.
- Prefijo **marketing_** en todas las tablas nuevas.

---

## 🏗️ Blueprint de Implementación

### Modelos y estructura

- **Nuevas tablas** (migración 004): marketing_loras, marketing_video_projects, marketing_video_blocks, marketing_video_renders (ver INITIAL.md sección DISEÑO DE BASE DE DATOS).
- **Modelos SQLAlchemy**: En `backend/src/db/models.py` siguiendo convención existente.
- **Schemas Pydantic**: En `backend/src/schemas/` (lora.py, video_project.py, etc.) para request/response de las nuevas APIs.

### Comandos Serena para replicar análisis

```bash
# Ver estructura backend
list_dir(relative_path="backend/src", recursive=False)

# Agentes
get_symbols_overview('backend/src/agents/base_agent.py')
get_symbols_overview('backend/src/agents/content_generator_agent.py')

# API
get_symbols_overview('backend/src/api/chat.py')
search_for_pattern('include_router', 'backend/src/main.py', context_lines_after=2)
```

---

## 📝 Lista de Tareas

### TAREA 0: Instalar y configurar MCP Serena (OBLIGATORIO)

**Herramientas:**
- MCP Serena: activate_project, check_onboarding_performed.
- Skill environment-setup-guide.

**Objetivo:** Serena activo para análisis simbólico.

**Pasos:**
1. Activar proyecto: `activate_project(project="/home/david/brain-mkt")`
2. Verificar onboarding: `check_onboarding_performed()`
3. Probar: `get_symbols_overview('backend/src/main.py')`

**Criterios:**
- [ ] Serena activo.
- [ ] get_symbols_overview ejecutable.

---

### TAREA 1: Migración DB y modelos (004 video system)

**Herramientas:**
- MCP Serena: get_symbols_overview('backend/src/db/models.py'), find_symbol para ver patrón de modelos.
- Skill database-design si hay dudas de esquema.

**Objetivo:** 4 tablas nuevas + modelos SQLAlchemy + schemas Pydantic básicos.

**Pasos:**
1. Crear `backend/db/004_video_system.sql` (copiar desde INITIAL.md sección DISEÑO DE BASE DE DATOS).
2. Añadir modelos en `backend/src/db/models.py` (MarketingLora, MarketingVideoProject, MarketingVideoBlock, MarketingVideoRender).
3. Ejecutar migración en DB de desarrollo.
4. Añadir schemas en `backend/src/schemas/lora.py` y `backend/src/schemas/video_project.py` (según endpoints abajo).

**Criterios:**
- [ ] Migración aplicada sin errores.
- [ ] Modelos y schemas coherentes con INITIAL.

**Validación:**
```bash
# Desde backend/
python -c "from src.db.models import MarketingLora; print('OK')"
```

---

### TAREA 2: FalAIService (cliente fal.ai)

**Herramientas:**
- **Documentación fal.ai (única fuente):** leer `docs/documentacion-api-fal-ltx2.md` (input/output schema, parámetros, ejemplos Python, submit/status/subscribe).
- Skill python-patterns, clean-code.

**Objetivo:** Cliente con train_lora, check_training_status, generate_video, check_generation_status; validate_frame_count y duration_to_frames.

**Pasos:**
1. Leer `docs/documentacion-api-fal-ltx2.md` para firma exacta de fal-client (submit, status, subscribe) y parámetros.
2. Crear `backend/src/services/fal_ai_service.py` con FalAIService(__init__(api_key), train_lora(...), check_training_status(request_id), generate_video(...), check_generation_status(request_id), validate_frame_count, duration_to_frames).
3. Usar asyncio.to_thread para llamadas fal_client (evitar bloquear event loop).
4. Inyectar FAL_KEY desde config/env.

**Criterios:**
- [ ] train_lora y generate_video usan endpoints correctos (ltx2-video-trainer, ltx-video).
- [ ] Validación de frames (frames % 8 == 1).
- [ ] Tests unitarios con mock de fal_client.

**Validación:**
```bash
pytest backend/tests/unit/test_fal_ai_service.py -v
ruff check backend/src/services/fal_ai_service.py
```

---

### TAREA 3: LoRATrainingService + StorageService (upload, polling, almacenamiento)

**Herramientas:**
- MCP Serena: get_symbols_overview de algún service existente (ej. chat_service.py) para patrón de inyección.
- Archon: rag_search_knowledge_base("Supabase storage upload", source_id de Supabase) si hace falta.
- Skill backend-dev-guidelines.

**Objetivo:** Subir dataset a Storage, llamar FalAIService.train_lora, polling, descargar lora_file y guardar en Supabase Storage; StorageService.download_and_store, get_user_storage_usage.

**Pasos:**
1. Crear `backend/src/services/storage_service.py` (download_and_store desde URL, upload a Supabase; get_user_storage_usage desde DB o Storage).
2. Crear `backend/src/services/lora_training_service.py` (orquesta upload → train_lora → polling → download_and_store; actualiza marketing_loras).
3. Definir bucket y rutas (loras/{user_id}/{lora_id}.safetensors, etc.) según INITIAL.

**Criterios:**
- [ ] Dataset sube; entrenamiento inicia; estado se actualiza; LoRA se descarga y guarda.
- [ ] Tests con mocks de FalAIService y Storage.

**Validación:**
```bash
pytest backend/tests/unit/test_lora_training_service.py -v
ruff check backend/src/services/
```

---

### TAREA 4: API LoRAs (POST train, GET list, GET status, DELETE)

**Herramientas:**
- MCP Serena: get_symbols_overview('backend/src/api/knowledge.py') o similar para patrón router + Depends.
- Skill api-patterns, backend-dev-guidelines.

**Objetivo:** Endpoints POST /api/loras/train, GET /api/loras, GET /api/loras/{id}/status, DELETE /api/loras/{id}; autenticación con usuario actual.

**Pasos:**
1. Crear `backend/src/api/loras.py` con APIRouter(prefix="/api/loras", tags=["loras"]).
2. Implementar endpoints; usar LoRATrainingService y StorageService; schemas en schemas/lora.py.
3. Registrar en main.py: app.include_router(loras.router).

**Criterios:**
- [ ] Cliente puede listar, entrenar, consultar estado y eliminar LoRA.
- [ ] Respuestas con schemas Pydantic; errores HTTP adecuados.

**Validación:**
```bash
ruff check backend/src/api/loras.py
# Manual: curl POST /api/loras/train (con auth) y GET /api/loras
```

---

### TAREA 5: CinematographyAgent + VideoProductionAgent

**Herramientas:**
- MCP Serena: find_symbol('BaseAgent/execute', 'backend/src/agents/base_agent.py', include_body=True); find_symbol('ContentGeneratorAgent/execute', 'backend/src/agents/content_generator_agent.py', include_body=True).
- Skill ai-agents-architect, python-patterns.

**Objetivo:** CinematographyAgent (generate_cinematography con LLM + RAG de libros); VideoProductionAgent (create_video_project, generate_video orquestando bloques).

**Pasos:**
1. Crear `backend/src/agents/video_agents/` (__init__.py, cinematography_agent.py, video_production_agent.py).
2. CinematographyAgent: hereda BaseAgent; método generate_cinematography(dialogo, estilo, duracion) → dict con escenografia, camara, audio_notes, continuidad (prompt según INITIAL).
3. VideoProductionAgent: create_video_project (dividir guion en bloques, enriquecer con CinematographyAgent, guardar en marketing_video_projects); generate_video (por cada bloque llamar a VideoGenerationService, guardar bloques, render final).
4. Integrar con RAG de libros aprendidos para conocimiento de cinematografía si está disponible.

**Criterios:**
- [ ] Guion simple → descripción cinematográfica por bloque.
- [ ] create_video_project y generate_video orquestan correctamente (con mocks de VideoGenerationService si aún no existe).

**Validación:**
```bash
pytest backend/tests/test_agents.py -v -k "cinematography or video_production"
ruff check backend/src/agents/
```

---

### TAREA 6: VideoGenerationService + VideoProcessingService (FFmpeg)

**Herramientas:**
- **Documentación fal.ai:** `docs/documentacion-api-fal-ltx2.md` (generación ltx-video, parámetros, respuesta video.url).
- Skill python-patterns; dependencias: opencv-python, ffmpeg-python.

**Objetivo:** VideoGenerationService.generate_block (FalAIService.generate_video, first_frame para continuidad), extract_last_frame (OpenCV o FFmpeg); VideoProcessingService para concatenar bloques y normalizar audio (FFmpeg); render_final_video.

**Pasos:**
1. Crear `backend/src/services/video_generation_service.py` (generate_block, uso de FalAIService; extracción de último frame).
2. Crear `backend/src/services/video_processing_service.py` (concatenar MP4, audio; render_final_video).
3. Integrar con StorageService para guardar bloques y render final en Supabase.

**Criterios:**
- [ ] Un bloque se genera con prompt + lora_url + first_frame_url.
- [ ] Varios bloques se concatenan en un solo MP4.
- [ ] Tests con archivos de prueba o mocks.

**Validación:**
```bash
pytest backend/tests/unit/test_video_generation_service.py -v
ruff check backend/src/services/video_generation_service.py backend/src/services/video_processing_service.py
```

---

### TAREA 7: API Video Projects (POST create, POST generate, GET status)

**Herramientas:**
- MCP Serena: get_symbols_overview('backend/src/api/chat.py') para patrón de endpoints con body.
- Skill api-patterns.

**Objetivo:** POST /api/video-projects (crear proyecto), POST /api/video-projects/{id}/generate (disparar generación), GET /api/video-projects/{id} (status y detalle).

**Pasos:**
1. Crear `backend/src/api/video_projects.py` con router prefix /api/video-projects.
2. Implementar endpoints; usar VideoProductionAgent, VideoGenerationService, StorageService; BackgroundTasks para generación larga si aplica.
3. Registrar router en main.py.

**Criterios:**
- [ ] Crear proyecto con script + lora_id + config; iniciar generación; consultar estado.
- [ ] Respuestas alineadas con schemas de INITIAL.

**Validación:**
```bash
ruff check backend/src/api/video_projects.py
# Integración: POST create → POST generate → GET status hasta completed
```

---

### TAREA 8: API Video Renders y Storage (lista, download, delete, cleanup)

**Herramientas:**
- MCP Serena: get_symbols_overview('backend/src/api/documents.py') para patrón delete y list.
- Skill backend-dev-guidelines.

**Objetivo:** GET /api/video-renders, GET /api/video-renders/{id}/download, DELETE /api/video-renders/{id}, POST /api/storage/cleanup; GET /api/storage/usage.

**Pasos:**
1. Crear `backend/src/api/video_renders.py` y `backend/src/api/storage.py`.
2. Implementar endpoints; usar StorageService y modelos marketing_video_renders.
3. Registrar routers en main.py.

**Criterios:**
- [ ] Listar renders; descargar por ID; eliminar; cleanup y uso de almacenamiento.

**Validación:**
```bash
ruff check backend/src/api/video_renders.py backend/src/api/storage.py
```

---

### TAREA 9: Frontend – Layout y Mis LoRAs

**Herramientas:**
- MCP Serena: get_symbols_overview('frontend/app/components/Sidebar.tsx'); list_dir('frontend/app/dashboard').
- Skill nextjs-best-practices, frontend-dev-guidelines.

**Objetivo:** Layout Estudio de Videos (sidebar Videos: LoRAs, Producir, Galería); página Mis LoRAs (lista, TrainLoRAModal, upload dataset, polling estado).

**Pasos:**
1. Crear `frontend/app/dashboard/videos/layout.tsx` y `frontend/app/components/videos/VideosSidebar.tsx`.
2. Crear `frontend/app/dashboard/videos/loras/page.tsx`, LoRACard, TrainLoRAModal; llamadas a /api/loras.
3. Añadir enlace "Videos" en Sidebar principal al layout de videos.

**Criterios:**
- [ ] Navegación a /dashboard/videos/loras; listar LoRAs; abrir modal y subir dataset; ver progreso de entrenamiento.

**Validación:**
```bash
cd frontend && npm run build
# Manual: navegar a /dashboard/videos/loras y entrenar un LoRA
```

---

### TAREA 10: Frontend – Producir Video y Galería

**Herramientas:**
- MCP Serena: get_symbols_overview de una página del dashboard existente (ej. knowledge).
- Skill nextjs-best-practices.

**Objetivo:** Página Producir (guion, selector LoRA, config, botón Generar, preview y progreso); Página Galería (lista renders, filtros, descarga, eliminar); StorageStats/StorageWarning.

**Pasos:**
1. Crear `frontend/app/dashboard/videos/produce/page.tsx` y componentes VideoScriptInput, VideoConfigPanel, VideoPreview; integración con /api/video-projects.
2. Crear `frontend/app/dashboard/videos/gallery/page.tsx` y VideoGalleryCard; llamadas a /api/video-renders y /api/storage/usage.
3. Opcional: en ChatInterface botón "Generar Video con este Guion" que redirige a produce con guion pre-cargado.

**Criterios:**
- [ ] Crear proyecto desde guion y LoRA; ver progreso; ver video en Galería; descargar y eliminar.

**Validación:**
```bash
npm run build
# Flujo E2E: producir video → esperar → galería → descargar
```

---

## 🔄 Bucle de Validación

### Nivel 1: Sintaxis y estilo
```bash
ruff check backend/src/ --fix
mypy backend/src/
cd frontend && npm run lint
```

### Nivel 2: Tests unitarios
- Tests para FalAIService, LoRATrainingService, StorageService, agentes de video, servicios de video.
- Ejecutar: `pytest backend/tests/ -v`

### Nivel 3: Integración
- Backend levantado: `python -m backend.run` o según README.
- Probar: POST /api/loras/train (con auth), GET /api/loras, POST /api/video-projects, POST /api/video-projects/{id}/generate, GET /api/video-renders.

---

## ✅ Checklist de Calidad PRP

- [x] API fal.ai definida como **solo** docs/documentacion-api-fal-ltx2.md (fuente única actualizada).
- [x] Archon usado para el resto del stack (FastAPI, Supabase, Next.js, etc.).
- [x] Serena usada para patrones (get_symbols_overview, find_symbol); comandos incluidos para replicar.
- [x] Tarea 0 (Serena) incluida.
- [x] Skills por fase identificadas.
- [x] Tareas con herramientas, pasos, criterios y validación.
- [x] Gotchas (frames % 8 == 1, submit vs subscribe, asyncio.to_thread) documentados.
- [x] Referencias a INITIAL.md para esquema DB, agentes y flujos.

---

## 📊 Score de Confianza

**Estado actual: 8/10.** Objetivo: **10/10** cuando se rellenen las respuestas de la sección *Preguntas para 10/10* y se incorporen al PRP.

- **Contexto:** INITIAL.md detallado; fal.ai fijado a `docs/documentacion-api-fal-ltx2.md`; Archon para el resto del stack.
- **Serena:** Comandos concretos; patrones de agentes y APIs referenciados.
- **Skills:** Por fase; Archon como respaldo para todo lo que no sea API fal.
- **Tareas:** Desglose claro; validación en 3 niveles.
- **Para 10/10:** Completar variables de entorno, nombres de buckets, auth, versiones, timeouts y patrones de tests (ver sección siguiente).

---

## 🎯 Preguntas para llegar a 10/10

Rellena lo que sepas; lo que falte se puede definir en implementación. Cuando tengas las respuestas, incorpóralas al PRP (sección "Contexto Necesario" o en la tarea correspondiente) para que el agente no tenga huecos.

**Config y entorno**
1. ¿Nombre exacto de la variable de API key de fal? (ej. `FAL_KEY`, `FAL_API_KEY`). ¿Está ya en `.env.example` o hay que añadirla?
2. ¿El backend lee env desde `os.getenv`, `pydantic-settings`, o otro? ¿Dónde está el patrón actual (archivo de config)?

**Supabase Storage**
3. ¿Nombre del bucket para videos/LoRAs? (ej. `marketing-videos`, `videos`). ¿Ya existe o hay que crearlo en Supabase?
4. ¿Hay políticas RLS o permisos ya definidos para ese bucket que debamos seguir, o las definimos en esta feature?

**Auth en nuevas APIs**
5. ¿Cómo se obtiene el `user_id` actual en los endpoints existentes? (ej. Depends que lee JWT/session). ¿Nombre del dependency (ej. `get_current_user`) para reutilizar en `/api/loras`, `/api/video-projects`, etc.?

**Dependencias y versiones**
6. ¿Versión fija de `fal-client` que quieras usar? (ej. en pyproject.toml o requirements).
7. ¿`opencv-python` y `ffmpeg-python` ya están en el proyecto o se añaden? ¿Alguna versión concreta por compatibilidad?

**fal.ai y resiliencia**
8. ¿Timeouts que quieras para entrenamiento (ej. 3600 s) y para generación de un bloque (ej. 300 s)?
9. ¿Hay rate limits conocidos de fal.ai (req/min) que debamos documentar o respetar (retries, backoff)?

**Tests**
10. ¿Patrón de tests del backend? (ej. `conftest.py` con fixtures, uso de pytest-mock, base URL de API). ¿Hay que seguir un nombre/carpeta concreto para tests de servicios nuevos (ej. `tests/unit/test_*_service.py`)?

**Frontend**
11. ¿Las llamadas al backend desde Next.js van a `/api/...` (proxy al backend) o a una URL base tipo `NEXT_PUBLIC_API_URL`? ¿Dónde está definida esa base hoy?

Cuando tengas estas respuestas, pégalas aquí o dime "añade las respuestas al PRP" y las integro en el documento para dejarlo listo a 10/10.

---

## ❌ Anti-Patrones a Evitar

- No leer archivos completos del backend sin usar antes get_symbols_overview/find_symbol.
- No asumir firma de fal_client: usar **solo** `docs/documentacion-api-fal-ltx2.md`.
- No usar funciones sync bloqueantes en rutas async sin asyncio.to_thread.
- No olvidar validar number_of_frames (frames % 8 == 1) antes de llamar a fal.ai.
- No modificar BaseAgent ni ContentGeneratorAgent; solo extender con nuevos agentes y servicios.
