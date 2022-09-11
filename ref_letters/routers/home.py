from fastapi import Depends, APIRouter, Form
from ..database import User
from ..users import current_active_user

router = APIRouter(prefix='/api')

@router.get("/")
def read_root():
    return {"message": "This is a fastapi backend application that supports reference letters handling! "+
    "It is currently being used by the corresponding VueJS application."}