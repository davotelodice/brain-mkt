// ✅ Server Component por defecto (no necesita 'use client')
// Solo para layout estático - la interactividad va en Client Components

import Link from 'next/link'
import { LogoutButton } from './components/LogoutButton'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            🧠 Marketing Second Brain
          </h1>

          <nav className="flex gap-4 items-center">
            <Link
              href="/chats"
              className="text-gray-600 hover:text-gray-900 font-medium transition"
            >
              Mis Chats
            </Link>
            <LogoutButton />
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Bienvenido a tu Asistente de Marketing IA
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Analiza tu audiencia, genera contenido viral y optimiza tu estrategia digital
            con el poder de la inteligencia artificial.
          </p>
        </div>

        {/* Feature cards */}
        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Buyer Persona
            </h3>
            <p className="text-gray-600">
              Análisis profundo de tu cliente ideal con 40+ preguntas estratégicas
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition">
            <div className="text-3xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Generación de Contenido
            </h3>
            <p className="text-gray-600">
              Crea posts, guiones y carruseles virales basados en tu audiencia
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition">
            <div className="text-3xl mb-4">🚀</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Estrategia de Contenido
            </h3>
            <p className="text-gray-600">
              Customer journey, pain points y estrategias de conversión
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-12">
          <Link
            href="/chats/new"
            className="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition"
          >
            ✨ Comenzar Nueva Conversación
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-20 py-8 text-center text-gray-500 text-sm">
        <p>Marketing Second Brain v0.1.0 - Powered by FastAPI + Next.js + OpenAI</p>
      </footer>
    </div>
  )
}
