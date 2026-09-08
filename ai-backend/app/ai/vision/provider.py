import asyncio
import base64
import json
from openai import AsyncOpenAI
from app.ai.vision.base import BaseVisionProvider
from app.schemas.image import VisionAnalysis, VisionAttribute
from app.core.config import settings
from app.core.logging import logger

class MockVisionProvider(BaseVisionProvider):
    async def analyze_image(self, image_bytes: bytes) -> VisionAnalysis:
        await asyncio.sleep(0.8)
        return VisionAnalysis(
            objects=[{
                "label": "handcrafted basket",
                "confidence": 0.91,
                "bounding_box": {"x": 120, "y": 80, "width": 820, "height": 760}
            }],
            attributes=[
                VisionAttribute(name="color", value="brown", confidence=0.93),
                VisionAttribute(name="material", value="bamboo", confidence=0.85)
            ],
            category="handicraft",
            background_type="cluttered"
        )

class RealVisionProvider(BaseVisionProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_image(self, image_bytes: bytes) -> VisionAnalysis:
        logger.info("Analyzing image using OpenAI Vision")
        # Convert bytes to base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        prompt = '''
        You are an AI vision assistant for an artisan marketplace.
        Analyze this image and extract:
        1. "objects": List of objects detected (label, confidence, rough bounding_box if possible or empty).
        2. "attributes": List of visual attributes (color, pattern, material). Output format: {"name": "color", "value": "red", "confidence": 0.9}. Only output what is visually observed, not assumed.
        3. "category": The product category.
        4. "background_type": Is the background "plain" or "cluttered"?

        Return strictly as a JSON object matching this schema.
        '''
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Map to schema
            attributes = [VisionAttribute(**attr) for attr in data.get("attributes", [])]
            
            return VisionAnalysis(
                objects=data.get("objects", []),
                attributes=attributes,
                category=data.get("category"),
                background_type=data.get("background_type", "unknown")
            )
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            # Fallback
            return VisionAnalysis(
                background_type="unknown"
            )
