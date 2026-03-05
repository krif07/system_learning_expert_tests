"""Tests del endpoint GET /estadisticas."""
import pytest

PERFILES_VALIDOS = ["dmre", "secundaria", "primaria", "universitario", "profesional"]


class TestEstadisticas:
    """
    Verifica el endpoint GET /estadisticas?perfil=... que devuelve estadísticas
    grupales usadas por el panel comparativo de comparativa.html.
    """

    def test_perfil_dmre_retorna_200(self, api_client):
        """GET /estadisticas?perfil=dmre debe devolver 200."""
        response = api_client.get("/estadisticas", params={"perfil": "dmre"})
        assert response.status_code == 200

    def test_respuesta_es_dict(self, api_client):
        """La respuesta debe ser un objeto JSON (dict)."""
        response = api_client.get("/estadisticas", params={"perfil": "dmre"})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_perfil_invalido_retorna_error(self, api_client):
        """Un perfil fuera del enum válido debe devolver 422 (validación de FastAPI)."""
        response = api_client.get("/estadisticas", params={"perfil": "perfil-inexistente-xyz"})
        assert response.status_code == 422

    def test_sin_perfil_usa_default_o_retorna_error(self, api_client):
        """Sin parámetro perfil debe devolver 200 (default) o 422 (requerido)."""
        response = api_client.get("/estadisticas")
        assert response.status_code in (200, 422)

    @pytest.mark.parametrize("perfil", PERFILES_VALIDOS)
    def test_perfiles_validos_retornan_200_o_404(self, api_client, perfil):
        """Cada perfil válido retorna 200 si tiene datos o 404 si no tiene historial."""
        response = api_client.get("/estadisticas", params={"perfil": perfil})
        assert response.status_code in (200, 404)
