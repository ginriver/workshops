"""API routes for instrument management."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.instrument import InstrumentCreate, InstrumentUpdate, InstrumentRead
from app.services import instrument_service

router = APIRouter(prefix="/instruments", tags=["instruments"])


@router.post("", response_model=InstrumentRead, status_code=201)
def create_instrument(payload: InstrumentCreate, db: Session = Depends(get_db)):
    return instrument_service.create_instrument(db, payload)


@router.get("", response_model=List[InstrumentRead])
def list_instruments(
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return instrument_service.list_instruments(db, category=category, status=status)


@router.get("/{instrument_id}", response_model=InstrumentRead)
def get_instrument(instrument_id: int, db: Session = Depends(get_db)):
    return instrument_service.get_instrument(db, instrument_id)


@router.patch("/{instrument_id}", response_model=InstrumentRead)
def update_instrument(instrument_id: int, payload: InstrumentUpdate, db: Session = Depends(get_db)):
    return instrument_service.update_instrument(db, instrument_id, payload)
