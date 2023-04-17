from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users(auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...

@router.put("/users/", tags=["users"])
async def create_user(username: str, auth: Depends = Depends(get_current_user)) -> dict[str, str]:
    ...
