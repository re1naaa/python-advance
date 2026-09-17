"""Domain model for a Product."""
from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    quantity: int
    created_at: str
