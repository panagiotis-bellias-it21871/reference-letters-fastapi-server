from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import database
from .. import database, cruds, schemas

router = APIRouter(prefix='/api/teachers')

@router.get("/")
async def get_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    teachers = cruds.get_teachers(db, skip=skip, limit=limit)
    return teachers

@router.get("/{teacher_id}")
async def get_a_teacher(teacher_id: int, db: Session = Depends(database.get_db)):
    db_teacher = cruds.get_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@router.post("/")
async def add_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(database.get_db)):
    db_teacher = cruds.get_teacher_by_email(db, email=teacher.email)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Email already registered")
    return cruds.create_teacher(db=db, teacher=teacher)

"""
@router.put("/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: Teacher):
    query = teacher_db.update().where(teacher_db.c.id == teacher_id).values(
        name=teacher.name,
        email=teacher.email,
        description=teacher.description,
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = teacher_db.delete().where(teacher_db.c.id == teacher_id)
    return await database.execute(query)
"""