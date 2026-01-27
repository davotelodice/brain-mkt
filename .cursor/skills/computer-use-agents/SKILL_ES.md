---
name: computer-use-agents
description: "Construir agentes IA que interactúan con computadoras como humanos - viendo pantallas, moviendo cursores, haciendo clic en botones y escribiendo texto. Cubre Computer Use de Anthropic, Operator/CUA de OpenAI y alternativas open-source. Enfoque crítico en sandboxing, seguridad y manejo de desafíos únicos de control basado en visión. Usar cuando: computer use, agente de automatización de escritorio, IA de control de pantalla, agente basado en visión, automatización GUI."
source: vibeship-spawner-skills (Apache 2.0)
---

# Agentes de Uso de Computadora

## Patrones

### Loop Percepción-Razonamiento-Acción

La arquitectura fundamental de agentes de uso de computadora: observar pantalla,
razonar sobre siguiente acción, ejecutar acción, repetir. Este loop integra
modelos de visión con ejecución de acciones a través de un pipeline iterativo.

Componentes clave:
1. PERCEPCIÓN: Screenshot captura estado actual de pantalla
2. RAZONAMIENTO: Modelo visión-lenguaje analiza y planifica
3. ACCIÓN: Ejecutar operaciones mouse/teclado
4. RETROALIMENTACIÓN: Observar resultado, continuar o corregir

Insight crítico: Los agentes de visión están completamente quietos durante fase
de "pensamiento" (1-5 segundos), creando un patrón de pausa detectable.

### Patrón de Entorno Sandboxed

Los agentes de uso de computadora DEBEN ejecutarse en entornos aislados y sandboxed.
Nunca dar a agentes acceso directo a tu sistema principal - los riesgos de seguridad
son demasiado altos. Usar contenedores Docker con escritorios virtuales.

Requisitos clave de aislamiento:
1. RED: Restringir solo a endpoints necesarios
2. FILESYSTEM: Solo lectura o limitado a directorios temp
3. CREDENCIALES: Sin acceso a credenciales del host
4. SYSCALLS: Filtrar system calls peligrosos
5. RECURSOS: Limitar CPU, memoria, tiempo

El objetivo es "minimización de radio de explosión" - si el agente va mal,
el daño está contenido al sandbox.

## Ejemplos de Uso

### Ejemplo 1: Construir un Agente que Controla tu Computadora
**Situación**: Quieres crear un agente que pueda interactuar con tu computadora visualmente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero construir un agente que pueda controlar mi computadora"
2. Cursor usará esta skill para:
   - Implementar el loop percepción-razonamiento-acción
   - Configurar captura de screenshots
   - Integrar modelos de visión para entender la pantalla
   - Implementar ejecución de acciones (click, type, etc.)
   - Configurar sandboxing apropiado para seguridad

**Resultado**: Un agente que puede ver y controlar tu computadora de forma segura.

### Ejemplo 2: Configurar Sandboxing para Agentes de Uso de Computadora
**Situación**: Quieres ejecutar un agente de uso de computadora pero necesitas asegurarte de que sea seguro.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar sandboxing para mi agente de uso de computadora"
2. Cursor:
   - Configurará un entorno Docker aislado
   - Restringirá acceso a red y filesystem
   - Limitará recursos (CPU, memoria)
   - Filtrará system calls peligrosos
   - Asegurará que el agente no pueda dañar tu sistema

**Resultado**: Un entorno sandboxed seguro donde puedes ejecutar agentes de uso de computadora sin riesgos.

### Ejemplo 3: Integrar Modelos de Visión con Control de Computadora
**Situación**: Quieres que tu agente use visión para entender la pantalla y luego actuar.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero integrar modelos de visión con control de computadora"
2. Cursor:
   - Configurará captura de screenshots
   - Integrará modelos de visión (Computer Use, Operator, etc.)
   - Implementará el loop percepción-razonamiento-acción
   - Agregará manejo de retroalimentación
   - Optimizará para latencia baja

**Resultado**: Un agente que puede ver la pantalla, entenderla y actuar basado en lo que ve.
