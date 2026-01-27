---
name: git-pushing
description: Hacer stage, commit y push de cambios git con mensajes de commit convencionales. Usar cuando el usuario quiere hacer commit y push de cambios, menciona hacer push a remoto o pide guardar y hacer push de su trabajo. También se activa cuando el usuario dice "push changes", "commit and push", "push this", "push to github" o solicitudes similares de flujo de trabajo git.
---

# Flujo de Trabajo Git Push

Hacer stage de todos los cambios, crear un commit convencional y hacer push a la rama remota.

## Cuándo Usar

Se activa automáticamente cuando el usuario:

- Pide explícitamente hacer push de cambios ("push this", "commit and push")
- Menciona guardar trabajo en remoto ("save to github", "push to remote")
- Completa una característica y quiere compartirla
- Dice frases como "let's push this up" o "commit these changes"

## Flujo de Trabajo

**SIEMPRE usar el script** - NO usar comandos git manuales:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

Con mensaje personalizado:

```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

El script maneja: staging, mensaje de commit convencional, footer de Claude, push con flag -u.

## Ejemplos de Uso

### Ejemplo 1: Guardar y Hacer Push de tu Trabajo
**Situación**: Has terminado de trabajar en una característica y quieres guardarla en GitHub.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero hacer push de estos cambios a GitHub"
2. Cursor usará esta skill para:
   - Hacer stage de todos los cambios
   - Crear un commit con mensaje convencional (por ejemplo, "feat: agregar autenticación")
   - Hacer push a la rama remota
   - Todo automáticamente usando el script apropiado

**Resultado**: Tus cambios guardados y enviados a GitHub con un mensaje de commit claro y profesional.

### Ejemplo 2: Hacer Commit y Push con Mensaje Personalizado
**Situación**: Quieres hacer commit con un mensaje específico que describes.

**Cómo usar esta skill**:
1. Di a Cursor: "Haz commit y push con el mensaje 'fix: corregir bug de login'"
2. Cursor:
   - Usará el script con tu mensaje personalizado
   - Creará el commit con ese mensaje
   - Hará push a remoto

**Resultado**: Commit y push con tu mensaje específico, manteniendo el formato convencional.

### Ejemplo 3: Guardar Trabajo Antes de Cambiar de Rama
**Situación**: Estás trabajando en una rama y quieres guardar tu progreso antes de cambiar a otra.

**Cómo usar esta skill**:
1. Di a Cursor: "Guarda mi trabajo y haz push antes de cambiar de rama"
2. Cursor:
   - Hará stage de todos los cambios
   - Creará un commit apropiado
   - Hará push para que tu trabajo esté seguro en remoto
   - Luego puedes cambiar de rama con confianza

**Resultado**: Tu trabajo guardado y respaldado en remoto, listo para continuar después.
