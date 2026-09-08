from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated

from app.api.dependencies import get_search_engine, get_vector_store
from app.services.search_engine import SearchEngine
from app.ai.search.recommendation import BaseRecommendationProvider, MockRecommendationProvider
from app.ai.search.vector_store import BaseVectorStore
from app.schemas.search import SearchResponse, SimilarProductResponse, SearchSuggestionResponse

router = APIRouter()

def get_recommendation_provider(vector_store: BaseVectorStore = Depends(get_vector_store)) -> BaseRecommendationProvider:
    return MockRecommendationProvider(vector_store)

@router.post("/products", response_model=SearchResponse)
async def search_products(
    query: Annotated[str, Query(..., min_length=2, max_length=500)],
    language: Annotated[str, Query(max_length=10)] = "en",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 20,
    search_engine: SearchEngine = Depends(get_search_engine)
):
    """Semantic product search with hard filters."""
    result = await search_engine.search_products(query, language, page, page_size)
    return SearchResponse(success=True, data=result)

@router.get("/products/{product_id}/similar", response_model=SimilarProductResponse)
async def get_similar_products(
    product_id: Annotated[str, Path(..., max_length=50)],
    recommendation_provider: BaseRecommendationProvider = Depends(get_recommendation_provider)
):
    """Get similar products via vector embeddings."""
    result = await recommendation_provider.get_similar_products(product_id)
    return SimilarProductResponse(success=True, data={"products": result})

@router.get("/suggestions", response_model=SearchSuggestionResponse)
async def search_suggestions(
    q: str = Query(..., min_length=1)
):
    """Autocomplete suggestions (Mock for Phase 5)."""
    # Simple mock response
    suggestions = [
        f"{q} basket",
        f"{q} handicrafts",
        f"{q} corporate gifts"
    ]
    return SearchSuggestionResponse(success=True, data=suggestions)
