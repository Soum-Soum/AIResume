import hashlib

from fastapi import UploadFile


async def file_to_sha256(file: UploadFile) -> str:
    await file.seek(0)
    content = await file.read()
    return hashlib.sha256(content).hexdigest()