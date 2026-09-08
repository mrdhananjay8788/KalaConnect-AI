from abc import ABC, abstractmethod
from app.schemas.matching import BuyerMatchRequest
import re

class BaseRequirementExtractionProvider(ABC):
    @abstractmethod
    async def extract_requirements(self, query: str) -> BuyerMatchRequest:
        """Extract structured JSON from natural language."""
        pass

class MockRequirementExtractionProvider(BaseRequirementExtractionProvider):
    async def extract_requirements(self, query: str) -> BuyerMatchRequest:
        query_lower = query.lower()
        
        req = BuyerMatchRequest(
            query=query,
            allow_split_order=False
        )
        
        # Quantity
        qty_match = re.search(r'(\d+)\s*(units|pieces|baskets|sarees|items)?', query_lower)
        if qty_match:
            req.quantity = int(qty_match.group(1))
            
        # Price / Budget
        price_match = re.search(r'(under|below)\s*(?:rs|rupees|₹)?\s*(\d+)', query_lower)
        if price_match:
            req.budget_max = float(price_match.group(2))
            
        # Category / Material
        if "basket" in query_lower or "टोपल्या" in query_lower or "टोकरियां" in query_lower:
            req.product_category = "basket"
        if "bamboo" in query_lower or "बांबूच्या" in query_lower or "बांस" in query_lower:
            req.materials.append("bamboo")
            
        # Location
        if "pune" in query_lower:
            req.delivery_location = "Pune"
        elif "mumbai" in query_lower:
            req.delivery_location = "Mumbai"
            
        # Days deadline
        days_match = re.search(r'within (\d+) days', query_lower)
        if days_match:
            req.required_delivery_days = int(days_match.group(1))
            
        # Customization
        if "branding" in query_lower or "logo" in query_lower or "custom" in query_lower:
            req.customization_required = True
            req.customization_description = "custom branding/logo"
            
        return req
