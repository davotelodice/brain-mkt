---
name: content-creator
description: Crear contenido de marketing optimizado para SEO con voz de marca consistente. Incluye analizador de voz de marca, optimizador SEO, frameworks de contenido y plantillas de redes sociales. Usar al escribir posts de blog, crear contenido de redes sociales, analizar voz de marca, optimizar SEO, planificar calendarios de contenido o cuando el usuario menciona creación de contenido, voz de marca, optimización SEO, marketing de redes sociales o estrategia de contenido.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Creador de Contenido

Análisis de voz de marca de grado profesional, optimización SEO y frameworks de contenido específicos de plataforma.

## Inicio Rápido

### Para Desarrollo de Voz de Marca
1. Ejecutar `scripts/brand_voice_analyzer.py` en contenido existente para establecer baseline
2. Revisar `references/brand_guidelines.md` para seleccionar atributos de voz
3. Aplicar voz elegida consistentemente a través de todo el contenido

### Para Creación de Contenido de Blog
1. Elegir plantilla de `references/content_frameworks.md`
2. Investigar keywords para tema
3. Escribir contenido siguiendo estructura de plantilla
4. Ejecutar `scripts/seo_optimizer.py [archivo] [keyword-primario]` para optimizar
5. Aplicar recomendaciones antes de publicar

### Para Contenido de Redes Sociales
1. Revisar mejores prácticas de plataforma en `references/social_media_optimization.md`
2. Usar plantilla apropiada de `references/content_frameworks.md`
3. Optimizar basado en guías específicas de plataforma
4. Programar usando `assets/content_calendar_template.md`

## Workflows Centrales

### Establecer Voz de Marca (Configuración Inicial)

Cuando crear contenido para una marca o cliente nueva:

1. **Analizar Contenido Existente** (si disponible)
2. **Definir Atributos de Voz**
   - Revisar arquetipos de personalidad de marca
   - Seleccionar arquetipos primarios y secundarios
   - Elegir 3-5 atributos de tono
   - Documentar en guías de marca

3. **Crear Muestra de Voz**
   - Escribir 3 piezas de muestra en voz elegida
   - Probar consistencia usando analizador
   - Refinar basado en resultados

### Crear Posts de Blog Optimizados para SEO

1. **Investigación de Keywords**
   - Identificar keyword primario (volumen de búsqueda 500-5000/mes)
   - Encontrar 3-5 keywords secundarios
   - Listar 10-15 keywords LSI

2. **Estructura de Contenido**
   - Usar plantilla de blog
   - Incluir keyword en título, primer párrafo y 2-3 H2s
   - Apuntar a 1,500-2,500 palabras para cobertura comprehensiva

3. **Verificación de Optimización**
   - Ejecutar seo_optimizer.py
   - Aplicar recomendaciones SEO

### Creación de Contenido de Redes Sociales

1. **Selección de Plataforma**
   - Identificar plataformas primarias basadas en audiencia
   - Revisar guías específicas de plataforma

2. **Adaptación de Contenido**
   - Comenzar con post de blog o mensaje central
   - Usar matriz de reutilización
   - Adaptar para cada plataforma siguiendo plantillas

3. **Lista de Verificación de Optimización**
   - Longitud apropiada para plataforma
   - Tiempo de publicación óptimo
   - Dimensiones de imagen correctas
   - Hashtags específicos de plataforma
   - Elementos de engagement (polls, preguntas)

## Scripts Clave

### brand_voice_analyzer.py
Analiza contenido de texto para características de voz, legibilidad y consistencia.

**Uso**: `python scripts/brand_voice_analyzer.py <archivo> [json|text]`

### seo_optimizer.py
Analiza contenido para optimización SEO y proporciona recomendaciones accionables.

**Uso**: `python scripts/seo_optimizer.py <archivo> [keyword_primario] [keywords_secundarios]`

## Ejemplos de Uso

### Ejemplo 1: Crear Contenido de Blog Optimizado para SEO
**Situación**: Quieres escribir un post de blog que rankee bien en búsquedas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un post de blog optimizado para SEO sobre [tema]"
2. Cursor usará esta skill para:
   - Investigar keywords apropiadas
   - Usar framework de contenido apropiado
   - Escribir contenido siguiendo mejores prácticas SEO
   - Optimizar con seo_optimizer.py
   - Aplicar voz de marca consistente
   - Aplicar todas las mejores prácticas

**Resultado**: Post de blog optimizado para SEO que rankea bien y mantiene voz de marca.

### Ejemplo 2: Crear Contenido para Redes Sociales
**Situación**: Quieres crear contenido de redes sociales que se adapte a diferentes plataformas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear contenido de redes sociales para [plataformas]"
2. Cursor:
   - Usará plantillas específicas de plataforma
   - Adaptará contenido para cada plataforma
   - Optimizará según mejores prácticas de cada plataforma
   - Mantendrá voz de marca consistente
   - Aplicará todas las optimizaciones

**Resultado**: Contenido de redes sociales optimizado para cada plataforma que mantiene consistencia de marca.

### Ejemplo 3: Establecer Voz de Marca para tu Contenido
**Situación**: Quieres establecer una voz de marca consistente para todo tu contenido.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero establecer voz de marca para mi contenido"
2. Cursor:
   - Analizará contenido existente si hay
   - Te ayudará a definir atributos de voz
   - Creará muestras de voz
   - Verificará consistencia
   - Te dará guías de voz de marca

**Resultado**: Voz de marca establecida que puedes aplicar consistentemente a todo tu contenido.
