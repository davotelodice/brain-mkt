---
name: agent-memory-mcp
author: Amit Rathiesh
description: Un sistema de memoria híbrido que proporciona gestión de conocimiento persistente y buscable para agentes IA (Arquitectura, Patrones, Decisiones).
---

# Skill de Memoria de Agente

Esta skill proporciona un banco de memoria persistente y buscable que se sincroniza automáticamente con documentación del proyecto. Se ejecuta como un servidor MCP para permitir lectura/escritura/búsqueda de memorias a largo plazo.

## Prerrequisitos

- Node.js (v18+)

## Configuración

1. **Clonar el Repositorio**:
   Clonar el proyecto `agentMemory` en el workspace de tu agente o un directorio paralelo:

   ```bash
   git clone https://github.com/webzler/agentMemory.git .agent/skills/agent-memory
   ```

2. **Instalar Dependencias**:

   ```bash
   cd .agent/skills/agent-memory
   npm install
   npm run compile
   ```

3. **Iniciar el Servidor MCP**:
   Usar el script helper para activar el banco de memoria para tu proyecto actual:

   ```bash
   npm run start-server <project_id> <absolute_path_to_target_workspace>
   ```

   _Ejemplo para directorio actual:_

   ```bash
   npm run start-server my-project $(pwd)
   ```

## Capacidades (Herramientas MCP)

### `memory_search`

Buscar memorias por query, tipo o tags.

- **Args**: `query` (string), `type?` (string), `tags?` (string[])
- **Uso**: "Encontrar todos los patrones de autenticación" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`

Registrar nuevo conocimiento o decisiones.

- **Args**: `key` (string), `type` (string), `content` (string), `tags?` (string[])
- **Uso**: "Guardar esta decisión de arquitectura" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`

Recuperar contenido de memoria específica por clave.

- **Args**: `key` (string)
- **Uso**: "Obtener el diseño de auth" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`

Ver analytics sobre uso de memoria.

- **Uso**: "Mostrar estadísticas de memoria" -> `memory_stats({})`

## Dashboard

Esta skill incluye un dashboard independiente para visualizar uso de memoria.

```bash
npm run start-dashboard <absolute_path_to_target_workspace>
```

Acceder en: `http://localhost:3333`

## Ejemplos de Uso

### Ejemplo 1: Configurar Memoria Persistente para tu Agente
**Situación**: Quieres que tu agente recuerde información entre sesiones.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar memoria persistente para mi agente"
2. Cursor usará esta skill para:
   - Clonar e instalar el servidor MCP de memoria
   - Configurar el banco de memoria para tu proyecto
   - Sincronizar con documentación del proyecto
   - Habilitar lectura/escritura/búsqueda de memorias

**Resultado**: Un sistema de memoria persistente que tu agente puede usar para recordar información importante.

### Ejemplo 2: Guardar y Buscar Decisiones de Arquitectura
**Situación**: Quieres guardar decisiones de arquitectura y poder buscarlas después.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero guardar esta decisión de arquitectura y poder buscarla después"
2. Cursor:
   - Usará memory_write para guardar la decisión
   - La etiquetará apropiadamente (tipo: "decision", tags relevantes)
   - Te permitirá buscarla después usando memory_search
   - La mantendrá sincronizada con tu documentación

**Resultado**: Decisiones de arquitectura guardadas y fácilmente buscables cuando las necesites.

### Ejemplo 3: Buscar Patrones y Conocimiento Guardado
**Situación**: Quieres buscar patrones o conocimiento que guardaste anteriormente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero buscar patrones de autenticación que guardé antes"
2. Cursor:
   - Usará memory_search con query apropiada
   - Filtrará por tipo y tags si es necesario
   - Te mostrará todas las memorias relevantes
   - Te permitirá leer contenido completo con memory_read

**Resultado**: Búsqueda rápida y efectiva de conocimiento guardado previamente.
