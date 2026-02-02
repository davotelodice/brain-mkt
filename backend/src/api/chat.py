"""Chat API endpoints."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..agents.buyer_persona_agent import BuyerPersonaAgent
from ..agents.router_agent import AgentState, RouterAgent
from ..db.database import get_db
from ..db.models import MarketingUser
from ..middleware.auth import get_current_user
from ..schemas.chat import (
    ChatSummary,
    ChatWithMessages,
    CreateChatRequest,
    CreateChatResponse,
    Message,
    SendMessageRequest,
    UpdateChatTitleRequest,
)
from ..services.chat_service import ChatService
from ..services.embedding_service import EmbeddingService
from ..services.llm_service import LLMService
from ..services.memory_manager import MemoryManager
from ..services.rag_service import RAGService

router = APIRouter(prefix="/api/chats", tags=["chats"])


def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    """Dependency for chat service.

    Args:
        db: Database session

    Returns:
        ChatService instance
    """
    return ChatService(db)


def get_agent_system(db: AsyncSession = Depends(get_db)):
    """Dependency for complete agent system.

    Args:
        db: Database session

    Returns:
        Tuple of (router_agent, buyer_persona_agent, memory_manager)
    """
    # Initialize services
    llm_service = LLMService()
    embedding_service = EmbeddingService()
    rag_service = RAGService(db, embedding_service)
    memory_manager = MemoryManager(db, rag_service, llm_service)

    # Initialize agents
    router_agent = RouterAgent(llm_service, memory_manager)
    buyer_persona_agent = BuyerPersonaAgent(llm_service, memory_manager, db)

    return router_agent, buyer_persona_agent, memory_manager


@router.post("", response_model=CreateChatResponse)
async def create_chat(
    request: CreateChatRequest,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> CreateChatResponse:
    """Create new chat.

    Args:
        request: Chat creation request
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        Created chat
    """
    chat = await chat_service.create_chat(
        user_id=user.id,
        project_id=user.project_id,
        title=request.title or "New Chat"
    )

    return CreateChatResponse(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at
    )


@router.get("", response_model=list[ChatSummary])
async def list_chats(
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> list[ChatSummary]:
    """List all chats for current user.

    Args:
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        List of chat summaries
    """
    chats = await chat_service.list_chats(
        user_id=user.id,
        project_id=user.project_id
    )

    return [
        ChatSummary(
            id=chat.id,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        )
        for chat in chats
    ]


@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatWithMessages:
    """Get chat with messages.

    Args:
        chat_id: Chat ID
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        Chat with full message history
    """
    # Get chat (validates ownership)
    chat = await chat_service.get_chat(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id
    )

    # Get messages
    messages = await chat_service.get_messages(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id
    )

    return ChatWithMessages(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        messages=[
            Message(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                metadata=msg.metadata_,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )


@router.patch("/{chat_id}/title", response_model=ChatSummary)
async def update_chat_title(
    chat_id: UUID,
    request: UpdateChatTitleRequest,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatSummary:
    """Update chat title.

    Args:
        chat_id: Chat ID
        request: Update request
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        Updated chat
    """
    chat = await chat_service.update_chat_title(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id,
        new_title=request.title
    )

    return ChatSummary(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at
    )


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> None:
    """Delete chat (and all messages).

    Args:
        chat_id: Chat ID
        user: Current authenticated user
        chat_service: Chat service
    """
    await chat_service.delete_chat(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id
    )


@router.post("/{chat_id}/stream")
async def stream_message(
    chat_id: UUID,
    request: SendMessageRequest,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
    agent_system=Depends(get_agent_system)
):
    """
    Send message and stream response using SSE (Server-Sent Events).

    ⚠️ GOTCHA 3: Este endpoint debe ser EXCLUIDO del middleware de logging
    que lee request.body() para que el streaming funcione.

    Flow:
    1. Save user message
    2. Router Agent decides and streams execution
    3. Save final assistant response
    4. Stream chunks in real-time

    Args:
        chat_id: Chat ID
        request: Message request
        user: Current authenticated user
        chat_service: Chat service
        agent_system: Agent system (router, buyer_persona, memory)

    Returns:
        StreamingResponse with SSE format (data: {...}\n\n)
    """
    import json

    from fastapi.responses import StreamingResponse

    router_agent, buyer_persona_agent, memory_manager = agent_system

    # 1. Save user message
    await chat_service.create_message(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id,
        role="user",
        content=request.content
    )

    # 2. Ensure chat history loaded + add to short-term memory
    await memory_manager.ensure_chat_loaded(chat_id=chat_id, project_id=user.project_id, limit=20)
    await memory_manager.add_message_to_short_term(chat_id, "user", request.content)

    async def generate_sse():
        """
        Generate SSE (Server-Sent Events) stream.

        SSE Format:
        data: {"type": "status", "content": "..."}

        data: {"type": "chunk", "content": "..."}

        data: [DONE]

        """
        try:
            # Accumulate final content for database
            final_content_parts = []

            # Stream agent execution
            async for chunk_json in router_agent.process_stream(
                chat_id=chat_id,
                project_id=user.project_id,
                user_message=request.content,
                model=request.model,
                attachment_content=request.attachment_content,
            ):
                # Parse to accumulate final content
                try:
                    chunk_data = json.loads(chunk_json)
                    if chunk_data.get("type") == "chunk":
                        final_content_parts.append(chunk_data.get("content", ""))
                except json.JSONDecodeError:
                    pass

                # Send SSE chunk
                yield f"data: {chunk_json}\n\n"

            # Save final assistant message to database
            final_content = "".join(final_content_parts)
            if final_content.strip():
                await chat_service.create_message(
                    chat_id=chat_id,
                    user_id=user.id,
                    project_id=user.project_id,
                    role="assistant",
                    content=final_content
                )

                # Add to short-term memory
                await memory_manager.add_message_to_short_term(chat_id, "assistant", final_content)

            # Final done signal
            yield "data: [DONE]\n\n"

        except Exception as e:
            # Error in streaming
            error_msg = json.dumps({"type": "error", "content": str(e)})
            yield f"data: {error_msg}\n\n"

    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.post("/{chat_id}/messages", response_model=Message)
async def send_message(
    chat_id: UUID,
    request: SendMessageRequest,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
    agent_system=Depends(get_agent_system)
) -> Message:
    """Send message to chat and process with AI agents.

    Flow:
    1. Save user message
    2. Router Agent decides which agent to execute
    3. Execute corresponding agent (Buyer Persona, Content Generator, etc.)
    4. Save agent response
    5. Return agent message

    Args:
        chat_id: Chat ID
        request: Message request
        user: Current authenticated user
        chat_service: Chat service
        agent_system: Agent system (router, buyer_persona, memory)

    Returns:
        Created assistant message
    """
    router_agent, buyer_persona_agent, memory_manager = agent_system

    # 1. Create and save user message
    await chat_service.create_message(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id,
        role="user",
        content=request.content
    )

    # 2. Ensure chat history loaded + add to short-term memory
    await memory_manager.ensure_chat_loaded(chat_id=chat_id, project_id=user.project_id, limit=20)
    await memory_manager.add_message_to_short_term(chat_id, "user", request.content)

    # 3. Router Agent decides which agent to execute
    routing_result = await router_agent.execute(
        chat_id=chat_id,
        project_id=user.project_id,
        user_message=request.content
    )

    agent_state = routing_result["state"]

    # 4. Execute corresponding agent
    if agent_state == AgentState.BUYER_PERSONA:
        # Execute Buyer Persona Agent
        result = await buyer_persona_agent.execute(
            chat_id=chat_id,
            project_id=user.project_id,
            user_message=request.content
        )

        if result["success"]:
            assistant_content = (
                "✅ He generado tu buyer persona completo con 40+ preguntas respondidas.\n\n"
                "Puedes revisarlo y ahora puedes pedirme:\n"
                "- 'Dame ideas de contenido para redes sociales'\n"
                "- 'Genera posts para Instagram'\n"
                "- 'Crea un customer journey'\n"
                "- 'Dame puntos de dolor de mi audiencia'"
            )
        else:
            assistant_content = f"❌ Error al generar buyer persona: {result['message']}"

    elif agent_state == AgentState.WAITING:
        assistant_content = (
            "Estoy esperando tus instrucciones. Puedes pedirme:\n"
            "- 'Dame ideas de contenido'\n"
            "- 'Genera posts'\n"
            "- 'Analiza mi audiencia'\n"
            "- 'Crea un customer journey'"
        )

    elif agent_state == AgentState.CONTENT_GENERATION:
        # ✅ Content Generator Agent
        from ..agents.content_generator_agent import ContentGeneratorAgent
        from ..services.llm_service import LLMService

        llm_service = LLMService()
        content_agent = ContentGeneratorAgent(llm_service, memory_manager)
        result = await content_agent.execute(
            chat_id=chat_id,
            project_id=user.project_id,
            user_message=request.content
        )

        if result["success"]:
            ideas = result.get("content_ideas", [])
            if ideas:
                assistant_content = "✨ **Ideas de Contenido Generadas:**\n\n"
                for i, idea in enumerate(ideas[:10], 1):
                    if isinstance(idea, dict):
                        titulo = idea.get("titulo", f"Idea {i}")
                        plataforma = idea.get("plataforma", "TikTok/Instagram")
                        hook = idea.get("hook", "")
                        estructura = idea.get("estructura", "")
                        cta = idea.get("cta", "")

                        assistant_content += f"**{i}. {titulo}** ({plataforma})\n"
                        if hook:
                            assistant_content += f"🎣 Hook: {hook}\n"
                        if estructura:
                            assistant_content += f"📋 Estructura: {estructura}\n"
                        if cta:
                            assistant_content += f"📢 CTA: {cta}\n"
                        assistant_content += "\n"
                    else:
                        assistant_content += f"**{i}.** {str(idea)}\n\n"
                assistant_content += "\n💡 Ideas personalizadas para tu buyer persona."
            else:
                assistant_content = result.get("message", "✅ Contenido generado.")
        else:
            assistant_content = f"❌ {result.get('message', 'Error al generar contenido')}"

    else:
        assistant_content = f"Estado: {routing_result['reason']}"

    # 5. Create and save assistant message
    assistant_message = await chat_service.create_message(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id,
        role="assistant",
        content=assistant_content
    )

    # 6. Add to short-term memory
    await memory_manager.add_message_to_short_term(chat_id, "assistant", assistant_content)

    return Message(
        id=assistant_message.id,
        role=assistant_message.role,
        content=assistant_message.content,
        metadata=assistant_message.metadata_,
        created_at=assistant_message.created_at
    )


@router.get("/{chat_id}/messages", response_model=list[Message])
async def get_messages(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> list[Message]:
    """Get all messages from chat.

    Args:
        chat_id: Chat ID
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        List of messages
    """
    messages = await chat_service.get_messages(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id
    )

    return [
        Message(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            metadata=msg.metadata_,  # Corregido: metadata_ es el atributo ORM
            created_at=msg.created_at
        )
        for msg in messages
    ]
