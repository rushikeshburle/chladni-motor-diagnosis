"""
Temporal feature extraction for video analysis
"""

import cv2
import numpy as np
from typing import Dict, List
from scipy import stats


class TemporalFeatureExtractor:
    """Extract temporal features from video frames"""
    
    def __init__(self):
        pass
    
    def extract(self, frames: List[np.ndarray]) -> Dict:
        """
        Extract temporal features from a sequence of frames
        
        Args:
            frames: List of preprocessed frames
            
        Returns:
            Dictionary of temporal features
        """
        if not frames or len(frames) < 2:
            return {}
        
        features = {}
        
        # Frame-to-frame differences
        features.update(self._extract_frame_differences(frames))
        
        # Optical flow features
        features.update(self._extract_optical_flow_features(frames))
        
        # Temporal statistics
        features.update(self._extract_temporal_statistics(frames))
        
        # Vibration frequency estimation
        features.update(self._estimate_vibration_frequency(frames))
        
        return features
    
    def _extract_frame_differences(self, frames: List[np.ndarray]) -> Dict:
        """Extract frame-to-frame difference features"""
        differences = []
        
        for i in range(len(frames) - 1):
            diff = cv2.absdiff(
                (frames[i] * 255).astype(np.uint8),
                (frames[i+1] * 255).astype(np.uint8)
            )
            differences.append(np.mean(diff))
        
        differences = np.array(differences)
        
        return {
            "temporal_variation": np.mean(differences),
            "temporal_std": np.std(differences),
            "max_frame_diff": np.max(differences),
            "min_frame_diff": np.min(differences)
        }
    
    def _extract_optical_flow_features(self, frames: List[np.ndarray]) -> Dict:
        """Extract optical flow features"""
        # Convert to uint8
        frames_uint8 = [(f * 255).astype(np.uint8) for f in frames]
        
        flow_magnitudes = []
        
        for i in range(len(frames) - 1):
            # Calculate optical flow using Farneback method
            flow = cv2.calcOpticalFlowFarneback(
                frames_uint8[i], frames_uint8[i+1],
                None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            # Calculate magnitude
            magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            flow_magnitudes.append(np.mean(magnitude))
        
        if not flow_magnitudes:
            return {
                "avg_flow_magnitude": 0,
                "max_flow_magnitude": 0,
                "flow_std": 0
            }
        
        flow_magnitudes = np.array(flow_magnitudes)
        
        return {
            "avg_flow_magnitude": np.mean(flow_magnitudes),
            "max_flow_magnitude": np.max(flow_magnitudes),
            "flow_std": np.std(flow_magnitudes)
        }
    
    def _extract_temporal_statistics(self, frames: List[np.ndarray]) -> Dict:
        """Extract temporal statistical features"""
        # Calculate intensity statistics across frames
        frame_means = [np.mean(f) for f in frames]
        frame_stds = [np.std(f) for f in frames]
        
        return {
            "mean_intensity_mean": np.mean(frame_means),
            "mean_intensity_std": np.std(frame_means),
            "std_intensity_mean": np.mean(frame_stds),
            "std_intensity_std": np.std(frame_stds),
            "intensity_trend": np.polyfit(range(len(frame_means)), frame_means, 1)[0] if len(frame_means) > 1 else 0
        }
    
    def _estimate_vibration_frequency(self, frames: List[np.ndarray]) -> Dict:
        """Estimate vibration frequency from frame sequence"""
        # Calculate center of mass for each frame
        centers = []
        for frame in frames:
            total = np.sum(frame)
            if total > 0:
                y_coords, x_coords = np.indices(frame.shape)
                center_y = np.sum(y_coords * frame) / total
                center_x = np.sum(x_coords * frame) / total
                centers.append((center_y, center_x))
        
        if len(centers) < 4:
            return {
                "estimated_frequency": 0,
                "dominant_period": 0
            }
        
        # Extract y-coordinate movement
        y_positions = [c[0] for c in centers]
        
        # Calculate FFT to find dominant frequency
        fft_result = np.fft.fft(y_positions - np.mean(y_positions))
        freqs = np.fft.fftfreq(len(y_positions))
        
        # Find dominant frequency (excluding DC component)
        dominant_idx = np.argmax(np.abs(fft_result[1:len(fft_result)//2])) + 1
        dominant_freq = abs(freqs[dominant_idx])
        
        # Period in frames
        period = 1 / dominant_freq if dominant_freq > 0 else len(y_positions)
        
        return {
            "estimated_frequency": dominant_freq,
            "dominant_period": period
        }
