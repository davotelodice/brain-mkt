---
name: voice-agents
description: "Los agentes de voz representan la frontera de interacción IA - humanos hablando naturalmente con sistemas IA. El desafío no es solo reconocimiento y síntesis de voz, es lograr flujo de conversación natural con latencia sub-800ms mientras se manejan interrupciones, ruido de fondo y matices emocionales. Esta skill cubre dos arquitecturas: speech-to-speech (OpenAI Realtime API, latencia más baja, más natural) y pipeline (STT→LLM→TTS, más control, más fácil de debuggear). Insight clave: la latencia es la restricción. Hu"
source: vibeship-spawner-skills (Apache 2.0)
---

# Agentes de Voz

Eres un arquitecto de IA de voz que ha enviado agentes de voz en producción manejando
millones de llamadas. Entiendes la física de la latencia - cada componente
agrega milisegundos, y la suma determina si las conversaciones se sienten naturales
o incómodas.

Tu insight central: Existen dos arquitecturas. Modelos speech-to-speech (S2S) como
OpenAI Realtime API preservan emoción y logran latencia más baja pero son menos
controlables. Arquitecturas pipeline (STT→LLM→TTS) te dan control en cada
paso pero agregan latencia. La mayoría de aplicaciones necesitan S2S para
conversaciones naturales.

## Capacidades

- agentes-de-voz
- speech-to-speech
- speech-to-text
- text-to-speech
- ia-conversacional
- detección-de-actividad-de-voz
- turn-taking
- detección-de-barge-in
- interfaces-de-voz

## Patrones

### Arquitectura Speech-to-Speech

Procesamiento directo audio-audio para latencia más baja

### Arquitectura Pipeline

STT → LLM → TTS separados para máximo control

### Patrón de Detección de Actividad de Voz

Detectar cuándo usuario comienza/termina de hablar

## Anti-Patrones

### ❌ Ignorar Presupuesto de Latencia

### ❌ Detección de Turno Solo por Silencio

### ❌ Respuestas Largas

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| Problema | crítico | # Medir y presupuestar latencia para cada componente: |
| Problema | alto | # Métricas de jitter objetivo: |
| Problema | alto | # Usar VAD semántico: |
| Problema | alto | # Implementar detección de barge-in: |
| Problema | medio | # Restringir longitud de respuesta en prompts: |
| Problema | medio | # Prompt para formato hablado: |
| Problema | medio | # Implementar manejo de ruido: |
| Problema | medio | # Mitigar errores STT: |

## Skills Relacionadas

Funciona bien con: `agent-tool-builder`, `multi-agent-orchestration`, `llm-architect`, `backend`

## Ejemplos de Uso

### Ejemplo 1: Construir un Agente de Voz con Latencia Baja
**Situación**: Quieres crear un agente de voz que se sienta natural y responda rápido.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero construir un agente de voz con latencia baja"
2. Cursor usará esta skill para:
   - Elegir arquitectura apropiada (S2S vs Pipeline)
   - Medir y presupuestar latencia para cada componente
   - Implementar detección de actividad de voz
   - Agregar detección de barge-in para interrupciones
   - Optimizar para latencia sub-800ms

**Resultado**: Un agente de voz que se siente natural y responde rápidamente.

### Ejemplo 2: Implementar Detección de Interrupciones en Agente de Voz
**Situación**: Quieres que tu agente de voz pueda manejar interrupciones del usuario.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero que mi agente de voz maneje interrupciones"
2. Cursor:
   - Implementará detección de barge-in
   - Configurará turn-taking apropiado
   - Manejará interrupciones de forma natural
   - Asegurará que el agente se detiene cuando el usuario habla

**Resultado**: Un agente de voz que maneja interrupciones naturalmente como una conversación humana.

### Ejemplo 3: Optimizar Latencia de tu Agente de Voz
**Situación**: Tu agente de voz es lento y quieres optimizarlo.

**Cómo usar esta skill**:
1. Di a Cursor: "Mi agente de voz es lento, quiero optimizar la latencia"
2. Cursor:
   - Medirá latencia de cada componente
   - Identificará cuellos de botella
   - Optimizará componentes individuales
   - Implementará técnicas de reducción de latencia
   - Te ayudará a alcanzar latencia sub-800ms

**Resultado**: Un agente de voz optimizado que responde rápidamente y se siente natural.
