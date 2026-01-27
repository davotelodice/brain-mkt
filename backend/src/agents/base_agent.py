"""Base Agent - Shared functionality for all agents."""

from abc import ABC, abstractmethod
from uuid import UUID

from ..services.llm_service import LLMService
from ..services.memory_manager import MemoryManager


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Provides shared functionality:
    - Access to LLM service
    - Access to memory manager
    - Common logging/error handling patterns
    """

    def __init__(
        self,
        llm_service: LLMService,
        memory_manager: MemoryManager
    ):
        """
        Initialize base agent.

        Args:
            llm_service: LLM service for text generation
            memory_manager: Memory manager for context
        """
        self.llm = llm_service
        self.memory = memory_manager

    @abstractmethod
    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        """
        Execute agent's main task.

        This method must be implemented by all concrete agents.

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User's message/request

        Returns:
            Agent execution result
        """
        pass

    async def _get_context(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        """
        Get complete context from memory manager.

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: Current user message

        Returns:
            Context dictionary from memory manager
        """
        return await self.memory.get_context(
            chat_id=chat_id,
            project_id=project_id,
            current_message=user_message
        )
