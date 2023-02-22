from fastapi import FastAPI
from app.routers import players
import psycopg2

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(players.router)
