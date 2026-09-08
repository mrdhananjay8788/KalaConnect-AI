import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_catalog_from_text_marathi():
    response = client.post("/api/v1/catalog/from-text", json={
        "text": "ही पैठणी साडी आहे. ती रेशमापासून बनवली आहे.",
        "language": "mr"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    catalog_data = data["data"]
    
    # Assert extraction
    product = catalog_data["product"]
    assert product["product_name"] == "Paithani Saree"
    assert "Silk" in product["material"]
    assert "dimensions" in product["missing_fields"]
    
    # Assert descriptions
    descriptions = catalog_data["descriptions"]
    assert descriptions["hindi"] is not None
    assert descriptions["english"] is not None
    
    # Assert keywords
    keywords = catalog_data["keywords"]
    assert len(keywords) > 0
    assert "handcrafted" in keywords
    
    # Assert missing fields list
    missing = catalog_data["missing_fields"]
    assert len(missing) > 0
    assert any(m["field"] == "dimensions" for m in missing)
    
    # Assert next question
    assert catalog_data["next_question"] is not None
    assert "किंमत" in catalog_data["next_question"] # Since it's Marathi

def test_catalog_from_text_empty():
    response = client.post("/api/v1/catalog/from-text", json={
        "text": "   ",
        "language": "en"
    })
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "error" in data
