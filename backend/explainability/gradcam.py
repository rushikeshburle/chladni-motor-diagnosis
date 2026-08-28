"""
Grad-CAM and heatmap generation for explainability
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional
import uuid


class GradCAMGenerator:
    """Generate Grad-CAM heatmaps for model explainability"""
    
    def __init__(self):
        self.heatmap_dir = Path("uploads/heatmaps")
        self.heatmap_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, image_path: str, predicted_fault: str) -> Optional[str]:
        """
        Generate Grad-CAM heatmap for image
        
        Args:
            image_path: Path to input image
            predicted_fault: Predicted fault class
            
        Returns:
            Path to generated heatmap image
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # For demo mode, generate a simulated heatmap
            # In production, this would use actual model gradients
            heatmap = self._generate_demo_heatmap(image, predicted_fault)
            
            # Save heatmap
            heatmap_filename = f"heatmap_{uuid.uuid4().hex}.png"
            heatmap_path = self.heatmap_dir / heatmap_filename
            cv2.imwrite(str(heatmap_path), heatmap)
            
            return str(heatmap_path)
            
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return None
    
    def _generate_demo_heatmap(self, image: np.ndarray, fault: str) -> np.ndarray:
        """
        Generate a demonstration heatmap
        In production, replace with actual Grad-CAM implementation
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        
        # Detect edges
        edges = cv2.Canny(blurred, 50, 150)
        
        # Create heatmap by coloring edges
        heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
        
        # Resize to match original image
        heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
        
        # Blend with original image
        alpha = 0.4
        blended = cv2.addWeighted(image, 1-alpha, heatmap, alpha, 0)
        
        return blended
    
    def generate_saliency_map(self, image_path: str) -> Optional[str]:
        """
        Generate saliency map for image
        
        Args:
            image_path: Path to input image
            
        Returns:
            Path to generated saliency map
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Compute gradient magnitude
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            
            # Normalize
            gradient_magnitude = (gradient_magnitude / gradient_magnitude.max() * 255).astype(np.uint8)
            
            # Apply colormap
            saliency = cv2.applyColorMap(gradient_magnitude, cv2.COLORMAP_HOT)
            
            # Save
            saliency_filename = f"saliency_{uuid.uuid4().hex}.png"
            saliency_path = self.heatmap_dir / saliency_filename
            cv2.imwrite(str(saliency_path), saliency)
            
            return str(saliency_path)
            
        except Exception as e:
            print(f"Error generating saliency map: {e}")
            return None
    
    def overlay_heatmap(self, image_path: str, heatmap_path: str, alpha: float = 0.5) -> Optional[str]:
        """
        Overlay heatmap on original image
        
        Args:
            image_path: Path to original image
            heatmap_path: Path to heatmap
            alpha: Blending factor
            
        Returns:
            Path to overlay image
        """
        try:
            image = cv2.imread(image_path)
            heatmap = cv2.imread(heatmap_path)
            
            if image is None or heatmap is None:
                return None
            
            # Resize heatmap to match image
            heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
            
            # Blend
            overlay = cv2.addWeighted(image, 1-alpha, heatmap, alpha, 0)
            
            # Save
            overlay_filename = f"overlay_{uuid.uuid4().hex}.png"
            overlay_path = self.heatmap_dir / overlay_filename
            cv2.imwrite(str(overlay_path), overlay)
            
            return str(overlay_path)
            
        except Exception as e:
            print(f"Error creating overlay: {e}")
            return None


class FeatureImportanceVisualizer:
    """Visualize feature importance for explainability"""
    
    @staticmethod
    def generate_feature_chart(feature_importance: list, output_path: str):
        """
        Generate a bar chart of feature importance
        
        Args:
            feature_importance: List of feature importance dictionaries
            output_path: Path to save chart
        """
        try:
            import matplotlib.pyplot as plt
            
            features = [f["feature"] for f in feature_importance]
            contributions = [1 if f["contribution"] == "High" else 
                           0.5 if f["contribution"] == "Medium" else 0.25 
                           for f in feature_importance]
            
            plt.figure(figsize=(10, 6))
            plt.barh(features, contributions, color='steelblue')
            plt.xlabel('Importance Level')
            plt.ylabel('Features')
            plt.title('Feature Importance for Diagnosis')
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            
        except Exception as e:
            print(f"Error generating feature chart: {e}")
