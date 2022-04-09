from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class ReferenceLetterRequest(Base):
    __tablename__ = 'reference_letter_requests'
    id = Column(Integer, primary_key=True, index=True)
    name: Column(String)
    description: Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    student_id = Column(Integer, ForeignKey('student.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))

    student = relationship('Student')
    teacher = relationship('Teacher')

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    school_id = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    degree = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
