import json
import os
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorStore(ABC):
    @abstractmethod
    async def index_product(self, product_id: str, embedding: List[float], metadata: Dict[str, Any]):
        """Store a product embedding with its associated metadata."""
        pass

    @abstractmethod
    async def search(self, query_embedding: List[float], filters: Dict[str, Any] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for products using embedding and apply hard filters."""
        pass

class MockVectorStore(BaseVectorStore):
    def __init__(self, data_path: str = "data/catalog/demo_catalog.json"):
        self.data_path = data_path
        self._data = []
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self._data = json.load(f)

    async def index_product(self, product_id: str, embedding: List[float], metadata: Dict[str, Any]):
        # Mock doesn't strictly index dynamically, it uses the static JSON catalog for Phase 5 demo.
        pass

    async def search(self, query_embedding: List[float], filters: Dict[str, Any] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Since we don't have real embeddings in Mock, we simulate semantic search 
        by returning ALL filtered products and letting the SearchEngine rank them 
        using keywords and category matching.
        """
        results = []
        for item in self._data:
            # Apply Hard Filters
            if filters:
                # Price Filter
                price_max = filters.get("price_max")
                if price_max and item.get("price", 0) > price_max:
                    continue
                
                # Quantity Filter
                quantity = filters.get("quantity")
                if quantity and item.get("availability", 0) < quantity:
                    continue

                # Category Filter
                category = filters.get("category")
                if category and item.get("category", "").lower() != category.lower():
                    continue

            # Return the item to the engine for scoring
            results.append({
                "product_id": item["product_id"],
                "product_name": item["product_name"],
                "price": item["price"],
                "availability": item["availability"],
                "category": item.get("category", ""),
                "materials": item.get("materials", []),
                "keywords": item.get("keywords", []),
                "metadata": item
            })

        return results[:limit]
