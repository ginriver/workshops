"""Pydantic schemas for Instrument resources."""
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InstrumentBase(BaseModel):
    code: str = Field(..., description="機器ID / 管理番号", examples=["CAL-0001"])
    name: str = Field(..., description="名称", examples=["デジタルノギス"])
    model: str = Field(..., description="型式", examples=["SD-150"])
    serial_number: str = Field(..., description="シリアル番号")
    manufacturer: str = Field(..., description="製造元")
    category: str = Field(..., description="カテゴリ")
    measurement_range: str = Field(..., description="測定範囲", examples=["0-150 mm"])
    resolution: str = Field(..., description="分解能", examples=["0.01 mm"])
    site: str = Field(..., description="所属拠点", examples=["京都本社"])
    department: str = Field(..., description="部署")
    storage_location: str = Field(..., description="保管場所")
    status: str = Field("in_use", description="ステータス")
    calibration_cycle_days: int = Field(365, description="校正周期（日）")
    last_calibration_date: Optional[date] = Field(None, description="最終校正日")


class InstrumentCreate(InstrumentBase):
    """Payload for registering a new instrument."""


class InstrumentUpdate(BaseModel):
    """Payload for updating an existing instrument. All fields optional."""

    name: Optional[str] = None
    status: Optional[str] = None
    storage_location: Optional[str] = None
    calibration_cycle_days: Optional[int] = None
    last_calibration_date: Optional[date] = None


class InstrumentRead(InstrumentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
