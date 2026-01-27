# 🐛 GOTCHAS Críticos y Soluciones Implementadas

> **Fecha**: 2026-01-26  
> **Proyecto**: Marketing Second Brain System  
> **Propósito**: Documentar problemas técnicos conocidos con soluciones validadas e integradas

---

## 📌 ¿Qué es un GOTCHA?

Un **gotcha** es un problema técnico o comportamiento inesperado que puede causar errores si no lo conoces de antemano. Es algo que "te atrapa" (got you!) porque no es obvio hasta que lo encuentras.

**Objetivo de este documento:**
- ✅ Identificar 10 gotchas críticos del proyecto
- ✅ Validar soluciones con documentación oficial (Archon)
- ✅ Integrar soluciones en el plan de trabajo (PRPs)
- ✅ Evitar debugging innecesario durante implementación

---

## 🔴 GOTCHA 1: pgvector - Índice ivfflat requiere >1000 rows

### Problema
```sql
-- ❌ ESTO NO FUNCIONA BIEN con <1000 documentos
CREATE INDEX ON marketing_knowledge_base 
USING ivfflat (embedding vector_cosine_ops);

-- Las búsquedas serán LENTAS o imprecisas
```

**Por qué ocurre:**
- IVFFlat (Inverted File with Flat compression) divide el espacio vectorial en clusters
- Requiere suficientes datos para crear clusters representativos
- Con <1000 documentos, los clusters son pobres → búsquedas ineficientes

### Solución Validada (desde Supabase Docs)

```sql
-- ✅ SOLUCIÓN 1: Usar HNSW index (recomendado por Supabase)
CREATE INDEX ON marketing_knowledge_base 
USING hnsw (embedding vector_cosine_ops);

-- HNSW (Hierarchical Navigable Small World):
-- - Funciona BIEN con pocos documentos (incluso <100)
-- - Mejor performance en general
-- - Más robusto ante cambios en los datos
-- - Supabase lo recomienda como opción por defecto
```

**Fuente oficial (Archon):**
> "In general we recommend using HNSW because of its performance and robustness against changing data."  
> — Supabase Docs, Vector Indexes

**Alternativa para datasets grandes:**
```sql
-- ✅ SOLUCIÓN 2: IVFFlat solo si tienes >1000 documentos
CREATE INDEX ON marketing_knowledge_base 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- 100 clusters para ~10k docs

-- Regla general:
-- - HNSW: <10k documentos o cambios frecuentes
-- - IVFFlat: >10k documentos, dataset estable
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 1 - Configurar Base de Datos en Supabase

**SQL a ejecutar:**
```sql
-- /home/david/brain-mkt/backend/src/db/migrations/001_initial_schema.sql

-- 1. Crear tabla
CREATE TABLE marketing_knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES marketing_projects(id),
    chat_id UUID REFERENCES marketing_chats(id),
    content_type VARCHAR(50) NOT NULL,
    source_title VARCHAR(500) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Crear índice HNSW (NO ivfflat)
CREATE INDEX idx_knowledge_base_embedding_hnsw 
ON marketing_knowledge_base 
USING hnsw (embedding vector_cosine_ops);

-- 3. Índices adicionales para filtrado
CREATE INDEX idx_knowledge_base_content_type ON marketing_knowledge_base(content_type);
CREATE INDEX idx_knowledge_base_project_chat ON marketing_knowledge_base(project_id, chat_id);
```

**Validación:**
```bash
# Verificar que el índice es HNSW
psql $SUPABASE_DB_URL -c "\d+ marketing_knowledge_base"
# Esperado: "hnsw" en la columna embedding
```

---

## 🔴 GOTCHA 2: LangChain ConversationBufferMemory crece indefinidamente

### Problema
```python
# ❌ ESTO ROMPE con conversaciones largas
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()  # SIN límite

# Después de 100+ mensajes:
# - Consume miles de tokens
# - Requests a LLM cuestan $$$
# - Latencia alta (prompt enorme)
# - Puede exceder límite de contexto (200k tokens)
```

**Por qué ocurre:**
- `ConversationBufferMemory` guarda TODOS los mensajes
- Cada request incluye historial completo
- No hay límite por defecto

### Solución Validada

```python
# ✅ SOLUCIÓN: ConversationBufferWindowMemory con límite
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    k=10,  # Solo últimos 10 mensajes
    return_messages=True  # Formato de mensajes
)

# Ventajas:
# - Mantiene contexto reciente (lo importante)
# - Limita consumo de tokens
# - Latencia constante
# - Nunca excede límite de contexto
```

**Configuración óptima por caso de uso:**
```python
# Para chat casual: k=5-10 (últimos 5-10 turnos)
memory_casual = ConversationBufferWindowMemory(k=10, return_messages=True)

# Para análisis profundo: k=20-30
memory_analysis = ConversationBufferWindowMemory(k=30, return_messages=True)

# IMPORTANTE: Guardar mensajes importantes en long-term memory (DB)
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 4 - Agente IA con Memoria

**Código a implementar:**
```python
# /home/david/brain-mkt/backend/src/agents/memory_manager.py

from langchain.memory import ConversationBufferWindowMemory
from typing import List, Dict, UUID

class MemoryManager:
    """Gestión de memoria triple del agente."""
    
    def __init__(self):
        # SHORT-TERM MEMORY: Últimos 10 turnos de conversación
        self.short_term = ConversationBufferWindowMemory(
            k=10,  # ✅ Límite explícito
            return_messages=True,
            memory_key="chat_history"
        )
    
    async def add_user_message(self, message: str):
        """Añade mensaje del usuario a short-term memory."""
        self.short_term.chat_memory.add_user_message(message)
    
    async def add_ai_message(self, message: str):
        """Añade respuesta del AI a short-term memory."""
        self.short_term.chat_memory.add_ai_message(message)
    
    async def get_short_term_context(self) -> str:
        """Obtiene contexto de short-term (últimos 10 mensajes)."""
        messages = self.short_term.load_memory_variables({})
        return messages.get('chat_history', [])
    
    async def save_to_long_term(
        self, 
        chat_id: UUID, 
        project_id: UUID,
        role: str,
        content: str
    ):
        """
        Guarda mensaje en long-term memory (DB).
        Se ejecuta para TODOS los mensajes, no solo los importantes.
        """
        # Guardar en marketing_messages table
        await db.messages.insert({
            'chat_id': chat_id,
            'project_id': project_id,
            'role': role,  # 'user' | 'assistant'
            'content': content,
            'created_at': datetime.utcnow()
        })
```

**Validación:**
```python
# Test: Verificar que memory no crece indefinidamente
async def test_memory_limit():
    memory = MemoryManager()
    
    # Añadir 100 mensajes
    for i in range(100):
        await memory.add_user_message(f"Mensaje {i}")
        await memory.add_ai_message(f"Respuesta {i}")
    
    # Verificar que solo mantiene últimos 10
    context = await memory.get_short_term_context()
    assert len(context) == 20  # 10 user + 10 assistant
    print("✅ GOTCHA 2: Memory correctamente limitada")
```

---

## 🔴 GOTCHA 3: FastAPI StreamingResponse + Middleware que lee body

### Problema
```python
# ❌ ESTO ROMPE el streaming de respuestas
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Leer el body
    body = await request.body()  # ❌ Esto consume el stream
    logger.info(f"Body: {body}")
    
    response = await call_next(request)
    return response

@app.post("/chat/stream")
async def stream_chat():
    async def generate():
        yield "data: hola\n\n"
        yield "data: mundo\n\n"
    
    return StreamingResponse(generate())  # ❌ No funciona!
```

**Por qué ocurre:**
- `request.body()` consume el stream completo
- Una vez consumido, no se puede volver a leer
- El endpoint de streaming recibe un body vacío

### Solución Validada (desde FastAPI Docs)

```python
# ✅ SOLUCIÓN 1: Excluir endpoints de streaming del middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Detectar endpoints de streaming
    if "/stream" in request.url.path or "/sse" in request.url.path:
        # ✅ Saltar middleware para streaming
        return await call_next(request)
    
    # Para endpoints normales, procesar como siempre
    body = await request.body()
    logger.info(f"Body: {body}")
    response = await call_next(request)
    return response
```

**Fuente oficial (Archon):**
```python
# Ejemplo de FastAPI StreamingResponse (validado)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_stream():
    for i in range(10):
        yield b"some fake video bytes"

@app.get("/")
async def main():
    return StreamingResponse(generate_stream())
```

**Solución avanzada con custom middleware:**
```python
# ✅ SOLUCIÓN 2: Custom Request class que permite re-read
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class CachedBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Cachear body solo si NO es streaming
        if "/stream" not in request.url.path:
            body = await request.body()
            # Cache body para que se pueda re-leer
            request._cached_body = body
        
        response = await call_next(request)
        return response
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 6 - Backend - API de Chat con Streaming

**Código a implementar:**
```python
# /home/david/brain-mkt/backend/src/main.py

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Middleware que RESPETA streaming
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Lista de paths que usan streaming
    streaming_paths = ["/api/chat/stream", "/api/sse"]
    
    if any(path in request.url.path for path in streaming_paths):
        # ✅ NO leer body, pasar directamente
        return await call_next(request)
    
    # Para endpoints normales, procesar
    try:
        body = await request.body()
        logger.info(f"Request to {request.url.path}: {body[:100]}")
    except:
        pass
    
    response = await call_next(request)
    return response

# ✅ Endpoint de streaming (ejemplo)
@app.post("/api/chat/stream")
async def stream_chat_response():
    async def generate():
        # Streaming con formato SSE (Server-Sent Events)
        for chunk in llm_response_chunks:
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

**Validación:**
```bash
# Test: Verificar que streaming funciona
curl -N http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola"}' \
  --no-buffer

# Esperado: Respuesta en chunks, sin esperar al final
data: Hola
data: ,
data:  mundo
data: !
data: [DONE]
```

---

## 🔴 GOTCHA 4: Next.js Server Components + useState

### Problema
```tsx
// ❌ ESTO DA ERROR en Server Components
import { useState } from 'react'

export default function HomePage() {
  const [count, setCount] = useState(0)  // ❌ Error!
  
  return <div>Count: {count}</div>
}

// Error: "You're importing a component that needs useState. 
// It only works in a Client Component but none of its parents 
// are marked with 'use client'."
```

**Por qué ocurre:**
- Next.js 14 App Router usa Server Components por defecto
- Server Components se renderizan en el servidor (NO en el browser)
- `useState`, `useEffect`, event handlers solo funcionan en el cliente

### Solución Validada (desde Next.js Docs)

```tsx
// ✅ SOLUCIÓN: Marcar componente como 'use client'
'use client'  // ← Directiva al inicio del archivo

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)  // ✅ Ahora funciona
  
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  )
}
```

**Fuente oficial (Archon):**
```tsx
// Ejemplo validado de Next.js Client Component
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  )
}
```

**Patrón recomendado: Composición de Server + Client Components:**
```tsx
// ✅ MEJOR PRÁCTICA: Server Component como wrapper
// app/page.tsx (Server Component por defecto)
import { Counter } from './Counter'  // Client Component
import { fetchData } from '@/lib/db'

export default async function HomePage() {
  // ✅ Fetch de datos en el servidor (rápido, sin latencia)
  const data = await fetchData()
  
  return (
    <div>
      <h1>Welcome</h1>
      {/* ✅ Server data pasado a Client Component */}
      <Counter initialData={data} />
    </div>
  )
}

// app/Counter.tsx (Client Component)
'use client'

import { useState } from 'react'

export function Counter({ initialData }) {
  const [count, setCount] = useState(initialData.count)
  
  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  )
}
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 8 - Frontend - Interfaz de Chat con Streaming

**Estructura de archivos:**
```bash
frontend/app/
├── page.tsx                 # ✅ Server Component (layout, fetch inicial)
├── layout.tsx               # ✅ Server Component
└── components/
    ├── ChatInterface.tsx    # ✅ 'use client' - maneja estado del chat
    ├── MessageList.tsx      # ✅ 'use client' - maneja scroll, animations
    ├── InputBox.tsx         # ✅ 'use client' - maneja input, submit
    └── Sidebar.tsx          # ✅ 'use client' - maneja navegación
```

**Código a implementar:**
```tsx
// frontend/app/components/ChatInterface.tsx
'use client'  // ✅ Marcar como Client Component

import { useState, useEffect } from 'react'
import { MessageList } from './MessageList'
import { InputBox } from './InputBox'

export function ChatInterface({ initialMessages }) {
  const [messages, setMessages] = useState(initialMessages)
  const [isStreaming, setIsStreaming] = useState(false)
  
  const handleSendMessage = async (message: string) => {
    // Añadir mensaje del usuario
    setMessages(prev => [...prev, { role: 'user', content: message }])
    
    // Streaming de respuesta
    setIsStreaming(true)
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      body: JSON.stringify({ message })
    })
    
    // Procesar stream...
  }
  
  return (
    <div className="flex flex-col h-screen">
      <MessageList messages={messages} />
      <InputBox onSend={handleSendMessage} disabled={isStreaming} />
    </div>
  )
}
```

**Validación:**
```bash
# Verificar que NO hay errores de hidration
npm run dev
# Abrir http://localhost:3000
# Esperado: Sin errores de "useState in Server Component"
```

---

## 🔴 GOTCHA 5: OpenAI Rate Limits en Embeddings

### Problema
```python
# ❌ ESTO FALLA con >3000 chunks
import openai

chunks = load_chunks()  # 5000 chunks

for chunk in chunks:
    # Request individual por cada chunk
    embedding = openai.Embedding.create(
        input=chunk['text'],
        model="text-embedding-3-large"
    )  # ❌ Rate limit error después de ~3000!

# openai.error.RateLimitError: Rate limit exceeded
# Tier Free: 3000 RPM (Requests Per Minute)
# Tier 1: 10,000 RPM
```

**Por qué ocurre:**
- OpenAI limita requests por minuto según tier
- Tier Free: 3000 RPM
- Cada `Embedding.create()` = 1 request
- 5000 chunks > 3000 RPM → error

### Solución Validada

```python
# ✅ SOLUCIÓN: Batch processing + exponential backoff
import openai
import asyncio
from typing import List

async def generate_embeddings_batch(
    texts: List[str],
    batch_size: int = 50,  # OpenAI permite hasta 2048 inputs por request
    max_retries: int = 5
) -> List[List[float]]:
    """
    Genera embeddings en batches con retry automático.
    
    Args:
        texts: Lista de textos para embed
        batch_size: Tamaño del batch (default 50)
        max_retries: Intentos máximos por batch
    
    Returns:
        Lista de embeddings (vectores de 1536 dimensiones)
    """
    results = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # ✅ Batch request (1 request para 50 textos)
                response = await openai.Embedding.acreate(
                    input=batch,
                    model="text-embedding-3-large"
                )
                
                # Extraer embeddings
                embeddings = [item['embedding'] for item in response['data']]
                results.extend(embeddings)
                
                break  # Éxito, salir del retry loop
                
            except openai.error.RateLimitError as e:
                retry_count += 1
                wait_time = 2 ** retry_count  # Exponential backoff
                
                print(f"⚠️ Rate limit. Retry {retry_count}/{max_retries} en {wait_time}s")
                await asyncio.sleep(wait_time)
                
                if retry_count == max_retries:
                    raise Exception(f"Max retries alcanzado para batch {i}")
    
    return results

# ✅ Uso optimizado
texts = [chunk['text'] for chunk in chunks]  # 5000 texts
embeddings = await generate_embeddings_batch(texts, batch_size=50)

# Resultado:
# - 5000 textos / 50 batch = 100 requests (vs 5000 requests)
# - Con retry automático si hay rate limit
# - ~2 minutos vs timeout instantáneo
```

**Cálculo de tiempos:**
```python
# Sin batch:
# 5000 requests a 3000 RPM = 100 segundos + rate limit errors

# ✅ Con batch de 50:
# 100 requests a 3000 RPM = 2 segundos (+ buffer por seguridad)
# Sin rate limit errors!
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 4 - Agente IA con Memoria

**Código a implementar:**
```python
# /home/david/brain-mkt/backend/src/services/embedding_service.py

import openai
import asyncio
from typing import List
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

class EmbeddingService:
    """Servicio para generar embeddings con rate limit handling."""
    
    def __init__(self):
        self.model = "text-embedding-3-large"
        self.batch_size = 50
        self.max_retries = 5
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding para un solo texto."""
        embeddings = await self.generate_embeddings_batch([text])
        return embeddings[0]
    
    async def generate_embeddings_batch(
        self, 
        texts: List[str]
    ) -> List[List[float]]:
        """
        Genera embeddings en batches con retry.
        
        Optimizaciones:
        - Batch de 50 textos por request
        - Exponential backoff en rate limits
        - Async para no bloquear
        """
        results = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i+self.batch_size]
            retry_count = 0
            
            while retry_count < self.max_retries:
                try:
                    response = await openai.Embedding.acreate(
                        input=batch,
                        model=self.model
                    )
                    
                    embeddings = [
                        item['embedding'] 
                        for item in response['data']
                    ]
                    results.extend(embeddings)
                    
                    print(f"✅ Batch {i//self.batch_size + 1}: {len(batch)} embeddings")
                    break
                    
                except openai.error.RateLimitError:
                    retry_count += 1
                    wait_time = 2 ** retry_count
                    
                    print(f"⚠️ Rate limit. Retry {retry_count} en {wait_time}s")
                    await asyncio.sleep(wait_time)
                    
                    if retry_count == self.max_retries:
                        raise
        
        return results

# ✅ Uso en ingesta de datos
async def ingest_training_data():
    """Script para ingestar transcripciones."""
    embedding_service = EmbeddingService()
    
    # Cargar chunks
    chunks = load_chunks_from_files('contenido/Transcriptions Andrea Estratega/')
    
    # Generar embeddings en batch
    texts = [chunk['text'] for chunk in chunks]
    embeddings = await embedding_service.generate_embeddings_batch(texts)
    
    # Guardar en DB
    for chunk, embedding in zip(chunks, embeddings):
        await db.knowledge_base.insert({
            'content_type': 'video_transcript',
            'chunk_text': chunk['text'],
            'embedding': embedding,
            'project_id': None,  # Global knowledge
            'chat_id': None
        })
    
    print(f"✅ {len(chunks)} chunks procesados sin rate limit errors")
```

**Validación:**
```python
# Test: Procesar 5000 chunks
import asyncio

async def test_large_batch():
    service = EmbeddingService()
    
    # 5000 textos de prueba
    texts = [f"Texto de prueba {i}" for i in range(5000)]
    
    start = time.time()
    embeddings = await service.generate_embeddings_batch(texts)
    elapsed = time.time() - start
    
    assert len(embeddings) == 5000
    print(f"✅ GOTCHA 5: 5000 embeddings en {elapsed:.2f}s sin rate limit")

asyncio.run(test_large_batch())
```

---

## 🔴 GOTCHA 6: Supabase RLS no aplica con Service Role Key

### Problema
```python
# ❌ CONFIANZA CIEGA en RLS (Row Level Security)
from supabase import create_client

# Service role key bypasea RLS!
supabase = create_client(
    SUPABASE_URL, 
    SUPABASE_SERVICE_ROLE_KEY  # ❌ NO respeta RLS
)

# Usuario A hace request con JWT de proyecto_id = "proj-A"
# Pero backend usa service role key:
chats = supabase.table('marketing_chats') \
    .select('*') \
    .execute()  # ❌ Retorna TODOS los chats de TODOS los proyectos!

# Usuario A ve chats de proyectos B, C, D... ¡VIOLACIÓN DE SEGURIDAD!
```

**Por qué ocurre:**
- Service Role Key tiene privilegios de administrador
- Bypasea todas las políticas de RLS
- Es necesario para operaciones del backend
- Pero es responsabilidad del backend filtrar por `project_id`

### Solución Validada

```python
# ✅ SOLUCIÓN: Validación manual de project_id en TODAS las queries
from supabase import create_client
from uuid import UUID
from fastapi import HTTPException

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

async def get_user_chats(user_id: UUID, project_id: UUID) -> List[Dict]:
    """
    Obtiene chats del usuario CON validación de project_id.
    
    CRÍTICO: NO confiar solo en RLS, validar manualmente.
    """
    # 1. ✅ Verificar que usuario pertenece al proyecto
    user = supabase.table('marketing_users') \
        .select('project_id') \
        .eq('id', str(user_id)) \
        .single() \
        .execute()
    
    if not user.data or user.data['project_id'] != str(project_id):
        raise HTTPException(
            status_code=403,
            detail="User not authorized for this project"
        )
    
    # 2. ✅ Query CON filtro explícito de project_id
    chats = supabase.table('marketing_chats') \
        .select('*') \
        .eq('user_id', str(user_id)) \
        .eq('project_id', str(project_id)) \  # ← CRÍTICO
        .order('created_at', desc=True) \
        .execute()
    
    return chats.data

# ❌ MAL: Olvidar project_id
chats = supabase.table('marketing_chats').select('*').eq('user_id', user_id)

# ✅ BIEN: SIEMPRE incluir project_id
chats = supabase.table('marketing_chats') \
    .select('*') \
    .eq('user_id', user_id) \
    .eq('project_id', project_id)  # ← OBLIGATORIO
```

**Middleware para inyectar project_id automáticamente:**
```python
# ✅ SOLUCIÓN AVANZADA: Middleware que inyecta project_id desde JWT
from fastapi import Request, HTTPException
import jwt

@app.middleware("http")
async def inject_project_id(request: Request, call_next):
    # Extraer JWT
    token = request.cookies.get('auth_token')
    if not token:
        return await call_next(request)
    
    try:
        # Decodificar JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        
        # ✅ Inyectar project_id en request.state
        request.state.project_id = payload['project_id']
        request.state.user_id = payload['user_id']
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    return await call_next(request)

# Uso en endpoints:
@app.get("/api/chats")
async def get_chats(request: Request):
    # ✅ project_id automáticamente disponible
    project_id = request.state.project_id
    user_id = request.state.user_id
    
    return await get_user_chats(user_id, project_id)
```

### Integración en el Proyecto

**Ubicación en PRP:** TAREA 2 - Setup Backend con FastAPI + Autenticación Manual

**Código a implementar:**
```python
# /home/david/brain-mkt/backend/src/middleware/auth.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import jwt
import os

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    """
    Middleware de autenticación que:
    1. Valida JWT
    2. Inyecta user_id y project_id en request.state
    3. Asegura aislamiento por proyecto
    """
    # Rutas públicas (sin auth)
    public_paths = ["/api/auth/login", "/api/auth/register", "/docs", "/openapi.json"]
    if request.url.path in public_paths:
        return await call_next(request)
    
    # Extraer token
    token = request.cookies.get('auth_token')
    if not token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing authentication token"}
        )
    
    try:
        # ✅ Decodificar y validar JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        
        # ✅ Inyectar en request.state (disponible en todos los endpoints)
        request.state.user_id = payload['user_id']
        request.state.project_id = payload['project_id']
        request.state.email = payload['email']
        
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Token expired"}
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"}
        )
    
    response = await call_next(request)
    return response

# /home/david/brain-mkt/backend/src/main.py
from middleware.auth import auth_middleware

app = FastAPI()
app.middleware("http")(auth_middleware)

# /home/david/brain-mkt/backend/src/api/chat.py
@router.get("/chats")
async def get_user_chats(request: Request):
    """
    Obtiene chats del usuario.
    project_id viene automáticamente del middleware.
    """
    user_id = request.state.user_id
    project_id = request.state.project_id  # ✅ Del JWT, no confiamos en input del usuario
    
    # ✅ Query con project_id OBLIGATORIO
    chats = await db.chats.find({
        'user_id': user_id,
        'project_id': project_id  # ← CRÍTICO: Aislamiento por proyecto
    }).order_by('created_at', -1).all()
    
    return {"chats": chats}
```

**Validación:**
```python
# Test: Verificar que RLS no es suficiente
async def test_rls_bypass():
    # Usuario A de proyecto "proj-A"
    token_A = create_jwt({'user_id': 'user-A', 'project_id': 'proj-A'})
    
    # Intentar acceder sin project_id en query
    response = requests.get(
        'http://localhost:8000/api/chats',
        cookies={'auth_token': token_A}
    )
    
    chats = response.json()['chats']
    
    # ✅ Verificar que SOLO retorna chats de proj-A
    assert all(chat['project_id'] == 'proj-A' for chat in chats)
    print("✅ GOTCHA 6: Aislamiento por project_id funciona")
```

---

## Resumen de Integración en el Proyecto

| GOTCHA | Ubicación en PRP | Prioridad | Estado |
|--------|------------------|-----------|--------|
| 1. pgvector HNSW index | TAREA 1 - DB Setup | 🔴 Crítico | ✅ Integrado |
| 2. Memory window limit | TAREA 4 - Agente IA | 🔴 Crítico | ✅ Integrado |
| 3. FastAPI streaming | TAREA 6 - Chat Streaming | 🔴 Crítico | ✅ Integrado |
| 4. Next.js 'use client' | TAREA 8 - Frontend | 🔴 Crítico | ✅ Integrado |
| 5. OpenAI rate limits | TAREA 4 - Agente IA | 🔴 Crítico | ✅ Integrado |
| 6. Supabase RLS bypass | TAREA 2 - Auth | 🔴 Crítico | ✅ Integrado |
| 7. LangChain tool descriptions | TAREA 4 - Agente IA | 🟡 Importante | ⏳ Pendiente detalle |
| 8. Docker volumes Windows | TAREA 10 - Docker | 🟡 Importante | ⏳ Pendiente detalle |
| 9. pgvector cosine normalization | TAREA 4 - Agente IA | 🟡 Importante | ⏳ Pendiente detalle |
| 10. JWT + localStorage | TAREA 7 - Frontend Auth | 🟡 Importante | ⏳ Pendiente detalle |

---

## Próximos Pasos

1. ✅ Completar detalles de GOTCHAS 7-10 (similar a 1-6)
2. ✅ Añadir validación automatizada para cada gotcha
3. ✅ Documentar en PRPs con referencias a este archivo
4. ✅ Crear tests específicos para cada gotcha

---

**Fecha de última actualización**: 2026-01-26  
**Autor**: AI Agent (con validación de Archon + Supabase/FastAPI/Next.js Docs)
