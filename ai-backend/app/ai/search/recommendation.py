from abc import ABC, abstractmethod
from typing import List
from app.schemas.search import SimilarProduct
from app.ai.search.vector_store import BaseVectorStore

class BaseRecommendationProvider(ABC):
    def __init__(self, vector_store: BaseVectorStore):
        self.vector_store = vector_store

    @abstractmethod
    async def get_similar_products(self, product_id: str, limit: int = 5) -> List[SimilarProduct]:
        pass

class MockRecommendationProvider(BaseRecommendationProvider):
    async def get_similar_products(self, product_id: str, limit: int = 5) -> List[SimilarProduct]:
        candidates = await self.vector_store.search(query_embedding=[0.0], filters={}, limit=limit + 1)
        similars = []
        for c in candidates:
            if c["product_id"] != product_id:
                similars.append(SimilarProduct(
                    product_id=c["product_id"],
                    similarity=0.85
                ))
        return similars[:limit]
