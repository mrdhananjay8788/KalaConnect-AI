from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePricingProvider(ABC):
    @abstractmethod
    async def suggest_price(self, product_features: Dict[str, Any]) -> dict:
        """Suggest pricing based on product features."""
        pass
