from fastapi import APIRouter, File, UploadFile
import uuid
import os
from pathlib import Path

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
        
        # Read file content
        content = await file.read()
        
        # Try Minio first if available
        try:
            from app.core.storage import storage
            url = storage.upload_file(filename, content, file.content_type)
            logger.info(f"Successfully uploaded {filename} to Minio: {url}")
            return {"url": url}
        except Exception as minio_error:
            logger.warning(f"Minio not available: {minio_error}, falling back to local storage")
            
            # Fallback to local storage
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            file_path = upload_dir / filename
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Return relative URL
            base_url = os.getenv("BASE_URL", "https://link-shop-platform-production.up.railway.app")
            url = f"{base_url}/uploads/{filename}"
            
            logger.info(f"Successfully uploaded {filename} locally: {url}")
            return {"url": url}
            
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )
