"""Shared pytest fixtures: isolated in-memory database + FastAPI TestClient."""
from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    """Provide an isolated in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient wired to the isolated test database."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def sample_instrument_payload() -> dict:
    """A realistic instrument registration payload (digital caliper)."""
    return {
        "code": "CAL-0001",
        "name": "デジタルノギス",
        "model": "SD-150",
        "serial_number": "SN-20240001",
        "manufacturer": "サンプル精密機器",
        "category": "length",
        "measurement_range": "0-150 mm",
        "resolution": "0.01 mm",
        "site": "京都本社",
        "department": "品質保証部",
        "storage_location": "計測室 A-1",
        "status": "in_use",
        "calibration_cycle_days": 365,
        "last_calibration_date": "2025-06-01",
    }
