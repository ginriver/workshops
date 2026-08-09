"""Seed the calibration database with a realistic set of instruments.

Usage:
    python3 -m data.seed

Creates 8 instruments across multiple categories and calibration states,
plus a few calibration records. Safe to re-run: it clears existing rows first.
"""
from __future__ import annotations

from datetime import date

from app.database import Base, SessionLocal, engine
from app.models.instrument import Instrument
from app.models.calibration import CalibrationRecord

INSTRUMENTS = [
    dict(
        code="CAL-0001", name="デジタルノギス", model="CD-15APX", serial_number="SN-20240001",
        manufacturer="ミツトヨ", category="length", measurement_range="0-150 mm", resolution="0.01 mm",
        site="京都本社", department="品質保証部", storage_location="計測室 A-1", status="in_use",
        calibration_cycle_days=365, last_calibration_date=date(2025, 6, 1),
    ),
    dict(
        code="CAL-0002", name="マイクロメータ", model="MDC-25PX", serial_number="SN-20240002",
        manufacturer="ミツトヨ", category="length", measurement_range="0-25 mm", resolution="0.001 mm",
        site="京都本社", department="品質保証部", storage_location="計測室 A-2", status="in_use",
        calibration_cycle_days=365, last_calibration_date=date(2026, 1, 15),
    ),
    dict(
        code="CAL-0003", name="圧力計", model="PG-100N", serial_number="SN-20240003",
        manufacturer="長野計器", category="pressure", measurement_range="0-1 MPa", resolution="0.005 MPa",
        site="大阪工場", department="製造部", storage_location="ライン B 工具棚", status="in_use",
        calibration_cycle_days=180, last_calibration_date=date(2025, 12, 1),
    ),
    dict(
        code="CAL-0004", name="標準温度計", model="RTD-PT100", serial_number="SN-20240004",
        manufacturer="横河電機", category="temperature", measurement_range="-50-300 degC", resolution="0.01 degC",
        site="京都本社", department="研究開発部", storage_location="恒温槽室", status="calibrating",
        calibration_cycle_days=365, last_calibration_date=date(2025, 7, 20),
    ),
    dict(
        code="CAL-0005", name="分析天秤", model="APX-220", serial_number="SN-20240005",
        manufacturer="サンプル精密機器", category="mass", measurement_range="0-220 g", resolution="0.01 mg",
        site="京都本社", department="研究開発部", storage_location="天秤室 C-1", status="in_use",
        calibration_cycle_days=365, last_calibration_date=date(2026, 3, 10),
    ),
    dict(
        code="CAL-0006", name="メスフラスコ", model="VF-100", serial_number="SN-20240006",
        manufacturer="柴田科学", category="volume", measurement_range="100 mL", resolution="Class A",
        site="東京ラボ", department="分析センター", storage_location="ガラス器具棚", status="in_use",
        calibration_cycle_days=730, last_calibration_date=date(2024, 9, 5),
    ),
    dict(
        code="CAL-0007", name="デジタルマルチメータ", model="7561A", serial_number="SN-20240007",
        manufacturer="横河電機", category="electrical", measurement_range="0-1000 V", resolution="6.5 digit",
        site="大阪工場", department="設備保全部", storage_location="電気室", status="in_use",
        calibration_cycle_days=365, last_calibration_date=date(2025, 3, 22),
    ),
    dict(
        code="CAL-0008", name="ハイトゲージ", model="QH-300", serial_number="SN-20240008",
        manufacturer="ミツトヨ", category="length", measurement_range="0-300 mm", resolution="0.01 mm",
        site="大阪工場", department="製造部", storage_location="検査室", status="stored",
        calibration_cycle_days=365, last_calibration_date=None,
    ),
]


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing data so the script is idempotent.
        db.query(CalibrationRecord).delete()
        db.query(Instrument).delete()
        db.commit()

        instruments = [Instrument(**data) for data in INSTRUMENTS]
        db.add_all(instruments)
        db.commit()

        # Attach a couple of calibration records to the first instrument.
        first = instruments[0]
        db.add_all(
            [
                CalibrationRecord(
                    instrument_id=first.id,
                    calibration_date=date(2025, 6, 1),
                    performed_by="佐藤花子",
                    reference_standard="ブロックゲージ 等級0",
                    environmental_conditions="20.0 degC / 45% RH",
                    measured_value="25.002 mm",
                    reference_value="25.000 mm",
                    result="pass",
                    certificate_number="CERT-2025-0601",
                ),
                CalibrationRecord(
                    instrument_id=first.id,
                    calibration_date=date(2026, 6, 1),
                    performed_by="佐藤花子",
                    reference_standard="ブロックゲージ 等級0",
                    environmental_conditions="20.1 degC / 46% RH",
                    measured_value="25.001 mm",
                    reference_value="25.000 mm",
                    result="pass",
                    certificate_number="CERT-2026-0601",
                ),
            ]
        )
        db.commit()
        print(f"Seeded {len(instruments)} instruments and 2 calibration records.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
