from typing import Optional
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
  name: str = Field(..., min_length=2, max_length=100)
  description: Optional[str] = None
  price: float = Field(..., gt=0, description="Price must be greater than zero")
  in_stock: bool = True


class ItemUpdate(BaseModel):
  name: Optional[str] = Field(None, min_length=2, max_length=100)
  description: Optional[str] = None
  price: Optional[float] = Field(None, gt=0)
  in_stock: Optional[bool] = None


class ItemResponse(BaseModel):
  id: int
  name: str
  description: Optional[str]
  price: float
  in_stock: bool

  class Config:
    from_attributes = True