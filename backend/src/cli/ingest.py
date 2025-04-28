from pathlib import Path
import requests
import typer
import mimetypes
from loguru import logger

app = typer.Typer()


@app.command()
def ingest(
    data_dir: Path = typer.Argument(..., help="Directory containing resume files"),
    api_host: str = typer.Option("http://localhost:9093", help="API host"),
    limit: int = typer.Option(-1, help="Limit the number of files to ingest"),
):
    extensions = [".png", ".jpg", ".jpeg", ".webp"]
    files = sum(
        [list(Path(data_dir).rglob(f"*{ext}")) for ext in extensions],
        [],
    )

    logger.info(f"Found {len(files)} files in {data_dir} with extensions {extensions}")

    if limit > 0:
        logger.info(f"Limiting ingestion to {limit} files")
        files = files[:limit]

    for file in files:
        mime_type, _ = mimetypes.guess_type(file)
        if not mime_type:
            logger.warning(
                f"Could not guess MIME type for {file}, defaulting to 'application/octet-stream'"
            )
            mime_type = "application/octet-stream"

        with open(file, "rb") as f:
            response = requests.post(
                f"{api_host}/resume_analyse/",
                files={"files": (file.name, f, mime_type)},
            )
        if response.status_code == 200:
            logger.info(f"Successfully ingested {file}")
        else:
            logger.error(f"Failed to ingest {file}: {response.text}")
            raise Exception(f"Failed to ingest {file}: {response.text}")


if __name__ == "__main__":
    app()
