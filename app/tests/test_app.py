import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "KubeMind AI is running" in response.get_data(as_text=True)


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}
