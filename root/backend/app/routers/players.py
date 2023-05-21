from fastapi import FastAPI, APIRouter, Request
from app.schemas import Player
from typing import List
import pandas as pd
import os
import json
import math


def snake_picks(number_of_teams=12, rounds=16):
    all_picks = {}
    for draft_position in range(1, 13):
        picks = []
        for round_no in range(1, rounds + 1):
            if round_no % 2 == 0:
                draft_pick = (round_no * number_of_teams) - draft_position + 1
            else:
                draft_pick = ((round_no - 1) * number_of_teams) + draft_position
            picks.append(draft_pick)
        all_picks[draft_position] = picks

    return all_picks


while True:
    try:
        file_path = (
            "/Users/tylerbakely/Desktop/repos/thefantasybot/root/backend/app/data/"
        )
        with open(os.path.join(file_path, "draftboard_STD.json"), "r") as f:
            data = json.load(f)

            player_data = [
                Player(
                    id=id,
                    player=player["Player"],
                    position=player["Position"],
                    value_score=player["VOR Rank"],
                    adp=player["ADP Rank"],
                    sleeper_score=player["Sleeper Score"],
                    tier=player["Tier"],
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


@router.post("/draft-pick")
async def make_draft_pick(players: List[dict]):
    roster_map = {
        "RB": 0,
        "WR": 0,
        "QB": 0,
        "TE": 0,
    }

    ids_player_data = [player.id for player in player_data]
    ids_drafted = [player["id"] for player in players]
    snake_pick = snake_picks()
    currentPick = len(players) + 1
    currentRound = math.ceil(len(players) / 12)
    currentDrafter = [k for k, v in snake_pick.items() if currentPick in v][0]
    id_available = list(set(ids_player_data) - set(ids_drafted))
    drafterNextPick = snake_pick[currentDrafter][currentRound]
    picksBetweenNext = drafterNextPick - currentPick - 1
    current_roster_ids = [
        player["id"] for player in players if player["teamNo"] == currentDrafter
    ]
    roster = [player for player in players if player["id"] in current_roster_ids]
    for player in roster:
        position = player["position"]
        roster_map[position] += 1

    def recommended(player_ids: List[int]):
        available = [player for player in player_data if player.id in player_ids]
        recommend = min(available, key=lambda x: x.value_score)
        return recommend

    result = recommended(id_available)

    return {
        "message": "It worked!",
        "the-pick-is-in": f"Based on your current roster, we recommend you to pick {result.player}.",
        "player-best-valuescore": result,
        "current-pick": currentPick,
        "current-round": currentRound,
        "current-drafter": currentDrafter,
        "drafter-next-pick": drafterNextPick,
        "picks-between-next-pick": picksBetweenNext,
        "current-roster-ids": current_roster_ids,
        "roster": roster,
        "roster_count": roster_map,
        "undrafted_ids": id_available,
    }
