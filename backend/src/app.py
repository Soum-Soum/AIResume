import uuid

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlmodel import Session, select
from litellm import acompletion

from config import settings
from db import find_resume_by_hash, insert_new_resume
from guided_gen import Resume
from models import (
    get_session,
    ResumeModelPublicWithDetails,
    ResumeModel,
    ResumeModelPublic,
)
from utils.image_utils import file_to_image, to_base64
from utils.utils import file_to_sha256

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou ["http://localhost:5173"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    completion = await acompletion(
        api_key=settings.OPENAI_API_KEY,
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

    insert_new_resume(resume_data=resume_data, file_hash=file_hash)
    logger.info(f"Resume inserted in the database with hash: {file_hash}")
    return {"status": "ok"}


@app.get("/resume/details/{resume_uuid}", response_model=ResumeModelPublicWithDetails)
async def read_resume(*, resume_uuid: uuid.UUID, session: Session = Depends(get_session)):
    resume = session.get(ResumeModel, resume_uuid)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@app.get("/resume/list", response_model=list[ResumeModelPublic])
async def list_resumes(
    session: Session = Depends(get_session),
    limit: int = 10,
):
    return session.exec(select(ResumeModel).limit(limit)).all()
