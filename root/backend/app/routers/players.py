from fastapi import FastAPI, APIRouter


router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
async def get_players():
    return {"message": "Checked!"}
