from database import get_db_connection
from models import ItemCreate, ItemUpdate


def get_all_items():
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM items")
  items = cursor.fetchall()
  conn.close()
  return [dict(item) for item in items]


def get_item_by_id(item_id: int):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
  item = cursor.fetchone()
  conn.close()
  return dict(item) if item else None


def create_item(item: ItemCreate):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO items (name, description, price, in_stock)
        VALUES (?, ?, ?, ?)
    """,
      (item.name, item.description, item.price, int(item.in_stock)),
  )
  conn.commit()
  item_id = cursor.lastrowid
  conn.close()
  return get_item_by_id(item_id)


def update_item(item_id: int, item_update: ItemUpdate):
  existing_item = get_item_by_id(item_id)
  if not existing_item:
    return None

  # Merge updates with existing data
  update_data = item_update.dict(exclude_unset=True)

  conn = get_db_connection()
  cursor = conn.cursor()

  for key, value in update_data.items():
    if key == "in_stock":
      value = int(value)
    cursor.execute(f"UPDATE items SET {key} = ? WHERE id = ?", (value, item_id))

  conn.commit()
  conn.close()
  return get_item_by_id(item_id)


def delete_item(item_id: int):
  existing_item = get_item_by_id(item_id)
  if not existing_item:
    return False

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
  conn.commit()
  conn.close()
  return True