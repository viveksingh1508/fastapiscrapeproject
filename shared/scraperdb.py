# shared/db_sync.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SCRAPER_DATABASE_URL = os.getenv("SCRAPER_DATABASE_URL")  # same DB, just sync driver
# e.g. postgresql+psycopg2://user:password@host/db
engine = create_engine(SCRAPER_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
