---
name: vercel-react-best-practices
description: Guías de optimización de rendimiento de React y Next.js de Vercel Engineering. Esta skill debe usarse al escribir, revisar o refactorizar código React/Next.js para asegurar patrones de rendimiento óptimos. Se activa en tareas involucrando componentes React, páginas Next.js, data fetching, optimización de bundle o mejoras de rendimiento.
---

# Mejores Prácticas React de Vercel

Guía comprehensiva de optimización de rendimiento para aplicaciones React y Next.js, mantenida por Vercel. Contiene 45 reglas a través de 8 categorías, priorizadas por impacto para guiar refactorización automatizada y generación de código.

## Cuándo Aplicar

Referenciar estas guías cuando:
- Escribir nuevos componentes React o páginas Next.js
- Implementar data fetching (cliente o server-side)
- Revisar código para problemas de rendimiento
- Refactorizar código React/Next.js existente
- Optimizar tamaño de bundle o tiempos de carga

## Categorías de Reglas por Prioridad

| Prioridad | Categoría | Impacto | Prefijo |
|-----------|-----------|---------|---------|
| 1 | Eliminar Waterfalls | CRÍTICO | `async-` |
| 2 | Optimización de Tamaño de Bundle | CRÍTICO | `bundle-` |
| 3 | Rendimiento Server-Side | ALTO | `server-` |
| 4 | Data Fetching Client-Side | MEDIO-ALTO | `client-` |
| 5 | Optimización de Re-render | MEDIO | `rerender-` |
| 6 | Rendimiento de Renderizado | MEDIO | `rendering-` |
| 7 | Rendimiento JavaScript | BAJO-MEDIO | `js-` |
| 8 | Patrones Avanzados | BAJO | `advanced-` |

## Referencia Rápida

### 1. Eliminar Waterfalls (CRÍTICO)

- `async-defer-await` - Mover await a ramas donde realmente se usa
- `async-parallel` - Usar Promise.all() para operaciones independientes
- `async-dependencies` - Usar better-all para dependencias parciales
- `async-api-routes` - Iniciar promesas temprano, await tarde en rutas API
- `async-suspense-boundaries` - Usar Suspense para stream de contenido

### 2. Optimización de Tamaño de Bundle (CRÍTICO)

- `bundle-barrel-imports` - Importar directamente, evitar archivos barrel
- `bundle-dynamic-imports` - Usar next/dynamic para componentes pesados
- `bundle-defer-third-party` - Cargar analytics/logging después de hidratación
- `bundle-conditional` - Cargar módulos solo cuando característica está activada
- `bundle-preload` - Preload en hover/focus para velocidad percibida

### 3. Rendimiento Server-Side (ALTO)

- `server-cache-react` - Usar React.cache() para deduplicación por request
- `server-cache-lru` - Usar caché LRU para caching cross-request
- `server-serialization` - Minimizar datos pasados a componentes cliente
- `server-parallel-fetching` - Reestructurar componentes para paralelizar fetches
- `server-after-nonblocking` - Usar after() para operaciones no bloqueantes

### 4. Data Fetching Client-Side (MEDIO-ALTO)

- `client-swr-dedup` - Usar SWR para deduplicación automática de requests
- `client-event-listeners` - Deduplicar event listeners globales

### 5. Optimización de Re-render (MEDIO)

- `rerender-defer-reads` - No subscribirse a estado solo usado en callbacks
- `rerender-memo` - Extraer trabajo costoso a componentes memoizados
- `rerender-dependencies` - Usar dependencias primitivas en effects
- `rerender-derived-state` - Subscribirse a booleanos derivados, no valores crudos
- `rerender-functional-setstate` - Usar setState funcional para callbacks estables
- `rerender-lazy-state-init` - Pasar función a useState para valores costosos
- `rerender-transitions` - Usar startTransition para actualizaciones no urgentes

### 6. Rendimiento de Renderizado (MEDIO)

- `rendering-animate-svg-wrapper` - Animar wrapper div, no elemento SVG
- `rendering-content-visibility` - Usar content-visibility para listas largas
- `rendering-hoist-jsx` - Extraer JSX estático fuera de componentes
- `rendering-svg-precision` - Reducir precisión de coordenadas SVG
- `rendering-hydration-no-flicker` - Usar script inline para datos solo cliente
- `rendering-activity` - Usar componente Activity para show/hide
- `rendering-conditional-render` - Usar ternario, no && para condicionales

### 7. Rendimiento JavaScript (BAJO-MEDIO)

- `js-batch-dom-css` - Agrupar cambios CSS vía clases o cssText
- `js-index-maps` - Construir Map para búsquedas repetidas
- `js-cache-property-access` - Cachear acceso a propiedades de objeto en loops
- `js-cache-function-results` - Cachear resultados de función en Map a nivel módulo
- `js-cache-storage` - Cachear lecturas localStorage/sessionStorage
- `js-combine-iterations` - Combinar múltiples filter/map en un loop
- `js-length-check-first` - Verificar longitud de array antes de comparación costosa
- `js-early-exit` - Retornar temprano de funciones
- `js-hoist-regexp` - Hoist creación RegExp fuera de loops
- `js-min-max-loop` - Usar loop para min/max en lugar de sort
- `js-set-map-lookups` - Usar Set/Map para búsquedas O(1)
- `js-tosorted-immutable` - Usar toSorted() para inmutabilidad

### 8. Patrones Avanzados (BAJO)

- `advanced-event-handler-refs` - Almacenar event handlers en refs
- `advanced-use-latest` - useLatest para callback refs estables

## Cómo Usar

Leer archivos de reglas individuales para explicaciones detalladas y ejemplos de código:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Cada archivo de regla contiene:
- Explicación breve de por qué importa
- Ejemplo de código incorrecto con explicación
- Ejemplo de código correcto con explicación
- Contexto adicional y referencias

## Documento Completo Compilado

Para la guía completa con todas las reglas expandidas: `AGENTS.md`

## Ejemplos de Uso

### Ejemplo 1: Optimizar el Rendimiento de tu Aplicación React
**Situación**: Tu aplicación React es lenta y quieres aplicar las mejores prácticas de rendimiento.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero optimizar el rendimiento de mi aplicación React usando las mejores prácticas de Vercel"
2. Cursor usará esta skill para:
   - Identificar y eliminar waterfalls (operaciones secuenciales innecesarias)
   - Optimizar el tamaño del bundle (imports directos, dynamic imports)
   - Mejorar rendimiento server-side (caching, serialización)
   - Optimizar re-renders (memoización, dependencias)
   - Aplicar todas las optimizaciones priorizadas por impacto

**Resultado**: Una aplicación significativamente más rápida siguiendo las mejores prácticas probadas de Vercel.

### Ejemplo 2: Optimizar Data Fetching en tu Aplicación
**Situación**: Tu aplicación hace muchas llamadas a APIs y quieres optimizarlas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero optimizar cómo obtengo datos en mi aplicación React"
2. Cursor aplicará:
   - Eliminar waterfalls (usar Promise.all() para operaciones paralelas)
   - Usar SWR para deduplicación automática
   - Implementar caching apropiado
   - Optimizar para Suspense boundaries

**Resultado**: Data fetching más eficiente que reduce llamadas redundantes y mejora tiempos de carga.

### Ejemplo 3: Reducir el Tamaño del Bundle
**Situación**: Tu bundle de JavaScript es muy grande y quieres reducirlo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero reducir el tamaño del bundle de mi aplicación"
2. Cursor:
   - Eliminará imports de barrel files
   - Implementará dynamic imports para componentes pesados
   - Diferirá carga de third-party scripts
   - Aplicará todas las optimizaciones de bundle

**Resultado**: Un bundle significativamente más pequeño que carga más rápido y mejora la experiencia del usuario.
