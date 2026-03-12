from fastapi.testclient import TestClient

from app.main import app


def test_search_endpoint_returns_comprehensive_payload() -> None:
    client = TestClient(app)
    payload = {
        "case_name": "Integration Test Case",
        "description": "test",
        "identifiers": [{"input_type": "username", "value": "janedoe"}],
    }

    res = client.post("/api/v1/search", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert "case_id" in body
    assert body["profiles"]
    assert body["findings"]
    assert body["geo_signals"]
    assert body["relationships"]


def test_dashboard_summary_endpoint() -> None:
    client = TestClient(app)
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    assert "active_cases" in res.json()
