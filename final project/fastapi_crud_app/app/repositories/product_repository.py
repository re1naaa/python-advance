"""Data-access layer — all SQL queries live in this module only."""
import sqlite3
from typing import List, Optional

from app.database import get_connection
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def _row_to_product(row: sqlite3.Row) -> Product:
    return Product(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        quantity=row["quantity"],
        created_at=row["created_at"],
    )


class ProductRepository:
    """CRUD operations for the products table."""

    @staticmethod
    def get_all() -> List[Product]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY id"
            ).fetchall()
        return [_row_to_product(row) for row in rows]

    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,)
            ).fetchone()
        return _row_to_product(row) if row else None

    @staticmethod
    def create(data: ProductCreate) -> Product:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO products (name, description, price, quantity) "
                "VALUES (?, ?, ?, ?)",
                (data.name, data.description, data.price, data.quantity),
            )
            new_id = cursor.lastrowid
        return ProductRepository.get_by_id(new_id)

    @staticmethod
    def update(product_id: int, data: ProductUpdate) -> Optional[Product]:
        existing = ProductRepository.get_by_id(product_id)
        if existing is None:
            return None

        # Only update the fields that were actually provided
        updated = ProductUpdate(
            name=data.name if data.name is not None else existing.name,
            description=data.description if data.description is not None else existing.description,
            price=data.price if data.price is not None else existing.price,
            quantity=data.quantity if data.quantity is not None else existing.quantity,
        )

        with get_connection() as conn:
            conn.execute(
                "UPDATE products SET name = ?, description = ?, price = ?, quantity = ? "
                "WHERE id = ?",
                (updated.name, updated.description, updated.price,
                 updated.quantity, product_id),
            )
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def delete(product_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM products WHERE id = ?", (product_id,)
            )
        return cursor.rowcount > 0
