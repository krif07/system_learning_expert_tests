"""Tests de autenticación con el header X-Api-Key."""
import httpx
import pytest

# Endpoints protegidos que deben requerir autenticación
ENDPOINTS_PROTEGIDOS = [
    ("POST", "/analizar"),
    ("POST", "/analizar/lote"),
    ("GET",  "/historial"),
    ("GET",  "/historial/estudiante-inexistente"),
    ("GET",  "/conocimiento"),
    ("GET",  "/recursos/links"),
]


class TestAutenticacion:
    """
    Verifica que los endpoints protegidos devuelven 401 cuando no se envía
    la API key o se envía una incorrecta, y que retornan un código distinto
    de 401 cuando la key es correcta.
    """

    def test_sin_header_retorna_401(self, client_sin_key):
        """POST /analizar sin X-Api-Key debe devolver 401."""
        response = client_sin_key.post(
            "/analizar",
            json={"historial": "x", "examen": "x", "conocimiento": "x"},
        )
        assert response.status_code == 401

    def test_header_incorrecto_retorna_401(self, client_key_incorrecta):
        """POST /analizar con key incorrecta debe devolver 401."""
        response = client_key_incorrecta.post(
            "/analizar",
            json={"historial": "x", "examen": "x", "conocimiento": "x"},
        )
        assert response.status_code == 401

    def test_header_correcto_retorna_200(self, api_client):
        """GET /historial con key correcta no debe devolver 401."""
        response = api_client.get("/historial")
        assert response.status_code != 401

    @pytest.mark.parametrize("method,endpoint", ENDPOINTS_PROTEGIDOS)
    def test_endpoints_protegidos_parametrizado(self, client_sin_key, method, endpoint):
        """Todos los endpoints protegidos deben devolver 401 sin API key."""
        if method == "GET":
            response = client_sin_key.get(endpoint)
        else:
            response = client_sin_key.post(endpoint, json={})
        assert response.status_code == 401
