# Ejecutar PRP v3 - Con MCPs y Skills Integrados

## 🎯 Archivo PRP: $ARGUMENTS

Implementar una feature usando el archivo PRP con integración completa de **MCPs (Archon, Serena) y Skills**.

**IMPORTANTE**: Esta versión v3 está diseñada para ejecutar PRPs generados con `generate-prp-v3.md` que incluyen:
- 🎯 **MCP Archon**: Documentación oficial via RAG
- ⚡ **MCP Serena**: Análisis simbólico de código
- 📚 **Skills**: Guías expertas por fase
- 📝 **Estructura detallada**: Tareas con comandos específicos

---

## 📋 Proceso de Ejecución

### FASE 0: Preparación y Verificación ⚙️

#### 0.1 Cargar y Analizar PRP
```yaml
Acciones:
  1. Leer el archivo PRP completo especificado en $ARGUMENTS
  2. Identificar todas las secciones:
     - Objetivo y contexto
     - Skills requeridas
     - MCPs a utilizar
     - Lista de tareas (incluyendo Tarea 0)
     - Criterios de validación
     - Anti-patrones a evitar
  
  3. Entender requisitos globales del proyecto
  
  4. [OPCIONAL] Revisar ejemplos si PRP los menciona:
     - Ubicación: Context-Engineering-Intro/examples/
     - SI PRP dice "ver ejemplos en X" → leer ese ejemplo específico
     - Usar Serena para análisis simbólico si es código
     - Extraer patrones aplicables a la tarea actual
```

#### 0.2 Verificar MCPs Disponibles
```yaml
Verificar Archon:
  - comando: rag_get_available_sources()
  - esperado: Lista de fuentes disponibles
  - si_falla: "Archon MCP no está disponible. Revisar configuración de Cursor"

Verificar Serena:
  - nota: "Se instalará en Tarea 0, pero verificar que esté en configuración"
  - ubicación: "Debería estar en configuración de MCPs de Cursor"
```

#### 0.3 Identificar Skills Requeridas
```yaml
Para cada skill mencionada en el PRP:
  - Anotar nombre de la skill
  - Anotar ubicación: .cursor/skills/[nombre-skill]/SKILL.md
  - Anotar cuándo debe usarse (fase del proyecto)
  - Anotar método de invocación:
    * Automática: keywords a mencionar
    * Manual: comando @ a usar
```

#### 0.4 Crear TODOs Basados en el PRP
```yaml
Usar herramienta TodoWrite:

TodoWrite([
  {
    id: "task-0",
    content: "Instalar y configurar MCP Serena",
    status: "pending"
  },
  {
    id: "task-1", 
    content: "[Nombre de Tarea 1 del PRP]",
    status: "pending"
  },
  {
    id: "task-2",
    content: "[Nombre de Tarea 2 del PRP]",
    status: "pending"
  },
  // ... todas las tareas del PRP
], merge=false)

Resultado: Lista de TODOs sincronizada con tareas del PRP
```

---

### FASE 1: TAREA 0 - Instalación Serena (⚡ OBLIGATORIO)

```yaml
⚠️ CRÍTICO: Esta tarea DEBE completarse antes de cualquier otra

Objetivo:
  Instalar y configurar MCP Serena para análisis simbólico de código

Pasos:
  1. Verificar que Serena está en configuración de Cursor MCP
  
  2. Activar Serena en el proyecto actual:
     - Si es primera vez: Realizar onboarding
     - Si ya existe: Verificar que está activo
  
  3. Probar funcionamiento básico:
     comando: get_symbols_overview('.')
     esperado: Vista general de símbolos en directorio raíz
  
  4. Si hay error:
     - Revisar configuración de MCP en Cursor
     - Consultar Archon: rag_search_knowledge_base(query="MCP Serena installation", match_count=5)
     - Revisar logs de Cursor

Criterios de Aceptación:
  - [ ] Serena responde a comandos
  - [ ] get_symbols_overview funciona
  - [ ] No hay errores en logs
  - [ ] Listo para usar en siguientes tareas

Actualizar TODO:
  TodoWrite([{id: "task-0", status: "completed"}], merge=true)
```

---

### FASE 2: Ejecución de Tareas del PRP 🚀

**Para CADA tarea listada en el PRP (Tarea 1, 2, 3, ... N):**

```yaml
## Estructura de Ejecución por Tarea

PASO 1 - LEER TAREA COMPLETA:
  acción: Leer toda la sección de la tarea en el PRP
  incluye:
    - Nombre y objetivo
    - Herramientas a utilizar (Archon, Serena, Skills)
    - Pasos detallados
    - Criterios de aceptación
    - Archivos a crear/modificar
    - Comandos de validación

PASO 2 - INVOCAR SKILLS REQUERIDAS:
  
  Método A - Activación Automática (Preferida):
    acción: |
      Mencionar keywords relevantes en tu pensamiento/análisis
      
      Ejemplo: "Voy a implementar esta nueva feature de autenticación,
      necesito explorar primero los requisitos y decidir la arquitectura"
      
      → El sistema detectará automáticamente:
      - "nueva feature" → activa brainstorming
      - "decidir arquitectura" → activa architecture
  
  Método B - Invocación Manual (Si necesario):
    formato: "@.cursor/skills/[nombre-skill]/SKILL.md [instrucción]"
    
    ejemplo_brainstorming: |
      @.cursor/skills/brainstorming/SKILL.md
      Explorar requisitos de la feature de autenticación
    
    ejemplo_architecture: |
      @.cursor/skills/architecture/SKILL.md
      Decidir entre JWT vs session-based authentication
    
    ejemplo_tdd: |
      @.cursor/skills/test-driven-development/SKILL.md
      Escribir tests antes de implementar el endpoint

  cuándo_usar_manual:
    - Skill no se activó automáticamente
    - Necesitas guía específica en ese momento
    - Quieres ser explícito sobre qué skill usar

PASO 3 - EJECUTAR COMANDOS DE ARCHON:
  
  si_la_tarea_menciona_archon:
    
    3.1 - Obtener fuentes (si es primera vez):
      comando: rag_get_available_sources()
      resultado: Lista con source_id de cada documentación
    
    3.2 - Buscar documentación específica:
      formato: |
        rag_search_knowledge_base(
            query="keywords cortos 2-5 palabras",
            source_id="src_xxx",  # Del PRP o del paso 3.1
            match_count=5-10
        )
      
      ejemplo: |
        rag_search_knowledge_base(
            query="FastAPI JWT auth",
            source_id="src_fastapi_123",
            match_count=5
        )
    
    3.3 - Buscar ejemplos de código (si necesario):
      comando: |
        rag_search_code_examples(
            query="pydantic validator",
            source_id="src_pydantic_456",
            match_count=3
        )
    
    3.4 - Aplicar conocimiento obtenido:
      - Leer resultados de Archon
      - Incorporar patrones oficiales
      - Seguir mejores prácticas encontradas

PASO 4 - EJECUTAR COMANDOS DE SERENA:
  
  si_la_tarea_menciona_serena:
    
    4.1 - Ver estructura de archivo (ANTES de leer completo):
      comando: get_symbols_overview('path/to/file.py')
      resultado: Lista de funciones, clases, métodos sin bodies
      usar_para: Entender qué contiene el archivo
    
    4.2 - Leer símbolo específico:
      comando: |
        find_symbol(
            name_path='ClassName/method_name',
            relative_path='path/to/file.py',
            include_body=True
        )
      usar_para: Leer solo el código necesario
    
    4.3 - Buscar por patrón (si no sabes ubicación):
      comando: search_for_pattern('async def.*login', 'src/')
      usar_para: Encontrar código similar
    
    4.4 - Ver referencias (para entender impacto):
      comando: |
        find_referencing_symbols(
            name_path='ClassName',
            relative_path='path/to/file.py'
        )
      usar_para: Ver dónde se usa el código

PASO 5 - IMPLEMENTAR SEGÚN ESTRUCTURA:
  
  5.1 - Crear archivos listados en "Archivos a crear":
    para_cada_archivo:
      - Crear con propósito documentado en el PRP
      - Seguir estructura del proyecto
      - Aplicar patrones de ejemplos (si PRP los menciona)
      - Aplicar patrones encontrados con Serena
  
  5.2 - Modificar archivos listados en "Archivos a modificar":
    para_cada_archivo:
      - Usar Serena para ver estructura primero
      - Hacer cambios quirúrgicos con find_symbol/replace_symbol_body
      - NO leer archivo completo si no es necesario
  
  5.3 - Seguir pseudocódigo con gotchas:
    - Prestar atención a comentarios CRÍTICO
    - Seguir comentarios PATRÓN
    - Evitar comentarios GOTCHA
    
    ejemplo:
      ```python
      # PATRÓN: Siempre validar input primero
      # GOTCHA: Esta API retorna 429 si >10 req/sec
      # CRÍTICO: Requiere connection pooling
      ```

PASO 6 - VALIDAR POR TAREA (3 NIVELES):
  
  Nivel 1: Sintaxis & Estilo
    comandos: |
      ruff check src/ --fix
      mypy src/
    
    esperado: "Sin errores"
    
    si_hay_errores:
      - LEER el error completo
      - ENTENDER la causa raíz
      - ARREGLAR el código
      - RE-EJECUTAR hasta que pase
  
  Nivel 2: Tests Unitarios
    si_la_tarea_tiene_tests:
      comando: pytest tests/test_tarea_n.py -v
      
      si_fallan:
        proceso: |
          1. LEER output del test
          2. ENTENDER qué está fallando
          3. NO modificar tests para que pasen
          4. ARREGLAR la implementación
          5. RE-EJECUTAR tests
          6. REPETIR hasta que todos pasen
  
  Nivel 3: Test de Integración (si aplica)
    si_la_tarea_tiene_test_integracion:
      pasos:
        1. Iniciar servicio (si necesario)
        2. Ejecutar comando de prueba (ej: curl)
        3. Verificar respuesta esperada
        4. Revisar logs si hay error

PASO 7 - ACTUALIZAR TODO:
  
  si_validacion_exitosa:
    TodoWrite([
      {
        id: "task-N",
        status: "completed"
      }
    ], merge=true)
  
  si_hay_problemas:
    - Anotar problemas encontrados
    - Documentar desviaciones del plan
    - NO marcar como completado hasta resolver

PASO 8 - CONTINUAR A SIGUIENTE TAREA:
  
  acción: Repetir PASO 1-7 para siguiente tarea del PRP
```

---

### FASE 3: Validación Final 🎯

```yaml
Después de completar TODAS las tareas del PRP:

PASO 1 - EJECUTAR CHECKLIST COMPLETO:
  
  Leer sección "Checklist de Validación Final" del PRP
  
  Verificar cada ítem (típicamente incluye):
    - [ ] Todos los tests pasan: pytest tests/ -v
    - [ ] Sin errores de linting: ruff check src/
    - [ ] Sin errores de tipos: mypy src/
    - [ ] Test manual exitoso: [comando específico del PRP]
    - [ ] Casos de error manejados gracefully
    - [ ] Logs informativos pero no verbosos
    - [ ] Documentación actualizada si fue necesario

PASO 2 - VALIDACIÓN DE 3 NIVELES COMPLETA:
  
  Ejecutar comandos finales:
    # Nivel 1: Todo el proyecto
    ruff check src/ --fix
    mypy src/
    
    # Nivel 2: Toda la suite de tests
    pytest tests/ -v --cov
    
    # Nivel 3: Tests de integración si existen
    [comandos específicos del PRP]

PASO 3 - VERIFICAR CRITERIOS DE ÉXITO:
  
  Releer sección "Criterios de Éxito" del PRP
  
  Verificar cada criterio marcado como [ ]:
    ejemplo:
      - [ ] Feature implementada y funcionando
      - [ ] Tests con 80%+ cobertura
      - [ ] Documentación actualizada
      - [ ] Sin warnings de linter

PASO 4 - REVISAR ANTI-PATRONES:
  
  Leer sección "Anti-Patrones a Evitar" del PRP
  
  Verificar que NO se cayó en ninguno:
    ejemplos_comunes:
      - ❌ Creaste nuevos patrones cuando existían
      - ❌ Saltaste validación
      - ❌ Ignoraste tests fallidos
      - ❌ Usaste sync en contexto async
      - ❌ Hardcodeaste valores
      - ❌ Leíste archivos completos sin Serena
      - ❌ Buscaste en web sin consultar Archon
```

---

### FASE 4: Completitud y Reporte 📊

```yaml
PASO 1 - RELEER PRP COMPLETO:
  
  acción: Volver a leer el PRP de inicio a fin
  
  verificar:
    - Todas las tareas completadas
    - Todos los archivos creados
    - Todos los archivos modificados
    - Todos los comandos de validación ejecutados
    - Todos los criterios de aceptación cumplidos

PASO 2 - VERIFICAR TODOS LOS TODOs:
  
  comando: [Listar TODOs]
  
  esperado: Todos con status="completed"
  
  si_hay_pending:
    - Identificar qué falta
    - Completar tareas pendientes
    - NO reportar completitud hasta que todo esté done

PASO 3 - REPORTAR MÉTRICAS:
  
  generar_reporte:
    tareas_completadas: X/X
    tests_pasando: Y/Y
    cobertura_tests: Z%
    linting_status: "✅ Sin errores"
    type_checking: "✅ Sin errores"
    integracion: "✅ Funcionando"

PASO 4 - DOCUMENTAR DESVIACIONES:
  
  si_hubo_cambios_al_plan:
    - Documentar qué se cambió
    - Explicar por qué se cambió
    - Justificar decisiones tomadas

PASO 5 - ESTADO FINAL:
  
  confirmar:
    - "✅ PRP completamente implementado"
    - "✅ Todas las validaciones pasan"
    - "✅ Todos los criterios cumplidos"
    - "✅ Ready para revisión/merge"
```

---

## 🔧 Guía de Herramientas

### MCP Archon - Documentación

```yaml
Cuándo usar:
  - Necesitas documentación oficial
  - El PRP menciona "Consultar Archon"
  - Tienes dudas sobre cómo usar una librería

Comandos principales:

1. rag_get_available_sources()
   retorna: Lista con source_id, title, url
   usar_para: Ver qué documentación está disponible

2. rag_search_knowledge_base(query, source_id, match_count)
   parámetros:
     - query: "2-5 keywords" (corto y focalizado)
     - source_id: "src_xxx" (opcional pero recomendado)
     - match_count: 5-10 para docs
   usar_para: Buscar información específica

3. rag_search_code_examples(query, source_id, match_count)
   parámetros:
     - query: "tipo de código necesitado"
     - source_id: "src_xxx"
     - match_count: 3-5 para ejemplos
   usar_para: Ver implementaciones de ejemplo

Tips:
  - ✅ Query corto: "FastAPI JWT auth"
  - ❌ Query largo: "cómo implementar autenticación JWT..."
  - Siempre usar source_id cuando sea posible
  - Leer resultados antes de implementar
```

### MCP Serena - Análisis Simbólico

```yaml
Filosofía:
  "❌ NO leer archivos completos innecesariamente"
  "✅ Usar análisis simbólico para lectura inteligente"

Comandos principales:

1. get_symbols_overview(relative_path)
   parámetros: path del archivo o directorio
   retorna: Lista de símbolos (funciones, clases) sin bodies
   usar_para: Ver estructura ANTES de leer
   
   ejemplo:
     get_symbols_overview('src/api/auth.py')

2. find_symbol(name_path, relative_path, include_body)
   parámetros:
     - name_path: "ClassName/method" o "function_name"
     - relative_path: "path/to/file.py"
     - include_body: True si quieres ver implementación
   retorna: Definición del símbolo específico
   usar_para: Leer solo lo necesario
   
   ejemplo:
     find_symbol('AuthService/login', 'src/api/auth.py', True)

3. search_for_pattern(pattern, relative_path)
   parámetros:
     - pattern: regex pattern
     - relative_path: opcional, limitar búsqueda
   retorna: Ubicaciones que coinciden
   usar_para: Buscar cuando no sabes dónde está
   
   ejemplo:
     search_for_pattern('async def.*authenticate', 'src/')

4. find_referencing_symbols(name_path, relative_path)
   parámetros:
     - name_path: símbolo a buscar
     - relative_path: archivo del símbolo
   retorna: Dónde se usa ese símbolo
   usar_para: Entender impacto de cambios
   
   ejemplo:
     find_referencing_symbols('UserModel', 'src/models/user.py')

Flujo recomendado:
  1. get_symbols_overview() → ver qué hay
  2. find_symbol() → leer solo lo necesario
  3. Implementar/modificar
  4. find_referencing_symbols() → verificar impacto
```

### Skills - Guías Expertas

```yaml
Ubicación: .cursor/skills/[nombre-skill]/SKILL.md

Activación Automática:
  método: Mencionar keywords relevantes
  ejemplo: "Voy a crear una nueva feature" → activa brainstorming
  ventaja: Más natural, menos explícito

Invocación Manual:
  formato: "@.cursor/skills/[nombre-skill]/SKILL.md [instrucción]"
  ejemplo: "@.cursor/skills/brainstorming/SKILL.md explorar requisitos"
  ventaja: Control explícito sobre cuándo usar

Skills comunes por fase:

PLANIFICACIÓN:
  - brainstorming (keywords: "nueva feature", "crear")
  - architecture (keywords: "decidir", "arquitectura")
  - planning-with-files (keywords: "tarea compleja")

DESARROLLO:
  - clean-code (se activa al escribir código)
  - python-patterns (proyecto Python)
  - react-patterns (proyecto React)

TESTING:
  - test-driven-development (keywords: "escribir tests primero")
  - test-fixing (keywords: "tests fallando")

VALIDACIÓN:
  - lint-and-validate (después de modificaciones)
  - verification-before-completion (antes de completar)
  - systematic-debugging (keywords: "bug", "error")
```

---

## ⚠️ Puntos Críticos

### ❌ NO HACER:

```yaml
- NO saltar Tarea 0 (Serena es obligatorio)
- NO buscar en web sin consultar Archon primero
- NO leer archivos completos sin usar Serena
- NO ignorar comandos específicos del PRP
- NO saltar validaciones
- NO marcar TODO como completado sin validar
- NO ignorar skills mencionadas en el PRP
- NO declarar completitud sin releer PRP completo
```

### ✅ SIEMPRE HACER:

```yaml
- ✅ Ejecutar Tarea 0 primero (Serena)
- ✅ Consultar Archon cuando el PRP lo mencione
- ✅ Usar Serena para análisis simbólico
- ✅ Invocar skills según indicaciones del PRP
- ✅ Seguir los 3 niveles de validación
- ✅ Actualizar TODOs al completar tareas
- ✅ Ejecutar todos los comandos de validación
- ✅ Releer PRP completo antes de reportar completitud
```

---

## 📊 Checklist de Ejecución

```yaml
PREPARACIÓN:
  - [ ] PRP leído completamente
  - [ ] MCPs verificados (Archon, Serena)
  - [ ] Skills identificadas
  - [ ] TODOs creados

TAREA 0:
  - [ ] Serena instalado y funcionando
  - [ ] get_symbols_overview probado
  - [ ] TODO task-0 marcado como completado

TAREAS 1-N (para cada una):
  - [ ] Tarea leída completamente
  - [ ] Skills invocadas según PRP
  - [ ] Comandos Archon ejecutados (si aplica)
  - [ ] Comandos Serena ejecutados (si aplica)
  - [ ] Archivos creados según lista
  - [ ] Archivos modificados según lista
  - [ ] Nivel 1: Sintaxis OK
  - [ ] Nivel 2: Tests OK
  - [ ] Nivel 3: Integración OK (si aplica)
  - [ ] TODO actualizado

VALIDACIÓN FINAL:
  - [ ] Checklist del PRP completado
  - [ ] 3 niveles validación global ejecutados
  - [ ] Criterios de éxito verificados
  - [ ] Anti-patrones revisados
  - [ ] Todos los TODOs completed

COMPLETITUD:
  - [ ] PRP releído completamente
  - [ ] TODOs todos completed
  - [ ] Métricas reportadas
  - [ ] Desviaciones documentadas
  - [ ] Ready para revisión
```

---

## 🎯 Meta del Proceso

**Implementación exitosa siguiendo el PRP al 100% mediante:**

1. ✅ Uso correcto de Archon para documentación oficial
2. ✅ Uso correcto de Serena para análisis simbólico
3. ✅ Invocación apropiada de Skills en cada fase
4. ✅ Seguimiento estricto de estructura de tareas
5. ✅ Validación en 3 niveles por tarea
6. ✅ Verificación final exhaustiva
7. ✅ Zero desviaciones no documentadas

**Resultado esperado**: Feature implementada, validada y lista para producción en un solo ciclo de ejecución.
