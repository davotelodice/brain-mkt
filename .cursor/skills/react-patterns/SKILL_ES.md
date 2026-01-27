---
name: react-patterns
description: Patrones y principios modernos de React. Hooks, composición, rendimiento, mejores prácticas de TypeScript.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Patrones React

> Principios para construir aplicaciones React listas para producción.

---

## 1. Principios de Diseño de Componentes

### Tipos de Componentes

| Tipo | Usar | Estado |
|------|------|--------|
| **Server** | Data fetching, estático | Ninguno |
| **Client** | Interactividad | useState, effects |
| **Presentational** | Visualización UI | Solo props |
| **Container** | Lógica/estado | Estado pesado |

### Reglas de Diseño

- Una responsabilidad por componente
- Props abajo, eventos arriba
- Composición sobre herencia
- Preferir componentes pequeños y enfocados

---

## 2. Patrones de Hooks

### Cuándo Extraer Hooks

| Patrón | Extraer Cuando |
|--------|----------------|
| **useLocalStorage** | Misma lógica de almacenamiento necesaria |
| **useDebounce** | Múltiples valores debounced |
| **useFetch** | Patrones de fetch repetidos |
| **useForm** | Estado de formulario complejo |

### Reglas de Hooks

- Hooks solo en nivel superior
- Mismo orden cada render
- Hooks personalizados comienzan con "use"
- Limpiar effects en unmount

---

## 3. Selección de Gestión de Estado

| Complejidad | Solución |
|-------------|----------|
| Simple | useState, useReducer |
| Compartido local | Context |
| Estado de servidor | React Query, SWR |
| Global complejo | Zustand, Redux Toolkit |

### Colocación de Estado

| Alcance | Dónde |
|---------|-------|
| Componente único | useState |
| Padre-hijo | Lift state up |
| Subárbol | Context |
| App-wide | Global store |

---

## 4. Patrones React 19

### Nuevos Hooks

| Hook | Propósito |
|------|-----------|
| **useActionState** | Estado de envío de formulario |
| **useOptimistic** | Actualizaciones optimistas de UI |
| **use** | Leer recursos en render |

### Beneficios del Compilador

- Memoización automática
- Menos useMemo/useCallback manual
- Enfoque en componentes puros

---

## 5. Patrones de Composición

### Componentes Compuestos

- Padre proporciona contexto
- Hijos consumen contexto
- Composición flexible basada en slots
- Ejemplo: Tabs, Accordion, Dropdown

### Render Props vs Hooks

| Caso de Uso | Preferir |
|-------------|----------|
| Lógica reutilizable | Hook personalizado |
| Flexibilidad de render | Render props |
| Cross-cutting | Higher-order component |

---

## 6. Principios de Rendimiento

### Cuándo Optimizar

| Señal | Acción |
|-------|--------|
| Renders lentos | Perfilar primero |
| Listas grandes | Virtualizar |
| Cálculo costoso | useMemo |
| Callbacks estables | useCallback |

### Orden de Optimización

1. Verificar si realmente es lento
2. Perfilar con DevTools
3. Identificar cuello de botella
4. Aplicar corrección dirigida

---

## 7. Manejo de Errores

### Uso de Error Boundary

| Alcance | Colocación |
|---------|------------|
| App-wide | Nivel raíz |
| Característica | Nivel ruta/característica |
| Componente | Alrededor de componente riesgoso |

### Recuperación de Errores

- Mostrar fallback UI
- Registrar error
- Ofrecer opción de reintento
- Preservar datos de usuario

---

## 8. Patrones TypeScript

### Tipado de Props

| Patrón | Usar |
|--------|------|
| Interface | Props de componente |
| Type | Unions, complejo |
| Generic | Componentes reutilizables |

### Tipos Comunes

| Necesidad | Tipo |
|-----------|------|
| Children | ReactNode |
| Event handler | MouseEventHandler |
| Ref | RefObject<Element> |

---

## 9. Principios de Pruebas

| Nivel | Enfoque |
|-------|---------|
| Unit | Funciones puras, hooks |
| Integration | Comportamiento de componente |
| E2E | Flujos de usuario |

### Prioridades de Pruebas

- Comportamiento visible al usuario
- Casos límite
- Estados de error
- Accesibilidad

---

## 10. Anti-Patrones

| ❌ No Hacer | ✅ Hacer |
|-------------|----------|
| Prop drilling profundo | Usar context |
| Componentes gigantes | Dividir más pequeños |
| useEffect para todo | Server components |
| Optimización prematura | Perfilar primero |
| Index como key | ID único estable |

---

> **Recuerda:** React es sobre composición. Construir pequeño, combinar cuidadosamente.

## Ejemplos de Uso

### Ejemplo 1: Elegir el Patrón Correcto para tu Componente
**Situación**: Quieres crear un componente pero no sabes qué patrón usar.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un componente pero no sé qué patrón usar"
2. Cursor usará esta skill para:
   - Identificar si es Server Component (data fetching) o Client Component (interactividad)
   - Recomendar si usar composición, hooks personalizados o render props
   - Sugerir gestión de estado apropiada (useState, Context, o store global)
   - Aplicar los patrones correctos para tu caso específico

**Resultado**: Un componente bien diseñado usando los patrones apropiados para tu caso de uso específico.

### Ejemplo 2: Optimizar Rendimiento de Componentes
**Situación**: Tienes componentes que se re-renderizan demasiado y quieres optimizarlos.

**Cómo usar esta skill**:
1. Di a Cursor: "Mis componentes se re-renderizan demasiado, quiero optimizarlos"
2. Cursor:
   - Identificará qué componentes necesitan memoización
   - Aplicará useMemo para cálculos costosos
   - Usará useCallback para callbacks estables
   - Optimizará dependencias de effects
   - Aplicará todas las optimizaciones apropiadas

**Resultado**: Componentes optimizados que se re-renderizan solo cuando es necesario, mejorando el rendimiento.

### Ejemplo 3: Crear Hooks Personalizados Reutilizables
**Situación**: Tienes lógica que se repite en múltiples componentes y quieres extraerla a un hook.

**Cómo usar esta skill**:
1. Di a Cursor: "Tengo lógica que se repite, quiero crear un hook personalizado"
2. Cursor usará esta skill para:
   - Identificar qué lógica debería extraerse
   - Crear un hook personalizado siguiendo las convenciones (nombre con "use")
   - Asegurar que el hook sigue las reglas de hooks
   - Hacerlo reutilizable y bien tipado

**Resultado**: Un hook personalizado reutilizable que simplifica tu código y lo hace más mantenible.
