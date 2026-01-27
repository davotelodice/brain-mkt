---
name: database-design
description: Principios de diseño de bases de datos y toma de decisiones. Diseño de esquema, estrategia de indexación, selección de ORM, bases de datos serverless.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Diseño de Bases de Datos

> **Aprende a PENSAR, no copiar patrones SQL.**

## 🎯 Regla de Lectura Selectiva

**¡Lee SOLO archivos relevantes a la solicitud!** Revisa el mapa de contenido, encuentra lo que necesitas.

| Archivo | Descripción | Cuándo Leer |
|---------|-------------|-------------|
| `database-selection.md` | PostgreSQL vs Neon vs Turso vs SQLite | Elegir base de datos |
| `orm-selection.md` | Drizzle vs Prisma vs Kysely | Elegir ORM |
| `schema-design.md` | Normalización, PKs, relaciones | Diseñar esquema |
| `indexing.md` | Tipos de índice, índices compuestos | Ajuste de rendimiento |
| `optimization.md` | N+1, EXPLAIN ANALYZE | Optimización de consultas |
| `migrations.md` | Migraciones seguras, DBs serverless | Cambios de esquema |

---

## ⚠️ Principio Central

- PREGUNTAR al usuario sobre preferencias de base de datos cuando no esté claro
- Elegir base de datos/ORM basado en CONTEXTO
- No usar PostgreSQL por defecto para todo

---

## Lista de Verificación de Decisión

Antes de diseñar esquema:

- [ ] ¿Preguntaste al usuario sobre preferencia de base de datos?
- [ ] ¿Elegiste base de datos para ESTE contexto?
- [ ] ¿Consideraste entorno de deployment?
- [ ] ¿Planificaste estrategia de índices?
- [ ] ¿Definiste tipos de relaciones?

---

## Anti-Patrones

❌ Usar PostgreSQL por defecto para apps simples (SQLite puede bastar)
❌ Omitir indexación
❌ Usar SELECT * en producción
❌ Almacenar JSON cuando datos estructurados son mejores
❌ Ignorar consultas N+1

## Ejemplos de Uso

### Ejemplo 1: Elegir la Base de Datos Correcta para tu Proyecto
**Situación**: Estás empezando un nuevo proyecto y no sabes qué base de datos usar.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito elegir una base de datos para mi proyecto"
2. Cursor usará esta skill para:
   - Preguntarte sobre tus necesidades específicas
   - Considerar tu entorno de deployment
   - Recomendar la base de datos apropiada (PostgreSQL, Neon, Turso, SQLite)
   - Explicar por qué esa elección es correcta para tu contexto

**Resultado**: Elección informada de base de datos que se adapta a tus necesidades específicas.

### Ejemplo 2: Diseñar el Esquema de tu Base de Datos
**Situación**: Necesitas diseñar el esquema de tu base de datos pero no sabes cómo estructurarlo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero diseñar el esquema de mi base de datos"
2. Cursor:
   - Te ayudará a normalizar tus datos apropiadamente
   - Diseñará relaciones entre tablas
   - Planificará estrategia de índices
   - Aplicará mejores prácticas de diseño

**Resultado**: Un esquema de base de datos bien diseñado que es eficiente y fácil de mantener.

### Ejemplo 3: Optimizar Consultas Lentas
**Situación**: Tienes consultas que son lentas y quieres optimizarlas.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo consultas lentas, quiero optimizarlas"
2. Cursor:
   - Identificará problemas N+1
   - Sugerirá índices apropiados
   - Optimizará consultas usando EXPLAIN ANALYZE
   - Aplicará técnicas de optimización

**Resultado**: Consultas optimizadas que se ejecutan mucho más rápido.
