import asyncio
import json
from typing import List
from openai import AsyncOpenAI
from app.ai.llm.base import BaseLLMProvider
from app.core.config import settings
from app.schemas.catalog import ProductExtraction
from app.ai.prompts.catalog_extraction import CATALOG_EXTRACTION_SYSTEM_PROMPT, CATALOG_EXTRACTION_USER_PROMPT
from app.ai.prompts.description_generation import DESCRIPTION_GENERATION_SYSTEM_PROMPT, DESCRIPTION_GENERATION_USER_PROMPT
from app.ai.prompts.keyword_generation import KEYWORD_GENERATION_SYSTEM_PROMPT, KEYWORD_GENERATION_USER_PROMPT
from app.ai.prompts.followup_questions import FOLLOWUP_QUESTION_SYSTEM_PROMPT, FOLLOWUP_QUESTION_USER_PROMPT

class MockLLMProvider(BaseLLMProvider):
    async def generate_text(self, prompt: str) -> str:
        await asyncio.sleep(0.5)
        return "This is a mocked LLM response."

    async def extract_product_info(self, text: str) -> dict:
        await asyncio.sleep(0.5)
        # Return a structure matching ProductExtraction
        return {
            "product_name": "Paithani Saree" if "पैठणी" in text else "Bamboo Basket",
            "category": "Clothing" if "साडी" in text else "Handicraft",
            "material": ["Silk"] if "रेशमा" in text else ["Bamboo"],
            "price": 8000 if "आठ हजार" in text else None,
            "color": ["Purple"] if "जांभळा" in text else [],
            "confidence": 0.95,
            "missing_fields": ["dimensions", "weight"] if "साडी" in text else ["dimensions", "color", "weight", "price"]
        }

    async def generate_description(self, product_json: str, language: str) -> str:
        await asyncio.sleep(0.5)
        if language == "hi":
            return "यह एक सुंदर हाथ से बनी हुई उत्पाद है। यह आपके घर के लिए एकदम सही है।"
        elif language == "en":
            return "This is a beautiful handcrafted product. It is perfect for your home."
        return "ही एक सुंदर हाताने बनवलेली वस्तू आहे."

    async def generate_keywords(self, product_json: str) -> List[str]:
        await asyncio.sleep(0.2)
        return ["handcrafted", "traditional", "indian art"]

    async def generate_followup_question(self, language: str, missing_fields_json: str) -> str:
        await asyncio.sleep(0.2)
        if language == "mr":
            return "या उत्पादनाची विक्री किंमत किती आहे?"
        elif language == "hi":
            return "इस उत्पाद की बिक्री कीमत कितनी है?"
        return "What is the selling price of this product?"

class RealLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_text(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    async def extract_product_info(self, text: str) -> dict:
        # Use OpenAI structured outputs
        # We can pass the JSON schema of ProductExtraction
        schema = ProductExtraction.model_json_schema()
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CATALOG_EXTRACTION_SYSTEM_PROMPT},
                {"role": "user", "content": CATALOG_EXTRACTION_USER_PROMPT.format(text=text)}
            ],
            functions=[{"name": "extract_product", "parameters": schema}],
            function_call={"name": "extract_product"},
            temperature=0.1
        )
        
        args = response.choices[0].message.function_call.arguments
        try:
            return json.loads(args)
        except json.JSONDecodeError:
            return {}

    async def generate_description(self, product_json: str, language: str) -> str:
        sys_prompt = DESCRIPTION_GENERATION_SYSTEM_PROMPT
        user_prompt = DESCRIPTION_GENERATION_USER_PROMPT.format(language=language, product_json=product_json)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    async def generate_keywords(self, product_json: str) -> List[str]:
        sys_prompt = KEYWORD_GENERATION_SYSTEM_PROMPT
        user_prompt = KEYWORD_GENERATION_USER_PROMPT.format(product_json=product_json)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        content = response.choices[0].message.content.strip()
        try:
            # Sometime model returns markdown wrapper
            if content.startswith("```json"):
                content = content[7:-3]
            return json.loads(content)
        except Exception:
            return []

    async def generate_followup_question(self, language: str, missing_fields_json: str) -> str:
        sys_prompt = FOLLOWUP_QUESTION_SYSTEM_PROMPT
        user_prompt = FOLLOWUP_QUESTION_USER_PROMPT.format(language=language, missing_fields_json=missing_fields_json)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
