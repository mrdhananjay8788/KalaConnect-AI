from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import settings
from app.core.exceptions import APIException
from app.core.logging import logger

# Import routes
from app.api.routes import health, catalog, voice, image, pricing, search, matching

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Exception handler
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred."
            }
        }
    )

# Middleware for basic logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} - Method: {request.method} - "
        f"Status: {response.status_code} - Processing Time: {process_time:.4f}s"
    )
    return response

# Include routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(catalog.router, prefix=f"{settings.API_V1_STR}/catalog", tags=["Catalog"])
app.include_router(voice.router, prefix=f"{settings.API_V1_STR}/voice", tags=["Voice"])
app.include_router(image.router, prefix=f"{settings.API_V1_STR}/image", tags=["Image"])
app.include_router(pricing.router, prefix=f"{settings.API_V1_STR}/pricing", tags=["Pricing"])
app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search", tags=["Search"])
app.include_router(matching.router, prefix=f"{settings.API_V1_STR}/matching", tags=["Matching"])
