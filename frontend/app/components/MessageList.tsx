'use client'

import { useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { Message } from '@/lib/types'

interface MessageListProps {
  messages: Message[]
  isStreaming?: boolean
}

/**
 * MessageList component - Displays chat messages with auto-scroll.
 * 
 * ✅ react-ui-patterns: Empty state, loading states
 * ✅ context-window-management: Scroll to bottom for new messages
 */
export function MessageList({ messages, isStreaming = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isStreaming])

  // Empty state
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        {isStreaming ? (
          <div className="text-center text-gray-500">
            <div className="flex justify-center mb-4">
              <div className="w-10 h-10 border-4 border-blue-300 border-t-blue-600 rounded-full animate-spin" />
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Generando la primera respuesta...
            </h3>
            <p className="text-sm">
              Esto puede tardar unos segundos mientras preparo el contexto inicial.
            </p>
          </div>
        ) : (
          <div className="text-center text-gray-500">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              No hay mensajes aún
            </h3>
            <p className="text-sm">
              Comienza una conversación escribiendo un mensaje
            </p>
          </div>
        )}
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto space-y-4 p-4 bg-gradient-to-b from-gray-50 to-white"
    >
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm ${
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-900 border border-gray-200'
            }`}
          >
            {/* Role indicator */}
            <div className="text-xs font-semibold mb-1 opacity-70">
              {message.role === 'user' ? 'Tú' : '🧠 Asistente'}
            </div>

            {/* Message content - TAREA 6.2: Markdown para asistente */}
            <div className="break-words">
              {message.role === 'assistant' ? (
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    // Estilos para Markdown
                    h1: ({ children }) => <h1 className="text-xl font-bold mt-4 mb-2">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-bold mt-3 mb-2">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-base font-semibold mt-2 mb-1">{children}</h3>,
                    p: ({ children }) => <p className="mb-2">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc list-inside mb-2 ml-2">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal list-inside mb-2 ml-2">{children}</ol>,
                    li: ({ children }) => <li className="mb-1">{children}</li>,
                    strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                    em: ({ children }) => <em className="italic">{children}</em>,
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-gray-300 pl-3 my-2 italic text-gray-600">
                        {children}
                      </blockquote>
                    ),
                    code: ({ children, className }) => {
                      const isInline = !className
                      return isInline ? (
                        <code className="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm">{children}</code>
                      ) : (
                        <code className="block bg-gray-100 text-gray-800 p-3 rounded my-2 text-sm overflow-x-auto">
                          {children}
                        </code>
                      )
                    },
                    hr: () => <hr className="my-4 border-gray-200" />,
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              ) : (
                <div className="whitespace-pre-wrap">{message.content}</div>
              )}
            </div>

            {/* Timestamp */}
            <div
              className={`text-xs mt-2 ${
                message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
              }`}
            >
              {new Date(message.created_at).toLocaleTimeString('es-ES', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </div>
          </div>
        </div>
      ))}

      {/* Streaming indicator */}
      {isStreaming && (
        <div className="flex justify-start">
          <div className="max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3 bg-white border border-gray-200 shadow-sm">
            <div className="flex items-center gap-2 text-gray-500">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <span className="text-sm">Escribiendo...</span>
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  )
}
