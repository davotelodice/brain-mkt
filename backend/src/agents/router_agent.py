"""Router Agent - Main orchestrator deciding which agent to execute."""

from enum import Enum
from uuid import UUID

from .base_agent import BaseAgent


class AgentState(str, Enum):
    """
    Agent states for routing decisions.

    Flow:
    INITIAL → BUYER_PERSONA → WAITING → CONTENT_GENERATION (on-demand)
    """
    INITIAL = "initial"
    BUYER_PERSONA = "buyer_persona"
    WAITING = "waiting"
    CONTENT_GENERATION = "content_generation"
    DOCUMENT_PROCESSING = "document_processing"  # Future: for processing docs


class RouterAgent(BaseAgent):
    """
    Router Agent - Main orchestrator.

    Uses rule-based routing (no LLM call needed for routing decision).

    Routing logic:
    1. No buyer persona? → BUYER_PERSONA
    2. Has pending documents? → DOCUMENT_PROCESSING (future)
    3. User requests content? → CONTENT_GENERATION
    4. Default → WAITING

    CRITICAL: Content generation ONLY happens on explicit user request.
    """

    async def route(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> AgentState:
        """
        Decide which agent should execute based on chat state and user message.

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User's message

        Returns:
            Agent state (which agent to execute)
        """
        # 1. Get context from memory manager
        context = await self._get_context(chat_id, project_id, user_message)

        # 2. Rule-based routing

        # Priority 1: If no buyer persona, create one
        if not context['has_buyer_persona']:
            return AgentState.BUYER_PERSONA

        # Priority 2: If user uploaded documents but not processed
        # (Future: implement document processing agent)
        # if self._has_pending_documents(context):
        #     return AgentState.DOCUMENT_PROCESSING

        # Priority 3: If user explicitly requests content generation
        if self._is_content_request(user_message):
            return AgentState.CONTENT_GENERATION

        # Default: Just waiting for user request
        return AgentState.WAITING

    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        """
        Execute routing decision.

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User message

        Returns:
            Routing result:
            {
                "state": AgentState,
                "reason": str,
                "should_execute_agent": bool
            }
        """
        state = await self.route(chat_id, project_id, user_message)

        return {
            "state": state,
            "reason": self._get_state_reason(state),
            "should_execute_agent": state != AgentState.WAITING
        }

    def _is_content_request(self, message: str) -> bool:
        """
        Detect if user is requesting content generation.

        Keywords: dame, genera, crea, escribe, ideas, posts, videos, scripts

        Args:
            message: User message

        Returns:
            True if content request detected
        """
        content_keywords = [
            'dame', 'genera', 'crea', 'escribe', 'ideas',
            'posts', 'videos', 'scripts', 'contenido',
            'publica', 'redacta', 'hazme', 'necesito'
        ]

        message_lower = message.lower()
        return any(keyword in message_lower for keyword in content_keywords)

    def _get_state_reason(self, state: AgentState) -> str:
        """
        Get human-readable reason for state.

        Args:
            state: Agent state

        Returns:
            Reason string
        """
        reasons = {
            AgentState.BUYER_PERSONA: "No hay buyer persona. Creando análisis completo...",
            AgentState.WAITING: "Esperando instrucciones del usuario.",
            AgentState.CONTENT_GENERATION: "Generando contenido solicitado...",
            AgentState.DOCUMENT_PROCESSING: "Procesando documentos subidos..."
        }

        return reasons.get(state, "Estado desconocido")
