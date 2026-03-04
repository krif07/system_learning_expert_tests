"""Tests del endpoint GET /health."""
import httpx
import pytest


class TestHealth:
    """Verifica que el endpoint /health responde correctamente y es público."""

    def test_retorna_200(self, api_client):
        response = api_client.get("/health")
        assert response.status_code == 200

    def test_body_contiene_status_ok(self, api_client):
        response = api_client.get("/health")
        assert response.json().get("status") == "ok"

    def test_no_requiere_api_key(self, base_url):
        """El endpoint debe responder 200 incluso sin enviar X-Api-Key."""
        with httpx.Client(base_url=base_url, timeout=10) as client:
            response = client.get("/health")
        assert response.status_code == 200
