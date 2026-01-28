"""Buyer Persona Agent - Generates complete buyer persona analysis (40+ questions)."""

import json
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import MarketingBuyerPersona
from .base_agent import BaseAgent


class BuyerPersonaAgent(BaseAgent):
    """
    Buyer Persona Agent.

    Generates ULTRA DETAILED buyer persona following complete template:
    - 11 categories
    - 40+ specific questions
    - Must answer ALL questions (cannot skip any)
    - Follows example format ("Ana" case from PRP)
    """

    def __init__(self, llm_service, memory_manager, db: AsyncSession):
        """
        Initialize buyer persona agent.

        Args:
            llm_service: LLM service
            memory_manager: Memory manager
            db: Database session
        """
        super().__init__(llm_service, memory_manager)
        self.db = db

    async def execute(
        self,
        chat_id: UUID,
        project_id: UUID,
        user_message: str
    ) -> dict:
        """
        Generate complete buyer persona and derived analysis (forum + CJ).

        Args:
            chat_id: Chat ID
            project_id: Project ID
            user_message: User's message/context

        Returns:
            {
                "success": bool,
                "buyer_persona": dict,
                "message": str
            }
        """
        # 1. Get context (relevant documents)
        context = await self._get_context(chat_id, project_id, user_message)

        # 2. Build prompt with complete template (desde buyer-plantilla.md)
        prompt = self._build_buyer_persona_prompt(
            user_message=user_message,
            relevant_docs=context["relevant_docs"],
        )

        # 3. Generate buyer persona
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system=(
                    "Eres un experto en marketing digital especializado en crear buyer personas "
                    "ULTRA DETALLADAS. SIEMPRE responde en formato JSON válido."
                ),
                max_tokens=8000,
                temperature=0.7,
            )

            # 4. Clean response (remove markdown code blocks if present)
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()

            # 5. Parse JSON response
            if not response_clean:
                raise json.JSONDecodeError("Empty response from LLM", response, 0)

            buyer_persona_data = json.loads(response_clean)

            # 6. Save base buyer persona in DB
            buyer_persona = MarketingBuyerPersona(
                chat_id=chat_id,
                project_id=project_id,
                initial_questions={},
                full_analysis=buyer_persona_data,
                forum_simulation={},
                pain_points={},
                customer_journey={},
            )
            self.db.add(buyer_persona)
            await self.db.commit()

            # 7. Generate forum + pain points + customer journey en background lógico
            try:
                forum_simulation, pain_points = await self._generate_forum_and_pain_points(
                    buyer_persona_data
                )
                customer_journey = await self._generate_customer_journey(
                    buyer_persona_data, forum_simulation, pain_points
                )

                buyer_persona.forum_simulation = forum_simulation
                buyer_persona.pain_points = pain_points
                buyer_persona.customer_journey = customer_journey
                await self.db.commit()
            except Exception:
                # Si falla la parte extendida, mantenemos al menos el buyer persona base
                pass

            return {
                "success": True,
                "buyer_persona": buyer_persona_data,
                "message": "Buyer persona y análisis extendido generados correctamente.",
            }

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "buyer_persona": None,
                "message": f"Error al parsear respuesta del LLM: {e}",
            }
        except Exception as e:
            return {
                "success": False,
                "buyer_persona": None,
                "message": f"Error al generar buyer persona: {e}",
            }

    def _build_buyer_persona_prompt(
        self,
        user_message: str,
        relevant_docs: list[dict],
    ) -> str:
        """
        Build complete prompt with buyer persona template loaded from markdown file.
        """
        docs_text = (
            "\n\n".join(
                [
                    f"Documento: {doc['source_title']}\n{doc['content']}"
                    for doc in relevant_docs
                ]
            )
            if relevant_docs
            else "No hay documentos adicionales."
        )

        # Cargar plantilla completa desde contenido/buyer-plantilla.md
        project_root = Path(__file__).resolve().parents[3]
        template_path = project_root / "contenido" / "buyer-plantilla.md"
        try:
            buyer_template = template_path.read_text(encoding="utf-8")
        except OSError:
            buyer_template = ""

        prompt = f"""
Eres un experto en marketing digital con amplios conocimientos en mercadología.

Estás por comenzar una campaña publicitaria (paid + orgánico) y antes necesitas construir
un buyer persona ULTRA DETALLADO para el siguiente negocio:

## INFORMACIÓN DEL NEGOCIO (mensaje del usuario)
{user_message}

## DOCUMENTOS ADICIONALES RELEVANTES (RAG)
{docs_text}

## PLANTILLA COMPLETA DE BUYER PERSONA (archivo buyer-plantilla.md)

La siguiente plantilla contiene TODAS las preguntas que debes responder, junto con
un ejemplo real para otro negocio distinto (caso "Ana"). DEBES:
- Usar TODAS LAS PREGUNTAS como lista exacta de campos a responder.
- Usar las RESPUESTAS DE EJEMPLO solo como referencia de tono, nivel de detalle y estilo,
  pero sin copiarlas literalmente (el contenido debe ser 100% coherente con este negocio).
- Construir un buyer persona totalmente nuevo y coherente con el negocio actual.

---
{buyer_template}
---

INSTRUCCIONES CRÍTICAS:
- Responde **CADA PREGUNTA** de la plantilla, sin saltarte ninguna.
- Cada pregunta debe convertirse en un campo explícito dentro del JSON de salida.
- Si falta información, infiere de forma realista según el contexto del negocio.
- Mantén coherencia total entre todas las respuestas (una sola persona).
- Sé específico y detallado, pensando en campañas de Meta ADS y content marketing.
- Devuelve ÚNICAMENTE un JSON VÁLIDO, estructurado por secciones (usa los títulos
  de la plantilla como claves de primer nivel y cada pregunta como campos internos).
"""

        return prompt

    async def _generate_forum_and_pain_points(
        self,
        buyer_persona_data: dict,
    ) -> tuple[dict, dict]:
        """
        Generate forum simulation and pain points based on buyer persona.
        """
        base_instructions = (
            "Basándonos en el buyer persona que te paso en JSON, toma el papel de esa persona "
            "e imagina que estás en un foro de internet donde las personas se reúnen a quejarse "
            "o recomendar este tipo de servicios. Debes:\n"
            "1) Generar varios posts de foro donde el buyer persona se queja de problemas al "
            "contratar servicios similares, y después de cada queja incluya la solución o lo que "
            "le gustaría que ocurriera para que el problema no exista.\n"
            "2) Después, generar una lista clara de 10 puntos de dolor que resuman todo lo que "
            "piensa y siente antes de la compra (criterios y comportamientos).\n"
        )

        prompt = f"""
Buyer persona en JSON (contexto completo):
{json.dumps(buyer_persona_data, ensure_ascii=False, indent=2)}

{base_instructions}

Responde EXCLUSIVAMENTE en JSON válido con la siguiente estructura:
{{
  "posts": [
    {{"queja": "texto de la queja", "solucion_deseada": "texto de la solución deseada"}}
  ],
  "pain_points": {{
    "items": [
      "Punto de dolor 1",
      "Punto de dolor 2",
      "... hasta 10 elementos ..."
    ]
  }}
}}
"""

        response = await self.llm.generate(
            prompt=prompt,
            system=(
                "Eres el buyer persona descrito en el JSON anterior. "
                "Respondes con lenguaje natural pero SIEMPRE en formato JSON válido."
            ),
            max_tokens=4000,
            temperature=0.7,
        )

        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        response_clean = response_clean.strip()

        if not response_clean:
            raise json.JSONDecodeError("Empty response from LLM (forum)", response, 0)

        data = json.loads(response_clean)
        forum_simulation = {"posts": data.get("posts", [])}
        pain_points_raw = data.get("pain_points") or {}
        if isinstance(pain_points_raw, dict):
            items = pain_points_raw.get("items", [])
        else:
            items = pain_points_raw or []
        pain_points = {"items": items}
        return forum_simulation, pain_points

    async def _generate_customer_journey(
        self,
        buyer_persona_data: dict,
        forum_simulation: dict,
        pain_points: dict,
    ) -> dict:
        """
        Generate customer journey (awareness, consideration, purchase).
        """
        cj_instructions = (
            "Actúa como un experto en content marketing. Basándote en el buyer persona, "
            "en su comportamiento en foros y en sus puntos de dolor, crea un customer journey "
            "para estrategia de contenidos con 3 fases de conciencia:\n"
            "- conciencia: todo lo que hace hasta tomar conciencia de su necesidad.\n"
            "- consideracion: cuando ya compara 2-3 opciones.\n"
            "- compra: cuando decide comprar.\n"
            "Para cada fase, genera al menos 10 frases de lo que busca en internet "
            "(busquedas) y 10 frases de lo que pasa por su cabeza / lo que quiere saber "
            "(preguntas_cabeza).\n"
        )

        prompt = f"""
Buyer persona en JSON:
{json.dumps(buyer_persona_data, ensure_ascii=False, indent=2)}

Simulación de foro:
{json.dumps(forum_simulation, ensure_ascii=False, indent=2)}

Puntos de dolor:
{json.dumps(pain_points, ensure_ascii=False, indent=2)}

{cj_instructions}

Responde ÚNICAMENTE en JSON válido con la estructura:
{{
  "awareness": {{
    "busquedas": ["...", "..."],
    "preguntas_cabeza": ["...", "..."]
  }},
  "consideration": {{
    "busquedas": ["...", "..."],
    "preguntas_cabeza": ["...", "..."]
  }},
  "purchase": {{
    "busquedas": ["...", "..."],
    "preguntas_cabeza": ["...", "..."]
  }}
}}
"""

        response = await self.llm.generate(
            prompt=prompt,
            system=(
                "Eres un experto en customer journey y content marketing. "
                "Devuelves SIEMPRE JSON válido con fases awareness/consideration/purchase."
            ),
            max_tokens=4000,
            temperature=0.7,
        )

        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        response_clean = response_clean.strip()

        if not response_clean:
            raise json.JSONDecodeError("Empty response from LLM (CJ)", response, 0)

        customer_journey = json.loads(response_clean)
        return customer_journey
