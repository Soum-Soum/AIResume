import base64
import io
from io import BytesIO

from PIL import Image
from PIL.Image import Image as PILImage
from fastapi import UploadFile


def to_base64(image: PILImage) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


async def file_to_image(file: UploadFile) -> PILImage:
    await file.seek(0)
    return Image.open(io.BytesIO(await file.read()))
