from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import database
from .. import database, cruds, schemas

router = APIRouter(prefix='/api/rl_requests')

@router.get("/")
async def get_rl_requests(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    rl_requests = cruds.get_referenceletterrequests(db, skip=skip, limit=limit)
    return rl_requests

@router.get("/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int, db: Session = Depends(database.get_db)):
    db_rl_request = cruds.get_referenceletterrequest(db, referenceletterrequest_id=rl_request_id)
    if db_rl_request is None:
        raise HTTPException(status_code=404, detail="Reference letter request not found")
    return db_rl_request

@router.post("/")
async def add_rl_request(rl_request: schemas.ReferenceLetterRequestCreate, db: Session = Depends(database.get_db)):
    return cruds.create_referenceletterrequest(db=db, referenceletterrequest=rl_request)

@router.get("/pending")
async def get_rl_requests(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), teacher: bool = True):
    rl_requests = cruds.get_referenceletterrequests(db, skip=skip, limit=limit, teacher=teacher)
    return rl_requests

@router.get("/pending/{rl_request_id}")
async def get_rl_requests(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), teacher: bool = True):
    rl_requests = cruds.get_referenceletterrequests(db, skip=skip, limit=limit, teacher=teacher)
    return rl_requests

@router.post("/pending")
async def add_rl_request(rl_request: schemas.ReferenceLetterRequestCreate, db: Session = Depends(database.get_db)):
    return cruds.create_referenceletterrequest(db=db, referenceletterrequest=rl_request)

@router.delete("/pending")
async def add_rl_request(rl_request: schemas.ReferenceLetterRequestCreate, db: Session = Depends(database.get_db)):
    return cruds.create_referenceletterrequest(db=db, referenceletterrequest=rl_request)

"""
@router.put("/{rl_request_id}")
async def update_rl_request(rl_request_id: int, rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.update().where(reference_letter_request_db.c.id == rl_request_id).values(
        teacher_id=rl_request.teacher_id,
        student_id=rl_request.student_id,
        carrier_name=rl_request.carrier_name,
        carrier_email=rl_request.carrier_email,
        status=rl_request.status,
        text=rl_request.text
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/{rl_request_id}")
async def delete_rl_request(rl_request_id: int):
    query = reference_letter_request_db.delete().where(reference_letter_request_db.c.id == rl_request_id)
    return await database.execute(query)
"""