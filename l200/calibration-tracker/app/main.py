"""Calibration Tracker — FastAPI application entry point.

計量校正管理システム（Calibration Tracker）
Baseline scope: instrument master management + calibration records.
Calibration alerts and measurement-uncertainty evaluation are planned
features (see prd/校正管理システム_要件定義書.md) and are intentionally
NOT implemented in this starter repository.
"""
from __future__ import annotations

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import calibrations_router, instruments_router

# Create tables on startup (fine for the SQLite-based POC).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Calibration Tracker",
    description="計量校正管理システム — 校正スケジュール・校正記録・トレーサビリティ管理",
    version="0.1.0",
)

app.include_router(instruments_router, prefix="/api/v1")
app.include_router(calibrations_router, prefix="/api/v1")


@app.get("/healthz", tags=["health"])
def healthz():
    """Liveness probe used by the workshop runbook."""
    return {"status": "ok"}
