"""
Text preprocessing module for operating condition analysis
"""

import re
import numpy as np
from typing import Dict, List, Optional


class TextProcessor:
    """Process text input for motor operating conditions"""
    
    def __init__(self):
        # Define patterns for extracting motor parameters
        self.rpm_pattern = re.compile(r'(\d+)\s*(?:rpm|RPM)', re.IGNORECASE)
        self.load_pattern = re.compile(r'(\d+)\s*(?:%|percent|load)', re.IGNORECASE)
        self.temp_pattern = re.compile(r'(\d+)\s*(?:°C|deg|celsius|temperature)', re.IGNORECASE)
        
        # Fault-related keywords
        self.fault_keywords = {
            "bearing": ["bearing", "ball", "race", "cage"],
            "rotor": ["rotor", "bar", "asymmetry"],
            "stator": ["stator", "winding", "coil"],
            "unbalance": ["unbalance", "unbalanced", "mass"],
            "misalignment": ["misalignment", "align", "angular", "parallel"],
            "looseness": ["loose", "looseness", "mount", "bolt"],
            "coupling": ["coupling", "couple", "shaft"]
        }
    
    def process(self, text: str) -> Dict:
        """
        Process text input and extract features
        
        Args:
            text: User-provided text about motor conditions
            
        Returns:
            Dictionary of extracted features
        """
        if not text or not text.strip():
            return {}
        
        features = {}
        
        # Extract numerical parameters
        features["rpm"] = self._extract_rpm(text)
        features["load_percent"] = self._extract_load(text)
        features["temperature"] = self._extract_temperature(text)
        
        # Extract fault-related keywords
        features["fault_keywords"] = self._extract_fault_keywords(text)
        
        # Extract vibration description
        features["vibration_description"] = self._analyze_vibration_description(text)
        
        # Text embeddings (simplified - in production use actual embeddings)
        features["text_length"] = len(text)
        features["word_count"] = len(text.split())
        
        return features
    
    def _extract_rpm(self, text: str) -> Optional[float]:
        """Extract RPM value from text"""
        match = self.rpm_pattern.search(text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_load(self, text: str) -> Optional[float]:
        """Extract load percentage from text"""
        match = self.load_pattern.search(text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_temperature(self, text: str) -> Optional[float]:
        """Extract temperature from text"""
        match = self.temp_pattern.search(text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_fault_keywords(self, text: str) -> Dict[str, int]:
        """Count fault-related keywords in text"""
        text_lower = text.lower()
        keyword_counts = {}
        
        for fault_type, keywords in self.fault_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                keyword_counts[fault_type] = count
        
        return keyword_counts
    
    def _analyze_vibration_description(self, text: str) -> Dict:
        """Analyze vibration-related descriptions"""
        text_lower = text.lower()
        
        vibration_indicators = {
            "high_vibration": any(word in text_lower for word in ["high", "excessive", "severe", "abnormal"]),
            "low_vibration": any(word in text_lower for word in ["low", "minimal", "normal"]),
            "location_bearing": "bearing" in text_lower,
            "location_housing": "housing" in text_lower,
            "location_shaft": "shaft" in text_lower
        }
        
        return vibration_indicators
    
    def normalize_features(self, features: Dict) -> np.ndarray:
        """
        Normalize features for ML model input
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Normalized feature vector
        """
        # Create feature vector
        feature_vector = []
        
        # Numerical features (normalized)
        rpm = features.get("rpm", 1500) / 3000  # Normalize to [0, 1]
        load = features.get("load_percent", 50) / 100  # Normalize to [0, 1]
        temp = features.get("temperature", 50) / 100  # Normalize to [0, 1]
        
        feature_vector.extend([rpm, load, temp])
        
        # Keyword counts (normalized)
        fault_keywords = features.get("fault_keywords", {})
        for fault_type in self.fault_keywords.keys():
            count = fault_keywords.get(fault_type, 0)
            feature_vector.append(min(count / 5, 1.0))  # Cap at 5 occurrences
        
        # Vibration indicators
        vib_desc = features.get("vibration_description", {})
        feature_vector.extend([
            1.0 if vib_desc.get("high_vibration", False) else 0.0,
            1.0 if vib_desc.get("low_vibration", False) else 0.0,
            1.0 if vib_desc.get("location_bearing", False) else 0.0,
            1.0 if vib_desc.get("location_housing", False) else 0.0,
            1.0 if vib_desc.get("location_shaft", False) else 0.0
        ])
        
        return np.array(feature_vector, dtype=np.float32)
