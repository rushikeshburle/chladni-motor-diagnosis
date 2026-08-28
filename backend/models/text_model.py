"""
Text-based fault classification model
"""

import numpy as np
from typing import Dict, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path


class TextModel:
    """Text-based fault classification model for operating conditions"""
    
    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.model = None
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
        
        # Try to load trained model
        self._load_model()
    
    def _load_model(self):
        """Load trained model if available"""
        model_path = Path("backend/models/trained/text_model.pkl")
        if model_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.is_trained = True
            except Exception:
                self._initialize_model()
        else:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize model"""
        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=8,
            random_state=42
        )
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train the model"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        self._save_model()
        
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            accuracy = self.model.score(X_val_scaled, y_val)
            return {"accuracy": accuracy}
        
        return {"status": "trained"}
    
    def predict(self, features: Dict) -> Dict:
        """Predict fault from text features"""
        if not self.is_trained:
            return self._demo_prediction(features)
        
        feature_vector = self._features_to_vector(features)
        if feature_vector is None:
            return self._demo_prediction(features)
        
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        prediction = self.model.predict(feature_vector_scaled)[0]
        probabilities = self.model.predict_proba(feature_vector_scaled)[0]
        
        prob_distribution = {
            self.fault_classes[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        return {
            "predicted_fault": prediction,
            "confidence": float(max(probabilities)),
            "probability_distribution": prob_distribution
        }
    
    def _features_to_vector(self, features: Dict) -> Optional[np.ndarray]:
        """Convert features to vector"""
        try:
            # Numerical features
            vector = [
                features.get("rpm", 1500) / 3000,
                features.get("load_percent", 50) / 100,
                features.get("temperature", 50) / 100,
                features.get("text_length", 0) / 500,
                features.get("word_count", 0) / 100
            ]
            
            # Fault keyword counts
            fault_keywords = features.get("fault_keywords", {})
            for fault in ["bearing", "rotor", "stator", "unbalance", "misalignment", "looseness", "coupling"]:
                count = fault_keywords.get(fault, 0)
                vector.append(min(count / 3, 1.0))
            
            # Vibration indicators
            vib_desc = features.get("vibration_description", {})
            vector.extend([
                1.0 if vib_desc.get("high_vibration", False) else 0.0,
                1.0 if vib_desc.get("location_bearing", False) else 0.0,
                1.0 if vib_desc.get("location_housing", False) else 0.0
            ])
            
            return np.array(vector)
        except Exception:
            return None
    
    def _demo_prediction(self, features: Dict) -> Dict:
        """Generate demo prediction"""
        import random
        
        probabilities = {fault: random.uniform(0.01, 0.1) for fault in self.fault_classes}
        
        # Bias based on fault keywords
        fault_keywords = features.get("fault_keywords", {})
        if "bearing" in fault_keywords and fault_keywords["bearing"] > 0:
            probabilities["Bearing Fault"] = random.uniform(0.7, 0.9)
        elif "unbalance" in fault_keywords:
            probabilities["Rotor Unbalance"] = random.uniform(0.7, 0.9)
        else:
            probabilities["Healthy"] = random.uniform(0.5, 0.7)
        
        total = sum(probabilities.values())
        probabilities = {k: v/total for k, v in probabilities.items()}
        
        predicted_fault = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_fault]
        
        return {
            "predicted_fault": predicted_fault,
            "confidence": confidence,
            "probability_distribution": probabilities
        }
    
    def _save_model(self):
        """Save trained model"""
        model_dir = Path("backend/models/trained")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, model_dir / "text_model.pkl")
        joblib.dump(self.scaler, model_dir / "text_scaler.pkl")
