import io
import time
import uuid
from typing import Optional
from PIL import Image, ImageStat
from app.core.logging import logger
from app.core.exceptions import InvalidInputException
from app.services.storage import storage_service
from app.schemas.image import ImageQualityMetrics, ImageMetadata, ImageProcessResponseData, ImageProcessResponse, ImageConflict
from app.ai.vision.base import BaseVisionProvider
from app.ai.vision.segmentation import BaseSegmentationProvider
from app.ai.vision.enhancement import BaseImageEnhancementProvider

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_IMAGE_SIZE = 15 * 1024 * 1024  # 15 MB

class ImageService:
    def __init__(
        self,
        vision_provider: BaseVisionProvider,
        segmentation_provider: BaseSegmentationProvider,
        enhancement_provider: BaseImageEnhancementProvider
    ):
        self.vision = vision_provider
        self.segmentation = segmentation_provider
        self.enhancement = enhancement_provider

    def validate_image(self, image_bytes: bytes, filename: str, content_type: str) -> str:
        """Validate MIME type, size, extension, and corrupted files."""
        if content_type not in ALLOWED_MIME_TYPES:
            raise InvalidInputException("Unsupported image format. Allowed: JPG, PNG, WEBP.")
            
        if len(image_bytes) > MAX_IMAGE_SIZE:
            raise InvalidInputException("Image too large. Max size is 15MB.")

        # Check for corrupted files via Pillow
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()  # verify checks if the file is broken
            format = img.format.lower() if img.format else "unknown"
            if format not in ["jpeg", "png", "webp", "mpo"]:
                raise InvalidInputException("Invalid image content.")
        except Exception as e:
            raise InvalidInputException(f"Corrupted image file: {e}")
            
        # Ensure safe extension based on content
        ext = ".jpg" if format in ["jpeg", "mpo"] else f".{format}"
        return ext

    def analyze_quality(self, image_bytes: bytes) -> ImageQualityMetrics:
        """Calculate simple quality metrics using Pillow."""
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        stat = ImageStat.Stat(img)
        # stat.mean gives avg color, stat.stddev gives spread (contrast)
        brightness = sum(stat.mean) / 3.0 / 255.0
        contrast = sum(stat.stddev) / 3.0 / 127.5
        
        # very rudimentary sharpness estimate using variance of laplacian usually, 
        # but here we'll mock a sharpness score derived from contrast
        sharpness = min(contrast * 1.2, 1.0)
        
        blur_detected = sharpness < 0.3
        
        quality_score = min(((brightness * 0.5 + contrast * 0.5) * 100), 100)
        
        recs = []
        if brightness < 0.4:
            recs.append("Increase lighting")
        if blur_detected:
            recs.append("Hold camera steady to avoid blur")

        return ImageQualityMetrics(
            quality_score=round(quality_score, 1),
            resolution={"width": img.width, "height": img.height},
            brightness=round(brightness, 2),
            sharpness=round(sharpness, 2),
            contrast=round(contrast, 2),
            blur_detected=blur_detected,
            background_clutter=False, # to be updated by vision
            recommendations=recs
        )

    async def analyze_image_only(self, image_bytes: bytes, filename: str, content_type: str) -> dict:
        """Run just quality + vision analysis."""
        self.validate_image(image_bytes, filename, content_type)
        quality = self.analyze_quality(image_bytes)
        vision_result = await self.vision.analyze_image(image_bytes)
        
        quality.background_clutter = vision_result.background_type == "cluttered"
        if quality.background_clutter:
            quality.recommendations.append("Remove background clutter")
            
        return {
            "quality": quality.model_dump(),
            "vision": vision_result.model_dump()
        }

    async def process_image_pipeline(
        self, 
        image_bytes: bytes, 
        filename: str, 
        content_type: str,
        product_id: Optional[str] = None
    ) -> ImageProcessResponseData:
        start_time = time.time()
        
        # 1. Validation
        ext = self.validate_image(image_bytes, filename, content_type)
        
        # 2. Save Original
        original_path = storage_service.save_original_image(image_bytes, ext)
        
        # 3. Quality Analysis
        quality = self.analyze_quality(image_bytes)
        
        # 4. Vision
        vision_result = await self.vision.analyze_image(image_bytes)
        quality.background_clutter = vision_result.background_type == "cluttered"
        
        # 5. Segmentation & Enhancement
        current_image = image_bytes
        background_info = {"removed": False, "type": vision_result.background_type}
        
        # If background is cluttered, remove it
        if quality.background_clutter:
            current_image = await self.segmentation.remove_background(current_image)
            background_info["removed"] = True
            
        # Enhance
        current_image = await self.enhancement.enhance(current_image)
        
        # 6. Format
        current_image = await self.enhancement.format_for_ecommerce(current_image, width=1200, height=1200)
        
        # 7. Save Processed
        processed_path = storage_service.save_processed_image(current_image, ext=".webp")
        
        # 8. Metadata
        img = Image.open(io.BytesIO(current_image))
        metadata = ImageMetadata(
            image_id=str(uuid.uuid4()),
            product_id=product_id,
            original_filename=filename,
            width=img.width,
            height=img.height,
            format=img.format or "WEBP",
            file_size=len(current_image),
            quality_score=quality.quality_score,
            processing_status="completed",
            processing_time=round(time.time() - start_time, 2),
            model_provider="multi-provider"
        )
        
        return ImageProcessResponseData(
            product_id=product_id,
            original_image=original_path.replace("\\", "/"),
            processed_image=processed_path.replace("\\", "/"),
            quality=quality,
            background=background_info,
            vision_attributes=vision_result.model_dump(),
            metadata=metadata
        )

    async def remove_background_only(self, image_bytes: bytes, filename: str, content_type: str) -> str:
        ext = self.validate_image(image_bytes, filename, content_type)
        result = await self.segmentation.remove_background(image_bytes)
        return storage_service.save_processed_image(result, ".png")
