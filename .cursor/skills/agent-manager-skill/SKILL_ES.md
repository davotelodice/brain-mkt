---
name: agent-manager-skill
description: Gestionar múltiples agentes CLI locales vía sesiones tmux (iniciar/detener/monitorear/asignar) con programación compatible con cron.
---

# Skill de Gestor de Agentes

## Cuándo usar

Usar esta skill cuando necesites:

- ejecutar múltiples agentes CLI locales en paralelo (sesiones tmux separadas)
- iniciar/detener agentes y seguir sus logs
- asignar tareas a agentes y monitorear salida
- programar trabajo recurrente de agentes (cron)

## Prerrequisitos

Instalar `agent-manager-skill` en tu workspace:

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## Comandos Comunes

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start EMP_0001
python3 agent-manager/scripts/main.py monitor EMP_0001 --follow
python3 agent-manager/scripts/main.py assign EMP_0002 <<'EOF'
Follow teams/fractalmind-ai-maintenance.md Workflow
EOF
```

## Notas

- Requiere `tmux` y `python3`.
- Los agentes se configuran bajo un directorio `agents/` (ver el repo para ejemplos).

## Ejemplos de Uso

### Ejemplo 1: Ejecutar Múltiples Agentes en Paralelo
**Situación**: Necesitas ejecutar varios agentes al mismo tiempo para diferentes tareas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero ejecutar múltiples agentes en paralelo"
2. Cursor usará esta skill para:
   - Iniciar cada agente en su propia sesión tmux
   - Monitorear los logs de todos los agentes
   - Gestionar el ciclo de vida de cada agente
   - Permitirte asignar tareas a agentes específicos

**Resultado**: Múltiples agentes ejecutándose en paralelo, cada uno en su propia sesión aislada.

### Ejemplo 2: Programar Trabajo Recurrente de Agentes
**Situación**: Quieres que un agente ejecute una tarea periódicamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero programar un agente para que ejecute una tarea cada día"
2. Cursor:
   - Configurará el agente con la tarea
   - Creará un cron job para ejecutarlo periódicamente
   - Te permitirá monitorear las ejecuciones
   - Gestionará el ciclo de vida del agente programado

**Resultado**: Un agente que ejecuta tareas automáticamente según un horario programado.

### Ejemplo 3: Monitorear y Gestionar Agentes Activos
**Situación**: Tienes varios agentes ejecutándose y quieres monitorearlos y gestionarlos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero ver qué agentes están ejecutándose y monitorear sus logs"
2. Cursor:
   - Te mostrará lista de agentes activos
   - Te permitirá seguir logs en tiempo real
   - Te permitirá detener agentes si es necesario
   - Te ayudará a gestionar el estado de todos los agentes

**Resultado**: Visibilidad completa y control sobre todos tus agentes activos.
