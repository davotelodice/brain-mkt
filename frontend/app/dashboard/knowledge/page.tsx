'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { BookUpload } from '@/app/components/BookUpload'
import { LearnedBookCard } from '@/app/components/LearnedBookCard'
import { ConceptsViewer } from '@/app/components/ConceptsViewer'
import { listLearnedBooks } from '@/lib/api-knowledge'
import type { LearnedBook } from '@/lib/types'

/**
 * Knowledge Library Page - Manage learned books.
 * TAREA 6: Full page for book management.
 * 
 * ✅ react-patterns: Loading/error/empty states
 * ✅ nextjs-best-practices: Client component with data fetching
 */
export default function KnowledgePage() {
  const [books, setBooks] = useState<LearnedBook[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedBook, setSelectedBook] = useState<LearnedBook | null>(null)
  const router = useRouter()

  useEffect(() => {
    loadBooks()
  }, [])

  const loadBooks = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const loadedBooks = await listLearnedBooks()
      setBooks(loadedBooks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al cargar libros')
    } finally {
      setIsLoading(false)
    }
  }

  const handleBookUploaded = (book: LearnedBook) => {
    setBooks(prev => [book, ...prev])
  }

  const handleBookDeleted = (bookId: string) => {
    setBooks(prev => prev.filter(b => b.id !== bookId))
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/')}
              className="text-gray-500 hover:text-gray-700 transition"
            >
              ← Volver
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">📚 Biblioteca de Conocimiento</h1>
              <p className="text-sm text-gray-500">
                Sube libros para que el asistente aprenda de ellos
              </p>
            </div>
          </div>
          <button
            onClick={loadBooks}
            className="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition"
          >
            🔄 Actualizar
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Upload section */}
        <section className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Subir nuevo libro</h2>
          <BookUpload onBookUploaded={handleBookUploaded} />
        </section>

        {/* Books list */}
        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Libros procesados ({books.length})
          </h2>

          {isLoading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4" />
              <p className="text-gray-500">Cargando libros...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12 bg-white rounded-xl">
              <div className="text-red-500 text-4xl mb-4">⚠️</div>
              <p className="text-red-600 mb-4">{error}</p>
              <button
                onClick={loadBooks}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                Reintentar
              </button>
            </div>
          ) : books.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-xl">
              <div className="text-6xl mb-4">📚</div>
              <p className="text-gray-600 mb-2">No hay libros en tu biblioteca</p>
              <p className="text-sm text-gray-500">
                Sube tu primer libro para que el asistente aprenda de él
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {books.map(book => (
                <LearnedBookCard
                  key={book.id}
                  book={book}
                  onDeleted={handleBookDeleted}
                  onViewConcepts={setSelectedBook}
                />
              ))}
            </div>
          )}
        </section>
      </main>

      {/* Concepts Modal */}
      {selectedBook && (
        <ConceptsViewer
          book={selectedBook}
          onClose={() => setSelectedBook(null)}
        />
      )}
    </div>
  )
}
