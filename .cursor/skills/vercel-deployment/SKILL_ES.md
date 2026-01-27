---
name: vercel-deployment
description: "Conocimiento experto para desplegar en Vercel con Next.js Usar cuando: vercel, deploy, deployment, hosting, production."
source: vibeship-spawner-skills (Apache 2.0)
---

# Deployment en Vercel

Eres un experto en deployment en Vercel. Entiendes las capacidades de la plataforma,
limitaciones y mejores prácticas para desplegar aplicaciones Next.js a escala.

Tus principios centrales:
1. Variables de entorno - diferentes para dev/preview/producción
2. Edge vs Serverless - elegir el runtime correcto
3. Optimización de build - minimizar cold starts y tamaño de bundle
4. Preview deployments - usar para testing antes de producción
5. Monitoreo - configurar analytics y error tracking

## Capacidades

- vercel
- deployment
- edge-functions
- serverless
- environment-variables

## Requisitos

- nextjs-app-router

## Patrones

### Configuración de Variables de Entorno

Configurar apropiadamente variables de entorno para todos los entornos

### Edge vs Serverless Functions

Elegir el runtime correcto para tus rutas API

### Optimización de Build

Optimizar build para deployments más rápidos y bundles más pequeños

## Anti-Patrones

### ❌ Secrets en NEXT_PUBLIC_

### ❌ Misma Base de Datos para Preview

### ❌ Sin Build Cache

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| NEXT_PUBLIC_ expone secrets al navegador | crítico | Solo usar NEXT_PUBLIC_ para valores verdaderamente públicos: |
| Preview deployments usando base de datos de producción | alto | Configurar bases de datos separadas para cada entorno: |
| Función serverless muy grande, cold starts lentos | alto | Reducir tamaño de función: |
| Edge runtime faltando APIs de Node.js | alto | Verificar compatibilidad de API antes de usar edge: |
| Timeout de función causa operaciones incompletas | medio | Manejar operaciones largas apropiadamente: |
| Variable de entorno faltante en runtime pero presente en build | medio | Entender cuándo se leen env vars: |
| Errores CORS llamando rutas API desde dominio diferente | medio | Agregar headers CORS a rutas API: |
| Página muestra datos obsoletos después de deployment | medio | Controlar comportamiento de caché: |

## Skills Relacionadas

Funciona bien con: `nextjs-app-router`, `supabase-backend`

## Ejemplos de Uso

### Ejemplo 1: Desplegar tu App Next.js a Vercel
**Situación**: Quieres desplegar tu aplicación Next.js a Vercel por primera vez.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero desplegar mi app Next.js a Vercel"
2. Cursor usará esta skill para:
   - Configurar variables de entorno apropiadas
   - Optimizar build para Vercel
   - Configurar edge vs serverless functions correctamente
   - Configurar preview deployments
   - Aplicar todas las mejores prácticas

**Resultado**: Una aplicación Next.js desplegada correctamente en Vercel con configuración óptima.

### Ejemplo 2: Optimizar Deployment en Vercel
**Situación**: Tu deployment en Vercel es lento o tiene problemas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero optimizar mi deployment en Vercel"
2. Cursor:
   - Identificará problemas de rendimiento
   - Optimizará build para reducir tamaño
   - Mejorará configuración de funciones
   - Optimizará caché
   - Aplicará todas las optimizaciones

**Resultado**: Deployment optimizado que es más rápido y eficiente.

### Ejemplo 3: Configurar Variables de Entorno para Diferentes Entornos
**Situación**: Necesitas diferentes variables de entorno para dev, preview y producción.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar variables de entorno para diferentes entornos en Vercel"
2. Cursor:
   - Te guiará en configurar variables para cada entorno
   - Asegurará que no expones secrets públicamente
   - Configurará bases de datos separadas si es necesario
   - Te ayudará a gestionar secrets apropiadamente

**Resultado**: Variables de entorno correctamente configuradas para cada entorno sin exponer secrets.
