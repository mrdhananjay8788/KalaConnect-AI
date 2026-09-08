from abc import ABC, abstractmethod
from app.schemas.image import VisionAnalysis

class BaseVisionProvider(ABC):
    @abstractmethod
    async def analyze_image(self, image_bytes: bytes) -> VisionAnalysis:
        """Analyze image and extract visual product features, background details, and attributes."""
        pass
