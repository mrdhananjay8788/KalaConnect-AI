import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_bamboo_basket():
    # Should extract 'basket', 'bamboo' and '500' max price
    response = client.post(
        "/api/v1/search/products",
        params={"query": "I need 10 handmade bamboo baskets under 500", "language": "en"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    
    filters = data["filters"]
    assert "bamboo" in filters["material"]
    assert filters["price_max"] == 500.0
    assert filters["quantity"] == 10
    
    # Expect the bamboo basket to be ranked first
    results = data["results"]
    assert len(results) > 0
    assert results[0]["product_id"] == "PRD-001"
    assert results[0]["price"] <= 500

def test_search_hard_filter_exclusion():
    # Looking for a basket under 100, but our bamboo basket is 450.
    # It should fail the hard filter, triggering alternative matching (dropping price_max).
    response = client.post(
        "/api/v1/search/products",
        params={"query": "bamboo basket under 100"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    
    # We should see `is_alternative` flag turned on
    assert data["is_alternative"] is True
    # And we get the PRD-001 anyway as a fallback recommendation
    assert len(data["results"]) > 0

def test_search_pagination():
    response = client.post(
        "/api/v1/search/products",
        params={"query": "bag", "page": 1, "page_size": 1}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["results"]) == 1

def test_similar_products():
    response = client.get("/api/v1/search/products/PRD-001/similar")
    assert response.status_code == 200
    data = response.json()["data"]["products"]
    assert len(data) > 0
    # PRD-001 itself should be excluded
    assert all(p["product_id"] != "PRD-001" for p in data)

def test_search_suggestions():
    response = client.get("/api/v1/search/suggestions", params={"q": "bamb"})
    assert response.status_code == 200
    assert "bamb basket" in response.json()["data"]
