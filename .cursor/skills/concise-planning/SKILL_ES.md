---
name: concise-planning
description: Usar cuando un usuario pide un plan para una tarea de codificación, para generar una lista de verificación clara, accionable y atómica.
---

# Planificación Concisa

## Objetivo

Convertir una solicitud del usuario en un **plan único y accionable** con pasos atómicos.

## Flujo de Trabajo

### 1. Escanear Contexto

- Leer `README.md`, docs y archivos de código relevantes.
- Identificar restricciones (lenguaje, frameworks, pruebas).

### 2. Interacción Mínima

- Hacer **como máximo 1–2 preguntas** y solo si realmente bloquean.
- Hacer suposiciones razonables para incógnitas no bloqueantes.

### 3. Generar Plan

Usar la siguiente estructura:

- **Approach**: 1-3 oraciones sobre qué y por qué.
- **Scope**: Puntos de viñeta para "In" y "Out".
- **Action Items**: Una lista de 6-10 tareas atómicas y ordenadas (Verbo primero).
- **Validation**: Al menos un elemento para pruebas.

## Plantilla de Plan

```markdown
# Plan

<Enfoque de alto nivel>

## Scope

- In:
- Out:

## Action Items

[ ] <Paso 1: Descubrimiento>
[ ] <Paso 2: Implementación>
[ ] <Paso 3: Implementación>
[ ] <Paso 4: Validación/Pruebas>
[ ] <Paso 5: Lanzamiento/Commit>

## Open Questions

- <Pregunta 1 (máx 3)>
```

## Guías de Lista de Verificación

- **Atómico**: Cada paso debe ser una unidad lógica única de trabajo.
- **Verbo primero**: "Agregar...", "Refactorizar...", "Verificar...".
- **Concreto**: Nombrar archivos o módulos específicos cuando sea posible.

## Ejemplos de Uso

### Ejemplo 1: Crear un Plan Rápido para una Tarea Simple
**Situación**: Quieres agregar un botón a tu página pero necesitas un plan claro y conciso de los pasos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero un plan para agregar un botón de 'Comprar Ahora' a mi página de producto"
2. Cursor usará esta skill para crear:
   - Un plan corto con 6-10 pasos atómicos
   - Cada paso con un verbo claro (Agregar, Estilizar, Probar)
   - Alcance claro de qué está incluido y qué no
   - Una verificación al final para probar que funciona

**Resultado**: Un plan conciso que puedes seguir rápidamente sin sobrecarga de información innecesaria.

### Ejemplo 2: Planificar una Refactorización Rápida
**Situación**: Necesitas refactorizar una función pero quieres un plan simple y directo.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito un plan para refactorizar mi función de cálculo de precios"
2. Cursor generará:
   - Un plan enfocado solo en lo esencial
   - Pasos atómicos que puedes completar uno por uno
   - Verificación incluida para asegurar que no rompiste nada
   - Sin preguntas innecesarias, solo lo que necesitas

**Resultado**: Un plan directo y ejecutable que te lleva de A a B sin rodeos.

### Ejemplo 3: Planificar una Característica Nueva de Forma Concisa
**Situación**: Quieres agregar una nueva característica pero necesitas ver todos los pasos de forma clara y breve.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero un plan para agregar búsqueda a mi aplicación"
2. Cursor creará:
   - Un plan que escanea tu código existente para entender el contexto
   - Pasos específicos basados en tu stack tecnológico
   - Lista de verificación atómica que puedes seguir
   - Validación incluida para probar la característica

**Resultado**: Un plan completo pero conciso que te muestra exactamente qué hacer sin información innecesaria.
