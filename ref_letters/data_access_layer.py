from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from .database import Teacher, Student, ReferenceLetterRequest

class TeacherDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def create_teacher(self, name: str, description: str):
        new_teacher = Teacher(name=name, description=description)
        self.db_session.add(new_teacher)
        await self.db_session.flush()
    
    async def get_all_teachers(self) -> List[Teacher]:
        q = await self.db_session.execute(select(Teacher).order_by(Teacher.id))
        return q.scalars().all()
    
    async def get_a_teacher(self, teacher_id: int) -> Teacher:
        q = await self.db_session.execute(select(Teacher).where(Teacher.id == teacher_id))
        return q.scalars().all()

    async def update_teacher(self, teacher_id: int, name: Optional[str], description: Optional[str]):
        q = update(Teacher).where(Teacher.id == teacher_id)
        if name:
            q = q.values(name=name)
        if description:
            q = q.values(description=description)
        await self.db_session.execute(q)

class StudentDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_student(self, name: str, school: str, school_id: str, grades_url: str):
        new_student = Student(name=name, school=school, school_id=school_id, grades_url=grades_url)
        self.db_session.add(new_student)
        await self.db_session.flush()
    
    async def get_all_students(self) -> List[Student]:
        q = await self.db_session.execute(select(Student).order_by(Student.id))
        return q.scalars().all()
    
    async def get_a_student(self, student_id: int) -> Student:
        q = await self.db_session.execute(select(Student).where(Student.id == student_id))
        return q.scalars().all()

    async def update_student(self, student_id: int, name: Optional[str], school: Optional[str], school_id: Optional[str], 
            grades_url: Optional[str]):
        q = update(Student).where(Student.id == student_id)
        if name:
            q = q.values(name=name)
        if school:
            q = q.values(school=school)
        if school_id:
            q = q.values(school_id=school_id)
        if grades_url:
            q = q.values(grades_url=grades_url)
        await self.db_session.execute(q)

class ReferenceLetterRequestDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # get for a student
    async def get_students_rl_requests(self, student_id: int) -> List[ReferenceLetterRequest]:
        q = await self.db.session.execute(select(ReferenceLetterRequest).where(ReferenceLetterRequest.student_id == student_id).
            order_by(ReferenceLetterRequest.id))
        return q.scalars().all()

    # get pending for a teacher
    async def get_pending_for_teacher(self, teacher_id: int) -> List[ReferenceLetterRequest]:
        q = await self.db.session.execute(
            select(ReferenceLetterRequest).where(ReferenceLetterRequest.teacher_id == teacher_id and 
                ReferenceLetterRequest.status == "pending").
            order_by(ReferenceLetterRequest.id)
        )
        return q.scalars().all()

    # approve a pending
    async def approve_rl_request(self, rl_request_id: int, text: str):
        q = update(ReferenceLetterRequest).where(ReferenceLetterRequest.id == rl_request_id and 
                ReferenceLetterRequest.status == "pending")
        q = q.values(status="approved", text=text)
        await self.db_session.execute(q)

    # decline a pending
    async def decline_rl_request(self, rl_request_id: int):
        q = update(ReferenceLetterRequest).where(ReferenceLetterRequest.id == rl_request_id and 
                ReferenceLetterRequest.status == "pending")
        q = q.values(status="declined")
        await self.db_session.execute(q)

    async def create_rl_request(self, teacher_id: int, student_id: int, carrier_name: str, carrier_email: str, status: str, 
                text: str):
        new_rl_request = ReferenceLetterRequest(teacher_id=teacher_id, student_id=student_id, carrier_name=carrier_name, 
            carrier_email=carrier_email, status=status, text=text)
        self.db_session.add(new_rl_request)
        await self.db_session.flush()
    
    async def get_all_rl_requests(self) -> List[ReferenceLetterRequest]:
        q = await self.db_session.execute(select(ReferenceLetterRequest).order_by(ReferenceLetterRequest.id))
        return q.scalars().all()
    
    async def get_a_rl_request(self, rl_request_id: int) -> ReferenceLetterRequest:
        q = await self.db_session.execute(select(ReferenceLetterRequest).where(ReferenceLetterRequest.id == rl_request_id))
        return q.scalars().all()

    async def update_rl_request(self, rl_request_id: int, teacher_id: Optional[int], student_id: Optional[int], 
            carrier_name: Optional[str], carrier_email: Optional[str], status: Optional[str], text: Optional[str]):
        q = update(ReferenceLetterRequest).where(ReferenceLetterRequest.id == rl_request_id)
        if teacher_id:
            q = q.values(teacher_id=teacher_id)
        if student_id:
            q = q.values(student_id=student_id)
        if carrier_name:
            q = q.values(carrier_name=carrier_name)
        if carrier_email:
            q = q.values(carrier_email=carrier_email)
        if status:
            q = q.values(status=status)
        if text:
            q = q.values(text=text)
        await self.db_session.execute(q)