from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.dependencies import get_pricing_engine
from app.services.pricing_engine import PricingEngine
from app.schemas.pricing import PricingRequest, PricingResponse, PricingSimulationRequest, PricingSimulationResponse

router = APIRouter()

@router.post("/suggest", response_model=PricingResponse)
async def suggest_price(
    request: PricingRequest,
    pricing_engine: Annotated[PricingEngine, Depends(get_pricing_engine)]
):
    """Generate an explainable, data-driven price recommendation."""
    pricing_data = await pricing_engine.suggest_price(request)
    return PricingResponse(success=True, data=pricing_data)

@router.post("/simulate", response_model=PricingSimulationResponse)
async def simulate_price(
    request: PricingSimulationRequest,
    pricing_engine: Annotated[PricingEngine, Depends(get_pricing_engine)]
):
    """Simulate what-if scenarios for pricing."""
    sim_data = pricing_engine.simulate_price(request)
    return PricingSimulationResponse(success=True, data=sim_data)
