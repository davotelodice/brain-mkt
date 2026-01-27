# 🎨 Frontend - Marketing Second Brain

Next.js 14 App Router con TypeScript y Tailwind CSS.

## 🚀 Quick Start

```bash
# Instalar dependencias
npm install

# Modo desarrollo (con Turbopack)
npm run dev

# Build para producción
npm run build

# Iniciar en producción
npm start
```

## 📁 Estructura del Proyecto

```
frontend/
├── app/
│   ├── layout.tsx           # Layout raíz (Server Component)
│   ├── page.tsx             # Homepage/Dashboard
│   ├── login/
│   │   └── page.tsx         # Login (Client Component)
│   ├── register/
│   │   └── page.tsx         # Register (Client Component)
│   └── components/
│       └── LogoutButton.tsx # Botón de logout (Client Component)
├── lib/
│   └── api.ts               # API client utilities
├── middleware.ts            # Auth middleware (cookies httpOnly)
└── .env.local              # Variables de entorno
```

## 🔐 Autenticación

### GOTCHA 10: Cookies httpOnly vs localStorage

**Problema:** `localStorage` no es accesible en Server Components.

**Solución:** El backend setea cookies httpOnly que el middleware de Next.js puede leer.

### Flujo de Autenticación

1. **Login:** Usuario envía email + password
2. **Backend:** Valida credenciales y setea cookie `auth_token` (httpOnly)
3. **Middleware:** Lee cookie y protege rutas privadas
4. **Logout:** Backend limpia cookie

### Rutas

| Ruta | Tipo | Acceso |
|------|------|--------|
| `/` | Privada | Requiere auth |
| `/login` | Pública | Solo sin auth |
| `/register` | Pública | Solo sin auth |
| `/chats` | Privada | Requiere auth |

## 🎨 Diseño

- **Framework CSS:** Tailwind CSS v3
- **Fuentes:** Inter (Google Fonts)
- **Paleta de colores:**
  - Primary: Blue-600 (login)
  - Secondary: Purple-600 (register)
  - Background: Gradientes suaves

## 🔗 Integración con Backend

El frontend se conecta al backend FastAPI en:
- **Development:** `http://localhost:8000`
- **Production:** Variable `NEXT_PUBLIC_API_URL`

### Variables de Entorno

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## 📦 Dependencias Principales

```json
{
  "dependencies": {
    "next": "14.2.30",
    "react": "^18",
    "react-dom": "^18",
    "zustand": "^5.0.2",
    "@tanstack/react-query": "^5.62.11"
  }
}
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando se implementen)
npm test

# Lint
npm run lint
```

## 🚢 Deployment (Vercel)

```bash
# El proyecto está configurado para deployment en Vercel
vercel

# O conectar repo de GitHub y deployment automático
```

## ⚠️ Notas Importantes

1. **Server vs Client Components:**
   - Por defecto, todos los componentes son **Server Components**
   - Solo usa `'use client'` cuando necesites: useState, useEffect, event handlers
   - Ejemplo: Formularios de login/register son Client Components

2. **Middleware:**
   - Protege todas las rutas excepto `/login`, `/register`, `/reset-password`
   - Lee cookies httpOnly (NO localStorage)
   - Redirige automáticamente según estado de autenticación

3. **API Calls:**
   - Todas las llamadas usan `credentials: 'include'` para cookies
   - Utilizar helpers de `lib/api.ts` para consistencia

4. **Turbopack:**
   - Habilitado por defecto en desarrollo (`npm run dev`)
   - ~5x más rápido que Webpack

## 📚 Próximas Implementaciones

- [ ] Chat interface con streaming SSE (TAREA 8)
- [ ] Subida de documentos
- [ ] Gestión de múltiples chats
- [ ] Configuración de usuario
