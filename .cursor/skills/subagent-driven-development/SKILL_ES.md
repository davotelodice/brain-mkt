---
name: subagent-driven-development
description: Usar al ejecutar planes de implementación con tareas independientes en la sesión actual
---

# Desarrollo Dirigido por Subagentes

Ejecutar plan despachando subagente fresco por tarea, con revisión de dos etapas después de cada una: revisión de cumplimiento de spec primero, luego revisión de calidad de código.

**Principio central:** Subagente fresco por tarea + revisión de dos etapas (spec luego calidad) = alta calidad, iteración rápida

## Cuándo Usar

**vs. Ejecutar Planes (sesión paralela):**
- Misma sesión (sin cambio de contexto)
- Subagente fresco por tarea (sin contaminación de contexto)
- Revisión de dos etapas después de cada tarea: cumplimiento de spec primero, luego calidad de código
- Iteración más rápida (sin human-in-loop entre tareas)

## El Proceso

Por cada tarea:
1. Despachar subagente implementador
2. Subagente implementa, prueba, hace commit, auto-revisa
3. Despachar revisor de spec para confirmar que código coincide con spec
4. Si hay problemas de spec, implementador los arregla
5. Despachar revisor de calidad de código
6. Si hay problemas de calidad, implementador los arregla
7. Marcar tarea completa

Después de todas las tareas:
- Despachar revisor final de código para toda la implementación
- Usar finishing-a-development-branch

## Ventajas

**vs. Ejecución manual:**
- Subagentes siguen TDD naturalmente
- Contexto fresco por tarea (sin confusión)
- Seguro para paralelo (subagentes no interfieren)
- Subagente puede hacer preguntas (antes Y durante trabajo)

**Ganancias de eficiencia:**
- Sin overhead de lectura de archivos (controlador proporciona texto completo)
- Controlador cura exactamente qué contexto se necesita
- Subagente obtiene información completa desde el inicio
- Preguntas surgidas antes de que comience el trabajo (no después)

**Puertas de calidad:**
- Auto-revisión atrapa problemas antes de handoff
- Revisión de dos etapas: cumplimiento de spec, luego calidad de código
- Loops de revisión aseguran que las correcciones realmente funcionan

## Ejemplos de Uso

### Ejemplo 1: Ejecutar un Plan de Implementación con Revisión Automática
**Situación**: Tienes un plan de implementación y quieres ejecutarlo con revisión automática de calidad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero ejecutar este plan usando desarrollo dirigido por subagentes"
2. Cursor usará esta skill para:
   - Despachar un subagente fresco para cada tarea
   - Cada subagente implementa, prueba y auto-revisa
   - Revisión de spec para asegurar cumplimiento
   - Revisión de calidad de código para asegurar código bien construido
   - Iteración hasta que ambas revisiones aprueben

**Resultado**: Plan ejecutado con alta calidad, cada tarea revisada y aprobada antes de continuar.

### Ejemplo 2: Implementar Múltiples Características con Calidad Asegurada
**Situación**: Tienes un plan con múltiples características y quieres asegurar que cada una cumple spec y es de alta calidad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar múltiples características con revisión de dos etapas"
2. Cursor:
   - Ejecutará cada característica con un subagente fresco
   - Revisará cumplimiento de spec primero
   - Luego revisará calidad de código
   - Solo avanzará cuando ambas revisiones aprueben

**Resultado**: Múltiples características implementadas con calidad asegurada, cada una cumpliendo spec y estándares de código.

### Ejemplo 3: Desarrollo Rápido con Puertas de Calidad
**Situación**: Quieres desarrollo rápido pero sin sacrificar calidad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero desarrollo rápido pero con puertas de calidad"
2. Cursor:
   - Ejecutará tareas rápidamente con subagentes frescos
   - Pero mantendrá puertas de calidad estrictas (spec + calidad)
   - Iterará hasta aprobación en ambas
   - Te dará desarrollo rápido pero de alta calidad

**Resultado**: Desarrollo rápido con calidad asegurada, sin comprometer estándares.
