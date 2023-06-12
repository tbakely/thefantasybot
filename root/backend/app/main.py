from fastapi import FastAPI
from routers import players
import uvicorn

# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

origins = [
    "*",
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
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
    uvicorn.run(app, host="127.0.0.1", port=8000)
