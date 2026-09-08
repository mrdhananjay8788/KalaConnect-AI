from fastapi import APIRouter, Depends, UploadFile, File
from typing import Annotated

from app.api.dependencies import get_speech_provider
from app.ai.speech.base import BaseSpeechProvider
from app.schemas.common import APISuccessResponse

router = APIRouter()

@router.post("/transcribe", response_model=APISuccessResponse)
async def transcribe_voice(
    voice: Annotated[UploadFile, File(...)],
    speech_provider: BaseSpeechProvider = Depends(get_speech_provider)
):
    voice_data = await voice.read()
    text = await speech_provider.transcribe(voice_data)
    
    return APISuccessResponse(data={"transcription": text})
