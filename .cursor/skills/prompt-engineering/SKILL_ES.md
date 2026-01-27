---
name: prompt-engineering
description: Guía experta sobre patrones de prompt engineering, mejores prácticas y técnicas de optimización. Usar cuando el usuario quiere mejorar prompts, aprender estrategias de prompting o depurar comportamiento de agente.
---

# Patrones de Prompt Engineering

Técnicas avanzadas de prompt engineering para maximizar rendimiento, confiabilidad y controlabilidad de LLM.

## Capacidades Centrales

### 1. Few-Shot Learning

Enseñar al modelo mostrando ejemplos en lugar de explicar reglas. Incluir 2-5 pares input-output que demuestren el comportamiento deseado. Usar cuando necesitas formateo consistente, patrones de razonamiento específicos o manejo de casos límite.

### 2. Chain-of-Thought Prompting

Solicitar razonamiento paso a paso antes de la respuesta final. Agregar "Pensemos paso a paso" (zero-shot) o incluir trazas de razonamiento de ejemplo (few-shot). Usar para problemas complejos que requieren lógica multi-paso.

### 3. Optimización de Prompts

Mejorar prompts sistemáticamente a través de testing y refinamiento. Comenzar simple, medir rendimiento, luego iterar. Probar en inputs diversos incluyendo casos límite.

### 4. Sistemas de Plantillas

Construir estructuras de prompts reutilizables con variables, secciones condicionales y componentes modulares. Usar para conversaciones multi-turno, interacciones basadas en roles o cuando el mismo patrón aplica a diferentes inputs.

### 5. Diseño de System Prompt

Establecer comportamiento global y constraints que persisten a través de la conversación. Definir rol del modelo, nivel de expertise, formato de salida y guías de seguridad.

## Patrones Clave

### Divulgación Progresiva

Comenzar con prompts simples, agregar complejidad solo cuando se necesite

### Jerarquía de Instrucciones

```
[Contexto del Sistema] → [Instrucción de Tarea] → [Ejemplos] → [Datos de Entrada] → [Formato de Salida]
```

### Recuperación de Errores

Construir prompts que manejen fallos elegantemente:
- Incluir instrucciones de fallback
- Solicitar scores de confianza
- Pedir interpretaciones alternativas cuando incierto
- Especificar cómo indicar información faltante

## Mejores Prácticas

1. **Ser Específico**: Prompts vagos producen resultados inconsistentes
2. **Mostrar, No Decir**: Los ejemplos son más efectivos que descripciones
3. **Probar Extensivamente**: Evaluar en inputs diversos y representativos
4. **Iterar Rápidamente**: Pequeños cambios pueden tener grandes impactos
5. **Monitorear Rendimiento**: Rastrear métricas en producción
6. **Control de Versiones**: Tratar prompts como código con versionado apropiado
7. **Documentar Intención**: Explicar por qué los prompts están estructurados como están

## Errores Comunes

- **Sobre-ingeniería**: Comenzar con prompts complejos antes de probar simples
- **Contaminación de ejemplos**: Usar ejemplos que no coinciden con la tarea objetivo
- **Desbordamiento de contexto**: Exceder límites de tokens con ejemplos excesivos
- **Instrucciones ambiguas**: Dejar espacio para múltiples interpretaciones
- **Ignorar casos límite**: No probar en inputs inusuales o límite

## Ejemplos de Uso

### Ejemplo 1: Mejorar un Prompt que No Funciona Bien
**Situación**: Tienes un prompt que produce resultados inconsistentes.

**Cómo usar esta skill**:
1. Di a Cursor: "Mi prompt no funciona bien, quiero mejorarlo"
2. Cursor usará esta skill para:
   - Analizar el prompt actual
   - Identificar problemas (vaguedad, falta de ejemplos, etc.)
   - Aplicar técnicas de optimización
   - Agregar few-shot learning si es necesario
   - Implementar chain-of-thought si ayuda
   - Probar y refinar

**Resultado**: Prompt mejorado que produce resultados más consistentes y precisos.

### Ejemplo 2: Crear un Prompt con Few-Shot Learning
**Situación**: Quieres que tu LLM aprenda de ejemplos específicos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un prompt con few-shot learning"
2. Cursor:
   - Seleccionará ejemplos apropiados y diversos
   - Formateará ejemplos consistentemente
   - Optimizará número de ejemplos
   - Incluirá casos límite si es necesario
   - Aplicará todas las mejores prácticas

**Resultado**: Prompt con few-shot learning que enseña efectivamente al LLM el comportamiento deseado.

### Ejemplo 3: Optimizar Prompts para Producción
**Situación**: Quieres asegurarte de que tus prompts están optimizados para producción.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero optimizar mis prompts para producción"
2. Cursor:
   - Implementará testing sistemático
   - Optimizará para consistencia
   - Reducirá uso de tokens donde sea posible
   - Agregará manejo de errores
   - Configurará monitoreo de rendimiento

**Resultado**: Prompts optimizados que son consistentes, eficientes y listos para producción.
