from app.api.routes.health import router as health_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.voice import router as voice_router
from app.api.routes.image import router as image_router
from app.api.routes.pricing import router as pricing_router
from app.api.routes.search import router as search_router

__all__ = ["health_router", "catalog_router", "voice_router", "image_router", "pricing_router", "search_router"]
