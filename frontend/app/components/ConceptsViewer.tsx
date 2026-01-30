'use client'

import type { LearnedBook } from '@/lib/types'

interface ConceptsViewerProps {
  book: LearnedBook
  onClose: () => void
}

/**
 * ConceptsViewer - Modal to display book concepts and summary.
 * TAREA 6: Simple modal showing book details.
 * 
 * ✅ react-patterns: Presentational component, props-driven
 * ✅ nextjs-best-practices: Client component for modal
 */
export function ConceptsViewer({ book, onClose }: ConceptsViewerProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{book.title}</h2>
            {book.author && (
              <p className="text-sm text-gray-500">por {book.author}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-blue-600">{book.total_chunks ?? '-'}</div>
              <div className="text-sm text-blue-700">Fragmentos totales</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-green-600">{book.processed_chunks ?? 0}</div>
              <div className="text-sm text-green-700">Chunks procesados</div>
            </div>
          </div>

          {/* Global Summary */}
          {book.global_summary && (
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">📝 Resumen Global</h3>
              <div className="bg-gray-50 rounded-lg p-4 text-gray-700 whitespace-pre-wrap">
                {book.global_summary}
              </div>
            </div>
          )}

          {/* Info */}
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">ℹ️ Información</h3>
            <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
              {book.file_type && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Tipo de archivo:</span>
                  <span className="font-medium">{book.file_type.toUpperCase()}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500">Estado:</span>
                <span className="font-medium text-green-600">
                  ✅ {book.status === 'completed' ? 'Procesado completamente' : book.status}
                </span>
              </div>
              {book.completed_at && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Completado:</span>
                  <span className="font-medium">
                    {new Date(book.completed_at).toLocaleString('es-ES')}
                  </span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500">Creado:</span>
                <span className="font-medium">
                  {new Date(book.created_at).toLocaleString('es-ES')}
                </span>
              </div>
            </div>
          </div>

          {/* Usage hint */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              <strong>💡 Tip:</strong> Los conceptos de este libro ahora están disponibles 
              automáticamente cuando generas contenido. El asistente usará este conocimiento 
              para crear contenido más específico y fundamentado.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  )
}
