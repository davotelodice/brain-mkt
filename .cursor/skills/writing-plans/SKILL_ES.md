---
name: writing-plans
description: Usar cuando tienes una especificación o requisitos para una tarea de múltiples pasos, antes de tocar código
---

# Escribir Planes

## Resumen

Escribir planes de implementación comprehensivos asumiendo que el ingeniero tiene cero contexto para nuestro codebase y gusto cuestionable. Documentar todo lo que necesitan saber: qué archivos tocar para cada tarea, código, pruebas, docs que podrían necesitar verificar, cómo probarlo. Darles todo el plan como tareas pequeñas. DRY. YAGNI. TDD. Commits frecuentes.

Asumir que son desarrolladores hábiles, pero saben casi nada sobre nuestro conjunto de herramientas o dominio del problema. Asumir que no conocen muy bien el diseño de pruebas.

**Anunciar al inicio:** "Estoy usando la skill writing-plans para crear el plan de implementación."

**Contexto:** Esto debe ejecutarse en un worktree dedicado (creado por la skill brainstorming).

**Guardar planes en:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Granularidad de Tareas Pequeñas

**Cada paso es una acción (2-5 minutos):**
- "Escribir la prueba que falla" - paso
- "Ejecutarla para asegurar que falla" - paso
- "Implementar el código mínimo para que la prueba pase" - paso
- "Ejecutar las pruebas y asegurar que pasan" - paso
- "Hacer commit" - paso

## Encabezado del Documento de Plan

**Cada plan DEBE comenzar con este encabezado:**

```markdown
# [Nombre de Característica] Plan de Implementación

> **Para Claude:** REQUIRED SUB-SKILL: Usar superpowers:executing-plans para implementar este plan tarea por tarea.

**Goal:** [Una oración describiendo qué construye esto]

**Architecture:** [2-3 oraciones sobre el enfoque]

**Tech Stack:** [Tecnologías/bibliotecas clave]

---
```

## Estructura de Tarea

```markdown
### Tarea N: [Nombre de Componente]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Recordar

- Rutas de archivo exactas siempre
- Código completo en el plan (no "agregar validación")
- Comandos exactos con salida esperada
- Referenciar skills relevantes con sintaxis @
- DRY, YAGNI, TDD, commits frecuentes

## Entrega de Ejecución

Después de guardar el plan, ofrecer opción de ejecución:

**"Plan completo y guardado en `docs/plans/<filename>.md`. Dos opciones de ejecución:**

**1. Subagent-Driven (esta sesión)** - Despacho subagente fresco por tarea, revisión entre tareas, iteración rápida

**2. Parallel Session (separada)** - Abrir nueva sesión con executing-plans, ejecución por lotes con puntos de control

**¿Qué enfoque?"**

**Si se elige Subagent-Driven:**
- **REQUIRED SUB-SKILL:** Usar superpowers:subagent-driven-development
- Permanecer en esta sesión
- Subagente fresco por tarea + revisión de código

**Si se elige Parallel Session:**
- Guiarlos a abrir nueva sesión en worktree
- **REQUIRED SUB-SKILL:** Nueva sesión usa superpowers:executing-plans

## Ejemplos de Uso

### Ejemplo 1: Crear un Plan para Agregar Autenticación a tu App
**Situación**: Quieres agregar login y registro a tu aplicación Next.js pero no sabes por dónde empezar.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un plan para agregar autenticación con Supabase a mi app Next.js"
2. Cursor usará esta skill para crear:
   - Un plan detallado con tareas pequeñas (2-5 minutos cada una)
   - Cada tarea con código completo, no solo descripciones vagas
   - Comandos exactos para ejecutar y verificar
   - Rutas de archivo exactas para cada archivo a crear/modificar
   - Un plan guardado en `docs/plans/` listo para ejecutar

**Resultado**: Un plan paso a paso que puedes seguir o que otro agente puede ejecutar, con todo detallado para que no haya ambigüedad.

### Ejemplo 2: Planificar una Refactorización Compleja
**Situación**: Necesitas refactorizar múltiples archivos pero quieres asegurarte de no romper nada.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito un plan para refactorizar mi sistema de autenticación sin romper nada"
2. Cursor creará:
   - Un plan que incluye escribir pruebas primero (TDD)
   - Tareas pequeñas que se pueden verificar independientemente
   - Commits frecuentes después de cada tarea completada
   - Verificación después de cada paso para asegurar que nada se rompió

**Resultado**: Un plan seguro que te permite refactorizar con confianza, sabiendo que cada paso está verificado antes de continuar.

### Ejemplo 3: Planificar un Proyecto Nuevo desde Cero
**Situación**: Quieres crear una nueva aplicación pero necesitas un plan claro de todos los pasos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un plan para construir una app de notas con Next.js, Supabase y TypeScript"
2. Cursor generará:
   - Un plan completo desde la configuración inicial hasta el despliegue
   - Cada paso con código específico y comandos exactos
   - Estructura de archivos clara
   - Orden lógico de implementación (dependencias primero)
   - Criterios de verificación para cada tarea

**Resultado**: Un plan completo que puedes seguir paso a paso para construir tu aplicación, con todo detallado para que no tengas que adivinar nada.
