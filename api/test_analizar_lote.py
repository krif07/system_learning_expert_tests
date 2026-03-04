"""Tests del endpoint POST /analizar/lote."""
import pytest

HISTORIAL = "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas."
EXAMEN    = "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta."
RECURSOS  = "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento."

ESTUDIANTE_VALIDO = {
    "nombre": "Test",
    "documento": "12345",
    "historial": HISTORIAL,
    "examen": EXAMEN,
    "conocimiento": RECURSOS,
    "perfil": "dmre",
}


class TestAnalizarLote:
    """
    Verifica el comportamiento del endpoint POST /analizar/lote, incluyendo
    el límite de 50 estudiantes y la estructura de la respuesta agrupada.
    """

    def test_lote_mayor_50_retorna_400(self, api_client):
        """Un lote con más de 50 estudiantes debe devolver 400."""
        lote = {"estudiantes": [ESTUDIANTE_VALIDO.copy() for _ in range(51)]}
        response = api_client.post("/analizar/lote", json=lote)
        assert response.status_code == 400

    @pytest.mark.integration
    def test_respuesta_contiene_totales(self, api_client):
        """La respuesta debe incluir los campos total, exitosos y fallidos."""
        lote = {"estudiantes": [ESTUDIANTE_VALIDO.copy()]}
        response = api_client.post("/analizar/lote", json=lote)
        assert response.status_code in (200, 429)
        if response.status_code == 200:
            body = response.json()
            assert "total" in body
            assert "exitosos" in body
            assert "fallidos" in body
            assert "resultados" in body

    @pytest.mark.integration
    def test_campo_exitosos_mas_fallidos_igual_total(self, api_client):
        """exitosos + fallidos debe ser igual a total en la respuesta."""
        lote = {"estudiantes": [ESTUDIANTE_VALIDO.copy()]}
        response = api_client.post("/analizar/lote", json=lote)
        if response.status_code == 429:
            pytest.skip("Rate limit alcanzado")
        assert response.status_code == 200
        body = response.json()
        assert body["exitosos"] + body["fallidos"] == body["total"]
