# Phase 3: AI Image Intelligence & E-commerce Image Studio

## Overview
Phase 3 extends the KalaConnect-AI backend to process mobile photographs taken by artisans and automatically format them into professional e-commerce product shots.

## Image Processing Pipeline
The `ImageService` orchestrates the following flow:
1. **Validation**: Enforces strict MIME type checks, size constraints (<15MB), and corruption detection using `Pillow`.
2. **Quality Analysis**: Computes `brightness`, `contrast`, `sharpness`, and `blur_detected` using image statistics. Provides actionable recommendations.
3. **Vision Analysis**: Identifies products, objects, and visual attributes using an external vision model (GPT-4o in production, Mock in development).
4. **Segmentation**: Detects if the background is cluttered. If so, removes the background.
5. **Enhancement**: Mildly adjusts lighting and contrast. Crucially, maintains **product authenticity**.
6. **Formatting**: Resizes, pads, and saves the final output as a standardized `WEBP` file (1200x1200px default) for fast e-commerce loading.
7. **Catalog Integration**: Associates the processed image with the specific `product_id`.

## Provider Abstraction
To avoid vendor lock-in, image processing tools are abstracted:
- `BaseVisionProvider`: For object detection and attribute extraction.
- `BaseSegmentationProvider`: For background removal (supports optional `rembg` for local real-time segmentation).
- `BaseImageEnhancementProvider`: For lighting and formatting.

## Storage
Images are temporarily saved to local disk for development:
- `data/images/original/`: Uploaded raw files.
- `data/images/processed/`: Web-ready edited files.
- `data/images/temporary/`: Intermediate files during processing.
A cleanup mechanism is implemented in `StorageService`.

## Security & Privacy
- **No Path Traversal**: Files are saved with safe `uuid` identifiers.
- **Data Minimization**: No sensitive PII is stored. Original EXIF data is implicitly stripped during processing and saving via `Pillow`.
- **Authenticity Rules**: The AI is strictly instructed to NEVER change product colors, hide defects, or generate fake materials. The enhancement is strictly limited to lighting and background editing.
