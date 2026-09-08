# Phase 2: Multilingual AI Auto-Cataloger

## Overview
Phase 2 enhances the KalaConnect-AI backend with a Multilingual Auto-Cataloger. The system can process voice or text input from artisans in regional Indian languages (Marathi, Hindi, English) and automatically generate a complete, structured e-commerce product catalog.

## Pipeline
The processing pipeline executes the following stages sequentially in a highly modular fashion:
1. **Audio/Voice Processing (Speech-to-Text):** Validates and transcribes uploaded audio files (or processes direct text input).
2. **Language Detection:** Detects the language of the provided text.
3. **Product Information Extraction:** Uses strict JSON schema enforcement with LLMs to extract fields such as `product_name`, `material`, `color`, `price`, etc. Identifies missing fields.
4. **Missing Information Detection:** Adds importance levels (e.g. `price` is high importance) to fields that the AI couldn't extract.
5. **Translation:** Translates descriptions between Marathi, Hindi, and English while preserving cultural terminology.
6. **Description Generation:** Generates a professional e-commerce product description in the target languages.
7. **SEO Keyword Generation:** Extracts 5-10 SEO-optimized keywords.
8. **Follow-up Question Generation:** Formulates a short, localized question in the artisan's language to ask for missing information.

## API Usage

### `POST /api/v1/catalog/from-voice`
Accepts an audio file via `multipart/form-data`.

**Request:**
- `audio`: The audio file (`.wav`, `.mp3`, etc. Max 10MB)
- `language_preference`: (Optional) The preferred language for the response/question.

**Response:**
Returns a `CatalogResponse` with transcription data, structured product data, missing fields, generated descriptions, and the next question.

### `POST /api/v1/catalog/from-text`
Accepts a JSON payload for text-based catalog generation.

**Request:**
```json
{
  "text": "ही हाताने बनवलेली बांबूची टोपली आहे.",
  "language": "mr"
}
```

## AI Provider Configuration
The system uses the `AI_MODE` environment variable:
- `AI_MODE=mock`: (Default) Uses mock providers for fast, deterministic testing without API keys.
- `AI_MODE=production`: Uses `Real` providers (OpenAI Whisper, GPT-4o-mini). Ensure `OPENAI_API_KEY` is set in your `.env` file.

## Known Limitations
- Background noise in voice recordings may reduce transcription accuracy.
- Extremely dialect-heavy speech might occasionally misclassify the language.
- The system focuses on text/voice pipelines. Complex image+voice simultaneous integration is scheduled for future phases.
