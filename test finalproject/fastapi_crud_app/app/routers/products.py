"""API endpoints for product CRUD operations."""
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse], summary="Get all products")
def list_products():
    """Return every product in the database, ordered by ID."""
    return ProductRepository.get_all()


@router.get("/{product_id}", response_model=ProductResponse, summary="Get one product")
def get_product(product_id: int):
    """Return a single product by its ID."""
    product = ProductRepository.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
    return product


@router.post("", response_model=ProductResponse,
             status_code=status.HTTP_201_CREATED, summary="Create a product")
def create_product(payload: ProductCreate):
    """Create a new product and return it."""
    return ProductRepository.create(payload)


@router.put("/{product_id}", response_model=ProductResponse, summary="Update a product")
def update_product(product_id: int, payload: ProductUpdate):
    """Update a product (partial update — send only the fields you want to change)."""
    product = ProductRepository.update(product_id, payload)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a product")
def delete_product(product_id: int):
    """Delete a product by its ID."""
    if not ProductRepository.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
