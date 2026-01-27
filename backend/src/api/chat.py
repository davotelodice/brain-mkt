"""Chat API endpoints."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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

router = APIRouter(prefix="/api/chats", tags=["chats"])


def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    """Dependency for chat service.

    Args:
        db: Database session

    Returns:
        ChatService instance
    """
    return ChatService(db)


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
                metadata=msg.metadata,
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


@router.post("/{chat_id}/messages", response_model=Message)
async def send_message(
    chat_id: UUID,
    request: SendMessageRequest,
    user: MarketingUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> Message:
    """Send message to chat.

    Args:
        chat_id: Chat ID
        request: Message request
        user: Current authenticated user
        chat_service: Chat service

    Returns:
        Created message
    """
    # Create user message
    message = await chat_service.create_message(
        chat_id=chat_id,
        user_id=user.id,
        project_id=user.project_id,
        role="user",
        content=request.content
    )

    # TODO: In TAREA 4, trigger AI agent here

    return Message(
        id=message.id,
        role=message.role,
        content=message.content,
        metadata=message.metadata,
        created_at=message.created_at
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
            metadata=msg.metadata,
            created_at=msg.created_at
        )
        for msg in messages
    ]
