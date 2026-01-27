---
name: frontend-dev-guidelines
description: Guías de desarrollo frontend para aplicaciones React/TypeScript. Patrones modernos incluyendo Suspense, lazy loading, useSuspenseQuery, organización de archivos con directorio features, estilos MUI v7, TanStack Router, optimización de rendimiento y mejores prácticas de TypeScript. Usar al crear componentes, páginas, características, obtener datos, estilizar, routing o trabajar con código frontend.
---

# Guías de Desarrollo Frontend

## Propósito

Guía comprehensiva para desarrollo React moderno, enfatizando data fetching basado en Suspense, lazy loading, organización apropiada de archivos y optimización de rendimiento.

## Cuándo Usar Esta Skill

- Crear nuevos componentes o páginas
- Construir nuevas características
- Obtener datos con TanStack Query
- Configurar routing con TanStack Router
- Estilizar componentes con MUI v7
- Optimización de rendimiento
- Organizar código frontend
- Mejores prácticas de TypeScript

---

## Inicio Rápido

### Lista de Verificación de Nuevo Componente

¿Creando un componente? Seguir esta lista de verificación:

- [ ] Usar patrón `React.FC<Props>` con TypeScript
- [ ] Lazy load si componente pesado: `React.lazy(() => import())`
- [ ] Envolver en `<SuspenseLoader>` para estados de carga
- [ ] Usar `useSuspenseQuery` para obtener datos
- [ ] Aliases de import: `@/`, `~types`, `~components`, `~features`
- [ ] Estilos: Inline si <100 líneas, archivo separado si >100 líneas
- [ ] Usar `useCallback` para event handlers pasados a hijos
- [ ] Default export al final
- [ ] Sin early returns con loading spinners
- [ ] Usar `useMuiSnackbar` para notificaciones de usuario

### Lista de Verificación de Nueva Característica

¿Creando una característica? Configurar esta estructura:

- [ ] Crear directorio `features/{feature-name}/`
- [ ] Crear subdirectorios: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] Crear archivo de servicio API: `api/{feature}Api.ts`
- [ ] Configurar tipos TypeScript en `types/`
- [ ] Crear ruta en `routes/{feature-name}/index.tsx`
- [ ] Lazy load componentes de característica
- [ ] Usar límites de Suspense
- [ ] Exportar API pública desde `index.ts` de característica

---

## Referencia Rápida de Aliases de Import

| Alias | Resuelve A | Ejemplo |
|-------|------------|---------|
| `@/` | `src/` | `import { apiClient } from '@/lib/apiClient'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { SuspenseLoader } from '~components/SuspenseLoader'` |
| `~features` | `src/features` | `import { authApi } from '~features/auth'` |

Definido en: [vite.config.ts](../../vite.config.ts) líneas 180-185

---

## Cheatsheet de Imports Comunes

```typescript
// React & Lazy Loading
import React, { useState, useCallback, useMemo } from 'react';
const Heavy = React.lazy(() => import('./Heavy'));

// Componentes MUI
import { Box, Paper, Typography, Button, Grid } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

// TanStack Query (Suspense)
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';

// TanStack Router
import { createFileRoute } from '@tanstack/react-router';

// Componentes del Proyecto
import { SuspenseLoader } from '~components/SuspenseLoader';

// Hooks
import { useAuth } from '@/hooks/useAuth';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

// Types
import type { Post } from '~types/post';
```

---

## Guías de Temas

### 🎨 Patrones de Componente

**Los componentes React modernos usan:**
- `React.FC<Props>` para type safety
- `React.lazy()` para code splitting
- `SuspenseLoader` para estados de carga
- Patrón named const + default export

**Conceptos Clave:**
- Lazy load componentes pesados (DataGrid, charts, editors)
- Siempre envolver componentes lazy en Suspense
- Usar componente SuspenseLoader (con animación fade)
- Estructura de componente: Props → Hooks → Handlers → Render → Export

**[📖 Guía Completa: resources/component-patterns.md](resources/component-patterns.md)**

---

### 📊 Obtención de Datos

**PATRÓN PRIMARIO: useSuspenseQuery**
- Usar con límites de Suspense
- Estrategia cache-first (verificar caché de grid antes de API)
- Reemplaza verificaciones `isLoading`
- Type-safe con genéricos

**Capa de Servicio API:**
- Crear `features/{feature}/api/{feature}Api.ts`
- Usar instancia axios `apiClient`
- Métodos centralizados por característica
- Formato de ruta: `/form/route` (NO `/api/form/route`)

**[📖 Guía Completa: resources/data-fetching.md](resources/data-fetching.md)**

---

### 📁 Organización de Archivos

**features/ vs components/:**
- `features/`: Específico de dominio (posts, comments, auth)
- `components/`: Verdaderamente reutilizable (SuspenseLoader, CustomAppBar)

**Subdirectorios de Característica:**
```
features/
  my-feature/
    api/          # Capa de servicio API
    components/   # Componentes de característica
    hooks/        # Hooks personalizados
    helpers/      # Funciones de utilidad
    types/        # Tipos TypeScript
```

**[📖 Guía Completa: resources/file-organization.md](resources/file-organization.md)**

---

### 🎨 Estilizado

**Inline vs Separado:**
- <100 líneas: Inline `const styles: Record<string, SxProps<Theme>>`
- >100 líneas: Archivo `.styles.ts` separado

**Método Primario:**
- Usar prop `sx` para componentes MUI
- Type-safe con `SxProps<Theme>`
- Acceso a tema: `(theme) => theme.palette.primary.main`

**MUI v7 Grid:**
```typescript
<Grid size={{ xs: 12, md: 6 }}>  // ✅ sintaxis v7
<Grid xs={12} md={6}>             // ❌ Sintaxis antigua
```

**[📖 Guía Completa: resources/styling-guide.md](resources/styling-guide.md)**

---

### 🛣️ Routing

**TanStack Router - Basado en Carpetas:**
- Directorio: `routes/my-route/index.tsx`
- Lazy load componentes
- Usar `createFileRoute`
- Datos de breadcrumb en loader

**Ejemplo:**
```typescript
import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));

export const Route = createFileRoute('/my-route/')({
    component: MyPage,
    loader: () => ({ crumb: 'My Route' }),
});
```

**[📖 Guía Completa: resources/routing-guide.md](resources/routing-guide.md)**

---

### ⏳ Estados de Carga y Error

**REGLA CRÍTICA: Sin Early Returns**

```typescript
// ❌ NUNCA - Causa layout shift
if (isLoading) {
    return <LoadingSpinner />;
}

// ✅ SIEMPRE - Layout consistente
<SuspenseLoader>
    <Content />
</SuspenseLoader>
```

**Por qué:** Previene Cumulative Layout Shift (CLS), mejor UX

**Manejo de Errores:**
- Usar `useMuiSnackbar` para retroalimentación de usuario
- NUNCA `react-toastify`
- Callbacks `onError` de TanStack Query

**[📖 Guía Completa: resources/loading-and-error-states.md](resources/loading-and-error-states.md)**

---

### ⚡ Rendimiento

**Patrones de Optimización:**
- `useMemo`: Cálculos costosos (filter, sort, map)
- `useCallback`: Event handlers pasados a hijos
- `React.memo`: Componentes costosos
- Búsqueda debounced (300-500ms)
- Prevención de memory leaks (cleanup en useEffect)

**[📖 Guía Completa: resources/performance.md](resources/performance.md)**

---

### 📘 TypeScript

**Estándares:**
- Modo estricto, sin tipo `any`
- Tipos de retorno explícitos en funciones
- Imports de tipo: `import type { User } from '~types/user'`
- Interfaces de props de componente con JSDoc

**[📖 Guía Completa: resources/typescript-standards.md](resources/typescript-standards.md)**

---

### 🔧 Patrones Comunes

**Temas Cubiertos:**
- React Hook Form con validación Zod
- Contratos de wrapper DataGrid
- Estándares de componente Dialog
- Hook `useAuth` para usuario actual
- Patrones de mutación con invalidación de caché

**[📖 Guía Completa: resources/common-patterns.md](resources/common-patterns.md)**

---

### 📚 Ejemplos Completos

**Ejemplos completos funcionando:**
- Componente moderno con todos los patrones
- Estructura de característica completa
- Capa de servicio API
- Ruta con lazy loading
- Suspense + useSuspenseQuery
- Formulario con validación

**[📖 Guía Completa: resources/complete-examples.md](resources/complete-examples.md)**

---

## Guía de Navegación

| Necesitas... | Lee este recurso |
|--------------|------------------|
| Crear un componente | [component-patterns.md](resources/component-patterns.md) |
| Obtener datos | [data-fetching.md](resources/data-fetching.md) |
| Organizar archivos/carpetas | [file-organization.md](resources/file-organization.md) |
| Estilizar componentes | [styling-guide.md](resources/styling-guide.md) |
| Configurar routing | [routing-guide.md](resources/routing-guide.md) |
| Manejar carga/errores | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Optimizar rendimiento | [performance.md](resources/performance.md) |
| Tipos TypeScript | [typescript-standards.md](resources/typescript-standards.md) |
| Forms/Auth/DataGrid | [common-patterns.md](resources/common-patterns.md) |
| Ver ejemplos completos | [complete-examples.md](resources/complete-examples.md) |

---

## Principios Fundamentales

1. **Lazy Load Todo lo Pesado**: Rutas, DataGrid, charts, editors
2. **Suspense para Carga**: Usar SuspenseLoader, no early returns
3. **useSuspenseQuery**: Patrón primario de obtención de datos para código nuevo
4. **Las Características Están Organizadas**: subdirs api/, components/, hooks/, helpers/
5. **Estilos Basados en Tamaño**: <100 inline, >100 separado
6. **Aliases de Import**: Usar @/, ~types, ~components, ~features
7. **Sin Early Returns**: Previene layout shift
8. **useMuiSnackbar**: Para todas las notificaciones de usuario

---

## Referencia Rápida: Estructura de Archivos

```
src/
  features/
    my-feature/
      api/
        myFeatureApi.ts       # Servicio API
      components/
        MyFeature.tsx         # Componente principal
        SubComponent.tsx      # Componentes relacionados
      hooks/
        useMyFeature.ts       # Hooks personalizados
        useSuspenseMyFeature.ts  # Hooks Suspense
      helpers/
        myFeatureHelpers.ts   # Utilidades
      types/
        index.ts              # Tipos TypeScript
      index.ts                # Exports públicos

  components/
    SuspenseLoader/
      SuspenseLoader.tsx      # Loader reutilizable
    CustomAppBar/
      CustomAppBar.tsx        # App bar reutilizable

  routes/
    my-route/
      index.tsx               # Componente de ruta
      create/
        index.tsx             # Ruta anidada
```

---

## Plantilla de Componente Moderno (Copia Rápida)

```typescript
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
    id: number;
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
    const [state, setState] = useState<string>('');

    const { data } = useSuspenseQuery({
        queryKey: ['feature', id],
        queryFn: () => featureApi.getFeature(id),
    });

    const handleAction = useCallback(() => {
        setState('updated');
        onAction?.();
    }, [onAction]);

    return (
        <Box sx={{ p: 2 }}>
            <Paper sx={{ p: 3 }}>
                {/* Contenido */}
            </Paper>
        </Box>
    );
};

export default MyComponent;
```

Para ejemplos completos, ver [resources/complete-examples.md](resources/complete-examples.md)

---

## Skills Relacionadas

- **error-tracking**: Seguimiento de errores con Sentry (aplica a frontend también)
- **backend-dev-guidelines**: Patrones de API backend que el frontend consume

---

**Estado de Skill**: Estructura modular con carga progresiva para gestión óptima de contexto

## Ejemplos de Uso

### Ejemplo 1: Crear un Nuevo Componente React Siguiendo las Guías
**Situación**: Quieres crear un nuevo componente React pero quieres asegurarte de seguir las mejores prácticas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un nuevo componente React siguiendo las guías de frontend"
2. Cursor usará esta skill para:
   - Usar el patrón `React.FC<Props>` con TypeScript
   - Lazy load el componente si es pesado
   - Envolverlo en SuspenseLoader para estados de carga
   - Usar useSuspenseQuery para obtener datos
   - Organizar el código apropiadamente con aliases de import
   - Seguir todas las mejores prácticas de la skill

**Resultado**: Un componente React moderno y optimizado que sigue todas las mejores prácticas, con código limpio y bien organizado.

### Ejemplo 2: Crear una Nueva Característica Completa
**Situación**: Quieres agregar una nueva característica a tu aplicación pero necesitas saber cómo organizarla correctamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una nueva característica de posts siguiendo la estructura correcta"
2. Cursor:
   - Creará la estructura de directorios apropiada (features/posts/)
   - Configurará subdirectorios (api/, components/, hooks/, helpers/, types/)
   - Creará el servicio API para obtener datos
   - Configurará las rutas con TanStack Router
   - Implementará lazy loading y Suspense
   - Exportará la API pública correctamente

**Resultado**: Una característica completa y bien organizada que es fácil de mantener y extender.

### Ejemplo 3: Optimizar el Rendimiento de tu Aplicación React
**Situación**: Tu aplicación React es lenta y quieres optimizarla.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero optimizar el rendimiento de mi aplicación React"
2. Cursor usará esta skill para:
   - Identificar componentes que deberían lazy loadearse
   - Optimizar data fetching con useSuspenseQuery
   - Aplicar useMemo y useCallback donde sea apropiado
   - Mejorar la organización de archivos para mejor code splitting
   - Implementar todas las optimizaciones recomendadas

**Resultado**: Una aplicación más rápida y eficiente que carga más rápido y usa menos recursos.
