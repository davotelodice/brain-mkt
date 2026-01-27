"""
Script para ingestar transcripciones de YouTube a la knowledge base.
Procesa archivos .txt, genera embeddings y los almacena en marketing_knowledge_base.

TAREA 5: Entrenamiento RAG con contenido de Andrea Estratega
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from db.database import AsyncSessionLocal  # noqa: E402
from db.models import MarketingKnowledgeBase  # noqa: E402
from services.embedding_service import EmbeddingService  # noqa: E402

# Configuración de chunking (según PRP y skill rag-implementation)
CHUNK_SIZE = 800  # tokens (~3000 caracteres)
CHUNK_OVERLAP = 100  # tokens para mantener contexto


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Divide texto en chunks con overlap para mantener contexto.

    Usa word-based chunking (recomendación de rag-implementation skill).

    Args:
        text: Texto completo a dividir
        chunk_size: Tamaño aproximado en tokens (words)
        overlap: Cantidad de tokens de overlap entre chunks

    Returns:
        Lista de chunks de texto
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():  # Solo agregar chunks no vacíos
            chunks.append(chunk)

    return chunks


async def ingest_youtube_transcripts(source_dir: str):
    """
    Procesa transcripciones de YouTube y las sube a knowledge_base.

    Args:
        source_dir: Directorio con archivos .txt de transcripciones
    """
    print("=" * 70)
    print("📚 INGESTA DE DATOS - TAREA 5: Entrenamiento RAG")
    print("=" * 70)

    # 1. Inicializar servicios
    print("\n🔧 Inicializando servicios...")
    embedding_service = EmbeddingService()  # Carga OPENAI_API_KEY desde .env automáticamente

    # 2. Cargar archivos .txt
    transcript_dir = Path(source_dir)
    if not transcript_dir.exists():
        print(f"❌ ERROR: Directorio no encontrado: {transcript_dir}")
        return

    transcript_files = sorted(transcript_dir.glob('*.txt'))

    if len(transcript_files) == 0:
        print(f"❌ ERROR: No se encontraron archivos .txt en {transcript_dir}")
        return

    print(f"✅ Encontrados {len(transcript_files)} archivos de transcripciones")
    print()

    all_chunks = []

    # 3. Procesar cada archivo
    print("📄 Procesando archivos...")
    print("-" * 70)

    for file_path in transcript_files:
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            # Dividir en chunks con overlap
            chunks = chunk_text(content)

            # Preparar metadata para cada chunk
            for idx, chunk_text_content in enumerate(chunks):
                all_chunks.append({
                    'source_title': file_path.stem,  # Nombre del video (sin extensión)
                    'chunk_text': chunk_text_content,
                    'chunk_index': idx,
                    'content_type': 'video_transcript',
                    'metadata': {
                        'source': 'youtube',
                        'author': 'Andrea Estratega',
                        'filename': file_path.name
                    }
                })

            print(f"  ✅ {file_path.name}")
            print(f"     └─ {len(chunks)} chunks ({len(content)} caracteres)")

        except Exception as e:
            print(f"  ❌ ERROR en {file_path.name}: {e}")

    print("-" * 70)
    print(f"📊 Total: {len(all_chunks)} chunks a procesar\n")

    if len(all_chunks) == 0:
        print("❌ No hay chunks para procesar. Abortando.")
        return

    # 4. Generar embeddings en batch (GOTCHA 5 - rate limits manejados)
    print("🔄 Generando embeddings...")
    print("⏳ Esto puede tomar 2-5 minutos dependiendo del tamaño...")
    print()

    try:
        texts = [chunk['chunk_text'] for chunk in all_chunks]
        embeddings = await embedding_service.generate_embeddings_batch(texts)

        print(f"✅ {len(embeddings)} embeddings generados correctamente")
    except Exception as e:
        print(f"❌ ERROR generando embeddings: {e}")
        return

    # 5. Insertar en base de datos
    print("\n💾 Insertando en marketing_knowledge_base...")
    print("⏳ Guardando chunks en la base de datos...")
    print()

    try:
        async with AsyncSessionLocal() as db:
            inserted_count = 0

            for chunk, embedding in zip(all_chunks, embeddings):
                # IMPORTANTE: Usar el ORM de SQLAlchemy (como en document_processor.py)
                # SQLAlchemy + pgvector maneja automáticamente la conversión de list a vector
                # NO necesitamos convertir a string manualmente

                kb_entry = MarketingKnowledgeBase(
                    project_id=None,  # Global knowledge (NULL en DB)
                    chat_id=None,     # Global knowledge (NULL en DB)
                    content_type=chunk['content_type'],
                    source_title=chunk['source_title'],
                    chunk_text=chunk['chunk_text'],
                    chunk_index=chunk['chunk_index'],
                    metadata_=chunk['metadata'],  # Note: metadata_ not metadata (SQLAlchemy reserved)
                    embedding=embedding  # List de Python, SQLAlchemy lo convierte automáticamente
                )

                db.add(kb_entry)
                inserted_count += 1

                # Progress indicator cada 50 chunks
                if inserted_count % 50 == 0:
                    print(f"  ⏳ Progreso: {inserted_count}/{len(all_chunks)} chunks insertados...")

            await db.commit()
            print(f"✅ {inserted_count} chunks insertados exitosamente")

    except Exception as e:
        print(f"❌ ERROR insertando en base de datos: {e}")
        import traceback
        traceback.print_exc()
        return

    # 6. Resumen final
    print()
    print("=" * 70)
    print("✨ INGESTA COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print(f"📁 Archivos procesados: {len(transcript_files)}")
    print(f"📦 Chunks creados: {len(all_chunks)}")
    print(f"🔢 Embeddings generados: {len(embeddings)}")
    print(f"💾 Registros en DB: {inserted_count}")
    print()
    print("🔍 Verifica los datos con:")
    print("   SELECT content_type, COUNT(*) FROM marketing_knowledge_base")
    print("   WHERE content_type = 'video_transcript' GROUP BY content_type;")
    print("=" * 70)


if __name__ == "__main__":
    # Ruta al directorio de transcripciones (relativa al root del proyecto)
    project_root = Path(__file__).parent.parent.parent
    source_directory = project_root / "contenido" / "Transcriptions Andrea Estratega"

    # Ejecutar ingesta
    asyncio.run(ingest_youtube_transcripts(str(source_directory)))
