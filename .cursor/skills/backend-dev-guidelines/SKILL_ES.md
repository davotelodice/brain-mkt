---
name: backend-dev-guidelines
description: Guía comprehensiva de desarrollo backend para microservicios Node.js/Express/TypeScript. Usar al crear rutas, controladores, servicios, repositorios, middleware o trabajar con APIs Express, acceso a base de datos Prisma, seguimiento de errores Sentry, validación Zod, unifiedConfig, inyección de dependencias o patrones async. Cubre arquitectura en capas (routes → controllers → services → repositories), patrón BaseController, manejo de errores, monitoreo de rendimiento, estrategias de testing y migración desde patrones legacy.
---

# Guías de Desarrollo Backend

## Propósito

Establecer consistencia y mejores prácticas a través de microservicios backend (blog-api, auth-service, notifications-service) usando patrones modernos Node.js/Express/TypeScript.

## Cuándo Usar Esta Skill

Se activa automáticamente al trabajar en:
- Crear o modificar rutas, endpoints, APIs
- Construir controladores, servicios, repositorios
- Implementar middleware (auth, validación, manejo de errores)
- Operaciones de base de datos con Prisma
- Seguimiento de errores con Sentry
- Validación de entrada con Zod
- Gestión de configuración
- Testing y refactorización backend

---

## Inicio Rápido

### Lista de Verificación de Nueva Característica Backend

- [ ] **Route**: Definición limpia, delegar a controlador
- [ ] **Controller**: Extender BaseController
- [ ] **Service**: Lógica de negocio con DI
- [ ] **Repository**: Acceso a base de datos (si es complejo)
- [ ] **Validation**: Schema Zod
- [ ] **Sentry**: Seguimiento de errores
- [ ] **Tests**: Pruebas unitarias + integración
- [ ] **Config**: Usar unifiedConfig

### Lista de Verificación de Nuevo Microservicio

- [ ] Estructura de directorios (ver [architecture-overview.md](architecture-overview.md))
- [ ] instrument.ts para Sentry
- [ ] Configuración unifiedConfig
- [ ] Clase BaseController
- [ ] Stack de middleware
- [ ] Error boundary
- [ ] Framework de testing

---

## Resumen de Arquitectura

### Arquitectura en Capas

```
HTTP Request
    ↓
Routes (solo routing)
    ↓
Controllers (manejo de request)
    ↓
Services (lógica de negocio)
    ↓
Repositories (acceso a datos)
    ↓
Database (Prisma)
```

**Principio Clave:** Cada capa tiene UNA responsabilidad.

Ver [architecture-overview.md](architecture-overview.md) para detalles completos.

---

## Estructura de Directorios

```
service/src/
├── config/              # UnifiedConfig
├── controllers/         # Request handlers
├── services/            # Lógica de negocio
├── repositories/        # Acceso a datos
├── routes/              # Definiciones de ruta
├── middleware/          # Middleware Express
├── types/               # Tipos TypeScript
├── validators/          # Schemas Zod
├── utils/               # Utilidades
├── tests/               # Pruebas
├── instrument.ts        # Sentry (PRIMER IMPORT)
├── app.ts               # Configuración Express
└── server.ts            # Servidor HTTP
```

**Convenciones de Nomenclatura:**
- Controllers: `PascalCase` - `UserController.ts`
- Services: `camelCase` - `userService.ts`
- Routes: `camelCase + Routes` - `userRoutes.ts`
- Repositories: `PascalCase + Repository` - `UserRepository.ts`

---

## Principios Fundamentales (7 Reglas Clave)

### 1. Routes Solo Rutean, Controllers Controlan

```typescript
// ❌ NUNCA: Lógica de negocio en rutas
router.post('/submit', async (req, res) => {
    // 200 líneas de lógica
});

// ✅ SIEMPRE: Delegar a controlador
router.post('/submit', (req, res) => controller.submit(req, res));
```

### 2. Todos los Controllers Extienden BaseController

```typescript
export class UserController extends BaseController {
    async getUser(req: Request, res: Response): Promise<void> {
        try {
            const user = await this.userService.findById(req.params.id);
            this.handleSuccess(res, user);
        } catch (error) {
            this.handleError(error, res, 'getUser');
        }
    }
}
```

### 3. Todos los Errores a Sentry

```typescript
try {
    await operation();
} catch (error) {
    Sentry.captureException(error);
    throw error;
}
```

### 4. Usar unifiedConfig, NUNCA process.env

```typescript
// ❌ NUNCA
const timeout = process.env.TIMEOUT_MS;

// ✅ SIEMPRE
import { config } from './config/unifiedConfig';
const timeout = config.timeouts.default;
```

### 5. Validar Toda la Entrada con Zod

```typescript
const schema = z.object({ email: z.string().email() });
const validated = schema.parse(req.body);
```

### 6. Usar Patrón Repository para Acceso a Datos

```typescript
// Service → Repository → Database
const users = await userRepository.findActive();
```

### 7. Testing Comprehensivo Requerido

```typescript
describe('UserService', () => {
    it('should create user', async () => {
        expect(user).toBeDefined();
    });
});
```

---

## Imports Comunes

```typescript
// Express
import express, { Request, Response, NextFunction, Router } from 'express';

// Validación
import { z } from 'zod';

// Base de datos
import { PrismaClient } from '@prisma/client';
import type { Prisma } from '@prisma/client';

// Sentry
import * as Sentry from '@sentry/node';

// Config
import { config } from './config/unifiedConfig';

// Middleware
import { SSOMiddlewareClient } from './middleware/SSOMiddleware';
import { asyncErrorWrapper } from './middleware/errorBoundary';
```

---

## Referencia Rápida

### Códigos de Estado HTTP

| Código | Caso de Uso |
|--------|-------------|
| 200 | Éxito |
| 201 | Creado |
| 400 | Bad Request |
| 401 | No Autorizado |
| 403 | Prohibido |
| 404 | No Encontrado |
| 500 | Error del Servidor |

### Plantillas de Servicio

**Blog API** (✅ Maduro) - Usar como plantilla para APIs REST
**Auth Service** (✅ Maduro) - Usar como plantilla para patrones de autenticación

---

## Anti-Patrones a Evitar

❌ Lógica de negocio en rutas
❌ Uso directo de process.env
❌ Manejo de errores faltante
❌ Sin validación de entrada
❌ Prisma directo en todas partes
❌ console.log en lugar de Sentry

---

## Guía de Navegación

| Necesitas... | Lee esto |
|--------------|----------|
| Entender arquitectura | [architecture-overview.md](architecture-overview.md) |
| Crear rutas/controladores | [routing-and-controllers.md](routing-and-controllers.md) |
| Organizar lógica de negocio | [services-and-repositories.md](services-and-repositories.md) |
| Validar entrada | [validation-patterns.md](validation-patterns.md) |
| Agregar seguimiento de errores | [sentry-and-monitoring.md](sentry-and-monitoring.md) |
| Crear middleware | [middleware-guide.md](middleware-guide.md) |
| Acceso a base de datos | [database-patterns.md](database-patterns.md) |
| Gestionar config | [configuration.md](configuration.md) |
| Manejar async/errores | [async-and-errors.md](async-and-errors.md) |
| Escribir pruebas | [testing-guide.md](testing-guide.md) |
| Ver ejemplos | [complete-examples.md](complete-examples.md) |

---

## Archivos de Recursos

### [architecture-overview.md](architecture-overview.md)
Arquitectura en capas, ciclo de vida de request, separación de preocupaciones

### [routing-and-controllers.md](routing-and-controllers.md)
Definiciones de ruta, BaseController, manejo de errores, ejemplos

### [services-and-repositories.md](services-and-repositories.md)
Patrones de servicio, DI, patrón repository, caching

### [validation-patterns.md](validation-patterns.md)
Schemas Zod, validación, patrón DTO

### [sentry-and-monitoring.md](sentry-and-monitoring.md)
Inicialización Sentry, captura de errores, monitoreo de rendimiento

### [middleware-guide.md](middleware-guide.md)
Auth, audit, error boundaries, AsyncLocalStorage

### [database-patterns.md](database-patterns.md)
PrismaService, repositorios, transacciones, optimización

### [configuration.md](configuration.md)
UnifiedConfig, configs de entorno, secrets

### [async-and-errors.md](async-and-errors.md)
Patrones async, errores personalizados, asyncErrorWrapper

### [testing-guide.md](testing-guide.md)
Pruebas unitarias/integración, mocking, cobertura

### [complete-examples.md](complete-examples.md)
Ejemplos completos, guía de refactorización

---

## Skills Relacionadas

- **database-verification** - Verificar nombres de columna y consistencia de esquema
- **error-tracking** - Patrones de integración Sentry
- **skill-developer** - Meta-skill para crear y gestionar skills

---

**Estado de Skill**: COMPLETA ✅
**Conteo de Líneas**: < 500 ✅
**Divulgación Progresiva**: 11 archivos de recursos ✅

## Ejemplos de Uso

### Ejemplo 1: Crear un Nuevo Endpoint API
**Situación**: Quieres crear un nuevo endpoint API pero quieres asegurarte de seguir la arquitectura correcta.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un nuevo endpoint API siguiendo las guías de backend"
2. Cursor usará esta skill para:
   - Crear la ruta que solo delega al controlador
   - Crear un controlador que extiende BaseController
   - Crear un servicio con la lógica de negocio
   - Crear un repositorio para acceso a datos si es necesario
   - Agregar validación Zod para la entrada
   - Configurar Sentry para seguimiento de errores
   - Seguir la arquitectura en capas correctamente

**Resultado**: Un endpoint API bien estructurado que sigue todas las mejores prácticas, con código organizado y fácil de mantener.

### Ejemplo 2: Refactorizar Código Legacy a la Nueva Arquitectura
**Situación**: Tienes código antiguo con lógica de negocio en las rutas y quieres refactorizarlo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero refactorizar mi código legacy para seguir la arquitectura en capas"
2. Cursor:
   - Identificará código que viola los principios (lógica en rutas, etc.)
   - Moverá la lógica a servicios apropiados
   - Creará controladores que extienden BaseController
   - Separará acceso a datos en repositorios
   - Aplicará todas las mejores prácticas de la skill

**Resultado**: Código refactorizado que sigue la arquitectura moderna, más fácil de mantener y testear.

### Ejemplo 3: Crear un Nuevo Microservicio desde Cero
**Situación**: Necesitas crear un nuevo microservicio y quieres configurarlo correctamente desde el inicio.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un nuevo microservicio siguiendo las guías"
2. Cursor configurará:
   - La estructura de directorios completa
   - Sentry para seguimiento de errores
   - UnifiedConfig para configuración
   - BaseController para todos los controladores
   - Stack de middleware apropiado
   - Framework de testing
   - Todo siguiendo las mejores prácticas

**Resultado**: Un microservicio completamente configurado y listo para desarrollo, siguiendo todos los estándares del proyecto.
