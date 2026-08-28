"""
Multimodal fusion model for combining image, video, and text features
"""

import numpy as np
from typing import Dict, Optional
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

from backend.models.image_model import ImageModel
from backend.models.video_model import VideoModel
from backend.models.text_model import TextModel


class FusionModel:
    """Multimodal fusion model for fault classification"""
    
    def __init__(self):
        self.image_model = ImageModel()
        self.video_model = VideoModel()
        self.text_model = TextModel()
        self.fusion_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.fault_classes = [
            "Healthy",
            "Rotor Unbalance",
            "Shaft Misalignment",
            "Bearing Fault",
            "Rotor Fault",
            "Stator Fault",
            "Mechanical Looseness",
            "Coupling Fault"
        ]
        
        # Try to load trained fusion model
        self._load_model()
    
    def _load_model(self):
        """Load trained fusion model if available"""
        model_path = Path("backend/models/trained/fusion_model.pkl")
        if model_path.exists():
            try:
                self.fusion_model = joblib.load(model_path)
                self.is_trained = True
            except Exception:
                self._initialize_fusion_model()
        else:
            self._initialize_fusion_model()
    
    def _initialize_fusion_model(self):
        """Initialize fusion model"""
        self.fusion_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            random_state=42
        )
    
    def fuse(self, image_features: Optional[Dict] = None,
             video_features: Optional[Dict] = None,
             text_features: Optional[Dict] = None) -> np.ndarray:
        """
        Fuse features from multiple modalities
        
        Args:
            image_features: Image feature dictionary
            video_features: Video feature dictionary
            text_features: Text feature dictionary
            
        Returns:
            Fused feature vector
        """
        fused_vector = []
        
        # Get predictions from individual models
        if image_features:
            image_pred = self.image_model.predict(image_features)
            fused_vector.extend([
                image_pred["confidence"],
                image_pred["probability_distribution"].get("Bearing Fault", 0),
                image_pred["probability_distribution"].get("Rotor Unbalance", 0),
                image_pred["probability_distribution"].get("Healthy", 0)
            ])
        else:
            fused_vector.extend([0, 0, 0, 0])
        
        if video_features:
            video_pred = self.video_model.predict(video_features)
            fused_vector.extend([
                video_pred["confidence"],
                video_pred["probability_distribution"].get("Mechanical Looseness", 0),
                video_pred["probability_distribution"].get("Healthy", 0)
            ])
        else:
            fused_vector.extend([0, 0, 0])
        
        if text_features:
            text_pred = self.text_model.predict(text_features)
            fused_vector.extend([
                text_pred["confidence"],
                1.0 if text_features.get("fault_keywords", {}).get("bearing", 0) > 0 else 0.0,
                1.0 if text_features.get("vibration_description", {}).get("high_vibration", False) else 0.0
            ])
        else:
            fused_vector.extend([0, 0, 0])
        
        # Add raw feature statistics if available
        if image_features:
            fused_vector.extend([
                image_features.get("irregularity", 0),
                image_features.get("nodal_density", 0),
                image_features.get("edge_density", 0)
            ])
        else:
            fused_vector.extend([0, 0, 0])
        
        if video_features:
            fused_vector.extend([
                video_features.get("temporal_variation", 0) / 100,
                video_features.get("avg_flow_magnitude", 0) / 10
            ])
        else:
            fused_vector.extend([0, 0])
        
        return np.array(fused_vector)
    
    def classify(self, fused_features: np.ndarray) -> Dict:
        """
        Classify fault using fused features
        
        Args:
            fused_features: Fused feature vector
            
        Returns:
            Prediction dictionary
        """
        if not self.is_trained:
            return self._demo_classification(fused_features)
        
        # Scale features
        fused_features_scaled = self.scaler.transform([fused_features])
        
        # Predict
        prediction = self.fusion_model.predict(fused_features_scaled)[0]
        probabilities = self.fusion_model.predict_proba(fused_features_scaled)[0]
        
        prob_distribution = {
            self.fault_classes[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        return {
            "predicted_fault": prediction,
            "confidence": float(max(probabilities)),
            "probability_distribution": prob_distribution
        }
    
    def _demo_classification(self, fused_features: np.ndarray) -> Dict:
        """Generate demo classification"""
        import random
        
        probabilities = {fault: random.uniform(0.01, 0.1) for fault in self.fault_classes}
        
        # Bias based on fused features
        if len(fused_features) > 0:
            # Check for high irregularity (first image feature)
            if len(fused_features) >= 10 and fused_features[9] > 0.5:
                probabilities["Bearing Fault"] = random.uniform(0.6, 0.85)
            # Check for high temporal variation
            elif len(fused_features) >= 12 and fused_features[11] > 0.3:
                probabilities["Mechanical Looseness"] = random.uniform(0.6, 0.85)
            else:
                probabilities["Healthy"] = random.uniform(0.4, 0.6)
        
        total = sum(probabilities.values())
        probabilities = {k: v/total for k, v in probabilities.items()}
        
        predicted_fault = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_fault]
        
        return {
            "predicted_fault": predicted_fault,
            "confidence": confidence,
            "probability_distribution": probabilities
        }
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train fusion model"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.fusion_model.fit(X_train_scaled, y_train)
        self.is_trained = True
        self._save_model()
        
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            accuracy = self.fusion_model.score(X_val_scaled, y_val)
            return {"accuracy": accuracy}
        
        return {"status": "trained"}
    
    def _save_model(self):
        """Save trained fusion model"""
        model_dir = Path("backend/models/trained")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.fusion_model, model_dir / "fusion_model.pkl")
        joblib.dump(self.scaler, model_dir / "fusion_scaler.pkl")
