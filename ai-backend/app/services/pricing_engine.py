import json
from typing import Dict, Any, Optional
from app.schemas.pricing import (
    PricingRequest, 
    PricingResponseData, 
    CostBreakdown, 
    PricingExplanation, 
    ArtisanMessage,
    PricingSimulationRequest,
    PricingSimulationResponseData
)
from app.ai.pricing.market import BaseMarketDataProvider
from app.ai.pricing.ml import BasePricePredictionModel
from app.ai.llm.base import BaseLLMProvider

CRAFT_COMPLEXITY_FACTORS = {
    "low": 1.00,
    "medium": 1.08,
    "high": 1.15
}

class PricingEngine:
    def __init__(
        self,
        market_provider: BaseMarketDataProvider,
        ml_provider: BasePricePredictionModel,
        llm_provider: BaseLLMProvider
    ):
        self.market_provider = market_provider
        self.ml_provider = ml_provider
        self.llm_provider = llm_provider
        
        # Default Weights
        self.COST_WEIGHT = 0.40
        self.MARKET_WEIGHT = 0.60
        self.ML_WEIGHT = 0.0

    async def suggest_price(self, request: PricingRequest) -> PricingResponseData:
        # 1. Base Cost Calculation
        material = request.material_cost
        labor_hours = request.labor_hours or 0.0
        labor_rate = request.labor_cost or 0.0 # Treating labor_cost as rate if hours provided, or total
        if request.labor_hours and request.labor_cost:
            labor = request.labor_hours * request.labor_cost
        else:
            labor = request.labor_cost or 0.0
            
        production = request.production_cost
        packaging = request.packaging_cost
        transport = request.transportation_cost
        
        total_base_cost = material + labor + production + packaging + transport
        
        cost_breakdown = CostBreakdown(
            material=material,
            labor=labor,
            packaging=packaging,
            transportation=transport,
            production=production,
            total_base_cost=total_base_cost
        )
        
        # 2. Minimum Price based on requested margin
        margin = request.desired_margin
        min_price = total_base_cost * (1 + margin)
        
        # 3. Apply Craft Complexity Factor
        complexity = request.customization_level.lower()
        factor = CRAFT_COMPLEXITY_FACTORS.get(complexity, 1.0)
        cost_plus_price = min_price * factor
        
        # 4. Market Analysis
        comparables = await self.market_provider.get_comparables(
            category=request.product_category or "",
            subcategory=request.subcategory,
            material=request.materials[0] if request.materials else None,
            region=request.region
        )
        market_stats = await self.market_provider.get_market_statistics(comparables)
        
        # 5. ML Model Check
        ml_prediction = await self.ml_provider.predict(request.model_dump())
        ml_confidence = await self.ml_provider.confidence(request.model_dump())
        
        # 6. Hybrid Price Calculation
        recommended_price = cost_plus_price
        maximum_price = cost_plus_price * 1.2
        
        confidence = 0.4 # Baseline for just having costs
        if material > 0 and labor > 0:
            confidence = 0.6
            
        if market_stats:
            # Adjust weights if market data exists
            market_median = market_stats.median
            recommended_price = (cost_plus_price * self.COST_WEIGHT) + (market_median * self.MARKET_WEIGHT)
            maximum_price = max(market_stats.max, recommended_price * 1.1)
            min_price = max(min_price, market_stats.min)
            
            # Boost confidence based on sample size
            if market_stats.sample_size > 5:
                confidence = 0.8
            elif market_stats.sample_size > 2:
                confidence = 0.7
                
        if ml_prediction and ml_confidence > 0.5:
            # Redistribute if ML is actually confident
            recommended_price = (cost_plus_price * 0.3) + (market_stats.median * 0.4) + (ml_prediction * 0.3)
            confidence = min(confidence + 0.1, 0.95)
            
        confidence_level = "high" if confidence >= 0.75 else "medium" if confidence >= 0.5 else "low"
        
        # 7. Generate Explanations
        explanation = PricingExplanation(
            cost_basis=f"₹{total_base_cost:.2f}",
            market_basis=f"Comparable products range from ₹{market_stats.min:.2f} to ₹{market_stats.max:.2f}." if market_stats else "Limited market data available.",
            labor_contribution=f"₹{labor:.2f}",
            recommended_margin=f"{margin*100}%",
            final_reason="The recommended price balances your production costs and desired margin with currently available market comparable prices."
        )
        
        # 8. Artisan Message Formatting
        message_en = f"Recommended price: ₹{recommended_price:.0f}. Suggested range: ₹{min_price:.0f} - ₹{maximum_price:.0f}. Based on material costs (₹{material}), your labor (₹{labor}), and market prices."
        message_hi = f"अनुमानित कीमत: ₹{recommended_price:.0f}। सुझावित सीमा: ₹{min_price:.0f} - ₹{maximum_price:.0f}। यह आपके सामग्री (₹{material}) और मेहनत (₹{labor}) पर आधारित है।"
        message_mr = f"अंदाजे किंमत: ₹{recommended_price:.0f}. योग्य विक्री किंमत: ₹{min_price:.0f} - ₹{maximum_price:.0f}. हे साहित्य (₹{material}) आणि तुमच्या श्रमावर (₹{labor}) आधारित आहे."
        
        # Fallback to LLM translation if needed, but we hardcode a template here for speed and reliability, matching the requirement
        artisan_message = ArtisanMessage(
            english=message_en,
            hindi=message_hi,
            marathi=message_mr
        )
        
        return PricingResponseData(
            minimum_price=round(min_price, 2),
            recommended_price=round(recommended_price, 2),
            maximum_price=round(maximum_price, 2),
            confidence=round(confidence, 2),
            confidence_level=confidence_level,
            market_data=market_stats,
            cost_breakdown=cost_breakdown,
            explanation=explanation,
            artisan_message=artisan_message
        )

    def simulate_price(self, request: PricingSimulationRequest) -> PricingSimulationResponseData:
        labor = 0.0
        if request.labor_hours and request.labor_cost:
            labor = request.labor_hours * request.labor_cost
        else:
            labor = request.labor_cost or 0.0
            
        estimated_cost = request.material_cost + labor + request.packaging_cost + request.transportation_cost
        estimated_profit = request.selling_price - estimated_cost
        margin = estimated_profit / estimated_cost if estimated_cost > 0 else 1.0
        
        # Market position estimation based on arbitrary threshold since we don't fetch full market data here
        # In a real app we might pass market_median to this simulation
        position = "competitive"
        if margin < 0.1:
            position = "too_low"
        elif margin > 0.6:
            position = "premium"
            
        return PricingSimulationResponseData(
            selling_price=request.selling_price,
            estimated_cost=round(estimated_cost, 2),
            estimated_profit=round(estimated_profit, 2),
            margin=round(margin, 3),
            market_position=position
        )
