from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated
from pydantic import BaseModel

from app.api.dependencies import get_matching_engine
from app.services.matching_engine import MatchingEngine
from app.schemas.matching import MatchResponse, MatchPreviewResponse

router = APIRouter()

class MatchRequestPayload(BaseModel):
    query: str
    quantity: int = None
    budget_max: float = None
    delivery_location: str = None
    required_delivery_days: int = None
    allow_split_order: bool = False

@router.post("/preview", response_model=MatchPreviewResponse)
async def preview_matches(
    payload: MatchRequestPayload,
    engine: MatchingEngine = Depends(get_matching_engine)
):
    """Preview matches for UI."""
    data = await engine.preview_matches(payload.query)
    return MatchPreviewResponse(success=True, data=data)

@router.post("/buyers", response_model=MatchResponse)
async def get_buyers_matches(
    payload: MatchRequestPayload,
    engine: MatchingEngine = Depends(get_matching_engine)
):
    """Get full artisan matches based on B2B query."""
    data = await engine.find_matches(payload.query, allow_split=payload.allow_split_order)
    return MatchResponse(success=True, data=data)

@router.get("/{request_id}")
async def get_match_request(
    request_id: str
):
    """Mock endpoint to retrieve past matching request."""
    return {"success": True, "message": f"Retrieved request {request_id}"}
