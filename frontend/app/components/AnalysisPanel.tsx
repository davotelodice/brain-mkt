'use client'

import { useEffect, useState } from 'react'
import { getChatAnalysis, type ChatAnalysis } from '@/lib/api-analysis'

export function AnalysisPanel({ chatId }: { chatId: string }) {
  const [data, setData] = useState<ChatAnalysis | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function run() {
      try {
        setLoading(true)
        setError(null)
        const res = await getChatAnalysis(chatId)
        if (!cancelled) setData(res)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load analysis')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    if (chatId) run()
    return () => {
      cancelled = true
    }
  }, [chatId])

  if (loading) return <div className="text-sm text-neutral-400">Cargando análisis…</div>
  if (error) return <div className="text-sm text-red-400">{error}</div>
  if (!data || !data.has_buyer_persona) {
    return <div className="text-sm text-neutral-400">Aún no hay buyer persona para este chat.</div>
  }

  return (
    <div className="space-y-2 rounded-xl border border-neutral-800 bg-neutral-950/40 p-3">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Análisis</div>
        <div className="text-xs text-neutral-400">
          Foro: {data.has_forum_simulation ? '✅' : '—'} · Dolor: {data.has_pain_points ? '✅' : '—'} · Journey:{' '}
          {data.has_customer_journey ? '✅' : '—'}
        </div>
      </div>

      <details className="rounded-lg border border-neutral-800 bg-neutral-950/60 p-2">
        <summary className="cursor-pointer text-sm text-neutral-200">Ver buyer persona (JSON)</summary>
        <pre className="mt-2 max-h-64 overflow-auto text-xs text-neutral-200">
          {JSON.stringify(data.buyer_persona?.full_analysis ?? {}, null, 2)}
        </pre>
      </details>

      {data.has_forum_simulation && (
        <details className="rounded-lg border border-neutral-800 bg-neutral-950/60 p-2">
          <summary className="cursor-pointer text-sm text-neutral-200">Ver foro (JSON)</summary>
          <pre className="mt-2 max-h-64 overflow-auto text-xs text-neutral-200">
            {JSON.stringify(data.buyer_persona?.forum_simulation ?? {}, null, 2)}
          </pre>
        </details>
      )}

      {data.has_pain_points && (
        <details className="rounded-lg border border-neutral-800 bg-neutral-950/60 p-2">
          <summary className="cursor-pointer text-sm text-neutral-200">Ver puntos de dolor (JSON)</summary>
          <pre className="mt-2 max-h-64 overflow-auto text-xs text-neutral-200">
            {JSON.stringify(data.buyer_persona?.pain_points ?? {}, null, 2)}
          </pre>
        </details>
      )}

      {data.has_customer_journey && (
        <details className="rounded-lg border border-neutral-800 bg-neutral-950/60 p-2">
          <summary className="cursor-pointer text-sm text-neutral-200">Ver customer journey (JSON)</summary>
          <pre className="mt-2 max-h-64 overflow-auto text-xs text-neutral-200">
            {JSON.stringify(data.buyer_persona?.customer_journey ?? {}, null, 2)}
          </pre>
        </details>
      )}
    </div>
  )
}

