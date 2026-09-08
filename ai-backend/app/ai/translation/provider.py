import asyncio
import json
from openai import AsyncOpenAI
from app.ai.translation.base import BaseTranslationProvider
from app.core.config import settings
from app.ai.prompts.translation import TRANSLATION_SYSTEM_PROMPT, TRANSLATION_USER_PROMPT

class MockTranslationProvider(BaseTranslationProvider):
    async def translate(self, text: str, target_lang: str) -> str:
        await asyncio.sleep(0.3)
        if target_lang == "hi":
            return "यह हाथ से बनी हुई बांस की टोकरी है।"
        elif target_lang == "en":
            return "This is a handmade bamboo basket."
        return f"Translated to {target_lang}: {text}"

    async def detect_language(self, text: str) -> dict:
        await asyncio.sleep(0.1)
        # Mocking for Marathi test cases mostly
        if "ही" in text or "आहे" in text:
            return {"language_code": "mr", "language_name": "Marathi", "confidence": 0.98}
        elif "है" in text:
            return {"language_code": "hi", "language_name": "Hindi", "confidence": 0.98}
        return {"language_code": "en", "language_name": "English", "confidence": 0.98}

class RealTranslationProvider(BaseTranslationProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def translate(self, text: str, target_lang: str) -> str:
        sys_prompt = TRANSLATION_SYSTEM_PROMPT.format(target_language=target_lang)
        user_prompt = TRANSLATION_USER_PROMPT.format(text=text)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    async def detect_language(self, text: str) -> dict:
        sys_prompt = "You are a language detection expert. Detect the language of the user's text. Return ONLY a JSON object with keys: language_code (iso 639-1), language_name, confidence (float 0-1)."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            result = json.loads(response.choices[0].message.content)
            # Ensure proper fallbacks
            if "confidence" not in result or result["confidence"] < 0.5:
                 return {"language_code": None, "requires_confirmation": True}
            return result
        except Exception:
            return {"language_code": None, "requires_confirmation": True}
