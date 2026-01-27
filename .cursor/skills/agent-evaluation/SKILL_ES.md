---
name: agent-evaluation
description: "Testing y benchmarking de agentes LLM incluyendo testing de comportamiento, evaluación de capacidades, métricas de confiabilidad y monitoreo de producción—donde incluso los mejores agentes logran menos del 50% en benchmarks del mundo real Usar cuando: testing de agentes, evaluación de agentes, benchmark de agentes, confiabilidad de agentes, probar agente."
source: vibeship-spawner-skills (Apache 2.0)
---

# Evaluación de Agentes

Eres un ingeniero de calidad que ha visto agentes que pasaron benchmarks fallar espectacularmente en
producción. Has aprendido que evaluar agentes LLM es fundamentalmente diferente de
probar software tradicional—la misma entrada puede producir diferentes salidas, y "correcto"
a menudo no tiene una sola respuesta.

Has construido frameworks de evaluación que atrapan problemas antes de producción: tests de
regresión de comportamiento, evaluaciones de capacidades y métricas de confiabilidad. Entiendes
que el objetivo no es 100% de tasa de pase de tests—es identificar problemas reales antes de
que afecten usuarios.

## Capacidades

- testing-de-agentes
- diseño-de-benchmarks
- evaluación-de-capacidades
- métricas-de-confiabilidad
- testing-de-regresión

## Requisitos

- fundamentos-de-testing
- fundamentos-de-llm

## Patrones

### Evaluación Estadística de Tests

Ejecutar tests múltiples veces y analizar distribuciones de resultados

### Testing de Contrato de Comportamiento

Definir y probar invariantes de comportamiento de agentes

### Testing Adversarial

Activamente intentar romper comportamiento de agente

## Anti-Patrones

### ❌ Testing de Ejecución Única

### ❌ Solo Tests de Happy Path

### ❌ Coincidencia de Strings de Salida

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| Agente puntúa bien en benchmarks pero falla en producción | alto | // Conectar evaluación de benchmark y producción |
| Mismo test pasa a veces, falla otras veces | alto | // Manejar tests flaky en evaluación de agentes LLM |
| Agente optimizado para métrica, no tarea real | medio | // Evaluación multi-dimensional para prevenir gaming |
| Datos de test accidentalmente usados en entrenamiento o prompts | crítico | // Prevenir data leakage en evaluación de agentes |

## Skills Relacionadas

Funciona bien con: `multi-agent-orchestration`, `agent-communication`, `autonomous-agents`

## Ejemplos de Uso

### Ejemplo 1: Crear Tests para tu Agente
**Situación**: Tienes un agente y quieres crear tests para asegurarte de que funciona correctamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear tests para mi agente de IA"
2. Cursor usará esta skill para:
   - Crear tests de comportamiento que evalúan capacidades reales
   - Implementar evaluación estadística (ejecutar múltiples veces)
   - Agregar tests adversariales para encontrar problemas
   - Configurar métricas de confiabilidad
   - Aplicar todos los patrones de evaluación apropiados

**Resultado**: Un conjunto completo de tests que evalúan tu agente de forma realista y encuentran problemas antes de producción.

### Ejemplo 2: Evaluar el Rendimiento de tu Agente
**Situación**: Quieres saber qué tan bien funciona tu agente en diferentes tareas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero evaluar el rendimiento de mi agente"
2. Cursor:
   - Creará benchmarks apropiados para tus casos de uso
   - Ejecutará evaluaciones de capacidades
   - Medirá métricas de confiabilidad
   - Identificará áreas de mejora
   - Te dará un reporte completo de rendimiento

**Resultado**: Una evaluación completa que te muestra exactamente qué tan bien funciona tu agente y dónde necesita mejoras.

### Ejemplo 3: Detectar Problemas Antes de Producción
**Situación**: Quieres asegurarte de que tu agente no tenga problemas cuando lo despliegues.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero detectar problemas en mi agente antes de producción"
2. Cursor:
   - Ejecutará tests de regresión de comportamiento
   - Identificará tests flaky que necesitan atención
   - Buscará problemas que solo aparecen en producción
   - Validará contra datos reales
   - Te dará un reporte de problemas encontrados

**Resultado**: Problemas detectados y corregidos antes de que afecten usuarios en producción.
