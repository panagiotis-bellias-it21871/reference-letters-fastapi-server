'''
Importing modules needed
'''
import databases
import sqlalchemy

import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", default="")             # Declare database url (e.g. sqlite or postgreSQL)

# Initialize some utility objects for the database connection
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

# Our custom tables
teacher_db = sqlalchemy.Table(
    "teacher",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
    sqlalchemy.Column("description", sqlalchemy.String(750)),
)

student_db = sqlalchemy.Table(
    "student",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
    sqlalchemy.Column("school", sqlalchemy.String(125)),
    sqlalchemy.Column("school_id", sqlalchemy.String(125)),
    sqlalchemy.Column("grades_url", sqlalchemy.String(500)),
)

reference_letter_request_db = sqlalchemy.Table(
    "reference_letter_request",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("teacher_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('teacher.id', ondelete='CASCADE')),
    sqlalchemy.Column("student_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('student.id', ondelete='CASCADE')),
    sqlalchemy.Column("carrier_name", sqlalchemy.String(500)),
    sqlalchemy.Column("carrier_email", sqlalchemy.String(500)),
    sqlalchemy.Column("status", sqlalchemy.String(500)),
    sqlalchemy.Column("text", sqlalchemy.String(500)),
    sqlalchemy.Column("student_name", sqlalchemy.String(500)),
)

# Initialize db engine to have tables ready at application's startup
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)