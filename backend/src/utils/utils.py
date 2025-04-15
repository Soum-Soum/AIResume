from datetime import datetime
import hashlib
from typing import Optional

import dateparser
from fastapi import UploadFile


async def file_to_sha256(file: UploadFile) -> str:
    await file.seek(0)
    content = await file.read()
    return hashlib.sha256(content).hexdigest()


def parse_date(date_str: str) -> Optional[datetime]:
    if date_str == "N/A":
        return None
    try:
        return dateparser.parse(date_str)
    except Exception as e:
        return None
