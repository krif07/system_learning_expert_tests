"""Tests del endpoint POST /analizar."""
import pytest

PERFILES_VALIDOS = ["dmre", "secundaria", "primaria", "universitario", "profesional"]

HISTORIAL = "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas."
EXAMEN    = "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta."
RECURSOS  = "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento."


class TestAnalizar:
    """
    Verifica la validación de campos y la estructura de la respuesta del
    endpoint POST /analizar. Los tests que invocan Gemini están marcados
    con @pytest.mark.integration y se excluyen por defecto.
    """

    # ------------------------------------------------------------------
    # Tests de validación — no requieren Gemini
    # ------------------------------------------------------------------

    def test_campos_obligatorios_vacios_retornan_422(self, api_client):
        """Campos requeridos vacíos deben devolver 422."""
        response = api_client.post(
            "/analizar",
            json={"historial": "", "examen": "", "conocimiento": ""},
        )
        assert response.status_code == 422

    def test_perfil_invalido_retorna_422(self, api_client):
        """Un perfil que no existe en la lista válida debe devolver 422."""
        response = api_client.post(
            "/analizar",
            json={
                "historial": HISTORIAL,
                "examen": EXAMEN,
                "conocimiento": RECURSOS,
                "perfil": "perfil_que_no_existe",
            },
        )
        assert response.status_code == 422

    def test_campo_mayor_20000_chars_retorna_422(self, api_client):
        """Un campo con más de 20 000 caracteres debe devolver 422."""
        texto_largo = "a" * 20_001
        response = api_client.post(
            "/analizar",
            json={
                "historial": texto_largo,
                "examen": EXAMEN,
                "conocimiento": RECURSOS,
            },
        )
        assert response.status_code == 422

    @pytest.mark.integration
    def test_campo_exactamente_20000_chars_pasa(self, api_client):
        """Un campo con exactamente 20 000 caracteres debe ser aceptado — POST retorna task_id."""
        texto_limite = "a" * 20_000
        response = api_client.post(
            "/analizar",
            json={"historial": texto_limite, "examen": EXAMEN, "conocimiento": RECURSOS},
        )
        assert response.status_code in (200, 429)
        if response.status_code == 200:
            assert "task_id" in response.json()

    # ------------------------------------------------------------------
    # Tests de estructura de respuesta — requieren Gemini + polling
    # ------------------------------------------------------------------

    @pytest.mark.integration
    def test_respuesta_tiene_estructura_completa(self, analizar_y_esperar):
        """El resultado final debe contener todas las claves del contrato."""
        data = analizar_y_esperar({
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
            "perfil": "dmre",
        })
        assert "diagnostico" in data
        assert "ruta_nivelacion" in data
        assert "metrica_progreso_estimada" in data
        assert "nivel_sugerido" in data
        assert "mensaje_motivador" in data

    @pytest.mark.integration
    def test_respuesta_puntaje_no_es_nulo(self, analizar_y_esperar):
        """El campo puntaje_general del diagnóstico no debe ser nulo ni vacío."""
        data = analizar_y_esperar({
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
        })
        puntaje = data["diagnostico"]["puntaje_general"]
        assert puntaje is not None and puntaje != ""

    @pytest.mark.integration
    def test_respuesta_ruta_nivelacion_es_lista(self, analizar_y_esperar):
        """El campo ruta_nivelacion debe ser una lista."""
        data = analizar_y_esperar({
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
        })
        assert isinstance(data["ruta_nivelacion"], list)

    @pytest.mark.integration
    def test_metrica_es_numero_entre_0_y_100(self, analizar_y_esperar):
        """metrica_progreso_estimada debe ser un número en el rango [0, 100]."""
        data = analizar_y_esperar({
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
        })
        metrica = data["metrica_progreso_estimada"]
        assert isinstance(metrica, (int, float))
        assert 0 <= metrica <= 100

    @pytest.mark.integration
    @pytest.mark.parametrize("perfil", PERFILES_VALIDOS)
    def test_todos_los_perfiles_aceptados(self, api_client, perfil):
        """Cada perfil válido debe ser aceptado — POST retorna 200 con task_id."""
        response = api_client.post("/analizar", json={
            "historial": HISTORIAL,
            "examen": EXAMEN,
            "conocimiento": RECURSOS,
            "perfil": perfil,
        })
        assert response.status_code in (200, 429)
        if response.status_code == 200:
            assert "task_id" in response.json()
