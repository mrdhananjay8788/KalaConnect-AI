# Phase 6: AI Buyer-Artisan Intelligent Matching Engine

## Overview
Phase 6 introduces a robust B2B matchmaking engine bridging natural language requirements with strict B2B logistics. It safely extracts buyer constraints (budget, quantity, delivery location) without hallucination and strictly filters incompatible suppliers before executing an explainable, weighted scoring pipeline on remaining candidates. 

## Features
- **Multilingual Extraction (`app.ai.matching.extraction`)**: Utilizes `BaseRequirementExtractionProvider` to isolate limits like `price_max` or `quantity` thresholds from free-text.
- **Strict B2B Hard Constraints (`app.services.matching_engine`)**: Automatically eliminates artisans who cannot logically fulfill requirements (e.g., missed deadlines, exceeded budgets, lack of customization support).
- **Split-Order Algorithms**: When `allow_split_order=True` is provided, a greedy capacity algorithm intelligently groups smaller artisans together to fulfill massive B2B quantities securely.
- **Fairness-Aware Weighted Ranking**: Results are mathematically scored utilizing:
  - `Semantic Fit`: 0.30
  - `Capacity Feasibility`: 0.20
  - `Price Proximity`: 0.15
  - `Delivery Feasibility`: 0.10
  - `Customization Fit`: 0.10
  - `Profile/Region/Reliability`: Remaining 0.15

## Safety and Explanations
Every matched artisan contains an `explanation` array breaking down the exact criteria satisfied alongside `warnings` for missing or unproven data (e.g. unverified shipping costs or lack of historical data for new sellers). Confidence scores dynamically fluctuate based on profile completeness.
