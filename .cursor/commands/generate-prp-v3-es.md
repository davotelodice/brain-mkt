# Crear PRP v3 - Con MCPs y Skills Integrados

## 🎯 Archivo de Feature: $ARGUMENTS

Generar un PRP completo para implementación de features con investigación exhaustiva usando **MCPs (Archon, Serena) y Skills**. Asegurar que el contexto permita auto-validación e iteración refinada del agente de IA.

**IMPORTANTE**: Este comando usa el nuevo template `prp_base_nuevo.md` que integra:
- 🎯 **MCP Archon**: Base de datos RAG con documentación oficial (PRIORIDAD)
- ⚡ **MCP Serena**: Análisis simbólico de código (OBLIGATORIO)
- **MCP FAL**: ver documentacion oficial de la api de video (en caso de requerirse para el proyecto)
- 📚 **Skills**: Por fase del proyecto (Planificación, Desarrollo, Testing, etc.) /home/david/brain-mkt/skills_index.json

---

## 📖 Proceso de Investigación Mejorado

### FASE 0: Revisar Ejemplos de Referencia (OPCIONAL)

**⚠️ EJECUTAR SOLO SI LA CARPETA TIENE CONTENIDO**

```yaml
Ubicación: Context-Engineering-Intro/examples/

Propósito: Aprender de proyectos similares antes de diseñar

Pasos:
  1. Listar archivos en carpeta:
     comando: ls Context-Engineering-Intro/examples/
  
  2. SI carpeta vacía:
     - Continuar a FASE 1 directamente
     - No perder tiempo buscando ejemplos
  
  3. SI hay archivos:
     - Identificar los más relevantes al proyecto actual
     - Decidir método de lectura:
       
       Opción A - Con Serena (si es código):
         comando: get_symbols_overview('Context-Engineering-Intro/examples/')
         luego: find_symbol() para partes específicas
       
       Opción B - Lectura directa (archivos pequeños/docs):
         comando: Leer archivos directamente
  
  4. Extraer información útil:
     - Estructura de proyecto
     - Decisiones de arquitectura
     - Stack tecnológico usado
     - Patrones de código
     - Configuraciones importantes
     - Gotchas mencionados
  
  5. Anotar insights para aplicar:
     - Patrones reutilizables
     - Problemas a evitar
     - Mejores prácticas observadas

Tiempo máximo: 5 minutos

IMPORTANTE: Si ejemplos no son relevantes, NO forzar su uso
```

---

### FASE 1: Análisis del Archivo de Feature

**Lee `$ARGUMENTS` para entender:**
- ¿Qué necesita ser creado?
- ¿Cómo ayudan los ejemplos proporcionados? (si se leyeron en FASE 0)
- ¿Qué consideraciones especiales hay?

---

### FASE 2: Consulta de Documentación con Archon 🎯

**⚡ PRIORIDAD MÁXIMA - USAR ANTES QUE WEB SEARCH**

```yaml
Paso 1 - Obtener fuentes disponibles:
  comando: rag_get_available_sources()
  objetivo: Ver qué documentación oficial está disponible
  resultado: Lista con source_id, title, url de cada fuente

Paso 2 - Buscar documentación específica:
  comando: |
    rag_search_knowledge_base(
        query="keywords cortos 2-5 palabras",
        source_id="src_xxx",  # Del paso 1
        match_count=5-10
    )
  tips:
    - "✅ BUENO: 'FastAPI JWT authentication'"
    - "❌ MALO: 'cómo implementar autenticación JWT con FastAPI...'"
    - "Siempre usar source_id cuando sepas la fuente"

Paso 3 - Buscar ejemplos de código:
  comando: |
    rag_search_code_examples(
        query="pydantic validator custom",
        source_id="src_pydantic_456",
        match_count=3-5
    )
  cuándo: "Después de entender conceptos, necesitas ver implementaciones"

Paso 4 - URLs externos (SOLO SI ARCHON NO TIENE):
  nota: "Último recurso - Archon tiene Python, Pydantic, FastAPI, Supabase, Next.js, React, TypeScript completos"
  acción: "Incluir URLs específicas con secciones exactas a consultar"
```

**Documentación disponible en Archon:**
- Python (libros completos, PEPs, guías)
- Pydantic v2 (docs + ejemplos)
- FastAPI (tutorial + API reference completo)
- Supabase (documentación completa)
- Next.js, React, Node.js, TypeScript
- Y muchas más fuentes oficiales

---

### FASE 3: Análisis del Codebase con Serena ⚡

**⚡ CRÍTICO - NO LEER ARCHIVOS COMPLETOS**

```yaml
Filosofía:
  - "❌ NO leer archivos completos innecesariamente"
  - "✅ Usar get_symbols_overview para ver estructura PRIMERO"
  - "✅ Usar find_symbol para leer SOLO lo necesario"
  - "✅ Ediciones simbólicas para cambios quirúrgicos"

Paso 1 - Buscar features/patrones similares:
  comando: |
    # Buscar por patrón si no sabes ubicación
    search_for_pattern('async def.*authenticate', 'src/')
    
  resultado: "Lista de ubicaciones con el patrón"

Paso 2 - Ver estructura de archivos relevantes:
  comando: |
    # Ver qué contiene sin leer todo
    get_symbols_overview('src/api/auth.py')
    
  resultado: "Lista de funciones, clases, métodos (sin bodies)"

Paso 3 - Leer símbolos específicos necesarios:
  comando: |
    # Leer solo el símbolo que necesitas
    find_symbol(
        name_path='AuthService/login',
        relative_path='src/api/auth.py',
        include_body=True
    )
    
  resultado: "Implementación del símbolo específico"

Paso 4 - Entender relaciones y dependencias:
  comando: |
    # Ver dónde se usa este símbolo
    find_referencing_symbols(
        name_path='AuthService',
        relative_path='src/api/auth.py'
    )
    
  resultado: "Snippets de código donde se referencia + info simbólica"

Paso 5 - Identificar para el PRP:
  - Archivos a referenciar (path + propósito específico)
  - Patrones existentes a seguir
  - Convenciones del proyecto
  - Gotchas y quirks encontrados
```

**⚠️ IMPORTANTE**: Usa Serena `get_symbols_overview` ANTES de leer archivos completos

---

### FASE 4: Identificación de Skills Relevantes 📚

```yaml
Revisar qué Skills son necesarias según la fase:

PLANIFICACIÓN (antes de codificar):
  - planning-with-files: Si tarea compleja multi-paso (>5 tool calls)
  - brainstorming: OBLIGATORIO antes de features nuevas
  - architecture: Si hay decisiones arquitectónicas
  - writing-plans: Si hay spec/requisitos para multi-paso

DESARROLLO:
  - clean-code: Siempre al escribir código
  - python-patterns: Si proyecto Python
  - react-patterns: Si proyecto React
  - nextjs-best-practices: Si proyecto Next.js
  - [framework específico]: Según stack tecnológico

DOCUMENTACIÓN:
  - documentation-templates: Para README, API docs
  - doc-coauthoring: Para specs técnicas, propuestas

TESTING:
  - test-driven-development: ANTES de escribir implementación
  - test-fixing: Si hay tests fallando
  - testing-patterns: Para patrones Jest, mocking

VALIDACIÓN:
  - lint-and-validate: DESPUÉS de cada modificación
  - verification-before-completion: Antes de declarar completitud
  - systematic-debugging: Si hay bugs/comportamiento inesperado
```

---

### FASE 5: Clarificación con Usuario (si necesario)

**Preguntar solo si:**
- Hay ambigüedad en requisitos que Archon o Serena no resuelven
- Múltiples patrones válidos y no está claro cuál seguir
- Decisiones de negocio que requieren input

**NO preguntar si:**
- Archon tiene la documentación
- Serena puede encontrar el patrón en el codebase
- Es decisión técnica estándar

---

## 🏗️ Generación del PRP

### Usar como template: `PRPs/templates/prp_base_nuevo.md`

### ✅ Contexto Crítico a Incluir

```yaml
1. DOCUMENTACIÓN (con Archon):
   prioridad: MÁXIMA
   método: |
     - Primero: rag_get_available_sources()
     - Segundo: rag_search_knowledge_base() con source_id
     - Tercero: rag_search_code_examples() si necesario
   incluir_en_prp:
     - Source IDs relevantes
     - Queries exactas usadas
     - Resultados clave encontrados
   
   solo_si_archon_no_tiene:
     - URLs específicas con secciones exactas
     - Nota: "Archon no tiene esta información"

2. ANÁLISIS DE CODEBASE (con Serena):
   método: |
     - get_symbols_overview() para estructura
     - find_symbol() para símbolos específicos
     - search_for_pattern() para búsquedas
   incluir_en_prp:
     - Paths de archivos relevantes
     - Símbolos a seguir como patrón (name_path)
     - Convenciones encontradas
     - Comandos Serena para que el agente replique análisis
   
   prohibido:
     - "❌ NO incluir archivos completos leídos manualmente"
     - "✅ SÍ incluir comandos Serena para análisis"

3. GOTCHAS Y QUIRKS:
   incluir:
     - Quirks de librerías (versiones, configuraciones)
     - Gotchas del proyecto específico
     - Patrones que DEBEN seguirse
     - Anti-patrones a evitar
   formato:
     ```python
     # CRÍTICO: [Librería] requiere [setup específico]
     # GOTCHA: [Comportamiento no obvio]
     # PATRÓN: [Enfoque que debe seguirse]
     ```

4. SKILLS A ACTIVAR:
   incluir:
     - Lista de skills por fase con justificación
     - Cuándo llamar cada skill
     - Por qué es importante en este contexto
   ejemplo:
     ```yaml
     Skill: brainstorming
       cuándo: "Antes de implementar nueva feature"
       por_qué: "Explorar requisitos antes de codificar"
       obligatorio: true
     ```
```

---

### 📝 Blueprint de Implementación

```yaml
TAREA 0 (SIEMPRE INCLUIR):
  nombre: "Instalar y configurar MCP Serena"
  herramientas:
    - MCP Archon: "Consultar instalación de MCPs"
    - MCP Serena: "Onboarding del proyecto"
    - Skill environment-setup-guide: "Setup correcto"
  objetivo: "Serena activo para análisis simbólico"
  criterios:
    - "Serena activo en proyecto"
    - "Puede ejecutar get_symbols_overview"
    - "Onboarding completado"

TAREAS 1-N (estructura mejorada):
  formato: |
    Tarea N: [NOMBRE_DESCRIPTIVO]
    
    Herramientas a utilizar:
      - ⚡ MCP Archon: [Query específica]
        Importancia: "[Razón específica]"
        Comando: rag_search_knowledge_base(query="...", source_id="...", match_count=5)
      
      - 🔧 MCP Serena: [Herramienta específica]
        Importancia: "[Razón específica]"
        Comando: get_symbols_overview('path/to/file.py')
      
      - 📚 Skills: [Lista con justificación]
        Importancia: "[Capacidad que aporta]"
    
    Objetivo:
      [Resultado esperado claro y medible]
    
    Pasos a seguir:
      1. [Paso con comando específico de MCP/Skill]
      2. [Siguiente paso con herramienta específica]
      3. [Validación con skill correspondiente]
    
    Criterios de aceptación:
      - [ ] [Criterio medible 1]
      - [ ] [Criterio medible 2]
      - [ ] [Tests pasan]
      - [ ] [Linting OK]
    
    Archivos a crear:
      - path/to/new/file.py - [Propósito específico]
    
    Archivos a modificar:
      - path/to/existing.py - [Qué cambiar y por qué]
    
    Pseudocódigo (con gotchas):
      ```python
      # PATRÓN: [Patrón del proyecto a seguir]
      async def nueva_funcion(param: str) -> Result:
          # GOTCHA: [Quirk de librería]
          # CRÍTICO: [Limitación importante]
          ...
      ```
    
    Comandos de validación:
      ```bash
      pytest tests/test_tarea_n.py -v
      ruff check src/ --fix
      mypy src/
      ```

PSEUDOCÓDIGO:
  incluir:
    - Enfoque general con patrones
    - Referencias a archivos para seguir
    - Gotchas críticos marcados
    - NO código completo (solo estructura)
  
  ejemplo:
    ```python
    # PATRÓN: Siempre validar input (ver src/validators.py)
    async def process_payment(data: PaymentData) -> Result:
        # GOTCHA: Esta librería requiere connection pooling
        async with get_connection() as conn:
            # CRÍTICO: API retorna 429 si >10 req/sec
            await rate_limiter.acquire()
            return await external_api.call(data)
    ```

MANEJO DE ERRORES:
  estrategia: [Enfoque general]
  patrones: [Patrones del proyecto a seguir]
  logging: [Nivel y formato esperado]
```

---

### ✅ Gates de Validación (Ejecutables por IA)

```yaml
Nivel 1: Sintaxis & Estilo
  comandos: |
    ruff check src/ --fix
    mypy src/
  esperado: "Sin errores. Si hay, LEER y ARREGLAR"

Nivel 2: Tests Unitarios
  crear: "test_nueva_feature.py con casos:"
  casos_mínimos:
    - test_happy_path: "Funcionalidad básica"
    - test_validation_error: "Input inválido"
    - test_error_handling: "Manejo de errores"
  comando: "pytest test_nueva_feature.py -v"
  proceso: "Ejecutar, leer error, entender, arreglar, re-ejecutar"

Nivel 3: Test de Integración
  pasos:
    1. "Iniciar servicio: python -m src.main --dev"
    2. "Probar endpoint con curl [comando específico]"
    3. "Verificar logs: logs/app.log"
  esperado: "[Respuesta específica exitosa]"
```

---

## 💾 Guardar PRP

```bash
Ubicación: PRPs/{feature-name}-v3.md
Formato: Markdown con sintaxis YAML para estructura de tareas
Incluir: Metadata al inicio (name, version, descripcion)
```

---

## ✅ Checklist de Calidad PRP

```yaml
Contexto y Documentación:
  - [ ] Archon consultado PRIMERO (rag_get_available_sources + rag_search_knowledge_base)
  - [ ] Source IDs y queries incluidos en PRP
  - [ ] URLs solo si Archon no tiene la info
  - [ ] Documentación específica (no genérica)

Análisis de Codebase:
  - [ ] Serena usado para análisis simbólico (NO lectura completa)
  - [ ] Comandos Serena incluidos para que agente replique
  - [ ] Patrones existentes identificados y referenciados
  - [ ] Convenciones del proyecto documentadas
  - [ ] Tests patterns identificados

Skills y MCPs:
  - [ ] Tarea 0: Instalación Serena incluida
  - [ ] Skills relevantes identificadas por fase
  - [ ] Justificación de cada skill incluida
  - [ ] MCPs integrados en estructura de tareas

Implementación:
  - [ ] Tareas con estructura completa (herramientas, pasos, criterios)
  - [ ] Comandos específicos de MCPs en cada tarea
  - [ ] Pseudocódigo con gotchas y patrones
  - [ ] Archivos a crear/modificar con propósitos claros

Validación:
  - [ ] 3 niveles de validación definidos
  - [ ] Comandos ejecutables por IA incluidos
  - [ ] Criterios de aceptación medibles
  - [ ] Proceso de iteración claro

Gotchas y Anti-patrones:
  - [ ] Quirks de librerías documentados
  - [ ] Gotchas del proyecto incluidos
  - [ ] Anti-patrones a evitar listados
  - [ ] Versiones específicas mencionadas

Calidad General:
  - [ ] Referencias claras a código existente
  - [ ] Path de implementación claro
  - [ ] Error handling documentado
  - [ ] Todos los pasos verificables
```

---

## 📊 Score de Confianza

**Evaluar el PRP en escala 1-10:**

```yaml
Criterios de Scoring:
  10/10: "Implementación one-pass garantizada"
    - Archon consultado exhaustivamente
    - Serena usado para análisis completo
    - Todas las skills relevantes incluidas
    - Estructura de tareas completa con comandos
    - Validación en 3 niveles
    - Gotchas y anti-patrones documentados
  
  7-9/10: "Alta probabilidad one-pass"
    - Contexto suficiente pero puede faltar detalle
    - MCPs usados pero no exhaustivamente
    - Skills mayormente identificadas
  
  4-6/10: "Requiere iteración"
    - Contexto incompleto
    - MCPs poco aprovechados
    - Skills no identificadas
  
  1-3/10: "Alto riesgo de fallos"
    - Contexto insuficiente
    - MCPs no usados
    - Sin estructura clara

Objetivo: Mínimo 8/10, ideal 9-10/10
```

---

## 🎯 Meta Final

**Implementación exitosa en un solo paso (one-pass) a través de:**
1. ✅ Contexto exhaustivo con Archon RAG
2. ✅ Análisis simbólico inteligente con Serena
3. ✅ Skills activadas en momento correcto
4. ✅ Estructura de tareas con comandos específicos
5. ✅ Validación en 3 niveles ejecutable
6. ✅ Gotchas y anti-patrones documentados

**Recuerda**: Un agente de IA solo tiene el contexto que le das + training data. Tu PRP debe ser tan completo que el agente pueda ejecutar sin preguntar.

---

## 🚨 CRÍTICO: ANTES DE ESCRIBIR EL PRP

### ⚡ ULTRATHINK SOBRE EL PRP

**Pausa y reflexiona:**
1. ¿Consulté Archon exhaustivamente?
2. ¿Usé Serena para análisis simbólico?
3. ¿Identifiqué todas las skills relevantes?
4. ¿Incluí Tarea 0 de instalación Serena?
5. ¿Las tareas tienen comandos específicos de MCPs?
6. ¿Los criterios de aceptación son medibles?
7. ¿Documenté todos los gotchas encontrados?
8. ¿El agente puede ejecutar sin más contexto?

**Solo cuando TODO sea ✅, comienza a escribir el PRP**

---

## 📚 Referencias

- Template base: `PRPs/templates/prp_base_nuevo.md`
- Ejemplo completo: `PRPs/EXAMPLE_multi_agent_prp.md`
- MCPs disponibles: Archon (docs), Serena (código), browser (testing)
- Skills disponibles: 600+ en `skills_index.json`
