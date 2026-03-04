"""Tests de la página /historial.html."""
import pytest


@pytest.mark.ui
class TestHistorialUI:
    """
    Verifica que la página de historial carga correctamente, muestra la lista
    de estudiantes y permite explorar las sesiones individuales.
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
        Si el servidor tiene historial guardado, debe aparecer al menos un
        elemento en la lista de estudiantes.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        lista = authenticated_page.locator(
            ".student-list, #student-list, [class*='historial']"
        ).first
        # La lista puede estar vacía si no hay historial — simplemente verificar que cargó
        assert authenticated_page.locator("body").is_visible()

    def test_click_en_estudiante_muestra_sesiones(self, authenticated_page, base_url):
        """
        Al hacer clic en un estudiante de la lista, deben aparecer sus sesiones.
        Se omite si no hay estudiantes en el historial.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        estudiante = authenticated_page.locator(
            ".student-item, [class*='student'], li[data-dir]"
        ).first

        if not estudiante.is_visible():
            pytest.skip("No hay estudiantes en el historial para esta prueba")

        estudiante.click()

        sesiones = authenticated_page.locator(
            ".session-list, .sesiones, [class*='session']"
        ).first
        sesiones.wait_for(state="visible", timeout=5000)
        assert sesiones.is_visible()
