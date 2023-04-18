from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter()

class Game(BaseModel):
    id: int
    card_id: str
    home_score: int
    away_score: int


@router.get("/games/", tags=["game"])
async def read_games(auth: Depends = Depends(get_current_user)) -> dict[str, list[dict]]:
    games = await db.game.find_many()
    return {"games": games}

@router.get("/games/{game_id}", tags=["game"])
async def read_game(game_id: str, auth: Depends = Depends(get_current_user)) -> dict[str, dict]:
    game = await db.game.find_first(where={"id": game_id})
    return {"game": game}

@router.put("/games/{game_id}", tags=["game"])
async def create_game(game: Game, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    game = await db.game.find_first(where={"id": game.id})
    if game:
        return {"message": "Game already exists"}


    await db.game.create(data={})


@router.put("/games/{game_id}", tags=["game"])
async def update_game(game_id: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...
