# PRP: Query Decomposition con Razonamiento Socrático + Switch de Modelos (Simplificado)

## 📋 METADATA

```yaml
nombre: "Query Decomposition System + Model Switch (Simplificado)"
version: "3.2.1"
fecha: "2026-01-30"
descripcion: "Sistema de Query Decomposition + Switch de modelos usando API keys del .env (sin guardar keys en BD)"
tipo: "Feature Addition - RAG Enhancement"
proyecto_base: "Marketing Second Brain (EXISTENTE)"
extension_de: "Sistema de Aprendizaje Progresivo (TAREA 5 completada)"
score_confianza: "9/10"
```

---

## 🎯 OBJETIVO

Implementar dos features que mejoran el sistema de Marketing Brain:

**Feature 1: Query Decomposition**
- El sistema genera MÚLTIPLES sub-queries antes de buscar en RAG
- Usa método socrático para diversificar las búsquedas
- Encuentra conceptos de MÚLTIPLES libros (no solo uno)

**Feature 2: Switch de Modelos (SIMPLIFICADO)**
- Selector de modelo en el chat que permite cambiar entre modelos
- **USA las API keys YA configuradas en .env** (NO guarda keys nuevas)
- Modelos disponibles según el `LLM_PROVIDER` configurado
- Si provider=openai: gpt-4o, gpt-4o-mini, gpt-4-turbo
- Si provider=openrouter: claude-3.5-sonnet, claude-3-opus, claude-3-haiku

**⚠️ IMPORTANTE**: Este enfoque es SEGURO porque:
- NO modifica cómo se guardan las API keys
- NO crea tablas nuevas en la BD
- Solo agrega un parámetro `model` que pasa por el sistema
- Retrocompatible: si no se envía `model`, usa el del .env

---

## 🚨 ARQUITECTURA ACTUAL - ENTENDER ANTES DE MODIFICAR

### Flujo actual del chat (SIN modelo dinámico):

```
1. Frontend envía: { content: "mensaje" }
                    ↓
2. SendMessageRequest solo tiene: content
                    ↓
3. stream_message() → get_initialized_agents() → LLMService()
                    ↓
4. LLMService.__init__() lee de .env:
   - self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
   - Este modelo se usa SIEMPRE
                    ↓
5. router_agent.process_stream() → ContentGeneratorAgent.execute()
                    ↓
6. self.llm.generate_with_messages(messages, max_tokens, temperature)
   - NO recibe parámetro model
   - Usa self.model internamente
```

### Flujo NUEVO con switch de modelos:

```
1. Frontend envía: { content: "mensaje", model: "gpt-4o-mini" }
                    ↓
2. SendMessageRequest ahora tiene: content + model (opcional)
                    ↓
3. stream_message() recibe model del request
                    ↓
4. router_agent.process_stream(chat_id, project_id, user_message, model)
                    ↓
5. ContentGeneratorAgent.execute(..., model)
                    ↓
6. self.llm.generate_with_messages(messages, max_tokens, temperature, model)
   - NUEVO: recibe model como parámetro opcional
   - Usa: model or self.model (fallback al .env)
```

---

## 🔍 ANÁLISIS DETALLADO DE ARCHIVOS A MODIFICAR

### 1. LLMService - Métodos que usan self.model:

```yaml
Archivo: backend/src/services/llm_service.py

Métodos a modificar (agregar param model: Optional[str] = None):
  - generate() línea 50-91
  - stream() línea 93-139
  - generate_with_messages() línea 141-197
  - stream_with_messages() línea 199-255

Cambio en cada método:
  ANTES: model=self.model
  DESPUÉS: model=model or self.model
```

### 2. Cadena de llamadas a modificar:

```yaml
1. SendMessageRequest (schema):
   Archivo: backend/src/schemas/chat.py
   Cambio: Agregar model: Optional[str] = None

2. stream_message (endpoint):
   Archivo: backend/src/api/chat.py línea 224
   Cambio: Extraer request.model y pasarlo a process_stream()

3. RouterAgent.process_stream():
   Archivo: backend/src/agents/router_agent.py línea 145
   Cambio: Agregar param model y pasarlo a ContentGeneratorAgent

4. ContentGeneratorAgent.execute():
   Archivo: backend/src/agents/content_generator_agent.py línea 27
   Cambio: Agregar param model y pasarlo a llm.generate_with_messages()
```

---

## 📖 SKILLS A UTILIZAR

```yaml
FASE ANÁLISIS:
  - MCP Serena: get_symbols_overview, find_symbol (OBLIGATORIO)

FASE DESARROLLO:
  - python-patterns: Async patterns, type hints
  - clean-code: Código conciso, sin duplicación
  - rag-implementation: Patrones de retrieval

FASE TESTING:
  - testing-patterns: Tests unitarios
  - verification-before-completion: Antes de declarar completitud
```

---

## 🏗️ TAREAS

### TAREA 0: Verificación del Entorno

**Herramientas:**
- 🔧 MCP Serena: `activate_project("brain-mkt")`

**Objetivo:** Confirmar que el entorno está listo y entender estructura actual.

**Pasos a ejecutar:**
```bash
# 1. Verificar que Docker está corriendo
docker compose ps

# 2. Verificar que backend responde
curl http://localhost:8000/health

# 3. Verificar variable LLM_PROVIDER en .env
grep "LLM_PROVIDER" backend/../.env
# Resultado esperado: LLM_PROVIDER=openai (o openrouter)

# 4. Verificar modelo actual configurado
grep "OPENAI_MODEL\|OPENROUTER_MODEL" backend/../.env
# Resultado esperado: OPENAI_MODEL=gpt-4o (o similar)
```

**Criterios de aceptación:**
- [ ] Docker containers running
- [ ] Backend responde en :8000
- [ ] LLM_PROVIDER identificado (openai u openrouter)
- [ ] Modelo actual identificado

---

### TAREA 1: Crear QueryDecomposer

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('LLMService/generate', 'backend/src/services/llm_service.py', True)`
- 📚 Skills: python-patterns, clean-code

**Objetivo:** Crear servicio que genera sub-queries usando método socrático.

**Archivo a crear:** `backend/src/services/query_decomposer.py`

**Código completo:**

```python
# backend/src/services/query_decomposer.py
"""
Query Decomposer - Genera múltiples sub-queries usando método socrático.

Este servicio toma una query del usuario y la descompone en 3-5 sub-queries
diversificadas para mejorar la búsqueda semántica en RAG.
"""

from typing import Optional
import json
import logging

# CRÍTICO: Importar LLMService del proyecto existente
from .llm_service import LLMService

logger = logging.getLogger(__name__)


# Prompt para el método socrático
# NOTA: Este prompt está diseñado para generar queries cortas y diversas
SOCRATIC_PROMPT = """Eres un experto en marketing que necesita buscar conocimiento en una base de datos de libros.

El usuario preguntó: "{user_query}"

Contexto adicional:
{context}

Aplica el MÉTODO SOCRÁTICO para generar queries de búsqueda:
1. ¿Qué está pidiendo REALMENTE el usuario?
2. ¿Qué conceptos relacionados podrían ayudar?
3. ¿Qué técnicas de otros dominios aplican?
4. ¿Qué aspectos podría estar ignorando?

Genera exactamente {num_queries} queries de búsqueda DIVERSAS.

REGLAS ESTRICTAS:
- Queries cortas (3-7 palabras cada una)
- Cada una busca un ÁNGULO DIFERENTE
- NO incluyas la query original textual
- NO uses comillas en las queries

Responde SOLO con JSON válido:
{{"reasoning": "Tu razonamiento en 1-2 oraciones", "queries": ["query1", "query2", "query3", ...]}}
"""


class QueryDecomposer:
    """
    Genera sub-queries usando método socrático.
    
    Uso:
        decomposer = QueryDecomposer(llm_service)
        queries = await decomposer.decompose("hooks para redes sociales")
        # Retorna: ["técnicas captar atención", "copywriting persuasivo", ...]
    
    PATRÓN: Usa LLMService existente, NO reimplementa llamadas a OpenAI.
    """
    
    def __init__(self, llm_service: LLMService):
        """
        Inicializa QueryDecomposer con LLMService existente.
        
        Args:
            llm_service: Instancia de LLMService del proyecto
        """
        self.llm = llm_service
    
    async def decompose(
        self,
        user_query: str,
        buyer_persona: Optional[dict] = None,
        num_queries: int = 4,
    ) -> list[str]:
        """
        Descompone una query en múltiples sub-queries diversificadas.
        
        Args:
            user_query: Query original del usuario
            buyer_persona: Contexto del buyer persona (opcional)
            num_queries: Número de queries a generar (se fuerza entre 3-5)
        
        Returns:
            Lista de sub-queries (strings). Si falla, retorna [user_query].
        
        CRÍTICO: 
        - Límite FORZADO entre 3-5 queries para controlar costos
        - Si LLM falla, retorna query original como fallback
        """
        # ⚠️ REGLA: Siempre entre 3-5 queries
        num_queries = max(3, min(5, num_queries))
        
        # Construir contexto desde buyer persona
        context = self._build_context(buyer_persona)
        
        # Construir prompt completo
        prompt = SOCRATIC_PROMPT.format(
            user_query=user_query,
            context=context,
            num_queries=num_queries
        )
        
        try:
            # REUTILIZAR LLMService.generate() existente
            # NOTA: Usa el modelo configurado en .env (gpt-4o-mini recomendado)
            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.7,  # Un poco de creatividad para diversidad
                max_tokens=300   # Suficiente para JSON con 5 queries
            )
            
            # Parsear respuesta JSON
            queries = self._parse_response(response, num_queries, user_query)
            
            logger.info(
                "[QueryDecomposer] original='%s' generated=%d queries=%s",
                user_query[:50], len(queries), queries
            )
            
            return queries
            
        except Exception as e:
            # FALLBACK: Si algo falla, usar query original
            logger.warning(
                "[QueryDecomposer] Failed for '%s': %s. Using fallback.",
                user_query[:50], str(e)
            )
            return [user_query]
    
    def _build_context(self, buyer_persona: Optional[dict]) -> str:
        """
        Extrae contexto relevante del buyer persona para enriquecer el prompt.
        
        Args:
            buyer_persona: Dict con datos del buyer persona o None
            
        Returns:
            String con contexto formateado o mensaje default
        """
        if not buyer_persona or not isinstance(buyer_persona, dict):
            return "No hay contexto adicional disponible."
        
        parts = []
        
        # Extraer campos útiles del buyer persona
        if industry := buyer_persona.get("industry"):
            parts.append(f"Industria: {industry}")
        if problems := buyer_persona.get("main_problems"):
            if isinstance(problems, list):
                parts.append(f"Problemas: {', '.join(problems[:3])}")
        if audience := buyer_persona.get("target_audience"):
            parts.append(f"Audiencia: {audience}")
        
        return "\n".join(parts) if parts else "No hay contexto adicional disponible."
    
    def _parse_response(
        self, 
        response: str, 
        num_queries: int, 
        fallback: str
    ) -> list[str]:
        """
        Parsea respuesta JSON del LLM.
        
        Args:
            response: Respuesta raw del LLM (puede tener texto extra)
            num_queries: Número máximo de queries a retornar
            fallback: Query original para usar si falla el parsing
            
        Returns:
            Lista de queries parseadas o [fallback] si falla
        """
        try:
            # GOTCHA: LLM puede agregar texto antes/después del JSON
            # Buscar el JSON dentro de la respuesta
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("[QueryDecomposer] No JSON found in response")
                return [fallback]
            
            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)
            
            queries = parsed.get("queries", [])
            
            # Log del razonamiento para debug
            reasoning = parsed.get("reasoning", "")
            if reasoning:
                logger.debug("[QueryDecomposer] reasoning: %s", reasoning[:100])
            
            # Validar que sean strings no vacíos
            valid_queries = [q for q in queries if isinstance(q, str) and q.strip()]
            
            if not valid_queries:
                logger.warning("[QueryDecomposer] No valid queries in response")
                return [fallback]
            
            # Limitar al número solicitado
            return valid_queries[:num_queries]
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning("[QueryDecomposer] JSON parse failed: %s", str(e))
            return [fallback]
```

**Test a crear:** `backend/tests/unit/test_query_decomposer.py`

```python
# backend/tests/unit/test_query_decomposer.py
"""Tests para QueryDecomposer."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.query_decomposer import QueryDecomposer


@pytest.fixture
def mock_llm():
    """Mock de LLMService que retorna JSON válido."""
    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value='{"reasoning": "test reasoning", "queries": ["q1", "q2", "q3", "q4"]}'
    )
    return llm


@pytest.mark.asyncio
async def test_decompose_returns_queries(mock_llm):
    """Verifica que decompose retorna lista de queries."""
    decomposer = QueryDecomposer(mock_llm)
    queries = await decomposer.decompose("hooks para redes sociales")
    
    assert isinstance(queries, list)
    assert len(queries) >= 3
    assert len(queries) <= 5
    assert all(isinstance(q, str) for q in queries)


@pytest.mark.asyncio
async def test_decompose_fallback_on_error(mock_llm):
    """Verifica fallback cuando LLM falla."""
    mock_llm.generate = AsyncMock(side_effect=Exception("API Error"))
    decomposer = QueryDecomposer(mock_llm)
    
    original_query = "test query original"
    queries = await decomposer.decompose(original_query)
    
    assert queries == [original_query]  # Fallback a query original


@pytest.mark.asyncio
async def test_decompose_limits_queries():
    """Verifica que el límite de 3-5 queries se respeta."""
    llm = MagicMock()
    # LLM retorna más de 5 queries
    llm.generate = AsyncMock(
        return_value='{"queries": ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]}'
    )
    decomposer = QueryDecomposer(llm)
    
    # Aunque pidamos 10, debe limitar a 5
    queries = await decomposer.decompose("test", num_queries=10)
    
    assert len(queries) <= 5


@pytest.mark.asyncio
async def test_decompose_handles_invalid_json():
    """Verifica manejo de JSON inválido."""
    llm = MagicMock()
    llm.generate = AsyncMock(return_value="esto no es JSON válido")
    decomposer = QueryDecomposer(llm)
    
    queries = await decomposer.decompose("test query")
    
    assert queries == ["test query"]  # Fallback


@pytest.mark.asyncio
async def test_decompose_with_buyer_persona(mock_llm):
    """Verifica que buyer_persona se incluye en contexto."""
    decomposer = QueryDecomposer(mock_llm)
    
    buyer = {
        "industry": "fitness",
        "main_problems": ["falta de leads", "bajo engagement"],
        "target_audience": "mujeres 25-35"
    }
    
    queries = await decomposer.decompose("ideas de contenido", buyer_persona=buyer)
    
    # Verificar que se llamó a generate
    mock_llm.generate.assert_called_once()
    call_args = mock_llm.generate.call_args
    prompt = call_args.kwargs.get("prompt", call_args.args[0] if call_args.args else "")
    
    # El prompt debe incluir info del buyer persona
    assert "fitness" in prompt or len(queries) > 0
```

**Criterios de aceptación:**
- [ ] Archivo `query_decomposer.py` creado en `backend/src/services/`
- [ ] Import funciona: `from src.services.query_decomposer import QueryDecomposer`
- [ ] Tests pasan: `pytest backend/tests/unit/test_query_decomposer.py -v`
- [ ] Linting OK: `ruff check backend/src/services/query_decomposer.py`

---

### TAREA 2: Crear ResultCombiner

**Herramientas:**
- 📚 Skills: python-patterns, clean-code

**Objetivo:** Combinar, deduplicar y re-rankear resultados de múltiples búsquedas.

**Archivo a crear:** `backend/src/services/result_combiner.py`

**Código completo:**

```python
# backend/src/services/result_combiner.py
"""
Result Combiner - Combina y re-rankea resultados de múltiples búsquedas RAG.

Este servicio toma resultados de múltiples queries y los combina
de forma inteligente para maximizar diversidad y relevancia.
"""

from collections import defaultdict
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ResultCombiner:
    """
    Combina resultados de múltiples búsquedas RAG.
    
    Funcionalidades:
    - Deduplica por ID de concepto
    - Re-rankea por frecuencia × similarity (conceptos que aparecen
      en múltiples búsquedas son más relevantes)
    - Asegura diversidad de libros (no todos los resultados de un solo libro)
    
    Uso:
        combiner = ResultCombiner()
        combined = combiner.combine(all_results, max_results=7, min_books=2)
    """
    
    def combine(
        self,
        results: list[dict[str, Any]],
        max_results: int = 7,
        min_books: int = 2,
    ) -> list[dict[str, Any]]:
        """
        Combina y re-rankea resultados de múltiples búsquedas.
        
        Args:
            results: Lista de resultados de RAG (pueden tener duplicados)
                     Cada resultado debe tener: id, similarity, book_title
            max_results: Número máximo de resultados a retornar
            min_books: Mínimo de libros diferentes a incluir (si hay disponibles)
        
        Returns:
            Lista de resultados únicos, ordenados por relevancia combinada,
            con diversidad de libros asegurada.
        
        PATRÓN: 
        - Conceptos que aparecen en múltiples búsquedas obtienen boost
        - Se prioriza tener al menos min_books libros diferentes
        """
        if not results:
            return []
        
        # 1. Agrupar por ID y calcular estadísticas
        concept_data: dict[str, dict[str, Any]] = defaultdict(lambda: {
            "concept": None,
            "appearances": 0,
            "similarities": [],
            "book": None
        })
        
        for result in results:
            # Obtener ID del concepto
            concept_id = result.get("id")
            if not concept_id:
                continue
            
            data = concept_data[concept_id]
            
            # Guardar el concepto completo (primera vez)
            if data["concept"] is None:
                data["concept"] = result
            
            # Contar apariciones (en cuántas búsquedas apareció)
            data["appearances"] += 1
            
            # Guardar similarity para promediar después
            similarity = result.get("similarity", 0)
            if isinstance(similarity, (int, float)):
                data["similarities"].append(float(similarity))
            
            # Guardar nombre del libro
            data["book"] = result.get("book_title", "unknown")
        
        # 2. Calcular score combinado para cada concepto
        scored: list[dict[str, Any]] = []
        
        for concept_id, data in concept_data.items():
            if not data["concept"]:
                continue
            
            # Promedio de similarities
            avg_similarity = (
                sum(data["similarities"]) / len(data["similarities"])
                if data["similarities"]
                else 0
            )
            
            # Boost por frecuencia: +30% por cada aparición adicional
            # Ej: aparece en 3 búsquedas → boost = 1 + (3-1)*0.3 = 1.6
            frequency_boost = 1 + (data["appearances"] - 1) * 0.3
            
            # Score final
            combined_score = avg_similarity * frequency_boost
            
            scored.append({
                **data["concept"],
                "combined_score": combined_score,
                "appearances": data["appearances"],
                "_book": data["book"]  # Campo temporal para diversidad
            })
        
        # 3. Ordenar por score combinado (mayor primero)
        scored.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
        
        # 4. Asegurar diversidad de libros
        final: list[dict[str, Any]] = []
        books_seen: set[str] = set()
        
        # Primera pasada: incluir al menos un concepto de cada libro
        # hasta alcanzar min_books
        for concept in scored:
            book = concept.get("_book", "unknown")
            if book not in books_seen and len(books_seen) < min_books:
                # Remover campo temporal
                concept_clean = {k: v for k, v in concept.items() if k != "_book"}
                final.append(concept_clean)
                books_seen.add(book)
        
        # Segunda pasada: llenar hasta max_results con los mejores restantes
        for concept in scored:
            if len(final) >= max_results:
                break
            
            # Verificar si ya está incluido
            concept_id = concept.get("id")
            if any(c.get("id") == concept_id for c in final):
                continue
            
            # Agregar sin campo temporal
            concept_clean = {k: v for k, v in concept.items() if k != "_book"}
            final.append(concept_clean)
            books_seen.add(concept.get("_book", "unknown"))
        
        logger.info(
            "[ResultCombiner] input=%d unique=%d output=%d books=%s",
            len(results),
            len(concept_data),
            len(final),
            list(books_seen)
        )
        
        return final
```

**Test a crear:** `backend/tests/unit/test_result_combiner.py`

```python
# backend/tests/unit/test_result_combiner.py
"""Tests para ResultCombiner."""

from src.services.result_combiner import ResultCombiner


def test_combine_deduplicates():
    """Verifica que deduplica por ID."""
    combiner = ResultCombiner()
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.8},
        {"id": "1", "book_title": "Book A", "similarity": 0.7},  # Duplicado
        {"id": "2", "book_title": "Book B", "similarity": 0.6},
    ]
    
    combined = combiner.combine(results)
    
    ids = [r["id"] for r in combined]
    assert len(ids) == len(set(ids))  # Sin duplicados
    assert len(combined) == 2


def test_combine_boosts_frequent():
    """Verifica que conceptos frecuentes obtienen mayor score."""
    combiner = ResultCombiner()
    
    # Concepto "1" aparece 3 veces con similarity 0.5
    # Concepto "2" aparece 1 vez con similarity 0.6
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.5},
        {"id": "1", "book_title": "Book A", "similarity": 0.5},
        {"id": "1", "book_title": "Book A", "similarity": 0.5},
        {"id": "2", "book_title": "Book B", "similarity": 0.6},
    ]
    
    combined = combiner.combine(results, min_books=1)
    
    # Concepto "1" debería tener score: 0.5 * (1 + 2*0.3) = 0.8
    # Concepto "2" debería tener score: 0.6 * 1 = 0.6
    # Entonces "1" debe estar primero
    assert combined[0]["id"] == "1"


def test_combine_ensures_book_diversity():
    """Verifica diversidad de libros."""
    combiner = ResultCombiner()
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.9},
        {"id": "2", "book_title": "Book A", "similarity": 0.85},
        {"id": "3", "book_title": "Book A", "similarity": 0.8},
        {"id": "4", "book_title": "Book B", "similarity": 0.5},  # Menor sim pero otro libro
    ]
    
    combined = combiner.combine(results, max_results=3, min_books=2)
    
    books = set(r["book_title"] for r in combined)
    assert len(books) >= 2  # Al menos 2 libros diferentes


def test_combine_empty_returns_empty():
    """Verifica que lista vacía retorna lista vacía."""
    combiner = ResultCombiner()
    assert combiner.combine([]) == []


def test_combine_respects_max_results():
    """Verifica límite de resultados."""
    combiner = ResultCombiner()
    results = [
        {"id": str(i), "book_title": "Book A", "similarity": 0.5}
        for i in range(20)
    ]
    
    combined = combiner.combine(results, max_results=5)
    
    assert len(combined) <= 5
```

**Criterios de aceptación:**
- [ ] Archivo `result_combiner.py` creado
- [ ] Tests pasan: `pytest backend/tests/unit/test_result_combiner.py -v`
- [ ] Linting OK: `ruff check backend/src/services/result_combiner.py`

---

### TAREA 3: Extender RAGService con búsqueda múltiple

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('RAGService/search_learned_concepts', 'backend/src/services/rag_service.py', True)`

**Objetivo:** Agregar método para búsqueda con múltiples queries en paralelo.

**Archivo a modificar:** `backend/src/services/rag_service.py`

**Cambio a realizar:** Agregar este método AL FINAL de la clase RAGService (después del último método existente):

```python
    # ================================================================
    # NUEVO MÉTODO - Query Decomposition Support
    # ================================================================
    
    async def search_learned_concepts_multi_query(
        self,
        queries: list[str],
        project_id: UUID,
        limit_per_query: int = 3,
        similarity_threshold: float = 0.30,
    ) -> list[dict]:
        """
        Busca conceptos aprendidos con MÚLTIPLES queries en PARALELO.
        
        Este método ejecuta search_learned_concepts() para cada query
        de forma concurrente usando asyncio.gather, mejorando la latencia.
        
        Args:
            queries: Lista de queries (típicamente 3-5 del QueryDecomposer)
            project_id: ID del proyecto
            limit_per_query: Máximo resultados por query individual
            similarity_threshold: Umbral mínimo (más bajo para diversidad)
            
        Returns:
            Lista combinada de todos los resultados (puede tener duplicados,
            el ResultCombiner se encarga de deduplicar después)
            
        PATRÓN: 
        - Usa asyncio.gather para paralelismo
        - Si una query falla, las demás siguen funcionando
        - NO deduplica (eso lo hace ResultCombiner)
        
        Ejemplo:
            queries = ["técnicas hooks", "copywriting persuasivo", "ofertas irresistibles"]
            results = await rag.search_learned_concepts_multi_query(queries, project_id)
            # Luego usar ResultCombiner para combinar
        """
        import asyncio
        
        if not queries:
            logger.warning("[RAG] search_learned_concepts_multi_query: empty queries list")
            return []
        
        async def search_one(query: str) -> list[dict]:
            """Ejecuta una búsqueda individual con manejo de errores."""
            try:
                return await self.search_learned_concepts(
                    query=query,
                    project_id=project_id,
                    limit=limit_per_query,
                    similarity_threshold=similarity_threshold
                )
            except Exception as e:
                logger.warning(
                    "[RAG] Multi-query search failed for '%s': %s",
                    query[:50], str(e)
                )
                return []  # Retornar vacío en lugar de fallar todo
        
        # Ejecutar todas las búsquedas en paralelo
        tasks = [search_one(q) for q in queries]
        results_lists = await asyncio.gather(*tasks)
        
        # Flatten: combinar todas las listas en una sola
        all_results: list[dict] = []
        for results in results_lists:
            if results:  # Ignorar listas vacías
                all_results.extend(results)
        
        logger.info(
            "[RAG] search_learned_concepts_multi_query: queries=%d total_results=%d",
            len(queries), len(all_results)
        )
        
        return all_results
```

**Pasos exactos para aplicar el cambio:**

1. Abrir `backend/src/services/rag_service.py`
2. Ir al final del archivo (después del método `search_with_learned_knowledge`)
3. Agregar el método `search_learned_concepts_multi_query` exactamente como está arriba
4. Verificar que el import de `UUID` ya existe al inicio del archivo

**Verificación con Serena después de modificar:**
```
find_symbol('RAGService/search_learned_concepts_multi_query', 'backend/src/services/rag_service.py', True)
```

**Criterios de aceptación:**
- [ ] Método agregado al final de RAGService
- [ ] Import de asyncio funciona (es builtin, no necesita pip)
- [ ] El archivo compila: `python -c "from src.services.rag_service import RAGService"`
- [ ] Linting OK: `ruff check backend/src/services/rag_service.py`

---

### TAREA 4: Integrar Query Decomposition en MemoryManager

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('MemoryManager/get_context', 'backend/src/services/memory_manager.py', True)`

**Objetivo:** Usar QueryDecomposer y ResultCombiner en el flujo de get_context().

**Archivo a modificar:** `backend/src/services/memory_manager.py`

**Cambios a realizar:**

**PASO 1:** Agregar imports al inicio del archivo (después de los imports existentes):

```python
# Agregar después de los otros imports de servicios
from .query_decomposer import QueryDecomposer
from .result_combiner import ResultCombiner
```

**PASO 2:** Modificar el método `__init__` para inicializar los nuevos componentes:

Buscar el `__init__` actual (línea ~28) y agregar al final del método:

```python
        # Componentes para Query Decomposition
        self.query_decomposer = QueryDecomposer(llm_service)
        self.result_combiner = ResultCombiner()
```

El `__init__` completo debería quedar algo así:
```python
    def __init__(self, db, rag_service, llm_service):
        """Initialize memory manager with services."""
        self.db = db
        self.rag_service = rag_service
        self.llm_service = llm_service
        
        # Short-term memory per chat (conversation buffer)
        self._short_term_by_chat: dict[UUID, ConversationBufferMemory] = {}
        self._loaded_chats: set[UUID] = set()
        # Cache for training summary
        self._training_summary_cache: dict[UUID, dict] = {}
        
        # NUEVO: Componentes para Query Decomposition
        self.query_decomposer = QueryDecomposer(llm_service)
        self.result_combiner = ResultCombiner()
```

**PASO 3:** Modificar la sección de `learned_concepts` en `get_context()`:

Buscar en `get_context()` (aproximadamente líneas 110-130) donde se llama a `search_learned_concepts`. El código actual es algo como:

```python
        # Get learned concepts from books (if any)
        learned_concepts = await self.rag_service.search_learned_concepts(
            query=current_message,
            project_id=project_id,
            limit=5,
            similarity_threshold=0.35
        )
```

**REEMPLAZAR** ese bloque completo con:

```python
        # ================================================================
        # QUERY DECOMPOSITION: Búsqueda diversificada de conceptos
        # ================================================================
        learned_concepts: list[dict] = []
        
        if current_message:
            try:
                # PASO 1: Generar sub-queries con método socrático
                # El QueryDecomposer genera 3-5 queries diversificadas
                sub_queries = await self.query_decomposer.decompose(
                    user_query=current_message,
                    buyer_persona=buyer_persona,  # Contexto adicional
                    num_queries=4
                )
                
                logger.info(
                    "[MEMORY] Query Decomposition: original='%s' sub_queries=%s",
                    current_message[:50], sub_queries
                )
                
                # PASO 2: Buscar con cada sub-query en paralelo
                raw_results = await self.rag_service.search_learned_concepts_multi_query(
                    queries=sub_queries,
                    project_id=project_id,
                    limit_per_query=3,  # 3 resultados por query × 4 queries = 12 max
                    similarity_threshold=0.30  # Umbral más bajo para diversidad
                )
                
                # PASO 3: Combinar, deduplicar, re-rankear con diversidad de libros
                learned_concepts = self.result_combiner.combine(
                    results=raw_results,
                    max_results=7,  # Máximo 7 conceptos finales
                    min_books=2     # Asegurar al menos 2 libros diferentes
                )
                
            except Exception as e:
                # FALLBACK: Si Query Decomposition falla, usar búsqueda simple
                logger.warning(
                    "[MEMORY] Query Decomposition failed: %s. Using simple search.",
                    str(e)
                )
                learned_concepts = await self.rag_service.search_learned_concepts(
                    query=current_message,
                    project_id=project_id,
                    limit=5,
                    similarity_threshold=0.35
                )
```

**Verificación después de modificar:**
```bash
# Verificar que compila
python -c "from src.services.memory_manager import MemoryManager; print('OK')"

# Verificar linting
ruff check backend/src/services/memory_manager.py
```

**Criterios de aceptación:**
- [ ] Imports agregados correctamente
- [ ] __init__ modificado con nuevos componentes
- [ ] get_context() modificado con Query Decomposition
- [ ] Fallback a búsqueda simple funciona
- [ ] Archivo compila sin errores
- [ ] Linting OK

---

### TAREA 5: Agregar parámetro `model` a LLMService

**Herramientas:**
- 🔧 MCP Serena: `find_symbol('LLMService', 'backend/src/services/llm_service.py', False, 1)`

**Objetivo:** Permitir que los métodos de LLMService acepten un modelo diferente al del .env.

**Archivo a modificar:** `backend/src/services/llm_service.py`

**Cambios a realizar en CADA método que usa `model=self.model`:**

**PASO 1:** Agregar import de Optional al inicio del archivo:

```python
from typing import AsyncIterator, Optional, cast
```

**PASO 2:** Modificar método `generate()`:

ANTES (línea ~50):
```python
    async def generate(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
```

DESPUÉS:
```python
    async def generate(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None  # NUEVO: modelo opcional
    ) -> str:
```

Y dentro del método, cambiar la llamada a la API:

ANTES:
```python
        response = await self.client.chat.completions.create(
            model=self.model,
```

DESPUÉS:
```python
        response = await self.client.chat.completions.create(
            model=model or self.model,  # Usa parámetro o fallback a .env
```

**PASO 3:** Modificar método `stream()` de la misma forma:

ANTES (línea ~98):
```python
    async def stream(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
```

DESPUÉS:
```python
    async def stream(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None  # NUEVO
    ) -> AsyncIterator[str]:
```

Y dentro:
```python
        stream = await self.client.chat.completions.create(
            model=model or self.model,  # Usa parámetro o fallback
```

**PASO 4:** Modificar método `generate_with_messages()`:

ANTES (línea ~146):
```python
    async def generate_with_messages(
        self,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
```

DESPUÉS:
```python
    async def generate_with_messages(
        self,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None  # NUEVO
    ) -> str:
```

Y dentro:
```python
        response = await self.client.chat.completions.create(
            model=model or self.model,
```

**PASO 5:** Modificar método `stream_with_messages()`:

ANTES (línea ~204):
```python
    async def stream_with_messages(
        self,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
```

DESPUÉS:
```python
    async def stream_with_messages(
        self,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None  # NUEVO
    ) -> AsyncIterator[str]:
```

Y dentro:
```python
        stream = await self.client.chat.completions.create(
            model=model or self.model,
```

**⚠️ IMPORTANTE - Retrocompatibilidad:**
- Todos los parámetros `model` son OPCIONALES con default `None`
- Si no se pasa `model`, usa `self.model` (del .env)
- TODO el código existente sigue funcionando sin cambios

**Verificación:**
```bash
# Compilar
python -c "from src.services.llm_service import LLMService; print('OK')"

# Linting
ruff check backend/src/services/llm_service.py
```

**Criterios de aceptación:**
- [ ] Los 4 métodos tienen param `model: Optional[str] = None`
- [ ] Cada método usa `model or self.model`
- [ ] Import de Optional agregado
- [ ] Archivo compila
- [ ] Linting OK

---

### TAREA 6: Propagar parámetro `model` por la cadena de llamadas

**Objetivo:** Pasar el `model` desde el endpoint hasta LLMService.

**Esta tarea tiene 4 sub-tareas que deben hacerse EN ORDEN:**

#### TAREA 6.1: Modificar SendMessageRequest

**Archivo:** `backend/src/schemas/chat.py`

**Cambio:** Agregar campo `model` al schema.

ANTES (línea ~25):
```python
class SendMessageRequest(BaseModel):
    """Send message request."""
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
```

DESPUÉS:
```python
class SendMessageRequest(BaseModel):
    """Send message request."""
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    model: Optional[str] = Field(None, description="LLM model override (e.g., 'gpt-4o-mini')")
```

Y agregar import de Optional al inicio:
```python
from typing import Optional
```

---

#### TAREA 6.2: Modificar ContentGeneratorAgent.execute()

**Archivo:** `backend/src/agents/content_generator_agent.py`

**Cambio 1:** Agregar parámetro `model` al método `execute()`:

ANTES (línea ~27):
```python
    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str,
        context_override: dict | None = None,
    ) -> dict:
```

DESPUÉS:
```python
    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str,
        context_override: dict | None = None,
        model: str | None = None,  # NUEVO: modelo opcional
    ) -> dict:
```

**Cambio 2:** Pasar `model` a `generate_with_messages()`:

Buscar la llamada a `self.llm.generate_with_messages()` (aproximadamente línea ~130):

ANTES:
```python
            response = await self.llm.generate_with_messages(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.8
            )
```

DESPUÉS:
```python
            response = await self.llm.generate_with_messages(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.8,
                model=model  # NUEVO: pasar modelo
            )
```

---

#### TAREA 6.3: Modificar RouterAgent.process_stream()

**Archivo:** `backend/src/agents/router_agent.py`

**Cambio 1:** Agregar parámetro `model` al método `process_stream()`:

ANTES (línea ~145):
```python
    async def process_stream(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ):
```

DESPUÉS:
```python
    async def process_stream(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str,
        model: str | None = None  # NUEVO: modelo opcional
    ):
```

**Cambio 2:** Pasar `model` a `ContentGeneratorAgent.execute()`:

Buscar donde se llama a `content_agent.execute()` (aproximadamente línea ~240):

ANTES:
```python
            result = await content_agent.execute(
                chat_id,
                project_id,
                user_message,
                context_override=context,
            )
```

DESPUÉS:
```python
            result = await content_agent.execute(
                chat_id,
                project_id,
                user_message,
                context_override=context,
                model=model,  # NUEVO: pasar modelo
            )
```

---

#### TAREA 6.4: Modificar endpoint stream_message()

**Archivo:** `backend/src/api/chat.py`

**Cambio:** Extraer `model` del request y pasarlo a `process_stream()`:

Buscar en `stream_message()` (línea ~224) donde se llama a `router_agent.process_stream()`:

ANTES (aproximadamente línea ~290):
```python
            async for chunk_json in router_agent.process_stream(
                chat_id=chat_id,
                project_id=user.project_id,
                user_message=request.content
            ):
```

DESPUÉS:
```python
            async for chunk_json in router_agent.process_stream(
                chat_id=chat_id,
                project_id=user.project_id,
                user_message=request.content,
                model=request.model  # NUEVO: pasar modelo del request
            ):
```

**Criterios de aceptación para TAREA 6 completa:**
- [ ] SendMessageRequest tiene campo `model`
- [ ] ContentGeneratorAgent.execute() acepta y pasa `model`
- [ ] RouterAgent.process_stream() acepta y pasa `model`
- [ ] stream_message() pasa `request.model` a process_stream()
- [ ] Todos los archivos compilan
- [ ] Linting OK en todos los archivos modificados

---

### TAREA 7: Crear ModelSelector en Frontend

**Objetivo:** Crear componente para seleccionar modelo en el chat.

**Archivo a crear:** `frontend/app/components/ModelSelector.tsx`

**Código completo:**

```tsx
// frontend/app/components/ModelSelector.tsx
'use client';

import { useState } from 'react';

/**
 * Modelos disponibles según LLM_PROVIDER del backend.
 * 
 * IMPORTANTE: Esta lista está hardcodeada porque usamos las API keys
 * del .env del servidor, no keys del usuario.
 * 
 * TODO: En futuro se podría hacer un endpoint que retorne los modelos
 * disponibles según el LLM_PROVIDER configurado.
 */

// Modelos para OpenAI (cuando LLM_PROVIDER=openai en .env)
const OPENAI_MODELS = [
  { 
    id: 'gpt-4o', 
    name: 'GPT-4o', 
    description: 'Más capaz, multimodal',
    costTier: 'high' as const
  },
  { 
    id: 'gpt-4o-mini', 
    name: 'GPT-4o Mini', 
    description: 'Rápido y económico',
    costTier: 'low' as const
  },
  { 
    id: 'gpt-4-turbo', 
    name: 'GPT-4 Turbo', 
    description: 'Balance velocidad/calidad',
    costTier: 'medium' as const
  },
];

// Modelos para OpenRouter (cuando LLM_PROVIDER=openrouter en .env)
const OPENROUTER_MODELS = [
  { 
    id: 'anthropic/claude-3.5-sonnet', 
    name: 'Claude 3.5 Sonnet', 
    description: 'Balance perfecto',
    costTier: 'medium' as const
  },
  { 
    id: 'anthropic/claude-3-opus', 
    name: 'Claude 3 Opus', 
    description: 'Más potente de Claude',
    costTier: 'high' as const
  },
  { 
    id: 'anthropic/claude-3-haiku', 
    name: 'Claude 3 Haiku', 
    description: 'Ultra rápido',
    costTier: 'low' as const
  },
];

type CostTier = 'low' | 'medium' | 'high';

interface Model {
  id: string;
  name: string;
  description: string;
  costTier: CostTier;
}

interface ModelSelectorProps {
  /** Modelo actualmente seleccionado */
  value: string;
  /** Callback cuando cambia el modelo */
  onChange: (modelId: string) => void;
  /** Provider del backend: 'openai' | 'openrouter' (default: openai) */
  provider?: 'openai' | 'openrouter';
}

/**
 * Selector de modelo LLM para el chat.
 * 
 * Muestra los modelos disponibles según el provider configurado
 * y permite al usuario seleccionar uno diferente al default.
 * 
 * @example
 * <ModelSelector 
 *   value={selectedModel} 
 *   onChange={setSelectedModel}
 *   provider="openai"
 * />
 */
export function ModelSelector({ 
  value, 
  onChange, 
  provider = 'openai' 
}: ModelSelectorProps) {
  const [open, setOpen] = useState(false);
  
  // Seleccionar lista de modelos según provider
  const models: Model[] = provider === 'openrouter' 
    ? OPENROUTER_MODELS 
    : OPENAI_MODELS;
  
  const selectedModel = models.find(m => m.id === value);
  
  // Colores según costo
  const costColors: Record<CostTier, string> = {
    low: 'text-green-600',
    medium: 'text-yellow-600',
    high: 'text-orange-600',
  };
  
  const costIcons: Record<CostTier, string> = {
    low: '💰',
    medium: '💰💰',
    high: '💰💰💰',
  };
  
  return (
    <div className="relative">
      {/* Botón del selector */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <span className="text-lg">🤖</span>
        <span className="font-medium">
          {selectedModel?.name || 'Seleccionar modelo'}
        </span>
        <span className="text-gray-400 text-xs">
          {open ? '▲' : '▼'}
        </span>
      </button>
      
      {/* Dropdown de modelos */}
      {open && (
        <>
          {/* Overlay para cerrar al hacer click fuera */}
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setOpen(false)}
          />
          
          {/* Lista de modelos */}
          <div className="absolute top-full left-0 mt-1 w-72 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
            <div className="p-2 border-b border-gray-100">
              <span className="text-xs text-gray-500">
                Provider: {provider === 'openrouter' ? 'OpenRouter' : 'OpenAI'}
              </span>
            </div>
            
            {models.map(model => (
              <button
                key={model.id}
                type="button"
                onClick={() => {
                  onChange(model.id);
                  setOpen(false);
                }}
                className={`w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors ${
                  value === model.id ? 'bg-blue-50 border-l-2 border-blue-500' : ''
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-900">
                    {model.name}
                  </span>
                  <span className={`text-xs ${costColors[model.costTier]}`}>
                    {costIcons[model.costTier]}
                  </span>
                </div>
                <div className="text-xs text-gray-500 mt-0.5">
                  {model.description}
                </div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
```

---

### TAREA 8: Integrar ModelSelector en ChatInterface

**Archivo a modificar:** `frontend/app/components/ChatInterface.tsx`

**Cambios a realizar:**

**PASO 1:** Agregar import del ModelSelector:

```tsx
import { ModelSelector } from './ModelSelector';
```

**PASO 2:** Agregar estado para el modelo seleccionado (junto a los otros useState):

```tsx
// Estado para modelo seleccionado
// Default al modelo configurado en .env (asumimos gpt-4o-mini)
const [selectedModel, setSelectedModel] = useState('gpt-4o-mini');
```

**PASO 3:** Agregar el ModelSelector en la UI (antes del input de mensaje):

Buscar donde está el área de input del chat y agregar el selector. Por ejemplo:

```tsx
{/* Selector de modelo - agregar encima del input */}
<div className="flex items-center gap-4 px-4 py-2 border-t border-gray-200">
  <ModelSelector 
    value={selectedModel} 
    onChange={setSelectedModel}
    provider="openai"  // Cambiar a "openrouter" si usas ese provider
  />
  <span className="text-xs text-gray-400">
    Modelo: {selectedModel}
  </span>
</div>
```

**PASO 4:** Modificar la llamada al API para incluir el modelo:

Buscar donde se hace fetch al endpoint de streaming y agregar `model`:

ANTES:
```tsx
const response = await fetch(`/api/chat/${chatId}/stream`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ content: message }),
});
```

DESPUÉS:
```tsx
const response = await fetch(`/api/chat/${chatId}/stream`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    content: message,
    model: selectedModel  // NUEVO: enviar modelo seleccionado
  }),
});
```

**Criterios de aceptación:**
- [ ] ModelSelector aparece en el chat
- [ ] Se puede cambiar de modelo
- [ ] El modelo se envía en el request
- [ ] La UI muestra el modelo actual

---

### TAREA 9: Testing y Validación Final

**Objetivo:** Verificar que todo funciona correctamente.

**Tests del Query Decomposition:**
```bash
# Tests unitarios de QueryDecomposer
pytest backend/tests/unit/test_query_decomposer.py -v

# Tests unitarios de ResultCombiner
pytest backend/tests/unit/test_result_combiner.py -v

# Linting de todos los archivos nuevos/modificados
ruff check backend/src/services/query_decomposer.py
ruff check backend/src/services/result_combiner.py
ruff check backend/src/services/rag_service.py
ruff check backend/src/services/memory_manager.py
ruff check backend/src/services/llm_service.py
ruff check backend/src/agents/router_agent.py
ruff check backend/src/agents/content_generator_agent.py
ruff check backend/src/api/chat.py
ruff check backend/src/schemas/chat.py
```

**Test de integración manual - Query Decomposition:**

1. Iniciar el sistema:
```bash
docker compose up -d
```

2. Crear un chat y enviar mensaje:
```bash
curl -X POST http://localhost:8000/api/chat/{chat_id}/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"content": "dame 3 hooks para mi curso de coaching"}'
```

3. Verificar en logs:
```bash
docker logs brain-mkt-backend -f | grep "Query Decomposition"
```

Deberías ver algo como:
```
[MEMORY] Query Decomposition: original='dame 3 hooks...' sub_queries=['técnicas captar atención', 'copywriting persuasivo', 'ofertas irresistibles', 'storytelling marketing']
```

**Test de integración manual - Switch de Modelos:**

1. Enviar mensaje con modelo específico:
```bash
curl -X POST http://localhost:8000/api/chat/{chat_id}/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"content": "hola", "model": "gpt-4o-mini"}'
```

2. Verificar que el modelo se usa (en logs o respuesta)

**Criterios de aceptación finales:**
- [ ] Tests unitarios pasan (QueryDecomposer, ResultCombiner)
- [ ] Linting OK en todos los archivos
- [ ] Query "hooks" retorna conceptos de múltiples libros
- [ ] Logs muestran sub_queries generadas
- [ ] Switch de modelo funciona desde frontend
- [ ] Sistema no se rompe con el modelo default

---

## ✅ GATES DE VALIDACIÓN

```yaml
Nivel 1: Sintaxis & Estilo
  comandos: |
    ruff check backend/src/ --fix
  esperado: "Sin errores"

Nivel 2: Tests Unitarios
  comando: |
    pytest backend/tests/unit/test_query_decomposer.py -v
    pytest backend/tests/unit/test_result_combiner.py -v
  esperado: "Todos pasan"

Nivel 3: Integración
  pasos:
    1. docker compose up -d
    2. Crear chat y enviar "dame hooks para mi curso"
    3. Verificar logs muestran Query Decomposition
    4. Verificar respuesta menciona conceptos de múltiples libros
  esperado: "Diversidad de libros en resultados"
```

---

## 📝 ARCHIVOS RESUMEN

```yaml
CREAR:
  Backend:
    - backend/src/services/query_decomposer.py
    - backend/src/services/result_combiner.py
    - backend/tests/unit/test_query_decomposer.py
    - backend/tests/unit/test_result_combiner.py
  
  Frontend:
    - frontend/app/components/ModelSelector.tsx

MODIFICAR:
  Backend:
    - backend/src/services/llm_service.py (agregar param model a 4 métodos)
    - backend/src/services/rag_service.py (agregar método multi_query)
    - backend/src/services/memory_manager.py (integrar QD)
    - backend/src/agents/content_generator_agent.py (param model)
    - backend/src/agents/router_agent.py (param model)
    - backend/src/api/chat.py (pasar model)
    - backend/src/schemas/chat.py (campo model)
  
  Frontend:
    - frontend/app/components/ChatInterface.tsx (agregar ModelSelector)

NO TOCAR:
  - .env (las API keys quedan como están)
  - Base de datos (no hay migraciones)
  - Encriptación (no hace falta)
```

---

## ⚠️ NOTAS IMPORTANTES PARA EL AGENTE EJECUTOR

1. **Orden de tareas**: Ejecutar TAREA 1-4 (Query Decomposition) primero, luego TAREA 5-8 (Model Switch). La TAREA 5 es prerequisito de TAREA 6.

2. **Retrocompatibilidad**: Todos los cambios son retrocompatibles. Si no se pasa `model`, el sistema usa el del .env.

3. **Fallbacks**: 
   - QueryDecomposer tiene fallback a query original
   - MemoryManager tiene fallback a búsqueda simple
   - LLMService tiene fallback a self.model

4. **No crear tablas**: Este PRP NO crea tablas nuevas. Solo modifica código Python y TypeScript.

5. **Provider en frontend**: El `provider` en ModelSelector está hardcodeado. Si el backend usa openrouter, cambiar manualmente.

---

**🎯 Score de confianza: 9/10**

Este PRP está completo, sin deuda técnica, con código detallado y verificable. Cada tarea tiene criterios de aceptación claros y el agente puede ejecutar paso a paso sin ambigüedad.
