from typing import Optional, Sequence

from sqlmodel import Session, select

from db.models import (
    ResumeModel,
    engine,
    ExperienceModel,
    EducationModel,
    SkillModel,
    File,
)
from llm.kie.guided_gen import Resume
from utils.utils import parse_date


def find_resume_by_id(resume_id: str) -> Optional[ResumeModel]:
    with Session(engine) as session:
        statement = select(ResumeModel).where(ResumeModel.id == resume_id)
        result = session.exec(statement).first()
        return result


def find_resume_by_hash(file_hash: str) -> Optional[ResumeModel]:
    with Session(engine) as session:
        statement = select(File).where(File.file_hash == file_hash)
        result = session.exec(statement).first()
        return result


def insert_new_resume(resume_data: Resume, file_hash: str) -> None:
    with Session(engine) as session:
        experiences = [
            ExperienceModel(
                **exp.model_dump(exclude={"start_date", "end_date"}),
                summary=str(exp),
                start_date=parse_date(exp.start_date),
                end_date=parse_date(exp.end_date),
            )
            for exp in resume_data.experiences
        ]

        educations = [
            EducationModel(
                **edu.model_dump(exclude={"start_date", "end_date"}),
                summary=str(edu),
                start_date=parse_date(edu.start_date),
                end_date=parse_date(edu.end_date),
            )
            for edu in resume_data.educations
        ]

        skills = [SkillModel(**skill.model_dump()) for skill in resume_data.skills]

        resume = ResumeModel(
            file_hash=file_hash,
            **resume_data.model_dump(exclude={"experiences", "educations", "skills"}),
            experiences=experiences,
            educations=educations,
            skills=skills,
        )

        session.add(resume)
        session.commit()


def list_resumes(n: int = 10) -> Sequence[ResumeModel]:
    with Session(engine) as session:
        statement = select(ResumeModel).limit(n)
        result = session.exec(statement).scalars().all()
        return result
