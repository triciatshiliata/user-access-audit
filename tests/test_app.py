"""Tests for the web routes, using Flask's built-in test client (no browser needed)."""

from pathlib import Path

import pytest

from app import app

DATA = Path(__file__).parent.parent / "sample_data"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"User Access Audit" in response.data


def test_upload_returns_a_report(client):
    with open(DATA / "users.csv", "rb") as users, open(DATA / "hr_roster.csv", "rb") as roster:
        response = client.post("/api/audit", data={"users": users, "roster": roster})
    assert response.status_code == 200
    assert response.get_json()["total_accounts"] == 20


def test_upload_needs_both_files(client):
    with open(DATA / "users.csv", "rb") as users:
        response = client.post("/api/audit", data={"users": users})
    assert response.status_code == 400
    assert "both" in response.get_json()["error"]


def test_upload_rejects_wrong_columns(client):
    # Uploading the roster in BOTH slots: it has no status/is_admin columns
    with open(DATA / "hr_roster.csv", "rb") as a, open(DATA / "hr_roster.csv", "rb") as b:
        response = client.post("/api/audit", data={"users": a, "roster": b})
    assert response.status_code == 400


def test_sample_route(client):
    response = client.get("/api/sample")
    assert response.status_code == 200
    assert response.get_json()["total_accounts"] == 20
