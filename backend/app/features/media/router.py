from fastapi import APIRouter, File, UploadFile
import os
import uuid
from app.core.config import settings

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Return URL (Hardcoded localhost for now as in old main.py)
    # In production, this should be a configurable base URL
    return {"url": f"http://localhost:8000/uploads/{filename}"}
