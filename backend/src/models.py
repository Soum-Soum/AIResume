import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine

from src.config import settings


class ExperienceModel(SQLModel, table=True):
    __tablename__ = "experiencemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")
    title: str
    company: str
    location: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

    parent_resume: "ResumeModel" = Relationship(back_populates="experiences")


class EducationModel(SQLModel, table=True):
    __tablename__ = "educationmodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")
    institution: str
    degree: str
    field_of_study: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

    parent_resume: "ResumeModel" = Relationship(back_populates="educations")


class SkillModel(SQLModel, table=True):
    __tablename__ = "skillmodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")
    name: str
    level: str

    parent_resume: "ResumeModel" = Relationship(back_populates="skills")


class ResumeModel(SQLModel, table=True):
    __tablename__ = "resumemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_hash: str
    name: str
    email: str
    phone: str
    summary: Optional[str] = None

    experiences: List[ExperienceModel] = Relationship(back_populates="parent_resume")
    educations: List[EducationModel] = Relationship(back_populates="parent_resume")
    skills: List[SkillModel] = Relationship(back_populates="parent_resume")


database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=False)
SQLModel.metadata.create_all(engine)
