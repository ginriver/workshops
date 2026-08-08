"""CalibrationRecord (校正記録) ORM model.

Stores the outcome of a single calibration event for an instrument,
including the reference standard, environmental conditions, measured
values and pass/fail judgment.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Judgment results for a calibration (合否判定).
CALIBRATION_RESULTS = ("pass", "fail")


class CalibrationRecord(Base):
    __tablename__ = "calibration_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    instrument_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False, index=True
    )

    calibration_date: Mapped[date] = mapped_column(Date, nullable=False)      # 校正実施日
    performed_by: Mapped[str] = mapped_column(String(64), nullable=False)      # 校正実施者
    reference_standard: Mapped[str] = mapped_column(String(128), nullable=False)  # 基準器情報

    # 環境条件（温度・湿度など）。例: "20.1 degC / 45% RH"
    environmental_conditions: Mapped[str] = mapped_column(String(128), nullable=False)

    measured_value: Mapped[str] = mapped_column(String(128), nullable=False)   # 測定値（表示値）
    reference_value: Mapped[str] = mapped_column(String(128), nullable=False)  # 基準値（標準値）

    result: Mapped[str] = mapped_column(String(16), nullable=False)            # 合否判定

    certificate_number: Mapped[str] = mapped_column(String(64), nullable=True)  # 校正証明書番号
    notes: Mapped[str] = mapped_column(Text, nullable=True)                     # 備考

    instrument = relationship("Instrument", back_populates="calibration_records")

    def __repr__(self) -> str:
        return f"<CalibrationRecord instrument_id={self.instrument_id} date={self.calibration_date} result={self.result}>"
