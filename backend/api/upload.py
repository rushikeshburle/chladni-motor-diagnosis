"""
File upload API endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uuid
import shutil
from typing import Optional

upload_router = APIRouter()

# Upload directory
UPLOAD_DIR = Path("uploads/temp")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# Maximum file sizes (in bytes)
MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB


@upload_router.get("/file/{filename}")
async def get_file(filename: str):
    """
    Serve an uploaded file
    """
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve file: {str(e)}")


@upload_router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file for vibration pattern analysis
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image format. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )
        
        # Read file content to check size
        content = await file.read()
        if len(content) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Image too large. Maximum size: {MAX_IMAGE_SIZE // (1024*1024)} MB"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Get file info
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(content))
        
        return {
            "success": True,
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": str(file_path),
            "file_size": len(content),
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "message": "Image uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@upload_router.post("/video")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file for vibration analysis
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_VIDEO_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid video format. Allowed: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
            )
        
        # Read file content to check size
        content = await file.read()
        if len(content) > MAX_VIDEO_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Video too large. Maximum size: {MAX_VIDEO_SIZE // (1024*1024)} MB"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Get video metadata
        import cv2
        temp_video = cv2.VideoCapture(str(file_path))
        frame_count = int(temp_video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = temp_video.get(cv2.CAP_PROP_FPS)
        width = int(temp_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(temp_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        temp_video.release()
        
        return {
            "success": True,
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": str(file_path),
            "file_size": len(content),
            "frame_count": frame_count,
            "fps": fps,
            "width": width,
            "height": height,
            "duration": duration,
            "message": "Video uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@upload_router.delete("/{filename}")
async def delete_file(filename: str):
    """
    Delete an uploaded file
    """
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()
            return {"success": True, "message": "File deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
