"""Tests for the calibration record API."""
from __future__ import annotations


def _create_instrument(client, sample_instrument_payload) -> int:
    response = client.post("/api/v1/instruments", json=sample_instrument_payload)
    assert response.status_code == 201
    return response.json()["id"]


def test_create_calibration_record(client, sample_instrument_payload):
    instrument_id = _create_instrument(client, sample_instrument_payload)

    payload = {
        "instrument_id": instrument_id,
        "calibration_date": "2026-06-01",
        "performed_by": "田中太郎",
        "reference_standard": "ブロックゲージ 等級0",
        "environmental_conditions": "20.1 degC / 45% RH",
        "measured_value": "25.002 mm",
        "reference_value": "25.000 mm",
        "result": "pass",
        "certificate_number": "CERT-2026-0601",
        "notes": None,
    }
    response = client.post("/api/v1/calibrations", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["instrument_id"] == instrument_id
    assert body["result"] == "pass"


def test_create_calibration_record_updates_last_calibration_date(client, sample_instrument_payload):
    instrument_id = _create_instrument(client, sample_instrument_payload)

    payload = {
        "instrument_id": instrument_id,
        "calibration_date": "2026-06-01",
        "performed_by": "田中太郎",
        "reference_standard": "ブロックゲージ 等級0",
        "environmental_conditions": "20.1 degC / 45% RH",
        "measured_value": "25.002 mm",
        "reference_value": "25.000 mm",
        "result": "pass",
    }
    client.post("/api/v1/calibrations", json=payload)

    instrument = client.get(f"/api/v1/instruments/{instrument_id}").json()
    assert instrument["last_calibration_date"] == "2026-06-01"


def test_create_calibration_record_invalid_result_rejected(client, sample_instrument_payload):
    instrument_id = _create_instrument(client, sample_instrument_payload)

    payload = {
        "instrument_id": instrument_id,
        "calibration_date": "2026-06-01",
        "performed_by": "田中太郎",
        "reference_standard": "ブロックゲージ 等級0",
        "environmental_conditions": "20.1 degC / 45% RH",
        "measured_value": "25.002 mm",
        "reference_value": "25.000 mm",
        "result": "maybe",
    }
    response = client.post("/api/v1/calibrations", json=payload)
    assert response.status_code == 422


def test_create_calibration_record_missing_instrument(client):
    payload = {
        "instrument_id": 9999,
        "calibration_date": "2026-06-01",
        "performed_by": "田中太郎",
        "reference_standard": "ブロックゲージ 等級0",
        "environmental_conditions": "20.1 degC / 45% RH",
        "measured_value": "25.002 mm",
        "reference_value": "25.000 mm",
        "result": "pass",
    }
    response = client.post("/api/v1/calibrations", json=payload)
    assert response.status_code == 404


def test_list_calibration_records(client, sample_instrument_payload):
    instrument_id = _create_instrument(client, sample_instrument_payload)

    for day, result in [("2025-06-01", "pass"), ("2026-06-01", "pass")]:
        payload = {
            "instrument_id": instrument_id,
            "calibration_date": day,
            "performed_by": "田中太郎",
            "reference_standard": "ブロックゲージ 等級0",
            "environmental_conditions": "20.0 degC / 45% RH",
            "measured_value": "25.002 mm",
            "reference_value": "25.000 mm",
            "result": result,
        }
        assert client.post("/api/v1/calibrations", json=payload).status_code == 201

    response = client.get("/api/v1/calibrations", params={"instrument_id": instrument_id})
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 2
    # Newest first.
    assert records[0]["calibration_date"] == "2026-06-01"
