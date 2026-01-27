---
name: test-fixing
description: Ejecutar pruebas y arreglar sistemáticamente todas las pruebas que fallan usando agrupación inteligente de errores. Usar cuando el usuario pide arreglar pruebas que fallan, menciona fallos de pruebas, ejecuta suite de pruebas y ocurren fallos, o solicita hacer que las pruebas pasen.
---

# Arreglar Pruebas

Identificar y arreglar sistemáticamente todas las pruebas que fallan usando estrategias de agrupación inteligente.

## Cuándo Usar

- Pide explícitamente arreglar pruebas ("arregla estas pruebas", "haz que las pruebas pasen")
- Reporta fallos de pruebas ("las pruebas están fallando", "la suite de pruebas está rota")
- Completa implementación y quiere que las pruebas pasen
- Menciona fallos de CI/CD debido a pruebas

## Enfoque Sistemático

### 1. Ejecución Inicial de Pruebas

Ejecutar `make test` para identificar todas las pruebas que fallan.

Analizar salida para:

- Número total de fallos
- Tipos de error y patrones
- Módulos/archivos afectados

### 2. Agrupación Inteligente de Errores

Agrupar fallos similares por:

- **Tipo de error**: ImportError, AttributeError, AssertionError, etc.
- **Módulo/archivo**: Mismo archivo causando múltiples fallos de prueba
- **Causa raíz**: Dependencias faltantes, cambios de API, impactos de refactorización

Priorizar grupos por:

- Número de pruebas afectadas (mayor impacto primero)
- Orden de dependencias (arreglar infraestructura antes de funcionalidad)

### 3. Proceso Sistemático de Arreglo

Para cada grupo (comenzando con mayor impacto):

1. **Identificar causa raíz**

   - Leer código relevante
   - Verificar cambios recientes con `git diff`
   - Entender el patrón de error

2. **Implementar corrección**

   - Usar herramienta Edit para cambios de código
   - Seguir convenciones del proyecto (ver CLAUDE.md)
   - Hacer cambios mínimos y enfocados

3. **Verificar corrección**

   - Ejecutar subconjunto de pruebas para este grupo
   - Usar marcadores pytest o patrones de archivo:
     ```bash
     uv run pytest tests/path/to/test_file.py -v
     uv run pytest -k "pattern" -v
     ```
   - Asegurar que el grupo pasa antes de continuar

4. **Mover al siguiente grupo**

### 4. Estrategia de Orden de Arreglo

**Infraestructura primero:**

- Errores de importación
- Dependencias faltantes
- Problemas de configuración

**Luego cambios de API:**

- Cambios de firma de función
- Reorganización de módulos
- Variables/funciones renombradas

**Finalmente, problemas de lógica:**

- Fallos de aserción
- Bugs de lógica de negocio
- Manejo de casos límite

### 5. Verificación Final

Después de que todos los grupos estén arreglados:

- Ejecutar suite completa de pruebas: `make test`
- Verificar sin regresiones
- Verificar que la cobertura de pruebas permanece intacta

## Mejores Prácticas

- Arreglar un grupo a la vez
- Ejecutar pruebas enfocadas después de cada corrección
- Usar `git diff` para entender cambios recientes
- Buscar patrones en los fallos
- No mover al siguiente grupo hasta que el actual pase
- Mantener cambios mínimos y enfocados

## Ejemplo de Flujo de Trabajo

Usuario: "Las pruebas están fallando después de mi refactorización"

1. Ejecutar `make test` → 15 fallos identificados
2. Agrupar errores:
   - 8 ImportErrors (módulo renombrado)
   - 5 AttributeErrors (firma de función cambiada)
   - 2 AssertionErrors (bugs de lógica)
3. Arreglar ImportErrors primero → Ejecutar subconjunto → Verificar
4. Arreglar AttributeErrors → Ejecutar subconjunto → Verificar
5. Arreglar AssertionErrors → Ejecutar subconjunto → Verificar
6. Ejecutar suite completa → Todas pasan ✓

## Ejemplos de Uso

### Ejemplo 1: Arreglar Pruebas que Fallan Después de un Cambio
**Situación**: Hiciste un cambio en tu código y ahora muchas pruebas están fallando, pero no sabes por dónde empezar.

**Cómo usar esta skill**:
1. Di a Cursor: "Las pruebas están fallando después de mi cambio, necesito arreglarlas"
2. Cursor usará esta skill para:
   - Ejecutar todas las pruebas y ver cuántas fallan
   - Agrupar los errores por tipo (errores de importación, errores de lógica, etc.)
   - Arreglar los grupos uno por uno, empezando por los que afectan más pruebas
   - Verificar que cada grupo pasa antes de continuar con el siguiente

**Resultado**: Todas las pruebas arregladas de forma organizada, sin perder tiempo arreglando cosas al azar.

### Ejemplo 2: Arreglar Pruebas Después de una Refactorización
**Situación**: Refactorizaste tu código (cambiaste nombres de funciones, reorganizaste archivos) y ahora las pruebas no funcionan.

**Cómo usar esta skill**:
1. Di a Cursor: "Refactoricé mi código y ahora las pruebas fallan, necesito arreglarlas sistemáticamente"
2. Cursor implementará:
   - Agrupación inteligente que identifica que muchos errores son del mismo tipo (por ejemplo, funciones renombradas)
   - Arreglo de todos los errores de ese tipo de una vez
   - Verificación después de cada grupo
   - Continuación con el siguiente tipo de error

**Resultado**: Pruebas arregladas eficientemente, agrupando trabajos similares en lugar de arreglar uno por uno.

### Ejemplo 3: Hacer que Todas las Pruebas Pasen Antes de un Commit
**Situación**: Quieres hacer commit de tu código pero algunas pruebas están fallando y necesitas arreglarlas primero.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito que todas las pruebas pasen antes de hacer commit"
2. Cursor:
   - Ejecutará todas las pruebas para ver el estado completo
   - Identificará todos los fallos y los agrupará
   - Arreglará sistemáticamente cada grupo
   - Verificará que todas las pruebas pasan al final

**Resultado**: Suite de pruebas completamente funcional, lista para commit con confianza de que todo funciona.
