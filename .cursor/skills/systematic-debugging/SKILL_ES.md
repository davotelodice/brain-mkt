---
name: systematic-debugging
description: Usar al encontrar cualquier bug, fallo de prueba o comportamiento inesperado, antes de proponer correcciones
---

# Debugging Sistemático

## Resumen

Las correcciones aleatorias desperdician tiempo y crean nuevos bugs. Los parches rápidos enmascaran problemas subyacentes.

**Principio central:** SIEMPRE encontrar la causa raíz antes de intentar correcciones. Las correcciones de síntomas son fallos.

**Violar la letra de este proceso es violar el espíritu del debugging.**

## La Ley de Hierro

```
NO HAY CORRECCIONES SIN INVESTIGACIÓN DE CAUSA RAÍZ PRIMERO
```

Si no has completado la Fase 1, no puedes proponer correcciones.

## Cuándo Usar

Usar para CUALQUIER problema técnico:
- Fallos de pruebas
- Bugs en producción
- Comportamiento inesperado
- Problemas de rendimiento
- Fallos de build
- Problemas de integración

**Usar esto ESPECIALMENTE cuando:**
- Bajo presión de tiempo (las emergencias hacen tentador adivinar)
- "Solo una corrección rápida" parece obvio
- Ya intentaste múltiples correcciones
- La corrección anterior no funcionó
- No entiendes completamente el problema

**No omitir cuando:**
- El problema parece simple (los bugs simples también tienen causas raíz)
- Tienes prisa (apresurarse garantiza re-trabajo)
- El manager quiere que se arregle AHORA (sistemático es más rápido que trastear)

## Las Cuatro Fases

DEBES completar cada fase antes de proceder a la siguiente.

### Fase 1: Investigación de Causa Raíz

**ANTES de intentar CUALQUIER corrección:**

1. **Leer Mensajes de Error Cuidadosamente**
   - No omitir errores o advertencias
   - A menudo contienen la solución exacta
   - Leer stack traces completamente
   - Notar números de línea, rutas de archivo, códigos de error

2. **Reproducir Consistentemente**
   - ¿Puedes activarlo de forma confiable?
   - ¿Cuáles son los pasos exactos?
   - ¿Pasa cada vez?
   - Si no es reproducible → recopilar más datos, no adivinar

3. **Verificar Cambios Recientes**
   - ¿Qué cambió que podría causar esto?
   - Git diff, commits recientes
   - Nuevas dependencias, cambios de configuración
   - Diferencias ambientales

4. **Recopilar Evidencia en Sistemas Multi-Componente**

   **CUANDO el sistema tiene múltiples componentes (CI → build → signing, API → service → database):**

   **ANTES de proponer correcciones, agregar instrumentación de diagnóstico:**
   ```
   Para CADA límite de componente:
     - Registrar qué datos entran al componente
     - Registrar qué datos salen del componente
     - Verificar propagación de entorno/config
     - Verificar estado en cada capa

   Ejecutar una vez para recopilar evidencia mostrando DÓNDE se rompe
   LUEGO analizar evidencia para identificar componente que falla
   LUEGO investigar ese componente específico
   ```

   **Ejemplo (sistema multi-capa):**
   ```bash
   # Capa 1: Workflow
   echo "=== Secrets disponibles en workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Capa 2: Script de build
   echo "=== Env vars en script de build: ==="
   env | grep IDENTITY || echo "IDENTITY no en entorno"

   # Capa 3: Script de signing
   echo "=== Estado de keychain: ==="
   security list-keychains
   security find-identity -v

   # Capa 4: Signing real
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **Esto revela:** Qué capa falla (secrets → workflow ✓, workflow → build ✗)

5. **Rastrear Flujo de Datos**

   **CUANDO el error está profundo en la pila de llamadas:**

   Ver `root-cause-tracing.md` en este directorio para la técnica completa de rastreo hacia atrás.

   **Versión rápida:**
   - ¿Dónde se origina el valor malo?
   - ¿Qué llamó esto con valor malo?
   - Seguir rastreando hacia arriba hasta encontrar la fuente
   - Arreglar en la fuente, no en el síntoma

### Fase 2: Análisis de Patrón

**Encontrar el patrón antes de arreglar:**

1. **Encontrar Ejemplos que Funcionan**
   - Localizar código similar que funciona en el mismo codebase
   - ¿Qué funciona que es similar a lo que está roto?

2. **Comparar Contra Referencias**
   - Si implementando patrón, leer implementación de referencia COMPLETAMENTE
   - No escanear - leer cada línea
   - Entender el patrón completamente antes de aplicar

3. **Identificar Diferencias**
   - ¿Qué es diferente entre lo que funciona y lo roto?
   - Listar cada diferencia, por pequeña que sea
   - No asumir "eso no puede importar"

4. **Entender Dependencias**
   - ¿Qué otros componentes necesita esto?
   - ¿Qué configuraciones, config, entorno?
   - ¿Qué suposiciones hace?

### Fase 3: Hipótesis y Pruebas

**Método científico:**

1. **Formar Hipótesis Única**
   - Declarar claramente: "Creo que X es la causa raíz porque Y"
   - Escribirlo
   - Ser específico, no vago

2. **Probar Mínimamente**
   - Hacer el cambio MÁS PEQUEÑO posible para probar hipótesis
   - Una variable a la vez
   - No arreglar múltiples cosas a la vez

3. **Verificar Antes de Continuar**
   - ¿Funcionó? Sí → Fase 4
   - ¿No funcionó? Formar NUEVA hipótesis
   - NO agregar más correcciones encima

4. **Cuando No Sabes**
   - Decir "No entiendo X"
   - No fingir saber
   - Pedir ayuda
   - Investigar más

### Fase 4: Implementación

**Arreglar la causa raíz, no el síntoma:**

1. **Crear Caso de Prueba que Falla**
   - Reproducción más simple posible
   - Prueba automatizada si es posible
   - Script de prueba único si no hay framework
   - DEBE tener antes de arreglar
   - Usar la skill `superpowers:test-driven-development` para escribir pruebas que fallan apropiadas

2. **Implementar Corrección Única**
   - Abordar la causa raíz identificada
   - UN cambio a la vez
   - Sin mejoras "mientras estoy aquí"
   - Sin refactorización agrupada

3. **Verificar Corrección**
   - ¿La prueba pasa ahora?
   - ¿No se rompieron otras pruebas?
   - ¿El problema realmente se resolvió?

4. **Si la Corrección No Funciona**
   - DETENER
   - Contar: ¿Cuántas correcciones has intentado?
   - Si < 3: Volver a Fase 1, re-analizar con nueva información
   - **Si ≥ 3: DETENER y cuestionar la arquitectura (paso 5 abajo)**
   - NO intentar Corrección #4 sin discusión arquitectónica

5. **Si 3+ Correcciones Fallaron: Cuestionar Arquitectura**

   **Patrón indicando problema arquitectónico:**
   - Cada corrección revela nuevo estado compartido/acoplamiento/problema en lugar diferente
   - Las correcciones requieren "refactorización masiva" para implementar
   - Cada corrección crea nuevos síntomas en otros lugares

   **DETENER y cuestionar fundamentos:**
   - ¿Este patrón es fundamentalmente sólido?
   - ¿Estamos "aferrándonos a él por pura inercia"?
   - ¿Deberíamos refactorizar arquitectura vs. continuar arreglando síntomas?

   **Discutir con tu compañero humano antes de intentar más correcciones**

   Esto NO es una hipótesis fallida - esto es una arquitectura incorrecta.

## Banderas Rojas - DETENER y Seguir Proceso

Si te encuentras pensando:
- "Corrección rápida por ahora, investigar después"
- "Solo probar cambiar X y ver si funciona"
- "Agregar múltiples cambios, ejecutar pruebas"
- "Omitir la prueba, verificaré manualmente"
- "Probablemente es X, déjame arreglar eso"
- "No entiendo completamente pero esto podría funcionar"
- "El patrón dice X pero lo adaptaré diferente"
- "Aquí están los problemas principales: [lista correcciones sin investigación]"
- Proponer soluciones antes de rastrear flujo de datos
- **"Un intento de corrección más" (cuando ya intentaste 2+)**
- **Cada corrección revela nuevo problema en lugar diferente**

**TODAS estas significan: DETENER. Volver a Fase 1.**

**Si 3+ correcciones fallaron:** Cuestionar la arquitectura (ver Fase 4.5)

## Señales de tu Compañero Humano de que Lo Estás Haciendo Mal

**Observar estas redirecciones:**
- "¿Eso no está pasando?" - Asumiste sin verificar
- "¿Nos mostrará...?" - Deberías haber agregado recopilación de evidencia
- "Deja de adivinar" - Estás proponiendo correcciones sin entender
- "Ultrathink esto" - Cuestionar fundamentos, no solo síntomas
- "¿Estamos atascados?" (frustrado) - Tu enfoque no está funcionando

**Cuando veas estas:** DETENER. Volver a Fase 1.

## Racionalizaciones Comunes

| Excusa | Realidad |
|--------|----------|
| "El problema es simple, no necesito proceso" | Los problemas simples también tienen causas raíz. El proceso es rápido para bugs simples. |
| "Emergencia, no hay tiempo para proceso" | El debugging sistemático es MÁS RÁPIDO que trastear adivinando. |
| "Solo probar esto primero, luego investigar" | La primera corrección establece el patrón. Hazlo bien desde el inicio. |
| "Escribiré prueba después de confirmar que la corrección funciona" | Las correcciones no probadas no se mantienen. Probar primero lo prueba. |
| "Múltiples correcciones a la vez ahorra tiempo" | No puedes aislar qué funcionó. Causa nuevos bugs. |
| "Referencia demasiado larga, adaptaré el patrón" | Entendimiento parcial garantiza bugs. Léelo completamente. |
| "Veo el problema, déjame arreglarlo" | Ver síntomas ≠ entender causa raíz. |
| "Un intento de corrección más" (después de 2+ fallos) | 3+ fallos = problema arquitectónico. Cuestionar patrón, no arreglar de nuevo. |

## Referencia Rápida

| Fase | Actividades Clave | Criterios de Éxito |
|------|-------------------|-------------------|
| **1. Causa Raíz** | Leer errores, reproducir, verificar cambios, recopilar evidencia | Entender QUÉ y POR QUÉ |
| **2. Patrón** | Encontrar ejemplos que funcionan, comparar | Identificar diferencias |
| **3. Hipótesis** | Formar teoría, probar mínimamente | Confirmada o nueva hipótesis |
| **4. Implementación** | Crear prueba, arreglar, verificar | Bug resuelto, pruebas pasan |

## Cuando el Proceso Revela "Sin Causa Raíz"

Si la investigación sistemática revela que el problema es verdaderamente ambiental, dependiente de tiempo o externo:

1. Has completado el proceso
2. Documentar lo que investigaste
3. Implementar manejo apropiado (reintento, timeout, mensaje de error)
4. Agregar monitoreo/registro para investigación futura

**Pero:** 95% de los casos de "sin causa raíz" son investigación incompleta.

## Técnicas de Soporte

Estas técnicas son parte del debugging sistemático y están disponibles en este directorio:

- **`root-cause-tracing.md`** - Rastrear bugs hacia atrás a través de la pila de llamadas para encontrar activador original
- **`defense-in-depth.md`** - Agregar validación en múltiples capas después de encontrar causa raíz
- **`condition-based-waiting.md`** - Reemplazar timeouts arbitrarios con polling de condición

**Skills relacionadas:**
- **superpowers:test-driven-development** - Para crear caso de prueba que falla (Fase 4, Paso 1)
- **superpowers:verification-before-completion** - Verificar que la corrección funcionó antes de afirmar éxito

## Impacto del Mundo Real

De sesiones de debugging:
- Enfoque sistemático: 15-30 minutos para arreglar
- Enfoque de correcciones aleatorias: 2-3 horas de trastear
- Tasa de corrección a la primera: 95% vs 40%
- Nuevos bugs introducidos: Casi cero vs común

## Ejemplos de Uso

### Ejemplo 1: Depurar un Error que No Entiendes
**Situación**: Tu aplicación falla con un error pero no sabes por qué. Podrías intentar adivinar y arreglar cosas al azar, pero eso puede empeorar las cosas.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo un error pero no sé por qué, necesito depurarlo sistemáticamente"
2. Cursor usará esta skill para:
   - Leer cuidadosamente el mensaje de error completo
   - Reproducir el error de forma confiable
   - Verificar qué cambió recientemente que podría causarlo
   - Rastrear el flujo de datos para encontrar dónde se origina el problema
   - Formar una hipótesis y probarla mínimamente
   - Arreglar la causa raíz, no solo el síntoma

**Resultado**: Encuentras y arreglas el problema real en lugar de crear parches temporales que causan más problemas después.

### Ejemplo 2: Arreglar un Bug que Ya Intentaste Arreglar Varias Veces
**Situación**: Has intentado arreglar un bug 2-3 veces pero sigue apareciendo o crea nuevos problemas.

**Cómo usar esta skill**:
1. Di a Cursor: "He intentado arreglar este bug varias veces pero no funciona, necesito un enfoque sistemático"
2. Cursor seguirá el proceso de 4 fases:
   - **Fase 1**: Investigará la causa raíz desde cero, sin asumir nada
   - **Fase 2**: Comparará con código similar que funciona
   - **Fase 3**: Formará una hipótesis clara y la probará
   - **Fase 4**: Si 3+ intentos fallaron, cuestionará si hay un problema arquitectónico más profundo

**Resultado**: Encuentras la verdadera causa del problema o identificas que necesitas cambiar la arquitectura en lugar de seguir parcheando.

### Ejemplo 3: Depurar un Problema en un Sistema Complejo con Múltiples Componentes
**Situación**: Tienes un sistema con múltiples partes (API, base de datos, frontend) y algo falla pero no sabes en qué capa.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo un problema en mi sistema pero no sé en qué componente está fallando"
2. Cursor implementará:
   - Instrumentación de diagnóstico en cada límite de componente
   - Registro de qué datos entran y salen de cada capa
   - Una ejecución que muestra exactamente dónde se rompe
   - Análisis de la evidencia para identificar el componente problemático
   - Investigación enfocada en ese componente específico

**Resultado**: Identificas exactamente dónde está el problema en lugar de adivinar, ahorrando horas de trabajo.
