from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import auth
from app.routers import users, games

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(games.router)
