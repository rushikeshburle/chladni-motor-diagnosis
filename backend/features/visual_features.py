"""
Visual feature extraction for image-based analysis
"""

import cv2
import numpy as np
from typing import Dict
from scipy import stats


class VisualFeatureExtractor:
    """Extract general visual features from images"""
    
    def __init__(self):
        pass
    
    def extract(self, processed_image: np.ndarray) -> Dict:
        """
        Extract visual features from preprocessed image
        
        Args:
            processed_image: Preprocessed grayscale image
            
        Returns:
            Dictionary of visual features
        """
        features = {}
        
        # Statistical features
        features.update(self._extract_statistical_features(processed_image))
        
        # Shape descriptors
        features.update(self._extract_shape_descriptors(processed_image))
        
        # Frequency domain features
        features.update(self._extract_frequency_features(processed_image))
        
        # Connected component features
        features.update(self._extract_connected_component_features(processed_image))
        
        # Pattern irregularity
        features["irregularity"] = self._calculate_irregularity(processed_image)
        
        return features
    
    def _extract_statistical_features(self, image: np.ndarray) -> Dict:
        """Extract statistical features"""
        return {
            "mean_intensity": np.mean(image),
            "std_intensity": np.std(image),
            "min_intensity": np.min(image),
            "max_intensity": np.max(image),
            "median_intensity": np.median(image),
            "skewness": stats.skew(image.flatten()),
            "kurtosis": stats.kurtosis(image.flatten())
        }
    
    def _extract_shape_descriptors(self, image: np.ndarray) -> Dict:
        """Extract shape descriptors"""
        # Threshold to get binary
        _, binary = cv2.threshold((image * 255).astype(np.uint8), 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {
                "aspect_ratio": 1.0,
                "extent": 0.0,
                "solidity": 0.0,
                "convexity": 0.0
            }
        
        # Use largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        aspect_ratio = float(w) / h if h > 0 else 1.0
        
        # Area properties
        area = cv2.contourArea(largest_contour)
        bounding_area = w * h
        extent = area / bounding_area if bounding_area > 0 else 0
        
        # Solidity
        hull = cv2.convexHull(largest_contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0
        
        # Convexity
        convex_hull = cv2.convexHull(largest_contour)
        convexity = cv2.contourArea(convex_hull) / area if area > 0 else 0
        
        return {
            "aspect_ratio": aspect_ratio,
            "extent": extent,
            "solidity": solidity,
            "convexity": convexity
        }
    
    def _extract_frequency_features(self, image: np.ndarray) -> Dict:
        """Extract frequency domain features using FFT"""
        # Compute 2D FFT
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shift)
        
        # Calculate spectral features
        total_energy = np.sum(magnitude_spectrum**2)
        
        # Low frequency energy (center region)
        h, w = magnitude_spectrum.shape
        center_h, center_w = h//2, w//2
        low_freq_region = magnitude_spectrum[center_h-10:center_h+10, center_w-10:center_w+10]
        low_freq_energy = np.sum(low_freq_region**2)
        
        # High frequency energy (edges)
        high_freq_energy = total_energy - low_freq_energy
        
        # Spectral centroid
        y_coords, x_coords = np.indices(magnitude_spectrum.shape)
        centroid_y = np.sum(y_coords * magnitude_spectrum) / np.sum(magnitude_spectrum)
        centroid_x = np.sum(x_coords * magnitude_spectrum) / np.sum(magnitude_spectrum)
        
        return {
            "total_energy": total_energy,
            "low_freq_energy": low_freq_energy / total_energy if total_energy > 0 else 0,
            "high_freq_energy": high_freq_energy / total_energy if total_energy > 0 else 0,
            "spectral_centroid_y": centroid_y / h,
            "spectral_centroid_x": centroid_x / w
        }
    
    def _extract_connected_component_features(self, image: np.ndarray) -> Dict:
        """Extract connected component features"""
        from skimage.measure import label, regionprops
        
        # Threshold
        _, binary = cv2.threshold((image * 255).astype(np.uint8), 127, 255, cv2.THRESH_BINARY)
        
        # Label components
        labeled = label(binary)
        regions = regionprops(labeled)
        
        if not regions:
            return {
                "num_components": 0,
                "avg_component_size": 0,
                "max_component_size": 0
            }
        
        sizes = [r.area for r in regions]
        
        return {
            "num_components": len(regions),
            "avg_component_size": np.mean(sizes),
            "max_component_size": max(sizes)
        }
    
    def _calculate_irregularity(self, image: np.ndarray) -> float:
        """
        Calculate pattern irregularity score
        Higher values indicate more irregular patterns
        """
        # Use edge density and gradient variation
        edges = cv2.Canny((image * 255).astype(np.uint8), 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Gradient variation
        sobel_x = cv2.Sobel((image * 255).astype(np.uint8), cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel((image * 255).astype(np.uint8), cv2.CV_64F, 0, 1, ksize=3)
        gradient_variation = np.std(np.sqrt(sobel_x**2 + sobel_y**2))
        
        # Combine metrics
        irregularity = (edge_density * 0.5) + (gradient_variation / 255 * 0.5)
        
        return irregularity
