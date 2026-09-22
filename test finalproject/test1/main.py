from contextlib import asynccontextmanager
import crud
from database import init_db
from fastapi import FastAPI, HTTPException, status
from models import ItemCreate, ItemResponse, ItemUpdate


# Lifespan event to initialize the database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield


app = FastAPI(
    title="Professional Inventory API",
    description=(
        "A robust CRUD API built with FastAPI, SQLite3, and Pydantic."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
def read_root():
  return {
      "message": (
          "Welcome to the Inventory API! Go to /docs for interactive Swagger"
          " documentation."
      )
  }


@app.get("/items", response_model=list[ItemResponse], tags=["Items"])
def list_items():
  """Retrieve a list of all inventory items."""
  return crud.get_all_items()


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int):
  """Retrieve a single item by its ID."""
  item = crud.get_item_by_id(item_id)
  if not item:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )
  return item


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
)
def add_item(item: ItemCreate):
  """Create a new inventory item."""
  return crud.create_item(item)


@app.patch("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def patch_item(item_id: int, item_update: ItemUpdate):
  """Partially update an existing item by its ID."""
  updated_item = crud.update_item(item_id, item_update)
  if not updated_item:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )
  return updated_item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def remove_item(item_id: int):
  """Delete an item from the inventory."""
  success = crud.delete_item(item_id)
  if not success:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )
  return None


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)