from typing import Literal

from pydantic import BaseModel


class WithDates(BaseModel):
    start_date: str
    end_date: str


class Experience(WithDates):
    title: str
    company: str
    location: str
    description: str


class Education(WithDates):
    institution: str
    degree: str
    field_of_study: str
    description: str


class Skill(BaseModel):
    name: str
    level: Literal["beginner", "intermediate", "advanced", "expert"]


class Resume(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    experiences: list[Experience]
    educations: list[Education]
    skills: list[Skill]
