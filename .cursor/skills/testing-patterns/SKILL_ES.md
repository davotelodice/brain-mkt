---
name: testing-patterns
description: Patrones de pruebas Jest, funciones factory, estrategias de mocking y flujo de trabajo TDD. Usar al escribir pruebas unitarias, crear factories de prueba o seguir ciclo TDD red-verde-refactor.
---

# Patrones y Utilidades de Pruebas

## Filosofía de Pruebas

**Test-Driven Development (TDD):**
- Escribir prueba que falla PRIMERO
- Implementar código mínimo para pasar
- Refactorizar después de verde
- Nunca escribir código de producción sin una prueba que falla

**Behavior-Driven Testing:**
- Probar comportamiento, no implementación
- Enfocarse en APIs públicas y requisitos de negocio
- Evitar probar detalles de implementación
- Usar nombres de prueba descriptivos que describan comportamiento

**Patrón Factory:**
- Crear funciones `getMockX(overrides?: Partial<X>)`
- Proporcionar valores por defecto sensatos
- Permitir sobrescribir propiedades específicas
- Mantener pruebas DRY y mantenibles

## Utilidades de Pruebas

### Función Render Personalizada

Crear un render personalizado que envuelve componentes con proveedores requeridos:

```typescript
// src/utils/testUtils.tsx
import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};
```

**Uso:**
```typescript
import { renderWithTheme } from 'utils/testUtils';
import { screen } from '@testing-library/react-native';

it('should render component', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

## Patrón Factory

### Factory de Props de Componente

```typescript
import { ComponentProps } from 'react';

const getMockMyComponentProps = (
  overrides?: Partial<ComponentProps<typeof MyComponent>>
) => {
  return {
    title: 'Default Title',
    count: 0,
    onPress: jest.fn(),
    isLoading: false,
    ...overrides,
  };
};

// Uso en pruebas
it('should render with custom title', () => {
  const props = getMockMyComponentProps({ title: 'Custom Title' });
  renderWithTheme(<MyComponent {...props} />);
  expect(screen.getByText('Custom Title')).toBeTruthy();
});
```

### Factory de Datos

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

const getMockUser = (overrides?: Partial<User>): User => {
  return {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'user',
    ...overrides,
  };
};

// Uso
it('should display admin badge for admin users', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('Admin')).toBeTruthy();
});
```

## Patrones de Mocking

### Mocking de Módulos

```typescript
// Mock módulo completo
jest.mock('utils/analytics');

// Mock con función factory
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// Acceder a mock en prueba
const mockLogEvent = jest.requireMock('utils/analytics').Analytics.logEvent;
```

### Mocking de Hooks GraphQL

```typescript
jest.mock('./GetItems.generated', () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock(
  './GetItems.generated'
).useGetItemsQuery as jest.Mock;

// En prueba
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
```

## Estructura de Pruebas

Cada prueba sigue el patrón AAA (Arrange-Act-Assert):

```typescript
it('should calculate total correctly', () => {
  // Arrange: Configurar datos de prueba
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 },
  ];

  // Act: Ejecutar código bajo prueba
  const total = calculateTotal(items);

  // Assert: Verificar resultado esperado
  expect(total).toBe(35);
});
```

## Mejores Prácticas

- Una aserción por prueba (idealmente)
- Nombres descriptivos que describan comportamiento
- Usar factories para datos de prueba
- Mockear solo cuando sea necesario
- Probar comportamiento, no implementación

## Ejemplos de Uso

### Ejemplo 1: Crear Pruebas para un Componente React
**Situación**: Tienes un componente React y quieres escribir pruebas para asegurarte de que funciona correctamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero escribir pruebas para mi componente de botón usando Jest"
2. Cursor usará esta skill para:
   - Crear una función factory para las props del componente
   - Escribir pruebas usando el patrón AAA (Arrange-Act-Assert)
   - Usar funciones de render personalizadas si necesitas proveedores
   - Crear mocks apropiados para dependencias externas

**Resultado**: Pruebas bien estructuradas que son fáciles de mantener y entender, siguiendo patrones probados.

### Ejemplo 2: Probar una Función que Usa una API Externa
**Situación**: Tienes una función que llama a una API y quieres probarla sin hacer llamadas reales.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito probar mi función que usa una API, pero quiero mockearla"
2. Cursor implementará:
   - Mocking del módulo de API
   - Configuración de valores de retorno para diferentes escenarios
   - Pruebas que verifican que la función maneja correctamente los diferentes casos (éxito, error, etc.)

**Resultado**: Pruebas que verifican el comportamiento de tu función sin depender de servicios externos, haciéndolas rápidas y confiables.

### Ejemplo 3: Crear Factories para Datos de Prueba Reutilizables
**Situación**: Tienes que crear los mismos datos de prueba en múltiples archivos de prueba y quieres evitar duplicación.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear factories para mis datos de prueba para evitar duplicación"
2. Cursor creará:
   - Funciones factory que generan datos de prueba con valores por defecto sensatos
   - Capacidad de sobrescribir propiedades específicas cuando necesites casos especiales
   - Factories reutilizables que puedes usar en todas tus pruebas

**Resultado**: Código de prueba más limpio y mantenible, con datos de prueba consistentes y fáciles de modificar.
