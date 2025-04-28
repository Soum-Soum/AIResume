import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

from config import settings


class File(SQLModel, table=True):
    __tablename__ = "file"

    file_hash: str = Field(primary_key=True)
    file_name: str = Field(nullable=False)
    file_path: str = Field(nullable=False)

    resumes: List["ResumeModel"] = Relationship(back_populates="file")


class WithDate(SQLModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ExperienceModelBase(WithDate):
    title: str
    company: str
    location: str
    description: Optional[str] = None

    def __str__(self):
        return f"{self.title} at {self.company} ({self.start_date} - {self.end_date}). Description: {self.description}"


class ExperienceModelPublic(ExperienceModelBase):
    id: uuid.UUID


class ExperienceModel(ExperienceModelBase, table=True):
    __tablename__ = "experiencemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resumemodel.id")
    parent_resume: "ResumeModel" = Relationship(back_populates="experiences")


class EducationModelBase(WithDate):
    institution: str
    degree: str
    location: str
    field_of_study: str
    description: Optional[str] = None

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution} ({self.start_date} - {self.end_date}). Description: {self.description}"


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

    def __str__(self):
        return f"{self.name} ({self.level})"


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
    introduction: Optional[str] = None


class ResumeModel(ResumeModelBase, table=True):
    __tablename__ = "resumemodel"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_hash: str = Field(foreign_key="file.file_hash")

    file: File = Relationship(back_populates="resumes")
    experiences: List[ExperienceModel] = Relationship(back_populates="parent_resume")
    educations: List[EducationModel] = Relationship(back_populates="parent_resume")
    skills: List[SkillModel] = Relationship(back_populates="parent_resume")


class ResumeModelPublic(ResumeModelBase):
    id: uuid.UUID


class ResumeModelPublicWithDetails(ResumeModelPublic):
    experiences: List[ExperienceModelPublic] = []
    educations: List[EducationModelPublic] = []
    skills: List[SkillModelPublic] = []

    def __str__(self):
        experiences_str = "\n".join([str(exp) for exp in self.experiences])
        educations_str = "\n".join([str(edu) for edu in self.educations])
        return (
            f"Introduction: {self.introduction}\n"
            f"Experiences:\n{experiences_str}\n"
            f"Educations:\n{educations_str}\n"
            f"Skills: {', '.join([str(skill) for skill in self.skills])}\n"
        )


database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
