# KalaConnect-AI Backend

This is the AI backend for the KalaConnect-AI project, an AI Business Manager for marginalized artisans. It provides a FastAPI-based REST API that integrates with various AI services (mocked for Phase 1) to generate product listings from images and voice.

## Phase 1 Architecture

Currently, the backend implements the foundation and architecture, operating in a "mock mode." 
The pipeline is designed as:
`ARTISAN` -> `IMAGE/VOICE/TEXT` -> `AI INPUT PROCESSING` -> `AI ORCHESTRATOR` -> `SPECIALIZED AI MODULES` -> `STRUCTURED PRODUCT DATA`

## Phase 2: Multilingual Auto-Cataloger
The system now includes an advanced Phase 2 pipeline that can convert regional language voice or text (Marathi, Hindi, English) directly into a structured e-commerce catalog, including automatic translations, professional descriptions, SEO keywords, and intelligent follow-up questions for missing details.

## Phase 3: AI Image Intelligence & E-commerce Image Studio
The Phase 3 addition introduces an intelligent image pipeline that validates uploads, calculates quality metrics, performs vision-based attribute extraction, removes cluttered backgrounds automatically, and mildly enhances and formats artisan photos into professional e-commerce WEBP images without fabricating or falsifying the products.

## Phase 4: AI Dynamic Pricing Assistant
The Phase 4 pricing assistant generates explainable, data-driven pricing recommendations using a hybrid engine. It avoids using LLMs to guess pricing arbitrarily, relying instead on deterministic cost calculations, market data percentiles, and optional future ML modules. It provides full transparency via localized artisan-friendly explanations and supports what-if simulation scenarios.

## Phase 5: AI Smart Search & Product Discovery
The Phase 5 integration replaces keyword reliance with an intent-driven, multilingual Semantic Search engine. It processes natural language queries (Marathi/Hindi/English), extracts strict hard-filters (Price/Quantity limits), and applies a hybrid scoring mechanism (`Semantic Vector + Keyword Overlap + Hard Filter Compliance + Business Value`). It securely handles pagination, empty searches via alternative suggestions, and provides "match reasons" for explainable results.

## Phase 6: AI Buyer-Artisan Intelligent Matching
The Phase 6 matchmaking architecture bridges B2B buyer requirements directly to artisans capable of handling the logistics. It leverages deep extraction logic for quantities, budgets, and deadlines, followed by a weighted matching algorithm enforcing hard constraints, resulting in explainable recommendations. It even accommodates Split-Order architectures allowing large bulk quotas to be met securely by multiple independent, marginalized artisans sharing the burden.

## Folder Structure

- `app/api/`: FastAPI route definitions and dependency injection.
- `app/core/`: Configuration, logging, and global exceptions.
- `app/models/` & `app/schemas/`: Pydantic models for request/response validation (e.g., `Product`, `CatalogResponse`).
- `app/ai/`: The AI orchestrator, module interfaces, and prompt management (`app/ai/prompts`).
- `app/services/`: Business logic bridging routes and the orchestrator.
- `tests/`: Automated unit and integration tests.
- `docs/`: Architecture, API, Phase 2, and Evaluation Metrics documentation.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Copy `.env.example` to `.env` and configure as needed:
```bash
cp .env.example .env
```
Set `AI_MODE=mock` for fast, deterministic testing without API keys, or `AI_MODE=production` with `OPENAI_API_KEY` set to run the real AI pipeline.

## Running the Server
```bash
python run.py
```
The server will run at `http://localhost:8000`. You can view the automatic interactive API documentation at `http://localhost:8000/docs`.

## Running Tests
```bash
pytest tests/
```
