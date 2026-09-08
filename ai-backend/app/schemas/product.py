from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProductDescription(BaseModel):
    original: Optional[str] = None
    hindi: Optional[str] = None
    english: Optional[str] = None

class ProductImage(BaseModel):
    original_url: Optional[str] = None
    processed_url: Optional[str] = None
    quality_score: Optional[float] = None

class ProductPricing(BaseModel):
    raw_material_cost: Optional[float] = None
    labor_cost: Optional[float] = None
    suggested_price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    confidence: Optional[float] = None

class AIMetadata(BaseModel):
    model: str
    confidence: Optional[float] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel):
    product_id: str
    artisan_id: str
    
    product_name: str
    category: str
    subcategory: str
    
    craft_type: str
    material: List[str] = []
    color: List[str] = []
    dimensions: Dict[str, Any] = {}
    weight: Optional[float] = None
    
    region: str
    language: str
    
    description: ProductDescription
    keywords: List[str] = []
    
    image: ProductImage
    pricing: ProductPricing
    ai_metadata: AIMetadata
