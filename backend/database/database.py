"""
Database models and initialization for SQLite
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = Path("motor_diagnosis.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()


class DiagnosisRecord(Base):
    """Diagnosis record model"""
    __tablename__ = "diagnosis_records"
    
    id = Column(Integer, primary_key=True, index=True)
    motor_id = Column(String, nullable=True)
    motor_type = Column(String, nullable=True)
    rpm = Column(Float, nullable=True)
    load = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    
    # Input information
    input_type = Column(String)  # "image", "video", "image+text", "video+text", "all"
    image_path = Column(String, nullable=True)
    video_path = Column(String, nullable=True)
    text_input = Column(Text, nullable=True)
    
    # Diagnosis results
    predicted_fault = Column(String)
    confidence = Column(Float)
    severity = Column(String)  # "Low", "Medium", "High"
    severity_score = Column(Float)
    
    # Probability distribution (stored as JSON string)
    probability_distribution = Column(Text)
    
    # Feature information
    important_features = Column(Text, nullable=True)
    
    # Report
    report_path = Column(String, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "motor_id": self.motor_id,
            "motor_type": self.motor_type,
            "rpm": self.rpm,
            "load": self.load,
            "temperature": self.temperature,
            "input_type": self.input_type,
            "image_path": self.image_path,
            "video_path": self.video_path,
            "text_input": self.text_input,
            "predicted_fault": self.predicted_fault,
            "confidence": self.confidence,
            "severity": self.severity,
            "severity_score": self.severity_score,
            "probability_distribution": self.probability_distribution,
            "important_features": self.important_features,
            "report_path": self.report_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class TrainingRecord(Base):
    """Model training record"""
    __tablename__ = "training_records"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
    model_type = Column(String)  # "CNN", "RandomForest", etc.
    dataset_size = Column(Integer)
    
    # Training metrics
    accuracy = Column(Float)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    # Training parameters
    epochs = Column(Integer, nullable=True)
    batch_size = Column(Integer, nullable=True)
    learning_rate = Column(Float, nullable=True)
    
    # Model path
    model_path = Column(String)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
