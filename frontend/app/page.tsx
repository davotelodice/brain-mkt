import { Suspense } from 'react'
import { ChatPageContent } from './components/ChatPageContent'

/**
 * HomePage - Main chat interface with sidebar.
 * 
 * ✅ nextjs-best-practices: Suspense boundary for useSearchParams
 */
export default function HomePage() {
  return (
    <Suspense
      fallback={
        <div className="h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4" />
            <p className="text-gray-500">Cargando...</p>
          </div>
        </div>
      }
    >
      <ChatPageContent />
    </Suspense>
  )
}
