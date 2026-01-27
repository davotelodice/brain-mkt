---
name: skill-developer
description: Crear y gestionar skills de Claude Code siguiendo las mejores prácticas de Anthropic. Usar al crear nuevas skills, modificar skill-rules.json, entender patrones de activación, trabajar con hooks, depurar activación de skills o implementar divulgación progresiva. Cubre estructura de skills, frontmatter YAML, tipos de activadores (keywords, patrones de intención, rutas de archivo, patrones de contenido), niveles de aplicación (block, suggest, warn), mecanismos de hooks (UserPromptSubmit, PreToolUse), seguimiento de sesión y la regla de 500 líneas.
---

# Guía de Desarrollador de Skills

## Propósito

Guía comprehensiva para crear y gestionar skills en Claude Code con sistema de auto-activación, siguiendo las mejores prácticas oficiales de Anthropic incluyendo la regla de 500 líneas y el patrón de divulgación progresiva.

## Cuándo Usar Esta Skill

Se activa automáticamente cuando mencionas:
- Crear o agregar skills
- Modificar activadores o reglas de skills
- Entender cómo funciona la activación de skills
- Depurar problemas de activación de skills
- Trabajar con skill-rules.json
- Mecánica del sistema de hooks
- Mejores prácticas de Claude Code
- Divulgación progresiva
- Frontmatter YAML
- Regla de 500 líneas

---

## Resumen del Sistema

### Arquitectura de Dos Hooks

**1. Hook UserPromptSubmit** (Sugerencias Proactivas)
- **Archivo**: `.claude/hooks/skill-activation-prompt.ts`
- **Activador**: ANTES de que Claude vea el prompt del usuario
- **Propósito**: Sugerir skills relevantes basadas en keywords + patrones de intención
- **Método**: Inyecta recordatorio formateado como contexto (stdout → entrada de Claude)
- **Casos de uso**: Skills basadas en tema, detección de trabajo implícito

**2. Stop Hook - Recordatorio de Manejo de Errores** (Recordatorios Suaves)
- **Archivo**: `.claude/hooks/error-handling-reminder.ts`
- **Activador**: DESPUÉS de que Claude termina de responder
- **Propósito**: Recordatorio suave para auto-evaluar manejo de errores en código escrito
- **Método**: Analiza archivos editados para patrones riesgosos, muestra recordatorio si es necesario
- **Casos de uso**: Conciencia de manejo de errores sin fricción bloqueante

**Cambio de Filosofía (2025-10-27):** Nos alejamos de bloquear PreToolUse para Sentry/manejo de errores. En su lugar, usar recordatorios post-respuesta suaves que no bloquean el flujo de trabajo pero mantienen conciencia de calidad de código.

### Archivo de Configuración

**Ubicación**: `.claude/skills/skill-rules.json`

Define:
- Todas las skills y sus condiciones de activación
- Niveles de aplicación (block, suggest, warn)
- Patrones de ruta de archivo (glob)
- Patrones de detección de contenido (regex)
- Condiciones de omisión (seguimiento de sesión, marcadores de archivo, vars de entorno)

---

## Tipos de Skills

### 1. Skills de Guardrail

**Propósito:** Aplicar mejores prácticas críticas que previenen errores

**Características:**
- Tipo: `"guardrail"`
- Aplicación: `"block"`
- Prioridad: `"critical"` o `"high"`
- Bloquea ediciones de archivo hasta que se use la skill
- Previene errores comunes (nombres de columna, errores críticos)
- Consciente de sesión (no repetir molestia en misma sesión)

**Ejemplos:**
- `database-verification` - Verificar nombres de tabla/columna antes de consultas Prisma
- `frontend-dev-guidelines` - Aplicar patrones React/TypeScript

**Cuándo Usar:**
- Errores que causan errores en tiempo de ejecución
- Preocupaciones de integridad de datos
- Problemas críticos de compatibilidad

### 2. Skills de Dominio

**Propósito:** Proporcionar guía comprehensiva para áreas específicas

**Características:**
- Tipo: `"domain"`
- Aplicación: `"suggest"`
- Prioridad: `"high"` o `"medium"`
- Asesoría, no obligatoria
- Específica de tema o dominio
- Documentación comprehensiva

**Ejemplos:**
- `backend-dev-guidelines` - Patrones Node.js/Express/TypeScript
- `frontend-dev-guidelines` - Mejores prácticas React/TypeScript
- `error-tracking` - Guía de integración Sentry

**Cuándo Usar:**
- Sistemas complejos que requieren conocimiento profundo
- Documentación de mejores prácticas
- Patrones arquitectónicos
- Guías de cómo hacer

---

## Inicio Rápido: Crear una Nueva Skill

### Paso 1: Crear Archivo de Skill

**Ubicación:** `.claude/skills/{skill-name}/SKILL.md`

**Plantilla:**
```markdown
---
name: my-new-skill
description: Descripción breve incluyendo keywords que activan esta skill. Mencionar temas, tipos de archivo y casos de uso. Ser explícito sobre términos de activación.
---

# My New Skill

## Purpose
Con qué ayuda esta skill

## When to Use
Escenarios y condiciones específicas

## Key Information
La guía real, documentación, patrones, ejemplos
```

**Mejores Prácticas:**
- ✅ **Name**: Minúsculas, guiones, forma gerundio (verbo + -ing) preferida
- ✅ **Description**: Incluir TODOS los keywords/frases de activación (máx 1024 caracteres)
- ✅ **Content**: Bajo 500 líneas - usar archivos de referencia para detalles
- ✅ **Examples**: Ejemplos de código real
- ✅ **Structure**: Encabezados claros, listas, bloques de código

### Paso 2: Agregar a skill-rules.json

Ver [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) para esquema completo.

**Plantilla Básica:**
```json
{
  "my-new-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?something"]
    }
  }
}
```

### Paso 3: Probar Activadores

**Probar UserPromptSubmit:**
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Probar PreToolUse:**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

### Paso 4: Refinar Patrones

Basado en pruebas:
- Agregar keywords faltantes
- Refinar patrones de intención para reducir falsos positivos
- Ajustar patrones de ruta de archivo
- Probar patrones de contenido contra archivos reales

### Paso 5: Seguir Mejores Prácticas de Anthropic

✅ Mantener SKILL.md bajo 500 líneas
✅ Usar divulgación progresiva con archivos de referencia
✅ Agregar tabla de contenidos a archivos de referencia > 100 líneas
✅ Escribir descripción detallada con keywords de activación
✅ Probar con 3+ escenarios reales antes de documentar
✅ Iterar basado en uso real

---

## Niveles de Aplicación

### BLOCK (Guardrails Críticos)

- Previene físicamente la ejecución de herramientas Edit/Write
- Código de salida 2 del hook, stderr → Claude
- Claude ve mensaje y debe usar skill para proceder
- **Usar Para**: Errores críticos, integridad de datos, problemas de seguridad

**Ejemplo:** Verificación de nombre de columna de base de datos

### SUGGEST (Recomendado)

- Recordatorio inyectado antes de que Claude vea el prompt
- Claude está consciente de skills relevantes
- No aplicado, solo asesoría
- **Usar Para**: Guía de dominio, mejores prácticas, guías de cómo hacer

**Ejemplo:** Guías de desarrollo frontend

### WARN (Opcional)

- Sugerencias de baja prioridad
- Solo asesoría, aplicación mínima
- **Usar Para**: Sugerencias agradables de tener, recordatorios informativos

**Raramente usado** - la mayoría de las skills son BLOCK o SUGGEST.

---

## Condiciones de Omitir y Control del Usuario

### 1. Seguimiento de Sesión

**Propósito:** No molestar repetidamente en la misma sesión

**Cómo funciona:**
- Primera edición → Hook bloquea, actualiza estado de sesión
- Segunda edición (misma sesión) → Hook permite
- Sesión diferente → Bloquea de nuevo

**Archivo de Estado:** `.claude/hooks/state/skills-used-{session_id}.json`

### 2. Marcadores de Archivo

**Propósito:** Omitir permanentemente para archivos verificados

**Marcador:** `// @skip-validation`

**Uso:**
```typescript
// @skip-validation
import { PrismaService } from './prisma';
// Este archivo ha sido verificado manualmente
```

**NOTA:** Usar con moderación - derrota el propósito si se usa en exceso

### 3. Variables de Entorno

**Propósito:** Deshabilitar emergencia, anular temporalmente

**Deshabilitar global:**
```bash
export SKIP_SKILL_GUARDRAILS=true  # Deshabilita TODOS los bloques PreToolUse
```

**Específico de skill:**
```bash
export SKIP_DB_VERIFICATION=true
export SKIP_ERROR_REMINDER=true
```

---

## Lista de Verificación de Pruebas

Al crear una nueva skill, verificar:

- [ ] Archivo de skill creado en `.claude/skills/{name}/SKILL.md`
- [ ] Frontmatter apropiado con name y description
- [ ] Entrada agregada a `skill-rules.json`
- [ ] Keywords probadas con prompts reales
- [ ] Patrones de intención probados con variaciones
- [ ] Patrones de ruta de archivo probados con archivos reales
- [ ] Patrones de contenido probados contra contenidos de archivo
- [ ] Mensaje de bloqueo es claro y accionable (si guardrail)
- [ ] Condiciones de omisión configuradas apropiadamente
- [ ] Nivel de prioridad coincide con importancia
- [ ] Sin falsos positivos en pruebas
- [ ] Sin falsos negativos en pruebas
- [ ] Rendimiento es aceptable (<100ms o <200ms)
- [ ] Sintaxis JSON validada: `jq . skill-rules.json`
- [ ] **SKILL.md bajo 500 líneas** ⭐
- [ ] Archivos de referencia creados si es necesario
- [ ] Tabla de contenidos agregada a archivos > 100 líneas

---

## Archivos de Referencia

Para información detallada sobre temas específicos, ver:

### [TRIGGER_TYPES.md](TRIGGER_TYPES.md)
Guía completa de todos los tipos de activadores:
- Activadores de keywords (coincidencia explícita de tema)
- Patrones de intención (detección implícita de acción)
- Activadores de ruta de archivo (patrones glob)
- Patrones de contenido (regex en archivos)
- Mejores prácticas y ejemplos para cada uno
- Trampas comunes y estrategias de prueba

### [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md)
Esquema completo de skill-rules.json:
- Definiciones completas de interfaz TypeScript
- Explicaciones campo por campo
- Ejemplo completo de skill guardrail
- Ejemplo completo de skill de dominio
- Guía de validación y errores comunes

### [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md)
Inmersión profunda en internos de hooks:
- Flujo UserPromptSubmit (detallado)
- Flujo PreToolUse (detallado)
- Tabla de comportamiento de código de salida (CRÍTICO)
- Gestión de estado de sesión
- Consideraciones de rendimiento

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
Guía comprehensiva de depuración:
- Skill no se activa (UserPromptSubmit)
- PreToolUse no bloquea
- Falsos positivos (demasiados activadores)
- Hook no ejecuta en absoluto
- Problemas de rendimiento

### [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)
Colección de patrones listos para usar:
- Biblioteca de patrones de intención (regex)
- Biblioteca de patrones de ruta de archivo (glob)
- Biblioteca de patrones de contenido (regex)
- Organizado por caso de uso
- Listo para copiar-pegar

### [ADVANCED.md](ADVANCED.md)
Mejoras futuras e ideas:
- Actualizaciones dinámicas de reglas
- Dependencias de skills
- Aplicación condicional
- Analíticas de skills
- Versionado de skills

---

## Resumen de Referencia Rápida

### Crear Nueva Skill (5 Pasos)

1. Crear `.claude/skills/{name}/SKILL.md` con frontmatter
2. Agregar entrada a `.claude/skills/skill-rules.json`
3. Probar con comandos `npx tsx`
4. Refinar patrones basado en pruebas
5. Mantener SKILL.md bajo 500 líneas

### Tipos de Activadores

- **Keywords**: Menciones explícitas de tema
- **Intent**: Detección implícita de acción
- **File Paths**: Activación basada en ubicación
- **Content**: Detección específica de tecnología

Ver [TRIGGER_TYPES.md](TRIGGER_TYPES.md) para detalles completos.

### Aplicación

- **BLOCK**: Código de salida 2, solo crítico
- **SUGGEST**: Inyectar contexto, más común
- **WARN**: Asesoría, raramente usado

### Condiciones de Omitir

- **Seguimiento de sesión**: Automático (previene molestias repetidas)
- **Marcadores de archivo**: `// @skip-validation` (omitir permanente)
- **Vars de entorno**: `SKIP_SKILL_GUARDRAILS` (deshabilitar emergencia)

### Mejores Prácticas de Anthropic

✅ **Regla de 500 líneas**: Mantener SKILL.md bajo 500 líneas
✅ **Divulgación progresiva**: Usar archivos de referencia para detalles
✅ **Tabla de contenidos**: Agregar a archivos de referencia > 100 líneas
✅ **Un nivel profundo**: No anidar referencias profundamente
✅ **Descripciones ricas**: Incluir todos los keywords de activación (máx 1024 caracteres)
✅ **Probar primero**: Construir 3+ evaluaciones antes de documentación extensa
✅ **Nomenclatura gerundio**: Preferir verbo + -ing (p. ej., "processing-pdfs")

### Depurar

Probar hooks manualmente:
```bash
# UserPromptSubmit
echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para guía completa de depuración.

---

## Archivos Relacionados

**Configuración:**
- `.claude/skills/skill-rules.json` - Configuración maestra
- `.claude/hooks/state/` - Seguimiento de sesión
- `.claude/settings.json` - Registro de hooks

**Hooks:**
- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Evento Stop (recordatorios suaves)

**Todas las Skills:**
- `.claude/skills/*/SKILL.md` - Archivos de contenido de skill

---

**Estado de Skill**: COMPLETA - Reestructurada siguiendo mejores prácticas de Anthropic ✅
**Conteo de Líneas**: < 500 (siguiendo regla de 500 líneas) ✅
**Divulgación Progresiva**: Archivos de referencia para información detallada ✅

**Siguiente**: Crear más skills, refinar patrones basado en uso

## Ejemplos de Uso

### Ejemplo 1: Crear una Skill que se Active Automáticamente
**Situación**: Quieres crear una skill que se active automáticamente cuando alguien menciona trabajar con bases de datos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una skill que se active automáticamente cuando alguien menciona trabajar con Prisma o bases de datos"
2. Cursor usará esta skill para:
   - Crear el archivo SKILL.md con frontmatter apropiado
   - Agregar la skill a skill-rules.json con keywords como "prisma", "database", "query"
   - Configurar el nivel de aplicación (suggest o block según necesites)
   - Probar que los activadores funcionan correctamente
   - Asegurar que la skill sigue la regla de 500 líneas

**Resultado**: Una skill que se activa automáticamente cuando se mencionan temas relacionados, ayudando a los agentes a usar las mejores prácticas sin tener que recordarlo manualmente.

### Ejemplo 2: Crear una Skill que Bloquee Ediciones hasta que se Use
**Situación**: Quieres asegurar que los agentes siempre verifiquen nombres de columnas antes de hacer consultas a la base de datos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una skill guardrail que bloquee ediciones de archivos con consultas Prisma hasta que se verifiquen los nombres de columna"
2. Cursor implementará:
   - Una skill de tipo "guardrail" con enforcement "block"
   - Un hook PreToolUse que detecta cuando se editan archivos con consultas Prisma
   - Un mensaje claro que explica qué hacer
   - Seguimiento de sesión para no molestar repetidamente

**Resultado**: Una skill que previene errores críticos bloqueando ediciones hasta que se sigan las mejores prácticas de seguridad.

### Ejemplo 3: Depurar por qué una Skill No se Activa
**Situación**: Creaste una skill pero no se activa cuando debería.

**Cómo usar esta skill**:
1. Di a Cursor: "Mi skill no se activa cuando debería, necesito depurarla"
2. Cursor usará esta skill para:
   - Verificar que la skill está en skill-rules.json
   - Probar los activadores manualmente con comandos de prueba
   - Revisar los keywords y patrones de intención
   - Verificar que la descripción incluye los términos correctos
   - Identificar y corregir el problema

**Resultado**: Una skill que funciona correctamente y se activa cuando se necesita, con todos los activadores probados y verificados.
