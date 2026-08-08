"""Service-layer business logic for instruments."""
from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.instrument import Instrument, INSTRUMENT_CATEGORIES, INSTRUMENT_STATUSES
from app.schemas.instrument import InstrumentCreate, InstrumentUpdate


def _validate_category(category: str) -> None:
    if category not in INSTRUMENT_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid category '{category}'. Must be one of: {INSTRUMENT_CATEGORIES}",
        )


def _validate_status(status: str) -> None:
    if status not in INSTRUMENT_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status '{status}'. Must be one of: {INSTRUMENT_STATUSES}",
        )


def create_instrument(db: Session, payload: InstrumentCreate) -> Instrument:
    _validate_category(payload.category)
    _validate_status(payload.status)

    existing = db.query(Instrument).filter(Instrument.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Instrument code '{payload.code}' already exists")

    instrument = Instrument(**payload.model_dump())
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument


def list_instruments(
    db: Session,
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Instrument]:
    query = db.query(Instrument)
    if category:
        query = query.filter(Instrument.category == category)
    if status:
        query = query.filter(Instrument.status == status)
    return query.order_by(Instrument.code).all()


def get_instrument(db: Session, instrument_id: int) -> Instrument:
    instrument = db.get(Instrument, instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Instrument id={instrument_id} not found")
    return instrument


def update_instrument(db: Session, instrument_id: int, payload: InstrumentUpdate) -> Instrument:
    instrument = get_instrument(db, instrument_id)
    updates = payload.model_dump(exclude_unset=True)

    if "status" in updates:
        _validate_status(updates["status"])

    for field, value in updates.items():
        setattr(instrument, field, value)

    db.commit()
    db.refresh(instrument)
    return instrument


def next_calibration_date(instrument: Instrument) -> Optional[date]:
    """Compute the next calibration due date from the last calibration date
    plus the calibration cycle. Returns None if the instrument has never
    been calibrated."""
    if instrument.last_calibration_date is None:
        return None
    return instrument.last_calibration_date + timedelta(days=instrument.calibration_cycle_days)
