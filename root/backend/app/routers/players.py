from fastapi import FastAPI, APIRouter
from app.schemas import Player
import psycopg2

while True:
    try:
        conn = psycopg2.connect("dbname=thefantasybot user=tbakely")
        cursor = conn.cursor()
        print("Connection successful.")
        break
    except Exception as error:
        print("Connection failed.")
        print("Error: ", error)

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
async def get_players():
    cursor.execute("""SELECT * FROM players""")
    records = cursor.fetchall()
    results = [
        Player(
            id=i[0],
            player=i[1],
            position=i[2],
            value_score=i[3],
            adp=i[4],
            sleeper_score=i[5],
        )
        for i in records
    ]
    return {"data": results}
