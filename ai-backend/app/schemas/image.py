from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ImageQualityMetrics(BaseModel):
    quality_score: float = Field(ge=0, le=100)
    resolution: Dict[str, int]
    brightness: float
    sharpness: float
    contrast: float
    blur_detected: bool
    background_clutter: bool
    recommendations: List[str]

class VisionAttribute(BaseModel):
    name: str
    value: Any
    confidence: float
    source: str = "vision"

class VisionAnalysis(BaseModel):
    objects: List[Dict[str, Any]] = []
    attributes: List[VisionAttribute] = []
    category: Optional[str] = None
    background_type: Optional[str] = None

class ImageConflict(BaseModel):
    field: str
    catalog_value: Any
    vision_value: Any
    confidence: float
    requires_confirmation: bool = True

class ImageMetadata(BaseModel):
    image_id: str
    product_id: Optional[str] = None
    original_filename: str
    width: int
    height: int
    format: str
    file_size: int
    quality_score: float
    processing_status: str
    processing_time: float
    model_provider: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ImageProcessResponseData(BaseModel):
    product_id: Optional[str] = None
    original_image: str
    processed_image: Optional[str] = None
    quality: ImageQualityMetrics
    background: Dict[str, Any]
    vision_attributes: Dict[str, Any]
    conflicts: List[ImageConflict] = []
    metadata: ImageMetadata

class ImageProcessResponse(BaseModel):
    success: bool
    data: ImageProcessResponseData
