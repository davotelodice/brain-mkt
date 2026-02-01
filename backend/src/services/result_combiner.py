# backend/src/services/result_combiner.py
"""
Result Combiner - Combina y re-rankea resultados de múltiples búsquedas RAG.

Este servicio toma resultados de múltiples queries y los combina
de forma inteligente para maximizar diversidad y relevancia.
"""

import logging
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


class ResultCombiner:
    """
    Combina resultados de múltiples búsquedas RAG.

    Funcionalidades:
    - Deduplica por ID de concepto
    - Re-rankea por frecuencia × similarity
    - Asegura diversidad de libros

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
            max_results: Número máximo de resultados a retornar
            min_books: Mínimo de libros diferentes a incluir

        Returns:
            Lista de resultados únicos, ordenados por relevancia combinada.
        """
        if not results:
            return []

        concept_data = self._aggregate_concepts(results)
        scored = self._calculate_scores(concept_data)
        final = self._apply_diversity(scored, max_results, min_books)

        return final

    def _aggregate_concepts(
        self, results: list[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Agrupa resultados por ID y calcula estadísticas."""
        concept_data: dict[str, dict[str, Any]] = defaultdict(lambda: {
            "concept": None,
            "appearances": 0,
            "similarities": [],
            "book": None
        })

        for result in results:
            concept_id = result.get("id")
            if not concept_id:
                continue

            data = concept_data[concept_id]

            if data["concept"] is None:
                data["concept"] = result

            data["appearances"] += 1

            similarity = result.get("similarity", 0)
            if isinstance(similarity, (int, float)):
                data["similarities"].append(float(similarity))

            data["book"] = result.get("book_title", "unknown")

        return concept_data

    def _calculate_scores(
        self, concept_data: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Calcula score combinado para cada concepto."""
        scored: list[dict[str, Any]] = []

        for concept_id, data in concept_data.items():
            if not data["concept"]:
                continue

            avg_similarity = (
                sum(data["similarities"]) / len(data["similarities"])
                if data["similarities"]
                else 0
            )

            # Boost por frecuencia: +30% por cada aparición adicional
            frequency_boost = 1 + (data["appearances"] - 1) * 0.3
            combined_score = avg_similarity * frequency_boost

            scored.append({
                **data["concept"],
                "combined_score": combined_score,
                "appearances": data["appearances"],
                "_book": data["book"]
            })

        scored.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
        return scored

    def _apply_diversity(
        self,
        scored: list[dict[str, Any]],
        max_results: int,
        min_books: int,
    ) -> list[dict[str, Any]]:
        """Asegura diversidad de libros en los resultados."""
        final: list[dict[str, Any]] = []
        books_seen: set[str] = set()

        # Primera pasada: incluir al menos un concepto de cada libro
        for concept in scored:
            book = concept.get("_book", "unknown")
            if book not in books_seen and len(books_seen) < min_books:
                concept_clean = {k: v for k, v in concept.items() if k != "_book"}
                final.append(concept_clean)
                books_seen.add(book)

        # Segunda pasada: llenar hasta max_results
        for concept in scored:
            if len(final) >= max_results:
                break

            concept_id = concept.get("id")
            if any(c.get("id") == concept_id for c in final):
                continue

            concept_clean = {k: v for k, v in concept.items() if k != "_book"}
            final.append(concept_clean)
            books_seen.add(concept.get("_book", "unknown"))

        logger.info(
            "[ResultCombiner] input=%d unique=%d output=%d books=%s",
            len(scored) + len([c for c in scored if c.get("appearances", 1) > 1]),
            len(scored),
            len(final),
            list(books_seen)
        )

        return final
