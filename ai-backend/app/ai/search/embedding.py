from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for a given text."""
        pass

class MockEmbeddingProvider(BaseEmbeddingProvider):
    async def get_embedding(self, text: str) -> List[float]:
        """Return a dummy embedding. For Phase 5 mock, we'll return a 1D vector based on string length, or just rely on keyword logic."""
        # For a truly mock vector, we just return a stub.
        # The vector_store will handle the actual mock similarity matching using keywords instead to avoid complex local math.
        return [0.0, 0.0, 0.0]
