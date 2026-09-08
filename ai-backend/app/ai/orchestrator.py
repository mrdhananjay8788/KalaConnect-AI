import uuid
import json
from typing import Dict, Any, Optional

from app.schemas.product import Product, ProductDescription, ProductImage, ProductPricing, AIMetadata
from app.schemas.catalog import CatalogResponseData, MissingFieldInfo, TranscriptionResult
from app.ai.llm.base import BaseLLMProvider
from app.ai.speech.base import BaseSpeechProvider
from app.ai.vision.base import BaseVisionProvider
from app.ai.translation.base import BaseTranslationProvider
from app.ai.pricing.base import BasePricingProvider
from app.core.logging import logger

class AIOrchestrator:
    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        speech_provider: BaseSpeechProvider,
        vision_provider: BaseVisionProvider,
        translation_provider: BaseTranslationProvider,
        pricing_provider: BasePricingProvider
    ):
        self.llm = llm_provider
        self.speech = speech_provider
        self.vision = vision_provider
        self.translation = translation_provider
        self.pricing = pricing_provider

    async def _run_catalog_pipeline(self, text: str, transcription_result: Optional[TranscriptionResult] = None) -> CatalogResponseData:
        """Internal pipeline for Phase 2: Multilingual Auto-Cataloger."""
        # 1. Language Detection
        logger.info("Detecting language...")
        lang_result = await self.translation.detect_language(text)
        language_code = lang_result.get("language_code") or "en"

        # 2. Text Normalization (Skipped complex normalization for now, just stripping)
        normalized_text = text.strip()

        # 3. Product Information Extraction
        logger.info("Extracting product information...")
        product_json = await self.llm.extract_product_info(normalized_text)
        
        # 4. Missing Information Detection
        missing_fields = product_json.get("missing_fields", [])
        # Provide basic importance for missing fields
        important_fields = ["price", "material", "color", "dimensions"]
        missing_info_objects = []
        for field in missing_fields:
            importance = "high" if field in important_fields else "medium"
            missing_info_objects.append(MissingFieldInfo(field=field, importance=importance))

        # 5. Translation & 6. Description Generation
        logger.info("Generating descriptions...")
        # Get descriptions in English and Hindi
        product_json_str = json.dumps(product_json, ensure_ascii=False)
        
        hindi_desc = await self.llm.generate_description(product_json_str, "hi")
        english_desc = await self.llm.generate_description(product_json_str, "en")
        
        if language_code not in ["hi", "en"]:
            original_desc = await self.llm.generate_description(product_json_str, language_code)
        elif language_code == "hi":
            original_desc = hindi_desc
        else:
            original_desc = english_desc

        desc_obj = ProductDescription(
            original=original_desc,
            hindi=hindi_desc,
            english=english_desc
        )

        # 7. SEO Keyword Generation
        logger.info("Generating SEO keywords...")
        keywords = await self.llm.generate_keywords(product_json_str)

        # 8. Follow-up Question
        next_question = None
        high_priority_missing = [m.field for m in missing_info_objects if m.importance == "high"]
        if high_priority_missing:
            logger.info("Generating follow-up question...")
            next_question = await self.llm.generate_followup_question(
                language=language_code,
                missing_fields_json=json.dumps(high_priority_missing)
            )

        # Return structured CatalogResponseData
        return CatalogResponseData(
            transcription=transcription_result,
            product=product_json,
            descriptions=desc_obj,
            keywords=keywords,
            missing_fields=missing_info_objects,
            next_question=next_question
        )

    async def process_voice_catalog(self, audio_bytes: bytes, filename: str = "audio.wav") -> CatalogResponseData:
        logger.info("Starting Phase 2 voice catalog pipeline...")
        # Speech-to-Text
        transcription_result = await self.speech.transcribe(audio_bytes, filename)
        return await self._run_catalog_pipeline(
            text=transcription_result.text,
            transcription_result=transcription_result
        )

    async def process_text_catalog(self, text: str) -> CatalogResponseData:
        logger.info("Starting Phase 2 text catalog pipeline...")
        return await self._run_catalog_pipeline(text=text)

    # Legacy Phase 1 method
    async def process_product(
        self,
        artisan_id: str,
        image_data: Optional[bytes] = None,
        voice_data: Optional[bytes] = None,
        text_description: Optional[str] = None
    ) -> Product:
        logger.info(f"Starting Phase 1 AI orchestration for artisan {artisan_id}")
        
        # 1. Handle Voice Input
        raw_text = text_description or ""
        if voice_data:
            logger.info("Processing voice input...")
            transcription_result = await self.speech.transcribe(voice_data)
            raw_text = f"{raw_text}\n{transcription_result.text}".strip()

        if not raw_text and not image_data:
            raise ValueError("No valid input provided (need image, voice, or text).")

        # 2. Extract Product Info from Text
        product_features = {}
        if raw_text:
            logger.info("Extracting product info via LLM...")
            product_features = await self.llm.extract_product_info(raw_text)

        # 3. Vision Analysis
        image_analysis = {}
        if image_data:
            logger.info("Analyzing image...")
            vision_result = await self.vision.analyze_image(image_data)
            image_analysis = vision_result.model_dump()
            
            # Map attributes to colors for Phase 1 compatibility
            colors = [attr["value"] for attr in image_analysis.get("attributes", []) if attr["name"] == "color"]
            if colors and not product_features.get("color"):
                product_features["color"] = colors

        # 4. Translation
        original_desc = raw_text
        lang_result = await self.translation.detect_language(original_desc)
        detected_lang = lang_result.get("language_code") or "en"
        
        hindi_desc = None
        english_desc = None
        
        if detected_lang != "en":
            english_desc = await self.translation.translate(original_desc, "en")
        else:
            english_desc = original_desc
            
        if detected_lang != "hi":
            hindi_desc = await self.translation.translate(english_desc, "hi")
        else:
            hindi_desc = original_desc

        desc_obj = ProductDescription(
            original=original_desc,
            hindi=hindi_desc,
            english=english_desc
        )

        # 5. Pricing Suggestion
        logger.info("Suggesting pricing...")
        pricing_data = await self.pricing.suggest_price(product_features)
        pricing_obj = ProductPricing(**pricing_data)

        # 6. Construct Product Object
        image_obj = ProductImage(
            original_url="mock_url",
            processed_url="mock_processed_url",
            quality_score=image_analysis.get("quality_score", 0.0)
        )
        
        ai_meta = AIMetadata(
            model="mock_orchestrator_v1",
            confidence=0.85
        )

        product = Product(
            product_id=str(uuid.uuid4()),
            artisan_id=artisan_id,
            product_name=product_features.get("product_name", "Unknown Product"),
            category=product_features.get("category", "Uncategorized"),
            subcategory=product_features.get("subcategory", "Uncategorized"),
            craft_type=product_features.get("craft_type", "Unknown"),
            material=product_features.get("material", []),
            color=product_features.get("color", []),
            dimensions=product_features.get("dimensions", {}),
            weight=product_features.get("weight"),
            region=product_features.get("region", "Unknown"),
            language=detected_lang,
            description=desc_obj,
            keywords=product_features.get("keywords", []),
            image=image_obj,
            pricing=pricing_obj,
            ai_metadata=ai_meta
        )

        logger.info("Successfully constructed product object.")
        return product
