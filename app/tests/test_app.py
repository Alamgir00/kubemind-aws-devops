import os
import sys

import pytest


def _find_and_add_app_dir():
    """
    Walk upward from this test file's location looking for app.py, checking
    both the directory itself and a 'src' subdirectory at each level (e.g.
    app/tests/test_app.py alongside app/src/app.py). Adds the directory that
    contains app.py to sys.path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):  # search up to 6 levels up
        direct_candidate = os.path.join(current_dir, "app.py")
        if os.path.isfile(direct_candidate):
            sys.path.insert(0, current_dir)
            return current_dir

        src_candidate = os.path.join(current_dir, "src", "app.py")
        if os.path.isfile(src_candidate):
            sys.path.insert(0, os.path.join(current_dir, "src"))
            return os.path.join(current_dir, "src")

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    return None


_app_dir = _find_and_add_app_dir()
if _app_dir is None:
    raise ImportError(
        "Could not locate app.py by searching upward from "
        f"'{os.path.dirname(os.path.abspath(__file__))}'. "
        "Confirm app.py is committed to the repo and sits in the same "
        "folder as (or an ancestor of) the tests/ directory."
    )

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHomeRoute:
    def test_home_status_code(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_content_type_is_html(self, client):
        response = client.get("/")
        assert "text/html" in response.content_type

    def test_home_contains_calculator_title(self, client):
        response = client.get("/")
        html = response.get_data(as_text=True)
        assert "KubeMind" in html

    def test_home_contains_calculator_buttons(self, client):
        response = client.get("/")
        html = response.get_data(as_text=True)
        # Spot-check a few key buttons/ids exist in the markup
        assert 'id="expression"' in html
        assert 'id="result"' in html
        assert "calculate()" in html
        assert "clearAll()" in html
        assert "deleteLast()" in html

    def test_home_contains_all_digit_buttons(self, client):
        response = client.get("/")
        html = response.get_data(as_text=True)
        for digit in "0123456789":
            assert f"appendValue('{digit}')" in html

    def test_home_contains_all_operators(self, client):
        response = client.get("/")
        html = response.get_data(as_text=True)
        for op in ["+", "-", "*", "/", "%"]:
            assert f"appendValue('{op}')" in html


class TestHealthRoute:
    def test_health_status_code(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_content_type_is_json(self, client):
        response = client.get("/health")
        assert response.content_type == "application/json"

    def test_health_response_body(self, client):
        response = client.get("/health")
        assert response.get_json() == {"status": "healthy"}


class TestInvalidRoutes:
    def test_unknown_route_returns_404(self, client):
        response = client.get("/does-not-exist")
        assert response.status_code == 404

    def test_home_route_rejects_post(self, client):
        response = client.post("/")
        assert response.status_code == 405

    def test_health_route_rejects_post(self, client):
        response = client.post("/health")
        assert response.status_code == 405


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
