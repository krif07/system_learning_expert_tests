# system_learning_expert_tests

Suite de pruebas automatizadas (UI + API) para la API REST educativa **system_learning_expert**.

---

## Prerequisitos

- Python 3.11+
- El servidor FastAPI del proyecto original corriendo en `http://localhost:8000`
- (Opcional) API key configurada en el servidor

---

## Cómo arrancar el servidor del proyecto original

Desde la raíz del proyecto original:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O si usa variables de entorno:

```bash
API_ACCESS_KEY=tu_clave uvicorn main:app --reload
```

---

## Instalación de dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Configuración

Copiar `.env.example` a `.env` y completar con los valores reales:

```bash
cp .env.example .env
```

Variables disponibles:

| Variable   | Descripción                                | Default                    |
|------------|--------------------------------------------|----------------------------|
| `BASE_URL` | URL base del servidor FastAPI              | `http://localhost:8000`    |
| `API_KEY`  | Clave de acceso (header `X-Api-Key`)       | `""` (sin autenticación)   |

---

## Comandos para correr los tests

### Solo tests de API (sin llamadas a Gemini)
```bash
pytest api/ -m "not integration" -v
```

### Solo tests de UI
```bash
pytest ui/ -v
```

### Solo tests de integración (requiere Gemini configurado)
```bash
pytest -m integration -v
pytest "ui/test_resultados.py::TestResultados::test_formulario_completo_muestra_resultados" -m "" -v                                                                                                                                                                                                                                                                    
  El -m "" anula el filtro not integration del pytest.ini. También puedes correr todos los integration de UI:                                                                        

  pytest ui/ -m integration -v
```

### Todo junto (excluye integration por defecto)
```bash
pytest -v
```

### Todo incluyendo integration
```bash
pytest -m "" -v
```

### Con reporte HTML
```bash
pytest --html=report.html --self-contained-html -v
```

---

## Estructura del proyecto

```
system_learning_expert_tests/
  .env                    # Variables reales (NO commitear)
  .env.example            # Plantilla sin valores reales
  requirements.txt
  pytest.ini
  conftest.py             # Fixtures globales: base_url, api_key, api_client
  README.md
  api/
    conftest.py           # Fixtures de API: payloads, clientes sin key
    test_health.py        # Tests del endpoint GET /health
    test_auth.py          # Tests de autenticación
    test_analizar.py      # Tests del endpoint POST /analizar
    test_analizar_lote.py # Tests del endpoint POST /analizar/lote
    test_historial.py     # Tests de los endpoints GET /historial
    test_conocimiento.py  # Tests del endpoint GET /conocimiento
  ui/
    conftest.py           # Fixtures de UI: authenticated_page, sample_data
    test_resultados.py    # Tests de /resultados.html
    test_historial.py     # Tests de /historial.html
    test_navegacion.py    # Tests de navegación entre páginas
    test_persistencia_key.py  # Tests de persistencia de la API key
```
