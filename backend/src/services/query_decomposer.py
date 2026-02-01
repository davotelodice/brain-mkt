# backend/src/services/query_decomposer.py
"""
Query Decomposer - Genera múltiples sub-queries usando método socrático.

Este servicio toma una query del usuario y la descompone en 3-5 sub-queries
diversificadas para mejorar la búsqueda semántica en RAG.
"""

import json
import logging

from .llm_service import LLMService

logger = logging.getLogger(__name__)


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
    """

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def decompose(
        self,
        user_query: str,
        buyer_persona: dict | None = None,
        num_queries: int = 4,
    ) -> list[str]:
        """
        Descompone una query en múltiples sub-queries diversificadas.

        Args:
            user_query: Query original del usuario
            buyer_persona: Contexto del buyer persona (opcional)
            num_queries: Número de queries a generar (se fuerza entre 3-5)

        Returns:
            Lista de sub-queries. Si falla, retorna [user_query].
        """
        num_queries = max(3, min(5, num_queries))
        context = self._build_context(buyer_persona)

        prompt = SOCRATIC_PROMPT.format(
            user_query=user_query,
            context=context,
            num_queries=num_queries
        )

        try:
            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=300
            )

            queries = self._parse_response(response, num_queries, user_query)

            logger.info(
                "[QueryDecomposer] original='%s' generated=%d queries=%s",
                user_query[:50], len(queries), queries
            )

            return queries

        except Exception as e:
            logger.warning(
                "[QueryDecomposer] Failed for '%s': %s. Using fallback.",
                user_query[:50], str(e)
            )
            return [user_query]

    def _build_context(self, buyer_persona: dict | None) -> str:
        """Extrae contexto relevante del buyer persona."""
        if not buyer_persona or not isinstance(buyer_persona, dict):
            return "No hay contexto adicional disponible."

        parts = []

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
        """Parsea respuesta JSON del LLM."""
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start == -1 or json_end == 0:
                logger.warning("[QueryDecomposer] No JSON found in response")
                return [fallback]

            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)

            queries = parsed.get("queries", [])

            reasoning = parsed.get("reasoning", "")
            if reasoning:
                logger.debug("[QueryDecomposer] reasoning: %s", reasoning[:100])

            valid_queries = [q for q in queries if isinstance(q, str) and q.strip()]

            if not valid_queries:
                logger.warning("[QueryDecomposer] No valid queries in response")
                return [fallback]

            return valid_queries[:num_queries]

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning("[QueryDecomposer] JSON parse failed: %s", str(e))
            return [fallback]
