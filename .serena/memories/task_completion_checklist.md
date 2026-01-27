# Checklist de Completitud de Tareas

## Cuando Completas UNA Tarea

### Validación en 3 Niveles (OBLIGATORIA)

#### Nivel 1: Sintaxis & Estilo

**Backend (Python):**
```bash
# Ejecutar PRIMERO - arreglar errores antes de proceder
ruff check backend/src/ --fix
mypy backend/src/

# Esperado: Sin errores. Si hay errores, LEER y ARREGLAR
```

**Frontend (TypeScript):**
```bash
cd frontend
npx eslint app/ --fix
npx tsc --noEmit

# Esperado: Sin errores. Si hay errores, LEER y ARREGLAR
```

**Criterio de éxito:**
- [ ] Sin errores de linting
- [ ] Sin errores de tipos
- [ ] Código formateado correctamente

#### Nivel 2: Tests Unitarios

**Backend:**
```bash
# Ejecutar tests de la tarea
docker compose exec backend pytest tests/test_<nombre_tarea>.py -v

# Con cobertura
docker compose exec backend pytest tests/ -v --cov=src --cov-report=html

# Esperado: Todos los tests pasan, cobertura >80%
```

**Frontend:**
```bash
cd frontend
npm test -- --coverage

# Esperado: Todos los tests pasan, cobertura >80%
```

**Criterio de éxito:**
- [ ] Todos los tests pasan
- [ ] Cobertura >80% en archivos nuevos/modificados
- [ ] Tests relevantes creados para la funcionalidad

**IMPORTANTE:**
- Si tests fallan: LEER el error, ENTENDER la causa, ARREGLAR la implementación
- NO modificar tests para que pasen si la implementación está mal
- RE-EJECUTAR tests hasta que todos pasen

#### Nivel 3: Test de Integración (si aplica)

**Para tareas que involucran API:**
```bash
# 1. Iniciar servicios
docker compose up -d

# 2. Ejecutar curl de prueba (según tarea)
# Ejemplo para auth:
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","full_name":"Test","project_id":"<uuid>"}'

# 3. Verificar respuesta esperada
# 4. Revisar logs si hay error
docker compose logs backend
```

**Para tareas de frontend:**
```bash
# 1. Abrir frontend
open http://localhost:3000

# 2. Test manual del flujo
# 3. Verificar UI responsive (mobile + desktop)
# 4. Verificar interacciones funcionan
```

**Criterio de éxito:**
- [ ] Flujo completo funciona end-to-end
- [ ] API responde correctamente
- [ ] Frontend muestra datos correctos
- [ ] Sin errores en logs

---

### Verificación Específica por Tipo de Tarea

#### Si modificaste Backend:

- [ ] Tests unitarios creados/actualizados
- [ ] ruff + mypy sin errores
- [ ] Pydantic schemas validados
- [ ] Endpoints documentados en docstrings
- [ ] project_id incluido en queries sensibles
- [ ] Manejo de errores implementado
- [ ] Logs informativos añadidos

#### Si modificaste Frontend:

- [ ] Componentes tipados correctamente
- [ ] 'use client' solo si necesario
- [ ] UI responsive (mobile + desktop)
- [ ] Loading states implementados
- [ ] Error handling implementado
- [ ] Accesibilidad básica (aria-labels)

#### Si modificaste Base de Datos:

- [ ] Migración creada y probada
- [ ] Índices en columnas filtradas
- [ ] RLS configurado correctamente
- [ ] Constraints de FK añadidos
- [ ] project_id incluido en tabla
- [ ] Timestamps (created_at, updated_at) incluidos

#### Si creaste Agente IA:

- [ ] Herramientas (tools) con descripciones claras
- [ ] Input/output bien definidos
- [ ] Memoria integrada correctamente
- [ ] Busca en documentos del usuario cuando relevante
- [ ] Busca en knowledge base global
- [ ] Respuestas coherentes con contexto
- [ ] Streaming funcional (si aplica)

---

### Actualización de TODOs

```bash
# Después de validación exitosa:
TodoWrite([
  {
    id: "task-N",
    status: "completed"
  }
], merge=true)
```

**Solo marcar como completado si:**
- [ ] 3 niveles de validación pasados
- [ ] Criterios de aceptación del PRP cumplidos
- [ ] Sin errores críticos en logs
- [ ] Funcionalidad probada manualmente

---

### Documentación (si aplica)

- [ ] README actualizado (si cambios importantes)
- [ ] API docs actualizados (nuevos endpoints)
- [ ] Comentarios añadidos (lógica compleja)
- [ ] GOTCHAS documentados (problemas encontrados)

---

### Antes de Continuar a Siguiente Tarea

**Checklist Final:**
1. [ ] Validación 3 niveles completada
2. [ ] TODO actualizado a "completed"
3. [ ] Sin errores en logs
4. [ ] Funcionalidad probada
5. [ ] Listo para siguiente tarea

**Si algo falla:**
- NO marcar como completado
- Anotar problemas encontrados
- Arreglar antes de continuar
- Re-ejecutar validación completa

---

## Anti-Patrones a Evitar

❌ **NO saltar validación** porque "debería funcionar"
❌ **NO ignorar tests fallidos**
❌ **NO marcar TODO como completado** sin validar
❌ **NO declarar completitud** sin evidencia ejecutable
❌ **NO pasar a siguiente tarea** con errores pendientes