from fastapi import Depends, APIRouter, Form
from ..database import User
from ..users import current_active_user

router = APIRouter(prefix='/api')

@router.get("/")
def read_root():
    return {"message": "This is a fastapi backend application that supports reference letters handling! "+
    "It is currently being used by the corresponding VueJS application."}

@router.get("/authenticated-route/")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@router.get("/ping/")
async def ping():
    return {"ping": "pong!"}