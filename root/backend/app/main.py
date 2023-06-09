from fastapi import FastAPI
from routers import players
import uvicorn

# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5174",
    "http://localhost:5174/",
    "http://localhost:8000/players",
    "http://localhost:8000/players/",
    "http://localhost:8000/players/draft-pick",
    "http://127.0.0.1:8000/players/draft-pick",
    "*",
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(players.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
