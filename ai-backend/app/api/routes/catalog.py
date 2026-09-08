from fastapi import APIRouter, Depends, Form, UploadFile, File, Body
from typing import Annotated, Optional
from pydantic import BaseModel

from app.schemas.product import Product
from app.schemas.common import APISuccessResponse
from app.schemas.catalog import CatalogResponse
from app.api.dependencies import get_ai_orchestrator
from app.ai.orchestrator import AIOrchestrator
from app.core.exceptions import InvalidInputException
from app.core.logging import logger

router = APIRouter()

@router.post("/generate", response_model=APISuccessResponse)
async def generate_catalog(
    artisan_id: Annotated[str, Form(...)],
    text_description: Annotated[Optional[str], Form()] = None,
    image: Annotated[Optional[UploadFile], File()] = None,
    voice: Annotated[Optional[UploadFile], File()] = None,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    if not text_description and not image and not voice:
        raise InvalidInputException("Must provide at least one of: text_description, image, or voice.")

    image_data = await image.read() if image else None
    voice_data = await voice.read() if voice else None

    product: Product = await orchestrator.process_product(
        artisan_id=artisan_id,
        image_data=image_data,
        voice_data=voice_data,
        text_description=text_description
    )
    
    return APISuccessResponse(data=product)

# --- Phase 2 Endpoints ---

ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp3", "audio/m4a", "audio/mp4", "audio/ogg", "audio/webm"]
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/from-voice", response_model=CatalogResponse)
async def catalog_from_voice(
    audio: Annotated[UploadFile, File(...)],
    language_preference: Annotated[Optional[str], Form()] = None,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    if not audio:
        raise InvalidInputException("Audio file is required.")
        
    # Validate MIME type loosely, some clients send generic application/octet-stream
    if audio.content_type not in ALLOWED_AUDIO_TYPES and not audio.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.ogg', '.webm')):
        logger.warning(f"Unsupported audio format: {audio.content_type} / {audio.filename}")
        raise InvalidInputException(f"Unsupported audio format: {audio.content_type}")

    # Read and check size
    audio_bytes = await audio.read()
    if len(audio_bytes) == 0:
        raise InvalidInputException("Empty audio file.")
    if len(audio_bytes) > MAX_AUDIO_SIZE:
        raise InvalidInputException("Audio file too large. Max size is 10MB.")

    data = await orchestrator.process_voice_catalog(audio_bytes, audio.filename)
    return CatalogResponse(success=True, data=data)


class TextCatalogRequest(BaseModel):
    text: str
    language: Optional[str] = None

@router.post("/from-text", response_model=CatalogResponse)
async def catalog_from_text(
    request: TextCatalogRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    if not request.text or not request.text.strip():
        raise InvalidInputException("Text is required.")

    data = await orchestrator.process_text_catalog(request.text)
    return CatalogResponse(success=True, data=data)
