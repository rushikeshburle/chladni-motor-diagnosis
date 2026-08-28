"""
Pattern feature extraction for Chladni pattern analysis
"""

import cv2
import numpy as np
from typing import Dict, Tuple
from scipy import ndimage
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import regionprops, label


class PatternFeatureExtractor:
    """Extract features from Chladni/vibration patterns"""
    
    def __init__(self):
        pass
    
    def extract(self, processed_image: np.ndarray) -> Dict:
        """
        Extract pattern features from preprocessed image
        
        Args:
            processed_image: Preprocessed grayscale image
            
        Returns:
            Dictionary of pattern features
        """
        features = {}
        
        # Convert to uint8 for certain operations
        img_uint8 = (processed_image * 255).astype(np.uint8)
        
        # Pattern area and region features
        features.update(self._extract_region_features(img_uint8))
        
        # Nodal line features
        features.update(self._extract_nodal_features(img_uint8))
        
        # Edge features
        features.update(self._extract_edge_features(img_uint8))
        
        # Texture features
        features.update(self._extract_texture_features(img_uint8))
        
        # Symmetry features
        features.update(self._extract_symmetry_features(processed_image))
        
        # Spatial distribution features
        features.update(self._extract_spatial_features(processed_image))
        
        return features
    
    def _extract_region_features(self, image: np.ndarray) -> Dict:
        """Extract region-based features"""
        # Threshold to get binary mask
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        
        # Label connected components
        labeled = label(binary)
        regions = regionprops(labeled)
        
        if not regions:
            return {
                "pattern_area": 0,
                "num_regions": 0,
                "avg_region_area": 0,
                "max_region_area": 0,
                "region_circularity": 0
            }
        
        areas = [r.area for r in regions]
        
        return {
            "pattern_area": sum(areas),
            "num_regions": len(regions),
            "avg_region_area": np.mean(areas),
            "max_region_area": max(areas),
            "region_circularity": self._calculate_circularity(regions[0]) if regions else 0
        }
    
    def _calculate_circularity(self, region) -> float:
        """Calculate circularity of a region"""
        if region.perimeter == 0:
            return 0
        return 4 * np.pi * region.area / (region.perimeter ** 2)
    
    def _extract_nodal_features(self, image: np.ndarray) -> Dict:
        """Extract nodal line features"""
        # Edge detection for nodal lines
        edges = cv2.Canny(image, 50, 150)
        
        # Count edge pixels
        edge_pixels = np.sum(edges > 0)
        
        # Calculate edge density
        edge_density = edge_pixels / (image.shape[0] * image.shape[1])
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=30, maxLineGap=10)
        
        num_lines = len(lines) if lines is not None else 0
        
        return {
            "nodal_density": edge_density,
            "num_nodal_lines": num_lines,
            "edge_pixel_count": edge_pixels
        }
    
    def _extract_edge_features(self, image: np.ndarray) -> Dict:
        """Extract edge-related features"""
        # Canny edges
        edges = cv2.Canny(image, 50, 150)
        
        # Sobel gradients
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        return {
            "edge_density": np.sum(edges > 0) / edges.size,
            "avg_gradient": np.mean(gradient_magnitude),
            "max_gradient": np.max(gradient_magnitude),
            "gradient_std": np.std(gradient_magnitude)
        }
    
    def _extract_texture_features(self, image: np.ndarray) -> Dict:
        """Extract texture features using GLCM"""
        # Convert to appropriate range for GLCM
        img_scaled = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
        
        # Calculate GLCM
        glcm = graycomatrix(img_scaled, distances=[1], angles=[0], 
                           levels=256, symmetric=True, normed=True)
        
        # Extract GLCM properties
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]
        
        return {
            "texture_contrast": contrast,
            "texture_dissimilarity": dissimilarity,
            "texture_homogeneity": homogeneity,
            "texture_energy": energy,
            "texture_correlation": correlation
        }
    
    def _extract_symmetry_features(self, image: np.ndarray) -> Dict:
        """Extract symmetry features"""
        h, w = image.shape
        
        # Horizontal symmetry
        left_half = image[:, :w//2]
        right_half = np.fliplr(image[:, w//2:])
        
        # Pad if needed
        if left_half.shape != right_half.shape:
            min_w = min(left_half.shape[1], right_half.shape[1])
            left_half = left_half[:, :min_w]
            right_half = right_half[:, :min_w]
        
        horizontal_symmetry = np.corrcoef(left_half.flatten(), right_half.flatten())[0, 1]
        
        # Vertical symmetry
        top_half = image[:h//2, :]
        bottom_half = np.flipud(image[h//2:, :])
        
        if top_half.shape != bottom_half.shape:
            min_h = min(top_half.shape[0], bottom_half.shape[0])
            top_half = top_half[:min_h, :]
            bottom_half = bottom_half[:min_h, :]
        
        vertical_symmetry = np.corrcoef(top_half.flatten(), bottom_half.flatten())[0, 1]
        
        return {
            "horizontal_symmetry": horizontal_symmetry if not np.isnan(horizontal_symmetry) else 0,
            "vertical_symmetry": vertical_symmetry if not np.isnan(vertical_symmetry) else 0,
            "overall_symmetry": (horizontal_symmetry + vertical_symmetry) / 2
        }
    
    def _extract_spatial_features(self, image: np.ndarray) -> Dict:
        """Extract spatial distribution features"""
        h, w = image.shape
        
        # Calculate center of mass
        total_mass = np.sum(image)
        if total_mass > 0:
            y_coords, x_coords = np.indices(image.shape)
            center_y = np.sum(y_coords * image) / total_mass
            center_x = np.sum(x_coords * image) / total_mass
        else:
            center_y, center_x = h/2, w/2
        
        # Distance from image center
        image_center_y, image_center_x = h/2, w/2
        center_offset = np.sqrt((center_y - image_center_y)**2 + (center_x - image_center_x)**2)
        
        # Radial distribution
        y_coords, x_coords = np.indices(image.shape)
        distances = np.sqrt((y_coords - center_y)**2 + (x_coords - center_x)**2)
        radial_std = np.std(distances[image > 0]) if np.any(image > 0) else 0
        
        return {
            "center_offset": center_offset / max(h, w),
            "radial_std": radial_std / max(h, w),
            "pattern_spread": np.std(image) if np.std(image) > 0 else 0
        }
