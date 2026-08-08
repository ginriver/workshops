"""Tests for the instrument management API."""
from __future__ import annotations


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_instrument(client, sample_instrument_payload):
    response = client.post("/api/v1/instruments", json=sample_instrument_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "CAL-0001"
    assert body["category"] == "length"
    assert body["status"] == "in_use"
    assert "id" in body


def test_create_instrument_duplicate_code_rejected(client, sample_instrument_payload):
    client.post("/api/v1/instruments", json=sample_instrument_payload)
    response = client.post("/api/v1/instruments", json=sample_instrument_payload)
    assert response.status_code == 409


def test_create_instrument_invalid_category_rejected(client, sample_instrument_payload):
    payload = dict(sample_instrument_payload, category="humidity")
    response = client.post("/api/v1/instruments", json=payload)
    assert response.status_code == 422


def test_list_instruments_empty(client):
    response = client.get("/api/v1/instruments")
    assert response.status_code == 200
    assert response.json() == []


def test_list_instruments_filter_by_category(client, sample_instrument_payload):
    client.post("/api/v1/instruments", json=sample_instrument_payload)

    pressure = dict(
        sample_instrument_payload,
        code="CAL-0002",
        name="圧力計",
        category="pressure",
        serial_number="SN-20240002",
    )
    client.post("/api/v1/instruments", json=pressure)

    response = client.get("/api/v1/instruments", params={"category": "length"})
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["code"] == "CAL-0001"


def test_get_instrument_not_found(client):
    response = client.get("/api/v1/instruments/9999")
    assert response.status_code == 404


def test_update_instrument_status(client, sample_instrument_payload):
    created = client.post("/api/v1/instruments", json=sample_instrument_payload).json()
    response = client.patch(
        f"/api/v1/instruments/{created['id']}", json={"status": "calibrating"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "calibrating"
