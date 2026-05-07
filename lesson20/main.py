from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()


# Define a route for the root URL ("/") using the HTTP GET method
@app.get("/")
def root():
    # Return a dictionary with a single key-value pair as JSON response
    return {"message": "Hello World"}


# Define a route that accepts a query parameter
@app.get("/greet/")
def read_root(name: str):
    return {"message": f"Hello, {name}!"}