import json
import os
import statistics
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.pricing import MarketDataStats

class BaseMarketDataProvider(ABC):
    @abstractmethod
    async def get_comparables(self, category: str, subcategory: Optional[str] = None, material: Optional[str] = None, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find comparable products."""
        pass

    @abstractmethod
    async def get_market_statistics(self, comparables: List[Dict[str, Any]]) -> Optional[MarketDataStats]:
        """Calculate market statistics from comparables."""
        pass

class MockMarketDataProvider(BaseMarketDataProvider):
    def __init__(self, data_path: str = "data/market/market_products.json"):
        self.data_path = data_path
        self._data = []
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self._data = json.load(f)

    async def get_comparables(self, category: str, subcategory: Optional[str] = None, material: Optional[str] = None, region: Optional[str] = None) -> List[Dict[str, Any]]:
        # Simple exact/partial match logic
        comparables = []
        for item in self._data:
            score = 0
            if item.get("category") == category:
                score += 1
            if subcategory and item.get("subcategory") == subcategory:
                score += 1
            if material and item.get("material") == material:
                score += 1
            
            if score > 0:
                comparables.append(item)
        return comparables

    async def get_market_statistics(self, comparables: List[Dict[str, Any]]) -> Optional[MarketDataStats]:
        prices = [item["price"] for item in comparables if "price" in item]
        if not prices:
            return None
            
        prices.sort()
        return MarketDataStats(
            sample_size=len(prices),
            median=statistics.median(prices),
            mean=statistics.mean(prices),
            min=min(prices),
            max=max(prices),
            range=[min(prices), max(prices)]
        )
