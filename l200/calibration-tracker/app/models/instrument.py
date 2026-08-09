"""Instrument (機器) ORM model.

Represents a single measuring instrument under calibration management,
e.g. calipers, micrometers, pressure gauges, thermometers, balances.
"""
from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Instrument categories defined in the PRD (計量器カテゴリ).
INSTRUMENT_CATEGORIES = ("length", "mass", "temperature", "pressure", "electrical", "volume")

# Lifecycle statuses for an instrument (機器ステータス).
INSTRUMENT_STATUSES = ("in_use", "calibrating", "stored", "discarded")


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 機器ID / 管理番号 (unique human-readable code, e.g. "CAL-0001")
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(128), nullable=False)          # 名称
    model: Mapped[str] = mapped_column(String(128), nullable=False)          # 型式
    serial_number: Mapped[str] = mapped_column(String(64), nullable=False)   # シリアル番号
    manufacturer: Mapped[str] = mapped_column(String(128), nullable=False)   # 製造元

    category: Mapped[str] = mapped_column(String(32), nullable=False)        # カテゴリ
    measurement_range: Mapped[str] = mapped_column(String(64), nullable=False)  # 測定範囲
    resolution: Mapped[str] = mapped_column(String(64), nullable=False)      # 分解能

    site: Mapped[str] = mapped_column(String(64), nullable=False)            # 所属拠点
    department: Mapped[str] = mapped_column(String(64), nullable=False)      # 部署
    storage_location: Mapped[str] = mapped_column(String(128), nullable=False)  # 保管場所

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="in_use")

    # 校正周期（日）と最終校正日。次回校正日は service 層で算出する。
    calibration_cycle_days: Mapped[int] = mapped_column(Integer, nullable=False, default=365)
    last_calibration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    calibration_records = relationship(
        "CalibrationRecord",
        back_populates="instrument",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Instrument code={self.code!r} name={self.name!r} status={self.status!r}>"
