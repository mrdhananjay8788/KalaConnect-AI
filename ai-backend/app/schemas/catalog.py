from pydantic import BaseModel, Field
from typing import List, Optional, Any
from app.schemas.product import ProductDescription

class MissingFieldInfo(BaseModel):
    field: str
    importance: str = Field(description="high, medium, or low")

class ProductExtraction(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    craft_type: Optional[str] = None
    material: List[str] = []
    color: List[str] = []
    pattern: Optional[str] = None
    dimensions: Optional[dict] = None
    weight: Optional[float] = None
    region: Optional[str] = None
    production_method: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    customization: Optional[str] = None
    intended_use: Optional[str] = None
    cultural_significance: Optional[str] = None
    source_language: Optional[str] = None
    confidence: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    missing_fields: List[str] = []

class TranscriptionResult(BaseModel):
    text: str
    language: str
    confidence: float

class CatalogResponseData(BaseModel):
    transcription: Optional[TranscriptionResult] = None
    product: dict
    descriptions: ProductDescription
    keywords: List[str]
    missing_fields: List[MissingFieldInfo]
    next_question: Optional[str] = None

class CatalogResponse(BaseModel):
    success: bool
    data: CatalogResponseData
