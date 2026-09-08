import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pricing_suggest_success():
    payload = {
        "product_id": "PRD-TEST",
        "product_category": "Handicraft",
        "subcategory": "Basket",
        "craft_type": "Bamboo Weaving",
        "materials": ["Bamboo"],
        "material_cost": 400,
        "labor_hours": 8,
        "labor_cost": 75,
        "packaging_cost": 30,
        "transportation_cost": 50,
        "desired_margin": 0.25,
        "region": "Maharashtra"
    }

    response = client.post("/api/v1/pricing/suggest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    result = data["data"]
    assert "minimum_price" in result
    assert "recommended_price" in result
    assert "maximum_price" in result
    assert "confidence" in result
    
    # 400 + (8*75) + 30 + 50 = 400 + 600 + 80 = 1080 (Total Base Cost)
    # min_price = 1080 * 1.25 = 1350
    assert result["cost_breakdown"]["total_base_cost"] == 1080.0
    # The actual min price returned may be adjusted by market.min (which is 2400)
    # So min_price could be 2400 in the result due to market min.
    assert result["minimum_price"] >= 1350.0

def test_pricing_suggest_validation_error():
    payload = {
        "product_id": "PRD-TEST",
        "material_cost": -100, # Invalid
        "desired_margin": 1.5  # Invalid
    }

    response = client.post("/api/v1/pricing/suggest", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_pricing_simulate():
    payload = {
        "product_id": "PRD-SIM",
        "selling_price": 3000,
        "material_cost": 1200,
        "labor_cost": 800,
        "packaging_cost": 50,
        "transportation_cost": 100
    }
    
    response = client.post("/api/v1/pricing/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    result = data["data"]
    # Total cost = 2150
    # Profit = 850
    assert result["estimated_cost"] == 2150.0
    assert result["estimated_profit"] == 850.0
    assert result["margin"] > 0.3
    assert result["market_position"] == "competitive"
