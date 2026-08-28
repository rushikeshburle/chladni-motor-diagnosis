"""
Video preprocessing module for temporal vibration analysis
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional


class VideoProcessor:
    """Process videos for temporal vibration pattern analysis"""
    
    def __init__(self, target_size: Tuple[int, int] = (512, 512)):
        self.target_size = target_size
        self.frame_sample_rate = 5  # Sample every Nth frame
    
    def validate_video(self, video_path: str) -> bool:
        """
        Validate video file
        
        Args:
            video_path: Path to video file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return False
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            cap.release()
            
            # Check if video has frames and reasonable FPS
            return frame_count > 0 and fps > 0
        except Exception:
            return False
    
    def extract_frames(self, video_path: str, max_frames: int = 100) -> List[np.ndarray]:
        """
        Extract frames from video
        
        Args:
            video_path: Path to video file
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of frames as numpy arrays
        """
        if not self.validate_video(video_path):
            raise ValueError(f"Invalid video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_frames = min(frame_count, max_frames * self.frame_sample_rate)
        
        for i in range(0, total_frames, self.frame_sample_rate):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            
            if ret:
                frames.append(frame)
            
            if len(frames) >= max_frames:
                break
        
        cap.release()
        return frames
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame
        
        Args:
            frame: Input frame
            
        Returns:
            Processed frame
        """
        # Resize
        frame = self._resize(frame)
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Noise reduction
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Normalize
        normalized = enhanced.astype(np.float32) / 255.0
        
        return normalized
    
    def _resize(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame to target size"""
        return cv2.resize(frame, self.target_size, interpolation=cv2.INTER_AREA)
    
    def stabilize_frames(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """
        Stabilize frames using optical flow
        
        Args:
            frames: List of frames
            
        Returns:
            Stabilized frames
        """
        if len(frames) < 2:
            return frames
        
        stabilized = [frames[0]]
        
        # Convert to grayscale for optical flow
        gray_frames = [cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR) 
                      if len(f.shape) == 2 else f for f in frames]
        
        # Simple stabilization using frame-to-frame alignment
        for i in range(1, len(frames)):
            # Find transformation between consecutive frames
            prev_gray = cv2.cvtColor(stabilized[-1], cv2.COLOR_BGR2GRAY) if len(stabilized[-1].shape) == 3 else (stabilized[-1] * 255).astype(np.uint8)
            curr_gray = cv2.cvtColor(gray_frames[i], cv2.COLOR_BGR2GRAY) if len(gray_frames[i].shape) == 3 else (gray_frames[i] * 255).astype(np.uint8)
            
            # Use ECC for alignment
            warp_mode = cv2.MOTION_TRANSLATION
            warp_matrix = np.eye(2, 3, dtype=np.float32)
            
            try:
                _, warp_matrix = cv2.findTransformECC(
                    prev_gray, curr_gray, warp_matrix,
                    warp_mode, None
                )
                
                # Apply transformation
                aligned = cv2.warpAffine(
                    gray_frames[i], warp_matrix,
                    self.target_size,
                    flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
                )
                
                stabilized.append(aligned)
            except:
                stabilized.append(gray_frames[i])
        
        return stabilized
    
    def get_video_metadata(self, video_path: str) -> dict:
        """
        Get video metadata
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        cap = cv2.VideoCapture(video_path)
        
        metadata = {
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0
        }
        
        cap.release()
        return metadata
