import asyncio
import tempfile
import os
from openai import AsyncOpenAI
from app.ai.speech.base import BaseSpeechProvider
from app.schemas.catalog import TranscriptionResult
from app.core.config import settings
from app.core.logging import logger

class MockSpeechProvider(BaseSpeechProvider):
    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> TranscriptionResult:
        await asyncio.sleep(1.0)
        # Check size for mock error if empty
        if not audio_bytes:
            raise ValueError("Empty audio")
            
        # Return a mock Marathi text since we are testing Marathi
        return TranscriptionResult(
            text="ही पैठणी साडी आहे. ती रेशमापासून बनवली आहे.",
            language="mr",
            confidence=0.98
        )

class RealSpeechProvider(BaseSpeechProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> TranscriptionResult:
        if not audio_bytes:
            raise ValueError("Empty audio")
            
        logger.info(f"Transcribing audio file {filename} using OpenAI Whisper")
        
        # Whisper requires a file-like object with a filename or a file on disk
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1] or ".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as audio_file:
                # We use the prompt-less transcription. Whisper detects language automatically.
                # However, openai api returns text but language is not always directly exposed in the standard response unless verbose_json is used, but even then it's 'language'.
                # Let's request verbose_json to get language.
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
                
            text = response.text
            language = getattr(response, 'language', 'unknown')
            
            # Confidence is not provided by Whisper API directly in verbose_json in a simple way for the whole text, mock it
            # or extract from segments if available. We will just use a default high confidence if it succeeds.
            confidence = 0.95
            
            return TranscriptionResult(
                text=text,
                language=language,
                confidence=confidence
            )
        except Exception as e:
            logger.error(f"Speech recognition failed: {e}")
            raise ValueError(f"Speech recognition failed: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
