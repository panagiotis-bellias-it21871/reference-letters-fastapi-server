import databases
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", default="")
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
reference_letter_request_db = sqlalchemy.Table(
    "reference_letter_request",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("is_approved", sqlalchemy.Boolean),
    sqlalchemy.Column("is_declined", sqlalchemy.Boolean),
    sqlalchemy.Column("is_pending", sqlalchemy.Boolean),
)

student_db = sqlalchemy.Table(
    "student",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("school_id", sqlalchemy.String(125)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
)

teacher_db = sqlalchemy.Table(
    "teacher",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)