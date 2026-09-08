from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ArtisanProfile(BaseModel):
    artisan_id: str
    name: str
    region: str
    languages: List[str] = []
    crafts: List[str] = []
    materials: List[str] = []
    categories: List[str] = []
    available_quantity: int = 0
    minimum_order_quantity: int = 1
    maximum_order_quantity: Optional[int] = None
    average_lead_time_days: int = 7
    customization_supported: bool = False
    customization_types: List[str] = []
    quality_score: float = 0.0
    price_range: Optional[List[float]] = None
    reliability_score: Optional[float] = None # None means new artisan
    profile_completeness: float = 0.0
    active: bool = True
    product_ids: List[str] = []
