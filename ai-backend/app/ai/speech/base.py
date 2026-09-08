from abc import ABC, abstractmethod
from app.schemas.catalog import TranscriptionResult

class BaseSpeechProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> TranscriptionResult:
        """Transcribe audio to text and return TranscriptionResult."""
        pass
