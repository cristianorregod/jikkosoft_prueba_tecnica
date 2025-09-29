"""
FastAPI endpoint for order processing.
"""
from fastapi import FastAPI, HTTPException
from .models import OrderRequest, OrderResponse
from .service import OrderService

app = FastAPI(title="Order Processing API")

@app.post("/api/v1/orders", response_model=OrderResponse)
async def process_order(order: OrderRequest):
    """
    Process a new order with products, calculating totals with shipping and discounts.
    """
    try:
        subtotal, shipping_fee, discount_amount, total = OrderService.calculate_order_totals(order)
        
        return OrderResponse(
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            discount_amount=discount_amount,
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))