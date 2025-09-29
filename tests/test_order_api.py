"""
Tests for the order processing API.
"""
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.models import Product, OrderRequest
from src.api.service import OrderService

client = TestClient(app)

def create_test_order(products, stratum=1):
    """Helper function to create test orders"""
    return OrderRequest(
        products=products,
        stratum=stratum,
        address="Test Address 123"
    )

class TestOrderProcessing:
    def test_valid_order_processing(self):
        """Test processing a valid order"""
        # Create test order
        order_data = {
            "products": [
                {
                    "id": "1",
                    "name": "Product 1",
                    "price": "10.00",
                    "quantity": 2
                }
            ],
            "stratum": 1,
            "address": "Test Address 123"
        }
        
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["subtotal"] == "20.00"
        assert data["shipping_fee"] == "2000.00"
        assert data["total"] == "2020.00"

    def test_discount_calculation(self):
        """Test discount is applied correctly for large orders"""
        # Create order over 100k to test maximum discount
        order_data = {
            "products": [
                {
                    "id": "1",
                    "name": "Expensive Product",
                    "price": "100000.00",
                    "quantity": 1
                }
            ],
            "stratum": 1,
            "address": "Test Address 123"
        }
        
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 200
        
        data = response.json()
        # 10% discount on 100000 = 10000
        assert Decimal(data["discount_amount"]) == Decimal("10000.00")

    def test_stratum_based_shipping(self):
        """Test shipping fees vary by stratum"""
        product = {
            "id": "1",
            "name": "Test Product",
            "price": "10.00",
            "quantity": 1
        }
        
        # Test different strata
        for stratum in range(1, 7):
            order_data = {
                "products": [product],
                "stratum": stratum,
                "address": "Test Address 123"
            }
            
            response = client.post("/api/v1/orders", json=order_data)
            assert response.status_code == 200
            
            data = response.json()
            assert Decimal(data["shipping_fee"]) == OrderService.SHIPPING_FEES[stratum]

    def test_invalid_stratum(self):
        """Test invalid stratum values are rejected"""
        order_data = {
            "products": [
                {
                    "id": "1",
                    "name": "Test Product",
                    "price": "10.00",
                    "quantity": 1
                }
            ],
            "stratum": 7,  # Invalid stratum
            "address": "Test Address 123"
        }
        
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 422  # Validation error

    def test_invalid_product_data(self):
        """Test invalid product data is rejected"""
        # Test negative price
        order_data = {
            "products": [
                {
                    "id": "1",
                    "name": "Test Product",
                    "price": "-10.00",
                    "quantity": 1
                }
            ],
            "stratum": 1,
            "address": "Test Address 123"
        }
        
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 422

        # Test negative quantity
        order_data["products"][0]["price"] = "10.00"
        order_data["products"][0]["quantity"] = -1
        
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 422

class TestOrderService:
    def test_discount_rules(self):
        """Test discount rules are applied correctly"""
        products = [
            Product(id="1", name="Test Product", price=Decimal("100000"), quantity=1)
        ]
        order = create_test_order(products)
        
        subtotal, _, discount, _ = OrderService.calculate_order_totals(order)
        assert discount == subtotal * Decimal("0.10")  # 10% discount
        
        # Test medium order
        products = [
            Product(id="1", name="Test Product", price=Decimal("50000"), quantity=1)
        ]
        order = create_test_order(products)
        
        subtotal, _, discount, _ = OrderService.calculate_order_totals(order)
        assert discount == subtotal * Decimal("0.05")  # 5% discount
        
        # Test small order
        products = [
            Product(id="1", name="Test Product", price=Decimal("1000"), quantity=1)
        ]
        order = create_test_order(products)
        
        subtotal, _, discount, _ = OrderService.calculate_order_totals(order)
        assert discount == Decimal("0")  # No discount