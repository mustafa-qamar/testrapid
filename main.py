from fastapi import FastAPI
from fastapi import Request, UploadFile, File, Form
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload-test")


@app.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    description: str = Form("Test upload"),
):
    content = await file.read()

    # Inspect incoming request metadata without exposing secrets
    logger.info("Request headers: %s", list(request.headers.keys()))
    logger.info("RapidAPI host: %s", request.headers.get("x-rapidapi-host"))
    logger.info(
        "RapidAPI key received: %s",
        "Yes" if request.headers.get("x-rapidapi-key") else "No",
    )
    logger.info("Filename: %s", file.filename)
    logger.info("Content type: %s", file.content_type)
    logger.info("File size: %s bytes", len(content))
    logger.info("Description: %s", description)

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "description": description,
    }
