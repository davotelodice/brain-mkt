'use client'

import { useState, useEffect, useCallback } from 'react'
import { MessageList } from './MessageList'
import { DocumentUpload } from './DocumentUpload'
import { AnalysisPanel } from './AnalysisPanel'
import type { Message } from '@/lib/types'
import { streamMessage, getMessages } from '@/lib/api-chat'

interface ChatInterfaceProps {
  chatId: string
}

/**
 * ChatInterface component - Main chat UI with SSE streaming.
 * 
 * ✅ GOTCHA 4: Client Component ('use client')
 * ✅ react-ui-patterns: Loading states, error handling, optimistic updates
 * ✅ context-window-management: Auto-scroll, message accumulation
 */
export function ChatInterface({ chatId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showAnalysis, setShowAnalysis] = useState(false)

  // Load existing messages on mount
  useEffect(() => {
    async function loadMessages() {
      try {
        setIsLoading(true)
        const loadedMessages = await getMessages(chatId)
        setMessages(loadedMessages)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load messages')
      } finally {
        setIsLoading(false)
      }
    }

    if (chatId) {
      loadMessages()
    }
  }, [chatId])

  // Handle message send with streaming
  const handleSend = useCallback(async () => {
    if (!input.trim() || isStreaming) return

    const userMessage = input.trim()
    setInput('')
    setError(null)

    // ✅ Optimistic update: Add user message immediately
    const tempUserMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString()
    }
    setMessages((prev) => [...prev, tempUserMessage])

    // Start streaming
    setIsStreaming(true)
    let assistantContent = ''
    const tempAssistantId = `temp-assistant-${Date.now()}`

    try {
      // Create temporary assistant message for streaming
      const tempAssistantMessage: Message = {
        id: tempAssistantId,
        role: 'assistant',
        content: '',
        created_at: new Date().toISOString()
      }
      setMessages((prev) => [...prev, tempAssistantMessage])

      // Stream response
      for await (const chunk of streamMessage(chatId, userMessage)) {
        if (chunk.type === 'done') {
          break
        }

        if (chunk.type === 'error') {
          setError(chunk.content)
          break
        }

        if (chunk.type === 'chunk' || chunk.type === 'status') {
          assistantContent += chunk.content

          // Update assistant message in real-time
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === tempAssistantId
                ? { ...msg, content: assistantContent }
                : msg
            )
          )
        }
      }

      // Reload messages from server to get final IDs
      const updatedMessages = await getMessages(chatId)
      setMessages(updatedMessages)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
      // Remove temporary messages on error
      setMessages((prev) =>
        prev.filter((msg) => msg.id !== tempUserMessage.id && msg.id !== tempAssistantId)
      )
    } finally {
      setIsStreaming(false)
    }
  }, [input, isStreaming, chatId])

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4" />
          <p className="text-gray-500">Cargando mensajes...</p>
        </div>
      </div>
    )
  }

  // Error state
  if (error && messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Error al cargar mensajes
          </h3>
          <p className="text-sm text-gray-500 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Reintentar
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2">
        <div className="text-sm font-semibold text-gray-900">Chat</div>
        <button
          type="button"
          onClick={() => setShowAnalysis((v) => !v)}
          className="rounded-lg border border-gray-200 bg-white px-3 py-1 text-xs text-gray-700 hover:bg-gray-50"
        >
          {showAnalysis ? 'Ocultar análisis' : 'Ver análisis'}
        </button>
      </div>

      {showAnalysis ? (
        <div className="border-b border-gray-200 px-4 py-3 bg-gray-50">
          <AnalysisPanel chatId={chatId} />
        </div>
      ) : null}

      {/* Messages area */}
      <MessageList messages={messages} isStreaming={isStreaming} />

      {/* Error banner (if error during streaming) */}
      {error && messages.length > 0 && (
        <div className="px-4 py-2 bg-red-50 border-t border-red-200">
          <div className="flex items-center gap-2 text-red-700 text-sm">
            <span>⚠️</span>
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-auto text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Document upload */}
      <div className="px-4 py-2 border-t border-gray-200 bg-gray-50">
        <DocumentUpload chatId={chatId} />
      </div>

      {/* Input area */}
      <div className="px-4 py-4 border-t border-gray-200 bg-white">
        <div className="flex gap-3 items-end max-w-4xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje... (Enter para enviar, Shift+Enter para nueva línea)"
            disabled={isStreaming}
            rows={1}
            className="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ minHeight: '48px', maxHeight: '120px' }}
          />
          <button
            onClick={handleSend}
            disabled={isStreaming || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isStreaming ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Enviando...</span>
              </>
            ) : (
              <>
                <span>Enviar</span>
                <span className="text-lg">➤</span>
              </>
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          El asistente puede generar buyer personas, contenido viral y estrategias de marketing
        </p>
      </div>
    </div>
  )
}
