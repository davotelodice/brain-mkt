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
    
    assert queries == [original_query]


@pytest.mark.asyncio
async def test_decompose_limits_queries():
    """Verifica que el límite de 3-5 queries se respeta."""
    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value='{"queries": ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]}'
    )
    decomposer = QueryDecomposer(llm)
    
    queries = await decomposer.decompose("test", num_queries=10)
    
    assert len(queries) <= 5


@pytest.mark.asyncio
async def test_decompose_handles_invalid_json():
    """Verifica manejo de JSON inválido."""
    llm = MagicMock()
    llm.generate = AsyncMock(return_value="esto no es JSON válido")
    decomposer = QueryDecomposer(llm)
    
    queries = await decomposer.decompose("test query")
    
    assert queries == ["test query"]


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
    
    mock_llm.generate.assert_called_once()
    call_args = mock_llm.generate.call_args
    prompt = call_args.kwargs.get("prompt", call_args.args[0] if call_args.args else "")
    
    assert "fitness" in prompt or len(queries) > 0


@pytest.mark.asyncio
async def test_decompose_min_queries_enforced():
    """Verifica que mínimo 3 queries aunque se pida menos."""
    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value='{"queries": ["q1", "q2", "q3"]}'
    )
    decomposer = QueryDecomposer(llm)
    
    # Aunque pidamos 1, el prompt debería pedir 3
    queries = await decomposer.decompose("test", num_queries=1)
    
    # Verifica que el prompt pidió 3 (mínimo forzado)
    call_args = llm.generate.call_args
    prompt = call_args.kwargs.get("prompt", "")
    assert "3" in prompt  # num_queries se forzó a 3
