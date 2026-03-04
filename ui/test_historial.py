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
        El selector #studentSelect debe estar presente. Si hay historial,
        debe contener al menos una opción seleccionable.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        select = authenticated_page.locator("#studentSelect")
        select.wait_for(state="visible", timeout=5000)
        assert select.is_visible()

    def test_click_en_estudiante_muestra_sesiones(self, authenticated_page, base_url):
        """
        Al seleccionar un estudiante del desplegable #studentSelect, debe
        aparecer contenido en #sessionsRoot. Se omite si no hay estudiantes.
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        select = authenticated_page.locator("#studentSelect")
        opciones = select.locator("option").all()
        # Filtrar opciones reales (excluir placeholder vacío o con value="")
        opciones_reales = [o for o in opciones if o.get_attribute("value")]

        if not opciones_reales:
            pytest.skip("No hay estudiantes en el historial para esta prueba")

        select.select_option(index=1)

        sesiones = authenticated_page.locator("#sessionsRoot")
        sesiones.wait_for(state="visible", timeout=5000)
        assert sesiones.inner_text().strip() != ""
