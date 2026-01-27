---
name: python-patterns
description: Principios de desarrollo Python y toma de decisiones. Selección de framework, patrones async, type hints, estructura de proyecto. Enseña a pensar, no a copiar.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Patrones Python

> Principios de desarrollo Python y toma de decisiones para 2025.
> **Aprende a PENSAR, no memorizar patrones.**

---

## ⚠️ Cómo Usar Esta Skill

Esta skill enseña **principios de toma de decisiones**, no código fijo para copiar.

- PREGUNTAR al usuario por preferencia de framework cuando no esté claro
- Elegir async vs sync basado en CONTEXTO
- No usar por defecto el mismo framework cada vez

---

## 1. Selección de Framework (2025)

### Árbol de Decisión

```
¿Qué estás construyendo?
│
├── API-first / Microservicios
│   └── FastAPI (async, moderno, rápido)
│
├── Full-stack web / CMS / Admin
│   └── Django (baterías incluidas)
│
├── Simple / Script / Aprendizaje
│   └── Flask (mínimo, flexible)
│
├── API de servicio AI/ML
│   └── FastAPI (Pydantic, async, uvicorn)
│
└── Trabajadores en background
    └── Celery + cualquier framework
```

### Principios de Comparación

| Factor | FastAPI | Django | Flask |
|--------|---------|--------|-------|
| **Mejor para** | APIs, microservicios | Full-stack, CMS | Simple, aprendizaje |
| **Async** | Nativo | Django 5.0+ | Vía extensiones |
| **Admin** | Manual | Integrado | Vía extensiones |
| **ORM** | Elige el tuyo | Django ORM | Elige el tuyo |
| **Curva de aprendizaje** | Baja | Media | Baja |

### Preguntas de Selección a Hacer:
1. ¿Esto es solo API o full-stack?
2. ¿Necesitas interfaz de admin?
3. ¿El equipo está familiarizado con async?
4. ¿Infraestructura existente?

---

## 2. Decisión Async vs Sync

### Cuándo Usar Async

```
async def es mejor cuando:
├── Operaciones I/O-bound (base de datos, HTTP, archivo)
├── Muchas conexiones concurrentes
├── Características en tiempo real
├── Comunicación de microservicios
└── FastAPI/Starlette/Django ASGI

def (sync) es mejor cuando:
├── Operaciones CPU-bound
├── Scripts simples
├── Codebase legacy
├── Equipo no familiarizado con async
└── Bibliotecas bloqueantes (sin versión async)
```

### La Regla de Oro

```
I/O-bound → async (esperando externo)
CPU-bound → sync + multiprocessing (computando)

No hacer:
├── Mezclar sync y async descuidadamente
├── Usar bibliotecas sync en código async
└── Forzar async para trabajo CPU
```

### Selección de Biblioteca Async

| Necesidad | Biblioteca Async |
|-----------|------------------|
| Cliente HTTP | httpx |
| PostgreSQL | asyncpg |
| Redis | aioredis / redis-py async |
| I/O de archivo | aiofiles |
| ORM de base de datos | SQLAlchemy 2.0 async, Tortoise |

---

## 3. Estrategia de Type Hints

### Cuándo Tipar

```
Siempre tipar:
├── Parámetros de función
├── Tipos de retorno
├── Atributos de clase
├── APIs públicas

Puede omitir:
├── Variables locales (dejar que la inferencia funcione)
├── Scripts únicos
├── Pruebas (usualmente)
```

### Patrones de Tipo Comunes

```python
# Estos son patrones, entiéndelos:

# Optional → podría ser None
from typing import Optional
def find_user(id: int) -> Optional[User]: ...

# Union → uno de múltiples tipos
def process(data: str | dict) -> None: ...

# Colecciones genéricas
def get_items() -> list[Item]: ...
def get_mapping() -> dict[str, int]: ...

# Callable
from typing import Callable
def apply(fn: Callable[[int], str]) -> str: ...
```

### Pydantic para Validación

```
Cuándo usar Pydantic:
├── Modelos request/response de API
├── Configuración/settings
├── Validación de datos
├── Serialización

Beneficios:
├── Validación en tiempo de ejecución
├── Esquema JSON auto-generado
├── Funciona con FastAPI nativamente
└── Mensajes de error claros
```

---

## 4. Principios de Estructura de Proyecto

### Selección de Estructura

```
Proyecto pequeño / Script:
├── main.py
├── utils.py
└── requirements.txt

API mediana:
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── schemas/
├── tests/
└── pyproject.toml

Aplicación grande:
├── src/
│   └── myapp/
│       ├── core/
│       ├── api/
│       ├── services/
│       ├── models/
│       └── ...
├── tests/
└── pyproject.toml
```

### Principios de Estructura FastAPI

```
Organizar por característica o capa:

Por capa:
├── routes/ (endpoints API)
├── services/ (lógica de negocio)
├── models/ (modelos de base de datos)
├── schemas/ (modelos Pydantic)
└── dependencies/ (deps compartidas)

Por característica:
├── users/
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
└── products/
    └── ...
```

---

## 5. Principios Django (2025)

### Django Async (Django 5.0+)

```
Django soporta async:
├── Vistas async
├── Middleware async
├── ORM async (limitado)
└── Despliegue ASGI

Cuándo usar async en Django:
├── Llamadas a API externas
├── WebSocket (Channels)
├── Vistas de alta concurrencia
└── Activación de tareas en background
```

### Mejores Prácticas Django

```
Diseño de modelo:
├── Modelos gordos, vistas delgadas
├── Usar managers para consultas comunes
├── Clases base abstractas para campos compartidos

Vistas:
├── Basadas en clase para CRUD complejo
├── Basadas en función para endpoints simples
├── Usar viewsets con DRF

Consultas:
├── select_related() para FKs
├── prefetch_related() para M2M
├── Evitar consultas N+1
└── Usar .only() para campos específicos
```

---

## 6. Principios FastAPI

### async def vs def en FastAPI

```
Usar async def cuando:
├── Usando drivers de base de datos async
├── Haciendo llamadas HTTP async
├── Operaciones I/O-bound
└── Quieres manejar concurrencia

Usar def cuando:
├── Operaciones bloqueantes
├── Drivers de base de datos sync
├── Trabajo CPU-bound
└── FastAPI ejecuta en threadpool automáticamente
```

### Inyección de Dependencias

```
Usar dependencias para:
├── Sesiones de base de datos
├── Usuario actual / Auth
├── Configuración
├── Recursos compartidos

Beneficios:
├── Testabilidad (mockear dependencias)
├── Separación limpia
├── Limpieza automática (yield)
```

### Integración Pydantic v2

```python
# FastAPI + Pydantic están estrechamente integrados:

# Validación de request
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user ya está validado
    ...

# Serialización de response
# El tipo de retorno se convierte en esquema de response
```

---

## 7. Tareas en Background

### Guía de Selección

| Solución | Mejor Para |
|----------|------------|
| **BackgroundTasks** | Tareas simples, en-proceso |
| **Celery** | Distribuidas, flujos de trabajo complejos |
| **ARQ** | Async, basado en Redis |
| **RQ** | Cola Redis simple |
| **Dramatiq** | Basado en actores, más simple que Celery |

### Cuándo Usar Cada Uno

```
FastAPI BackgroundTasks:
├── Operaciones rápidas
├── No se necesita persistencia
├── Fire-and-forget
└── Mismo proceso

Celery/ARQ:
├── Tareas de larga duración
├── Necesitas lógica de reintento
├── Trabajadores distribuidos
├── Cola persistente
└── Flujos de trabajo complejos
```

---

## 8. Principios de Manejo de Errores

### Estrategia de Excepciones

```
En FastAPI:
├── Crear clases de excepción personalizadas
├── Registrar manejadores de excepciones
├── Devolver formato de error consistente
└── Registrar sin exponer internos

Patrón:
├── Lanzar excepciones de dominio en servicios
├── Capturar y transformar en manejadores
└── Cliente obtiene respuesta de error limpia
```

### Filosofía de Respuesta de Error

```
Incluir:
├── Código de error (programático)
├── Mensaje (legible por humanos)
├── Detalles (a nivel de campo cuando aplicable)
└── NO stack traces (seguridad)
```

---

## 9. Principios de Pruebas

### Estrategia de Pruebas

| Tipo | Propósito | Herramientas |
|------|-----------|--------------|
| **Unit** | Lógica de negocio | pytest |
| **Integration** | Endpoints API | pytest + httpx/TestClient |
| **E2E** | Flujos de trabajo completos | pytest + DB |

### Pruebas Async

```python
# Usar pytest-asyncio para pruebas async

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

### Estrategia de Fixtures

```
Fixtures comunes:
├── db_session → Conexión de base de datos
├── client → Cliente de prueba
├── authenticated_user → Usuario con token
└── sample_data → Configuración de datos de prueba
```

---

## 10. Lista de Verificación de Decisión

Antes de implementar:

- [ ] **¿Preguntaste al usuario sobre preferencia de framework?**
- [ ] **¿Elegiste framework para ESTE contexto?** (no solo por defecto)
- [ ] **¿Decidiste async vs sync?**
- [ ] **¿Planificaste estrategia de type hints?**
- [ ] **¿Definiste estructura de proyecto?**
- [ ] **¿Planificaste manejo de errores?**
- [ ] **¿Consideraste tareas en background?**

---

## 11. Anti-Patrones a Evitar

### ❌ NO HACER:
- Usar Django por defecto para APIs simples (FastAPI puede ser mejor)
- Usar bibliotecas sync en código async
- Omitir type hints para APIs públicas
- Poner lógica de negocio en routes/views
- Ignorar consultas N+1
- Mezclar async y sync descuidadamente

### ✅ HACER:
- Elegir framework basado en contexto
- Preguntar sobre requisitos async
- Usar Pydantic para validación
- Separar preocupaciones (routes → services → repos)
- Probar rutas críticas

---

> **Recuerda**: Los patrones Python son sobre toma de decisiones para TU contexto específico. No copies código—piensa en qué sirve mejor a tu aplicación.

## Ejemplos de Uso

### Ejemplo 1: Elegir el Framework Correcto para tu Proyecto
**Situación**: Quieres crear una API pero no sabes si usar FastAPI, Django o Flask.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una API para mi aplicación, ¿qué framework de Python debería usar?"
2. Cursor usará esta skill para:
   - Hacerte preguntas sobre tu proyecto (¿solo API o full-stack? ¿necesitas admin?)
   - Usar el árbol de decisión para recomendarte el framework apropiado
   - Explicar por qué ese framework es mejor para tu caso específico
   - No usar siempre el mismo framework, sino elegir basado en contexto

**Resultado**: El framework correcto para tu proyecto, no solo el más popular, asegurando que tu aplicación tenga las herramientas adecuadas.

### Ejemplo 2: Decidir si Usar Async o Sync
**Situación**: Estás escribiendo código Python y no sabes si debería ser async o sync.

**Cómo usar esta skill**:
1. Di a Cursor: "No sé si mi función debería ser async o sync"
2. Cursor evaluará:
   - Si tu función hace I/O (base de datos, HTTP) → async es mejor
   - Si hace trabajo CPU-intensivo → sync es mejor
   - El contexto de tu aplicación (FastAPI async, Django puede ser ambos)
   - Te guiará en la decisión correcta

**Resultado**: Código que usa async/sync apropiadamente, mejorando el rendimiento y evitando problemas de mezclar ambos incorrectamente.

### Ejemplo 3: Estructurar un Proyecto Python Correctamente
**Situación**: Estás empezando un nuevo proyecto Python y quieres organizarlo bien desde el inicio.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un proyecto FastAPI pero no sé cómo estructurarlo"
2. Cursor creará:
   - Una estructura de proyecto apropiada para el tamaño de tu aplicación
   - Organización por capas o por características según lo que funcione mejor
   - Separación clara de responsabilidades (routes, services, models)
   - Estructura que escala bien cuando el proyecto crece

**Resultado**: Un proyecto bien organizado desde el inicio, fácil de mantener y extender cuando crezca.
