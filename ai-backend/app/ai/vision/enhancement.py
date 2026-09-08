from abc import ABC, abstractmethod
import io
import asyncio
from PIL import Image, ImageEnhance
from app.core.logging import logger

class BaseImageEnhancementProvider(ABC):
    @abstractmethod
    async def enhance(self, image_bytes: bytes) -> bytes:
        """Apply basic lighting and contrast enhancements."""
        pass

    @abstractmethod
    async def format_for_ecommerce(self, image_bytes: bytes, width: int = 1200, height: int = 1200) -> bytes:
        """Format the image to WEBP with specific dimensions."""
        pass

class MockImageEnhancementProvider(BaseImageEnhancementProvider):
    async def enhance(self, image_bytes: bytes) -> bytes:
        await asyncio.sleep(0.2)
        return image_bytes

    async def format_for_ecommerce(self, image_bytes: bytes, width: int = 1200, height: int = 1200) -> bytes:
        await asyncio.sleep(0.2)
        return image_bytes

class RealImageEnhancementProvider(BaseImageEnhancementProvider):
    async def enhance(self, image_bytes: bytes) -> bytes:
        """Apply mild brightness and contrast corrections."""
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._enhance_sync, image_bytes)
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            return image_bytes

    def _enhance_sync(self, image_bytes: bytes) -> bytes:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB" and img.mode != "RGBA":
            img = img.convert("RGB")
            
        # Mild contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.05)
        
        # Mild brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)

        out_io = io.BytesIO()
        img.save(out_io, format=img.format or "PNG")
        return out_io.getvalue()

    async def format_for_ecommerce(self, image_bytes: bytes, width: int = 1200, height: int = 1200) -> bytes:
        """Resize and pad to square WEBP."""
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._format_sync, image_bytes, width, height)
        except Exception as e:
            logger.error(f"Formatting failed: {e}")
            return image_bytes

    def _format_sync(self, image_bytes: bytes, width: int, height: int) -> bytes:
        img = Image.open(io.BytesIO(image_bytes))
        
        # If RGBA, we can composite onto a white background to avoid transparent WEBPs looking bad
        # But we'll preserve transparency if it exists for e-commerce
        
        # Resize while maintaining aspect ratio
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        
        # Create a new blank image with target dimensions
        if img.mode == 'RGBA':
            background = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        else:
            background = Image.new('RGB', (width, height), (255, 255, 255))
            
        # Paste centered
        offset = ((width - img.width) // 2, (height - img.height) // 2)
        background.paste(img, offset)

        out_io = io.BytesIO()
        background.save(out_io, format="WEBP", quality=90)
        return out_io.getvalue()
