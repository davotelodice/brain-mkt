"""Content Generator Agent - Generates content ideas using buyer persona + RAG techniques."""

import hashlib
import json
import logging
import os
import re
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
        user_message: str,
        context_override: dict | None = None,
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
        # PERF: allow caller to pass a precomputed context to avoid double RAG.
        context = context_override or await self._get_context(chat_id, project_id, user_message)

        # 2. Check if buyer persona exists
        if not context['has_buyer_persona']:
            return {
                "success": False,
                "content_ideas": [],
                "message": "Primero necesito generar tu buyer persona. Por favor, cuéntame sobre tu negocio."
            }

        # 3. Detect follow-up requests (refinar / expandir ideas previas)
        requested_numbers = self._extract_requested_numbers(user_message)
        is_refine = self._is_refine_request(user_message)
        mode = self._select_mode(user_message, is_refine)

        trace = os.getenv("AGENT_TRACE", "0") == "1"
        if trace:
            logger.info(
                "[AGENT] chat_id=%s project_id=%s refine=%s nums=%s msg_len=%s",
                str(chat_id),
                str(project_id),
                is_refine,
                requested_numbers,
                len(user_message or ""),
            )

        if is_refine and not requested_numbers:
            return {
                "success": False,
                "content_ideas": [],
                "message": "¿Qué ideas (números) quieres que desarrolle? Ej: 'desarrolla la 3 y la 4'."
            }

        # 4. Build system prompt with training data, buyer persona, CJ, etc.
        system_prompt, prompt_debug = await self._build_system_prompt(
            context=context,
            project_id=project_id,
            mode=mode,
            requested_numbers=requested_numbers
        )

        if trace:
            sp = system_prompt or ""
            sp_hash = hashlib.sha256(sp.encode("utf-8")).hexdigest()[:12]
            logger.info("[PROMPT] system_chars=%s system_sha=%s", len(sp), sp_hash)
            if os.getenv("AGENT_TRACE_SHOW_PROMPTS", "0") == "1":
                logger.info("[PROMPT] system_preview=%s", sp[:1200])

        # 5. Format messages with full conversation history
        # TAREA 6.2: Si es follow-up, reforzamos la instrucción (ya no menciona JSON)
        final_user_message = user_message
        if is_refine and requested_numbers:
            nums = ", ".join(str(n) for n in requested_numbers)
            final_user_message = (
                f"{user_message}\n\n"
                f"INSTRUCCIÓN: No generes ideas nuevas. Desarrolla SOLO las ideas #{nums} de tu respuesta anterior "
                f"con guion/diálogo completo listo para grabar."
            )

        messages = self.memory.format_messages_from_memory(
            chat_id=chat_id,
            system_prompt=system_prompt,
            current_user_message=final_user_message
        )

        # 6. Generate content ideas with full conversation history
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

            # TAREA 6.2: Siempre texto Markdown directo (eliminado parsing JSON)
            content_ideas: list[dict[str, Any]] = []  # Mantenido por compatibilidad
            content_text: str = (response or "").strip()
            tecnicas_aplicadas_count: int = 0  # Ya no se extrae de JSON

            debug: dict[str, Any] = {}
            if trace or os.getenv("SSE_DEBUG", "0") == "1":
                # History length (best-effort)
                history_text = ""
                try:
                    history_text = (
                        self.memory._get_short_term(chat_id)  # type: ignore[attr-defined]
                        .load_memory_variables({})
                        .get("history", "")
                    )
                except Exception:
                    history_text = ""

                # RAG stats from context
                relevant_docs = context.get("relevant_docs", []) or []
                counts: dict[str, int] = {}
                for d in relevant_docs:
                    t = (d.get("content_type") or "unknown") if isinstance(d, dict) else "unknown"
                    counts[t] = counts.get(t, 0) + 1

                # Health check flags (prueba de vida)
                history_chars = len(history_text or "")
                rag_relevant_docs_total = len(relevant_docs)
                training_summary_chars = prompt_debug.get("training_summary_chars", 0) or 0

                # Count learned concepts from books
                learned_concepts = context.get("learned_concepts", []) or []
                learned_concepts_count = len(learned_concepts)
                
                debug = {
                    "stage": "content_generation",
                    "mode": mode,
                    "requested_numbers": requested_numbers,
                    "history_chars": history_chars,
                    "messages_count": len(messages),
                    "estimated_input_tokens": int(estimated_input_tokens),
                    "max_tokens": int(max_tokens),
                    "system_prompt_chars": len(system_prompt or ""),
                    "system_prompt_sha": hashlib.sha256((system_prompt or "").encode("utf-8")).hexdigest()[:12],
                    "rag_relevant_docs_total": rag_relevant_docs_total,
                    "rag_relevant_docs_by_type": counts,
                    "document_summaries_count": len(context.get("document_summaries", []) or []),
                    "learned_concepts_count": learned_concepts_count,  # NEW: Track book concepts
                    "tecnicas_aplicadas_count": tecnicas_aplicadas_count,
                    # Health check flags (prueba de vida automática)
                    "has_history": history_chars > 0,
                    "rag_used": rag_relevant_docs_total > 0,
                    "training_injected": training_summary_chars > 0,
                    "books_knowledge_used": learned_concepts_count > 0,  # NEW: Health check
                    **prompt_debug,
                }

            # TAREA 6.2: Siempre retorna content_text (Markdown)
            return {
                "success": True,
                "content_ideas": content_ideas,  # Mantenido vacío por compatibilidad
                "content_text": content_text,
                "message": "✅ Respuesta generada.",
                "debug": debug,
            }

        except Exception as e:
            return {
                "success": False,
                "content_ideas": [],
                "message": f"Error al generar contenido: {str(e)}"
            }

    def _extract_requested_numbers(self, message: str) -> list[int]:
        """
        Extrae números de ideas referenciadas (ej: "la 3 y la 4", "2,3", "idea 5").
        """
        text = (message or "").lower()
        # Captura números aislados pero evita años (2025, 2026) limitando a 1-2 dígitos
        nums = re.findall(r"\b(\d{1,2})\b", text)
        out: list[int] = []
        for n in nums:
            try:
                v = int(n)
                if 1 <= v <= 20:
                    out.append(v)
            except ValueError:
                continue
        # Mantener orden y únicos
        seen: set[int] = set()
        uniq: list[int] = []
        for v in out:
            if v not in seen:
                uniq.append(v)
                seen.add(v)
        return uniq

    def _is_refine_request(self, message: str) -> bool:
        """
        Detecta follow-ups del tipo: "desarrolla los diálogos de la 3 y la 4".
        """
        text = (message or "").strip().lower()
        if not text:
            return False
        refine_verbs = r"(desarrolla(me)?|detalla|profundiza|expande|contin[uú]a|guion|guiones|di[aá]logo|di[aá]logos|script)"
        has_refine = re.search(rf"\b{refine_verbs}\b", text) is not None
        has_numbers = re.search(r"\b\d{1,2}\b", text) is not None
        return has_refine and has_numbers

    def _select_mode(self, message: str, is_refine: bool) -> str:
        """
        Decide el modo de respuesta.
        
        TAREA 6.2: Simplificado - siempre retorna 'markdown' para flexibilidad.
        El modo ideas_json fue eliminado para permitir respuestas en Markdown puro.
        """
        # TAREA 6.2: Siempre markdown para máxima flexibilidad
        # Eliminado: lógica de ideas_json que forzaba estructura rígida
        return "markdown"

    async def _build_system_prompt(
        self,
        context: dict,
        project_id: UUID,
        mode: str = "ideas",
        requested_numbers: list[int] | None = None,
    ) -> tuple[str, dict[str, Any]]:
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
            mode: "ideas" (default) o "refine" (expandir ideas previas)
            requested_numbers: lista de números de ideas a expandir si mode="refine"

        Returns:
            Complete system prompt string
        """
        # 1. Get training summary (cacheado, siempre disponible)
        cache_hit = False
        # Best-effort: detect cache hit by calling twice is bad, so infer from log is enough.
        # We'll set cache_hit later via hash stability in Trace; for now leave explicit field.
        training_summary = await self.memory.get_training_summary(project_id)
        prompt_debug: dict[str, Any] = {
            "training_summary_chars": len(training_summary or ""),
            "training_summary_sha": hashlib.sha256((training_summary or "").encode("utf-8")).hexdigest()[:12],
            "training_summary_cache_hit": cache_hit,
        }

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

        # 7. TAREA 5: Format learned concepts from books
        # MEJORADO: Presentación más clara y enfática para que el LLM las use
        learned_concepts = context.get("learned_concepts", [])
        learned_concepts_text = ""
        if learned_concepts:
            learned_concepts_text = "\n⚠️ IMPORTANTE: DEBES aplicar estas técnicas en tu respuesta:\n"
            for i, concept in enumerate(learned_concepts[:5], 1):  # Aumentado a 5
                book_title = concept.get('book_title', 'Libro')
                main_concepts = concept.get('main_concepts', [])
                condensed = concept.get('condensed_text', '')[:500]  # Aumentado de 400 a 500
                terms = concept.get('technical_terms', {})
                
                learned_concepts_text += f"\n📚 [{i}] DE '{book_title}':"
                if main_concepts:
                    learned_concepts_text += f"\n   🎯 TÉCNICAS A APLICAR: {', '.join(main_concepts[:5])}"
                if condensed:
                    learned_concepts_text += f"\n   📝 Contexto: {condensed}"
                if terms:
                    terms_str = "; ".join(f"**{k}**: {v}" for k, v in list(terms.items())[:4])
                    learned_concepts_text += f"\n   📖 Definiciones: {terms_str}"
        else:
            learned_concepts_text = "No hay conocimiento de libros procesados aún."

        # --- Prompt base (TAREA 6.2: unificado para Markdown) ---
        base_prompt = """## TU ROL Y CAPACIDADES:

Eres un estratega de marketing digital especializado en contenido para redes sociales.

## TU METODOLOGÍA DE TRABAJO:

PASO 1: Entender la petición (qué servicio necesita y nivel de detalle)
PASO 2: Analizar contexto (buyer persona, pain points, journey, técnicas de entrenamiento)
PASO 3: Aplicar expertise (específico, accionable, no genérico)
PASO 4: Entregar valor (formato adecuado a la petición)

## PRINCIPIOS:
✅ especificidad, accionabilidad, fundamentación, versatilidad, memoria
❌ evita genérico e ignorar contexto
"""

        # TAREA 6.2: Formato unificado Markdown
        format_section = """## FORMATO DE RESPUESTA (Markdown):

Responde en **Markdown estructurado**. Elige el formato más apropiado:

### Para ideas de contenido (si piden ideas/hooks/posts):
Usa esta estructura para CADA idea:

**1. [Título descriptivo]** (Plataforma)
- 🎣 **Hook:** [Aplica técnicas del CONOCIMIENTO DE LIBROS proporcionado arriba]
- 📋 **Estructura:** [Desarrollo del contenido]
- 📢 **CTA:** [Call-to-action específico]
- 💡 **Técnica aplicada:** [NOMBRA la técnica específica Y el libro de donde viene]
- 🗣️ **Guion/Diálogo completo:**
  > [Texto completo listo para grabar]

### REGLAS:
1. USA las técnicas del CONOCIMIENTO DE LIBROS proporcionado arriba
2. NOMBRA la técnica y el libro de donde viene
3. CONECTA con el buyer persona y sus pain points
4. SÉ ESPECÍFICO - evita respuestas genéricas
5. Incluye guion completo listo para usar
"""

        # TAREA 6.2: Prompt unificado sin condicionales de modo
        system_prompt = f"""{base_prompt}

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

## CONOCIMIENTO APRENDIDO DE LIBROS (conceptos extraídos):
{learned_concepts_text}

## TU ESTILO Y ENFOQUE:

- APLICA las técnicas del CONOCIMIENTO DE LIBROS proporcionado arriba
- NOMBRA la técnica y su libro de origen cuando la uses
- ADAPTA al buyer persona (usa su lenguaje, menciona sus problemas)
- GENERA contenido completo y accionable
- Sé específico, evita respuestas genéricas
- Mantén conversación natural, recuerda contexto previo

{format_section}"""

        return system_prompt, prompt_debug

    def _parse_content_response(self, response: str) -> tuple[list[dict], int]:
        """
        Parse LLM response (JSON or markdown) and extract tecnicas_aplicadas.

        Args:
            response: LLM response

        Returns:
            Tuple of (list of content ideas, total tecnicas_aplicadas_count)
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
            ideas: list[dict[str, Any]] = []
            if isinstance(data, dict) and "ideas" in data:
                ideas_raw = data["ideas"]
                if isinstance(ideas_raw, list) and len(ideas_raw) > 0:
                    ideas = cast(list[dict[str, Any]], ideas_raw)
                else:
                    logger.warning(f"No ideas found in JSON response: {data}")
                    return ([{"titulo": "Idea generada", "contenido": response_clean}], 0)
            elif isinstance(data, list) and len(data) > 0:
                ideas = cast(list[dict[str, Any]], data)
            else:
                # Fallback: return as single idea
                logger.warning(f"Unexpected JSON structure: {type(data)}")
                return ([{"titulo": "Idea generada", "contenido": response_clean}], 0)

            # Validate and count tecnicas_aplicadas
            total_tecnicas = 0
            unique_tecnicas: set[str] = set()
            for idx, idea in enumerate(ideas):
                if not isinstance(idea, dict):
                    continue
                tecnicas = idea.get("tecnicas_aplicadas")
                if tecnicas is None:
                    logger.warning(f"Idea {idx + 1} missing 'tecnicas_aplicadas' field")
                    # Set empty array if missing (don't fail, but log)
                    idea["tecnicas_aplicadas"] = []
                elif isinstance(tecnicas, list):
                    # Normalize: ensure all items are strings
                    tecnicas_clean = [str(t).strip().lower() for t in tecnicas if t]
                    idea["tecnicas_aplicadas"] = tecnicas_clean
                    total_tecnicas += len(tecnicas_clean)
                    unique_tecnicas.update(tecnicas_clean)
                else:
                    logger.warning(f"Idea {idx + 1} has invalid 'tecnicas_aplicadas' type: {type(tecnicas)}")
                    idea["tecnicas_aplicadas"] = []

            logger.info(f"Parsed {len(ideas)} ideas with {total_tecnicas} total técnicas ({len(unique_tecnicas)} unique)")
            return (ideas, total_tecnicas)
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
                            ideas_fallback = cast(list[dict[str, Any]], data["ideas"])
                            # Validate tecnicas_aplicadas
                            total_tecnicas = 0
                            for idea in ideas_fallback:
                                if isinstance(idea, dict):
                                    tecnicas = idea.get("tecnicas_aplicadas", [])
                                    if isinstance(tecnicas, list):
                                        total_tecnicas += len([t for t in tecnicas if t])
                                    else:
                                        idea["tecnicas_aplicadas"] = []
                            return (ideas_fallback, total_tecnicas)
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
                            ideas_fallback = cast(list[dict[str, Any]], data["ideas"])
                            # Validate tecnicas_aplicadas
                            total_tecnicas = 0
                            for idea in ideas_fallback:
                                if isinstance(idea, dict):
                                    tecnicas = idea.get("tecnicas_aplicadas", [])
                                    if isinstance(tecnicas, list):
                                        total_tecnicas += len([t for t in tecnicas if t])
                                    else:
                                        idea["tecnicas_aplicadas"] = []
                            return (ideas_fallback, total_tecnicas)
                    except json.JSONDecodeError:
                        pass

            # Final fallback: return as markdown text
            logger.error("Could not parse response as JSON. Returning raw content.")
            return ([{"titulo": "Ideas de contenido", "contenido": response_clean, "tecnicas_aplicadas": []}], 0)
