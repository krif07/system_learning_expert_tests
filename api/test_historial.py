"""Tests de los endpoints GET /historial y GET /historial/{student_dir}."""
import pytest

HISTORIAL = "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas."
EXAMEN    = "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta."
RECURSOS  = "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento."


class TestHistorial:
    """
    Verifica la lista de estudiantes con sesiones guardadas y el detalle
    de sesiones individuales. El test que requiere analizar primero está
    marcado con @pytest.mark.integration.
    """

    def test_retorna_lista(self, api_client):
        """GET /historial debe devolver 200 con una lista (puede estar vacía)."""
        response = api_client.get("/historial")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_estudiante_inexistente_retorna_404(self, api_client):
        """GET /historial/<dir-inexistente> debe devolver 404."""
        response = api_client.get("/historial/estudiante-que-no-existe-xyz-9999")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_sesiones_de_estudiante_existen_despues_de_analizar(self, api_client):
        """
        Después de analizar a un estudiante con nombre y documento, sus sesiones
        deben aparecer en GET /historial y en GET /historial/{dir}.
        """
        payload = {
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
            "perfil": "dmre",
            "nombre": "IntegracionTest",
            "documento": "INT-001",
        }
        resp_analizar = api_client.post("/analizar", json=payload)
        if resp_analizar.status_code == 429:
            pytest.skip("Rate limit alcanzado")
        assert resp_analizar.status_code == 200

        # Verificar que el estudiante aparece en la lista de historial
        resp_lista = api_client.get("/historial")
        assert resp_lista.status_code == 200
        estudiantes = resp_lista.json()
        dirs = [e["dir"] for e in estudiantes]
        assert any("INT-001" in d or "IntegracionTest" in d for d in dirs), (
            f"Estudiante no encontrado en historial. Dirs disponibles: {dirs}"
        )
