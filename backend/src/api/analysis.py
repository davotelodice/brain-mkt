"""Analysis API endpoints (buyer persona + derived artifacts)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..db.models import MarketingBuyerPersona, MarketingUser
from ..middleware.auth import get_current_user
from ..schemas.analysis import BuyerPersonaResponse, ChatAnalysisResponse

router = APIRouter(prefix="/api/chats", tags=["analysis"])


async def _get_buyer_persona_or_none(
    db: AsyncSession, chat_id: UUID, project_id: UUID
) -> MarketingBuyerPersona | None:
    result = await db.execute(
        select(MarketingBuyerPersona).where(
            MarketingBuyerPersona.chat_id == chat_id,
            MarketingBuyerPersona.project_id == project_id,
        )
    )
    return result.scalar_one_or_none()


@router.get("/{chat_id}/buyer-persona", response_model=BuyerPersonaResponse)
async def get_buyer_persona(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BuyerPersonaResponse:
    persona = await _get_buyer_persona_or_none(db, chat_id, user.project_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Buyer persona not found for chat")
    return BuyerPersonaResponse.model_validate(persona)


@router.get("/{chat_id}/analysis", response_model=ChatAnalysisResponse)
async def get_chat_analysis(
    chat_id: UUID,
    user: MarketingUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatAnalysisResponse:
    persona = await _get_buyer_persona_or_none(db, chat_id, user.project_id)
    if not persona:
        return ChatAnalysisResponse(
            buyer_persona=None,
            has_buyer_persona=False,
            has_forum_simulation=False,
            has_pain_points=False,
            has_customer_journey=False,
        )

    forum = persona.forum_simulation or {}
    pains = persona.pain_points or {}
    journey = persona.customer_journey or {}

    return ChatAnalysisResponse(
        buyer_persona=BuyerPersonaResponse.model_validate(persona),
        has_buyer_persona=True,
        has_forum_simulation=bool(forum),
        has_pain_points=bool(pains),
        has_customer_journey=bool(journey),
    )

