from uvicorn import run
from src import create_app

if __name__ == "__main__":
    run("main:create_app", reload=True, factory=True)
