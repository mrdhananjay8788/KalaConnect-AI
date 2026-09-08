import json
import os
from typing import List, Dict, Any, Optional

from app.schemas.matching import BuyerMatchRequest, ArtisanMatchResult, MatchResponseData, MatchPreviewData, SplitOrderResult, SplitOrderAllocation
from app.schemas.artisan import ArtisanProfile
from app.ai.matching.extraction import BaseRequirementExtractionProvider
from app.ai.matching.feasibility import BaseDeliveryFeasibilityProvider

class MatchingEngine:
    def __init__(
        self,
        extractor: BaseRequirementExtractionProvider,
        feasibility: BaseDeliveryFeasibilityProvider,
        artisans_path: str = "data/matching/artisans.json"
    ):
        self.extractor = extractor
        self.feasibility = feasibility
        self.artisans_path = artisans_path
        self._artisans: List[ArtisanProfile] = []
        self._load_artisans()
        
        # Configurable weights (usually from config.py)
        self.weights = {
            "semantic": 0.30,
            "capacity": 0.20,
            "price": 0.15,
            "delivery": 0.10,
            "customization": 0.10,
            "region": 0.05,
            "reliability": 0.05,
            "profile": 0.05
        }

    def _load_artisans(self):
        if os.path.exists(self.artisans_path):
            with open(self.artisans_path, "r") as f:
                data = json.load(f)
                self._artisans = [ArtisanProfile(**item) for item in data]

    async def _evaluate_artisan(self, artisan: ArtisanProfile, req: BuyerMatchRequest) -> Optional[ArtisanMatchResult]:
        # 1. Hard Constraints
        # Customization
        if req.customization_required and not artisan.customization_supported:
            return None
            
        # Category
        if req.product_category and req.product_category not in artisan.categories:
            return None
            
        # Capacity
        if not req.allow_split_order and req.quantity and artisan.available_quantity < req.quantity:
            return None
            
        # Budget
        if req.budget_max and artisan.price_range:
            min_price = artisan.price_range[0]
            if min_price > req.budget_max:
                return None
                
        # 2. Feasibility Calculations
        delivery_days = None
        if req.delivery_location:
            delivery_days = await self.feasibility.estimate_delivery_days(
                artisan.region, req.delivery_location, req.quantity or 1, artisan.average_lead_time_days
            )
            if req.required_delivery_days and delivery_days > req.required_delivery_days:
                return None # Hard constraint
                
        # 3. Scoring
        semantic_score = 0.9 # Mock semantic match 
        
        # Capacity Score
        quantity_score = 1.0
        if req.quantity and req.quantity > artisan.available_quantity:
            quantity_score = artisan.available_quantity / req.quantity
            
        # Price Score
        price_score = 1.0
        est_price = artisan.price_range[0] if artisan.price_range else None
        if req.budget_max and est_price:
            price_score = max(0, 1 - (est_price / req.budget_max)) + 0.5 # basic logic
            price_score = min(1.0, price_score)
            
        # Delivery Score
        delivery_score = 1.0
        if req.required_delivery_days and delivery_days:
            delivery_score = max(0, 1 - (delivery_days / req.required_delivery_days)) + 0.5
            delivery_score = min(1.0, delivery_score)
            
        customization_score = 1.0 if (req.customization_required and artisan.customization_supported) else 0.8
        region_score = 1.0 if artisan.region == req.delivery_location else 0.5
        reliability_score = artisan.reliability_score if artisan.reliability_score is not None else 0.5 # Neutral for new artisans
        
        match_score = (
            semantic_score * self.weights["semantic"] +
            quantity_score * self.weights["capacity"] +
            price_score * self.weights["price"] +
            delivery_score * self.weights["delivery"] +
            customization_score * self.weights["customization"] +
            region_score * self.weights["region"] +
            reliability_score * self.weights["reliability"] +
            artisan.profile_completeness * self.weights["profile"]
        )
        
        # Confidence
        confidence = 0.8
        if artisan.reliability_score is None:
            confidence -= 0.1
        if not req.budget_max:
            confidence -= 0.1
            
        confidence_level = "high" if confidence > 0.75 else "medium"
        
        # Explanation
        reasons = []
        if quantity_score == 1.0:
            reasons.append(f"✓ Can supply {req.quantity} units")
        elif quantity_score > 0:
            reasons.append(f"✓ Can partially supply {artisan.available_quantity} units")
            
        if est_price and req.budget_max and est_price <= req.budget_max:
            reasons.append("✓ Price range fits buyer budget")
            
        if req.customization_required and artisan.customization_supported:
            reasons.append("✓ Supports custom branding")
            
        if delivery_days and req.required_delivery_days and delivery_days <= req.required_delivery_days:
            reasons.append(f"✓ Estimated delivery: {delivery_days} days (meets deadline)")
            
        warnings = []
        if artisan.reliability_score is None:
            warnings.append("⚠ New artisan, historical reliability unproven")
            
        if not req.delivery_location:
            warnings.append("⚠ Shipping cost requires confirmation")

        explanation = "\n".join(reasons)
            
        return ArtisanMatchResult(
            artisan_id=artisan.artisan_id,
            product_id=artisan.product_ids[0] if artisan.product_ids else None,
            match_score=round(match_score, 2),
            confidence=round(confidence, 2),
            confidence_level=confidence_level,
            semantic_score=round(semantic_score, 2),
            quantity_score=round(quantity_score, 2),
            price_score=round(price_score, 2),
            delivery_score=round(delivery_score, 2),
            customization_score=round(customization_score, 2),
            region_score=round(region_score, 2),
            reliability_score=round(reliability_score, 2),
            hard_constraints_passed=True,
            estimated_quantity=artisan.available_quantity,
            estimated_price=est_price,
            estimated_delivery_days=delivery_days,
            explanation=explanation,
            warnings=warnings
        )

    async def preview_matches(self, query: str) -> MatchPreviewData:
        req = await self.extractor.extract_requirements(query)
        eligible = 0
        budget = 0
        capacity = 0
        delivery = 0
        high = 0
        
        for artisan in self._artisans:
            # simple mock preview stats
            res = await self._evaluate_artisan(artisan, req)
            if res:
                eligible += 1
                if res.match_score > 0.8: high += 1
                if res.price_score == 1.0: budget += 1
                if res.quantity_score == 1.0: capacity += 1
                if res.delivery_score == 1.0: delivery += 1
                
        return MatchPreviewData(
            eligible_artisans=eligible,
            high_quality_matches=high,
            budget_compatible=budget,
            capacity_compatible=capacity,
            delivery_compatible=delivery
        )

    async def find_matches(self, query: str, allow_split: Optional[bool] = None) -> MatchResponseData:
        req = await self.extractor.extract_requirements(query)
        if allow_split is not None:
            req.allow_split_order = allow_split
            
        matches = []
        for artisan in self._artisans:
            res = await self._evaluate_artisan(artisan, req)
            if res:
                matches.append(res)
                
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        split_result = None
        if req.allow_split_order and req.quantity:
            # Check if we need a split
            if not matches or (matches and matches[0].estimated_quantity < req.quantity):
                # Greedy split algorithm
                unfilled = req.quantity
                allocations = []
                for m in matches:
                    if unfilled <= 0:
                        break
                    take = min(m.estimated_quantity, unfilled)
                    if take > 0:
                        allocations.append(SplitOrderAllocation(artisan_id=m.artisan_id, quantity=take))
                        unfilled -= take
                        
                allocated = req.quantity - unfilled
                split_result = SplitOrderResult(
                    required_quantity=req.quantity,
                    allocated_quantity=allocated,
                    artisans=allocations
                )

        return MatchResponseData(
            request_id="REQ-001",
            matches=matches,
            split_order_option=split_result
        )
