"""
Fixtures globales disponibles para todos los tests del proyecto.
Carga BASE_URL y API_KEY desde el archivo .env.
"""
import os

import httpx
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """URL base del servidor FastAPI bajo prueba."""
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api_key() -> str:
    """API key leída desde .env; cadena vacía si no está configurada."""
    return os.getenv("API_KEY", "")


@pytest.fixture(scope="session")
def api_headers(api_key: str) -> dict:
    """Headers con X-Api-Key si la key no está vacía."""
    if api_key:
        return {"X-Api-Key": api_key}
    return {}


@pytest.fixture(scope="session")
def api_client(base_url: str, api_headers: dict):
    """Cliente httpx configurado con base_url y headers de autenticación."""
    with httpx.Client(base_url=base_url, headers=api_headers, timeout=30) as client:
        yield client
