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

        # Priority 1: If no buyer persona, check if we have enough info
        if not context['has_buyer_persona']:
            # ✅ Check if user has provided business information
            has_business_info = self._has_business_information(
                user_message,
                context['recent_chat']
            )

            if has_business_info:
                # User provided info → Generate buyer persona
                return AgentState.BUYER_PERSONA
            else:
                # No info yet → Ask for business details first
                return AgentState.WAITING  # Will show onboarding message

        # Priority 2: If user uploaded documents but not processed
        # (Future: implement document processing agent)
        # if self._has_pending_documents(context):
        #     return AgentState.DOCUMENT_PROCESSING

        # Priority 3: If user explicitly requests content generation
        if self._is_content_request(user_message):
            return AgentState.CONTENT_GENERATION

        # Priority 4: Conversational fallback cuando YA hay buyer persona.
        # Cualquier mensaje no vacío después de tener buyer persona
        # se trata como parte de la conversación de contenido.
        if context["has_buyer_persona"] and user_message.strip():
            return AgentState.CONTENT_GENERATION

        # Default: Just waiting for user request (sin buyer persona)
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
            # ✅ Content Generator Agent
            yield json.dumps({
                "type": "chunk",
                "content": "🎨 Generando ideas de contenido personalizadas...\n"
            })

            from ..agents.content_generator_agent import ContentGeneratorAgent

            content_agent = ContentGeneratorAgent(self.llm, self.memory)
            result = await content_agent.execute(chat_id, project_id, user_message)

            if result["success"]:
                # Format content ideas nicely
                ideas = result.get("content_ideas", [])

                if ideas:
                    content_text = "✨ **Ideas de Contenido Generadas:**\n\n"

                    for i, idea in enumerate(ideas[:10], 1):  # Max 10 ideas
                        if isinstance(idea, dict):
                            titulo = idea.get("titulo", f"Idea {i}")
                            plataforma = idea.get("plataforma", "TikTok/Instagram")
                            hook = idea.get("hook", "")
                            estructura = idea.get("estructura", "")
                            cta = idea.get("cta", "")

                            content_text += f"**{i}. {titulo}** ({plataforma})\n"
                            if hook:
                                content_text += f"🎣 Hook: {hook}\n"
                            if estructura:
                                content_text += f"📋 Estructura: {estructura}\n"
                            if cta:
                                content_text += f"📢 CTA: {cta}\n"
                            content_text += "\n"
                        else:
                            # Fallback for non-dict ideas
                            content_text += f"**{i}.** {str(idea)}\n\n"

                    content_text += "\n💡 Estas ideas están personalizadas para tu buyer persona y usan técnicas probadas de contenido viral."
                else:
                    content_text = result.get("message", "✅ Contenido generado correctamente.")
            else:
                content_text = f"❌ {result.get('message', 'Error al generar contenido')}"

            yield json.dumps({"type": "chunk", "content": content_text})

        elif state == AgentState.WAITING:
            # Check if we need to ask for business info first
            context = await self._get_context(chat_id, project_id, user_message)

            if not context['has_buyer_persona']:
                # ✅ Onboarding: Ask for business information
                content = (
                    "👋 ¡Hola! Soy tu asistente de marketing IA.\n\n"
                    "Para crear tu buyer persona y ayudarte mejor, necesito conocer tu negocio:\n\n"
                    "📋 Por favor, cuéntame:\n"
                    "1. ¿Qué tipo de negocio tienes? (producto/servicio)\n"
                    "2. ¿A quién le vendes? (tu audiencia objetivo)\n"
                    "3. ¿Cuál es tu principal problema o necesidad de marketing?\n\n"
                    "Con esta información podré crear un análisis completo de tu cliente ideal. 😊"
                )
            else:
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

        Incluye:
        - Solicitudes iniciales ("dame ideas de contenido", "genera posts", etc.)
        - Solicitudes de profundizar en ideas ya generadas ("desarrolla la 2 y la 3", "detalla esas ideas")
        """
        import re

        text = (message or "").strip().lower()
        if len(text.split()) < 3:
            return False

        # Regla 1: verbo de solicitud + objeto de contenido (solicitud inicial)
        verbs = r"(dame|genera|crea|escribe|redacta|hazme|prop[oó]n|sugi[eé]reme)"
        objects = r"(ideas?|contenido|post(s)?|video(s)?|reel(s)?|guion(es)?|script(s)?)"
        if re.search(rf"\b{verbs}\b.*\b{objects}\b", text):
            return True

        # Regla 2: profundizar / desarrollar ideas ya propuestas
        refine_verbs = r"(desarrolla(me)?|detalla|profundiza|expande|contin[uú]a)"
        # Referencias típicas a ideas anteriores: "idea 2", "la 2 y la 3", "esas ideas"
        refine_objects = r"(idea(s)?|la\s+\d+|las\s+\d+|\d+\s+y\s+\d+|opci[oó]n(es)?|esas\s+ideas)"

        if re.search(rf"\b{refine_verbs}\b", text) and re.search(rf"\b{refine_objects}\b", text):
            return True

        return False

    def _has_business_information(
        self,
        current_message: str,
        recent_chat: dict
    ) -> bool:
        """
        Check if user has provided enough business information.

        Looks for:
        - Business type/product/service mentioned
        - Target audience mentioned
        - Marketing needs/problems mentioned
        - At least 30+ words of context

        Args:
            current_message: Current user message
            recent_chat: Recent chat history from memory (from ConversationBufferWindowMemory)

        Returns:
            True if enough information provided
        """
        # recent_chat comes from ConversationBufferWindowMemory.load_memory_variables({})
        # Format: {"history": "Human: ...\nAI: ...\nHuman: ..."}
        all_text = current_message.lower()

        # Extract text from history if available
        if isinstance(recent_chat, dict):
            history = recent_chat.get("history", "")
            if history:
                # Remove "Human:" and "AI:" prefixes, keep only content
                history_clean = history.replace("Human:", "").replace("AI:", "")
                all_text += " " + history_clean.lower()

        # Check for business-related keywords
        business_keywords = [
            "negocio", "empresa", "producto", "servicio", "vendo", "vendo",
            "cliente", "audiencia", "mercado", "competencia", "marketing",
            "ventas", "publicidad", "promocion", "estrategia", "objetivo",
            "tengo", "ofrezco", "dedico", "trabajo", "hago"
        ]

        keyword_count = sum(1 for keyword in business_keywords if keyword in all_text)

        # Need at least 2 business keywords AND reasonable length (30+ words)
        word_count = len(all_text.split())

        return keyword_count >= 2 and word_count >= 30

    def _get_state_reason(self, state: AgentState) -> str:
        """
        Get human-readable reason for state.

        Args:
            state: Agent state

        Returns:
            Reason string
        """
        reasons = {
            AgentState.BUYER_PERSONA: "Generando buyer persona completo...",
            AgentState.WAITING: "Esperando instrucciones del usuario.",
            AgentState.CONTENT_GENERATION: "Generando contenido solicitado...",
            AgentState.DOCUMENT_PROCESSING: "Procesando documentos subidos..."
        }

        return reasons.get(state, "Estado desconocido")
