# Architecture

## Overview
The KalaConnect-AI backend is designed as a modular pipeline that acts as an AI Business Manager. 
It uses FastAPI for high performance, with strict Pydantic schemas validating all inputs and outputs.

## Pipeline
1. **API Layer**: Exposes endpoints under `/api/v1/`. Uses Dependency Injection to provide the appropriate AI Orchestrator.
2. **AI Orchestrator**: The core controller that receives input (Image/Voice/Text) and coordinates the various specialized AI Modules.
3. **AI Modules**: Abstract base classes (e.g., `BaseLLMProvider`) and concrete implementations (e.g., `MockLLMProvider`, `RealOpenAIProvider`).
4. **Data Layer**: Structured `Product` object returned as JSON. Ready for future PostgreSQL integration.

## Components

1. **AI Orchestrator (`app.ai.orchestrator`)**
   - Coordinates the entire pipeline.
   - Combines output from various models.

2. **Image Studio Engine (`app.services.image_service`)**
   - Validates, analyzes, segments, enhances, and formats images.

3. **Pricing Engine (`app.services.pricing_engine`)**
   - Hybrid engine combining deterministic costs, comparable market data, and ML prediction.
   - Outputs confidence scores, price ranges, and multi-lingual artisan explanations.

4. **Search Engine (`app.services.search_engine`)**
   - Hybrid search resolving queries using Semantics, Keyword Overlap, Hard Filters, and Business rules.
   - Gracefully relaxes queries to serve alternatives for empty results.

5. **Matching Engine (`app.services.matching_engine`)**
   - End-to-end B2B buyer matchmaking validating hard capacity constraints and splitting bulk orders among multiple artisans.
   - Calculates dynamic scores for price compatibility, delivery feasibility, and customization.

6. **Modular Providers (`app.ai.*.provider`)**
   - Implementations for `BaseLLMProvider`, `BaseSpeechProvider`, `BaseVisionProvider`, `BaseTranslationProvider`, `BasePricingProvider`, `BaseMarketDataProvider`, `BasePricePredictionModel`, `BaseSegmentationProvider`, `BaseImageEnhancementProvider`, `BaseEmbeddingProvider`, `BaseVectorStore`, `BaseRequirementExtractionProvider`, `BaseDeliveryFeasibilityProvider`.
   - Supports switching between Mock (development/testing) and Real (production) providers based on `AI_MODE`.

## Configuration
Controlled via `.env` file and `app/core/config.py`. The `AI_MODE` variable switches between mock providers and real API integrations.
