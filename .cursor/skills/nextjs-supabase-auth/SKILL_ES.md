---
name: nextjs-supabase-auth
description: "Integración experta de Supabase Auth con Next.js App Router. Usar cuando: autenticación supabase next, autenticación next.js, login supabase, middleware de auth, ruta protegida."
source: vibeship-spawner-skills (Apache 2.0)
---

# Next.js + Supabase Auth

Eres un experto en integrar Supabase Auth con Next.js App Router.
Entiendes el límite servidor/cliente, cómo manejar auth en middleware,
Server Components, Client Components y Server Actions.

Tus principios fundamentales:
1. Usar @supabase/ssr para integración con App Router
2. Manejar tokens en middleware para rutas protegidas
3. Nunca exponer tokens de auth al cliente innecesariamente
4. Usar Server Actions para operaciones de auth cuando sea posible
5. Entender el flujo de sesión basado en cookies

## Capacidades

- nextjs-auth
- supabase-auth-nextjs
- auth-middleware
- auth-callback

## Requisitos

- nextjs-app-router
- supabase-backend

## Patrones

### Configuración del Cliente de Supabase

Crear clientes de Supabase correctamente configurados para diferentes contextos

### Middleware de Auth

Proteger rutas y refrescar sesiones en middleware

### Ruta de Callback de Auth

Manejar callback OAuth e intercambiar código por sesión

## Anti-Patrones

### ❌ getSession en Server Components

### ❌ Estado de Auth en Client Sin Listener

### ❌ Almacenar Tokens Manualmente

## Skills Relacionadas

Funciona bien con: `nextjs-app-router`, `supabase-backend`

## Ejemplos de Uso

### Ejemplo 1: Agregar Login y Registro a tu Aplicación Next.js
**Situación**: Tienes una aplicación Next.js y quieres que los usuarios puedan registrarse e iniciar sesión usando Supabase.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero agregar autenticación con Supabase a mi aplicación Next.js, necesito login y registro"
2. Cursor usará esta skill para crear:
   - Un middleware que protege las rutas y maneja las sesiones
   - Páginas de login y registro con formularios
   - Server Actions para procesar el login/registro de forma segura
   - Redirección automática después de autenticarse
   - Manejo de sesiones con cookies seguras

**Resultado**: Un sistema de autenticación completo y seguro donde los usuarios pueden registrarse, iniciar sesión y sus sesiones se mantienen automáticamente.

### Ejemplo 2: Proteger una Página para Solo Usuarios Autenticados
**Situación**: Tienes una página de dashboard que solo deben ver usuarios que hayan iniciado sesión.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero que mi página de dashboard solo sea accesible para usuarios que hayan iniciado sesión"
2. Cursor implementará:
   - Middleware que verifica si el usuario está autenticado
   - Redirección automática a login si no está autenticado
   - Acceso a la información del usuario en la página protegida
   - Manejo seguro de tokens sin exponerlos al cliente

**Resultado**: Una página protegida que solo usuarios autenticados pueden ver, con redirección automática para usuarios no autenticados.

### Ejemplo 3: Agregar Login con Google o GitHub
**Situación**: Quieres que los usuarios puedan iniciar sesión usando sus cuentas de Google o GitHub en lugar de crear una cuenta nueva.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero agregar login con Google y GitHub usando Supabase en Next.js"
2. Cursor configurará:
   - Ruta de callback para manejar la respuesta de OAuth
   - Botones de login con Google/GitHub
   - Intercambio automático del código OAuth por una sesión
   - Creación automática de usuario si es la primera vez que inicia sesión
   - Manejo de errores si el login falla

**Resultado**: Los usuarios pueden iniciar sesión con un clic usando sus cuentas de Google o GitHub, sin necesidad de crear una cuenta nueva.
