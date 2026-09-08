# Phase 5: AI Smart Search & Product Discovery

## Overview
Phase 5 introduces a robust, multi-lingual semantic product discovery system optimized for artisan handicrafts. Unlike rigid keyword search, it understands conversational natural language spanning Marathi, Hindi, and English, applying dynamic query comprehension to resolve shopper intent.

## Architecture
1. **Query Comprehension (`SearchEngine._understand_query`)**: Normalizes input text and isolates hard parameters such as `price_max` or `quantity` thresholds using a scalable regex (expandable to LLM-chain extraction).
2. **Embeddings (`app.ai.search.embedding`)**: `BaseEmbeddingProvider` creates vector signatures representing the contextual "meaning" of a query or product, crossing language barriers inherently.
3. **Vector Database (`app.ai.search.vector_store`)**: `BaseVectorStore` acts as a high-speed repository for semantic lookup. (Currently utilizing `MockVectorStore` with static demo JSON data for initial validation).
4. **Hybrid Ranking Algorithm**: Results are scored based on a weighted composite formula:
   - `0.55`: Semantic Proximity (Core Meaning)
   - `0.20`: Keyword Overlap (Exact matches on titles/tags)
   - `0.15`: Hard Filter Compliance (e.g. strict price limits)
   - `0.10`: Business Priority (e.g. high availability stock)

## Empty States & "Alternatives"
If a user applies a highly restrictive limit (e.g. `paithani saree under 100`), the engine intentionally relaxes the limit to find nearest alternatives, flagging `is_alternative=True` so UI can display "No exact matches found, but here are similar alternatives".

## Fairness
Search ranking consciously includes a `Business Priority` score that relies on *availability* rather than historical sales. This ensures new artisans with sufficient stock appear competitively alongside entrenched sellers, avoiding popularity bias loops.
