from fastapi import FastAPI, APIRouter
from app.schemas import Player
import pandas as pd
import os
import json

while True:
    try:
        file_path = (
            "/Users/tylerbakely/Desktop/repos/thefantasybot/root/backend/app/data/"
        )
        with open(os.path.join(file_path, "draftboard_standard.json"), "r") as f:
            data = json.load(f)
        print("Player data loaded successfully.")
        break
    except Exception as error:
        print("Could not load player data.")
        print("Error: ", error)
        break

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[Player])
async def get_players():
    results = [
        Player(
            id=id,
            player=player["PLAYER"],
            position=player["POS"],
            value_score=player["VOR Rank"],
            adp=player["ADP Rank"],
            sleeper_score=player["Sleeper Score"],
        )
        for id, player in enumerate(data)
    ]
    return results
