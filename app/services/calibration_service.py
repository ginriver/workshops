"""Service-layer business logic for calibration records."""
from __future__ import annotations

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.calibration import CalibrationRecord, CALIBRATION_RESULTS
from app.models.instrument import Instrument
from app.schemas.calibration import CalibrationRecordCreate


def create_calibration_record(db: Session, payload: CalibrationRecordCreate) -> CalibrationRecord:
    instrument = db.get(Instrument, payload.instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Instrument id={payload.instrument_id} not found")

    if payload.result not in CALIBRATION_RESULTS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid result '{payload.result}'. Must be one of: {CALIBRATION_RESULTS}",
        )

    record = CalibrationRecord(**payload.model_dump())
    db.add(record)

    # Advance the instrument's last calibration date when this record is newer.
    if (
        instrument.last_calibration_date is None
        or payload.calibration_date >= instrument.last_calibration_date
    ):
        instrument.last_calibration_date = payload.calibration_date

    db.commit()
    db.refresh(record)
    return record


def list_calibration_records(db: Session, instrument_id: int) -> List[CalibrationRecord]:
    instrument = db.get(Instrument, instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Instrument id={instrument_id} not found")

    return (
        db.query(CalibrationRecord)
        .filter(CalibrationRecord.instrument_id == instrument_id)
        .order_by(CalibrationRecord.calibration_date.desc())
        .all()
    )
