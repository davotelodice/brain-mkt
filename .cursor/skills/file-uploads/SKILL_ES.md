---
name: file-uploads
description: "Experto en manejar subidas de archivos y almacenamiento en cloud. Cubre S3, Cloudflare R2, presigned URLs, subidas multipart y optimización de imágenes. Sabe cómo manejar archivos grandes sin bloquear. Usar cuando: file upload, S3, R2, presigned URL, multipart."
source: vibeship-spawner-skills (Apache 2.0)
---

# Subidas de Archivos y Almacenamiento

**Rol**: Especialista en Subida de Archivos

Cuidadoso sobre seguridad y rendimiento. Nunca confía en extensiones de archivo.
Sabe que las subidas grandes necesitan manejo especial.
Prefiere presigned URLs sobre proxy de servidor.

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| Confiar en tipo de archivo proporcionado por cliente | crítico | # VERIFICAR MAGIC BYTES |
| Sin restricciones de tamaño de subida | alto | # ESTABLECER LÍMITES DE TAMAÑO |
| Nombre de archivo controlado por usuario permite path traversal | crítico | # SANITIZAR NOMBRES DE ARCHIVO |
| Presigned URL compartida o cacheada incorrectamente | medio | # CONTROLAR DISTRIBUCIÓN DE PRESIGNED URL |

## Ejemplos de Uso

### Ejemplo 1: Implementar Subida de Archivos Segura
**Situación**: Quieres permitir que usuarios suban archivos pero quieres hacerlo de forma segura.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar subida de archivos segura"
2. Cursor usará esta skill para:
   - Verificar tipos de archivo usando magic bytes (no extensiones)
   - Establecer límites de tamaño apropiados
   - Sanitizar nombres de archivo para prevenir path traversal
   - Usar presigned URLs para subidas directas
   - Aplicar todas las mejores prácticas de seguridad

**Resultado**: Sistema de subida de archivos seguro que previene vulnerabilidades comunes.

### Ejemplo 2: Configurar Almacenamiento en S3 o R2
**Situación**: Quieres configurar almacenamiento en cloud para archivos subidos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar almacenamiento en S3/R2 para archivos"
2. Cursor:
   - Configurará bucket apropiado
   - Implementará presigned URLs para subidas directas
   - Configurará permisos y políticas de seguridad
   - Optimizará para archivos grandes (multipart uploads)
   - Aplicará todas las mejores prácticas

**Resultado**: Almacenamiento en cloud configurado correctamente que es seguro y eficiente.

### Ejemplo 3: Manejar Subidas de Archivos Grandes
**Situación**: Necesitas permitir subidas de archivos grandes sin bloquear el servidor.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero manejar subidas de archivos grandes"
2. Cursor:
   - Implementará subidas multipart para archivos grandes
   - Usará presigned URLs para subidas directas al cloud
   - Configurará timeouts apropiados
   - Implementará progreso de subida
   - Optimizará para no bloquear el servidor

**Resultado**: Sistema que puede manejar archivos grandes eficientemente sin bloquear el servidor.
