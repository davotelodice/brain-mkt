---
name: using-git-worktrees
description: Usar al iniciar trabajo de característica que necesita aislamiento del workspace actual o antes de ejecutar planes de implementación - crea git worktrees aislados con selección inteligente de directorio y verificación de seguridad
---

# Usar Git Worktrees

## Resumen

Los git worktrees crean workspaces aislados compartiendo el mismo repositorio, permitiendo trabajar en múltiples ramas simultáneamente sin cambiar.

**Principio central:** Selección sistemática de directorio + verificación de seguridad = aislamiento confiable.

**Anunciar al inicio:** "Estoy usando la skill using-git-worktrees para configurar un workspace aislado."

## Proceso de Selección de Directorio

Seguir este orden de prioridad:

### 1. Verificar Directorios Existentes

```bash
# Verificar en orden de prioridad
ls -d .worktrees 2>/dev/null     # Preferido (oculto)
ls -d worktrees 2>/dev/null      # Alternativa
```

**Si se encuentra:** Usar ese directorio. Si ambos existen, `.worktrees` gana.

### 2. Verificar CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**Si se especifica preferencia:** Usarla sin preguntar.

### 3. Preguntar al Usuario

Si no existe directorio y no hay preferencia en CLAUDE.md:

```
No se encontró directorio de worktree. ¿Dónde debería crear worktrees?

1. .worktrees/ (local al proyecto, oculto)
2. ~/.config/superpowers/worktrees/<project-name>/ (ubicación global)

¿Cuál prefieres?
```

## Verificación de Seguridad

### Para Directorios Locales al Proyecto (.worktrees o worktrees)

**DEBE verificar que el directorio está ignorado antes de crear worktree:**

```bash
# Verificar si el directorio está ignorado (respeta gitignore local, global y del sistema)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**Si NO está ignorado:**

Según la regla de Jesse "Arreglar cosas rotas inmediatamente":
1. Agregar línea apropiada a .gitignore
2. Hacer commit del cambio
3. Proceder con creación de worktree

**Por qué es crítico:** Previene accidentalmente hacer commit de contenidos de worktree al repositorio.

### Para Directorio Global (~/.config/superpowers/worktrees)

No se necesita verificación de .gitignore - completamente fuera del proyecto.

## Pasos de Creación

### 1. Detectar Nombre del Proyecto

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Crear Worktree

```bash
# Determinar ruta completa
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Crear worktree con nueva rama
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Ejecutar Configuración del Proyecto

Auto-detectar y ejecutar configuración apropiada:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verificar Baseline Limpio

Ejecutar pruebas para asegurar que el worktree comienza limpio:

```bash
# Ejemplos - usar comando apropiado del proyecto
npm test
cargo test
pytest
go test ./...
```

**Si las pruebas fallan:** Reportar fallos, preguntar si proceder o investigar.

**Si las pruebas pasan:** Reportar listo.

### 5. Reportar Ubicación

```
Worktree listo en <ruta-completa>
Pruebas pasando (<N> pruebas, 0 fallos)
Listo para implementar <nombre-de-característica>
```

## Referencia Rápida

| Situación | Acción |
|-----------|--------|
| `.worktrees/` existe | Usarlo (verificar ignorado) |
| `worktrees/` existe | Usarlo (verificar ignorado) |
| Ambos existen | Usar `.worktrees/` |
| Ninguno existe | Preguntar al usuario |
| Preferencia en CLAUDE.md | Usar preferencia |
| Directorio no ignorado | Agregar a .gitignore primero |

## Ejemplos de Uso

### Ejemplo 1: Trabajar en una Característica en un Workspace Aislado
**Situación**: Quieres trabajar en una nueva característica pero no quieres afectar tu workspace actual.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un worktree para trabajar en una nueva característica de forma aislada"
2. Cursor usará esta skill para:
   - Detectar o crear el directorio apropiado para worktrees
   - Verificar que está en .gitignore para no hacer commit accidentalmente
   - Crear un nuevo worktree con una nueva rama
   - Configurar el proyecto (instalar dependencias, etc.)
   - Verificar que todo funciona antes de empezar

**Resultado**: Un workspace completamente aislado donde puedes trabajar en la nueva característica sin afectar tu trabajo actual.

### Ejemplo 2: Trabajar en Múltiples Características Simultáneamente
**Situación**: Necesitas trabajar en dos características diferentes al mismo tiempo sin cambiar de rama constantemente.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito trabajar en dos características diferentes, quiero crear worktrees para cada una"
2. Cursor:
   - Creará un worktree para cada característica
   - Cada uno en su propia rama
   - Puedes trabajar en ambos simultáneamente sin conflictos
   - Cada uno tiene su propio directorio y configuración

**Resultado**: Múltiples workspaces aislados, uno para cada característica, permitiéndote trabajar en ambos sin interferencia.

### Ejemplo 3: Ejecutar un Plan de Implementación en un Workspace Limpio
**Situación**: Tienes un plan de implementación y quieres ejecutarlo en un workspace limpio y aislado.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero ejecutar este plan de implementación en un worktree limpio"
2. Cursor:
   - Creará un worktree nuevo y limpio
   - Verificará que las pruebas pasan antes de empezar
   - Te dará un workspace aislado para ejecutar el plan
   - No afectará tu workspace principal

**Resultado**: Un workspace limpio y aislado perfecto para ejecutar tu plan de implementación sin riesgos.
