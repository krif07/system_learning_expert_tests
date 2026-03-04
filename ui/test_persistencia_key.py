"""Tests de persistencia de la API key en localStorage."""
import pytest

KEY_DE_PRUEBA = "clave-de-prueba-persistencia-12345"


@pytest.mark.ui
class TestPersistenciaKey:
    """
    Verifica que la API key se persiste correctamente en localStorage entre
    páginas y que el header X-Api-Key sólo se envía cuando la key no está vacía.
    """

    def test_key_persiste_entre_paginas(self, page, base_url):
        """
        La key escrita en /resultados.html debe seguir presente al navegar
        a /historial.html (misma sesión, mismo localStorage).
        """
        page.goto(f"{base_url}/resultados.html")
        campo = page.locator("#api-key")
        campo.wait_for(state="visible", timeout=5000)
        campo.fill(KEY_DE_PRUEBA)
        campo.dispatch_event("input")
        campo.dispatch_event("change")

        # Navegar a otra página
        page.goto(f"{base_url}/historial.html")
        campo_historial = page.locator("#api-key")
        campo_historial.wait_for(state="visible", timeout=5000)

        valor = campo_historial.input_value()
        assert valor == KEY_DE_PRUEBA, (
            f"La key no persistió entre páginas. Esperado: '{KEY_DE_PRUEBA}', "
            f"encontrado: '{valor}'"
        )

    def test_key_se_guarda_en_localstorage(self, page, base_url):
        """
        Al escribir una key en el campo #api-key, debe quedar guardada en
        localStorage bajo la clave 'api_key'.
        """
        page.goto(f"{base_url}/resultados.html")
        campo = page.locator("#api-key")
        campo.wait_for(state="visible", timeout=5000)
        campo.fill(KEY_DE_PRUEBA)
        campo.dispatch_event("input")
        campo.dispatch_event("change")

        valor_ls = page.evaluate("() => localStorage.getItem('api_key')")
        assert valor_ls == KEY_DE_PRUEBA, (
            f"localStorage no contiene la key correcta. "
            f"Esperado: '{KEY_DE_PRUEBA}', encontrado: '{valor_ls}'"
        )

    def test_key_vacia_no_envia_header(self, page, base_url):
        """
        Cuando el campo #api-key está vacío, las peticiones al servidor
        no deben incluir el header X-Api-Key.
        """
        cabeceras_capturadas = {}

        def interceptar(route):
            cabeceras_capturadas.update(route.request.headers)
            route.continue_()

        page.route("**/health", interceptar)
        page.goto(f"{base_url}/resultados.html")

        # Asegurarse de que el campo queda vacío
        campo = page.locator("#api-key")
        campo.wait_for(state="visible", timeout=5000)
        campo.fill("")
        campo.dispatch_event("input")
        campo.dispatch_event("change")

        # Esperar a que la página haga una petición (p.ej. para comprobar el estado)
        page.wait_for_timeout(2000)

        header_enviado = cabeceras_capturadas.get("x-api-key") or cabeceras_capturadas.get(
            "X-Api-Key"
        )
        assert not header_enviado, (
            f"Se envió X-Api-Key con campo vacío: '{header_enviado}'"
        )
