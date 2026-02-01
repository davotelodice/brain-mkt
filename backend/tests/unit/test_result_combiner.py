# backend/tests/unit/test_result_combiner.py
"""Tests para ResultCombiner."""

from src.services.result_combiner import ResultCombiner


def test_combine_deduplicates():
    """Verifica que deduplica por ID."""
    combiner = ResultCombiner()
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.8},
        {"id": "1", "book_title": "Book A", "similarity": 0.7},
        {"id": "2", "book_title": "Book B", "similarity": 0.6},
    ]

    combined = combiner.combine(results)

    ids = [r["id"] for r in combined]
    assert len(ids) == len(set(ids))
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
    assert combined[0]["id"] == "1"


def test_combine_ensures_book_diversity():
    """Verifica diversidad de libros."""
    combiner = ResultCombiner()
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.9},
        {"id": "2", "book_title": "Book A", "similarity": 0.85},
        {"id": "3", "book_title": "Book A", "similarity": 0.8},
        {"id": "4", "book_title": "Book B", "similarity": 0.5},
    ]

    combined = combiner.combine(results, max_results=3, min_books=2)

    books = set(r["book_title"] for r in combined)
    assert len(books) >= 2


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


def test_combine_handles_missing_id():
    """Verifica que ignora resultados sin ID."""
    combiner = ResultCombiner()
    results = [
        {"id": "1", "book_title": "Book A", "similarity": 0.8},
        {"book_title": "Book B", "similarity": 0.7},  # Sin ID
        {"id": "2", "book_title": "Book C", "similarity": 0.6},
    ]

    combined = combiner.combine(results)

    assert len(combined) == 2
    ids = [r["id"] for r in combined]
    assert "1" in ids
    assert "2" in ids
