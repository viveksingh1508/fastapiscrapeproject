from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean
import sqlalchemy as sa


Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    company_profile = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    salary_range = Column(String(100), nullable=True)
    job_type = Column(String(50), nullable=True)
    experience = Column(String(50), nullable=True)
    job_description = Column(Text, nullable=True)
    qualifications = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    preferences = Column(Text, nullable=True)
    role = Column(String(50), nullable=True)
    job_portal = Column(String(100), nullable=True)
    posted_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(
        Boolean, default=True, server_default=sa.text("true"), nullable=False
    )
    is_admin = Column(
        Boolean, default=False, server_default=sa.text("false"), nullable=False
    )
    profile_picture = Column(String(200), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
