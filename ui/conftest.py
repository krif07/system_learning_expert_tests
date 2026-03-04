"""
Fixtures específicos para los tests de UI (Playwright).
Incluye skip automático si el servidor no está disponible.
"""
import httpx
import pytest


# ---------------------------------------------------------------------------
# Skip automático si el servidor no responde
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def skip_if_server_down(base_url: str):
    """Salta todos los tests de UI si el servidor no responde en /health."""
    try:
        resp = httpx.get(f"{base_url}/health", timeout=5)
        if resp.status_code != 200:
            pytest.skip(
                f"Servidor no disponible — /health devolvió {resp.status_code}",
                allow_module_level=True,
            )
    except Exception as exc:
        pytest.skip(
            f"No se puede conectar al servidor ({exc})",
            allow_module_level=True,
        )


# ---------------------------------------------------------------------------
# Datos de ejemplo para UI
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_data() -> dict:
    """Datos mínimos válidos para el formulario de análisis."""
    return {
        "historial": "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas.",
        "examen": "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta.",
        "conocimiento": "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento.",
    }


# ---------------------------------------------------------------------------
# Página autenticada
# ---------------------------------------------------------------------------
@pytest.fixture
def authenticated_page(page, base_url: str, api_key: str):
    """
    Abre /resultados.html, inyecta la API key en localStorage y en el campo
    #api-key, luego espera a que el indicador de estado sea verde antes de
    retornar la página lista para usar.
    """
    page.goto(f"{base_url}/resultados.html")

    # Inyectar en localStorage de forma segura (evita problemas con caracteres especiales)
    page.evaluate("(key) => localStorage.setItem('api_key', key)", api_key)

    # Recargar para que la página lea el valor de localStorage
    page.reload()

    # Completar el campo visible y disparar el evento para que la app reaccione
    api_key_input = page.locator("#api-key")
    api_key_input.wait_for(state="visible", timeout=5000)
    api_key_input.fill(api_key)
    api_key_input.dispatch_event("input")
    api_key_input.dispatch_event("change")

    # Esperar el indicador verde (status-dot con clase "ok")
    page.wait_for_selector(".status-dot.ok", timeout=10000)

    return page
