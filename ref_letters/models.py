from sqlmodel import SQLModel, Field

class ReferenceLetterRequestBase(SQLModel):
    name: str
    description: str
    # time_created
    # time_updated
    student_id: int
    teacher_id: int

class ReferenceLetterRequest(ReferenceLetterRequestBase, table=True):
    id: int = Field(default=None, primary_key=True)

class ReferenceLetterRequestCreate(ReferenceLetterRequestBase):
    pass

class StudentBase(SQLModel):
    name: str
    email: str
    school_id: int
    # time_created
    # time_updated

class Student(StudentBase, table=True):
    id: int = Field(default=None, primary_key=True)

class StudentCreate(StudentBase):
    pass

class TeacherBase(SQLModel):
    name: str
    email: str
    degree: str
    # time_created
    # time_updated

class Teacher(TeacherBase):
    id: int = Field(default=None, primary_key=True)

class TeacherCreate(TeacherBase):
    pass