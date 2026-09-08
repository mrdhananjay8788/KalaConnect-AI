from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class BuyerMatchRequest(BaseModel):
    request_id: Optional[str] = None
    buyer_id: Optional[str] = None
    query: str
    product_category: Optional[str] = None
    product_name: Optional[str] = None
    craft_type: Optional[str] = None
    materials: List[str] = []
    quantity: Optional[int] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    delivery_location: Optional[str] = None
    required_delivery_date: Optional[datetime] = None
    required_delivery_days: Optional[int] = None
    customization_required: bool = False
    customization_description: Optional[str] = None
    quality_requirements: Optional[str] = None
    preferred_region: Optional[str] = None
    preferred_language: Optional[str] = None
    allow_split_order: bool = False
    minimum_quality_score: Optional[float] = None

class ArtisanMatchResult(BaseModel):
    artisan_id: str
    product_id: Optional[str] = None
    match_score: float
    confidence: float
    confidence_level: str
    semantic_score: float
    quantity_score: float
    price_score: float
    delivery_score: float
    customization_score: float
    region_score: float
    reliability_score: float
    hard_constraints_passed: bool
    estimated_quantity: int
    estimated_price: Optional[float] = None
    estimated_delivery_days: Optional[int] = None
    explanation: str
    warnings: List[str] = []

class SplitOrderAllocation(BaseModel):
    artisan_id: str
    quantity: int

class SplitOrderResult(BaseModel):
    required_quantity: int
    allocated_quantity: int
    artisans: List[SplitOrderAllocation]

class MatchResponseData(BaseModel):
    request_id: str
    matches: List[ArtisanMatchResult]
    split_order_option: Optional[SplitOrderResult] = None

class MatchResponse(BaseModel):
    success: bool
    data: MatchResponseData

class MatchPreviewData(BaseModel):
    eligible_artisans: int
    high_quality_matches: int
    budget_compatible: int
    capacity_compatible: int
    delivery_compatible: int

class MatchPreviewResponse(BaseModel):
    success: bool
    data: MatchPreviewData
