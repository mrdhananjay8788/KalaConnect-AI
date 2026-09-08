import os
import uuid
import time
from typing import Optional
from app.core.logging import logger

class StorageService:
    def __init__(self, base_dir: str = "data/images"):
        self.base_dir = base_dir
        self.original_dir = os.path.join(self.base_dir, "original")
        self.processed_dir = os.path.join(self.base_dir, "processed")
        self.temp_dir = os.path.join(self.base_dir, "temporary")

        for d in [self.original_dir, self.processed_dir, self.temp_dir]:
            os.makedirs(d, exist_ok=True)

    def save_temp_image(self, image_bytes: bytes, ext: str = ".jpg") -> str:
        """Save an image to the temporary directory and return its path."""
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        return filepath

    def save_original_image(self, image_bytes: bytes, ext: str = ".jpg") -> str:
        """Save an original uploaded image and return its path."""
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(self.original_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        return filepath

    def save_processed_image(self, image_bytes: bytes, ext: str = ".webp") -> str:
        """Save a processed e-commerce image and return its path."""
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(self.processed_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        return filepath

    def cleanup_temp_files(self, max_age_seconds: int = 3600):
        """Clean up temporary files older than max_age_seconds."""
        now = time.time()
        for filename in os.listdir(self.temp_dir):
            filepath = os.path.join(self.temp_dir, filename)
            if os.path.isfile(filepath):
                if os.stat(filepath).st_mtime < now - max_age_seconds:
                    try:
                        os.remove(filepath)
                        logger.info(f"Cleaned up temporary file: {filepath}")
                    except Exception as e:
                        logger.error(f"Error cleaning up file {filepath}: {e}")

    def delete_file(self, filepath: str):
        """Delete a specific file securely."""
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.error(f"Error deleting file {filepath}: {e}")

storage_service = StorageService()
