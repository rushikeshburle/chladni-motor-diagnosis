"""
Helper utilities for the application
"""

import os
import uuid
from pathlib import Path
from typing import Optional
import mimetypes


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving extension"""
    ext = Path(original_filename).suffix
    return f"{uuid.uuid4().hex}{ext}"


def validate_file_type(filename: str, allowed_extensions: set) -> bool:
    """Validate file type against allowed extensions"""
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions


def get_mime_type(filename: str) -> Optional[str]:
    """Get MIME type of a file"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal"""
    # Remove directory separators
    sanitized = filename.replace('/', '').replace('\\', '')
    # Remove potentially dangerous characters
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c in '._-')
    return sanitized


def ensure_directory(directory: Path) -> Path:
    """Ensure directory exists, create if it doesn't"""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def cleanup_temp_files(directory: Path, max_age_hours: int = 24):
    """Clean up temporary files older than specified hours"""
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                except Exception:
                    pass


def format_file_size(bytes_size: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def validate_image_dimensions(width: int, height: int, min_size: tuple = (64, 64)) -> bool:
    """Validate image dimensions meet minimum requirements"""
    return width >= min_size[0] and height >= min_size[1]


class Config:
    """Application configuration"""
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # File Upload Configuration
    MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB
    MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
    
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
    ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
    
    # Directory Configuration
    UPLOAD_DIR = Path("uploads/temp")
    REPORT_DIR = Path("reports")
    HEATMAP_DIR = Path("uploads/heatmaps")
    MODEL_DIR = Path("backend/models/trained")
    
    # Database Configuration
    DATABASE_PATH = "motor_diagnosis.db"
    
    # Model Configuration
    FAULT_CLASSES = [
        "Healthy",
        "Rotor Unbalance",
        "Shaft Misalignment",
        "Bearing Fault",
        "Rotor Fault",
        "Stator Fault",
        "Mechanical Looseness",
        "Coupling Fault"
    ]
    
    SEVERITY_LEVELS = ["Low", "Medium", "High"]
    
    @classmethod
    def initialize_directories(cls):
        """Initialize all required directories"""
        for directory in [cls.UPLOAD_DIR, cls.REPORT_DIR, cls.HEATMAP_DIR, cls.MODEL_DIR]:
            ensure_directory(directory)
