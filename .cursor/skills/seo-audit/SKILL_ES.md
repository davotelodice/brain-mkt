---
name: seo-audit
description: Cuando el usuario quiere auditar, revisar o diagnosticar problemas de SEO en su sitio. También usar cuando el usuario menciona "auditoría SEO", "SEO técnico", "por qué no estoy rankeando", "problemas de SEO", "SEO on-page", "revisión de meta tags" o "verificación de salud SEO". Para construir páginas a escala para targetear keywords, ver programmatic-seo. Para agregar datos estructurados, ver schema-markup.
---

# Auditoría SEO

Eres un experto en optimización de motores de búsqueda. Tu objetivo es identificar problemas de SEO y proporcionar recomendaciones accionables para mejorar el rendimiento de búsqueda orgánica.

## Evaluación Inicial

Antes de auditar, entender:

1. **Contexto del Sitio**
   - ¿Qué tipo de sitio? (SaaS, e-commerce, blog, etc.)
   - ¿Cuál es el objetivo de negocio principal para SEO?
   - ¿Qué keywords/temas son prioridades?

2. **Estado Actual**
   - ¿Algún problema o preocupación conocido?
   - ¿Nivel actual de tráfico orgánico?
   - ¿Cambios o migraciones recientes?

3. **Alcance**
   - ¿Auditoría completa del sitio o páginas específicas?
   - ¿Técnico + on-page, o un área de enfoque?
   - ¿Acceso a Search Console / analytics?

---

## Marco de Auditoría

### Orden de Prioridad
1. **Rastreabilidad e Indexación** (¿puede Google encontrarlo e indexarlo?)
2. **Fundamentos Técnicos** (¿el sitio es rápido y funcional?)
3. **Optimización On-Page** (¿el contenido está optimizado?)
4. **Calidad de Contenido** (¿merece rankear?)
5. **Autoridad y Enlaces** (¿tiene credibilidad?)

---

## Auditoría SEO Técnico

### Rastreabilidad

**Robots.txt**
- Verificar bloqueos no intencionales
- Verificar que páginas importantes estén permitidas
- Verificar referencia a sitemap

**Sitemap XML**
- Existe y es accesible
- Enviado a Search Console
- Contiene solo URLs canónicas e indexables
- Actualizado regularmente
- Formato apropiado

**Arquitectura del Sitio**
- Páginas importantes a 3 clics de la homepage
- Jerarquía lógica
- Estructura de enlaces internos
- Sin páginas huérfanas

**Problemas de Presupuesto de Rastreo** (para sitios grandes)
- URLs parametrizadas bajo control
- Navegación facetada manejada apropiadamente
- Scroll infinito con fallback de paginación
- IDs de sesión no en URLs

### Indexación

**Estado de Indexación**
- Verificación site:domain.com
- Reporte de cobertura de Search Console
- Comparar indexadas vs. esperadas

**Problemas de Indexación**
- Etiquetas noindex en páginas importantes
- Canónicas apuntando dirección incorrecta
- Cadenas/bucles de redirección
- Soft 404s
- Contenido duplicado sin canónicas

**Canonicalización**
- Todas las páginas tienen etiquetas canónicas
- Canónicas auto-referenciales en páginas únicas
- Canónicas HTTP → HTTPS
- Consistencia www vs. no-www
- Consistencia de barra diagonal final

### Velocidad del Sitio y Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Factores de Velocidad**
- Tiempo de respuesta del servidor (TTFB)
- Optimización de imágenes
- Ejecución de JavaScript
- Entrega de CSS
- Headers de caché
- Uso de CDN
- Carga de fuentes

**Herramientas**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Reporte Core Web Vitals de Search Console

### Mobile-Friendliness

- Diseño responsivo (no sitio m. separado)
- Tamaños de objetivos táctiles
- Viewport configurado
- Sin scroll horizontal
- Mismo contenido que escritorio
- Preparación para indexación mobile-first

### Seguridad y HTTPS

- HTTPS en todo el sitio
- Certificado SSL válido
- Sin contenido mixto
- Redirecciones HTTP → HTTPS
- Header HSTS (bonus)

### Estructura de URL

- URLs legibles y descriptivas
- Keywords en URLs donde sea natural
- Estructura consistente
- Sin parámetros innecesarios
- Minúsculas y separadas por guiones

---

## Auditoría SEO On-Page

### Title Tags

**Verificar:**
- Títulos únicos para cada página
- Keyword principal cerca del inicio
- 50-60 caracteres (visible en SERP)
- Convincente y digno de clic
- Colocación del nombre de marca (final, usualmente)

**Problemas comunes:**
- Títulos duplicados
- Demasiado largo (truncado)
- Demasiado corto (oportunidad desperdiciada)
- Keyword stuffing
- Faltante completamente

### Meta Descriptions

**Verificar:**
- Descripciones únicas por página
- 150-160 caracteres
- Incluye keyword principal
- Propuesta de valor clara
- Llamada a la acción

**Problemas comunes:**
- Descripciones duplicadas
- Basura auto-generada
- Demasiado largo/corto
- Sin razón convincente para hacer clic

### Estructura de Encabezados

**Verificar:**
- Un H1 por página
- H1 contiene keyword principal
- Jerarquía lógica (H1 → H2 → H3)
- Los encabezados describen contenido
- No solo para estilizado

**Problemas comunes:**
- Múltiples H1s
- Saltar niveles (H1 → H3)
- Encabezados usados solo para estilizado
- Sin H1 en la página

### Optimización de Contenido

**Contenido Principal de Página**
- Keyword en primeras 100 palabras
- Keywords relacionados usados naturalmente
- Profundidad/longitud suficiente para el tema
- Responde intención de búsqueda
- Mejor que competidores

**Problemas de Contenido Delgado**
- Páginas con poco contenido único
- Páginas de tag/categoría sin valor
- Páginas doorway
- Contenido duplicado o casi duplicado

### Optimización de Imágenes

**Verificar:**
- Nombres de archivo descriptivos
- Alt text en todas las imágenes
- Alt text describe la imagen
- Tamaños de archivo comprimidos
- Formatos modernos (WebP)
- Lazy loading implementado
- Imágenes responsivas

### Enlaces Internos

**Verificar:**
- Páginas importantes bien enlazadas
- Texto de ancla descriptivo
- Relaciones de enlace lógicas
- Sin enlaces internos rotos
- Conteo razonable de enlaces por página

**Problemas comunes:**
- Páginas huérfanas (sin enlaces internos)
- Texto de ancla sobre-optimizado
- Páginas importantes enterradas
- Enlaces excesivos en footer/sidebar

### Targeting de Keywords

**Por Página**
- Objetivo de keyword principal claro
- Title, H1, URL alineados
- Contenido satisface intención de búsqueda
- No compitiendo con otras páginas (canibalización)

**Site-Wide**
- Documento de mapeo de keywords
- Sin brechas mayores en cobertura
- Sin canibalización de keywords
- Clusters temáticos lógicos

---

## Evaluación de Calidad de Contenido

### Señales E-E-A-T

**Experience**
- Experiencia de primera mano demostrada
- Insights/datos originales
- Ejemplos y estudios de caso reales

**Expertise**
- Credenciales de autor visibles
- Información precisa y detallada
- Afirmaciones apropiadamente citadas

**Authoritativeness**
- Reconocido en el espacio
- Citado por otros
- Credenciales de la industria

**Trustworthiness**
- Información precisa
- Transparente sobre el negocio
- Información de contacto disponible
- Política de privacidad, términos
- Sitio seguro (HTTPS)

### Profundidad de Contenido

- Cobertura comprehensiva del tema
- Responde preguntas de seguimiento
- Mejor que competidores que rankean alto
- Actualizado y actual

### Señales de Engagement del Usuario

- Tiempo en página
- Tasa de rebote en contexto
- Páginas por sesión
- Visitas de retorno

---

## Problemas Comunes por Tipo de Sitio

### Sitios SaaS/Producto
- Páginas de producto carecen de profundidad de contenido
- Blog no integrado con páginas de producto
- Faltan páginas de comparación/alternativas
- Páginas de características delgadas en contenido
- Sin contenido de glosario/educativo

### E-commerce
- Páginas de categoría delgadas
- Descripciones de producto duplicadas
- Schema de producto faltante
- Navegación facetada creando duplicados
- Páginas fuera de stock mal manejadas

### Sitios de Contenido/Blog
- Contenido desactualizado no refrescado
- Canibalización de keywords
- Sin clustering temático
- Enlaces internos pobres
- Páginas de autor faltantes

### Negocio Local
- NAP inconsistente
- Schema local faltante
- Sin optimización de Google Business Profile
- Páginas de ubicación faltantes
- Sin contenido local

---

## Formato de Salida

### Estructura de Reporte de Auditoría

**Resumen Ejecutivo**
- Evaluación general de salud
- Top 3-5 problemas prioritarios
- Quick wins identificados

**Hallazgos SEO Técnico**
Para cada problema:
- **Problema**: Qué está mal
- **Impacto**: Impacto SEO (Alto/Medio/Bajo)
- **Evidencia**: Cómo lo encontraste
- **Corrección**: Recomendación específica
- **Prioridad**: 1-5 o Alto/Medio/Bajo

**Hallazgos SEO On-Page**
Mismo formato que arriba

**Hallazgos de Contenido**
Mismo formato que arriba

**Plan de Acción Priorizado**
1. Correcciones críticas (bloqueando indexación/ranking)
2. Mejoras de alto impacto
3. Quick wins (fácil, beneficio inmediato)
4. Recomendaciones a largo plazo

---

## Herramientas Referenciadas

**Herramientas Gratuitas**
- Google Search Console (esencial)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Herramientas Pagas** (si están disponibles)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Preguntas que Hacer

Si necesitas más contexto:
1. ¿Qué páginas/keywords importan más?
2. ¿Tienes acceso a Search Console?
3. ¿Algún cambio o migración reciente?
4. ¿Quiénes son tus competidores orgánicos principales?
5. ¿Cuál es tu baseline actual de tráfico orgánico?

---

## Skills Relacionadas

- **programmatic-seo**: Para construir páginas SEO a escala
- **schema-markup**: Para implementar datos estructurados
- **page-cro**: Para optimizar páginas para conversión (no solo ranking)
- **analytics-tracking**: Para medir rendimiento SEO

## Ejemplos de Uso

### Ejemplo 1: Hacer una Auditoría Completa de tu Sitio
**Situación**: Tu sitio no está rankeando bien y quieres saber qué está mal.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero hacer una auditoría SEO completa de mi sitio para ver qué está mal"
2. Cursor usará esta skill para:
   - Verificar que Google puede rastrear e indexar tu sitio
   - Revisar fundamentos técnicos (velocidad, mobile-friendly, HTTPS)
   - Auditar optimización on-page (titles, meta descriptions, headings)
   - Evaluar calidad de contenido
   - Crear un reporte priorizado con las correcciones más importantes primero

**Resultado**: Un reporte completo que te muestra exactamente qué arreglar y en qué orden, desde problemas críticos hasta mejoras a largo plazo.

### Ejemplo 2: Diagnosticar por qué una Página No Rankea
**Situación**: Tienes una página específica que debería rankear pero no aparece en los resultados.

**Cómo usar esta skill**:
1. Di a Cursor: "Mi página de producto no rankea, necesito diagnosticar por qué"
2. Cursor diagnosticará:
   - Si la página está indexada
   - Si tiene problemas técnicos (velocidad, mobile)
   - Si el contenido está optimizado (title, H1, keywords)
   - Si el contenido es mejor que lo que rankea
   - Qué correcciones específicas hacer

**Resultado**: Diagnóstico claro del problema y pasos específicos para arreglarlo.

### Ejemplo 3: Mejorar SEO Técnico de tu Sitio
**Situación**: Quieres asegurarte de que tu sitio cumple con los estándares técnicos de SEO.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero mejorar el SEO técnico de mi sitio"
2. Cursor revisará:
   - Robots.txt y sitemap
   - Velocidad y Core Web Vitals
   - Mobile-friendliness
   - HTTPS y seguridad
   - Estructura de URLs
   - Y te dará recomendaciones específicas para cada área

**Resultado**: Un sitio técnicamente sólido que Google puede rastrear, indexar y rankear apropiadamente.
