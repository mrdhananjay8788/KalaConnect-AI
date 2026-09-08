# Evaluation Metrics

To ensure the AI Multilingual Auto-Cataloger performs well, we track the following metrics during development and QA:

1. **Speech Transcription Accuracy (WER - Word Error Rate):** Evaluates how accurately the regional language audio is converted to text.
2. **Language Detection Accuracy:** The percentage of inputs where the correct language code is assigned.
3. **Product Extraction Accuracy:** Measures how many actual product attributes (material, color, price) are successfully extracted vs. missed.
4. **Missing-field Detection Accuracy:** How well the AI identifies that important data (like price) was NOT mentioned by the user.
5. **Translation Quality:** Manual rating (1-5) on how well the system preserves cultural terms instead of literal unnatural translations.
6. **Description Quality:** Subjective grading on professional tone and lack of hallucinations.
7. **Hallucination Rate:** The percentage of outputs where the AI invents information (e.g., claiming a product is silk when material was never mentioned).
8. **Average Processing Time:** The end-to-end latency for a voice request (Target < 5 seconds).
9. **AI API Cost per Catalog:** Tracking token usage to keep catalog generation cost under acceptable margins.

## Evaluation Dataset
We will maintain a dataset of at least:
- 20 Marathi examples (voice + text)
- 20 Hindi examples (voice + text)
- 10 English examples
*(Ensure no real PII/Personal Information is used)*
