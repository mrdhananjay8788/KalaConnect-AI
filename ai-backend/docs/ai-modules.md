# AI Modules

This project isolates AI logic from the API logic. All AI integration happens within `app/ai/`.

## Adding a new Provider

1. Inherit from the base provider (e.g., `BaseLLMProvider`).
2. Implement all abstract methods.
3. Update `app/api/dependencies.py` to inject your new provider when `AI_MODE="production"`.

## Modules
- **LLM**: Handles product info extraction and text generation.
- **Speech**: Converts audio files to text.
- **Vision**: Analyzes images for colors, quality, and objects.
- **Translation**: Detects language and translates to English and Hindi.
- **Pricing**: Suggests dynamic pricing based on materials, labor, and market trends.
- **### Search Engine Layer (Phase 5)
* `BaseEmbeddingProvider` / `MockEmbeddingProvider`: Converts text strings to semantic vectors crossing language barriers.
* `BaseVectorStore` / `MockVectorStore`: Stores and retrieves high dimensional product embeddings alongside hard filtering metadata.

### Matchmaking Layer (Phase 6)
* `BaseRequirementExtractionProvider` / `MockRequirementExtractionProvider`: Connects NLP to Pydantic extraction resolving queries to parameters.
* `BaseDeliveryFeasibilityProvider` / `MockDeliveryFeasibilityProvider`: Bridges logistics mapping expected regional fulfillment constraints.
