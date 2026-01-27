# 📡 API de Streaming - SSE (Server-Sent Events)

## Descripción

La API de streaming permite recibir respuestas del asistente de IA en tiempo real, mostrando progreso mientras los agentes procesan la información.

## Endpoints

### 1. Streaming Endpoint

**POST** `/api/chats/{chat_id}/stream`

Envía mensaje y recibe respuesta por streaming usando SSE.

**Headers requeridos:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "content": "Tu mensaje aquí"
}
```

**Response:**
```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
X-Accel-Buffering: no

data: {"type": "status", "content": "Routing message..."}

data: {"type": "chunk", "content": "📊 Analizando buyer persona..."}

data: {"type": "chunk", "content": "✅ Análisis completado"}

data: {"type": "done", "content": ""}

data: [DONE]

```

### 2. Non-Streaming Endpoint

**POST** `/api/chats/{chat_id}/messages`

Envía mensaje y espera respuesta completa (sin streaming).

## Formato de Eventos SSE

Cada evento tiene el formato:

```typescript
{
  "type": "status" | "chunk" | "done" | "error",
  "content": string
}
```

### Tipos de Eventos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `status` | Estado inicial del router | `"No hay buyer persona. Creando..."` |
| `chunk` | Fragmento de respuesta | `"📊 Analizando perfil..."` |
| `done` | Fin del procesamiento | `""` (vacío) |
| `error` | Error durante streaming | `"Error: connection timeout"` |

La señal `[DONE]` marca el cierre final del stream.

## Ejemplo con JavaScript (Frontend)

```javascript
const eventSource = new EventSource(
  `http://localhost:8000/api/chats/${chatId}/stream`,
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

eventSource.onmessage = (event) => {
  if (event.data === '[DONE]') {
    eventSource.close();
    return;
  }

  try {
    const data = JSON.parse(event.data);
    
    switch (data.type) {
      case 'status':
        console.log('Status:', data.content);
        break;
      case 'chunk':
        appendToChat(data.content);
        break;
      case 'done':
        console.log('Stream completed');
        break;
      case 'error':
        console.error('Error:', data.content);
        eventSource.close();
        break;
    }
  } catch (e) {
    console.error('Parse error:', e);
  }
};

eventSource.onerror = (error) => {
  console.error('EventSource failed:', error);
  eventSource.close();
};
```

## Ejemplo con curl

```bash
# Test rápido con curl
curl -N -X POST "http://localhost:8000/api/chats/{chat_id}/stream" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "Analiza mi buyer persona"}'
```

**Nota**: La opción `-N` es crucial para deshabilitar buffering en curl.

## Testing Automatizado

Ejecutar script de prueba:

```bash
# Configurar variables (opcional)
export TEST_USER_EMAIL="test@example.com"
export TEST_USER_PASSWORD="testpass123"

# Ejecutar test
./backend/scripts/test_streaming_endpoint.sh
```

El script automáticamente:
1. Verifica que el servidor esté corriendo
2. Autentica al usuario
3. Crea un chat de prueba
4. Envía mensaje con streaming
5. Muestra eventos SSE en tiempo real

## ⚡ GOTCHA 3 - Middleware y Streaming

**Problema**: Middleware que lee `request.body()` consume el stream y rompe SSE.

**Solución**: En `main.py`, excluir endpoints de streaming:

```python
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    streaming_paths = ["/stream", "/sse"]
    
    if any(path in request.url.path for path in streaming_paths):
        # ✅ NO leer body, pasar directamente
        return await call_next(request)
    
    # Para endpoints normales, procesar con body logging
    # ...
```

## Flujo Interno

```
User Message
     ↓
Save to DB (user message)
     ↓
RouterAgent.process_stream()
     ├─> Route to agent
     ├─> Yield status
     ├─> Execute agent
     │   ├─> BUYER_PERSONA: Progress updates
     │   ├─> CONTENT_GENERATION: Stream chunks (future)
     │   └─> WAITING: Acknowledge
     ├─> Yield chunks
     └─> Yield done
          ↓
Save to DB (assistant message)
     ↓
Close stream
```

## Headers Importantes

```python
headers = {
    "Cache-Control": "no-cache",         # Prevent caching
    "Connection": "keep-alive",          # Keep connection open
    "X-Accel-Buffering": "no"           # Disable nginx buffering
}
```

## Próximas Mejoras (TAREA 7+)

- [ ] Content Generator Agent con streaming real de chunks
- [ ] Progress tracking más granular
- [ ] Cancelación de streams (AbortController)
- [ ] Retry automático en caso de desconexión
