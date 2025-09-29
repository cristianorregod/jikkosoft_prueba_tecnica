"""
Data models for the order processing API.
"""
from typing import List
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class Product(BaseModel):
    id: str
    name: str
    price: Decimal = Field(gt=0)
    quantity: int = Field(gt=0)

class OrderRequest(BaseModel):
    products: List[Product]
    stratum: int = Field(ge=1, le=6)
    address: str

    @field_validator('stratum')
    @classmethod
    def validate_stratum(cls, v: int) -> int:
        if not 1 <= v <= 6:
            raise ValueError('Stratum must be between 1 and 6')
        return v

class OrderResponse(BaseModel):
    subtotal: Decimal
    shipping_fee: Decimal
    discount_amount: Decimal
    total: Decimal