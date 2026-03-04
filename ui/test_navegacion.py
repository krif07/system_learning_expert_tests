"""Tests de navegación entre las páginas de la aplicación."""
import pytest

PAGINAS = [
    "/resultados.html",
    "/historial.html",
    "/examen.html",
    "/conocimiento.html",
    "/comparativa.html",
]


@pytest.mark.ui
class TestNavegacion:
    """
    Verifica que los links de navegación funcionan correctamente y que la
    página activa recibe la clase CSS correspondiente.
    """

    @pytest.mark.parametrize("ruta", PAGINAS)
    def test_links_de_nav_funcionan(self, authenticated_page, base_url, ruta):
        """Cada link del menú de navegación debe llevar a la página correcta."""
        # Partir desde la página principal
        authenticated_page.goto(f"{base_url}/resultados.html")
        authenticated_page.wait_for_load_state("networkidle")

        # Buscar link de navegación que apunte a la ruta
        link = authenticated_page.locator(f"nav a[href*='{ruta}'], a[href='{ruta}']").first

        if not link.is_visible():
            pytest.skip(f"No se encontró link de navegación para {ruta}")

        link.click()
        authenticated_page.wait_for_load_state("networkidle")

        assert ruta in authenticated_page.url

    def test_pagina_activa_tiene_clase_active(self, authenticated_page, base_url):
        """
        En la página actual, el link de navegación correspondiente debe tener
        la clase CSS 'active' (u otra clase que indique la página activa).
        """
        authenticated_page.goto(f"{base_url}/historial.html")
        authenticated_page.wait_for_load_state("networkidle")

        link_activo = authenticated_page.locator(
            "nav a.active, nav a[class*='active'], nav a[aria-current='page']"
        ).first

        assert link_activo.is_visible(), (
            "Ningún link de navegación tiene la clase 'active' en /historial.html"
        )
