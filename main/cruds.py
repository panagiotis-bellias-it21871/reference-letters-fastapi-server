from sqlalchemy import select
from sqlalchemy.orm import Session

from . import schemas
from .models import ReferenceLetterRequest as RL, Student as S, Teacher as T

def get_rl_requests(db: Session):
    rl_requests = select(RL)
    return db.execute(rl_requests).scalars().all()


def create_rl_request(db: Session, rlRequest: schemas.ReferenceLetterRequestCreate):
    db_rl_request = RL(**rlRequest.dict())
    db.add(db_rl_request)
    db.commit()
    db.refresh(db_rl_request)
    return db_rl_request

def get_students(db: Session):
    students = select(S)
    return db.execute(students).scalars().all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = S(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_teachers(db: Session):
    teachers = select(T)
    return db.execute(teachers).scalars().all()


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = T(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
