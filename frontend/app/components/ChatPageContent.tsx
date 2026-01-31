'use client'

import { useState, useEffect, useCallback } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Sidebar } from './Sidebar'
import { ChatInterface } from './ChatInterface'

/**
 * ChatPageContent - Inner component that uses useSearchParams.
 * Must be wrapped in Suspense boundary.
 * 
 * ✅ TAREA 6.3: NO crea chat automáticamente
 * Chat se crea SOLO cuando el usuario envía el primer mensaje
 */
export function ChatPageContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [chatId, setChatId] = useState<string | null>(null)
  const [sidebarRefreshKey, setSidebarRefreshKey] = useState(0)

  // Read chatId from URL - NO automatic creation
  useEffect(() => {
    const chatIdFromUrl = searchParams.get('chat')
    setChatId(chatIdFromUrl)
  }, [searchParams])

  const handleChatSelect = (newChatId: string) => {
    setChatId(newChatId)
    router.replace(`/?chat=${newChatId}`)
  }

  // Called when a new chat is created from ChatInterface
  const handleChatCreated = useCallback((newChatId: string) => {
    setChatId(newChatId)
    router.replace(`/?chat=${newChatId}`)
    // Trigger sidebar refresh to show new chat
    setSidebarRefreshKey(prev => prev + 1)
  }, [router])

  // Main layout - always render immediately (no loading state for auto-creation)
  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      {/* Sidebar */}
      <Sidebar 
        key={sidebarRefreshKey}
        currentChatId={chatId || undefined} 
        onChatSelect={handleChatSelect} 
      />

      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        {/* ChatInterface handles both with and without chatId */}
        <ChatInterface 
          chatId={chatId || undefined} 
          onChatCreated={handleChatCreated}
        />
      </div>
    </div>
  )
}
