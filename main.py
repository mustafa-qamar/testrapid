from dotenv import load_dotenv
from dependecies import verify_rapidapi_request
from dependecies import RapidAPIIdentity
load_dotenv()

from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastapi import Request, UploadFile, File, Form
import logging


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload-test")


@app.post("/testapi")
async def upload_file(
    request: Request,
    rapidapi: RapidAPIIdentity = Depends(verify_rapidapi_request),
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

    print("RapidAPI User:", request.headers.get("x-rapidapi-user"))
    print("RapidAPI Subscription:", request.headers.get("x-rapidapi-subscription"))
    print("Mashape User:", request.headers.get("x-mashape-user"))
    print("Mashape Subscription:", request.headers.get("x-mashape-subscription"))
    print("RapidAPI Host:", request.headers.get("x-rapidapi-host"))
    print("RapidAPI Request ID:", request.headers.get("x-rapidapi-request-id"))
    print(
        "RapidAPI Proxy Secret Present:",
        bool(request.headers.get("x-rapidapi-proxy-secret"))
    )

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "description": description,
        "status": "worked"
    }


# @app.post("/testapi")
# async def debug_request(request: Request,
#                         file: UploadFile = File(...),
#                         description: str = Form("Test upload"),
#                         ):
#     print("Content-Type:", request.headers.get("content-type"))
#     body = await request.body()
#     print("Body preview:", body[:1000].decode("utf-8", errors="replace"))
#
#     return {
#         "content_type": request.headers.get("content-type"),
#         "body_length": len(body),
#     }


# @app.post("/upload")
# async def upload_file(
#     request: Request,
#     file: UploadFile = File(...),
#     description: str = Form("Test upload"),
# ):
#     content = await file.read()
#
#     # Inspect incoming request metadata without exposing secrets
#     logger.info("Request headers: %s", list(request.headers.keys()))
#     logger.info("RapidAPI host: %s", request.headers.get("x-rapidapi-host"))
#     logger.info(
#         "RapidAPI key received: %s",
#         "Yes" if request.headers.get("x-rapidapi-key") else "No",
#     )
#     logger.info("Filename: %s", file.filename)
#     logger.info("Content type: %s", file.content_type)
#     logger.info("File size: %s bytes", len(content))
#     logger.info("Description: %s", description)
#
#     return {
#         "message": "Upload successful",
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "file_size": len(content),
#         "description": description,
#     }

