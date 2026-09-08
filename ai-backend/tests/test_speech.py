import pytest
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_catalog_from_voice_valid():
    # Create a dummy valid audio file
    file_content = b"fake audio data for testing" * 100
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/catalog/from-voice",
        files={"audio": ("test.wav", file, "audio/wav")},
        data={"language_preference": "mr"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    catalog_data = data["data"]
    
    # Because mock speech provider returns text with "पैठणी साडी", it should map to Paithani Saree
    assert catalog_data["product"]["product_name"] == "Paithani Saree"
    assert catalog_data["transcription"]["language"] == "mr"

def test_catalog_from_voice_invalid_format():
    file_content = b"fake data"
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/catalog/from-voice",
        files={"audio": ("test.txt", file, "text/plain")},
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Unsupported audio format" in data["error"]["message"]

def test_catalog_from_voice_empty():
    file_content = b""
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/catalog/from-voice",
        files={"audio": ("empty.wav", file, "audio/wav")},
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Empty audio" in data["error"]["message"]

def test_catalog_from_voice_too_large():
    # Max size is 10MB
    file_content = b"0" * (10 * 1024 * 1024 + 10)
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/catalog/from-voice",
        files={"audio": ("large.wav", file, "audio/wav")},
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "too large" in data["error"]["message"]
