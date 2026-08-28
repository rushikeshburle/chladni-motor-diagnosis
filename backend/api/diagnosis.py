"""
Diagnosis API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import random

from backend.models.image_model import ImageModel
from backend.models.video_model import VideoModel
from backend.models.text_model import TextModel
from backend.models.fusion_model import FusionModel
from backend.preprocessing.image_processing import ImageProcessor
from backend.preprocessing.video_processing import VideoProcessor
from backend.preprocessing.text_processing import TextProcessor
from backend.features.pattern_features import PatternFeatureExtractor
from backend.features.visual_features import VisualFeatureExtractor
from backend.features.temporal_features import TemporalFeatureExtractor
from backend.explainability.gradcam import GradCAMGenerator
from backend.database.database import get_db, DiagnosisRecord
from backend.reports.report_generator import ReportGenerator

diagnosis_router = APIRouter()

# Fault classes
FAULT_CLASSES = [
    "Healthy",
    "Rotor Unbalance",
    "Shaft Misalignment",
    "Bearing Fault",
    "Rotor Fault",
    "Stator Fault",
    "Mechanical Looseness",
    "Coupling Fault"
]


class DiagnosisRequest(BaseModel):
    """Diagnosis request model"""
    motor_id: Optional[str] = None
    motor_type: Optional[str] = None
    rpm: Optional[float] = None
    load: Optional[float] = None
    temperature: Optional[float] = None
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    text_input: Optional[str] = None
    demo_mode: bool = False


class DiagnosisResponse(BaseModel):
    """Diagnosis response model"""
    success: bool
    predicted_fault: str
    confidence: float
    severity: str
    severity_score: float
    probability_distribution: Dict[str, float]
    important_features: List[Dict[str, str]]
    input_type: str
    demo_mode: bool
    processing_steps: List[str]
    heatmap_path: Optional[str] = None
    report_path: Optional[str] = None
    error: Optional[str] = None


@diagnosis_router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_diagnosis(request: DiagnosisRequest):
    """
    Perform motor fault diagnosis using multimodal inputs
    """
    try:
        processing_steps = []
        
        # Determine input type
        input_modalities = []
        if request.image_path:
            input_modalities.append("image")
        if request.video_path:
            input_modalities.append("video")
        if request.text_input:
            input_modalities.append("text")
        
        input_type = "+".join(input_modalities) if input_modalities else "none"
        processing_steps.append(f"Input validation - Type: {input_type}")
        
        # Demo mode - simplified for reliability
        if request.demo_mode:
            processing_steps.append("Demo mode activated - generating demonstration prediction")
            prediction = generate_demo_prediction(
                input_type=input_type,
                text_input=request.text_input
            )
            processing_steps.append("Fault classification complete")
            
            # Severity assessment
            severity = assess_severity(prediction["confidence"], prediction["predicted_fault"])
            processing_steps.append("Severity assessment complete")
            
            # Feature importance
            important_features = get_demo_feature_importance(prediction["predicted_fault"])
            processing_steps.append("Feature importance analysis complete")
            
            # Skip heatmap and report generation in demo mode for speed
            heatmap_path = None
            report_path = None
            processing_steps.append("Demo mode - skipping heatmap and report generation")
            
            processing_steps.append("Diagnosis complete")
            
            return DiagnosisResponse(
                success=True,
                predicted_fault=prediction["predicted_fault"],
                confidence=prediction["confidence"],
                severity=severity["level"],
                severity_score=severity["score"],
                probability_distribution=prediction["probability_distribution"],
                important_features=important_features,
                input_type=input_type,
                demo_mode=True,
                processing_steps=processing_steps,
                heatmap_path=heatmap_path,
                report_path=report_path
            )
        
        # Production mode with actual processing
        processing_steps.append("Initializing processors")
        image_processor = ImageProcessor()
        video_processor = VideoProcessor()
        text_processor = TextProcessor()
        pattern_extractor = PatternFeatureExtractor()
        visual_extractor = VisualFeatureExtractor()
        temporal_extractor = TemporalFeatureExtractor()
        
        # Extract features from each modality
        image_features = None
        video_features = None
        text_features = None
        
        if request.image_path:
            processing_steps.append("Image preprocessing started")
            try:
                processed_image = image_processor.process(request.image_path)
                processing_steps.append("Pattern extraction started")
                pattern_features = pattern_extractor.extract(processed_image)
                visual_features = visual_extractor.extract(processed_image)
                image_features = {**pattern_features, **visual_features}
                processing_steps.append("Image features extracted")
            except Exception as e:
                processing_steps.append(f"Image processing warning: {str(e)}")
                image_features = None
        
        if request.video_path:
            processing_steps.append("Video preprocessing started")
            try:
                frames = video_processor.extract_frames(request.video_path)
                processed_frames = [video_processor.process_frame(frame) for frame in frames]
                temporal_features = temporal_extractor.extract(processed_frames)
                video_features = temporal_features
                processing_steps.append("Video features extracted")
            except Exception as e:
                processing_steps.append(f"Video processing warning: {str(e)}")
                video_features = None
        
        if request.text_input:
            processing_steps.append("Text processing started")
            text_features = text_processor.process(request.text_input)
            processing_steps.append("Text features extracted")
        
        # Multimodal fusion
        processing_steps.append("Multimodal feature fusion")
        fusion_model = FusionModel()
        fused_features = fusion_model.fuse(
            image_features=image_features,
            video_features=video_features,
            text_features=text_features
        )
        
        # Fault classification
        processing_steps.append("Fault classification")
        prediction = fusion_model.classify(fused_features)
        
        # Severity assessment
        processing_steps.append("Severity assessment")
        severity = assess_severity(prediction["confidence"], prediction["predicted_fault"])
        
        # Feature importance
        processing_steps.append("Feature importance analysis")
        important_features = get_feature_importance(
            image_features=image_features,
            video_features=video_features,
            text_features=text_features,
            prediction=prediction
        )
        
        # Generate heatmap if image provided
        heatmap_path = None
        if request.image_path:
            processing_steps.append("Generating explainability heatmap")
            try:
                gradcam = GradCAMGenerator()
                heatmap_path = gradcam.generate(request.image_path, prediction["predicted_fault"])
            except Exception as e:
                processing_steps.append(f"Heatmap generation warning: {str(e)}")
        
        # Generate report
        processing_steps.append("Report generation")
        try:
            report_generator = ReportGenerator()
            report_path = report_generator.generate(
                motor_id=request.motor_id,
                motor_type=request.motor_type,
                rpm=request.rpm,
                load=request.load,
                temperature=request.temperature,
                input_type=input_type,
                image_path=request.image_path,
                video_path=request.video_path,
                text_input=request.text_input,
                predicted_fault=prediction["predicted_fault"],
                confidence=prediction["confidence"],
                severity=severity["level"],
                severity_score=severity["score"],
                probability_distribution=prediction["probability_distribution"],
                important_features=important_features,
                heatmap_path=heatmap_path
            )
        except Exception as e:
            processing_steps.append(f"Report generation warning: {str(e)}")
            report_path = None
        
        # Save to database
        try:
            db = next(get_db())
            record = DiagnosisRecord(
                motor_id=request.motor_id,
                motor_type=request.motor_type,
                rpm=request.rpm,
                load=request.load,
                temperature=request.temperature,
                input_type=input_type,
                image_path=request.image_path,
                video_path=request.video_path,
                text_input=request.text_input,
                predicted_fault=prediction["predicted_fault"],
                confidence=prediction["confidence"],
                severity=severity["level"],
                severity_score=severity["score"],
                probability_distribution=json.dumps(prediction["probability_distribution"]),
                important_features=json.dumps(important_features),
                report_path=report_path
            )
            db.add(record)
            db.commit()
            db.refresh(record)
        except Exception as e:
            processing_steps.append(f"Database save warning: {str(e)}")
        
        processing_steps.append("Diagnosis complete")
        
        return DiagnosisResponse(
            success=True,
            predicted_fault=prediction["predicted_fault"],
            confidence=prediction["confidence"],
            severity=severity["level"],
            severity_score=severity["score"],
            probability_distribution=prediction["probability_distribution"],
            important_features=important_features,
            input_type=input_type,
            demo_mode=request.demo_mode,
            processing_steps=processing_steps,
            heatmap_path=heatmap_path,
            report_path=report_path
        )
        
    except Exception as e:
        return DiagnosisResponse(
            success=False,
            predicted_fault="Unknown",
            confidence=0.0,
            severity="Unknown",
            severity_score=0.0,
            probability_distribution={fault: 0.0 for fault in FAULT_CLASSES},
            important_features=[],
            input_type=input_type if 'input_type' in locals() else "unknown",
            demo_mode=request.demo_mode,
            processing_steps=processing_steps if 'processing_steps' in locals() else [],
            error=str(e)
        )


def generate_demo_prediction(input_type: str, text_input: str = None) -> dict:
    """Generate demonstration prediction for demo mode"""
    # Generate reasonable demonstration probabilities
    # Bias towards specific faults based on input characteristics
    probabilities = {fault: random.uniform(0.01, 0.1) for fault in FAULT_CLASSES}
    
    # If text mentions bearing, bias towards bearing fault
    if text_input and "bearing" in text_input.lower():
        probabilities["Bearing Fault"] = random.uniform(0.7, 0.9)
    elif text_input and "unbalance" in text_input.lower():
        probabilities["Rotor Unbalance"] = random.uniform(0.7, 0.9)
    elif text_input and "misalignment" in text_input.lower():
        probabilities["Shaft Misalignment"] = random.uniform(0.7, 0.9)
    elif text_input and "vibration" in text_input.lower():
        # Randomly select a fault when vibration is mentioned
        primary_fault = random.choice(FAULT_CLASSES[1:])  # Exclude healthy
        probabilities[primary_fault] = random.uniform(0.6, 0.85)
    else:
        # Randomly select a fault to be primary
        primary_fault = random.choice(FAULT_CLASSES[1:])  # Exclude healthy
        probabilities[primary_fault] = random.uniform(0.6, 0.85)
    
    # Normalize probabilities
    total = sum(probabilities.values())
    probabilities = {k: v/total for k, v in probabilities.items()}
    
    predicted_fault = max(probabilities, key=probabilities.get)
    confidence = probabilities[predicted_fault]
    
    return {
        "predicted_fault": predicted_fault,
        "confidence": confidence,
        "probability_distribution": probabilities
    }


def get_demo_feature_importance(predicted_fault: str) -> list:
    """Get demo feature importance for explainability"""
    importance = [
        {
            "feature": "Nodal-line density",
            "contribution": "High",
            "value": "0.75"
        },
        {
            "feature": "Pattern irregularity",
            "contribution": "High",
            "value": "0.68"
        },
        {
            "feature": "Edge density",
            "contribution": "Medium",
            "value": "0.45"
        },
        {
            "feature": "Symmetry index",
            "contribution": "Medium",
            "value": "0.52"
        },
        {
            "feature": "Spatial distribution",
            "contribution": "Low",
            "value": "0.33"
        }
    ]
    
    # Adjust based on predicted fault
    if predicted_fault == "Bearing Fault":
        importance[0]["feature"] = "High-frequency components"
        importance[1]["feature"] = "Bearing region intensity"
    elif predicted_fault == "Rotor Unbalance":
        importance[0]["feature"] = "Rotational symmetry deviation"
        importance[1]["feature"] = "Mass distribution pattern"
    elif predicted_fault == "Shaft Misalignment":
        importance[0]["feature"] = "Angular pattern distortion"
        importance[1]["feature"] = "Alignment deviation index"
    
    return importance


def assess_severity(confidence: float, fault_type: str) -> dict:
    """Assess severity based on confidence and fault type"""
    if fault_type == "Healthy":
        return {"level": "Low", "score": 10}
    
    # High confidence faults are more severe
    if confidence > 0.8:
        score = random.uniform(75, 95)
        level = "High"
    elif confidence > 0.6:
        score = random.uniform(50, 75)
        level = "Medium"
    else:
        score = random.uniform(25, 50)
        level = "Low"
    
    return {"level": level, "score": score}


def get_feature_importance(image_features: dict, video_features: dict, 
                          text_features: dict, prediction: dict) -> list:
    """Get feature importance for explainability"""
    importance = []
    
    if image_features:
        importance.append({
            "feature": "Nodal-line density",
            "contribution": "High",
            "value": str(image_features.get("nodal_density", "N/A"))
        })
        importance.append({
            "feature": "Pattern irregularity",
            "contribution": "High",
            "value": str(image_features.get("irregularity", "N/A"))
        })
        importance.append({
            "feature": "Edge density",
            "contribution": "Medium",
            "value": str(image_features.get("edge_density", "N/A"))
        })
    
    if video_features:
        importance.append({
            "feature": "Temporal variation",
            "contribution": "High",
            "value": str(video_features.get("temporal_variation", "N/A"))
        })
    
    if text_features:
        importance.append({
            "feature": "Operating condition",
            "contribution": "Medium",
            "value": "Analyzed"
        })
    
    return importance[:5]  # Return top 5 features
