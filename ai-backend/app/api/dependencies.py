from fastapi import Depends
from typing import Annotated

from app.core.config import settings
from app.ai.orchestrator import AIOrchestrator

# Import Base Providers
from app.ai.llm.base import BaseLLMProvider
from app.ai.speech.base import BaseSpeechProvider
from app.ai.vision.base import BaseVisionProvider
from app.ai.translation.base import BaseTranslationProvider
from app.ai.pricing.base import BasePricingProvider
from app.ai.pricing.market import BaseMarketDataProvider, MockMarketDataProvider
from app.ai.pricing.ml import BasePricePredictionModel, MockPricePredictionModel
from app.ai.search.embedding import BaseEmbeddingProvider, MockEmbeddingProvider
from app.ai.search.vector_store import BaseVectorStore, MockVectorStore
from app.ai.vision.segmentation import BaseSegmentationProvider, MockSegmentationProvider, RealSegmentationProvider
from app.ai.vision.enhancement import BaseImageEnhancementProvider, MockImageEnhancementProvider, RealImageEnhancementProvider
from app.services.image_service import ImageService
from app.services.pricing_engine import PricingEngine
from app.services.search_engine import SearchEngine
from app.ai.matching.extraction import BaseRequirementExtractionProvider, MockRequirementExtractionProvider
from app.ai.matching.feasibility import BaseDeliveryFeasibilityProvider, MockDeliveryFeasibilityProvider
from app.services.matching_engine import MatchingEngine

# Import Mock Providers
from app.ai.llm.provider import MockLLMProvider, RealLLMProvider
from app.ai.speech.provider import MockSpeechProvider, RealSpeechProvider
from app.ai.vision.provider import MockVisionProvider, RealVisionProvider
from app.ai.translation.provider import MockTranslationProvider, RealTranslationProvider
from app.ai.pricing.provider import MockPricingProvider

def get_llm_provider() -> BaseLLMProvider:
    if settings.AI_MODE == "production":
        return RealLLMProvider()
    return MockLLMProvider()

def get_speech_provider() -> BaseSpeechProvider:
    if settings.AI_MODE == "production":
        return RealSpeechProvider()
    return MockSpeechProvider()

def get_vision_provider() -> BaseVisionProvider:
    if settings.AI_MODE == "production":
        return RealVisionProvider()
    return MockVisionProvider()

def get_segmentation_provider() -> BaseSegmentationProvider:
    if settings.AI_MODE == "production":
        return RealSegmentationProvider()
    return MockSegmentationProvider()

def get_enhancement_provider() -> BaseImageEnhancementProvider:
    if settings.AI_MODE == "production":
        return RealImageEnhancementProvider()
    return MockImageEnhancementProvider()

def get_image_service(
    vision: Annotated[BaseVisionProvider, Depends(get_vision_provider)],
    segmentation: Annotated[BaseSegmentationProvider, Depends(get_segmentation_provider)],
    enhancement: Annotated[BaseImageEnhancementProvider, Depends(get_enhancement_provider)]
) -> ImageService:
    return ImageService(vision, segmentation, enhancement)

def get_translation_provider() -> BaseTranslationProvider:
    if settings.AI_MODE == "production":
        return RealTranslationProvider()
    return MockTranslationProvider()

def get_pricing_provider() -> BasePricingProvider:
    if settings.AI_MODE == "mock":
        return MockPricingProvider()
    return MockPricingProvider()

def get_market_data_provider() -> BaseMarketDataProvider:
    return MockMarketDataProvider()

def get_price_prediction_model() -> BasePricePredictionModel:
    return MockPricePredictionModel()

def get_pricing_engine(
    market_provider: Annotated[BaseMarketDataProvider, Depends(get_market_data_provider)],
    ml_provider: Annotated[BasePricePredictionModel, Depends(get_price_prediction_model)],
    llm_provider: Annotated[BaseLLMProvider, Depends(get_llm_provider)]
) -> PricingEngine:
    return PricingEngine(market_provider, ml_provider, llm_provider)

def get_embedding_provider() -> BaseEmbeddingProvider:
    return MockEmbeddingProvider()

def get_vector_store() -> BaseVectorStore:
    return MockVectorStore()

def get_search_engine(
    embedding_provider: Annotated[BaseEmbeddingProvider, Depends(get_embedding_provider)],
    vector_store: Annotated[BaseVectorStore, Depends(get_vector_store)],
    llm_provider: Annotated[BaseLLMProvider, Depends(get_llm_provider)]
) -> SearchEngine:
    return SearchEngine(embedding_provider, vector_store, llm_provider)

def get_ai_orchestrator(
    llm: Annotated[BaseLLMProvider, Depends(get_llm_provider)],
    speech: Annotated[BaseSpeechProvider, Depends(get_speech_provider)],
    vision: Annotated[BaseVisionProvider, Depends(get_vision_provider)],
    translation: Annotated[BaseTranslationProvider, Depends(get_translation_provider)],
    pricing: Annotated[BasePricingProvider, Depends(get_pricing_provider)],
) -> AIOrchestrator:
    return AIOrchestrator(
        llm_provider=llm,
        speech_provider=speech,
        vision_provider=vision,
        translation_provider=translation,
        pricing_provider=pricing
    )

def get_requirement_extractor() -> BaseRequirementExtractionProvider:
    if settings.AI_MODE == "mock":
        return MockRequirementExtractionProvider()
    return MockRequirementExtractionProvider()

def get_delivery_feasibility() -> BaseDeliveryFeasibilityProvider:
    if settings.AI_MODE == "mock":
        return MockDeliveryFeasibilityProvider()
    return MockDeliveryFeasibilityProvider()

def get_matching_engine(
    extractor: Annotated[BaseRequirementExtractionProvider, Depends(get_requirement_extractor)],
    feasibility: Annotated[BaseDeliveryFeasibilityProvider, Depends(get_delivery_feasibility)]
) -> MatchingEngine:
    return MatchingEngine(extractor, feasibility)