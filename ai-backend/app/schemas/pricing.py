from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

class PricingRequest(BaseModel):
    product_id: str
    product_category: Optional[str] = None
    subcategory: Optional[str] = None
    craft_type: Optional[str] = None
    materials: List[str] = []
    
    # Cost inputs
    material_cost: float = Field(default=0.0, ge=0.0)
    labor_cost: Optional[float] = Field(default=None, ge=0.0)
    labor_hours: Optional[float] = Field(default=None, ge=0.0)
    production_cost: float = Field(default=0.0, ge=0.0)
    packaging_cost: float = Field(default=0.0, ge=0.0)
    transportation_cost: float = Field(default=0.0, ge=0.0)
    
    region: Optional[str] = None
    product_quality_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    customization_level: str = "none" # none, low, medium, high
    artisan_requested_price: Optional[float] = Field(default=None, ge=0.0)
    quantity: int = Field(default=1, ge=1)
    
    historical_sales: List[Dict[str, Any]] = []
    market_reference_prices: List[float] = []
    
    desired_margin: float = Field(default=0.25, ge=0.0, le=1.0)

class MarketDataStats(BaseModel):
    sample_size: int
    median: float
    mean: float
    min: float
    max: float
    range: List[float]

class CostBreakdown(BaseModel):
    material: float
    labor: float
    packaging: float
    transportation: float
    production: float
    total_base_cost: float

class PricingExplanation(BaseModel):
    cost_basis: str
    market_basis: str
    labor_contribution: str
    recommended_margin: str
    final_reason: str

class ArtisanMessage(BaseModel):
    english: str
    hindi: str
    marathi: str

class PricingResponseData(BaseModel):
    minimum_price: float
    recommended_price: float
    maximum_price: float
    confidence: float
    confidence_level: str
    market_data: Optional[MarketDataStats] = None
    cost_breakdown: CostBreakdown
    explanation: PricingExplanation
    artisan_message: ArtisanMessage

class PricingResponse(BaseModel):
    success: bool
    data: PricingResponseData

class HistoricalSale(BaseModel):
    product_id: str
    date: date
    quantity: int = Field(ge=1)
    selling_price: float = Field(ge=0.0)
    region: str
    buyer_type: str = "retail"
    discount: float = Field(default=0.0, ge=0.0, le=1.0)
    total_revenue: float = Field(ge=0.0)

class PricingSimulationRequest(BaseModel):
    product_id: str
    selling_price: float = Field(ge=0.0)
    material_cost: float = Field(default=0.0, ge=0.0)
    labor_cost: Optional[float] = Field(default=None, ge=0.0)
    labor_hours: Optional[float] = Field(default=None, ge=0.0)
    packaging_cost: float = Field(default=0.0, ge=0.0)
    transportation_cost: float = Field(default=0.0, ge=0.0)

class PricingSimulationResponseData(BaseModel):
    selling_price: float
    estimated_cost: float
    estimated_profit: float
    margin: float
    market_position: str # "too_low", "competitive", "premium"

class PricingSimulationResponse(BaseModel):
    success: bool
    data: PricingSimulationResponseData
