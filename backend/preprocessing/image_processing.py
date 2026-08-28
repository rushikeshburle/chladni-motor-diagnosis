"""
Image preprocessing module for vibration pattern analysis
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image


class ImageProcessor:
    """Process images for Chladni pattern analysis"""
    
    def __init__(self, target_size: Tuple[int, int] = (512, 512)):
        self.target_size = target_size
        self.min_size = (64, 64)  # Minimum acceptable image size
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            img = Image.open(image_path)
            img.verify()  # Verify it's a valid image
            
            # Check dimensions
            img = Image.open(image_path)
            if img.size[0] < self.min_size[0] or img.size[1] < self.min_size[1]:
                return False
            
            return True
        except Exception:
            return False
    
    def process(self, image_path: str) -> np.ndarray:
        """
        Complete image preprocessing pipeline
        
        Args:
            image_path: Path to image file
            
        Returns:
            Processed image as numpy array
        """
        # Validate image
        if not self.validate_image(image_path):
            raise ValueError(f"Invalid image: {image_path}")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Step 1: Resize
        image = self._resize(image)
        
        # Step 2: Convert to grayscale
        gray = self._to_grayscale(image)
        
        # Step 3: Noise reduction
        denoised = self._remove_noise(gray)
        
        # Step 4: Contrast enhancement
        enhanced = self._enhance_contrast(denoised)
        
        # Step 5: Normalization
        normalized = self._normalize(enhanced)
        
        # Step 6: Optional Gaussian filtering
        filtered = self._gaussian_filter(normalized)
        
        return filtered
    
    def _resize(self, image: np.ndarray) -> np.ndarray:
        """Resize image to target size while maintaining aspect ratio"""
        h, w = image.shape[:2]
        
        # Calculate scaling factor
        scale = min(self.target_size[0] / w, self.target_size[1] / h)
        
        # Resize
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Pad to target size
        pad_w = self.target_size[0] - new_w
        pad_h = self.target_size[1] - new_h
        padded = cv2.copyMakeBorder(
            resized, 
            pad_h // 2, pad_h - pad_h // 2,
            pad_w // 2, pad_w - pad_w // 2,
            cv2.BORDER_CONSTANT, 
            value=[0, 0, 0]
        )
        
        return padded
    
    def _to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def _remove_noise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise using bilateral filter"""
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Enhance contrast using CLAHE"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)
    
    def _normalize(self, image: np.ndarray) -> np.ndarray:
        """Normalize pixel values to [0, 1] range"""
        return image.astype(np.float32) / 255.0
    
    def _gaussian_filter(self, image: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        """Apply Gaussian blur for smoothing"""
        return cv2.GaussianBlur(image, (5, 5), sigma)
    
    def segment_pattern(self, image: np.ndarray) -> np.ndarray:
        """
        Segment the vibration pattern region
        
        Args:
            image: Preprocessed grayscale image
            
        Returns:
            Binary mask of pattern region
        """
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(
            (image * 255).astype(np.uint8),
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        return closed
    
    def detect_edges(self, image: np.ndarray) -> np.ndarray:
        """
        Detect edges using Canny edge detector
        
        Args:
            image: Preprocessed grayscale image
            
        Returns:
            Edge map
        """
        # Convert back to uint8 for Canny
        img_uint8 = (image * 255).astype(np.uint8)
        
        # Canny edge detection
        edges = cv2.Canny(img_uint8, 50, 150)
        
        return edges
    
    def detect_contours(self, binary_mask: np.ndarray) -> list:
        """
        Detect contours in binary mask
        
        Args:
            binary_mask: Binary mask
            
        Returns:
            List of contours
        """
        contours, _ = cv2.findContours(
            binary_mask.astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours
