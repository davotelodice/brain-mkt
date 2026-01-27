---
name: deployment-procedures
description: Principios de deployment en producción y toma de decisiones. Workflows de deployment seguros, estrategias de rollback y verificación. Enseña a pensar, no scripts.
allowed-tools: Read, Glob, Grep, Bash
---

# Procedimientos de Deployment

> Principios de deployment y toma de decisiones para releases seguros en producción.
> **Aprende a PENSAR, no memorizar scripts.**

---

## ⚠️ Cómo Usar Esta Skill

Esta skill enseña **principios de deployment**, no scripts bash para copiar.

- Cada deployment es único
- Entiende el POR QUÉ detrás de cada paso
- Adapta procedimientos a tu plataforma

---

## 1. Selección de Plataforma

### Árbol de Decisión

```
¿Qué estás desplegando?
│
├── Sitio estático / JAMstack
│   └── Vercel, Netlify, Cloudflare Pages
│
├── App web simple
│   ├── Gestionado → Railway, Render, Fly.io
│   └── Control → VPS + PM2/Docker
│
├── Microservicios
│   └── Orquestación de contenedores
│
└── Serverless
    └── Edge functions, Lambda
```

### Cada Plataforma Tiene Diferentes Procedimientos

| Plataforma | Método de Deployment |
|------------|----------------------|
| **Vercel/Netlify** | Git push, auto-deploy |
| **Railway/Render** | Git push o CLI |
| **VPS + PM2** | SSH + pasos manuales |
| **Docker** | Push de imagen + orquestación |
| **Kubernetes** | kubectl apply |

---

## 2. Principios Pre-Deployment

### Las 4 Categorías de Verificación

| Categoría | Qué Verificar |
|-----------|---------------|
| **Calidad de Código** | Tests pasando, linting limpio, revisado |
| **Build** | Build de producción funciona, sin warnings |
| **Entorno** | Env vars configuradas, secrets actuales |
| **Seguridad** | Backup hecho, plan de rollback listo |

### Lista de Verificación Pre-Deployment

- [ ] Todos los tests pasando
- [ ] Código revisado y aprobado
- [ ] Build de producción exitoso
- [ ] Variables de entorno verificadas
- [ ] Migraciones de base de datos listas (si hay)
- [ ] Plan de rollback documentado
- [ ] Equipo notificado
- [ ] Monitoreo listo

---

## 3. Principios de Workflow de Deployment

### El Proceso de 5 Fases

```
1. PREPARAR
   └── Verificar código, build, env vars

2. BACKUP
   └── Guardar estado actual antes de cambiar

3. DEPLOY
   └── Ejecutar con monitoreo abierto

4. VERIFICAR
   └── Health check, logs, flujos clave

5. CONFIRMAR o ROLLBACK
   └── ¿Todo bien? Confirmar. ¿Problemas? Rollback.
```

### Principios por Fase

| Fase | Principio |
|------|-----------|
| **Preparar** | Nunca desplegar código no probado |
| **Backup** | No puedes hacer rollback sin backup |
| **Deploy** | Observarlo suceder, no alejarse |
| **Verificar** | Confiar pero verificar |
| **Confirmar** | Tener trigger de rollback listo |

---

## 4. Verificación Post-Deployment

### Qué Verificar

| Verificación | Por Qué |
|--------------|---------|
| **Health endpoint** | Servicio está ejecutándose |
| **Error logs** | Sin errores nuevos |
| **Flujos de usuario clave** | Características críticas funcionan |
| **Rendimiento** | Tiempos de respuesta aceptables |

### Ventana de Verificación

- **Primeros 5 minutos**: Monitoreo activo
- **15 minutos**: Confirmar estable
- **1 hora**: Verificación final
- **Día siguiente**: Revisar métricas

---

## 5. Principios de Rollback

### Cuándo Hacer Rollback

| Síntoma | Acción |
|---------|--------|
| Servicio caído | Rollback inmediato |
| Errores críticos | Rollback |
| Rendimiento >50% degradado | Considerar rollback |
| Problemas menores | Arreglar hacia adelante si es rápido |

### Estrategia de Rollback por Plataforma

| Plataforma | Método de Rollback |
|------------|-------------------|
| **Vercel/Netlify** | Redeploy commit anterior |
| **Railway/Render** | Rollback en dashboard |
| **VPS + PM2** | Restaurar backup, reiniciar |
| **Docker** | Tag de imagen anterior |
| **K8s** | kubectl rollout undo |

### Principios de Rollback

1. **Velocidad sobre perfección**: Rollback primero, debug después
2. **No compondas errores**: Un rollback, no múltiples cambios
3. **Comunica**: Di al equipo qué pasó
4. **Post-mortem**: Entender por qué después de estable

---

## 6. Deployment Sin Downtime

### Estrategias

| Estrategia | Cómo Funciona |
|------------|---------------|
| **Rolling** | Reemplazar instancias una por una |
| **Blue-Green** | Cambiar tráfico entre entornos |
| **Canary** | Cambio gradual de tráfico |

### Principios de Selección

| Escenario | Estrategia |
|-----------|------------|
| Release estándar | Rolling |
| Cambio de alto riesgo | Blue-green (rollback fácil) |
| Necesitas validación | Canary (probar con tráfico real) |

---

## 7. Procedimientos de Emergencia

### Prioridad de Servicio Caído

1. **Evaluar**: ¿Cuál es el síntoma?
2. **Fix rápido**: Reiniciar si no está claro
3. **Rollback**: Si reinicio no ayuda
4. **Investigar**: Después de estable

### Orden de Investigación

| Verificar | Problemas Comunes |
|-----------|-------------------|
| **Logs** | Errores, excepciones |
| **Recursos** | Disco lleno, memoria |
| **Red** | DNS, firewall |
| **Dependencias** | Base de datos, APIs |

---

## 8. Anti-Patrones

| ❌ No Hacer | ✅ Hacer |
|-------------|----------|
| Deploy en viernes | Deploy temprano en semana |
| Apresurar deployment | Seguir el proceso |
| Omitir staging | Siempre probar primero |
| Deploy sin backup | Backup antes de deploy |
| Alejarse después de deploy | Monitorear por 15+ min |
| Múltiples cambios a la vez | Un cambio a la vez |

---

## 9. Lista de Verificación de Decisión

Antes de desplegar:

- [ ] **¿Procedimiento apropiado para plataforma?**
- [ ] **¿Estrategia de backup lista?**
- [ ] **¿Plan de rollback documentado?**
- [ ] **¿Monitoreo configurado?**
- [ ] **¿Equipo notificado?**
- [ ] **¿Tiempo para monitorear después?**

---

## 10. Mejores Prácticas

1. **Deploys pequeños y frecuentes** sobre releases grandes
2. **Feature flags** para cambios riesgosos
3. **Automatizar** pasos repetitivos
4. **Documentar** cada deployment
5. **Revisar** qué salió mal después de problemas
6. **Probar rollback** antes de necesitarlo

---

> **Recuerda:** Cada deployment es un riesgo. Minimiza riesgo a través de preparación, no velocidad.

## Ejemplos de Uso

### Ejemplo 1: Hacer tu Primer Deployment a Producción
**Situación**: Quieres desplegar tu aplicación a producción pero quieres hacerlo de forma segura.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero desplegar mi app a producción de forma segura"
2. Cursor usará esta skill para:
   - Verificar que todo está listo (tests, build, env vars)
   - Crear backup antes de desplegar
   - Ejecutar deployment con monitoreo
   - Verificar que todo funciona después
   - Tener plan de rollback listo

**Resultado**: Un deployment seguro y exitoso con capacidad de rollback si algo sale mal.

### Ejemplo 2: Configurar Deployment Sin Downtime
**Situación**: Quieres desplegar sin que los usuarios noten interrupciones.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar deployment sin downtime"
2. Cursor:
   - Elegirá estrategia apropiada (rolling, blue-green, canary)
   - Configurará el deployment según tu plataforma
   - Implementará health checks
   - Te guiará en el proceso completo

**Resultado**: Deployments que no interrumpen el servicio para los usuarios.

### Ejemplo 3: Manejar un Deployment que Falló
**Situación**: Acabas de desplegar y algo salió mal.

**Cómo usar esta skill**:
1. Di a Cursor: "Mi deployment falló, necesito ayuda"
2. Cursor:
   - Te ayudará a evaluar la situación rápidamente
   - Te guiará en hacer rollback si es necesario
   - Te ayudará a investigar qué salió mal
   - Te dará pasos para arreglar y redespachar

**Resultado**: Problema resuelto rápidamente con rollback apropiado y plan para arreglar.
