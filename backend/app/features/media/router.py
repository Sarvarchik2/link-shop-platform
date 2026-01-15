from fastapi import APIRouter, File, UploadFile
import uuid
from app.core.storage import storage

router = APIRouter()

import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4()}.{ext}"
        
        logger.info(f"Starting upload for file: {file.filename} as {filename}")
        
        # Save file to Minio
        content = await file.read()
        url = storage.upload_file(filename, content, file.content_type)
        
        logger.info(f"Successfully uploaded {filename} to {url}")
        
        # Return URL
        return {"url": url}
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )
