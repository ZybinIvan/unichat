import uvicorn
from fastapi import FastAPI

from src.apps.auth.routes import auth_routes
from src.apps.user.routes import user_routes

app = FastAPI()
app.include_router(auth_routes)
app.include_router(user_routes)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
