import re
from typing import List, Dict, Any, Tuple
from app.schemas.search import (
    SearchFilters, 
    QueryUnderstanding, 
    SearchResult, 
    SearchResponseData,
    SimilarProduct
)
from app.ai.search.embedding import BaseEmbeddingProvider
from app.ai.search.vector_store import BaseVectorStore
from app.ai.llm.base import BaseLLMProvider

class SearchEngine:
    def __init__(
        self,
        embedding_provider: BaseEmbeddingProvider,
        vector_store: BaseVectorStore,
        llm_provider: BaseLLMProvider
    ):
        self.embedding = embedding_provider
        self.store = vector_store
        self.llm = llm_provider
        
        # Hybrid Search Weights
        self.SEMANTIC_WEIGHT = 0.55
        self.KEYWORD_WEIGHT = 0.20
        self.FILTER_WEIGHT = 0.15
        self.BUSINESS_WEIGHT = 0.10

    async def _understand_query(self, query: str, lang: str) -> Tuple[QueryUnderstanding, SearchFilters]:
        """
        Simulates extracting filters and intent from a natural language string.
        In a real application, we would use the LLM to parse this into JSON.
        """
        query_lower = query.lower()
        
        # 1. Price Extraction
        price_max = None
        price_match = re.search(r'(under|below)\s*(?:rs|rupees|₹)?\s*(\d+)', query_lower)
        if price_match:
            price_max = float(price_match.group(2))
            
        # 2. Quantity Extraction
        quantity = None
        qty_match = re.search(r'(\d+)\s*(units|pieces|baskets|sarees|items)?', query_lower)
        if qty_match:
            quantity = int(qty_match.group(1))
            
        # 3. Category/Material keyword matching for the mock
        category = None
        if "basket" in query_lower or "टोपल्या" in query_lower or "टोकरियां" in query_lower:
            category = "basket"
        elif "saree" in query_lower:
            category = "textile"
            
        materials = []
        if "bamboo" in query_lower or "बांबूच्या" in query_lower or "बांस" in query_lower:
            materials.append("bamboo")
            
        intent = "BULK_PURCHASE" if quantity and quantity >= 50 else "PRODUCT_SEARCH"
        
        filters = SearchFilters(
            category=category,
            material=materials,
            price_max=price_max,
            quantity=quantity,
            intended_use="corporate gifting" if "corporate" in query_lower else None
        )
        
        understanding = QueryUnderstanding(
            original=query,
            normalized=query_lower.strip(),
            language=lang,
            intent=intent,
            semantic_query=query # The vector text
        )
        
        return understanding, filters

    async def _score_results(self, candidates: List[Dict[str, Any]], query_norm: str) -> List[SearchResult]:
        scored_results = []
        for c in candidates:
            semantic_score = 0.8 # Mock baseline
            keyword_score = 0.0
            filter_match = 1.0
            
            # Simple keyword overlap simulation
            words = set(query_norm.split())
            keywords = set([k.lower() for k in c.get("keywords", [])])
            overlap = words.intersection(keywords)
            if overlap:
                keyword_score = len(overlap) / len(words)
                
            availability_score = min(c["availability"] / 100, 1.0) # Business logic
            
            final_score = (
                (semantic_score * self.SEMANTIC_WEIGHT) + 
                (keyword_score * self.KEYWORD_WEIGHT) + 
                (filter_match * self.FILTER_WEIGHT) + 
                (availability_score * self.BUSINESS_WEIGHT)
            )
            
            reasons = []
            if overlap:
                reasons.append(f"Matches keywords: {', '.join(overlap)}")
            if c.get("price") and c.get("price") <= 500: # Example reason
                reasons.append("Price is below ₹500")
            if c["availability"] >= 50:
                reasons.append(f"{c['availability']} units available")
                
            scored_results.append(SearchResult(
                product_id=c["product_id"],
                product_name=c["product_name"],
                price=c["price"],
                availability=c["availability"],
                similarity=round(semantic_score, 2),
                relevance_score=round(final_score, 2),
                match_reasons=reasons
            ))
            
        scored_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return scored_results

    async def search_products(self, query: str, language: str = "en", page: int = 1, page_size: int = 20) -> SearchResponseData:
        # Prevent huge pages
        page_size = min(page_size, 50)
        
        # 1. Understand Query
        understanding, filters = await self._understand_query(query, language)
        
        # 2. Get Embedding
        query_embedding = await self.embedding.get_embedding(understanding.semantic_query)
        
        # 3. Vector Store Search with Hard Filters
        candidates = await self.store.search(
            query_embedding=query_embedding,
            filters=filters.model_dump(exclude_none=True),
            limit=100
        )
        
        is_alternative = False
        
        # 4. Empty Search Handling
        if not candidates:
            # Relax hard filters (drop price_max, drop category) to find alternatives
            relaxed_filters = filters.model_copy()
            relaxed_filters.price_max = None
            relaxed_filters.category = None
            
            candidates = await self.store.search(
                query_embedding=query_embedding,
                filters=relaxed_filters.model_dump(exclude_none=True),
                limit=100
            )
            is_alternative = True
            
        # 5. Score & Rank
        scored_results = await self._score_results(candidates, understanding.normalized)
        
        # 6. Pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = scored_results[start:end]
        
        message = None
        if is_alternative:
            message = f"No exact matches found for your criteria. Here are similar options:"
        
        return SearchResponseData(
            query=understanding,
            filters=filters,
            results=paginated_results,
            total_results=len(scored_results),
            is_alternative=is_alternative,
            message=message
        )

