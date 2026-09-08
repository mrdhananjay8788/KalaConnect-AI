from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SearchFilters(BaseModel):
    category: Optional[str] = None
    material: List[str] = []
    craft_type: Optional[str] = None
    region: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    quantity: Optional[int] = None
    intended_use: Optional[str] = None

class QueryUnderstanding(BaseModel):
    original: str
    normalized: str
    language: str
    intent: str
    semantic_query: str

class SearchResult(BaseModel):
    product_id: str
    product_name: str
    price: float
    availability: int
    similarity: float
    relevance_score: float
    match_reasons: List[str] = []

class SearchQuery(BaseModel):
    query: str
    language: str
    category: Optional[str] = None
    materials: List[str] = []
    craft_type: Optional[str] = None
    region: Optional[str] = None
    color: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    quantity: Optional[int] = None
    intended_use: Optional[str] = None
    buyer_type: Optional[str] = None
    semantic_query: str

class SearchResponseData(BaseModel):
    query: QueryUnderstanding
    filters: SearchFilters
    results: List[SearchResult]
    total_results: int
    is_alternative: bool = False
    message: Optional[str] = None

class SearchResponse(BaseModel):
    success: bool
    data: SearchResponseData

class SimilarProduct(BaseModel):
    product_id: str
    similarity: float

class SimilarProductResponseData(BaseModel):
    products: List[SimilarProduct]

class SimilarProductResponse(BaseModel):
    success: bool
    data: SimilarProductResponseData

class SearchSuggestionResponse(BaseModel):
    success: bool
    data: List[str]

class SearchEvent(BaseModel):
    query: str
    language: str
    timestamp: datetime
    filters: Dict[str, Any]
    result_count: int
    selected_product_id: Optional[str] = None
    buyer_type: str = "retail"
