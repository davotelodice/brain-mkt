"""Pydantic schemas for analysis/buyer persona visualization."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BuyerPersonaResponse(BaseModel):
    id: UUID
    chat_id: UUID
    project_id: UUID
    initial_questions: dict
    full_analysis: dict
    forum_simulation: dict
    pain_points: dict
    customer_journey: dict
    created_at: datetime

    class Config:
        from_attributes = True


class ChatAnalysisResponse(BaseModel):
    buyer_persona: BuyerPersonaResponse | None
    has_buyer_persona: bool
    has_forum_simulation: bool
    has_pain_points: bool
    has_customer_journey: bool

