from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importing model elements
from model.base import Base
from model.comment import Comment
from model.stock import Stock

db_path = "database/"
# Check if directory doesn't exist
if not os.path.exists(db_path):
   # then create directory
   os.makedirs(db_path)

# database access url (this is a url for local sqlite access)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# create database connection engine
engine = create_engine(db_url, echo=False)

# Instance a session maker with the database
Session = sessionmaker(bind=engine)

# create database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url) 

# create database tables if they don't exist
Base.metadata.create_all(engine)
