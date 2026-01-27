'use client'

import { useState, useRef } from 'react'
import { uploadDocument } from '@/lib/api-chat'

interface DocumentUploadProps {
  chatId: string
}

/**
 * DocumentUpload component - Upload .txt, .pdf, .docx files.
 * 
 * ✅ react-ui-patterns: Loading states, error handling
 * ✅ frontend-design: Clean, minimal UI
 */
export function DocumentUpload({ chatId }: DocumentUploadProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const ALLOWED_TYPES = ['.txt', '.pdf', '.docx']
  const MAX_SIZE_MB = 10

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file type
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED_TYPES.includes(fileExt)) {
      setError(`Tipo de archivo no permitido. Permitidos: ${ALLOWED_TYPES.join(', ')}`)
      return
    }

    // Validate file size
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`Archivo muy grande. Máximo: ${MAX_SIZE_MB}MB`)
      return
    }

    // Upload file
    setIsUploading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await uploadDocument(chatId, file)
      setSuccess(`✅ Archivo "${result.filename}" subido correctamente`)
      
      // Clear input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al subir archivo')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="flex items-center gap-3">
      <input
        ref={fileInputRef}
        type="file"
        accept={ALLOWED_TYPES.join(',')}
        onChange={handleFileSelect}
        disabled={isUploading}
        className="hidden"
        id="document-upload"
      />
      <label
        htmlFor="document-upload"
        className={`flex items-center gap-2 px-3 py-2 text-sm rounded-lg border transition cursor-pointer ${
          isUploading
            ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed'
            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-blue-400'
        }`}
      >
        {isUploading ? (
          <>
            <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
            <span>Subiendo...</span>
          </>
        ) : (
          <>
            <span className="text-lg">📄</span>
            <span>Subir documento</span>
          </>
        )}
      </label>

      {/* Error message */}
      {error && (
        <div className="flex items-center gap-2 text-sm text-red-600">
          <span>⚠️</span>
          <span>{error}</span>
          <button
            onClick={() => setError(null)}
            className="ml-2 text-red-400 hover:text-red-600"
          >
            ✕
          </button>
        </div>
      )}

      {/* Success message */}
      {success && (
        <div className="flex items-center gap-2 text-sm text-green-600">
          <span>{success}</span>
        </div>
      )}

      {/* File type hint */}
      <span className="text-xs text-gray-500 ml-auto">
        {ALLOWED_TYPES.join(', ')} (max {MAX_SIZE_MB}MB)
      </span>
    </div>
  )
}
