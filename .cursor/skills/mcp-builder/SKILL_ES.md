---
name: mcp-builder
description: Guía para crear servidores MCP (Model Context Protocol) de alta calidad que permiten a LLMs interactuar con servicios externos a través de herramientas bien diseñadas. Usar al construir servidores MCP para integrar APIs o servicios externos, ya sea en Python (FastMCP) o Node/TypeScript (MCP SDK).
license: Términos completos en LICENSE.txt
---

# Guía de Desarrollo de Servidor MCP

## Resumen

Crear servidores MCP (Model Context Protocol) que permiten a LLMs interactuar con servicios externos a través de herramientas bien diseñadas. La calidad de un servidor MCP se mide por qué tan bien permite a LLMs lograr tareas del mundo real.

---

# Proceso

## 🚀 Flujo de Trabajo de Alto Nivel

Crear un servidor MCP de alta calidad involucra cuatro fases principales:

### Fase 1: Investigación Profunda y Planificación

#### 1.1 Entender Diseño MCP Moderno

**Cobertura de API vs. Herramientas de Workflow:**
Balancear cobertura comprehensiva de endpoints API con herramientas de workflow especializadas. Las herramientas de workflow pueden ser más convenientes para tareas específicas, mientras que cobertura comprehensiva da a agentes flexibilidad para componer operaciones.

**Nomenclatura y Descubribilidad de Herramientas:**
Nombres de herramientas claros y descriptivos ayudan a agentes a encontrar las herramientas correctas rápidamente. Usar prefijos consistentes (ej., `github_create_issue`, `github_list_repos`) y nomenclatura orientada a acción.

**Gestión de Contexto:**
Los agentes se benefician de descripciones de herramientas concisas y la capacidad de filtrar/paginar resultados. Diseñar herramientas que retornen datos enfocados y relevantes.

**Mensajes de Error Accionables:**
Los mensajes de error deben guiar a agentes hacia soluciones con sugerencias específicas y próximos pasos.

#### 1.2 Estudiar Documentación del Protocolo MCP

**Navegar la especificación MCP:**

Comenzar con el sitemap para encontrar páginas relevantes: `https://modelcontextprotocol.io/sitemap.xml`

Luego obtener páginas específicas con sufijo `.md` para formato markdown (ej., `https://modelcontextprotocol.io/specification/draft.md`).

Páginas clave a revisar:
- Resumen de especificación y arquitectura
- Mecanismos de transporte (HTTP streamable, stdio)
- Definiciones de herramientas, recursos y prompts

#### 1.3 Estudiar Documentación del Framework

**Stack recomendado:**
- **Lenguaje**: TypeScript (soporte SDK de alta calidad y buena compatibilidad)
- **Transporte**: HTTP streamable para servidores remotos, stdio para servidores locales

#### 1.4 Planificar tu Implementación

**Entender la API:**
Revisar documentación de API del servicio para identificar endpoints clave, requisitos de autenticación y modelos de datos.

**Selección de Herramientas:**
Priorizar cobertura comprehensiva de API. Listar endpoints a implementar, comenzando con operaciones más comunes.

---

### Fase 2: Implementación

#### 2.1 Configurar Estructura del Proyecto

Ver guías específicas de lenguaje para configuración de proyecto.

#### 2.2 Implementar Infraestructura Central

Crear utilidades compartidas:
- Cliente API con autenticación
- Helpers de manejo de errores
- Formateo de respuestas (JSON/Markdown)
- Soporte de paginación

#### 2.3 Implementar Herramientas

Para cada herramienta:

**Schema de Entrada:**
- Usar Zod (TypeScript) o Pydantic (Python)
- Incluir restricciones y descripciones claras
- Agregar ejemplos en descripciones de campos

**Schema de Salida:**
- Definir `outputSchema` donde sea posible para datos estructurados
- Usar `structuredContent` en respuestas de herramientas
- Ayuda a clientes a entender y procesar salidas de herramientas

**Descripción de Herramienta:**
- Resumen conciso de funcionalidad
- Descripciones de parámetros
- Schema de tipo de retorno

**Implementación:**
- Async/await para operaciones I/O
- Manejo apropiado de errores con mensajes accionables
- Soporte de paginación donde sea aplicable
- Retornar tanto contenido de texto como datos estructurados

**Anotaciones:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Fase 3: Revisar y Probar

#### 3.1 Calidad de Código

Revisar para:
- Sin código duplicado (principio DRY)
- Manejo de errores consistente
- Cobertura de tipos completa
- Descripciones de herramientas claras

#### 3.2 Construir y Probar

**TypeScript:**
- Ejecutar `npm run build` para verificar compilación
- Probar con MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Verificar sintaxis: `python -m py_compile your_server.py`
- Probar con MCP Inspector

---

### Fase 4: Crear Evaluaciones

Después de implementar tu servidor MCP, crear evaluaciones comprehensivas para probar su efectividad.

#### 4.1 Entender Propósito de Evaluación

Usar evaluaciones para probar si LLMs pueden usar efectivamente tu servidor MCP para responder preguntas realistas y complejas.

#### 4.2 Crear 10 Preguntas de Evaluación

Para crear evaluaciones efectivas:
1. **Inspección de Herramientas**: Listar herramientas disponibles y entender sus capacidades
2. **Exploración de Contenido**: Usar operaciones READ-ONLY para explorar datos disponibles
3. **Generación de Preguntas**: Crear 10 preguntas complejas y realistas
4. **Verificación de Respuestas**: Resolver cada pregunta tú mismo para verificar respuestas

#### 4.3 Requisitos de Evaluación

Asegurar que cada pregunta es:
- **Independiente**: No dependiente de otras preguntas
- **Read-only**: Solo operaciones no destructivas requeridas
- **Compleja**: Requiriendo múltiples llamadas de herramientas y exploración profunda
- **Realista**: Basada en casos de uso reales que a humanos les importarían
- **Verificable**: Respuesta única y clara que puede verificarse por comparación de strings
- **Estable**: La respuesta no cambiará con el tiempo

---

## Archivos de Referencia

### 📚 Biblioteca de Documentación

Cargar estos recursos según se necesiten durante desarrollo:

### Documentación MCP Central (Cargar Primero)
- **Protocolo MCP**: Comenzar con sitemap en `https://modelcontextprotocol.io/sitemap.xml`
- **Mejores Prácticas MCP**: Guías universales incluyendo nomenclatura, formato de respuestas, paginación, transporte, seguridad

### Documentación SDK (Cargar Durante Fase 1/2)
- **Python SDK**: Obtener desde repositorio oficial
- **TypeScript SDK**: Obtener desde repositorio oficial

### Guías de Implementación Específicas de Lenguaje (Cargar Durante Fase 2)
- **Guía Python**: Patrones de inicialización, ejemplos Pydantic, registro de herramientas
- **Guía TypeScript**: Estructura de proyecto, patrones Zod, registro de herramientas

### Guía de Evaluación (Cargar Durante Fase 4)
- **Guía de Evaluación**: Guía completa de creación de evaluaciones con especificaciones de formato XML

## Ejemplos de Uso

### Ejemplo 1: Crear un Servidor MCP desde Cero
**Situación**: Quieres crear un servidor MCP para integrar un servicio externo con tu agente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un servidor MCP para integrar [servicio]"
2. Cursor usará esta skill para:
   - Investigar el protocolo MCP y mejores prácticas
   - Planificar qué herramientas implementar
   - Configurar estructura del proyecto
   - Implementar herramientas con schemas apropiados
   - Probar con MCP Inspector
   - Crear evaluaciones

**Resultado**: Un servidor MCP de alta calidad que permite a tu agente interactuar con el servicio externo.

### Ejemplo 2: Agregar Nuevas Herramientas a tu Servidor MCP
**Situación**: Ya tienes un servidor MCP y quieres agregar más herramientas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero agregar nuevas herramientas a mi servidor MCP"
2. Cursor:
   - Te guiará en diseño de herramientas apropiado
   - Creará schemas de entrada y salida claros
   - Implementará manejo de errores accionable
   - Agregará anotaciones apropiadas (readOnly, destructive, etc.)
   - Seguirá mejores prácticas de MCP

**Resultado**: Nuevas herramientas bien diseñadas que se integran perfectamente con tu servidor MCP existente.

### Ejemplo 3: Mejorar Calidad de tu Servidor MCP
**Situación**: Tienes un servidor MCP pero quieres mejorarlo para que sea de mayor calidad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero mejorar la calidad de mi servidor MCP"
2. Cursor:
   - Revisará tu código para problemas de calidad
   - Mejorará descripciones de herramientas
   - Optimizará schemas de entrada/salida
   - Agregará manejo de errores mejorado
   - Creará evaluaciones para probar efectividad

**Resultado**: Un servidor MCP mejorado que es más efectivo y fácil de usar para agentes.
