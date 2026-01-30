'use client'

import { useState, useRef } from 'react'
import { uploadBook } from '@/lib/api-knowledge'
import type { LearnedBook } from '@/lib/types'

interface BookUploadProps {
  onBookUploaded?: (book: LearnedBook) => void
}

/**
 * BookUpload component - Drag & drop or click to upload books.
 * TAREA 6: Similar pattern to DocumentUpload.tsx
 * 
 * ✅ react-patterns: useState for state, composition
 * ✅ nextjs-best-practices: Client component for interactivity
 */
export function BookUpload({ onBookUploaded }: BookUploadProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isDragOver, setIsDragOver] = useState(false)
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const ALLOWED_TYPES = ['.pdf', '.txt', '.docx']
  const MAX_SIZE_MB = 50 // Books can be larger

  const validateFile = (file: File): string | null => {
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED_TYPES.includes(fileExt)) {
      return `Tipo de archivo no permitido. Permitidos: ${ALLOWED_TYPES.join(', ')}`
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      return `Archivo muy grande. Máximo: ${MAX_SIZE_MB}MB`
    }
    return null
  }

  const handleUpload = async (file: File) => {
    const validationError = validateFile(file)
    if (validationError) {
      setError(validationError)
      return
    }

    const bookTitle = title.trim() || file.name.replace(/\.[^/.]+$/, '')
    
    setIsUploading(true)
    setError(null)
    setSuccess(null)

    try {
      const book = await uploadBook(file, bookTitle, author.trim() || undefined)
      setSuccess(`📚 "${book.title}" subido. Procesando en segundo plano...`)
      onBookUploaded?.(book)
      
      // Clear form
      setTitle('')
      setAuthor('')
      if (fileInputRef.current) fileInputRef.current.value = ''
      
      setTimeout(() => setSuccess(null), 5000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al subir libro')
    } finally {
      setIsUploading(false)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleUpload(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleUpload(file)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = () => setIsDragOver(false)

  return (
    <div className="space-y-4">
      {/* Title & Author inputs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <input
          type="text"
          placeholder="Título del libro (opcional)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isUploading}
          className="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
        />
        <input
          type="text"
          placeholder="Autor (opcional)"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          disabled={isUploading}
          className="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
        />
      </div>

      {/* Drag & drop zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition
          ${isDragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'}
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={ALLOWED_TYPES.join(',')}
          onChange={handleFileSelect}
          disabled={isUploading}
          className="hidden"
        />
        
        {isUploading ? (
          <div className="flex flex-col items-center gap-2">
            <div className="w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-gray-600">Subiendo libro...</span>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <span className="text-4xl">📚</span>
            <span className="text-gray-700 font-medium">
              Arrastra un libro o haz clic para seleccionar
            </span>
            <span className="text-sm text-gray-500">
              {ALLOWED_TYPES.join(', ')} (max {MAX_SIZE_MB}MB)
            </span>
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <span>⚠️</span>
          <span className="flex-1">{error}</span>
          <button onClick={() => setError(null)} className="text-red-400 hover:text-red-600">✕</button>
        </div>
      )}

      {/* Success message */}
      {success && (
        <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700">
          <span>{success}</span>
        </div>
      )}
    </div>
  )
}
