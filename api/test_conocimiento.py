"""Tests del endpoint GET /conocimiento."""
import pytest


class TestConocimiento:
    """
    Verifica el explorador de base de conocimiento filtrable por perfil
    y categoría. No requiere llamadas a Gemini.
    """

    def test_perfil_dmre_retorna_datos(self, api_client):
        """GET /conocimiento?perfil=dmre debe devolver 200 con un dict no vacío."""
        response = api_client.get("/conocimiento", params={"perfil": "dmre"})
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, dict)
        assert len(body) > 0

    def test_perfil_invalido_retorna_404(self, api_client):
        """Un perfil sin base de conocimiento debe devolver 404."""
        response = api_client.get("/conocimiento", params={"perfil": "perfil-inexistente-xyz"})
        assert response.status_code == 404

    def test_filtro_categoria_reduce_resultado(self, api_client):
        """
        El resultado filtrado por categoría debe tener igual o menos claves
        que el resultado sin filtro para el mismo perfil.
        """
        resp_completo = api_client.get("/conocimiento", params={"perfil": "dmre"})
        assert resp_completo.status_code == 200

        resp_filtrado = api_client.get(
            "/conocimiento", params={"perfil": "dmre", "categoria": "ALGEBRA"}
        )
        # 200 si la categoría existe, 404 si no existe — ambos son válidos
        assert resp_filtrado.status_code in (200, 404)

        if resp_filtrado.status_code == 200:
            assert len(resp_filtrado.json()) <= len(resp_completo.json())
