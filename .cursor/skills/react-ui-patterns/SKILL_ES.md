---
name: react-ui-patterns
description: Patrones modernos de UI React para estados de carga, manejo de errores y data fetching. Usar al construir componentes UI, manejar datos async o gestionar estados de UI.
---

# Patrones de UI React

## Principios Fundamentales

1. **Nunca mostrar UI obsoleta** - Loading spinners solo cuando realmente está cargando
2. **Siempre mostrar errores** - Los usuarios deben saber cuando algo falla
3. **Actualizaciones optimistas** - Hacer que la UI se sienta instantánea
4. **Divulgación progresiva** - Mostrar contenido conforme esté disponible
5. **Degradación elegante** - Datos parciales son mejores que ningún dato

## Patrones de Estado de Carga

### La Regla de Oro

**Mostrar indicador de carga SOLO cuando no hay datos para mostrar.**

```typescript
// CORRECTO - Solo mostrar loading cuando no hay datos
const { data, loading, error } = useGetItemsQuery();

if (error) return <ErrorState error={error} onRetry={refetch} />;
if (loading && !data) return <LoadingState />;
if (!data?.items.length) return <EmptyState />;

return <ItemList items={data.items} />;
```

```typescript
// INCORRECTO - Muestra spinner incluso cuando tenemos datos cacheados
if (loading) return <LoadingState />; // ¡Parpadea en refetch!
```

### Árbol de Decisión de Estado de Carga

```
¿Hay un error?
  → Sí: Mostrar estado de error con opción de reintento
  → No: Continuar

¿Está cargando Y no tenemos datos?
  → Sí: Mostrar indicador de carga (spinner/skeleton)
  → No: Continuar

¿Tenemos datos?
  → Sí, con items: Mostrar los datos
  → Sí, pero vacío: Mostrar estado vacío
  → No: Mostrar loading (fallback)
```

### Skeleton vs Spinner

| Usar Skeleton Cuando | Usar Spinner Cuando |
|----------------------|---------------------|
| Forma de contenido conocida | Forma de contenido desconocida |
| Layouts de lista/tarjeta | Acciones de modal |
| Carga inicial de página | Envíos de botón |
| Placeholders de contenido | Operaciones inline |

## Patrones de Manejo de Errores

### La Jerarquía de Manejo de Errores

```
1. Error inline (nivel campo) → Errores de validación de formulario
2. Notificación toast → Errores recuperables, usuario puede reintentar
3. Banner de error → Errores a nivel página, datos aún parcialmente usables
4. Pantalla de error completa → Irrecuperable, necesita acción del usuario
```

### Siempre Mostrar Errores

**CRÍTICO: Nunca tragar errores silenciosamente.**

```typescript
// CORRECTO - Error siempre mostrado al usuario
const [createItem, { loading }] = useCreateItemMutation({
  onCompleted: () => {
    toast.success({ title: 'Item creado' });
  },
  onError: (error) => {
    console.error('createItem falló:', error);
    toast.error({ title: 'Falló al crear item' });
  },
});

// INCORRECTO - Error capturado silenciosamente, usuario no tiene idea
const [createItem] = useCreateItemMutation({
  onError: (error) => {
    console.error(error); // ¡Usuario no ve nada!
  },
});
```

### Patrón de Componente de Estado de Error

```typescript
interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
  title?: string;
}

const ErrorState = ({ error, onRetry, title }: ErrorStateProps) => (
  <div className="error-state">
    <Icon name="exclamation-circle" />
    <h3>{title ?? 'Algo salió mal'}</h3>
    <p>{error.message}</p>
    {onRetry && (
      <Button onClick={onRetry}>Intentar de Nuevo</Button>
    )}
  </div>
);
```

## Patrones de Estado de Botón

### Estado de Carga de Botón

```tsx
<Button
  onClick={handleSubmit}
  isLoading={isSubmitting}
  disabled={!isValid || isSubmitting}
>
  Submit
</Button>
```

### Deshabilitar Durante Operaciones

**CRÍTICO: Siempre deshabilitar activadores durante operaciones async.**

```tsx
// CORRECTO - Botón deshabilitado mientras carga
<Button
  disabled={isSubmitting}
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Submit
</Button>

// INCORRECTO - Usuario puede tocar múltiples veces
<Button onClick={handleSubmit}>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</Button>
```

## Estados Vacíos

### Requisitos de Estado Vacío

Cada lista/colección DEBE tener un estado vacío:

```tsx
// INCORRECTO - Sin estado vacío
return <FlatList data={items} />;

// CORRECTO - Estado vacío explícito
return (
  <FlatList
    data={items}
    ListEmptyComponent={<EmptyState />}
  />
);
```

### Estados Vacíos Contextuales

```tsx
// Búsqueda sin resultados
<EmptyState
  icon="search"
  title="No se encontraron resultados"
  description="Prueba términos de búsqueda diferentes"
/>

// Lista sin items aún
<EmptyState
  icon="plus-circle"
  title="Aún no hay items"
  description="Crea tu primer item"
  action={{ label: 'Crear Item', onClick: handleCreate }}
/>
```

## Patrón de Envío de Formulario

```tsx
const MyForm = () => {
  const [submit, { loading }] = useSubmitMutation({
    onCompleted: handleSuccess,
    onError: handleError,
  });

  const handleSubmit = async () => {
    if (!isValid) {
      toast.error({ title: 'Por favor corrige errores' });
      return;
    }
    await submit({ variables: { input: values } });
  };

  return (
    <form>
      <Input
        value={values.name}
        onChange={handleChange('name')}
        error={touched.name ? errors.name : undefined}
      />
      <Button
        type="submit"
        onClick={handleSubmit}
        disabled={!isValid || loading}
        isLoading={loading}
      >
        Submit
      </Button>
    </form>
  );
};
```

## Anti-Patrones

### Estados de Carga

```typescript
// INCORRECTO - Spinner cuando datos existen (causa flash)
if (loading) return <Spinner />;

// CORRECTO - Solo mostrar loading sin datos
if (loading && !data) return <Spinner />;
```

### Manejo de Errores

```typescript
// INCORRECTO - Error tragado
try {
  await mutation();
} catch (e) {
  console.log(e); // ¡Usuario no tiene idea!
}

// CORRECTO - Error mostrado
onError: (error) => {
  console.error('operación falló:', error);
  toast.error({ title: 'Operación falló' });
}
```

### Estados de Botón

```typescript
// INCORRECTO - Botón no deshabilitado durante envío
<Button onClick={submit}>Submit</Button>

// CORRECTO - Deshabilitado y muestra loading
<Button onClick={submit} disabled={loading} isLoading={loading}>
  Submit
</Button>
```

## Lista de Verificación

Antes de completar cualquier componente UI:

**Estados de UI:**
- [ ] Estado de error manejado y mostrado al usuario
- [ ] Estado de carga mostrado solo cuando no hay datos
- [ ] Estado vacío proporcionado para colecciones
- [ ] Botones deshabilitados durante operaciones async
- [ ] Botones muestran indicador de carga cuando es apropiado

**Datos y Mutaciones:**
- [ ] Mutaciones tienen handler onError
- [ ] Todas las acciones de usuario tienen retroalimentación (toast/visual)

## Integración con Otras Skills

- **graphql-schema**: Usar patrones de mutación con manejo apropiado de errores
- **testing-patterns**: Probar todos los estados de UI (loading, error, empty, success)
- **formik-patterns**: Aplicar patrones de envío de formulario

## Ejemplos de Uso

### Ejemplo 1: Manejar Estados de Carga Correctamente
**Situación**: Quieres mostrar un indicador de carga pero no quieres que parpadee cuando hay datos cacheados.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero manejar estados de carga correctamente en mi componente"
2. Cursor usará esta skill para:
   - Mostrar loading solo cuando no hay datos (no cuando hay datos cacheados)
   - Usar skeletons cuando conoces la forma del contenido
   - Usar spinners para acciones de botón
   - Evitar el parpadeo molesto de spinners

**Resultado**: Estados de carga que mejoran la experiencia del usuario sin causar parpadeos innecesarios.

### Ejemplo 2: Manejar Errores de Forma que el Usuario los Vea
**Situación**: Tienes errores que se están tragando silenciosamente y el usuario no sabe qué pasó.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero asegurarme de que todos los errores se muestren al usuario"
2. Cursor:
   - Implementará handlers onError en todas las mutaciones
   - Mostrará errores apropiadamente (toast, banner, pantalla completa según severidad)
   - Dará opciones de reintento cuando sea apropiado
   - Nunca tragará errores silenciosamente

**Resultado**: Usuarios siempre informados cuando algo falla, con opciones claras de qué hacer.

### Ejemplo 3: Crear Estados Vacíos Contextuales
**Situación**: Tienes listas que a veces están vacías y quieres mostrar algo útil al usuario.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero agregar estados vacíos a mis listas"
2. Cursor:
   - Creará estados vacíos contextuales (diferentes para búsqueda sin resultados vs lista vacía)
   - Incluirá acciones apropiadas (botón para crear primer item)
   - Hará que los estados vacíos sean útiles y guíen al usuario

**Resultado**: Estados vacíos que mejoran la experiencia del usuario en lugar de solo mostrar una lista en blanco.
