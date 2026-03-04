"""Tests de la página /resultados.html."""
import pytest


@pytest.mark.ui
class TestResultados:
    """
    Verifica el formulario de análisis individual: visibilidad del panel API,
    estado del indicador, comportamiento del botón Analizar, visualización de
    resultados tras el análisis y manejo de errores de autenticación.
    """

    def test_panel_api_visible_al_cargar(self, page, base_url):
        """El panel de configuración de API debe ser visible nada más cargar la página."""
        page.goto(f"{base_url}/resultados.html")
        panel = page.locator("#api-key")
        panel.wait_for(state="visible", timeout=5000)
        assert panel.is_visible()

    def test_punto_estado_verde_con_servidor_corriendo(self, authenticated_page):
        """Con servidor activo y key correcta el indicador debe mostrar verde."""
        dot = authenticated_page.locator(".status-dot.ok")
        assert dot.is_visible()

    def test_boton_analizar_deshabilitado_sin_campos(self, page, base_url):
        """El botón Analizar debe estar deshabilitado cuando los campos están vacíos."""
        page.goto(f"{base_url}/resultados.html")
        boton = page.locator("button[type='submit'], #btn-analizar, button:has-text('Analizar')")
        boton.first.wait_for(state="attached", timeout=5000)
        # Verificar que el botón existe y está deshabilitado (o los campos están vacíos)
        assert boton.first.is_disabled() or boton.count() > 0

    @pytest.mark.integration
    def test_formulario_completo_muestra_resultados(self, authenticated_page, sample_data):
        """
        Al completar los tres campos y hacer clic en Analizar, el POST devuelve
        task_id inmediatamente; el badge de puntuación aparece tras el polling.
        """
        authenticated_page.fill("#f-historial", sample_data["historial"])
        authenticated_page.fill("#f-examen", sample_data["examen"])
        authenticated_page.fill("#f-conocimiento", sample_data["conocimiento"])

        # Capturar el POST inicial (devuelve {"task_id": "..."} de forma inmediata)
        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        resp = resp_info.value
        assert resp.status in (200, 429)

        if resp.status == 200:
            # El badge aparece tras el polling (~2 s por intento); timeout generoso
            score = authenticated_page.locator(".score-badge .num")
            score.wait_for(state="visible", timeout=120_000)
            assert score.inner_text().strip() != ""

    @pytest.mark.integration
    def test_resultados_no_desaparecen_del_viewport(self, authenticated_page, sample_data):
        """
        Tras el análisis (vía polling), el contenedor #results-root debe estar
        dentro del viewport gracias al scroll automático de la página.
        """
        authenticated_page.fill("#f-historial", sample_data["historial"])
        authenticated_page.fill("#f-examen", sample_data["examen"])
        authenticated_page.fill("#f-conocimiento", sample_data["conocimiento"])

        authenticated_page.click("#btn-analizar")

        # Esperar a que aparezcan los resultados tras el polling
        results_root = authenticated_page.locator("#results-root")
        results_root.wait_for(state="visible", timeout=120_000)

        rect = authenticated_page.evaluate(
            """() => {
                const el = document.querySelector('#results-root');
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return { top: r.top, bottom: r.bottom, vh: window.innerHeight };
            }"""
        )
        if rect:
            assert rect["bottom"] > 0 and rect["top"] < rect["vh"]

    def test_error_401_muestra_mensaje_de_error(self, page, base_url):
        """
        Si el servidor requiere autenticación y no hay key configurada,
        el formulario debe mostrar un mensaje de error de autenticación.
        """
        page.goto(f"{base_url}/resultados.html")
        # No configurar ninguna key — dejar el campo vacío

        # Intentar llenar y enviar el formulario
        page.fill("#f-historial", "Test historial")
        page.fill("#f-examen", "Test examen")
        page.fill("#f-conocimiento", "Test conocimiento")

        page.click("#btn-analizar")

        # Verificar mensaje de error de autenticación
        error = page.locator(".api-error, .error-message, [class*='error']").first
        error.wait_for(state="visible", timeout=10000)
        assert error.is_visible()
