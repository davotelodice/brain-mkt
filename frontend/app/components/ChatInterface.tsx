'use client'

import { useState, useEffect, useCallback } from 'react'
import { MessageList } from './MessageList'
import { DocumentUpload } from './DocumentUpload'
import { AnalysisPanel } from './AnalysisPanel'
import { ModelSelector } from './ModelSelector'
import type { Message } from '@/lib/types'
import { streamMessage, getMessages, createChat } from '@/lib/api-chat'

interface ChatInterfaceProps {
  chatId?: string  // Optional - can be undefined for new chat
  onChatCreated?: (newChatId: string) => void  // Callback when chat is created
}

/**
 * ChatInterface component - Main chat UI with SSE streaming.
 * 
 * ✅ GOTCHA 4: Client Component ('use client')
 * ✅ react-ui-patterns: Loading states, error handling, optimistic updates
 * ✅ context-window-management: Auto-scroll, message accumulation
 * ✅ TAREA 6.3: Chat se crea SOLO al enviar primer mensaje
 */
export function ChatInterface({ chatId, onChatCreated }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)  // Start false - no loading for welcome state
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [showTrace, setShowTrace] = useState(false)
  const [traceRuns, setTraceRuns] = useState<Array<{ startedAt: string; userMessage: string; events: unknown[] }>>([])
  const [selectedTraceRunIndex, setSelectedTraceRunIndex] = useState<number | null>(null)
  const [activeChatId, setActiveChatId] = useState<string | undefined>(chatId)
  const [selectedModel, setSelectedModel] = useState('gpt-4o-mini')
  const [selectedProvider, setSelectedProvider] = useState<'openai' | 'openrouter'>('openai')

  // Sync activeChatId with prop
  useEffect(() => {
    setActiveChatId(chatId)
  }, [chatId])

  // Load existing messages when chatId changes
  useEffect(() => {
    async function loadMessages() {
      if (!activeChatId) {
        setMessages([])
        setIsLoading(false)
        return
      }
      
      try {
        setIsLoading(true)
        const loadedMessages = await getMessages(activeChatId)
        setMessages(loadedMessages)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load messages')
      } finally {
        setIsLoading(false)
      }
    }

    loadMessages()
  }, [activeChatId])

  // Handle message send with streaming
  const handleSend = useCallback(async () => {
    if (!input.trim() || isStreaming) return

    const userMessage = input.trim()
    setInput('')
    setError(null)
    
    // ✅ TAREA 6.3: Create chat on first message if none exists
    let currentChatId = activeChatId
    if (!currentChatId) {
      try {
        // Extract first words for title (max 50 chars)
        const title = userMessage.length > 50 
          ? userMessage.substring(0, 47) + '...' 
          : userMessage
        
        const newChat = await createChat({ title })
        currentChatId = newChat.id
        setActiveChatId(currentChatId)
        
        // Notify parent component
        if (onChatCreated) {
          onChatCreated(currentChatId)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to create chat')
        return
      }
    }
    
    // Create new trace run for this message
    const newRun = {
      startedAt: new Date().toISOString(),
      userMessage,
      events: [] as unknown[]
    }
    setTraceRuns((prev) => {
      const updated = [...prev, newRun]
      setSelectedTraceRunIndex(updated.length - 1) // Select the new run
      return updated
    })

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

      // Stream response - use currentChatId (may be newly created)
      for await (const chunk of streamMessage(currentChatId, userMessage, selectedModel)) {
        if (chunk.type === 'done') {
          break
        }

        if (chunk.type === 'error') {
          setError(typeof chunk.content === 'string' ? chunk.content : 'Error desconocido')
          break
        }

        if (chunk.type === 'debug') {
          // Push debug event to the active (last) run
          setTraceRuns((prev) => {
            if (prev.length === 0) return prev
            const updated = [...prev]
            const lastIndex = updated.length - 1
            updated[lastIndex] = {
              ...updated[lastIndex],
              events: [...updated[lastIndex].events, chunk.content]
            }
            return updated
          })
          continue
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
      const updatedMessages = await getMessages(currentChatId)
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
  }, [input, isStreaming, activeChatId, onChatCreated, selectedModel])

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Loading state (only when loading existing chat)
  if (isLoading && activeChatId) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4" />
          <p className="text-gray-500">Cargando mensajes...</p>
        </div>
      </div>
    )
  }

  // Error state (only show if we have a chat and failed to load)
  if (error && messages.length === 0 && activeChatId) {
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

  // ✅ TAREA 6.3: Welcome state - no chat yet
  const isWelcomeState = !activeChatId && messages.length === 0

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2">
        <div className="text-sm font-semibold text-gray-900">
          {isWelcomeState ? 'Nueva Conversación' : 'Chat'}
        </div>
        {activeChatId && (
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setShowTrace((v) => !v)}
              className="rounded-lg border border-gray-200 bg-white px-3 py-1 text-xs text-gray-700 hover:bg-gray-50"
            >
              {showTrace ? 'Ocultar trace' : 'Ver trace'}
            </button>
            <button
              type="button"
              onClick={() => setShowAnalysis((v) => !v)}
              className="rounded-lg border border-gray-200 bg-white px-3 py-1 text-xs text-gray-700 hover:bg-gray-50"
            >
              {showAnalysis ? 'Ocultar análisis' : 'Ver análisis'}
            </button>
          </div>
        )}
      </div>

      {showTrace && activeChatId ? (
        <div className="border-b border-gray-200 px-4 py-3 bg-gray-50">
          <div className="text-xs font-semibold text-gray-700 mb-2">Trace (SSE debug)</div>
          {traceRuns.length === 0 ? (
            <div className="text-xs text-gray-500">Sin ejecuciones aún (activa `SSE_DEBUG=1` en backend).</div>
          ) : (
            <div className="space-y-3">
              {/* Runs list */}
              <div className="flex gap-2 flex-wrap">
                {traceRuns.map((run, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedTraceRunIndex(index)}
                    className={`px-2 py-1 text-xs rounded border transition ${
                      selectedTraceRunIndex === index
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                    }`}
                    title={run.userMessage}
                  >
                    #{index + 1} {new Date(run.startedAt).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  </button>
                ))}
              </div>
              
              {/* Selected run details */}
              {selectedTraceRunIndex !== null && traceRuns[selectedTraceRunIndex] && (
                <div className="space-y-2">
                  <div className="text-xs text-gray-600">
                    <strong>Mensaje:</strong> {traceRuns[selectedTraceRunIndex].userMessage}
                  </div>
                  <div className="text-xs text-gray-600">
                    <strong>Inicio:</strong> {new Date(traceRuns[selectedTraceRunIndex].startedAt).toLocaleString('es-ES')}
                  </div>
                  <div className="text-xs text-gray-600">
                    <strong>Eventos:</strong> {traceRuns[selectedTraceRunIndex].events.length}
                  </div>
                  {traceRuns[selectedTraceRunIndex].events.length === 0 ? (
                    <div className="text-xs text-gray-500 italic">Sin eventos de debug aún.</div>
                  ) : (
                    <pre className="text-[11px] leading-snug whitespace-pre-wrap break-words bg-white border border-gray-200 rounded p-3 max-h-96 overflow-auto">
                      {JSON.stringify(traceRuns[selectedTraceRunIndex].events, null, 2)}
                    </pre>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      ) : null}

      {showAnalysis && activeChatId ? (
        <div className="border-b border-gray-200 px-4 py-3 bg-gray-50">
          <AnalysisPanel chatId={activeChatId} />
        </div>
      ) : null}

      {/* Messages area or Welcome state */}
      {isWelcomeState ? (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center max-w-lg">
            <div className="text-6xl mb-6">🧠</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-3">
              Marketing Second Brain
            </h2>
            <p className="text-gray-600 mb-6">
              Tu asistente inteligente de marketing. Escribe tu mensaje para comenzar una nueva conversación.
            </p>
            <div className="grid grid-cols-2 gap-3 text-sm text-gray-500">
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="text-lg">📝</span>
                <p className="mt-1">Genera contenido viral</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="text-lg">👤</span>
                <p className="mt-1">Crea buyer personas</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="text-lg">🎯</span>
                <p className="mt-1">Estrategias de marketing</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="text-lg">📚</span>
                <p className="mt-1">Aprende de libros</p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <MessageList messages={messages} isStreaming={isStreaming} />
      )}

      {/* Error banner (if error during streaming or chat creation) */}
      {error && (
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

      {/* Document upload - only show when chat exists */}
      {activeChatId && (
        <div className="px-4 py-2 border-t border-gray-200 bg-gray-50">
          <DocumentUpload chatId={activeChatId} />
        </div>
      )}

      {/* Input area */}
      <div className="px-4 py-4 border-t border-gray-200 bg-white">
        {/* Provider toggle + Model selector */}
        <div className="flex items-center gap-4 pb-3 max-w-4xl mx-auto">
          {/* Provider toggle */}
          <div className="flex rounded-lg border border-gray-300 overflow-hidden text-xs">
            <button
              type="button"
              onClick={() => {
                setSelectedProvider('openai')
                setSelectedModel('gpt-4o-mini')
              }}
              className={`px-3 py-1.5 transition ${
                selectedProvider === 'openai'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              OpenAI
            </button>
            <button
              type="button"
              onClick={() => {
                setSelectedProvider('openrouter')
                setSelectedModel('anthropic/claude-sonnet-4')
              }}
              className={`px-3 py-1.5 transition ${
                selectedProvider === 'openrouter'
                  ? 'bg-purple-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              OpenRouter
            </button>
          </div>
          
          <ModelSelector
            value={selectedModel}
            onChange={setSelectedModel}
            provider={selectedProvider}
          />
          <span className="text-xs text-gray-400">
            {selectedModel}
          </span>
        </div>
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
