---
name: tdd-workflow
description: Principios de flujo de trabajo de Test-Driven Development. Ciclo RED-GREEN-REFACTOR.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Flujo de Trabajo TDD

> Escribir pruebas primero, código segundo.

---

## 1. El Ciclo TDD

```
🔴 RED → Escribir prueba que falla
    ↓
🟢 GREEN → Escribir código mínimo para pasar
    ↓
🔵 REFACTOR → Mejorar calidad de código
    ↓
   Repetir...
```

---

## 2. Las Tres Leyes de TDD

1. Escribir código de producción solo para hacer que una prueba que falla pase
2. Escribir solo suficiente prueba para demostrar fallo
3. Escribir solo suficiente código para hacer que la prueba pase

---

## 3. Principios de Fase RED

### Qué Escribir

| Enfoque | Ejemplo |
|---------|---------|
| Comportamiento | "debe sumar dos números" |
| Casos límite | "debe manejar entrada vacía" |
| Estados de error | "debe lanzar para datos inválidos" |

### Reglas de Fase RED

- La prueba debe fallar primero
- El nombre de la prueba describe comportamiento esperado
- Una aserción por prueba (idealmente)

---

## 4. Principios de Fase GREEN

### Código Mínimo

| Principio | Significado |
|-----------|------------|
| **YAGNI** | You Aren't Gonna Need It |
| **Cosa más simple** | Escribir el mínimo para pasar |
| **Sin optimización** | Solo hacer que funcione |

### Reglas de Fase GREEN

- No escribir código innecesario
- No optimizar aún
- Pasar la prueba, nada más

---

## 5. Principios de Fase REFACTOR

### Qué Mejorar

| Área | Acción |
|------|--------|
| Duplicación | Extraer código común |
| Nomenclatura | Hacer intención clara |
| Estructura | Mejorar organización |
| Complejidad | Simplificar lógica |

### Reglas REFACTOR

- Todas las pruebas deben permanecer verdes
- Cambios incrementales pequeños
- Commit después de cada refactorización

---

## 6. Patrón AAA

Cada prueba sigue:

| Paso | Propósito |
|------|-----------|
| **Arrange** | Configurar datos de prueba |
| **Act** | Ejecutar código bajo prueba |
| **Assert** | Verificar resultado esperado |

---

## 7. Cuándo Usar TDD

| Escenario | Valor TDD |
|-----------|-----------|
| Nueva característica | Alto |
| Corrección de bug | Alto (escribir prueba primero) |
| Lógica compleja | Alto |
| Exploratorio | Bajo (spike, luego TDD) |
| Diseño de UI | Bajo |

---

## 8. Priorización de Pruebas

| Prioridad | Tipo de Prueba |
|-----------|----------------|
| 1 | Camino feliz |
| 2 | Casos de error |
| 3 | Casos límite |
| 4 | Rendimiento |

---

## 9. Anti-Patrones

| ❌ No Hacer | ✅ Hacer |
|-------------|---------|
| Omitir fase RED | Observar que la prueba falle primero |
| Escribir pruebas después | Escribir pruebas antes |
| Sobre-ingeniería inicial | Mantenerlo simple |
| Múltiples aserciones | Un comportamiento por prueba |
| Probar implementación | Probar comportamiento |

---

## 10. TDD Aumentado con IA

### Patrón Multi-Agente

| Agente | Rol |
|--------|-----|
| Agente A | Escribir pruebas que fallan (RED) |
| Agente B | Implementar para pasar (GREEN) |
| Agente C | Optimizar (REFACTOR) |

---

> **Recuerda:** La prueba es la especificación. Si no puedes escribir una prueba, no entiendes el requisito.

## Ejemplos de Uso

### Ejemplo 1: Implementar una Nueva Característica Siguiendo TDD
**Situación**: Quieres agregar una función que valida emails pero quieres hacerlo correctamente con TDD.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar validación de email usando TDD"
2. Cursor seguirá el ciclo:
   - **RED**: Escribir primero una prueba que falla mostrando cómo debería funcionar la validación
   - Ejecutar la prueba y verificar que falla
   - **GREEN**: Escribir el código mínimo para que la prueba pase
   - Ejecutar la prueba y verificar que pasa
   - **REFACTOR**: Mejorar el código si es necesario

**Resultado**: Una función de validación bien probada que funciona correctamente y tiene pruebas que garantizan su comportamiento.

### Ejemplo 2: Arreglar un Bug con el Ciclo TDD
**Situación**: Encontraste un bug y quieres arreglarlo de forma que no vuelva a aparecer.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo un bug donde se aceptan números negativos, quiero arreglarlo con TDD"
2. Cursor implementará:
   - **RED**: Escribir una prueba que reproduce el bug (debe fallar mostrando el comportamiento incorrecto)
   - Verificar que la prueba falla
   - **GREEN**: Escribir la corrección mínima
   - Verificar que la prueba pasa y el bug está arreglado
   - **REFACTOR**: Limpiar si es necesario

**Resultado**: Bug arreglado con una prueba que previene regresiones.

### Ejemplo 3: Refactorizar Código con Confianza
**Situación**: Tienes código que funciona pero quieres mejorarlo sin romper nada.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero refactorizar mi código pero necesito asegurarme de que no rompo nada"
2. Cursor:
   - Asegurará que hay pruebas para el comportamiento actual
   - Refactorizará el código paso a paso
   - Ejecutará las pruebas después de cada cambio
   - Las pruebas te dan confianza para hacer cambios

**Resultado**: Código mejorado con la seguridad de que todo sigue funcionando gracias a las pruebas.
