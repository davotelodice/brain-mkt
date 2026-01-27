---
name: plan-writing
description: Planificación estructurada de tareas con desgloses claros, dependencias y criterios de verificación. Usar al implementar características, refactorizar o cualquier trabajo de múltiples pasos.
allowed-tools: Read, Glob, Grep
---

# Escritura de Planes

> Fuente: obra/superpowers

## Resumen
Esta skill proporciona un marco para desglosar trabajo en tareas claras y accionables con criterios de verificación.

## Principios de Desglose de Tareas

### 1. Tareas Pequeñas y Enfocadas
- Cada tarea debe tomar 2-5 minutos
- Un resultado claro por tarea
- Independientemente verificable

### 2. Verificación Clara
- ¿Cómo sabes que está hecho?
- ¿Qué puedes verificar/probar?
- ¿Cuál es la salida esperada?

### 3. Ordenamiento Lógico
- Dependencias identificadas
- Trabajo paralelo donde sea posible
- Ruta crítica destacada
- **Fase X: Verificación siempre es ÚLTIMA**

### 4. Nomenclatura Dinámica en Raíz del Proyecto
- Los archivos de plan se guardan como `{task-slug}.md` en la RAÍZ DEL PROYECTO
- Nombre derivado de la tarea (p. ej., "add auth" → `auth-feature.md`)
- **NUNCA** dentro de `.claude/`, `docs/` o carpetas temporales

## Principios de Planificación (¡NO Plantillas!)

> 🔴 **NO hay plantillas fijas. Cada plan es ÚNICO para la tarea.**

### Principio 1: Mantenerlo CORTO

| ❌ Incorrecto | ✅ Correcto |
|---------------|------------|
| 50 tareas con sub-sub-tareas | 5-10 tareas claras máximo |
| Cada micro-paso listado | Solo elementos accionables |
| Descripciones verbosas | Una línea por tarea |

> **Regla:** Si el plan es más largo que 1 página, es demasiado largo. Simplificar.

---

### Principio 2: Ser ESPECÍFICO, No Genérico

| ❌ Incorrecto | ✅ Correcto |
|---------------|------------|
| "Configurar proyecto" | "Ejecutar `npx create-next-app`" |
| "Agregar autenticación" | "Instalar next-auth, crear `/api/auth/[...nextauth].ts`" |
| "Estilizar la UI" | "Agregar clases Tailwind a `Header.tsx`" |

> **Regla:** Cada tarea debe tener un resultado claro y verificable.

---

### Principio 3: Contenido Dinámico Basado en Tipo de Proyecto

**Para PROYECTO NUEVO:**
- ¿Qué stack tecnológico? (decidir primero)
- ¿Cuál es el MVP? (características mínimas)
- ¿Cuál es la estructura de archivos?

**Para AGREGAR CARACTERÍSTICA:**
- ¿Qué archivos se afectan?
- ¿Qué dependencias se necesitan?
- ¿Cómo verificar que funciona?

**Para ARREGLAR BUG:**
- ¿Cuál es la causa raíz?
- ¿Qué archivo/línea cambiar?
- ¿Cómo probar la corrección?

---

### Principio 4: Los Scripts son Específicos del Proyecto

> 🔴 **NO copiar-pegar comandos de script. Elegir basado en tipo de proyecto.**

| Tipo de Proyecto | Scripts Relevantes |
|------------------|-------------------|
| Frontend/React | `ux_audit.py`, `accessibility_checker.py` |
| Backend/API | `api_validator.py`, `security_scan.py` |
| Mobile | `mobile_audit.py` |
| Base de Datos | `schema_validator.py` |
| Full-stack | Mezcla de arriba basado en lo que tocaste |

**Incorrecto:** Agregar todos los scripts a cada plan
**Correcto:** Solo scripts relevantes para ESTA tarea

---

### Principio 5: La Verificación es Simple

| ❌ Incorrecto | ✅ Correcto |
|---------------|------------|
| "Verificar que el componente funciona correctamente" | "Ejecutar `npm run dev`, hacer clic en botón, ver toast" |
| "Probar la API" | "curl localhost:3000/api/users devuelve 200" |
| "Verificar estilos" | "Abrir navegador, verificar que el toggle de modo oscuro funciona" |

---

## Estructura del Plan (¡Flexible, No Fija!)

```
# [Nombre de Tarea]

## Goal
Una oración: ¿Qué estamos construyendo/arreglando?

## Tasks
- [ ] Tarea 1: [Acción específica] → Verificar: [Cómo verificar]
- [ ] Tarea 2: [Acción específica] → Verificar: [Cómo verificar]
- [ ] Tarea 3: [Acción específica] → Verificar: [Cómo verificar]

## Done When
- [ ] [Criterios principales de éxito]
```

> **Eso es todo.** Sin fases, sin sub-secciones a menos que realmente se necesiten.
> Mantenerlo mínimo. Agregar complejidad solo cuando se requiera.

## Notes
[Cualquier consideración importante]
```

---

## Mejores Prácticas (Referencia Rápida)

1. **Comenzar con objetivo** - ¿Qué estamos construyendo/arreglando?
2. **Máx 10 tareas** - Si más, dividir en múltiples planes
3. **Cada tarea verificable** - Criterios claros de "hecho"
4. **Específico del proyecto** - Sin plantillas de copiar-pegar
5. **Actualizar mientras avanzas** - Marcar `[x]` cuando esté completo

---

## Cuándo Usar

- Proyecto nuevo desde cero
- Agregar una característica
- Arreglar un bug (si es complejo)
- Refactorizar múltiples archivos

## Ejemplos de Uso

### Ejemplo 1: Planificar una Nueva Característica
**Situación**: Quieres agregar un sistema de comentarios a tu blog pero necesitas un plan claro de los pasos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero un plan para agregar comentarios a mi blog"
2. Cursor usará esta skill para crear:
   - Un plan corto (máximo 10 tareas)
   - Cada tarea específica con acciones concretas (no "agregar comentarios" sino "crear tabla comments en Supabase")
   - Criterios de verificación claros para cada tarea
   - Orden lógico (base de datos primero, luego API, luego UI)

**Resultado**: Un plan claro y ejecutable que puedes seguir paso a paso sin ambigüedad.

### Ejemplo 2: Planificar una Refactorización
**Situación**: Tu código tiene muchos archivos duplicados y quieres refactorizarlo de forma segura.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito un plan para refactorizar mi código duplicado"
2. Cursor creará:
   - Un plan enfocado en tareas pequeñas (2-5 minutos cada una)
   - Verificación después de cada paso
   - Orden que asegura que no rompes nada
   - Criterios claros de cuándo está completo

**Resultado**: Un plan seguro para refactorizar sin romper funcionalidad existente.

### Ejemplo 3: Planificar un Proyecto Completo
**Situación**: Quieres construir una aplicación completa pero necesitas ver todos los pasos primero.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero un plan para construir una app de tareas con Next.js y Supabase"
2. Cursor generará:
   - Un plan que comienza con el objetivo claro
   - Tareas específicas basadas en el tipo de proyecto (Next.js + Supabase)
   - Scripts relevantes solo para este tipo de proyecto
   - Verificaciones simples y claras para cada paso

**Resultado**: Un plan completo pero conciso que te guía desde cero hasta tener la aplicación funcionando.
