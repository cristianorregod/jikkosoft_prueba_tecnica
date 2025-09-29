"""
Business logic for order processing.
"""
from decimal import Decimal
from typing import Tuple
from .models import OrderRequest

class OrderService:
    # Shipping fee matrix based on stratum (1-6)
    SHIPPING_FEES = {
        1: Decimal('2000.00'),
        2: Decimal('3000.00'),
        3: Decimal('4000.00'),
        4: Decimal('5000.00'),
        5: Decimal('6000.00'),
        6: Decimal('7000.00')
    }
    
    # Discount thresholds and percentages
    DISCOUNT_RULES = [
        (Decimal('100000'), Decimal('0.10')),  # 10% discount for orders over 100k
        (Decimal('50000'), Decimal('0.05')),   # 5% discount for orders over 50k
        (Decimal('20000'), Decimal('0.02')),   # 2% discount for orders over 20k
    ]

    @staticmethod
    def calculate_order_totals(order: OrderRequest) -> Tuple[Decimal, Decimal, Decimal, Decimal]:
        """
        Calculate order totals including shipping and discounts.
        
        Returns:
            Tuple containing (subtotal, shipping_fee, discount_amount, total)
        """
        # Calculate subtotal
        subtotal = sum(item.price * item.quantity for item in order.products)
        
        # Get shipping fee based on stratum
        shipping_fee = OrderService.SHIPPING_FEES[order.stratum]
        
        # Calculate discount
        discount_amount = Decimal('0')
        for threshold, discount_rate in OrderService.DISCOUNT_RULES:
            if subtotal >= threshold:
                discount_amount = subtotal * discount_rate
                break
        
        # Calculate total
        total = subtotal + shipping_fee - discount_amount
        
        return subtotal, shipping_fee, discount_amount, total