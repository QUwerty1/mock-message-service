import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def payload(token: str = "secret") -> dict[str, str | int]:
    return {"token": token, "body": "Test notification", "mira_id": "student-1", "type": "student"}


def test_message_is_saved(monkeypatch, tmp_path):
    monkeypatch.setenv("MESSAGE_SERVICE_TOKEN", "secret")
    output_file = tmp_path / "messages.jsonl"
    monkeypatch.setenv("MESSAGE_OUTPUT_FILE", str(output_file))
    response = client.post("/", json=payload())
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert json.loads(output_file.read_text(encoding="utf-8")) == payload()


def test_invalid_token_returns_401(monkeypatch):
    monkeypatch.setenv("MESSAGE_SERVICE_TOKEN", "secret")
    monkeypatch.delenv("MESSAGE_OUTPUT_FILE", raising=False)
    assert client.post("/", json=payload("wrong")).status_code == 401


def test_incomplete_payload_returns_422(monkeypatch):
    monkeypatch.setenv("MESSAGE_SERVICE_TOKEN", "secret")
    assert client.post("/", json={"token": "secret"}).status_code == 422
