import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sih_demo_scenario():
    """
    Test the exact SIH Demo scenario:
    "I need 500 handmade bamboo baskets under ₹700 each, delivered to Pune within 20 days, with custom branding."
    """
    payload = {
        "query": "I need 500 handmade bamboo baskets under 700 each, delivered to Pune within 20 days, with custom branding.",
        "quantity": 500,
        "budget_max": 700.0,
        "delivery_location": "Pune",
        "required_delivery_days": 20,
        "allow_split_order": False
    }

    response = client.post("/api/v1/matching/buyers", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    matches = data["matches"]
    
    # Assert we got matches
    assert len(matches) > 0
    
    # Assert top match is ART-101 (from demo data)
    top_match = matches[0]
    assert top_match["artisan_id"] == "ART-101"
    
    # Check match explanations and score expectations
    assert top_match["confidence"] > 0.8
    assert top_match["estimated_quantity"] == 600 # Artisan 101 has 600 available
    
    explanation_text = top_match["explanation"]
    assert "Can supply" in explanation_text
    assert "Price range fits buyer budget" in explanation_text
    assert "Supports custom branding" in explanation_text

def test_preview_matches():
    payload = {
        "query": "bamboo basket",
    }
    response = client.post("/api/v1/matching/preview", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    
    assert data["eligible_artisans"] > 0

def test_split_order():
    # Require 1000 units. No single artisan has this.
    payload = {
        "query": "I need 1000 handmade bamboo baskets",
        "quantity": 1000,
        "allow_split_order": True
    }
    response = client.post("/api/v1/matching/buyers", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    split_option = data.get("split_order_option")
    
    assert split_option is not None
    assert split_option["required_quantity"] == 1000
    # The allocated quantity will equal the sum of available quantities if total < 1000
    assert split_option["allocated_quantity"] <= 1000
    assert len(split_option["artisans"]) > 1

def test_hard_constraint_failure():
    # Bamboo masters (ART-102) doesn't support customization
    # New Bamboo Craft Co. (ART-104) supports branding
    # Meera weaves (ART-103) is sarees
    payload = {
        "query": "I need 1000 handmade bamboo baskets with logo printing",
        "quantity": 10,
        "allow_split_order": False,
        "budget_max": 200 # very low budget
    }
    response = client.post("/api/v1/matching/buyers", json=payload)
    assert response.status_code == 200
    matches = response.json()["data"]["matches"]
    
    # Budget filter should wipe everyone out
    assert len(matches) == 0
