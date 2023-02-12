from fastapi import FastAPI
from app.routers import players

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(players.router)
