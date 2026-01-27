"""Content Generator Agent - Generates content ideas using buyer persona + RAG techniques."""

import json
from uuid import UUID

from .base_agent import BaseAgent


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

        # 3. Build enhanced prompt with buyer persona + RAG techniques
        prompt = self._build_content_prompt(
            user_message=user_message,
            buyer_persona=context['buyer_persona'],
            relevant_docs=context['relevant_docs']
        )

        # 4. Generate content ideas
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system="Eres un experto en marketing digital especializado en crear contenido viral para redes sociales (TikTok, Instagram, YouTube).",
                max_tokens=4000,
                temperature=0.8
            )

            # 5. Parse response (can be JSON or markdown)
            content_ideas = self._parse_content_response(response)

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

    def _build_content_prompt(
        self,
        user_message: str,
        buyer_persona: dict,
        relevant_docs: list[dict]
    ) -> str:
        """
        Build prompt for content generation.

        Args:
            user_message: User's request
            buyer_persona: Buyer persona data
            relevant_docs: Relevant documents from RAG (transcripts + user docs)

        Returns:
            Complete prompt string
        """
        # Format buyer persona
        persona_text = json.dumps(buyer_persona, indent=2, ensure_ascii=False) if buyer_persona else "No disponible"

        # Format relevant documents (filter transcripts for techniques)
        techniques_text = ""
        user_docs_text = ""

        for doc in relevant_docs:
            if doc.get('content_type') == 'video_transcript':
                techniques_text += f"\n\n📹 TÉCNICA DE ANDREA ESTRATEGA ({doc.get('source_title', 'Video')}):\n{doc.get('content', '')}"
            elif doc.get('content_type') == 'user_document':
                user_docs_text += f"\n\n📄 DOCUMENTO DEL USUARIO ({doc.get('source_title', 'Documento')}):\n{doc.get('content', '')}"

        if not techniques_text:
            techniques_text = "No hay técnicas específicas disponibles en este momento."

        prompt = f"""
Eres un experto en marketing digital especializado en crear contenido viral para TikTok e Instagram.

## SOLICITUD DEL USUARIO:
{user_message}

## BUYER PERSONA DEL CLIENTE:
{persona_text}

## TÉCNICAS DE CONTENIDO VIRAL (de Andrea Estratega):
{techniques_text}

## DOCUMENTOS ADICIONALES DEL USUARIO:
{user_docs_text if user_docs_text else "No hay documentos adicionales."}

## TU TAREA:

Genera ideas de contenido personalizadas que:

1. **Se adapten específicamente al buyer persona:**
   - Usa su lenguaje y expresiones
   - Aborda sus problemas y necesidades reales
   - Resuena con su mentalidad y comportamiento

2. **Apliquen técnicas virales probadas:**
   - Hooks que capten atención en los primeros 3 segundos
   - Estructuras que mantengan engagement
   - Formatos que funcionan en TikTok/Instagram (2025-2026)

3. **Sean accionables y específicas:**
   - Cada idea debe tener: título, hook inicial, estructura, CTA
   - Adaptadas a la plataforma solicitada (TikTok, Instagram, etc.)
   - Listas para ejecutar

## FORMATO DE RESPUESTA:

Responde en formato JSON con esta estructura:

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

IMPORTANTE:
- Genera mínimo 5 ideas (ideal 7-10)
- Sé específico y personalizado (no genérico)
- Usa técnicas reales de las transcripciones
- Adapta al buyer persona específico
- Enfócate en contenido que realmente resuene con la audiencia

## TU RESPUESTA (JSON):
"""

        return prompt

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
                return data["ideas"]
            elif isinstance(data, list):
                return data
            else:
                # Fallback: return as single idea
                return [{"titulo": "Idea generada", "contenido": response_clean}]
        except json.JSONDecodeError:
            # If not JSON, return as markdown text
            return [{"titulo": "Ideas de contenido", "contenido": response_clean}]
