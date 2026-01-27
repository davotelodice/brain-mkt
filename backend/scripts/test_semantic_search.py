"""
Script para probar la búsqueda semántica después de la ingesta.
Verifica que los datos de Andrea Estratega se pueden recuperar correctamente.
"""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from db.database import AsyncSessionLocal  # noqa: E402
from services.embedding_service import EmbeddingService  # noqa: E402
from services.llm_service import LLMService  # noqa: E402
from services.rag_service import RAGService  # noqa: E402


async def test_searches():
    """Ejecuta varias búsquedas de prueba."""
    print("=" * 70)
    print("🔍 TEST DE BÚSQUEDA SEMÁNTICA - TAREA 5")
    print("=" * 70)
    print()

    # Inicializar servicios
    embedding_service = EmbeddingService()
    llm_service = LLMService()

    async with AsyncSessionLocal() as db:
        rag_service = RAGService(
            db=db,
            embedding_service=embedding_service,
            llm_service=llm_service
        )

        # ID de proyecto ficticio para testing
        test_project_id = uuid4()

        # Test 1: Búsqueda simple sobre carruseles
        print("📌 Test 1: Búsqueda sobre 'carruseles virales Instagram'")
        print("-" * 70)

        results_simple = await rag_service.search_relevant_docs(
            query="¿Cómo hacer carruseles virales en Instagram?",
            project_id=test_project_id,
            limit=3,
            rerank=False
        )

        print(f"✅ Encontrados {len(results_simple)} resultados (sin reranking):")
        for i, doc in enumerate(results_simple, 1):
            print(f"\n  [{i}] {doc['source_title']}")
            print(f"      Similarity: {doc['similarity']:.3f}")
            print(f"      Tipo: {doc['content_type']}")
            print(f"      Preview: {doc['content'][:150]}...")

        print()
        print("=" * 70)

        # Test 2: Búsqueda CON reranking
        print("\n📌 Test 2: Misma búsqueda CON reranking")
        print("-" * 70)

        results_reranked = await rag_service.search_relevant_docs(
            query="¿Cómo hacer carruseles virales en Instagram?",
            project_id=test_project_id,
            limit=3,
            rerank=True
        )

        print(f"✅ Encontrados {len(results_reranked)} resultados (CON reranking):")
        for i, doc in enumerate(results_reranked, 1):
            print(f"\n  [{i}] {doc['source_title']}")
            print(f"      Similarity: {doc.get('similarity', 0):.3f}")
            print(f"      Rerank Score: {doc.get('rerank_score', 0):.3f}")
            print(f"      Preview: {doc['content'][:150]}...")

        print()
        print("=" * 70)

        # Test 3: Búsqueda con filtro de metadata
        print("\n📌 Test 3: Búsqueda con filtro de metadata (solo video_transcript)")
        print("-" * 70)

        results_filtered = await rag_service.search_relevant_docs(
            query="estrategias de crecimiento en redes sociales",
            project_id=test_project_id,
            limit=3,
            rerank=False,
            metadata_filters={"content_type": "video_transcript"}
        )

        print(f"✅ Encontrados {len(results_filtered)} resultados (filtrados):")
        for i, doc in enumerate(results_filtered, 1):
            print(f"\n  [{i}] {doc['source_title']}")
            print(f"      Tipo: {doc['content_type']}")
            print(f"      Metadata: {doc.get('metadata', {})}")

        print()
        print("=" * 70)
        print("✨ TESTS COMPLETADOS")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_searches())
