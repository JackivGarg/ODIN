from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app import STATUS_CODES, app


client = TestClient(app)
MESSAGE = {"recipient": "demo-user", "message": "Hello"}


@pytest.mark.parametrize("codes,status", [
    ([200], "sent"),
    ([201], "sent"),
    ([503, 200], "sent"),
    ([400, 201], "sent"),
    ([500, 503], "failed"),
    ([429, 400], "failed"),
])
def test_status_routing(codes, status):
    with patch("app.choice", side_effect=codes) as sender:
        response = client.post("/send", json=MESSAGE)
    assert response.status_code == codes[-1]
    assert response.json() == {
        "simulation": True,
        "status": status,
        "status_code": codes[-1],
        "attempts": len(codes),
        "history": codes,
    }
    assert sender.call_count == len(codes)
    sender.assert_called_with(STATUS_CODES)


def test_each_request_starts_with_fresh_history():
    with patch("app.choice", side_effect=[500, 503, 201]) as sender:
        first = client.post("/send", json=MESSAGE)
        second = client.post("/send", json=MESSAGE)
    assert first.status_code == 503
    assert first.json()["history"] == [500, 503]
    assert first.json()["attempts"] == 2
    assert second.status_code == 201
    assert second.json()["history"] == [201]
    assert second.json()["attempts"] == 1
    assert sender.call_count == 3


@pytest.mark.parametrize("payload", [
    {"recipient": "", "message": "Hello"},
    {"recipient": "demo-user", "message": "   "},
    {"message": "Hello"},
])
def test_invalid_input_does_not_start_sending(payload):
    with patch("app.choice") as sender:
        response = client.post("/send", json=payload)
    assert response.status_code == 422
    sender.assert_not_called()
