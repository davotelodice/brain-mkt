"""Content Generator Agent - Generates content ideas using buyer persona + RAG techniques."""

import json
import logging
from typing import Any, cast
from uuid import UUID

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ContentGeneratorAgent(BaseAgent):
    """
    Content Generator Agent.

    Generates personalized content ideas using:
    1. Buyer persona from chat (long-term memory)
    2. RAG techniques from Andrea Estratega transcripts (semantic search)
    3. User's uploaded documents (if any)

    Only executes when explicitly requested by user.
    """

    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        """
        Generate content ideas based on buyer persona and RAG techniques.

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User's content request (e.g., "ideas de contenido para TikTok")

        Returns:
            {
                "success": bool,
                "content_ideas": list[dict],
                "message": str
            }
        """
        # 1. Get context (buyer persona + relevant docs)
        context = await self._get_context(chat_id, project_id, user_message)

        # 2. Check if buyer persona exists
        if not context['has_buyer_persona']:
            return {
                "success": False,
                "content_ideas": [],
                "message": "Primero necesito generar tu buyer persona. Por favor, cuéntame sobre tu negocio."
            }

        # 3. Build system prompt with training data, buyer persona, CJ, etc.
        system_prompt = await self._build_system_prompt(context, project_id)

        # 4. Format messages with full conversation history
        messages = self.memory.format_messages_from_memory(
            chat_id=chat_id,
            system_prompt=system_prompt,
            current_user_message=user_message
        )

        # 5. Generate content ideas with full conversation history
        try:
            # Calculate approximate tokens in messages to ensure we have enough for response
            # Rough estimate: 1 token ≈ 4 characters
            total_chars = sum(len(str(msg.get("content", ""))) for msg in messages)
            estimated_input_tokens = total_chars // 4

            # Reserve tokens for response (ensure at least 2000 tokens for output)
            # Most models have 128k context, but we'll be conservative
            max_tokens = min(6000, 8000 - estimated_input_tokens) if estimated_input_tokens < 8000 else 2000

            logger.info(f"Generating with max_tokens={max_tokens} (estimated input: {estimated_input_tokens} tokens)")

            response = await self.llm.generate_with_messages(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.8
            )

            # Log response for debugging (truncate if too long)
            response_preview = response[:500] if len(response) > 500 else response
            logger.info(f"LLM response preview: {response_preview}...")

            # 6. Parse response (can be JSON or markdown)
            content_ideas = self._parse_content_response(response)

            logger.info(f"Parsed {len(content_ideas)} content ideas")

            return {
                "success": True,
                "content_ideas": content_ideas,
                "message": f"✅ Generé {len(content_ideas)} ideas de contenido personalizadas."
            }

        except Exception as e:
            return {
                "success": False,
                "content_ideas": [],
                "message": f"Error al generar contenido: {str(e)}"
            }

    async def _build_system_prompt(self, context: dict, project_id: UUID) -> str:
        """
        Build system prompt with training data, buyer persona, CJ, and documents.

        This method constructs a comprehensive system prompt that includes:
        1. Training techniques from Andrea Estratega transcripts (always)
        2. Buyer persona data
        3. Customer journey
        4. Pain points
        5. Document summaries

        Args:
            context: Context dictionary from memory manager
            project_id: Project ID for training summary

        Returns:
            Complete system prompt string
        """
        # 1. Get training summary (cacheado, siempre disponible)
        training_summary = await self.memory.get_training_summary(project_id)

        # 2. Format buyer persona
        buyer_persona = context.get('buyer_persona')
        persona_text = json.dumps(buyer_persona, indent=2, ensure_ascii=False) if buyer_persona else "No disponible aún"

        # 3. Format customer journey
        customer_journey = context.get('customer_journey')
        cj_text = ""
        if customer_journey and isinstance(customer_journey, dict):
            parts: list[str] = []
            for phase_key, phase_label in [
                ("awareness", "Conciencia"),
                ("consideration", "Consideración"),
                ("purchase", "Compra"),
            ]:
                phase = customer_journey.get(phase_key) or {}
                if isinstance(phase, dict):
                    busquedas = phase.get("busquedas") or []
                    preguntas = phase.get("preguntas_cabeza") or []
                    if busquedas or preguntas:
                        parts.append(f"### Fase {phase_label}")
                        if busquedas:
                            parts.append("  - Búsquedas típicas:")
                            parts.extend([f"    * {b}" for b in busquedas])
                        if preguntas:
                            parts.append("  - Preguntas en su cabeza:")
                            parts.extend([f"    * {q}" for q in preguntas])
            if parts:
                cj_text = "\n".join(parts)
        else:
            cj_text = "Aún no se ha generado un customer journey detallado."

        # 4. Format pain points
        pain_points = context.get("pain_points")
        pain_points_text = ""
        if pain_points:
            items = []
            if isinstance(pain_points, dict):
                raw_items = pain_points.get("items", [])
                if isinstance(raw_items, list):
                    items = raw_items
            elif isinstance(pain_points, list):
                items = pain_points
            if items:
                pain_points_text = "\n".join(f"- {p}" for p in items)
        else:
            pain_points_text = "No hay puntos de dolor persistidos todavía."

        # 5. Format document summaries
        document_summaries = context.get("document_summaries", [])
        summaries_text = ""
        if document_summaries:
            summaries_text = "\n\n".join(
                [f"📄 {d.get('filename', 'Documento')}: {d.get('summary', '')}" for d in document_summaries[:5]]
            )
        else:
            summaries_text = "No hay resúmenes persistentes aún."

        # 6. Format user documents from RAG (if any)
        relevant_docs = context.get("relevant_docs", [])
        user_docs_text = ""
        for doc in relevant_docs:
            if doc.get('content_type') == 'user_document':
                user_docs_text += f"\n\n📄 DOCUMENTO DEL USUARIO ({doc.get('source_title', 'Documento')}):\n{doc.get('content', '')[:500]}"
        if not user_docs_text:
            user_docs_text = "No hay documentos adicionales."

        system_prompt = f"""Eres un experto en marketing digital especializado en crear contenido viral
para redes sociales (TikTok, Instagram, YouTube).

## TÉCNICAS DE ENTRENAMIENTO (de Andrea Estratega - experta en contenido viral):
{training_summary}

## BUYER PERSONA DEL CLIENTE:
{persona_text}

## PUNTOS DE DOLOR PRINCIPALES:
{pain_points_text}

## CUSTOMER JOURNEY (fases y preguntas):
{cj_text}

## DOCUMENTOS ADICIONALES DEL USUARIO:
{user_docs_text}

## RESÚMENES PERSISTENTES (Contexto largo de documentos):
{summaries_text}

## TU ESTILO Y ENFOQUE:

- Usa las técnicas probadas de arriba en TODO tu contenido
- Adapta técnicas al buyer persona específico (lenguaje, problemas, mentalidad)
- Considera la fase del customer journey (awareness/consideration/purchase)
- Sé específico y accionable (no genérico)
- Genera contenido listo para usar (hooks, estructuras, CTAs)
- Mantén conversación natural, recuerda contexto de mensajes anteriores

## FORMATO DE RESPUESTA:

CRÍTICO: Responde SOLO con JSON válido. No incluyas texto antes o después del JSON.
No uses markdown, no uses explicaciones. SOLO el objeto JSON.

Estructura requerida:

{{
  "ideas": [
    {{
      "titulo": "Título descriptivo de la idea",
      "plataforma": "TikTok" | "Instagram" | "Ambas",
      "hook": "Primeras 3 segundos que captan atención",
      "estructura": "Descripción de cómo desarrollar el contenido",
      "cta": "Call-to-action específico",
      "por_que_viral": "Por qué esta idea funcionará para este buyer persona"
    }},
    ...
  ]
}}

REGLAS ESTRICTAS:
- Genera mínimo 5 ideas (ideal 7-10)
- Responde SOLO con el objeto JSON, sin texto adicional
- No uses ```json o markdown
- Asegúrate de que el JSON esté completo y válido
- Sé específico y personalizado (no genérico)
- Usa técnicas reales de las transcripciones
- Adapta al buyer persona específico

RESPONDE AHORA CON EL JSON:"""

        return system_prompt

    def _parse_content_response(self, response: str) -> list[dict]:
        """
        Parse LLM response (JSON or markdown).

        Args:
            response: LLM response

        Returns:
            List of content ideas
        """
        # Clean response
        response_clean = response.strip()

        # Remove markdown code blocks if present
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        response_clean = response_clean.strip()

        try:
            # Try to parse as JSON
            data = json.loads(response_clean)

            # Extract ideas array
            if isinstance(data, dict) and "ideas" in data:
                ideas = data["ideas"]
                if isinstance(ideas, list) and len(ideas) > 0:
                    return cast(list[dict[str, Any]], ideas)
                logger.warning(f"No ideas found in JSON response: {data}")
                return [{"titulo": "Idea generada", "contenido": response_clean}]
            elif isinstance(data, list) and len(data) > 0:
                return cast(list[dict[str, Any]], data)
            else:
                # Fallback: return as single idea
                logger.warning(f"Unexpected JSON structure: {type(data)}")
                return [{"titulo": "Idea generada", "contenido": response_clean}]
        except json.JSONDecodeError as e:
            # If not JSON, try to extract JSON from markdown or partial JSON
            logger.warning(f"JSON decode error: {e}")
            logger.warning(f"Response that failed to parse: {response_clean[:200]}...")

            # Try to find JSON block in markdown
            if "```json" in response_clean:
                json_start = response_clean.find("```json") + 7
                json_end = response_clean.find("```", json_start)
                if json_end > json_start:
                    try:
                        json_block = response_clean[json_start:json_end].strip()
                        data = json.loads(json_block)
                        if isinstance(data, dict) and "ideas" in data:
                            return cast(list[dict[str, Any]], data["ideas"])
                    except (json.JSONDecodeError, KeyError):
                        pass

            # Try to find JSON object in text (look for { ... })
            if "{" in response_clean and "}" in response_clean:
                start_idx = response_clean.find("{")
                end_idx = response_clean.rfind("}")
                if end_idx > start_idx:
                    try:
                        json_block = response_clean[start_idx:end_idx + 1]
                        data = json.loads(json_block)
                        if isinstance(data, dict) and "ideas" in data:
                            return cast(list[dict[str, Any]], data["ideas"])
                    except json.JSONDecodeError:
                        pass

            # Final fallback: return as markdown text
            logger.error("Could not parse response as JSON. Returning raw content.")
            return [{"titulo": "Ideas de contenido", "contenido": response_clean}]
