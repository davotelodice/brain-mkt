---
name: executing-plans
description: Usar cuando tienes un plan de implementación escrito para ejecutar en una sesión separada con puntos de control de revisión
---

# Ejecutar Planes

## Resumen

Cargar plan, revisar críticamente, ejecutar tareas en lotes, reportar para revisión entre lotes.

**Principio central:** Ejecución por lotes con puntos de control para revisión de arquitecto.

**Anunciar al inicio:** "Estoy usando la skill executing-plans para implementar este plan."

## El Proceso

### Paso 1: Cargar y Revisar Plan
1. Leer archivo de plan
2. Revisar críticamente - identificar cualquier pregunta o preocupación sobre el plan
3. Si hay preocupaciones: Elevarlas con tu compañero humano antes de comenzar
4. Si no hay preocupaciones: Crear TodoWrite y proceder

### Paso 2: Ejecutar Lote
**Por defecto: Primeras 3 tareas**

Para cada tarea:
1. Marcar como in_progress
2. Seguir cada paso exactamente (el plan tiene pasos pequeños)
3. Ejecutar verificaciones como se especifica
4. Marcar como completada

### Paso 3: Reportar
Cuando el lote esté completo:
- Mostrar lo que se implementó
- Mostrar salida de verificación
- Decir: "Listo para retroalimentación."

### Paso 4: Continuar
Basado en retroalimentación:
- Aplicar cambios si es necesario
- Ejecutar siguiente lote
- Repetir hasta completar

### Paso 5: Completar Desarrollo

Después de que todas las tareas estén completas y verificadas:
- Anunciar: "Estoy usando la skill finishing-a-development-branch para completar este trabajo."
- **REQUIRED SUB-SKILL:** Usar superpowers:finishing-a-development-branch
- Seguir esa skill para verificar pruebas, presentar opciones, ejecutar elección

## Cuándo Detener y Pedir Ayuda

**DETENER ejecución inmediatamente cuando:**
- Encuentras un bloqueador a mitad del lote (dependencia faltante, prueba falla, instrucción poco clara)
- El plan tiene brechas críticas que previenen comenzar
- No entiendes una instrucción
- La verificación falla repetidamente

**Pedir aclaración en lugar de adivinar.**

## Cuándo Revisitar Pasos Anteriores

**Volver a Revisar (Paso 1) cuando:**
- El compañero actualiza el plan basado en tu retroalimentación
- El enfoque fundamental necesita reconsideración

**No forzar a través de bloqueadores** - detener y preguntar.

## Recordar

- Revisar plan críticamente primero
- Seguir pasos del plan exactamente
- No omitir verificaciones
- Referenciar skills cuando el plan lo dice
- Entre lotes: solo reportar y esperar
- Detener cuando bloqueado, no adivinar

## Ejemplos de Uso

### Ejemplo 1: Ejecutar un Plan de Implementación Paso a Paso
**Situación**: Tienes un plan detallado para agregar una característica y quieres ejecutarlo de forma organizada con revisiones periódicas.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo un plan en docs/plans/feature-auth.md, quiero ejecutarlo"
2. Cursor usará esta skill para:
   - Leer y revisar el plan críticamente primero
   - Ejecutar las primeras 3 tareas del plan
   - Verificar que cada paso funciona correctamente
   - Reportar el progreso y esperar tu retroalimentación
   - Continuar con el siguiente lote después de tu aprobación

**Resultado**: Implementación organizada con puntos de control donde puedes revisar el progreso y hacer ajustes antes de continuar.

### Ejemplo 2: Implementar un Plan Complejo con Múltiples Fases
**Situación**: Tienes un plan grande con muchas tareas y quieres ejecutarlo de forma sistemática sin perder el control.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero ejecutar este plan complejo pero necesito hacerlo en lotes para revisar"
2. Cursor implementará:
   - Ejecución en lotes de 3 tareas a la vez
   - Verificación después de cada lote
   - Reporte claro de lo que se completó
   - Pausa para tu revisión antes de continuar
   - Detención automática si encuentra problemas

**Resultado**: Un proceso controlado donde puedes supervisar el progreso y asegurarte de que todo funciona antes de continuar con más tareas.

### Ejemplo 3: Reanudar un Plan Después de una Pausa
**Situación**: Comenzaste a ejecutar un plan pero tuviste que pausar, y ahora quieres continuar donde te quedaste.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero continuar ejecutando el plan desde donde lo dejé"
2. Cursor:
   - Cargará el plan y verá qué tareas ya están completadas
   - Continuará desde la siguiente tarea pendiente
   - Ejecutará el siguiente lote de tareas
   - Mantendrá el progreso actualizado

**Resultado**: Continuación fluida del trabajo sin perder progreso ni repetir tareas ya completadas.
