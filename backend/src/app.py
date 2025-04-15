from fastapi import FastAPI, UploadFile, File
from loguru import logger
from openai import OpenAI

from src.config import settings
from src.db import find_resume_by_hash, insert_new_resume, create_tables
from src.guided_gen import Resume
from src.models import ResumeModel
from src.utils.image_utils import file_to_image, to_base64
from src.utils.utils import file_to_sha256

app = FastAPI(on_startup=[create_tables])


@app.get("/health/")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/resume_analyse/")
async def resume_analyse(files: list[UploadFile] = File(...)) -> dict[str, str]:
    assert len(files) == 1, f"Only one file is supported for now"
    file = files[0]
    file_hash = await file_to_sha256(file)
    resume = find_resume_by_hash(file_hash)
    if resume:
        logger.info(f"Resume found in the database with hash: {file_hash}")
        return {"status": "ok"}

    assert file.content_type in [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp",
    ], f"Only image files are supported for now"

    image = await file_to_image(file)

    completion = OpenAI(api_key=settings.OPENAI_API_KEY).beta.chat.completions.parse(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a resume analysis bot."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyse this resume and extract all the information. Reply with only a JSON that contains the extracted information. If an information is not available, reply with 'N/A'. Format date as 'YYYY-MM-DD'.",
                    },
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

    resume_model = ResumeModel(
        **resume_data.model_dump(),
        file_hash=file_hash,
    )

    insert_new_resume(resume_model)
    return {"status": "ok"}
