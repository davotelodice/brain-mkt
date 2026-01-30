'use client'

import { useState, useEffect } from 'react'
import type { LearnedBook } from '@/lib/types'
import { getBookStatus, deleteLearnedBook } from '@/lib/api-knowledge'

interface LearnedBookCardProps {
  book: LearnedBook
  onDeleted?: (bookId: string) => void
  onViewConcepts?: (book: LearnedBook) => void
}

/**
 * LearnedBookCard - Displays book info with processing status.
 * TAREA 6: Shows progress, concepts count, and actions.
 * 
 * ✅ react-patterns: Polling for status updates, clean UI states
 * ✅ nextjs-best-practices: Client component for interactivity
 */
export function LearnedBookCard({ book: initialBook, onDeleted, onViewConcepts }: LearnedBookCardProps) {
  const [book, setBook] = useState(initialBook)
  const [isDeleting, setIsDeleting] = useState(false)

  // Poll for status if processing
  useEffect(() => {
    if (book.status !== 'processing' && book.status !== 'pending') {
      return
    }

    const pollInterval = setInterval(async () => {
      try {
        const updated = await getBookStatus(book.id)
        setBook(updated)
        if (updated.status === 'completed' || updated.status === 'failed') {
          clearInterval(pollInterval)
        }
      } catch {
        // Silently fail polling
      }
    }, 3000) // Poll every 3 seconds

    return () => clearInterval(pollInterval)
  }, [book.id, book.status])

  const handleDelete = async () => {
    if (!confirm('¿Seguro que quieres eliminar este libro? Esta acción no se puede deshacer.')) return
    
    setIsDeleting(true)
    try {
      await deleteLearnedBook(book.id)
      onDeleted?.(book.id)
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Error al eliminar')
    } finally {
      setIsDeleting(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const statusConfig: Record<string, { icon: string; text: string; color: string }> = {
    pending: { icon: '⏳', text: 'Pendiente', color: 'text-yellow-600 bg-yellow-50' },
    processing: { icon: '⚙️', text: 'Procesando...', color: 'text-blue-600 bg-blue-50' },
    completed: { icon: '✅', text: 'Completado', color: 'text-green-600 bg-green-50' },
    failed: { icon: '❌', text: 'Error', color: 'text-red-600 bg-red-50' }
  }

  // Fallback para status desconocido
  const statusInfo = statusConfig[book.status] || { icon: '❓', text: book.status || 'Desconocido', color: 'text-gray-600 bg-gray-50' }

  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 truncate">{book.title}</h3>
          {book.author && (
            <p className="text-sm text-gray-500 truncate">por {book.author}</p>
          )}
        </div>
        <span className={`px-2 py-1 rounded text-xs font-medium ${statusInfo.color}`}>
          {statusInfo.icon} {statusInfo.text}
        </span>
      </div>

      {/* Processing progress */}
      {book.status === 'processing' && (
        <div className="mb-3">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-blue-500 rounded-full transition-all" 
              style={{ width: book.total_chunks ? `${Math.round((book.processed_chunks / book.total_chunks) * 100)}%` : '30%' }} 
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            {book.total_chunks ? `Procesando ${book.processed_chunks}/${book.total_chunks} chunks...` : 'Extrayendo conceptos...'}
          </p>
        </div>
      )}

      {/* Error message */}
      {book.status === 'failed' && book.error_message && (
        <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
          {book.error_message}
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 gap-2 mb-3 text-center">
        <div className="bg-gray-50 rounded p-2">
          <div className="text-lg font-bold text-gray-700">{book.total_chunks ?? '-'}</div>
          <div className="text-xs text-gray-500">Chunks</div>
        </div>
        <div className="bg-gray-50 rounded p-2">
          <div className="text-lg font-bold text-gray-700">{book.processed_chunks ?? 0}</div>
          <div className="text-xs text-gray-500">Procesados</div>
        </div>
      </div>

      {/* Summary preview */}
      {book.status === 'completed' && book.global_summary && (
        <div className="mb-3 p-3 bg-blue-50 rounded-lg">
          <p className="text-xs font-medium text-blue-700 mb-1">Resumen:</p>
          <p className="text-sm text-gray-700 line-clamp-3">{book.global_summary}</p>
        </div>
      )}

      {/* Meta */}
      <div className="text-xs text-gray-400 mb-3">
        {book.file_type && <><span>{book.file_type.toUpperCase()}</span><span className="mx-2">•</span></>}
        <span>Subido: {formatDate(book.created_at)}</span>
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        {book.status === 'completed' && (
          <button
            onClick={() => onViewConcepts?.(book)}
            className="flex-1 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm"
          >
            Ver detalles
          </button>
        )}
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className={`px-3 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition text-sm disabled:opacity-50 ${book.status === 'completed' ? '' : 'flex-1'}`}
        >
          {isDeleting ? '...' : 'Eliminar'}
        </button>
      </div>
    </div>
  )
}
