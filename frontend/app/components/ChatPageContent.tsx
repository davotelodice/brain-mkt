'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Sidebar } from './Sidebar'
import { ChatInterface } from './ChatInterface'
import { createChat } from '@/lib/api-chat'

/**
 * ChatPageContent - Inner component that uses useSearchParams.
 * Must be wrapped in Suspense boundary.
 */
export function ChatPageContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [chatId, setChatId] = useState<string | null>(null)
  const [isInitializing, setIsInitializing] = useState(true)

  // Initialize chat from URL or create new one
  useEffect(() => {
    async function initializeChat() {
      const chatIdFromUrl = searchParams.get('chat')

      if (chatIdFromUrl) {
        setChatId(chatIdFromUrl)
        setIsInitializing(false)
      } else {
        // Create new chat if none exists
        try {
          const newChat = await createChat({ title: 'Nueva Conversación' })
          setChatId(newChat.id)
          router.replace(`/?chat=${newChat.id}`)
        } catch (err) {
          console.error('Failed to create chat:', err)
        } finally {
          setIsInitializing(false)
        }
      }
    }

    initializeChat()
  }, [searchParams, router])

  const handleChatSelect = (newChatId: string) => {
    setChatId(newChatId)
  }

  // Loading state
  if (isInitializing) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4" />
          <p className="text-gray-500">Inicializando...</p>
        </div>
      </div>
    )
  }

  // Main layout
  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      {/* Sidebar */}
      <Sidebar currentChatId={chatId || undefined} onChatSelect={handleChatSelect} />

      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        {chatId ? (
          <ChatInterface chatId={chatId} />
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-gray-500">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Selecciona una conversación
              </h3>
              <p className="text-sm">
                O crea una nueva desde el sidebar
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
