from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import ReferenceLetterRequest, Student, Teacher

def get_rl_requests(db: Session):
    rl_requests = select(ReferenceLetterRequest)
    return db.execute(rl_requests).scalars().all()


def create_rl_request(db: Session, rlRequest: schemas.ReferenceLetterRequestCreate):
    db_rl_request = ReferenceLetterRequest(**rlRequest.dict())
    db.add(db_rl_request)
    db.commit()
    db.refresh(db_rl_request)
    return db_rl_request

def get_students(db: Session):
    students = select(Student)
    return db.execute(students).scalars().all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_teachers(db: Session):
    teachers = select(Teacher)
    return db.execute(teachers).scalars().all()


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher