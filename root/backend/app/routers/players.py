from fastapi import FastAPI, APIRouter, Request
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

            player_data = [
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
        print("Player data loaded successfully.")
        break
    except Exception as error:
        print("Could not load player data.")
        print("Error: ", error)
        break

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[Player])
async def get_players():
    return player_data


@router.get("/{id}")
async def get_player_by_id(id: int):
    results = [player for player in player_data if player.id == id]
    return results
