---
name: code-review-checklist
description: "Lista de verificación comprehensiva para realizar revisiones de código exhaustivas cubriendo funcionalidad, seguridad, rendimiento y mantenibilidad"
---

# Lista de Verificación de Revisión de Código

## Resumen

Proporcionar una lista de verificación sistemática para realizar revisiones de código exhaustivas. Esta skill ayuda a los revisores a asegurar calidad de código, atrapar bugs, identificar problemas de seguridad y mantener consistencia a través del codebase.

## Cuándo Usar Esta Skill

- Usar al revisar pull requests
- Usar al realizar auditorías de código
- Usar al establecer estándares de revisión de código para un equipo
- Usar al entrenar nuevos desarrolladores en prácticas de revisión de código
- Usar cuando quieras asegurar que nada se pase por alto en revisiones
- Usar al crear documentación de revisión de código

## Cómo Funciona

### Paso 1: Entender el Contexto

Antes de revisar código, te ayudaré a entender:
- ¿Qué problema resuelve este código?
- ¿Cuáles son los requisitos?
- ¿Qué archivos cambiaron y por qué?
- ¿Hay issues o tickets relacionados?
- ¿Cuál es la estrategia de pruebas?

### Paso 2: Revisar Funcionalidad

Verificar si el código funciona correctamente:
- ¿Resuelve el problema declarado?
- ¿Se manejan casos límite?
- ¿El manejo de errores es apropiado?
- ¿Hay errores lógicos?
- ¿Coincide con los requisitos?

### Paso 3: Revisar Calidad de Código

Evaluar mantenibilidad del código:
- ¿El código es legible y claro?
- ¿Los nombres son descriptivos?
- ¿Está apropiadamente estructurado?
- ¿Las funciones/métodos están enfocados?
- ¿Hay complejidad innecesaria?

### Paso 4: Revisar Seguridad

Verificar problemas de seguridad:
- ¿Se validan las entradas?
- ¿Se protegen datos sensibles?
- ¿Hay riesgos de inyección SQL?
- ¿La autenticación/autorización es correcta?
- ¿Las dependencias son seguras?

### Paso 5: Revisar Rendimiento

Buscar problemas de rendimiento:
- ¿Hay loops innecesarios?
- ¿El acceso a base de datos está optimizado?
- ¿Hay memory leaks?
- ¿Se usa caché apropiadamente?
- ¿Hay problemas de consultas N+1?

### Paso 6: Revisar Pruebas

Verificar cobertura de pruebas:
- ¿Hay pruebas para código nuevo?
- ¿Las pruebas cubren casos límite?
- ¿Las pruebas son significativas?
- ¿Todas las pruebas pasan?
- ¿La cobertura de pruebas es adecuada?

## Ejemplos

### Ejemplo 1: Lista de Verificación de Revisión de Funcionalidad

```markdown
## Revisión de Funcionalidad

### Requisitos
- [ ] El código resuelve el problema declarado
- [ ] Todos los criterios de aceptación se cumplen
- [ ] Se manejan casos límite
- [ ] Se manejan casos de error
- [ ] La entrada del usuario está validada

### Lógica
- [ ] Sin errores lógicos o bugs
- [ ] Las condiciones son correctas (sin errores off-by-one)
- [ ] Los loops terminan correctamente
- [ ] La recursión tiene casos base apropiados
- [ ] La gestión de estado es correcta

### Manejo de Errores
- [ ] Los errores se capturan apropiadamente
- [ ] Los mensajes de error son claros y útiles
- [ ] Los errores no exponen información sensible
- [ ] Las operaciones fallidas se revierten
- [ ] El logging es apropiado
```

## Ejemplos de Uso

### Ejemplo 1: Revisar un Pull Request Completo
**Situación**: Tienes un pull request que necesitas revisar y quieres asegurarte de no pasar nada por alto.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito revisar este pull request usando una lista de verificación completa"
2. Cursor usará esta skill para:
   - Revisar funcionalidad (¿resuelve el problema?)
   - Revisar calidad de código (¿es mantenible?)
   - Revisar seguridad (¿hay vulnerabilidades?)
   - Revisar rendimiento (¿hay problemas?)
   - Revisar pruebas (¿están cubiertas?)
   - Darte un reporte completo de todos los aspectos

**Resultado**: Una revisión exhaustiva que cubre todos los aspectos importantes, asegurando que el código es de alta calidad antes de hacer merge.

### Ejemplo 2: Establecer Estándares de Revisión para tu Equipo
**Situación**: Quieres crear una lista de verificación estándar que tu equipo use para todas las revisiones.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una lista de verificación de revisión de código para mi equipo"
2. Cursor:
   - Te proporcionará una lista de verificación comprehensiva
   - Incluirá todas las categorías importantes (funcionalidad, seguridad, rendimiento, pruebas)
   - Puedes personalizarla para tu proyecto específico
   - La puedes usar como estándar para todas las revisiones

**Resultado**: Una lista de verificación estándar que asegura que todas las revisiones cubren los aspectos críticos.

### Ejemplo 3: Revisar Código para Problemas de Seguridad
**Situación**: Quieres hacer una revisión enfocada específicamente en seguridad.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero revisar este código específicamente para problemas de seguridad"
2. Cursor usará esta skill para:
   - Verificar validación de entrada
   - Buscar riesgos de inyección SQL
   - Verificar autenticación y autorización
   - Revisar manejo de datos sensibles
   - Identificar cualquier vulnerabilidad potencial

**Resultado**: Una revisión de seguridad exhaustiva que identifica y ayuda a corregir problemas de seguridad antes de que lleguen a producción.
