import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Next.js Middleware para autenticación basada en cookies httpOnly.
 * 
 * ✅ GOTCHA 10: Usa cookies httpOnly en vez de localStorage
 * para que funcione con Server Components.
 * 
 * Protege rutas privadas y redirige según estado de autenticación.
 */
export function middleware(request: NextRequest) {
  // Leer cookie httpOnly desde el request
  const token = request.cookies.get('auth_token')?.value

  // Definir rutas públicas (accesibles sin autenticación)
  const publicPaths = ['/login', '/register', '/reset-password']
  const isPublicPath = publicPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  // Si no hay token y la ruta es privada → redirect a /login
  if (!token && !isPublicPath) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', request.nextUrl.pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Si hay token y está en página de login → redirect a /
  if (token && isPublicPath) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}

// Configuración de rutas que pasan por el middleware
export const config = {
  // Excluir: API routes, archivos estáticos, imágenes, favicon
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
