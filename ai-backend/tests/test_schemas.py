from app.schemas.product import Product
import pytest

def test_product_schema_validation():
    # Valid data
    data = {
        "product_id": "123",
        "artisan_id": "art-456",
        "product_name": "Test Saree",
        "category": "Clothing",
        "subcategory": "Sarees",
        "craft_type": "Handloom",
        "region": "Varanasi",
        "language": "hi",
        "description": {
            "original": "Test desc",
            "hindi": "टेस्ट",
            "english": "Test"
        },
        "image": {
            "original_url": "http://example.com/img.jpg"
        },
        "pricing": {
            "suggested_price": 500.0
        },
        "ai_metadata": {
            "model": "test-model"
        }
    }
    
    product = Product(**data)
    assert product.product_name == "Test Saree"
    assert product.ai_metadata.model == "test-model"

def test_product_schema_invalid():
    # Missing required field 'product_id'
    data = {
        "artisan_id": "art-456",
        "product_name": "Test Saree",
        "category": "Clothing",
        "subcategory": "Sarees",
        "craft_type": "Handloom",
        "region": "Varanasi",
        "language": "hi",
        "description": {},
        "image": {},
        "pricing": {},
        "ai_metadata": {
            "model": "test"
        }
    }
    
    with pytest.raises(ValueError):
        Product(**data)
