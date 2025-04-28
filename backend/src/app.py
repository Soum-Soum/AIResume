import uuid

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlmodel import Session, select
from qdrant_client import QdrantClient

from config import settings
from db.db import find_resume_by_hash, insert_new_resume
from llm.kie.guided_gen import extract_resume_information
from db.models import (
    get_session,
    ResumeModelPublicWithDetails,
    ResumeModel,
    ResumeModelPublic,
    create_db_and_tables,
)
from utils.image_utils import file_to_image
from utils.utils import file_to_sha256

qdrant = QdrantClient(settings.VECTORIAL_DB_URL)
app = FastAPI(on_startup=[create_db_and_tables])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    ], f"Only image files are supported for now but got {file.content_type}"

    image = await file_to_image(file)

    resume_data = await extract_resume_information(image=image)
    logger.info(f"Resume data extracted from file {file.filename} (hash: {file_hash})")
    insert_new_resume(resume_data=resume_data, file_hash=file_hash)
    logger.info(f"Resume data successfully inserted in the database")
    return {"status": "ok"}


@app.get("/resume/details/{resume_uuid}", response_model=ResumeModelPublicWithDetails)
async def read_resume(
    *, resume_uuid: uuid.UUID, session: Session = Depends(get_session)
):
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
