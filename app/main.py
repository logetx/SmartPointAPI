from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import auth
from app.core.database import db
from app.routers import admin, games

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
app.include_router(admin.router)
app.include_router(games.router)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await db.disconnect()