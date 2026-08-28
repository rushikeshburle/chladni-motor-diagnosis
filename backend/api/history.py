"""
History API endpoints for retrieving past diagnosis records
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.database.database import get_db, DiagnosisRecord

history_router = APIRouter()


@history_router.get("/")
async def get_history(
    limit: int = 50,
    offset: int = 0,
    fault_type: Optional[str] = None
):
    """
    Retrieve diagnosis history with optional filtering
    """
    try:
        db = next(get_db())
        
        query = db.query(DiagnosisRecord)
        
        if fault_type:
            query = query.filter(DiagnosisRecord.predicted_fault == fault_type)
        
        records = query.order_by(DiagnosisRecord.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "success": True,
            "count": len(records),
            "records": [record.to_dict() for record in records]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@history_router.get("/{record_id}")
async def get_record(record_id: int):
    """
    Retrieve a specific diagnosis record by ID
    """
    try:
        db = next(get_db())
        record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == record_id).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "record": record.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve record: {str(e)}")


@history_router.delete("/{record_id}")
async def delete_record(record_id: int):
    """
    Delete a specific diagnosis record
    """
    try:
        db = next(get_db())
        record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == record_id).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Delete associated files if they exist
        from pathlib import Path
        if record.image_path:
            image_file = Path(record.image_path)
            if image_file.exists():
                image_file.unlink()
        
        if record.video_path:
            video_file = Path(record.video_path)
            if video_file.exists():
                video_file.unlink()
        
        if record.report_path:
            report_file = Path(record.report_path)
            if report_file.exists():
                report_file.unlink()
        
        db.delete(record)
        db.commit()
        
        return {"success": True, "message": "Record deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete record: {str(e)}")


@history_router.get("/stats/summary")
async def get_statistics():
    """
    Get summary statistics of diagnosis history
    """
    try:
        db = next(get_db())
        
        total_records = db.query(DiagnosisRecord).count()
        
        # Count by fault type
        fault_counts = {}
        for record in db.query(DiagnosisRecord.predicted_fault).all():
            fault = record[0]
            fault_counts[fault] = fault_counts.get(fault, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for record in db.query(DiagnosisRecord.severity).all():
            severity = record[0]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Count by input type
        input_type_counts = {}
        for record in db.query(DiagnosisRecord.input_type).all():
            input_type = record[0]
            input_type_counts[input_type] = input_type_counts.get(input_type, 0) + 1
        
        return {
            "success": True,
            "total_records": total_records,
            "fault_distribution": fault_counts,
            "severity_distribution": severity_counts,
            "input_type_distribution": input_type_counts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")
