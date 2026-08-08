"""Pydantic schemas for CalibrationRecord resources."""
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CalibrationRecordBase(BaseModel):
    calibration_date: date = Field(..., description="校正実施日")
    performed_by: str = Field(..., description="校正実施者")
    reference_standard: str = Field(..., description="基準器情報")
    environmental_conditions: str = Field(..., description="環境条件", examples=["20.1 degC / 45% RH"])
    measured_value: str = Field(..., description="測定値（表示値）")
    reference_value: str = Field(..., description="基準値（標準値）")
    result: str = Field(..., description="合否判定", examples=["pass"])
    certificate_number: Optional[str] = Field(None, description="校正証明書番号")
    notes: Optional[str] = Field(None, description="備考")


class CalibrationRecordCreate(CalibrationRecordBase):
    """Payload for registering a new calibration record."""

    instrument_id: int = Field(..., description="対象機器の DB id")


class CalibrationRecordRead(CalibrationRecordBase):
    id: int
    instrument_id: int

    model_config = ConfigDict(from_attributes=True)
