from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path("/.env")
load_dotenv(dotenv_path=env_path)
SCRAPER_DATABASE_URL = os.getenv("SCRAPER_DATABASE_URL")
print("sssssssssssssssssssssssssss", SCRAPER_DATABASE_URL)
engine = create_engine(SCRAPER_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
