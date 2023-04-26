from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter()

class Game(BaseModel):
    card_id: str
    home_score: int
    away_score: int


async def card_exists(card_id: str) -> bool:
    card = await db.card.find_first(where={"id": card_id})
    if card:
        return True
    return False

@router.get("/games/", status_code=status.HTTP_200_OK, tags=["game"])
async def read_games() -> dict[str, list[dict]]:
    games = await db.game.find_many(include={"user": True})
    return {"games": games}

@router.get("/games/{game_id}", status_code=status.HTTP_200_OK, tags=["game"])
async def read_game(game_id: int) -> dict[str, dict]:
    game = await db.game.find_first(where={"id": game_id})
    return {"game": game}

@router.post("/games/", status_code=status.HTTP_201_CREATED, tags=["game"])
async def create_game(game: Game) -> dict[str, Union[str, dict]]:
    if card_exists(game.card_id) is False:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Card not authorized"})

    db_game = await db.game.create(data={
        "home_score": game.home_score,
        "away_score": game.away_score,
        "user_id": game.card_id
    })
    return {"message": "Game created", "game": db_game}

@router.put("/games/{game_id}", status_code=status.HTTP_200_OK, tags=["game"])
async def update_game(game_id: int, game: Game) -> dict[str, Union[str, dict]]:
    db_game = await db.game.find_first(where={"id": game_id})
    if db_game is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Game not found"})
    
    await db.game.update(
        where={"id": game_id},
        data={
            "home_score": game.home_score,
            "away_score": game.away_score
        }
    )
    return {"game": game}
