"""Chat service - Business logic for chat operations."""
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingChat, MarketingMessage


class ChatService:
    """Service for chat CRUD operations."""

    def __init__(self, db: AsyncSession):
        """Initialize chat service.

        Args:
            db: Async database session
        """
        self.db = db

    async def create_chat(
        self,
        user_id: UUID,
        project_id: UUID,
        title: str = "New Chat"
    ) -> MarketingChat:
        """Create new chat.

        Args:
            user_id: User ID
            project_id: Project ID (CRITICAL for isolation)
            title: Chat title

        Returns:
            Created chat
        """
        chat = MarketingChat(
            user_id=user_id,
            project_id=project_id,
            title=title
        )
        self.db.add(chat)
        await self.db.flush()
        await self.db.refresh(chat)
        return chat

    async def list_chats(
        self,
        user_id: UUID,
        project_id: UUID
    ) -> list[MarketingChat]:
        """List all chats for user in project.

        Args:
            user_id: User ID
            project_id: Project ID (CRITICAL filter)

        Returns:
            List of chats ordered by most recent
        """
        query = select(MarketingChat).where(
            MarketingChat.user_id == user_id,
            MarketingChat.project_id == project_id
        ).order_by(MarketingChat.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_chat(
        self,
        chat_id: UUID,
        user_id: UUID,
        project_id: UUID
    ) -> MarketingChat:
        """Get specific chat.

        Args:
            chat_id: Chat ID
            user_id: User ID (validates ownership)
            project_id: Project ID (validates isolation)

        Returns:
            Chat if found and owned by user

        Raises:
            HTTPException: 404 if chat not found or not owned by user
        """
        query = select(MarketingChat).where(
            MarketingChat.id == chat_id,
            MarketingChat.user_id == user_id,
            MarketingChat.project_id == project_id
        )
        result = await self.db.execute(query)
        chat = result.scalar_one_or_none()

        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        return chat

    async def update_chat_title(
        self,
        chat_id: UUID,
        user_id: UUID,
        project_id: UUID,
        new_title: str
    ) -> MarketingChat:
        """Update chat title.

        Args:
            chat_id: Chat ID
            user_id: User ID
            project_id: Project ID
            new_title: New title

        Returns:
            Updated chat
        """
        chat = await self.get_chat(chat_id, user_id, project_id)
        chat.title = new_title
        await self.db.flush()
        await self.db.refresh(chat)
        return chat

    async def delete_chat(
        self,
        chat_id: UUID,
        user_id: UUID,
        project_id: UUID
    ) -> None:
        """Delete chat (cascade deletes messages).

        Args:
            chat_id: Chat ID
            user_id: User ID
            project_id: Project ID
        """
        # Validate ownership first
        await self.get_chat(chat_id, user_id, project_id)

        # Delete (cascades to messages via ON DELETE CASCADE)
        stmt = delete(MarketingChat).where(MarketingChat.id == chat_id)
        await self.db.execute(stmt)
        await self.db.flush()

    async def get_messages(
        self,
        chat_id: UUID,
        user_id: UUID,
        project_id: UUID
    ) -> list[MarketingMessage]:
        """Get all messages from chat.

        Args:
            chat_id: Chat ID
            user_id: User ID
            project_id: Project ID

        Returns:
            List of messages ordered chronologically
        """
        # Validate access to chat first
        await self.get_chat(chat_id, user_id, project_id)

        query = select(MarketingMessage).where(
            MarketingMessage.chat_id == chat_id
        ).order_by(MarketingMessage.created_at.asc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_message(
        self,
        chat_id: UUID,
        user_id: UUID,
        project_id: UUID,
        role: str,
        content: str,
        metadata: dict[str, str] | None = None
    ) -> MarketingMessage:
        """Create new message in chat.

        Args:
            chat_id: Chat ID
            user_id: User ID
            project_id: Project ID
            role: Message role ('user' | 'assistant' | 'system')
            content: Message content
            metadata: Optional metadata

        Returns:
            Created message
        """
        # Validate access to chat
        await self.get_chat(chat_id, user_id, project_id)

        message = MarketingMessage(
            chat_id=chat_id,
            project_id=project_id,
            role=role,
            content=content,
            metadata_=metadata or {}  # Use metadata_ to avoid SQLAlchemy reserved name
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_chat_with_message_count(
        self,
        user_id: UUID,
        project_id: UUID
    ) -> list[dict]:
        """Get chats with message count.

        Args:
            user_id: User ID
            project_id: Project ID

        Returns:
            List of chat summaries with message counts
        """
        query = (
            select(
                MarketingChat,
                func.count(MarketingMessage.id).label('message_count')
            )
            .outerjoin(MarketingMessage, MarketingChat.id == MarketingMessage.chat_id)
            .where(
                MarketingChat.user_id == user_id,
                MarketingChat.project_id == project_id
            )
            .group_by(MarketingChat.id)
            .order_by(MarketingChat.created_at.desc())
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                **{k: v for k, v in row._mapping.items() if k != 'message_count'},
                'message_count': row.message_count
            }
            for row in rows
        ]
