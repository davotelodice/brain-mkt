# Estilo de Código y Convenciones

## Filosofía General

- **Cuantas menos líneas de código, mejor**: Priorizar código minimalista y conciso
- **Proceder como desarrollador senior**: Soluciones de alta calidad con buenas prácticas
- **No detenerse hasta terminar**: Ejecutar tareas completamente sin pausas innecesarias
- **Clean Code**: Código directo, sin sobre-ingeniería, sin comentarios innecesarios

## Python (Backend)

### Convenciones Generales

- **PEP 8**: Seguir guía de estilo oficial de Python
- **Type Hints**: SIEMPRE usar anotaciones de tipos
- **Async/Await**: Usar async para operaciones I/O (DB, API, LLM)
- **Pydantic v2**: Validación robusta en todos los endpoints
- **Nombres**: snake_case para funciones y variables, PascalCase para clases

```python
# ✅ BIEN
async def get_user_chats(
    user_id: UUID,
    project_id: UUID,
    db: AsyncSession
) -> list[Chat]:
    """Obtiene todos los chats de un usuario en un proyecto específico."""
    result = await db.execute(
        select(Chat)
        .where(Chat.user_id == user_id)
        .where(Chat.project_id == project_id)
        .order_by(Chat.created_at.desc())
    )
    return result.scalars().all()

# ❌ MAL
def getUserChats(userId, projectId):  # Sin tipos, sin async, camelCase
    return db.query(Chat).filter_by(user_id=userId).all()  # Sin project_id
```

### Patrones Específicos

**1. Validación con Pydantic:**

```python
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    project_id: UUID
```

**2. Dependency Injection en FastAPI:**

```python
from fastapi import Depends
from typing import Annotated

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    # Validar JWT y retornar usuario
    pass

@app.post("/api/chats")
async def create_chat(
    data: ChatCreate,
    user: Annotated[User, Depends(get_current_user)]
):
    # user ya validado y disponible
    pass
```

**3. Estructura de Agentes (LangChain):**

```python
from langchain.agents import AgentExecutor
from langchain.tools import tool

class BuyerPersonaAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
    
    @tool
    def generate_analysis(self, initial_questions: dict) -> dict:
        """Genera análisis completo de buyer persona.
        
        Args:
            initial_questions: Respuestas del usuario a 4-5 preguntas
        
        Returns:
            Dict con full_analysis (35+ campos)
        """
        # Implementación
        pass
```

### Prohibiciones

- ❌ **NO hardcodear datos**: Usar env vars o DB
- ❌ **NO usar sync en contexto async**: Todo debe ser async
- ❌ **NO ignorar project_id**: SIEMPRE filtrar por project_id
- ❌ **NO usar catch-all exceptions**: Ser específico con excepciones

## TypeScript (Frontend)

### Convenciones Generales

- **TypeScript estricto**: `strict: true` en tsconfig.json
- **React Hooks**: Preferir hooks sobre class components
- **Nombres**: camelCase para variables/funciones, PascalCase para componentes
- **Server Components**: Usar por defecto, solo 'use client' cuando necesario

```typescript
// ✅ BIEN
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: Date;
}

const ChatMessage: React.FC<{ message: ChatMessage }> = ({ message }) => {
  return (
    <div className="flex gap-2">
      <span className="font-semibold">{message.role}:</span>
      <p>{message.content}</p>
    </div>
  );
};

// ❌ MAL
const chat_message = (msg: any) => {  // any prohibido, snake_case incorrecto
  return <div>{msg.content}</div>;  // Sin tipos, sin estructura
};
```

### Patrones Específicos

**1. Server Components (Next.js 14):**

```typescript
// app/dashboard/page.tsx (Server Component por defecto)
import { getChats } from '@/lib/api';

export default async function DashboardPage() {
  const chats = await getChats();  // Fetch en servidor
  
  return (
    <div>
      <ChatList chats={chats} />
    </div>
  );
}
```

**2. Client Components:**

```typescript
'use client';  // Solo cuando necesario

import { useState } from 'react';

export function ChatInput() {
  const [message, setMessage] = useState('');
  
  return (
    <input 
      value={message} 
      onChange={(e) => setMessage(e.target.value)}
    />
  );
}
```

**3. Estado Global (Zustand):**

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(persist(
  (set) => ({
    user: null,
    token: null,
    login: async (email, password) => {
      // Implementación
    },
    logout: () => set({ user: null, token: null }),
  }),
  { name: 'auth-storage' }
));
```

### Prohibiciones

- ❌ **NO usar any**: Siempre tipar correctamente
- ❌ **NO 'use client' innecesario**: Solo cuando realmente necesario
- ❌ **NO hardcodear URLs**: Usar env vars (NEXT_PUBLIC_API_URL)

## SQL (Supabase)

### Convenciones

- **Prefijo**: Todas las tablas con `marketing_`
- **UUIDs**: Usar UUID para IDs (uuid_generate_v4())
- **Timestamps**: SIEMPRE incluir created_at, updated_at
- **Índices**: En columnas filtradas frecuentemente
- **RLS**: Row Level Security habilitado

```sql
-- ✅ BIEN
CREATE TABLE marketing_chats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES marketing_users(id),
  project_id UUID NOT NULL REFERENCES marketing_projects(id),
  title VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chats_user_project ON marketing_chats(user_id, project_id);

-- ❌ MAL
CREATE TABLE chats (  -- Sin prefijo marketing_
  id SERIAL PRIMARY KEY,  -- SERIAL en vez de UUID
  user_id INT,  -- Sin REFERENCES
  title TEXT  -- Sin timestamps, sin project_id
);
```

## Comentarios y Documentación

- **No borrar comentarios existentes**: Preservar documentación valiosa
- **Docstrings**: En funciones públicas y métodos complejos
- **Comentarios breves**: Solo cuando el código no es auto-explicativo
- **TODOs**: Marcar claramente con TODO: y descripción

```python
# ✅ BIEN
def process_document(file_path: str, content_type: str) -> list[dict]:
    """Procesa un documento y retorna chunks con embeddings.
    
    Args:
        file_path: Ruta al archivo (.txt, .pdf, .docx)
        content_type: Tipo de contenido ('user_document', 'video_transcript')
    
    Returns:
        Lista de chunks con metadata y embeddings
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato no es soportado
    """
    # GOTCHA: PDFs escaneados necesitan OCR, no solo text extraction
    # TODO: Implementar OCR con pytesseract para PDFs escaneados
    pass

# ❌ MAL
def process(f):  # Sin docstring, nombre vago, sin tipos
    # procesa archivo
    pass
```

## Git Commits

- **Conventional Commits**: Usar formato estándar
- **Mensajes descriptivos**: Explicar el "por qué", no solo el "qué"

```bash
# ✅ BIEN
git commit -m "feat(agents): add document processor agent for .pdf files

Implements processing of user-uploaded PDFs using PyPDF2.
Extracts text, chunks it, and generates embeddings for semantic search.

Closes #42"

# ❌ MAL
git commit -m "update"
git commit -m "fix stuff"
```

## Seguridad

- **API Keys**: NUNCA en código, siempre en .env
- **Passwords**: SIEMPRE hashear con bcrypt (cost 12)
- **JWT**: Secrets fuertes, expiración apropiada (7 días)
- **Input**: Validar TODO input con Pydantic
- **project_id**: SIEMPRE filtrar en queries sensibles

```python
# ✅ BIEN
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ❌ MAL
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 es inseguro
```