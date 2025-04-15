from typing import Optional, Sequence

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.models import ResumeModel, Base

engine = create_engine(settings.DB_PATH, echo=True)
SessionLocal = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def find_resume_by_id(resume_id: str) -> Optional[ResumeModel]:
    with SessionLocal() as session:
        statement = select(ResumeModel).where(ResumeModel.id == resume_id)
        result = session.execute(statement).scalar_one_or_none()
        return result


def find_resume_by_hash(file_hash: str) -> Optional[ResumeModel]:
    with SessionLocal() as session:
        statement = select(ResumeModel).where(ResumeModel.file_hash == file_hash)
        result = session.execute(statement).scalar_one_or_none()
        return result


def insert_new_resume(resume: ResumeModel):
    with SessionLocal() as session:
        session.add(resume)
        session.commit()


def list_resumes(n: int = 10) -> Sequence[ResumeModel]:
    with SessionLocal() as session:
        statement = select(ResumeModel).limit(n)
        result = session.execute(statement).scalars().all()
        return result
