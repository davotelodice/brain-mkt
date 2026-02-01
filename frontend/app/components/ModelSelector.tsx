// frontend/app/components/ModelSelector.tsx
'use client';

import { useState } from 'react';

/**
 * Modelos disponibles según LLM_PROVIDER del backend.
 *
 * IMPORTANTE: Esta lista está hardcodeada porque usamos las API keys
 * del .env del servidor, no keys del usuario.
 *
 * TODO: En futuro se podría hacer un endpoint que retorne los modelos
 * disponibles según el LLM_PROVIDER configurado.
 */

// Modelos para OpenAI (cuando LLM_PROVIDER=openai en .env)
const OPENAI_MODELS = [
  // === MODELOS DE RAZONAMIENTO (o-series) ===
  {
    id: 'o3',
    name: 'o3 🧠',
    description: 'Razonamiento más avanzado',
    costTier: 'high' as const,
  },
  {
    id: 'o3-mini',
    name: 'o3 Mini 🧠',
    description: 'Razonamiento rápido y económico',
    costTier: 'medium' as const,
  },
  {
    id: 'o1',
    name: 'o1 🧠',
    description: 'Razonamiento profundo',
    costTier: 'high' as const,
  },
  {
    id: 'o1-mini',
    name: 'o1 Mini 🧠',
    description: 'Razonamiento compacto',
    costTier: 'medium' as const,
  },
  {
    id: 'o1-pro',
    name: 'o1 Pro 🧠',
    description: 'Razonamiento profesional',
    costTier: 'high' as const,
  },
  // === GPT-4.5 / GPT-5 ===
  {
    id: 'gpt-4.5-preview',
    name: 'GPT-4.5 Preview',
    description: 'Preview del próximo modelo',
    costTier: 'high' as const,
  },
  // === GPT-4o SERIES ===
  {
    id: 'gpt-4o',
    name: 'GPT-4o',
    description: 'Multimodal, muy capaz',
    costTier: 'medium' as const,
  },
  {
    id: 'gpt-4o-mini',
    name: 'GPT-4o Mini',
    description: 'Rápido y económico',
    costTier: 'low' as const,
  },
  // === LEGACY ===
  {
    id: 'gpt-4-turbo',
    name: 'GPT-4 Turbo',
    description: 'Legacy, 128k context',
    costTier: 'medium' as const,
  },
];

// Modelos para OpenRouter (cuando LLM_PROVIDER=openrouter en .env)
const OPENROUTER_MODELS = [
  // === CLAUDE 4.5 (Más recientes) ===
  {
    id: 'anthropic/claude-sonnet-4.5',
    name: 'Claude Sonnet 4.5',
    description: 'Mejor para agentes y código',
    costTier: 'high' as const,
  },
  {
    id: 'anthropic/claude-opus-4.5',
    name: 'Claude Opus 4.5',
    description: 'Razonamiento frontier',
    costTier: 'high' as const,
  },
  // === CLAUDE 4 ===
  {
    id: 'anthropic/claude-sonnet-4',
    name: 'Claude Sonnet 4',
    description: 'Balance calidad/costo',
    costTier: 'medium' as const,
  },
  // === CLAUDE 3.5 ===
  {
    id: 'anthropic/claude-3.5-sonnet',
    name: 'Claude 3.5 Sonnet',
    description: 'Versión estable anterior',
    costTier: 'medium' as const,
  },
  // === CLAUDE 3 ===
  {
    id: 'anthropic/claude-3-opus',
    name: 'Claude 3 Opus',
    description: 'El más potente de Claude 3',
    costTier: 'high' as const,
  },
  {
    id: 'anthropic/claude-3-haiku',
    name: 'Claude 3 Haiku',
    description: 'Ultra rápido y barato',
    costTier: 'low' as const,
  },
  // === DEEPSEEK (via OpenRouter) ===
  {
    id: 'deepseek/deepseek-chat',
    name: 'DeepSeek V3',
    description: 'Chat económico y potente',
    costTier: 'low' as const,
  },
];

type CostTier = 'low' | 'medium' | 'high';

interface Model {
  id: string;
  name: string;
  description: string;
  costTier: CostTier;
}

interface ModelSelectorProps {
  /** Modelo actualmente seleccionado */
  value: string;
  /** Callback cuando cambia el modelo */
  onChange: (modelId: string) => void;
  /** Provider del backend: 'openai' | 'openrouter' (default: openai) */
  provider?: 'openai' | 'openrouter';
}

/**
 * Selector de modelo LLM para el chat.
 *
 * Muestra los modelos disponibles según el provider configurado
 * y permite al usuario seleccionar uno diferente al default.
 *
 * @example
 * <ModelSelector
 *   value={selectedModel}
 *   onChange={setSelectedModel}
 *   provider="openai"
 * />
 */
export function ModelSelector({
  value,
  onChange,
  provider = 'openai',
}: ModelSelectorProps) {
  const [open, setOpen] = useState(false);

  // Seleccionar lista de modelos según provider
  const models: Model[] =
    provider === 'openrouter' ? OPENROUTER_MODELS : OPENAI_MODELS;

  const selectedModel = models.find((m) => m.id === value);

  // Colores según costo
  const costColors: Record<CostTier, string> = {
    low: 'text-green-600',
    medium: 'text-yellow-600',
    high: 'text-orange-600',
  };

  const costIcons: Record<CostTier, string> = {
    low: '💰',
    medium: '💰💰',
    high: '💰💰💰',
  };

  return (
    <div className="relative">
      {/* Botón del selector */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <span className="text-lg">🤖</span>
        <span className="font-medium">
          {selectedModel?.name || 'Seleccionar modelo'}
        </span>
        <span className="text-gray-400 text-xs">{open ? '▲' : '▼'}</span>
      </button>

      {/* Dropdown de modelos */}
      {open && (
        <>
          {/* Overlay para cerrar al hacer click fuera */}
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />

          {/* Lista de modelos - se despliega hacia ARRIBA */}
          <div className="absolute bottom-full left-0 mb-1 w-72 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-80 overflow-y-auto">
            <div className="p-2 border-b border-gray-100 sticky top-0 bg-white">
              <span className="text-xs text-gray-500">
                Provider: {provider === 'openrouter' ? 'OpenRouter' : 'OpenAI'}
              </span>
            </div>

            {models.map((model) => (
              <button
                key={model.id}
                type="button"
                onClick={() => {
                  onChange(model.id);
                  setOpen(false);
                }}
                className={`w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors ${
                  value === model.id
                    ? 'bg-blue-50 border-l-2 border-blue-500'
                    : ''
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-900">{model.name}</span>
                  <span className={`text-xs ${costColors[model.costTier]}`}>
                    {costIcons[model.costTier]}
                  </span>
                </div>
                <div className="text-xs text-gray-500 mt-0.5">
                  {model.description}
                </div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
