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

# Initialize db engine to have tables ready at application's startup
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)