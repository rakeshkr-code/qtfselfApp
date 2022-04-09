import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


engine = None
Base = declarative_base()
db = SQLAlchemy() #instead of importing the base model from sqlalchemy we're importing that from flask-sqlalchemy

