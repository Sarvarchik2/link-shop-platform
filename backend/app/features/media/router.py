from fastapi import APIRouter, File, UploadFile
import uuid
from app.core.storage import storage

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    
    # Save file to Minio
    content = await file.read()
    url = storage.upload_file(filename, content, file.content_type)
    
    # Return URL
    return {"url": url}
