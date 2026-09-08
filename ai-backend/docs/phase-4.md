# Phase 4: AI Dynamic Pricing Assistant

## Overview
Phase 4 introduces an AI Dynamic Pricing Assistant that provides data-driven, explainable price recommendations for artisans. Instead of blindly guessing a price using an LLM, the system leverages deterministic cost calculations and market comparables to establish a fair baseline. 

## Pricing Architecture
The `PricingEngine` utilizes a hybrid approach:
1. **Cost-Based Calculation**: `(Material + Labor + Production + Packaging + Transportation) * (1 + Desired Margin)`.
2. **Market Comparable Engine**: Searches `MarketDataProvider` for similar items and calculates median price points.
3. **ML Check**: Supports `BasePricePredictionModel` for future ML prediction integration (disabled in Phase 4 to avoid "fake AI").

## Explainability
Pricing recommendations include an `explanation` block detailing exactly how the final price was determined, and an `artisan_message` block that automatically generates a localized, non-technical explanation in Marathi, Hindi, and English.

## Endpoints
- `POST /api/v1/pricing/suggest`: Computes the suggested price, range, and confidence score.
- `POST /api/v1/pricing/simulate`: Performs "What-if" analysis for an artisan testing a hypothetical selling price to see its margin and profit.

## Synthetic Data Disclaimer
The market products stored in `data/market/market_products.json` are **synthetic demo data** used to demonstrate the functionality of Phase 4 and should be replaced with real market intelligence sources in production.
