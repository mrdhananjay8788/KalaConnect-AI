from abc import ABC, abstractmethod
import asyncio
from app.core.logging import logger

class BaseSegmentationProvider(ABC):
    @abstractmethod
    async def remove_background(self, image_bytes: bytes) -> bytes:
        """Removes the background from the image and returns a transparent PNG bytes."""
        pass

class MockSegmentationProvider(BaseSegmentationProvider):
    async def remove_background(self, image_bytes: bytes) -> bytes:
        await asyncio.sleep(0.5)
        logger.info("Mock Segmentation: Returning original image bytes as placeholder.")
        return image_bytes

class RealSegmentationProvider(BaseSegmentationProvider):
    def __init__(self):
        self.rembg_session = None
        try:
            import rembg
            self.rembg = rembg
        except ImportError:
            self.rembg = None
            logger.warning("rembg is not installed. RealSegmentationProvider will fall back to returning original image.")

    async def remove_background(self, image_bytes: bytes) -> bytes:
        if not self.rembg:
            logger.warning("rembg not available, skipping actual segmentation.")
            return image_bytes

        logger.info("Running real background segmentation.")
        try:
            # We must run this in a threadpool to not block the async event loop
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self._run_rembg, image_bytes)
            return result
        except Exception as e:
            logger.error(f"Segmentation failed: {e}")
            return image_bytes

    def _run_rembg(self, image_bytes: bytes) -> bytes:
        if not self.rembg_session:
            self.rembg_session = self.rembg.new_session()
        return self.rembg.remove(image_bytes, session=self.rembg_session)
