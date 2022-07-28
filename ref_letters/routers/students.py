from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import database
from .. import database, cruds, schemas

router = APIRouter(prefix='/api/students')

@router.get("/")
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    students = cruds.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}")
async def get_a_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = cruds.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.post("/")
async def add_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = cruds.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return cruds.create_student(db=db, student=student)

"""
@router.put("/{student_id}")
async def update_student(student_id: int, student: Student):
    query = student_db.update().where(student_db.c.id == student_id).values(
        name=student.name,
        email=student.email,
        school=student.school,
        school_id=student.school_id,
        grades_url=student.grades_url
    )
    record_id = await database.execute(query)
    query = student_db.select().where(student_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/{student_id}")
async def delete_student(student_id: int):
    query = student_db.delete().where(student_db.c.id == student_id)
    return await database.execute(query)
"""