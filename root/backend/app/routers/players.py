from fastapi import FastAPI, APIRouter
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
    return {"data": records}
