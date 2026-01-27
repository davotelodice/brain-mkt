---
name: dispatching-parallel-agents
description: Usar cuando enfrentas 2+ tareas independientes que pueden trabajarse sin estado compartido o dependencias secuenciales
---

# Despachar Agentes Paralelos

## Resumen

Cuando tienes múltiples fallos no relacionados (diferentes archivos de test, diferentes subsistemas, diferentes bugs), investigarlos secuencialmente desperdicia tiempo. Cada investigación es independiente y puede suceder en paralelo.

**Principio central:** Despachar un agente por dominio de problema independiente. Dejarlos trabajar concurrentemente.

## Cuándo Usar

**Usar cuando:**
- 3+ archivos de test fallando con diferentes causas raíz
- Múltiples subsistemas rotos independientemente
- Cada problema puede entenderse sin contexto de otros
- Sin estado compartido entre investigaciones

**No usar cuando:**
- Los fallos están relacionados (arreglar uno podría arreglar otros)
- Necesitas entender estado completo del sistema
- Los agentes interferirían entre sí

## El Patrón

### 1. Identificar Dominios Independientes

Agrupar fallos por qué está roto:
- Tests de Archivo A: Flujo de aprobación de herramientas
- Tests de Archivo B: Comportamiento de completitud de batch
- Tests de Archivo C: Funcionalidad de abort

Cada dominio es independiente - arreglar aprobación de herramientas no afecta tests de abort.

### 2. Crear Tareas de Agente Enfocadas

Cada agente obtiene:
- **Alcance específico:** Un archivo de test o subsistema
- **Objetivo claro:** Hacer que estos tests pasen
- **Restricciones:** No cambiar otro código
- **Salida esperada:** Resumen de qué encontraste y arreglaste

### 3. Despachar en Paralelo

```typescript
// En Claude Code / entorno IA
Task("Arreglar fallos de agent-tool-abort.test.ts")
Task("Arreglar fallos de batch-completion-behavior.test.ts")
Task("Arreglar fallos de tool-approval-race-conditions.test.ts")
// Los tres ejecutan concurrentemente
```

### 4. Revisar e Integrar

Cuando los agentes retornan:
- Leer cada resumen
- Verificar que las correcciones no conflictan
- Ejecutar suite completa de tests
- Integrar todos los cambios

## Ejemplos de Uso

### Ejemplo 1: Arreglar Múltiples Fallos de Tests en Paralelo
**Situación**: Tienes varios archivos de test fallando y quieres arreglarlos todos rápidamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo múltiples archivos de test fallando, quiero arreglarlos en paralelo"
2. Cursor usará esta skill para:
   - Identificar qué fallos son independientes
   - Despachar un agente para cada dominio de problema
   - Dejar que trabajen en paralelo
   - Integrar todas las correcciones cuando terminen

**Resultado**: Múltiples problemas arreglados en el tiempo de uno, trabajando en paralelo.

### Ejemplo 2: Investigar Múltiples Bugs Independientes
**Situación**: Tienes varios bugs en diferentes partes del sistema que no están relacionados.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo varios bugs independientes, quiero investigarlos en paralelo"
2. Cursor:
   - Identificará qué bugs son independientes
   - Despachará un agente investigador para cada uno
   - Los dejará trabajar simultáneamente
   - Te dará resúmenes de cada investigación

**Resultado**: Múltiples bugs investigados y arreglados en paralelo, ahorrando tiempo significativo.

### Ejemplo 3: Revisar Múltiples Subsistemas Simultáneamente
**Situación**: Quieres revisar varios subsistemas diferentes al mismo tiempo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero revisar múltiples subsistemas en paralelo"
2. Cursor:
   - Identificará subsistemas independientes
   - Despachará un agente revisor para cada uno
   - Los dejará trabajar concurrentemente
   - Te dará reportes consolidados de cada subsistema

**Resultado**: Revisión completa de múltiples subsistemas en paralelo, mucho más rápido que secuencialmente.
