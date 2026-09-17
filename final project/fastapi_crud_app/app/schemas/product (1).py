"""Pydantic schemas for request validation and response serialization."""
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Shared fields for create/update."""

    name: str = Field(..., min_length=1, max_length=100, examples=["Mechanical Keyboard"])
    description: Optional[str] = Field(default="", max_length=500)
    price: float = Field(..., ge=0, examples=[79.99])
    quantity: int = Field(default=0, ge=0, examples=[25])


class ProductCreate(ProductBase):
    """Payload for POST /products."""


class ProductUpdate(BaseModel):
    """Payload for PUT /products — all fields optional (partial update)."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)


class ProductResponse(ProductBase):
    """Response model returned to clients."""

    id: int
    created_at: str
