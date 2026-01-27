---
name: autonomous-agent-patterns
description: "Patrones de diseño para construir agentes de código autónomos. Cubre integración de herramientas, sistemas de permisos, automatización de navegador y workflows human-in-the-loop. Usar al construir agentes IA, diseñar APIs de herramientas, implementar sistemas de permisos o crear asistentes de código autónomos."
---

# 🕹️ Patrones de Agentes Autónomos

> Patrones de diseño para construir agentes de código autónomos, inspirados en [Cline](https://github.com/cline/cline) y [OpenAI Codex](https://github.com/openai/codex).

## Cuándo Usar Esta Skill

Usar esta skill cuando:

- Construir agentes de IA autónomos
- Diseñar APIs de herramientas/function calling
- Implementar sistemas de permisos y aprobación
- Crear automatización de navegador para agentes
- Diseñar workflows human-in-the-loop

---

## 1. Arquitectura Central de Agente

### 1.1 Loop de Agente

```
┌─────────────────────────────────────────────────────────────┐
│                     LOOP DE AGENTE                           │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Think   │───▶│  Decide  │───▶│   Act    │              │
│  │ (Reason) │    │ (Plan)   │    │ (Execute)│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲                               │                     │
│       │         ┌──────────┐          │                     │
│       └─────────│ Observe  │◀─────────┘                     │
│                 │ (Result) │                                │
│                 └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Arquitectura Multi-Modelo

Usar diferentes modelos para diferentes propósitos:
- Modelo rápido para planificación
- Modelo poderoso para razonamiento complejo
- Modelo especializado para generación de código

---

## 2. Patrones de Diseño de Herramientas

### 2.1 Schema de Herramienta

Todas las herramientas deben tener:
- Nombre descriptivo
- Descripción clara
- Parámetros bien definidos con tipos
- Manejo de errores apropiado

### 2.2 Herramientas Esenciales para Agentes de Código

- Operaciones de archivo: read_file, write_file, edit_file, list_directory
- Comprensión de código: search_code, get_definition, get_references
- Terminal: run_command, read_output
- Navegador: open_browser, click_element, type_text, screenshot
- Contexto: ask_user, search_web

### 2.3 Diseño de Herramienta de Edición

Edición precisa de archivos con detección de conflictos usando patrones search/replace.

---

## 3. Patrones de Permisos y Seguridad

### 3.1 Niveles de Permiso

- AUTO: Completamente automático - no necesita aprobación
- ASK_ONCE: Preguntar una vez por sesión
- ASK_EACH: Preguntar cada vez
- NEVER: Nunca permitir

### 3.2 Patrón de UI de Aprobación

Sistema que muestra diálogos de aprobación basados en nivel de riesgo y configuración de permisos.

### 3.3 Sandboxing

Ejecutar código/comandos en entorno aislado con validación de paths y comandos permitidos.

---

## 4. Automatización de Navegador

### 4.1 Patrón de Herramienta de Navegador

Automatización de navegador usando Playwright/Puppeteer que permite debugging visual y testing web.

### 4.2 Patrón de Agente Visual

Agente que usa screenshots para entender páginas web, puede identificar elementos visualmente sin selectores.

---

## 5. Gestión de Contexto

### 5.1 Patrones de Inyección de Contexto

Sistema de gestión de contexto que permite agregar archivos, carpetas, URLs y problemas al contexto del agente.

### 5.2 Checkpoint/Resume

Guardar y restaurar estado del agente para tareas de larga duración.

---

## 6. Integración MCP (Model Context Protocol)

### 6.1 Patrón de Servidor MCP

Agente que puede descubrir y usar herramientas MCP dinámicamente, incluyendo creación de nuevas herramientas basadas en descripciones.

---

## Lista de Verificación de Mejores Prácticas

### Diseño de Agente

- [ ] Descomposición clara de tareas
- [ ] Granularidad apropiada de herramientas
- [ ] Manejo de errores en cada paso
- [ ] Visibilidad de progreso para usuario

### Seguridad

- [ ] Sistema de permisos implementado
- [ ] Operaciones peligrosas bloqueadas
- [ ] Sandbox para código no confiable
- [ ] Audit logging habilitado

### UX

- [ ] UI de aprobación es clara
- [ ] Actualizaciones de progreso proporcionadas
- [ ] Undo/rollback disponible
- [ ] Explicación de acciones

---

## Recursos

- [Cline](https://github.com/cline/cline)
- [OpenAI Codex](https://github.com/openai/codex)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)

## Ejemplos de Uso

### Ejemplo 1: Construir un Agente de Código Autónomo
**Situación**: Quieres crear un agente que pueda editar código automáticamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero construir un agente de código autónomo"
2. Cursor usará esta skill para:
   - Implementar el loop de agente (Think-Decide-Act-Observe)
   - Configurar herramientas esenciales (read_file, edit_file, etc.)
   - Implementar sistema de permisos apropiado
   - Agregar sandboxing para seguridad
   - Aplicar todos los patrones correctos

**Resultado**: Un agente de código autónomo bien diseñado que puede editar código de forma segura y controlada.

### Ejemplo 2: Agregar Automatización de Navegador a tu Agente
**Situación**: Quieres que tu agente pueda interactuar con páginas web.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero agregar automatización de navegador a mi agente"
2. Cursor:
   - Implementará herramientas de navegador (open_url, click, type_text)
   - Configurará captura de screenshots para debugging visual
   - Implementará patrón de agente visual si es necesario
   - Integrará con el loop de agente existente

**Resultado**: Tu agente puede ahora interactuar con páginas web de forma autónoma.

### Ejemplo 3: Implementar Sistema de Permisos para tu Agente
**Situación**: Quieres controlar qué puede hacer tu agente para mayor seguridad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar un sistema de permisos para mi agente"
2. Cursor:
   - Configurará niveles de permiso (AUTO, ASK_ONCE, ASK_EACH, NEVER)
   - Implementará UI de aprobación
   - Agregará validación de riesgo
   - Configurará sandboxing para operaciones peligrosas

**Resultado**: Un sistema de permisos robusto que mantiene tu agente seguro mientras permite autonomía apropiada.
