# Product Manager API

A professional REST API built with **FastAPI**, **SQLite3** and **Pydantic**.
It provides full CRUD operations for products.

## Project structure

```
fastapi_crud_app/
├── app/
│   ├── __init__.py
│   ├── main.py            # App entry point (uvicorn target)
│   ├── config.py          # Environment-based settings
│   ├── database.py        # SQLite connection + schema bootstrap
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py     # Product domain model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── product.py     # Pydantic request/response schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── product_repository.py  # All SQL lives here
│   └── routers/
│       ├── __init__.py
│       └── products.py    # API endpoints
├── .env
└── requirements.txt
```

## Setup in PyCharm

1. Open the folder `fastapi_crud_app` in PyCharm.
2. Create a virtual environment:
   `File -> Settings -> Project -> Python Interpreter -> Add Interpreter -> New Virtualenv`
3. Open PyCharm's **Terminal** and run:
   ```bash
   pip install -r requirements.txt
   ```

## Run the server

From the project root (the folder that contains `app/`):

```bash
uvicorn app.main:app --reload
```

Then open:

- API: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- Alternative docs (ReDoc): http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

The SQLite database file `products.db` is created automatically on startup.
