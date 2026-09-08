# Phase 3 Evaluation Metrics

To ensure the AI Image Studio performs well and maintains artisan authenticity, we track:

1. **Image Quality Score Accuracy**: Human validation of the calculated quality score vs actual perceived quality.
2. **Product Detection Accuracy**: Does the vision model correctly detect the primary object bounding box?
3. **Segmentation Quality (IoU)**: Intersection over Union for background removal against a ground-truth dataset.
4. **Processing Time**: E2E latency. Target < 10 seconds per image.
5. **Image Size Reduction**: Compare original upload size to final WEBP output. Target: >50% reduction in bytes for web.
6. **Vision Attribute Accuracy**: True positive rate of detected materials/colors vs actual text description.
7. **False Attribute Rate**: How often does the vision model hallucinate a material that is not present?
8. **Enhancement Failure Rate**: Number of images that look artificially modified or discolored.

## Evaluation Dataset
We will collect a sample set containing:
- 10 bright, well-composed photos.
- 10 dark/blurry mobile photos.
- 10 photos with heavily cluttered backgrounds.
- 5 corrupted or edge-case images (wrong formats).
