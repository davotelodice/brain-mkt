---
name: planning-with-files
version: "2.1.2"
description: Implementa planificación basada en archivos estilo Manus para tareas complejas. Crea task_plan.md, findings.md y progress.md. Usar al iniciar tareas complejas de múltiples pasos, proyectos de investigación o cualquier tarea que requiera >5 llamadas a herramientas.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: "echo '[planning-with-files] Listo. Se auto-activa para tareas complejas, o invocar manualmente con /planning-with-files'"
  PreToolUse:
    - matcher: "Write|Edit|Bash"
      hooks:
        - type: command
          command: "cat task_plan.md 2>/dev/null | head -30 || true"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] Archivo actualizado. Si esto completa una fase, actualizar estado de task_plan.md.'"
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/check-complete.sh"
---

# Planificación con Archivos

Trabajar como Manus: Usar archivos markdown persistentes como tu "memoria de trabajo en disco."

## Importante: Dónde Van los Archivos

Al usar esta skill:

- **Las plantillas** se almacenan en el directorio de la skill en `${CLAUDE_PLUGIN_ROOT}/templates/`
- **Tus archivos de planificación** (`task_plan.md`, `findings.md`, `progress.md`) deben crearse en **tu directorio de proyecto** — la carpeta donde estás trabajando

| Ubicación | Qué Va Allí |
|-----------|-------------|
| Directorio de skill (`${CLAUDE_PLUGIN_ROOT}/`) | Plantillas, scripts, docs de referencia |
| Tu directorio de proyecto | `task_plan.md`, `findings.md`, `progress.md` |

Esto asegura que tus archivos de planificación vivan junto a tu código, no enterrados en la carpeta de instalación de la skill.

## Inicio Rápido

Antes de CUALQUIER tarea compleja:

1. **Crear `task_plan.md`** en tu proyecto — Usar [templates/task_plan.md](templates/task_plan.md) como referencia
2. **Crear `findings.md`** en tu proyecto — Usar [templates/findings.md](templates/findings.md) como referencia
3. **Crear `progress.md`** en tu proyecto — Usar [templates/progress.md](templates/progress.md) como referencia
4. **Re-leer plan antes de decisiones** — Refresca objetivos en ventana de atención
5. **Actualizar después de cada fase** — Marcar completo, registrar errores

> **Nota:** Los tres archivos de planificación deben crearse en tu directorio de trabajo actual (raíz de tu proyecto), no en la carpeta de instalación de la skill.

## El Patrón Central

```
Ventana de Contexto = RAM (volátil, limitada)
Sistema de Archivos = Disco (persistente, ilimitado)

→ Cualquier cosa importante se escribe en disco.
```

## Propósitos de Archivos

| Archivo | Propósito | Cuándo Actualizar |
|---------|-----------|-------------------|
| `task_plan.md` | Fases, progreso, decisiones | Después de cada fase |
| `findings.md` | Investigación, descubrimientos | Después de CUALQUIER descubrimiento |
| `progress.md` | Registro de sesión, resultados de pruebas | A lo largo de la sesión |

## Reglas Críticas

### 1. Crear Plan Primero
Nunca iniciar una tarea compleja sin `task_plan.md`. No negociable.

### 2. La Regla de 2 Acciones
> "Después de cada 2 operaciones de ver/navegador/búsqueda, INMEDIATAMENTE guardar hallazgos clave en archivos de texto."

Esto previene que se pierda información visual/multimodal.

### 3. Leer Antes de Decidir
Antes de decisiones importantes, leer el archivo de plan. Esto mantiene objetivos en tu ventana de atención.

### 4. Actualizar Después de Actuar
Después de completar cualquier fase:
- Marcar estado de fase: `in_progress` → `complete`
- Registrar cualquier error encontrado
- Notar archivos creados/modificados

### 5. Registrar TODOS los Errores
Cada error va en el archivo de plan. Esto construye conocimiento y previene repetición.

```markdown
## Errores Encontrados
| Error | Intento | Resolución |
|-------|---------|------------|
| FileNotFoundError | 1 | Creado config por defecto |
| API timeout | 2 | Agregada lógica de reintento |
```

### 6. Nunca Repetir Fallos
```
if action_failed:
    next_action != same_action
```
Rastrear lo que intentaste. Mutar el enfoque.

## El Protocolo de Error de 3 Intentos

```
INTENTO 1: Diagnosticar y Arreglar
  → Leer error cuidadosamente
  → Identificar causa raíz
  → Aplicar corrección dirigida

INTENTO 2: Enfoque Alternativo
  → ¿Mismo error? Probar método diferente
  → ¿Herramienta diferente? ¿Biblioteca diferente?
  → NUNCA repetir exactamente la misma acción que falló

INTENTO 3: Reconsideración Más Amplia
  → Cuestionar suposiciones
  → Buscar soluciones
  → Considerar actualizar el plan

DESPUÉS DE 3 FALLOS: Escalar al Usuario
  → Explicar lo que intentaste
  → Compartir el error específico
  → Pedir guía
```

## Matriz de Decisión Leer vs Escribir

| Situación | Acción | Razón |
|-----------|--------|-------|
| Acabas de escribir un archivo | NO leer | Contenido aún en contexto |
| Viste imagen/PDF | Escribir hallazgos AHORA | Multimodal → texto antes de perder |
| Navegador devolvió datos | Escribir a archivo | Las capturas de pantalla no persisten |
| Iniciando nueva fase | Leer plan/hallazgos | Re-orientar si contexto está obsoleto |
| Ocurrió error | Leer archivo relevante | Necesitar estado actual para arreglar |
| Reanudando después de pausa | Leer todos los archivos de planificación | Recuperar estado |

## La Prueba de Reinicio de 5 Preguntas

Si puedes responder estas, tu gestión de contexto es sólida:

| Pregunta | Fuente de Respuesta |
|----------|---------------------|
| ¿Dónde estoy? | Fase actual en task_plan.md |
| ¿A dónde voy? | Fases restantes |
| ¿Cuál es el objetivo? | Declaración de objetivo en plan |
| ¿Qué he aprendido? | findings.md |
| ¿Qué he hecho? | progress.md |

## Cuándo Usar Este Patrón

**Usar para:**
- Tareas de múltiples pasos (3+ pasos)
- Tareas de investigación
- Construir/crear proyectos
- Tareas que abarcan muchas llamadas a herramientas
- Cualquier cosa que requiera organización

**Omitir para:**
- Preguntas simples
- Ediciones de archivo único
- Búsquedas rápidas

## Plantillas

Copiar estas plantillas para comenzar:

- [templates/task_plan.md](templates/task_plan.md) — Seguimiento de fases
- [templates/findings.md](templates/findings.md) — Almacenamiento de investigación
- [templates/progress.md](templates/progress.md) — Registro de sesión

## Scripts

Scripts auxiliares para automatización:

- `scripts/init-session.sh` — Inicializar todos los archivos de planificación
- `scripts/check-complete.sh` — Verificar que todas las fases estén completas

## Temas Avanzados

- **Principios de Manus:** Ver [reference.md](reference.md)
- **Ejemplos Reales:** Ver [examples.md](examples.md)

## Ejemplos de Uso

### Ejemplo 1: Planificar un Proyecto Complejo de Investigación
**Situación**: Necesitas investigar y comparar diferentes opciones de base de datos para tu proyecto, pero hay mucha información y quieres mantenerla organizada.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero planificar una investigación sobre qué base de datos usar para mi proyecto"
2. Cursor usará esta skill para:
   - Crear `task_plan.md` con fases de investigación
   - Crear `findings.md` para guardar todo lo que descubras
   - Crear `progress.md` para registrar tu progreso
   - Después de cada 2 búsquedas o lecturas, guardar automáticamente los hallazgos en `findings.md`
   - Mantener el plan actualizado con decisiones tomadas

**Resultado**: Toda tu investigación organizada en archivos que puedes consultar después, sin perder información importante.

### Ejemplo 2: Construir una Aplicación Completa con Múltiples Fases
**Situación**: Quieres construir una aplicación completa pero es un proyecto grande con muchas partes.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero construir una app completa, necesito planificar todas las fases"
2. Cursor creará:
   - Un `task_plan.md` con todas las fases del proyecto
   - Un sistema para actualizar el progreso después de cada fase
   - Archivos que mantienen el estado incluso si la conversación se interrumpe
   - Capacidad de reanudar exactamente donde te quedaste

**Resultado**: Un proyecto bien organizado donde siempre sabes dónde estás y qué falta por hacer, incluso después de pausar y reanudar.

### Ejemplo 3: Depurar un Problema Complejo con Múltiples Intentos
**Situación**: Tienes un bug difícil que requiere múltiples intentos y quieres rastrear qué has probado.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo un bug complejo, quiero rastrear todos mis intentos de solución"
2. Cursor implementará:
   - Un plan que registra cada intento de solución
   - Un sistema que previene repetir el mismo error
   - Registro de todos los errores encontrados
   - Un protocolo de 3 intentos antes de pedir ayuda

**Resultado**: Un proceso sistemático para resolver problemas complejos sin dar vueltas en círculos probando lo mismo repetidamente.
