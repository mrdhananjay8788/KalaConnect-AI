from app.ai.pricing.base import BasePricingProvider
import asyncio
from typing import Dict, Any

class MockPricingProvider(BasePricingProvider):
    async def suggest_price(self, product_features: Dict[str, Any]) -> dict:
        await asyncio.sleep(0.4)
        return {
            "raw_material_cost": 1500.0,
            "labor_cost": 3000.0,
            "suggested_price": 6500.0,
            "min_price": 5500.0,
            "max_price": 8000.0,
            "confidence": 0.9
        }
