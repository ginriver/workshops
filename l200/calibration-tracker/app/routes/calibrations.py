"""API routes for calibration records."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.calibration import CalibrationRecordCreate, CalibrationRecordRead
from app.services import calibration_service

router = APIRouter(prefix="/calibrations", tags=["calibrations"])


@router.post("", response_model=CalibrationRecordRead, status_code=201)
def create_calibration_record(payload: CalibrationRecordCreate, db: Session = Depends(get_db)):
    return calibration_service.create_calibration_record(db, payload)


@router.get("", response_model=List[CalibrationRecordRead])
def list_calibration_records(instrument_id: int, db: Session = Depends(get_db)):
    return calibration_service.list_calibration_records(db, instrument_id)
