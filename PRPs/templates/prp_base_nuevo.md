name: "Template Base PRP v3 - Contexto Rico con Skills y MCPs Integrados"
version: "3.0-ES"
descripcion: |
  Template optimizado para agentes de IA que implementan características con 
  contexto suficiente, capacidad de auto-validación, integración estratégica 
  de Skills y uso coordinado de MCPs (Archon, Serena, etc.)

## Principios Fundamentales
1. **Contexto es Rey**: Incluir TODA la documentación, ejemplos y advertencias necesarias
2. **Bucles de Validación**: Proporcionar tests/lints ejecutables que la IA puede correr y arreglar
3. **Denso en Información**: Usar keywords y patrones del codebase
4. **Éxito Progresivo**: Empezar simple, validar, luego mejorar
5. **Skills en Equipo**: Llamar skills relevantes en cada fase del desarrollo
6. **MCPs Estratégicos**: Archon para documentación, Serena para arquitectura
7. **Reglas Globales**: Seguir todas las reglas en CLAUDE.md

---

## 🎯 Objetivo

[Qué necesita ser construido - ser específico sobre el estado final y los deseos]

## 💡 Por Qué

- [Valor de negocio e impacto en el usuario]
- [Integración con características existentes]
- [Problemas que esto resuelve y para quién]

## 📋 Qué

[Comportamiento visible para el usuario y requisitos técnicos]

### Criterios de Éxito
- [ ] [Resultados específicos medibles]
- [ ] [Validación ejecutada]
- [ ] [Métricas de aceptación]

---

## 🧰 Skills del Proyecto a Utilizar

### 📝 FASE DE PLANIFICACIÓN

**Skill: planning-with-files**
- **Cuándo**: Tareas complejas multi-paso o proyectos de investigación (>5 tool calls)
- **Por qué**: Crea task_plan.md, findings.md y progress.md para seguimiento estructurado

**Skill: brainstorming**
- **Cuándo**: ANTES de cualquier trabajo creativo, nuevas features, o modificar comportamiento
- **Por qué**: Explora intención del usuario, requisitos y diseño antes de implementar
- **Crítico**: Uso OBLIGATORIO antes de implementación

**Skill: architecture**
- **Cuándo**: Decisiones arquitectónicas o análisis de diseño de sistema
- **Por qué**: Framework para análisis de requisitos, evaluación trade-offs, documentación ADR

**Skill: writing-plans**
- **Cuándo**: Tienes spec o requisitos para tarea multi-paso, antes de tocar código
- **Por qué**: Planificación estructurada con breakdowns claros, dependencias y criterios

### 💻 FASE DE DESARROLLO

**MCP: Serena** ⚡ CRÍTICO - INSTALAR PRIMERO
- **Cuándo**: SIEMPRE - Primera tarea en todo proyecto nuevo
- **Por qué**: Gestión de arquitectura, búsqueda simbólica, análisis sin leer archivos completos
- **Herramientas principales**: 
  - `get_symbols_overview`: Ver estructura sin leer todo
  - `find_symbol`: Buscar símbolos específicos
  - `search_for_pattern`: Búsqueda rápida de patrones
  - `replace_symbol_body`: Edición quirúrgica de código

**Skill: clean-code**
- **Cuándo**: Escribiendo o revisando código
- **Por qué**: Estándares pragmáticos: conciso, directo, sin sobre-ingeniería

**Skill: python-patterns** (si proyecto Python)
- **Cuándo**: Desarrollando en Python
- **Por qué**: Principios de decisión: framework, async, type hints, estructura

**Skill: react-patterns** (si proyecto React)
- **Cuándo**: Desarrollando componentes React
- **Por qué**: Patrones modernos: hooks, composición, performance, TypeScript

**Skill: nextjs-best-practices** (si proyecto Next.js)
- **Cuándo**: Trabajando con Next.js
- **Por qué**: Server Components, data fetching, routing patterns

### 📚 FASE DE DOCUMENTACIÓN

**MCP: Archon** 🎯 PRIORIDAD MÁXIMA
- **Cuándo**: SIEMPRE - Consultar ANTES que URLs externas
- **Por qué**: Base de datos RAG con TODA la documentación oficial
- **Documentación disponible**: Python, Pydantic, FastAPI, Supabase, Next.js, React, TypeScript
- **Herramientas**:
  - `rag_get_available_sources()`: Listar fuentes con IDs
  - `rag_search_knowledge_base(query, source_id, match_count)`: Buscar docs
  - `rag_search_code_examples(query, source_id, match_count)`: Buscar ejemplos

**Skill: documentation-templates**
- **Cuándo**: Crear README, API docs, comentarios
- **Por qué**: Templates para documentación amigable con IA

### 🧪 FASE DE TESTING

**Skill: test-driven-development**
- **Cuándo**: ANTES de escribir código de implementación
- **Por qué**: Tests primero aseguran calidad desde el inicio

**Skill: test-fixing**
- **Cuándo**: Tests fallando
- **Por qué**: Agrupación inteligente de errores y corrección sistemática

### ✅ FASE DE VALIDACIÓN

**Skill: lint-and-validate**
- **Cuándo**: Después de CADA modificación de código
- **Por qué**: QA automático, linting, análisis estático

**Skill: verification-before-completion**
- **Cuándo**: Antes de declarar completitud o crear PRs
- **Por qué**: Requiere evidencia de comandos ejecutados

**Skill: systematic-debugging**
- **Cuándo**: Bugs, test failures, comportamiento inesperado
- **Por qué**: Análisis sistemático ANTES de proponer fixes

---

## 🔌 Guía de MCPs

### MCP Archon 🎯 (USAR SIEMPRE PRIMERO)

**Flujo de trabajo:**

```yaml
Paso 1 - Obtener fuentes disponibles:
  comando: rag_get_available_sources()
  resultado: Lista con source_id de cada documentación

Paso 2 - Buscar en documentación específica:
  comando: |
    rag_search_knowledge_base(
        query="keywords cortos",
        source_id="src_xxx",
        match_count=5
    )
  tips:
    - "Query CORTO: 2-5 palabras clave"
    - "✅ BUENO: 'FastAPI JWT auth'"
    - "❌ MALO: 'cómo implementar autenticación JWT en FastAPI con...'"

Paso 3 - Buscar ejemplos de código:
  comando: |
    rag_search_code_examples(
        query="pydantic validator",
        source_id="src_xxx",
        match_count=3
    )
```

### MCP Serena ⚡ (INSTALAR PRIMERO)

**Filosofía:**
- ❌ NO leer archivos completos innecesariamente
- ✅ Usar `get_symbols_overview` para ver estructura primero
- ✅ Usar `find_symbol` para leer solo lo necesario
- ✅ Ediciones simbólicas para cambios quirúrgicos

**Herramientas principales:**

```yaml
get_symbols_overview(relative_path):
  propósito: "Ver estructura sin leer contenido completo"
  cuándo: "ANTES de leer archivos"
  
find_symbol(name_path, relative_path, include_body):
  propósito: "Buscar símbolo específico"
  ejemplo: "find_symbol('UserModel/validate', 'src/models.py', True)"

search_for_pattern(pattern, relative_path):
  propósito: "Búsqueda rápida cuando no sabes ubicación exacta"
  
replace_symbol_body(name_path, relative_path, new_body):
  propósito: "Reemplazar implementación completa de función/clase"
```

---

## 📦 Todo el Contexto Necesario

### Documentación & Referencias

```yaml
PASO 1 - Consultar Archon (PRIORITARIO):
  acción: |
    # Obtener fuentes
    rag_get_available_sources()
    
    # Buscar en fuente específica
    rag_search_knowledge_base(
        query="keywords cortos",
        source_id="src_xxx",
        match_count=5
    )
  por_qué: "Documentación oficial verificada"

PASO 2 - Archivos del proyecto con Serena:
  acción: |
    # Ver estructura primero
    get_symbols_overview('path/to/file.py')
    
    # Leer símbolo específico
    find_symbol('ClassName/method', 'path/to/file.py', True)
  por_qué: "Lectura inteligente, no archivos completos"

PASO 3 - URLs externos (SOLO SI ARCHON NO TIENE):
  - url: [URL oficial]
    por_qué: [Sección específica necesaria]
    nota: "Último recurso"
```

### Árbol del Codebase Actual
```bash
# Ejecutar `tree` en raíz o usar Serena get_symbols_overview
```

### Árbol del Codebase Deseado
```bash
# Estructura con archivos nuevos y sus responsabilidades
```

### Gotchas Conocidos
```python
# CRÍTICO: [Librería] requiere [setup específico]
# Ejemplo: FastAPI requiere funciones async
# Ejemplo: Pydantic v2, NO v1
# Ejemplo: Este ORM no soporta batch inserts >1000
```

---

## 🏗️ Blueprint de Implementación

### Modelos de Datos y Estructura

```python
# Ejemplos de modelos:
# - ORM models
# - Pydantic models  
# - Pydantic schemas
# - Pydantic validators
```

---

## 📝 Lista de Tareas

### 🎯 ESTRUCTURA DE CADA TAREA:

```yaml
Tarea N: [NOMBRE_DESCRIPTIVO]

Herramientas a utilizar:
  - ⚡ MCP Archon: [Query específica a buscar]
    Importancia: "Necesitamos documentación oficial sobre [tema] porque [razón]"
    Comando: |
      rag_search_knowledge_base(
          query="keywords",
          source_id="src_xxx",
          match_count=5
      )
  
  - 🔧 MCP Serena: [Herramienta específica]
    Importancia: "Usaremos [herramienta] para [propósito específico]"
    Comando: "get_symbols_overview('path/file.py')"
  
  - 📚 Skill [nombre]: [Justificación]
    Importancia: "Aporta [capacidad] al proceso"

Objetivo:
  [Descripción clara del resultado esperado]

Pasos a seguir:
  1. Consultar Archon sobre [tema]
     Comando: rag_search_knowledge_base(query="...", source_id="...", match_count=5)
  
  2. Usar Serena para analizar estructura
     Comando: get_symbols_overview('path/to/file.py')
  
  3. [Siguiente paso con herramienta específica]
  
  4. Validar con skill correspondiente

Criterios de aceptación:
  - [ ] [Criterio medible 1]
  - [ ] [Criterio medible 2]
  - [ ] [Tests pasan]
  - [ ] [Linting OK]

Archivos a crear:
  - path/to/new/file.py - [Propósito del archivo]

Archivos a modificar:
  - path/to/existing/file.py - [Qué cambiar y por qué]

Pseudocódigo (si aplica):
  ```python
  # PATRÓN: Validar input primero (ver src/validators.py)
  async def nueva_funcion(param: str) -> Result:
      # GOTCHA: Librería requiere connection pooling
      # CRÍTICO: API retorna 429 si >10 req/sec
      ...
  ```

Comandos de validación:
  ```bash
  # Ejecutar DESPUÉS de implementar
  pytest tests/test_tarea_n.py -v
  ruff check src/ --fix
  mypy src/
  ```
```

---

### TAREA 0: Instalar y configurar MCP Serena (⚡ OBLIGATORIO)

**Herramientas a utilizar:**
- ⚡ MCP Archon: Consultar sobre instalación de MCPs
  - Importancia: "Documentación oficial de configuración de MCPs en Cursor"
  - Comando: `rag_search_knowledge_base(query="MCP installation Cursor", match_count=5)`

- 🔧 MCP Serena: Onboarding del proyecto
  - Importancia: "Configurar para gestión de arquitectura"

- 📚 Skill environment-setup-guide: Configuración de entorno
  - Importancia: "Guía paso a paso para setup correcto"

**Objetivo:**
Instalar y configurar Serena para análisis simbólico de código y gestión de arquitectura

**Pasos a seguir:**
1. Verificar que Serena está en configuración de Cursor
2. Activar Serena en el proyecto actual
3. Realizar onboarding si es necesario
4. Verificar funcionamiento con `get_symbols_overview`

**Criterios de aceptación:**
- [ ] Serena activo en el proyecto
- [ ] Puede ejecutar comandos básicos
- [ ] Onboarding completado

---

### TAREA 1: [Tu primera tarea real]

**Herramientas a utilizar:**
- ⚡ MCP Archon: [Query específica]
  - Importancia: "[Razón]"
  - Comando: `rag_search_knowledge_base(query="...", source_id="...", match_count=5)`

- 🔧 MCP Serena: [Herramienta]
  - Importancia: "[Razón]"
  - Comando: `[comando específico]`

- 📚 Skills: [Lista con justificación]

**Objetivo:**
[Descripción clara]

**Pasos a seguir:**
1. [Paso con comando específico]
2. [Paso con comando específico]
3. [Paso con comando específico]

**Criterios de aceptación:**
- [ ] [Criterio 1]
- [ ] [Criterio 2]

**Archivos a crear:**
- path/file.py - [Propósito]

**Archivos a modificar:**
- path/existing.py - [Cambios]

**Comandos de validación:**
```bash
pytest tests/test_tarea1.py -v
ruff check src/ --fix
mypy src/
```

---

## 🔄 Bucle de Validación

### Nivel 1: Sintaxis & Estilo
```bash
# Ejecutar PRIMERO - arreglar errores antes de proceder
ruff check src/ --fix
mypy src/

# Esperado: Sin errores. Si hay errores, LEER y ARREGLAR
```

### Nivel 2: Tests Unitarios
```python
# CREAR test_nueva_feature.py con estos casos:

def test_happy_path():
    """Funcionalidad básica funciona"""
    result = nueva_funcion("input_valido")
    assert result.status == "success"

def test_validation_error():
    """Input inválido lanza ValidationError"""
    with pytest.raises(ValidationError):
        nueva_funcion("")

def test_error_handling():
    """Maneja errores gracefully"""
    with mock.patch('api.call', side_effect=TimeoutError):
        result = nueva_funcion("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# Ejecutar e iterar hasta que pasen:
pytest test_nueva_feature.py -v
# Si fallan: Leer error, entender causa raíz, arreglar código, re-ejecutar
```

### Nivel 3: Test de Integración
```bash
# Iniciar servicio
python -m src.main --dev

# Probar endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Esperado: {"status": "success", "data": {...}}
# Si error: Revisar logs en logs/app.log
```

---

## ✅ Checklist de Validación Final

- [ ] Todos los tests pasan: `pytest tests/ -v`
- [ ] Sin errores de linting: `ruff check src/`
- [ ] Sin errores de tipos: `mypy src/`
- [ ] Test manual exitoso: [comando específico]
- [ ] Casos de error manejados gracefully
- [ ] Logs informativos pero no verbosos
- [ ] Documentación actualizada si fue necesario

---

## ❌ Anti-Patrones a Evitar

- ❌ No crear nuevos patrones cuando los existentes funcionan
- ❌ No saltar validación porque "debería funcionar"
- ❌ No ignorar tests fallidos - arreglarlos
- ❌ No usar funciones sync en contexto async
- ❌ No hardcodear valores que deberían ser config
- ❌ No usar catch-all exceptions - ser específico
- ❌ No leer archivos completos sin usar Serena primero
- ❌ No buscar en web sin consultar Archon primero

---

## 📚 Integración con INITIAL.md

Cuando uses este template a través de `generate-prp.md`:

1. **Llena INITIAL.md** con todos los detalles de tu proyecto
2. **El sistema generará** un PRP específico usando este template
3. **Archon buscará** automáticamente documentación relevante
4. **Serena se instalará** como primera tarea
5. **Skills se activarán** en las fases correspondientes

**Recuerda:**
- Ser específico en INITIAL.md
- Listar todas las tecnologías que usarás
- Mencionar cualquier gotcha conocido
- Definir ejemplos que quieres incluir
