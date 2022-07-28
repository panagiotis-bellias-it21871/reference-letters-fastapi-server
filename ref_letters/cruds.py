from sqlalchemy.orm import Session
from . import database, schemas

def get_teacher(db: Session, teacher_id: int):
    return db.query(database.Teacher).filter(database.Teacher.id == teacher_id).first()

def get_teacher_by_email(db: Session, email: str):
    return db.query(database.Teacher).filter(database.Teacher.email == email).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Teacher).offset(skip).limit(limit).all()

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = database.Teacher(
        name=teacher.name,
        email=teacher.email,
        description=teacher.description
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_student(db: Session, student_id: int):
    return db.query(database.Student).filter(database.Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(database.Student).filter(database.Student.email == email).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = database.Student(
        name=student.name,
        email=student.email,
        school=student.school,
        school_id=student.school_id,
        grades_url=student.grades_url,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_referenceletterrequest(db: Session, referenceletterrequest_id: int):
    return db.query(database.ReferenceLetterRequest).filter(database.ReferenceLetterRequest.id == referenceletterrequest_id).first()

def get_referenceletterrequests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.ReferenceLetterRequest).offset(skip).limit(limit).all()

def create_referenceletterrequest(db: Session, referenceletterrequest: schemas.ReferenceLetterRequestCreate):
    db_referenceletterrequest = database.ReferenceLetterRequest(
        carrier_name=referenceletterrequest.carrier_name,
        carrier_email=referenceletterrequest.carrier_email,
        status=referenceletterrequest.status,
        text=referenceletterrequest.text,
        student_id=referenceletterrequest.student_id,
        teacher_id=referenceletterrequest.teacher_id
    )
    db.add(db_referenceletterrequest)
    db.commit()
    db.refresh(db_referenceletterrequest)
    return db_referenceletterrequest