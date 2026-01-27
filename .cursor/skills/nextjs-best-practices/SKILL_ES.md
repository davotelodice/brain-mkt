---
name: nextjs-best-practices
description: Principios del App Router de Next.js. Server Components, obtención de datos, patrones de enrutamiento.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Mejores Prácticas de Next.js

> Principios para el desarrollo con Next.js App Router.

---

## 1. Server vs Client Components

### Árbol de Decisión

```
¿Necesita...?
│
├── useState, useEffect, manejadores de eventos
│   └── Client Component ('use client')
│
├── Obtención directa de datos, sin interactividad
│   └── Server Component (por defecto)
│
└── ¿Ambos? 
    └── Dividir: Server padre + Client hijo
```

### Por Defecto

| Tipo | Usar |
|------|------|
| **Server** | Obtención de datos, layout, contenido estático |
| **Client** | Formularios, botones, UI interactiva |

---

## 2. Patrones de Obtención de Datos

### Estrategia de Fetch

| Patrón | Usar |
|--------|------|
| **Default** | Estático (cachead en build) |
| **Revalidate** | ISR (actualización basada en tiempo) |
| **No-store** | Dinámico (cada solicitud) |

### Flujo de Datos

| Fuente | Patrón |
|--------|--------|
| Base de datos | fetch en Server Component |
| API | fetch con caché |
| Entrada del usuario | estado del cliente + server action |

---

## 3. Principios de Enrutamiento

### Convenciones de Archivos

| Archivo | Propósito |
|---------|-----------|
| `page.tsx` | UI de ruta |
| `layout.tsx` | Layout compartido |
| `loading.tsx` | Estado de carga |
| `error.tsx` | Límite de error |
| `not-found.tsx` | Página 404 |

### Organización de Rutas

| Patrón | Usar |
|--------|------|
| Grupos de ruta `(name)` | Organizar sin URL |
| Rutas paralelas `@slot` | Múltiples páginas del mismo nivel |
| Interceptando `(.)` | Superposiciones modales |

---

## 4. Rutas API

### Route Handlers

| Método | Usar |
|--------|------|
| GET | Leer datos |
| POST | Crear datos |
| PUT/PATCH | Actualizar datos |
| DELETE | Eliminar datos |

### Mejores Prácticas

- Validar entrada con Zod
- Devolver códigos de estado apropiados
- Manejar errores con gracia
- Usar Edge runtime cuando sea posible

---

## 5. Principios de Rendimiento

### Optimización de Imágenes

- Usar componente next/image
- Establecer prioridad para above-fold
- Proporcionar placeholder borroso
- Usar tamaños responsivos

### Optimización de Bundle

- Imports dinámicos para componentes pesados
- Code splitting basado en rutas (automático)
- Analizar con bundle analyzer

---

## 6. Metadata

### Estático vs Dinámico

| Tipo | Usar |
|------|------|
| Static export | Metadata fija |
| generateMetadata | Dinámico por ruta |

### Etiquetas Esenciales

- title (50-60 caracteres)
- description (150-160 caracteres)
- Imágenes Open Graph
- URL canónica

---

## 7. Estrategia de Caché

### Capas de Caché

| Capa | Control |
|------|---------|
| Request | opciones de fetch |
| Data | revalidate/tags |
| Full route | config de ruta |

### Revalidación

| Método | Usar |
|--------|------|
| Basado en tiempo | `revalidate: 60` |
| On-demand | `revalidatePath/Tag` |
| Sin caché | `no-store` |

---

## 8. Server Actions

### Casos de Uso

- Envíos de formularios
- Mutaciones de datos
- Disparadores de revalidación

### Mejores Prácticas

- Marcar con 'use server'
- Validar todas las entradas
- Devolver respuestas tipadas
- Manejar errores

---

## 9. Anti-Patrones

| ❌ No Hacer | ✅ Hacer |
|------------|---------|
| 'use client' en todas partes | Server por defecto |
| Fetch en client components | Fetch en server |
| Omitir estados de carga | Usar loading.tsx |
| Ignorar límites de error | Usar error.tsx |
| Bundles grandes del cliente | Imports dinámicos |

---

## 10. Estructura del Proyecto

```
app/
├── (marketing)/     # Grupo de ruta
│   └── page.tsx
├── (dashboard)/
│   ├── layout.tsx   # Layout del dashboard
│   └── page.tsx
├── api/
│   └── [resource]/
│       └── route.ts
└── components/
    └── ui/
```

---

> **Recuerda:** Los Server Components son el predeterminado por una razón. Comienza ahí, agrega client solo cuando sea necesario.

## Ejemplos de Uso

### Ejemplo 1: Crear una Página que Muestra Datos de una Base de Datos
**Situación**: Quieres crear una página en Next.js que muestre una lista de productos desde tu base de datos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una página en Next.js que muestre productos desde mi base de datos"
2. Cursor usará esta skill para crear:
   - Un Server Component que obtiene los datos directamente de la base de datos
   - Una página que se renderiza en el servidor (más rápido)
   - Caché automático para que no tenga que consultar la base de datos en cada visita
   - Un layout compartido para mantener el diseño consistente

**Resultado**: Una página rápida que muestra tus productos sin necesidad de JavaScript en el cliente, mejorando el rendimiento y SEO.

### Ejemplo 2: Agregar un Formulario de Contacto Interactivo
**Situación**: Necesitas un formulario donde los usuarios puedan escribir y enviar mensajes.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito un formulario de contacto en Next.js donde los usuarios puedan escribir y enviar mensajes"
2. Cursor implementará:
   - Un Client Component para el formulario (necesita interactividad)
   - Un Server Action para procesar el envío del formulario
   - Validación de datos antes de enviar
   - Manejo de errores si algo falla
   - Mensaje de éxito después de enviar

**Resultado**: Un formulario funcional que procesa los datos de forma segura en el servidor, con buena experiencia de usuario.

### Ejemplo 3: Crear una API para tu Aplicación
**Situación**: Necesitas crear endpoints API para que otras aplicaciones o tu frontend puedan obtener datos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una API en Next.js que devuelva información de usuarios"
2. Cursor creará:
   - Un archivo `route.ts` en la carpeta `app/api/usuarios/`
   - Endpoints GET, POST, PUT, DELETE según necesites
   - Validación de datos de entrada
   - Respuestas con códigos de estado correctos (200, 404, 500, etc.)
   - Manejo de errores apropiado

**Resultado**: Una API RESTful completa y bien estructurada que sigue las mejores prácticas de Next.js, lista para usar en producción.
