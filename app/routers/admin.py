from typing import Union, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter()

class User(BaseModel):
    id: str
    name: str

@router.get("/users/", tags=["admin"])
async def read_users(auth: Depends = Depends(get_current_user)) -> dict[str, list]:
    users = await db.user.find_many()
    return {"users": users}

@router.get("/users/{username}", tags=["admin"])
async def read_user(username: str, auth: Depends = Depends(get_current_user)) -> dict[str, Union[dict, None]]:
    user = await db.user.find_first(where={"username": username})
    return {"user": user}

@router.post("/users/", tags=["admin"])
async def create_user(
    user: User,
    auth: Depends = Depends(get_current_user)
) -> dict[str, Any]:
    db_user = await db.user.find_first(where={"id": user.id})
    if db_user:
        return {"message": "User already exists"}
    
    db_user = await db.user.create(data={"id": user.id, "name": user.name})
    print(db_user)
    return {"message": "User created", "user": db_user}
