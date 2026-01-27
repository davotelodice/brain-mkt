---
name: parallel-agents
description: Patrones de orquestación multi-agente. Usar cuando múltiples tareas independientes pueden ejecutarse con diferente expertise de dominio o cuando análisis comprehensivo requiere múltiples perspectivas.
allowed-tools: Read, Glob, Grep
---

# Agentes Paralelos Nativos

> Orquestación a través de la herramienta Agent nativa de Claude Code

## Resumen

Esta skill permite coordinar múltiples agentes especializados a través del sistema de agentes nativo de Claude Code. A diferencia de scripts externos, este enfoque mantiene toda la orquestación bajo control de Claude.

## Cuándo Usar Orquestación

✅ **Bueno para:**
- Tareas complejas requiriendo múltiples dominios de expertise
- Análisis de código desde perspectivas de seguridad, rendimiento y calidad
- Revisiones comprehensivas (arquitectura + seguridad + testing)
- Implementación de características necesitando trabajo backend + frontend + base de datos

❌ **No para:**
- Tareas simples, de dominio único
- Correcciones rápidas o cambios pequeños
- Tareas donde un agente basta

---

## Invocación de Agente Nativo

### Agente Único
```
Usar el agente security-auditor para revisar autenticación
```

### Cadena Secuencial
```
Primero, usar explorer-agent para descubrir estructura del proyecto.
Luego, usar backend-specialist para revisar endpoints API.
Finalmente, usar test-engineer para identificar gaps de tests.
```

### Con Paso de Contexto
```
Usar frontend-specialist para analizar componentes React.
Basado en esos hallazgos, hacer que test-engineer genere tests de componentes.
```

---

## Patrones de Orquestación

### Patrón 1: Análisis Comprehensivo
```
Agentes: explorer-agent → [domain-agents] → síntesis

1. explorer-agent: Mapear estructura del codebase
2. security-auditor: Postura de seguridad
3. backend-specialist: Calidad de API
4. frontend-specialist: Patrones UI/UX
5. test-engineer: Cobertura de tests
6. Sintetizar todos los hallazgos
```

### Patrón 2: Revisión de Característica
```
Agentes: affected-domain-agents → test-engineer

1. Identificar dominios afectados (backend? frontend? ambos?)
2. Invocar agentes de dominio relevantes
3. test-engineer verifica cambios
4. Sintetizar recomendaciones
```

---

## Agentes Disponibles

| Agente | Expertise | Frases de Activación |
|--------|-----------|---------------------|
| `security-auditor` | Seguridad | "security", "auth", "vulnerabilities" |
| `backend-specialist` | Backend | "API", "server", "Node.js", "Express" |
| `frontend-specialist` | Frontend | "React", "UI", "components", "Next.js" |
| `test-engineer` | Testing | "tests", "coverage", "TDD" |
| `explorer-agent` | Descubrimiento | "explore", "map", "structure" |

---

## Protocolo de Síntesis

Después de que todos los agentes completen, sintetizar:

```markdown
## Síntesis de Orquestación

### Resumen de Tarea
[Qué se logró]

### Contribuciones de Agentes
| Agente | Hallazgo |
|--------|----------|
| security-auditor | Encontró X |
| backend-specialist | Identificó Y |

### Recomendaciones Consolidadas
1. **Crítico**: [Issue del Agente A]
2. **Importante**: [Issue del Agente B]
```

## Ejemplos de Uso

### Ejemplo 1: Análisis Comprehensivo de tu Código
**Situación**: Quieres una revisión completa de tu código desde múltiples perspectivas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero un análisis comprehensivo de mi código"
2. Cursor usará esta skill para:
   - Despachar múltiples agentes especializados (seguridad, backend, frontend, tests)
   - Dejarlos trabajar en paralelo o secuencialmente según necesidad
   - Sintetizar todos los hallazgos en un reporte unificado
   - Darte recomendaciones priorizadas

**Resultado**: Análisis completo desde múltiples perspectivas que identifica todos los problemas y mejoras.

### Ejemplo 2: Implementar una Característica Compleja
**Situación**: Necesitas implementar una característica que requiere trabajo en backend, frontend y base de datos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar una característica que requiere múltiples agentes"
2. Cursor:
   - Identificará qué agentes necesitas (backend-specialist, frontend-specialist, database-architect)
   - Los orquestará en el orden correcto
   - Coordinará el trabajo entre ellos
   - Te dará un resultado integrado

**Resultado**: Característica implementada completamente con trabajo coordinado de múltiples agentes especializados.

### Ejemplo 3: Revisión de Seguridad y Calidad
**Situación**: Quieres una revisión de seguridad y calidad de código simultáneamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero una revisión de seguridad y calidad en paralelo"
2. Cursor:
   - Despachará security-auditor y test-engineer en paralelo
   - Cada uno revisará desde su perspectiva
   - Sintetizará hallazgos de ambos
   - Te dará recomendaciones priorizadas

**Resultado**: Revisión completa de seguridad y calidad que identifica problemas desde ambas perspectivas.
