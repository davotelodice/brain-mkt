---
name: requesting-code-review
description: Usar al completar tareas, implementar características principales o antes de hacer merge para verificar que el trabajo cumple requisitos
---

# Solicitar Revisión de Código

Despachar subagente superpowers:code-reviewer para atrapar problemas antes de que se propaguen.

**Principio central:** Revisar temprano, revisar frecuentemente.

## Cuándo Solicitar Revisión

**Obligatorio:**
- Después de cada tarea en desarrollo dirigido por subagentes
- Después de completar característica principal
- Antes de merge a main

**Opcional pero valioso:**
- Cuando estás atascado (perspectiva fresca)
- Antes de refactorizar (verificación de baseline)
- Después de arreglar bug complejo

## Cómo Solicitar

**1. Obtener SHAs de git:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # o origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Despachar subagente code-reviewer:**

Usar herramienta Task con tipo superpowers:code-reviewer, llenar plantilla en `code-reviewer.md`

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - Lo que acabas de construir
- `{PLAN_OR_REQUIREMENTS}` - Qué debería hacer
- `{BASE_SHA}` - Commit inicial
- `{HEAD_SHA}` - Commit final
- `{DESCRIPTION}` - Resumen breve

**3. Actuar en retroalimentación:**
- Arreglar problemas Críticos inmediatamente
- Arreglar problemas Importantes antes de proceder
- Notar problemas Menores para después
- Hacer push back si el revisor está equivocado (con razonamiento)

## Ejemplo

```
[Acabas de completar Tarea 2: Agregar función de verificación]

Tú: Déjame solicitar revisión de código antes de proceder.

BASE_SHA=$(git log --oneline | grep "Tarea 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Despachar subagente superpowers:code-reviewer]
  WHAT_WAS_IMPLEMENTED: Funciones de verificación y reparación para índice de conversación
  PLAN_OR_REQUIREMENTS: Tarea 2 de docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Agregado verifyIndex() y repairIndex() con 4 tipos de problemas

[Subagente devuelve]:
  Fortalezas: Arquitectura limpia, pruebas reales
  Problemas:
    Importante: Faltan indicadores de progreso
    Menor: Número mágico (100) para intervalo de reporte
  Evaluación: Listo para proceder

Tú: [Arreglar indicadores de progreso]
[Continuar a Tarea 3]
```

## Integración con Flujos de Trabajo

**Desarrollo Dirigido por Subagentes:**
- Revisar después de CADA tarea
- Atrapar problemas antes de que se compongan
- Arreglar antes de mover a siguiente tarea

**Ejecutar Planes:**
- Revisar después de cada lote (3 tareas)
- Obtener retroalimentación, aplicar, continuar

**Desarrollo Ad-Hoc:**
- Revisar antes de merge
- Revisar cuando estás atascado

## Banderas Rojas

**Nunca:**
- Omitir revisión porque "es simple"
- Ignorar problemas Críticos
- Proceder con problemas Importantes sin arreglar
- Discutir con retroalimentación técnica válida

**Si el revisor está equivocado:**
- Hacer push back con razonamiento técnico
- Mostrar código/pruebas que prueban que funciona
- Solicitar aclaración

Ver plantilla en: requesting-code-review/code-reviewer.md

## Ejemplos de Uso

### Ejemplo 1: Solicitar Revisión Después de Completar una Característica
**Situación**: Acabas de implementar una característica importante y quieres que alguien la revise antes de hacer merge.

**Cómo usar esta skill**:
1. Di a Cursor: "Acabo de completar esta característica, quiero solicitar una revisión de código"
2. Cursor usará esta skill para:
   - Obtener los commits relevantes (desde dónde empezaste hasta ahora)
   - Despachar un revisor de código que revisará todo el trabajo
   - Obtener retroalimentación sobre qué está bien y qué necesita mejoras
   - Priorizar problemas (críticos primero, menores después)

**Resultado**: Retroalimentación estructurada que te ayuda a mejorar tu código antes de hacer merge, atrapando problemas temprano.

### Ejemplo 2: Revisar Después de Cada Tarea en un Plan
**Situación**: Estás ejecutando un plan con múltiples tareas y quieres revisar después de cada una.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero revisar después de cada tarea en mi plan"
2. Cursor:
   - Revisará después de completar cada tarea
   - Atrapará problemas antes de que se acumulen
   - Te permitirá arreglar problemas antes de continuar con la siguiente tarea
   - Mantendrá la calidad alta a lo largo del proceso

**Resultado**: Código de alta calidad desde el inicio, con problemas atrapados y arreglados temprano en lugar de acumularse.

### Ejemplo 3: Obtener Perspectiva Fresca Cuando Estás Atascado
**Situación**: Has estado trabajando en algo y estás atascado, necesitas una perspectiva fresca.

**Cómo usar esta skill**:
1. Di a Cursor: "Estoy atascado en este problema, quiero una revisión para obtener perspectiva"
2. Cursor:
   - Solicitará una revisión de tu código actual
   - El revisor puede identificar problemas que no viste
   - Puede sugerir enfoques alternativos
   - Te ayudará a ver el problema desde un ángulo diferente

**Resultado**: Nueva perspectiva que te ayuda a desbloquearte y encontrar soluciones que no habías considerado.
