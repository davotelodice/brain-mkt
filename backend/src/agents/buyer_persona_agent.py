"""Buyer Persona Agent - Generates complete buyer persona analysis (40+ questions)."""

import json
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
        Generate complete buyer persona.

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

        # 2. Build prompt with complete template
        prompt = self._build_buyer_persona_prompt(
            user_message=user_message,
            relevant_docs=context['relevant_docs']
        )

        # 3. Generate buyer persona (this will take ~20-30s)
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system="Eres un experto en marketing digital especializado en crear buyer personas ULTRA DETALLADAS. SIEMPRE responde en formato JSON válido.",
                max_tokens=8000,
                temperature=0.7
            )

            # 4. Clean response (remove markdown code blocks if present)
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]  # Remove ```json
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]  # Remove ```
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]  # Remove closing ```
            response_clean = response_clean.strip()

            # 5. Parse JSON response
            if not response_clean:
                raise json.JSONDecodeError("Empty response from LLM", response, 0)

            buyer_persona_data = json.loads(response_clean)

            # 5. Save to database
            # TODO: Parse buyer_persona_data and distribute across correct columns
            # For MVP, saving everything in full_analysis
            buyer_persona = MarketingBuyerPersona(
                chat_id=chat_id,
                project_id=project_id,
                initial_questions={},  # TODO: Extract from buyer_persona_data
                full_analysis=buyer_persona_data,  # Complete buyer persona
                forum_simulation={},  # TODO: Extract from buyer_persona_data
                pain_points={},  # TODO: Extract from buyer_persona_data
                customer_journey={}  # TODO: Extract from buyer_persona_data
            )

            self.db.add(buyer_persona)
            await self.db.commit()

            return {
                "success": True,
                "buyer_persona": buyer_persona_data,
                "message": "Buyer persona generado exitosamente con 40+ preguntas respondidas."
            }

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "buyer_persona": None,
                "message": f"Error al parsear respuesta del LLM: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "buyer_persona": None,
                "message": f"Error al generar buyer persona: {e}"
            }

    def _build_buyer_persona_prompt(
        self,
        user_message: str,
        relevant_docs: list[dict]
    ) -> str:
        """
        Build complete prompt with buyer persona template.

        Args:
            user_message: User's context about their business
            relevant_docs: Relevant documents from RAG

        Returns:
            Complete prompt string
        """
        # Format relevant documents
        docs_text = "\n\n".join([
            f"Documento: {doc['source_title']}\n{doc['content']}"
            for doc in relevant_docs
        ]) if relevant_docs else "No hay documentos adicionales."

        prompt = f"""
Eres un experto en marketing digital especializado en crear buyer personas ULTRA DETALLADAS.

Tu trabajo es analizar la información del usuario y generar un buyer persona completo siguiendo la plantilla de 11 categorías con 40+ preguntas.

## INFORMACIÓN DEL USUARIO:
{user_message}

## DOCUMENTOS ADICIONALES:
{docs_text}

## PLANTILLA DE BUYER PERSONA:

Debes responder TODAS las siguientes preguntas organizadas en 11 categorías:

### 1. Aspectos Demográficos (6 preguntas)
- Nombre (inventa uno realista)
- Edad
- Nivel de estudios
- Ingresos aproximados anuales
- Ubicación geográfica (ciudad/país)
- Estado civil

### 2. Hogar y Familia (3 preguntas)
- ¿Cuántas personas viven en su hogar? ¿Con quién vive?
- ¿Qué hace en su tiempo libre? ¿Cuáles son sus hobbies?
- ¿Qué responsabilidades familiares tiene?

### 3. Trabajo (3 preguntas)
- ¿Dónde trabaja? (industria, tipo de empresa, cargo)
- ¿Cuáles son sus mayores retos laborales? ¿Qué le frustra del trabajo?
- ¿Cómo equilibra vida laboral vs personal?

### 4. Comportamiento (2 preguntas)
- ¿Cómo son sus relaciones interpersonales? ¿Con quién interactúa más?
- ¿Qué expresiones y lenguaje específico usa su grupo social? (jerga, términos técnicos)

### 5. Problema (2 preguntas)
- ¿Qué dolor o necesidad específica activa su búsqueda de solución?
- ¿Cómo tu producto/servicio soluciona ese problema? (sé específico)

### 6. Búsqueda de la Solución (3 preguntas)
- ¿Dónde busca información? (Google, redes sociales, foros, amigos)
- ¿Cómo te encuentra? (SEO, anuncios, recomendaciones, influencers)
- ¿Cómo reacciona a mensajes comerciales? (escéptico, receptivo, ignorante)

### 7. Objeciones y Barreras (2 preguntas)
- ¿Qué barreras le impiden comprar? (precio, confianza, tiempo, competencia)
- ¿Qué excusas usa para no decidirse? ("lo pensaré", "está caro", etc.)

### 8. Miedos e Inseguridades (2 preguntas)
- ¿Qué odia encontrar en productos/servicios similares? (sus pesadillas)
- ¿Qué experiencias negativas previas ha tenido con soluciones similares?

### 9. Comparación con Competencia (5 preguntas)
- ¿Qué factores compara entre diferentes opciones? (precio, calidad, soporte)
- ¿Qué diferencias encuentra entre competidores?
- ¿Qué hace mejor la competencia?
- ¿Qué haces mejor tú?
- ¿Por qué te elige a ti finalmente? (factor decisivo)

### 10. Tu Producto o Servicio (4 preguntas)
- ¿Qué beneficios percibe claramente de tu producto?
- ¿Qué beneficios NO percibe pero existen? (valor oculto que debes comunicar)
- ¿Qué productos complementarios podría necesitar?
- ¿Qué dudas tiene post-compra? (uso, soporte, renovación)

### 11. Información Adicional Relevante
- Cualquier dato específico del contexto que sea relevante y no entre en categorías anteriores

## INSTRUCCIONES CRÍTICAS:

1. **COMPLETO**: Debes responder TODAS las preguntas. No puedes saltarte ninguna.
2. **REALISTA**: Basa tus respuestas en la información proporcionada.
3. **COHERENTE**: Todas las respuestas deben ser coherentes entre sí (crear una persona real).
4. **ESPECÍFICO**: Usa detalles concretos, no generalidades vagas.
5. **INFERENCIA**: Si falta información, infiere basado en contexto lógico del negocio.
6. **FORMATO JSON**: Respuesta en JSON estructurado siguiendo el ejemplo.

## EJEMPLO DE RESPUESTA ESPERADA (caso "Ana" - Enfermera preparando EIR):

{{
  "aspectos_demograficos": {{
    "nombre": "Ana",
    "edad": 35,
    "nivel_estudios": "Grado en Enfermería",
    "ingresos": "35000",
    "ubicacion": "Barcelona, España",
    "estado_civil": "Soltera"
  }},
  "hogar_familia": {{
    "integrantes_hogar": "Vive sola en piso alquilado, visita a padres los fines de semana",
    "tiempo_libre": "Lee novelas, hace yoga 2 veces por semana, sale con amigas enfermeras los viernes",
    "responsabilidades": "Cuidar ocasionalmente de su madre (diabética), pagar alquiler 800€/mes"
  }},
  "trabajo": {{
    "donde_trabaja": "Hospital público en Barcelona (contratos temporales 6 meses), turno rotatorio",
    "retos_laborales": "Inestabilidad laboral genera ansiedad, turnos rotatorios agotadores impiden vida social, falta de plaza fija",
    "vida_laboral_personal": "Muy difícil planificar vida personal con turnos cambiantes, no puede comprometerse a actividades regulares"
  }},
  "comportamiento": {{
    "relaciones": "Grupo cercano de 5 compañeras enfermeras, activa en foros de EIR en Facebook, interactúa en grupos de WhatsApp",
    "lenguaje": "Usa términos como 'EIRsilente', 'rEIRsilente', 'temario mil hojas', 'OPE', 'plaza fija', 'eventual'"
  }},
  "problema": {{
    "dolor": "Ansiedad constante por inestabilidad laboral, cansancio extremo de turnos, miedo a no conseguir plaza fija antes de los 40, presión familiar por estabilidad",
    "solucion": "Preparar examen EIR para conseguir especialidad (mejor pagada, más prestigio) y plaza fija en hospital público que le dé estabilidad económica y emocional"
  }},
  "busqueda_solucion": {{
    "donde_busca": "Grupos privados de Facebook 'Enfermeras EIR 2026', foros en enfermeria21.com, Instagram de academias, YouTube con experiencias de aprobados, pregunta a compañeras que aprobaron",
    "como_te_encuentra": "Anuncios segmentados en Facebook/Instagram 'Enfermeras 30-40 años Barcelona', búsquedas Google 'mejor academia EIR online', recomendaciones en grupos",
    "reaccion_comercial": "Muy escéptica de promesas vacías, busca DATOS REALES de tasa de aprobados, lee todos los comentarios negativos antes que positivos, desconfía de academias nuevas sin trayectoria"
  }},
  "objeciones": {{
    "barreras": "Precio alto academias prestigiosas (2000-3000€), miedo a invertir y no aprobar, falta de tiempo por turnos agotadores, comparación con academia barata que usó amiga",
    "excusas": "'Empiezo el próximo mes cuando tenga turnos mejores', 'Este año solo investigo opciones', 'Está muy caro, esperaré oferta', 'No sé si realmente necesito academia o puedo sola'"
  }},
  "miedos": {{
    "que_odia": "Academias con material desactualizado (examen cambia cada año), sin soporte personalizado, grupos masivos donde no te conocen, plataformas complicadas de usar después de turno nocturno",
    "experiencias_negativas": "Compró curso online barato (500€) en 2023 que nadie actualizaba, PDFs desorganizados, dudas sin responder, se sintió estafada y desmotivada"
  }},
  "comparacion_competencia": {{
    "factores_comparacion": "Precio vs calidad, tasa real de aprobados (no promesas), flexibilidad horaria para turnos, actualización de temario, soporte 24/7, comunidad activa",
    "diferencias": "Academia X (líder): 3000€, 78% aprobados, presencial Barcelona. Academia Y: 1500€, online, sin datos públicos. Academia Z: 2200€, semi-presencial, 65% aprobados",
    "mejor_competencia": "Academia X tiene 15 años trayectoria, estadísticas públicas verificables, profesores que son tribunal del examen",
    "mejor_tu": "Flexibilidad total 100% online, soporte WhatsApp 24/7, precio intermedio 1800€, comunidad muy activa con estudios grupales virtuales, material actualizado semanalmente",
    "por_que_te_elige": "Puede estudiar después de turnos nocturnos sin horarios fijos, precio razonable con pago en cuotas, grupo WhatsApp activo la hace sentir acompañada, testimonios de enfermeras como ella que aprobaron"
  }},
  "tu_producto": {{
    "beneficios_percibidos": "Flexibilidad horaria total, material siempre actualizado, comunidad de apoyo WhatsApp, simulacros cada mes, precio más accesible que líder",
    "beneficios_no_percibidos": "Networking con otras enfermeras especialistas que pueden recomendar hospitales, orientación laboral post-EIR sobre dónde aplicar, acceso a bolsa de trabajo exclusiva de especialistas",
    "productos_complementarios": "Simulacros extra premium (10€/mes), masterclasses con tribunales del examen (50€), revisión personalizada de exámenes (100€), mentoría 1-1 con especialista (200€)",
    "dudas_post_compra": "'¿El temario cubre TODO el examen oficial?', '¿Y si no apruebo, puedo repetir gratis?', '¿Cuánto tiempo debo estudiar al día?', '¿La comunidad seguirá activa después del examen?'"
  }},
  "info_adicional": "Ana prefiere formato 100% digital (no quiere cargar libros al hospital), muy activa en Instagram (sigue #EnfermeraEIR #OPEEnfermeria), confía más en testimonios de personas reales que en publicidad, tiene cuenta premium de Spotify para estudiar con música, usa Notion para organizar apuntes"
}}

## TU RESPUESTA:

Genera el buyer persona completo en formato JSON siguiendo la estructura del ejemplo de Ana.
Recuerda: TODAS las preguntas deben ser respondidas, NO puedes saltarte ninguna.
"""

        return prompt
