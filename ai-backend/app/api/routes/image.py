from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Annotated, Optional

from app.api.dependencies import get_image_service
from app.services.image_service import ImageService
from app.schemas.common import APISuccessResponse
from app.schemas.image import ImageProcessResponse

router = APIRouter()

@router.post("/analyze")
async def analyze_image(
    image: Annotated[UploadFile, File(...)],
    image_service: ImageService = Depends(get_image_service)
):
    """Analyze image quality and vision attributes."""
    image_bytes = await image.read()
    result = await image_service.analyze_image_only(image_bytes, image.filename, image.content_type)
    return APISuccessResponse(data=result)

@router.post("/process", response_model=ImageProcessResponse)
async def process_image(
    image: Annotated[UploadFile, File(...)],
    product_id: Annotated[Optional[str], Form()] = None,
    image_service: ImageService = Depends(get_image_service)
):
    """Run the complete image enhancement and vision pipeline."""
    image_bytes = await image.read()
    data = await image_service.process_image_pipeline(
        image_bytes, 
        image.filename, 
        image.content_type, 
        product_id
    )
    return ImageProcessResponse(success=True, data=data)

@router.post("/quality")
async def check_image_quality(
    image: Annotated[UploadFile, File(...)],
    image_service: ImageService = Depends(get_image_service)
):
    """Check image quality using basic metrics."""
    image_bytes = await image.read()
    image_service.validate_image(image_bytes, image.filename, image.content_type)
    quality = image_service.analyze_quality(image_bytes)
    return APISuccessResponse(data=quality.model_dump())

@router.post("/remove-background")
async def remove_background(
    image: Annotated[UploadFile, File(...)],
    image_service: ImageService = Depends(get_image_service)
):
    """Remove background and return transparent PNG path."""
    image_bytes = await image.read()
    path = await image_service.remove_background_only(image_bytes, image.filename, image.content_type)
    return APISuccessResponse(data={"processed_image": path.replace("\\", "/")})
