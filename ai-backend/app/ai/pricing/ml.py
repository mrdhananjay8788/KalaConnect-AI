from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BasePricePredictionModel(ABC):
    @abstractmethod
    async def predict(self, features: Dict[str, Any]) -> Optional[float]:
        """Predict the price using an ML model."""
        pass

    @abstractmethod
    async def confidence(self, features: Dict[str, Any]) -> float:
        """Return the confidence of the prediction (0.0 to 1.0)."""
        pass

class MockPricePredictionModel(BasePricePredictionModel):
    """
    Mock implementation that acts as a placeholder. 
    It returns None to simulate that no ML model is currently trained or active.
    """
    async def predict(self, features: Dict[str, Any]) -> Optional[float]:
        # Return None to signify no ML prediction available yet (avoid fake AI)
        return None

    async def confidence(self, features: Dict[str, Any]) -> float:
        return 0.0
