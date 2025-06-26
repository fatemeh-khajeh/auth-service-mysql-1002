from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv(".env")
DATABASE_URL = os.getenv("MYSQL_URL")

engin = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engin)
Base = declarative_base()