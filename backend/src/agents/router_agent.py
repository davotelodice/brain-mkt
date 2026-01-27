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

    async def process_stream(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ):  # type: ignore[return]
        """
        Process message and stream response in real-time.

        Flow:
        1. Route to appropriate agent
        2. Stream agent execution (if agent supports it)
        3. Save final response to memory

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User's message

        Yields:
            JSON chunks with streaming data:
            {"type": "status", "content": "..."}
            {"type": "chunk", "content": "..."}
            {"type": "done", "content": "..."}
        """
        import json

        # 1. Route to appropriate agent
        state = await self.route(chat_id, project_id, user_message)
        reason = self._get_state_reason(state)

        # 2. Send initial status
        yield json.dumps({"type": "status", "content": reason})

        # 3. Execute agent with streaming
        if state == AgentState.BUYER_PERSONA:
            # Buyer Persona is NOT streamable (long analysis)
            # Send progress updates instead
            yield json.dumps({
                "type": "chunk",
                "content": "📊 Analizando perfil de cliente ideal...\n"
            })

            yield json.dumps({
                "type": "chunk",
                "content": "🔍 Investigando puntos de dolor...\n"
            })

            yield json.dumps({
                "type": "chunk",
                "content": "💡 Generando insights de marketing...\n"
            })

            # Execute (non-streaming)
            # Note: BuyerPersonaAgent needs db parameter
            from ..agents.buyer_persona_agent import BuyerPersonaAgent

            buyer_agent = BuyerPersonaAgent(self.llm, self.memory, self.memory.db)
            result = await buyer_agent.execute(chat_id, project_id, user_message)

            if result["success"]:
                final_content = (
                    "✅ Buyer persona completo generado.\n\n"
                    "Ahora puedes pedirme:\n"
                    "- 'Dame ideas de contenido'\n"
                    "- 'Genera posts para Instagram'\n"
                    "- 'Crea customer journey'"
                )
            else:
                final_content = f"❌ Error: {result['message']}"

            yield json.dumps({"type": "chunk", "content": final_content})

        elif state == AgentState.CONTENT_GENERATION:
            # Future: Content Generator Agent with streaming
            # For now, placeholder
            yield json.dumps({
                "type": "chunk",
                "content": "🚧 Generación de contenido en desarrollo (TAREA 7+).\n"
            })

        elif state == AgentState.WAITING:
            # Just acknowledge
            content = (
                "Esperando tus instrucciones. Puedes pedirme:\n"
                "- 'Dame ideas de contenido'\n"
                "- 'Genera posts'\n"
                "- 'Analiza mi audiencia'"
            )
            yield json.dumps({"type": "chunk", "content": content})

        # 4. Done signal
        yield json.dumps({"type": "done", "content": ""})

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
