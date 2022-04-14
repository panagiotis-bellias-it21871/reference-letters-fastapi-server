from fastapi import Depends, FastAPI

from ref_letters.database import get_session, init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}