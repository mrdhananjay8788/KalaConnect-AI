# API Documentation

All API endpoints are versioned under `/api/v1/`.

## GET `/api/v1/`
Health check endpoint.
Response:
```json
{
  "status": "healthy",
  "service": "artisan-ai-backend"
}
```

## POST `/api/v1/catalog/from-voice` (Phase 2)
Processes an audio file containing an artisan's natural description and generates a complete structured product catalog.
Accepts `multipart/form-data`:
- `audio`: file (required, Max 10MB)
- `language_preference`: string (optional, e.g., 'mr', 'hi', 'en')

## POST `/api/v1/catalog/from-text` (Phase 2)
Generates a complete structured product catalog from a natural language text description.
Accepts `application/json`:
```json
{
  "text": "ही हाताने बनवलेली बांबूची टोपली आहे.",
  "language": "mr"
}
```

## POST `/api/v1/image/analyze` (Phase 3)
Runs image quality validation and vision attribute extraction without background removal.
Accepts `multipart/form-data`:
- `image`: file (required, Max 15MB, JPG/PNG/WEBP)

## POST `/api/v1/pricing/suggest` (Phase 4)
Suggests a dynamically computed product price based on costs, labor, and comparable market data.
Accepts JSON:
```json
{
  "product_id": "PRD-001",
  "material_cost": 400,
  "labor_hours": 8,
  "labor_cost": 75,
  "desired_margin": 0.25,
  "region": "Maharashtra",
  "product_category": "Handicraft"
}
```

## POST `/api/v1/pricing/simulate` (Phase 4)
Simulates profits, margins, and market competitiveness based on a user-suggested selling price.

## POST `/api/v1/search/products` (Phase 5)
Executes a multilingual semantic search with intent parsing and hybrid ranking.

## POST `/api/v1/matching/buyers` (Phase 6)
Analyzes natural language B2B queries extracting hard logistics/budget logic and returning scored subset mappings. Supports `allow_split_order` boolean payload for massive B2B quantities mapped across marginalized groups.

## POST `/api/v1/matching/preview` (Phase 6)
Previews eligible capacity/candidate totals before committing to a costly deep B2B retrieval pipeline.



## GET `/api/v1/search/products/{product_id}/similar` (Phase 5)
Recommends products by checking the nearest vector neighbors within the catalog database.

## GET `/api/v1/search/suggestions` (Phase 5)
Generates autocomplete search suggestions.

## POST `/api/v1/image/process` (Phase 3)
Runs the complete image processing pipeline including segmentation, enhancement, and e-commerce formatting.
Accepts `multipart/form-data`:
- `image`: file (required, Max 15MB, JPG/PNG/WEBP)
- `product_id`: string (optional, to associate with Phase 2 data)

## POST `/api/v1/image/quality` (Phase 3)
Calculates and returns only the basic image quality metrics.
Accepts `multipart/form-data`:
- `image`: file (required)

## POST `/api/v1/image/remove-background` (Phase 3)
Removes the background from the image and returns a transparent PNG path.
Accepts `multipart/form-data`:
- `image`: file (required)

## POST `/api/v1/catalog/generate` (Phase 1)
Generates a structured catalog product from various inputs.
Accepts `multipart/form-data`:
- `artisan_id`: string (required)
- `text_description`: string (optional)
- `image`: file (optional)
- `voice`: file (optional)

## POST `/api/v1/voice/transcribe`
Transcribes an audio file into text.
Accepts `multipart/form-data`:
- `voice`: file (required)

## POST `/api/v1/image/analyze`
Extracts visual features from an image.
Accepts `multipart/form-data`:
- `image`: file (required)

## POST `/api/v1/pricing/suggest`
Suggests pricing details given a JSON object of product features.
