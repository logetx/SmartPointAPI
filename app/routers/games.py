from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter()


@router.get("/games/", tags=["game"])
async def read_games(auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...

@router.get("/games/{game_id}", tags=["game"])
async def read_game(game_id: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...

@router.put("/games/{game_id}", tags=["game"])
async def create_game(game_id: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...

@router.put("/games/{game_id}", tags=["game"])
async def update_game(game_id: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    await db.connect()
