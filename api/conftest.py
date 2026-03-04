"""
Fixtures específicos para los tests de API.
Incluye datos de prueba estándar y clientes sin autenticación.
"""
import httpx
import pytest

# ---------------------------------------------------------------------------
# Datos de prueba mínimos válidos
# ---------------------------------------------------------------------------
HISTORIAL = "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas."
EXAMEN    = "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta."
RECURSOS  = "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento."

PAYLOAD_ANALISIS = {
    "historial": HISTORIAL,
    "examen": EXAMEN,
    "conocimiento": RECURSOS,
    "perfil": "dmre",
}


@pytest.fixture(scope="module")
def payload_analisis() -> dict:
    """Payload mínimo válido para POST /analizar."""
    return PAYLOAD_ANALISIS.copy()


@pytest.fixture(scope="module")
def client_sin_key(base_url: str):
    """Cliente httpx sin ningún header de autenticación."""
    with httpx.Client(base_url=base_url, timeout=10) as client:
        yield client


@pytest.fixture(scope="module")
def client_key_incorrecta(base_url: str):
    """Cliente httpx con una API key incorrecta."""
    with httpx.Client(
        base_url=base_url,
        headers={"X-Api-Key": "clave-incorrecta-xyz-9999"},
        timeout=10,
    ) as client:
        yield client
