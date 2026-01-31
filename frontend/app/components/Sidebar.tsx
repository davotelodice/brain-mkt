'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { LogoutButton } from './LogoutButton'
import type { ChatSummary } from '@/lib/types'
import { listChats, updateChatTitle, deleteChat } from '@/lib/api-chat'

interface SidebarProps {
  currentChatId?: string
  onChatSelect: (chatId: string) => void
}

/**
 * Sidebar component - List of chats with create new chat.
 * 
 * ✅ react-ui-patterns: Loading states, error handling, empty states
 * ✅ frontend-design: Clean sidebar with hover states
 * ✅ TAREA 6.3: NO crea chat automáticamente - solo navega a estado de bienvenida
 */
export function Sidebar({ currentChatId, onChatSelect }: SidebarProps) {
  const [chats, setChats] = useState<ChatSummary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  // Load chats on mount
  useEffect(() => {
    loadChats()
  }, [])

  const loadChats = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const loadedChats = await listChats()
      setChats(loadedChats)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load chats')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRenameChat = async (chatId: string, currentTitle: string) => {
    const newTitle = window.prompt('Nuevo nombre para la conversación:', currentTitle)
    if (!newTitle || newTitle.trim() === '' || newTitle === currentTitle) return

    try {
      const updated = await updateChatTitle(chatId, newTitle.trim())
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === chatId ? { ...chat, title: updated.title, updated_at: updated.updated_at } : chat
        )
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to rename chat')
    }
  }

  const handleDeleteChat = async (chatId: string) => {
    const confirm = window.confirm('¿Seguro que quieres eliminar esta conversación? Esta acción no se puede deshacer.')
    if (!confirm) return

    try {
      await deleteChat(chatId)
      setChats((prev) => prev.filter((chat) => chat.id !== chatId))

      // If deleted current chat, go to welcome state
      if (currentChatId === chatId) {
        onChatSelect('')
        router.push('/')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete chat')
    }
  }

  // ✅ TAREA 6.3: No crear chat - solo navegar a estado de bienvenida
  const handleNewConversation = () => {
    // Clear current chat selection and navigate to home
    onChatSelect('')
    router.push('/')
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) {
      return 'Hoy'
    } else if (diffDays === 1) {
      return 'Ayer'
    } else if (diffDays < 7) {
      return `Hace ${diffDays} días`
    } else {
      return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
    }
  }

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold mb-2">🧠 Marketing Brain</h1>
        <button
          onClick={handleNewConversation}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition flex items-center justify-center gap-2"
        >
          <span>+</span>
          <span>Nueva Conversación</span>
        </button>
      </div>

      {/* Chats list */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="p-4 text-center">
            <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-white mb-2" />
            <p className="text-sm text-gray-400">Cargando chats...</p>
          </div>
        ) : error ? (
          <div className="p-4 text-center">
            <div className="text-red-400 mb-2">⚠️</div>
            <p className="text-sm text-red-400 mb-2">{error}</p>
            <button
              onClick={loadChats}
              className="text-xs text-blue-400 hover:text-blue-300"
            >
              Reintentar
            </button>
          </div>
        ) : chats.length === 0 ? (
          <div className="p-4 text-center">
            <div className="text-4xl mb-2">💬</div>
            <p className="text-sm text-gray-400 mb-2">No hay conversaciones</p>
            <p className="text-xs text-gray-500">
              Escribe un mensaje para comenzar
            </p>
          </div>
        ) : (
          <div className="p-2">
            {chats.map((chat) => {
              const isActive = currentChatId === chat.id
              return (
                <div
                  key={chat.id}
                  className={`w-full rounded-lg mb-1 transition ${
                    isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <button
                    onClick={() => {
                      onChatSelect(chat.id)
                      router.push(`/?chat=${chat.id}`)
                    }}
                    className="w-full text-left p-3"
                  >
                    <div className="font-medium truncate mb-1">{chat.title}</div>
                    <div className="text-xs opacity-70 flex items-center justify-between">
                      <span>{formatDate(chat.updated_at)}</span>
                      {chat.message_count !== undefined && (
                        <span className="bg-gray-700 px-2 py-0.5 rounded">
                          {chat.message_count}
                        </span>
                      )}
                    </div>
                  </button>
                  <div className="flex justify-end gap-1 px-3 pb-2 text-[11px] opacity-80">
                    <button
                      type="button"
                      onClick={() => handleRenameChat(chat.id, chat.title)}
                      className="px-1 py-0.5 rounded border border-gray-600 hover:bg-gray-700"
                    >
                      Renombrar
                    </button>
                    <button
                      type="button"
                      onClick={() => handleDeleteChat(chat.id)}
                      className="px-1 py-0.5 rounded border border-red-500 text-red-300 hover:bg-red-600 hover:text-white"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Knowledge Library Link - TAREA 6 */}
      <div className="p-4 border-t border-gray-800">
        <button
          onClick={() => router.push('/dashboard/knowledge')}
          className="w-full flex items-center gap-2 px-3 py-2 text-gray-300 hover:bg-gray-800 rounded-lg transition text-sm"
        >
          <span className="text-lg">📚</span>
          <span>Biblioteca de Conocimiento</span>
        </button>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800">
        <LogoutButton variant="sidebar" />
      </div>
    </div>
  )
}
