"""Tests de la página /historial.html."""
import pytest


@pytest.mark.ui
class TestHistorialUI:
    """
    Verifica que la página de historial carga correctamente, muestra el campo
    de búsqueda con autocompletado (input + datalist) y permite explorar
    sesiones individuales seleccionando un estudiante.
    """

    def test_pagina_carga_sin_errores(self, authenticated_page, base_url):
        """La página /historial.html debe cargar sin errores de JavaScript."""
        errors = []
        authenticated_page.on("pageerror", lambda err: errors.append(err.message))

        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        assert len(errors) == 0, f"Errores de JS al cargar la página: {errors}"

    def test_lista_estudiantes_visible_si_hay_historial(self, authenticated_page, base_url):
        """
        El campo de búsqueda #studentSearch (input con datalist) debe estar
        presente. Si hay historial, el datalist debe tener opciones cargadas.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        search = authenticated_page.locator("#studentSearch")
        search.wait_for(state="visible", timeout=5000)
        assert search.is_visible()

        # Verificar que el datalist existe y está asociado
        datalist = authenticated_page.locator("#studentOptions")
        assert datalist.count() > 0

    def test_click_en_estudiante_muestra_sesiones(self, authenticated_page, base_url):
        """
        Al seleccionar un estudiante del autocompletado (#studentSearch + datalist),
        debe aparecer contenido en #sessionsRoot. Se omite si no hay estudiantes.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        # Obtener la primera opción del datalist
        primera_opcion = authenticated_page.evaluate(
            "() => { const opt = document.querySelector('#studentOptions option'); "
            "return opt ? opt.value : null; }"
        )

        if not primera_opcion:
            pytest.skip("No hay estudiantes en el historial para esta prueba")

        # Escribir el valor exacto en el input para simular la selección
        search = authenticated_page.locator("#studentSearch")
        search.fill(primera_opcion)
        search.dispatch_event("input")
        search.dispatch_event("change")

        sesiones = authenticated_page.locator("#sessionsRoot")
        sesiones.wait_for(state="visible", timeout=5000)
        assert sesiones.inner_text().strip() != ""
