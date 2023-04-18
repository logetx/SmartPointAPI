from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter()

class User(BaseModel):
    id: str
    name: str

@router.get("/users/", status_code=status.HTTP_200_OK, tags=["admin"])
async def read_users(_: Depends = Depends(get_current_user)) -> dict[str, list[dict]]:
    users = await db.user.find_many(include={"games": True})
    return {"users": users}

@router.get("/users/{username}", status_code=status.HTTP_200_OK, tags=["admin"])
async def read_user(username: str, _: Depends = Depends(get_current_user)) -> dict[str, Union[dict, None]]:
    user = await db.user.find_first(where={"username": username})
    return {"user": user}

@router.post("/users/", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_user(
    user: User,
    _: Depends = Depends(get_current_user)
) -> dict[str, Union[str, dict]]:
    db_user = await db.user.find_first(where={"id": user.id})
    if db_user:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "User already exists"})
    
    db_user = await db.user.create(data={"id": user.id, "name": user.name})
    return {"message": "User created", "user": db_user}
