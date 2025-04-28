from typing import Literal, Type

from PIL.Image import Image as PILImage
from litellm import acompletion

from pydantic import BaseModel, Field

from config import settings
from utils.image_utils import to_base64


class WithDates(BaseModel):
    start_date: str = Field(
        description="The date when the experience or education started. Format: YYYY-MM-DD"
    )
    end_date: str = Field(
        description="The date when the experience or education ended. Format: YYYY-MM-DD"
    )


class Experience(WithDates):
    title: str = Field(description="The title of the job or position held.")
    company: str = Field(description="The name of the company or organization.")
    location: str = Field(description="The location of the company or organization.")
    description: str = Field(
        description="Any details that the resume holder wants to add about the experience."
    )


class Education(WithDates):
    institution: str = Field(
        description="The name of the educational institution/university/school..."
    )
    degree: str = Field(description="The name of the degree obtained.")
    location: str = Field(description="The location of the educational institution.")
    field_of_study: str = Field(description="The field of study or major (if present).")
    description: str = Field(
        description="Any details that the resume holder wants to add about the education."
    )


class Skill(BaseModel):
    name: str = Field(description="The name of the skill.")
    level: Literal["beginner", "intermediate", "advanced", "expert"] = Field(
        description="The level of the skill. Can be one of the following: beginner, intermediate, advanced, expert."
    )


class Resume(BaseModel):
    name: str = Field(description="The name of the resume holder.")
    email: str = Field(description="The email address of the resume holder.")
    phone: str = Field(description="The phone number of the resume holder.")
    introduction: str = Field(
        description="A text that the resume holder put (often at the beginning of the resume) to introduce himself/herself."
    )
    experiences: list[Experience] = Field(
        description="A list of experiences of the resume holder."
    )
    educations: list[Education] = Field(
        description="A list of educations of the resume holder."
    )
    skills: list[Skill] = Field(description="A list of skills of the resume holder.")


def to_fields_description_dict(model: Type[BaseModel]) -> dict[str, str]:
    """
    Convert a Pydantic model to a dictionary of field names and descriptions.
    """
    return {
        field: field_info.description
        for field, field_info in model.model_fields.items()
        if field_info.description is not None
    }


async def extract_resume_information(image: PILImage) -> Resume:
    models_to_describe = {
        model.__name__: to_fields_description_dict(model)
        for model in [Resume, Experience, Education, Skill]
    }

    prompt = (
        f"Analyse this resume and extract all the information.\n"
        f"Reply with only a JSON that contains the extracted information.\n"
        f"If an information is not available, reply with 'N/A'.\n"
        f"Format date as 'YYYY-MM-DD'.\n"
        f"Here are the models and their fields:\n"
        f"{models_to_describe}\n"
    )

    completion = await acompletion(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a resume analysis bot."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{to_base64(image)}"
                        },
                    },
                ],
            },
        ],
        response_format=Resume,
    )

    resume_data = Resume.model_validate_json(completion.choices[0].message.content)
    return resume_data
