from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTranslationProvider(ABC):
    @abstractmethod
    async def translate(self, text: str, target_lang: str) -> str:
        """Translate text to target language."""
        pass
    
    @abstractmethod
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the provided text.
        Returns:
            {"language_code": "mr", "language_name": "Marathi", "confidence": 0.98}
        """
        pass
