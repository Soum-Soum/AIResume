import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

from config import settings

class ExperienceModelBase(SQLModel):
    title: str
    company: str
    location: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class ExperienceModelPublic(ExperienceModelBase):
    id: uuid.UUID

class ExperienceModel(ExperienceModelBase, table=True):
    __tablename__ = "experiencemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")
    parent_resume: "ResumeModel" = Relationship(back_populates="experiences")

class EducationModelBase(SQLModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class EducationModelPublic(EducationModelBase):
    id: uuid.UUID

class EducationModel(EducationModelBase, table=True):
    __tablename__ = "educationmodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")

    parent_resume: "ResumeModel" = Relationship(back_populates="educations")

class SkillModelBase(SQLModel):
    name: str
    level: str

class SkillModelPublic(SkillModelBase):
    id: uuid.UUID

class SkillModel(SkillModelBase, table=True):
    __tablename__ = "skillmodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")

    parent_resume: "ResumeModel" = Relationship(back_populates="skills")


class ResumeModelBase(SQLModel):
    name: str
    email: str
    phone: str
    summary: Optional[str] = None


class ResumeModel(ResumeModelBase, table=True):
    __tablename__ = "resumemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_hash: str

    experiences: List[ExperienceModel] = Relationship(back_populates="parent_resume")
    educations: List[EducationModel] = Relationship(back_populates="parent_resume")
    skills: List[SkillModel] = Relationship(back_populates="parent_resume")


class ResumeModelPublic(ResumeModelBase):
    id: uuid.UUID


class ResumeModelPublicWithDetails(ResumeModelPublic):
    experiences: List[ExperienceModelPublic] = []
    educations: List[EducationModelPublic] = []
    skills: List[SkillModelPublic] = []


database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
