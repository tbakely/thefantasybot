from pydantic import BaseModel, Field


class Player(BaseModel):
    id: int
    player: str
    position: str = Field(max_length=2)
    value_score: int
    adp: int
    sleeper_score: int
