import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_test_image(format="JPEG", size=(100, 100), color="red"):
    img = Image.new("RGB", size, color=color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

def test_image_quality_endpoint():
    img_bytes = create_test_image(format="JPEG")
    
    response = client.post(
        "/api/v1/image/quality",
        files={"image": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "quality_score" in data["data"]
    assert data["data"]["resolution"]["width"] == 100

def test_image_process_pipeline():
    img_bytes = create_test_image(format="PNG", size=(200, 200))
    
    response = client.post(
        "/api/v1/image/process",
        files={"image": ("test.png", img_bytes, "image/png")},
        data={"product_id": "PRD-TEST-123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    response_data = data["data"]
    assert response_data["product_id"] == "PRD-TEST-123"
    assert "original_image" in response_data
    assert "processed_image" in response_data
    assert "metadata" in response_data
    assert response_data["metadata"]["processing_status"] == "completed"
    
    # Mock vision should return handcraft
    assert response_data["vision_attributes"]["category"] == "handicraft"

def test_image_validation_invalid_type():
    response = client.post(
        "/api/v1/image/process",
        files={"image": ("test.txt", b"not an image", "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Unsupported image format" in response.json()["error"]["message"]

def test_image_validation_corrupted_file():
    response = client.post(
        "/api/v1/image/process",
        files={"image": ("test.jpg", b"corrupted bytes here", "image/jpeg")}
    )
    
    assert response.status_code == 400
    assert "Corrupted image file" in response.json()["error"]["message"]
