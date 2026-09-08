from abc import ABC, abstractmethod
from typing import List

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """Generate text based on a prompt."""
        pass
    
    @abstractmethod
    async def extract_product_info(self, text: str) -> dict:
        """Extract structured product information from raw text.
        Returns a dict matching the ProductExtraction schema."""
        pass

    @abstractmethod
    async def generate_description(self, product_json: str, language: str) -> str:
        """Generate a product description in the target language."""
        pass

    @abstractmethod
    async def generate_keywords(self, product_json: str) -> List[str]:
        """Generate SEO keywords based on product details."""
        pass

    @abstractmethod
    async def generate_followup_question(self, language: str, missing_fields_json: str) -> str:
        """Generate a follow-up question for missing information."""
        pass
