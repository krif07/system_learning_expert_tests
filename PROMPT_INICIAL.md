---                                                                                                                                                                             
  Crea un proyecto de automatización de pruebas (UI + API) completamente                                                                                                            independiente para una API REST educativa construida con FastAPI.
  El proyecto de pruebas debe estar en una carpeta separada llamada                                                                                                               
  `system_learning_expert_tests/`.

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTEXTO DE LA APLICACIÓN BAJO PRUEBA
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Servidor base: http://localhost:8000
  Autenticación: header `X-Api-Key` (si no se envía o es incorrecta → 401).
                 Si el servidor no tiene API_ACCESS_KEY configurada,
                 todos los requests fallan sin autenticación excepto /health.

  ENDPOINTS DE LA API:

    GET  /health
         → 200 { "status": "ok" }
         → Público, no requiere API key.

    GET  /perfiles
         → 200 { "perfiles": [...], "default": "dmre" }
         → Público.

    POST /analizar
         Content-Type: application/json
         Body: {
           "historial": str,        # obligatorio, max 20.000 chars
           "examen": str,           # obligatorio, max 20.000 chars
           "conocimiento": str,     # obligatorio, max 20.000 chars
           "perfil": str,           # opcional, valores: dmre|secundaria|
                                    #   primaria|universitario|profesional
           "nombre": str,           # opcional
           "documento": str         # opcional, número de identificación
         }
         → 200 {
             "diagnostico": {
               "puntaje_general": str,
               "fortalezas": [str],
               "puntos_ciegos": [{ "tema": str, "razon_del_error": str }]
             },
             "ruta_nivelacion": [{
               "prioridad": "Alta"|"Media",
               "tema": str,
               "recurso_sugerido": str,
               "accion_requerida": str
             }],
             "metrica_progreso_estimada": float,  # 0–100
             "nivel_sugerido": "básico"|"intermedio"|"avanzado",
             "mensaje_motivador": str
           }
         → 401 sin API key (si el servidor la requiere)
         → 422 campos vacíos / perfil inválido / campo > 20.000 chars
         → 429 rate limit excedido (máx 10 req/min por IP)

    POST /analizar/lote
         Body: {
           "estudiantes": [   # máx 50 elementos
             { "nombre": str, "documento": str,
               "historial": str, "examen": str,
               "conocimiento": str, "perfil": str }
           ]
         }
         → 200 { "resultados": [...], "total": int,
                 "exitosos": int, "fallidos": int }
         → 400 si lote > 50 estudiantes
         → 401 / 422 / 429 igual que /analizar

    GET  /historial
         → 200 [ { "dir": str, "nombre": str, "documento": str,
                   "total": int, "ultima_sesion": str } ]
         → 401 si requiere API key

    GET  /historial/{student_dir}
         → 200 [ { "fecha": str, "nombre": str, "documento": str,
                   "perfil": str, "resultado": {...} } ]
         → 401 / 404

    GET  /conocimiento?perfil=dmre&categoria=ALGEBRA
         → 200 { "ALGEBRA": { ... }, ... }
         → 401 / 404 si no existe base para ese perfil

    GET  /recursos/links?tipo=video&directorio=dmre
         → 200 { "RECURSO-ID": { "url": str, "tipo": str }, ... }
         → 401

  PÁGINAS WEB (servidas por el mismo FastAPI en /):

    /resultados.html   Formulario de análisis individual.
                       Campos: nombre, documento, historial, examen,
                       conocimiento, selector de perfil, botón "Analizar".
                       Tras el análisis hace scroll automático a los resultados.
                       Muestra: puntaje, barra de progreso, fortalezas,
                       puntos ciegos, ruta de nivelación, mensaje motivador.

    /historial.html    Lista todos los estudiantes con sesiones guardadas.
                       Al hacer clic en un estudiante muestra sus sesiones.

    /examen.html       Formulario para cargar y visualizar resultados de examen.

    /conocimiento.html Explorador de la base de conocimiento por perfil/categoría.

    /comparativa.html  Comparativa de rendimiento entre estudiantes.

  PANEL DE API (presente en las 5 páginas):
    - Campo URL (default: http://localhost:8000)
    - Campo KEY (tipo password, persiste en localStorage como 'api_key')
    - Indicador de estado: punto verde/rojo/amarillo + texto
    - La KEY se envía automáticamente en todas las llamadas como X-Api-Key

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TECNOLOGÍA Y PAQUETES A USAR
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Lenguaje: Python 3.11+
  Framework de UI: Playwright (pytest-playwright)
  Framework de API: httpx (cliente async/sync, sin levantar servidor)
  Test runner: pytest
  Utilidades: python-dotenv (leer BASE_URL y API_KEY desde .env)

  Instalación:
    pip install pytest pytest-playwright httpx python-dotenv
    playwright install chromium

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ESTRUCTURA DEL PROYECTO A CREAR
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  system_learning_expert_tests/
    .env                        # BASE_URL y API_KEY (no commitear)
    .env.example                # plantilla sin valores reales
    requirements.txt
    pytest.ini                  # markers, base_url, etc.
    conftest.py                 # fixtures globales: api_client, base_url, api_key
    api/
      conftest.py               # fixtures específicos de API
      test_health.py
      test_auth.py
      test_analizar.py
      test_analizar_lote.py
      test_historial.py
      test_conocimiento.py
    ui/
      conftest.py               # fixtures de UI: page con key precargada,
                                # helper para esperar el punto verde
      test_resultados.py
      test_historial.py
      test_navegacion.py
      test_persistencia_key.py

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FIXTURES GLOBALES (conftest.py raíz)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Crea los siguientes fixtures con scope adecuado:

    base_url   → lee BASE_URL del .env, default "http://localhost:8000"
    api_key    → lee API_KEY del .env, default "" (sin autenticación)
    api_headers → dict con X-Api-Key si api_key no está vacío
    api_client → httpx.Client configurado con base_url y headers

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TESTS DE API A IMPLEMENTAR
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  test_health.py — clase TestHealth:
    - test_retorna_200
    - test_body_contiene_status_ok
    - test_no_requiere_api_key (request sin header → 200)

  test_auth.py — clase TestAutenticacion:
    - test_sin_header_retorna_401
    - test_header_incorrecto_retorna_401
    - test_header_correcto_retorna_200
    - test_endpoints_protegidos_parametrizado  (marca 6 endpoints con
      @pytest.mark.parametrize y verifica que todos devuelven 401 sin key)

  test_analizar.py — clase TestAnalizar:
    - test_campos_obligatorios_vacios_retornan_422
    - test_perfil_invalido_retorna_422
    - test_campo_mayor_20000_chars_retorna_422
    - test_campo_exactamente_20000_chars_pasa
    - test_respuesta_tiene_estructura_completa
    - test_respuesta_puntaje_no_es_nulo
    - test_respuesta_ruta_nivelacion_es_lista
    - test_metrica_es_numero_entre_0_y_100
    - test_todos_los_perfiles_aceptados (parametrizado)

    NOTA: los tests que llaman realmente a Gemini deben marcarse con
    @pytest.mark.integration y excluirse por defecto con:
      pytest -m "not integration"

  test_analizar_lote.py — clase TestAnalizarLote:
    - test_lote_mayor_50_retorna_400
    - test_respuesta_contiene_totales
    - test_campo_exitosos_mas_fallidos_igual_total

  test_historial.py — clase TestHistorial:
    - test_retorna_lista
    - test_estudiante_inexistente_retorna_404
    - test_sesiones_de_estudiante_existen_despues_de_analizar
      (requiere @pytest.mark.integration)

  test_conocimiento.py — clase TestConocimiento:
    - test_perfil_dmre_retorna_datos
    - test_perfil_invalido_retorna_404
    - test_filtro_categoria_reduce_resultado

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TESTS DE UI A IMPLEMENTAR
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ui/conftest.py debe definir:
    - Fixture `authenticated_page`: abre una página, inyecta la API key
      en localStorage y en el campo #api-key, espera a que el punto de
      estado sea verde (status-dot.ok) antes de retornar.
    - Fixture `sample_data`: dict con historial, examen, conocimiento
      de ejemplo suficientemente cortos para pruebas rápidas.

  test_resultados.py — clase TestResultados:
    - test_panel_api_visible_al_cargar
    - test_punto_estado_verde_con_servidor_corriendo
    - test_boton_analizar_deshabilitado_sin_campos
    - test_formulario_completo_muestra_resultados
      (llena los 3 campos obligatorios, hace clic en Analizar,
       espera page.expect_response("**/analizar"),
       verifica que .score-badge .num es visible y no vacío)
    - test_resultados_no_desaparecen_del_viewport
      (verifica que tras el análisis, results-root está dentro del
       viewport usando page.evaluate sobre getBoundingClientRect)
    - test_error_401_muestra_mensaje_de_error
      (sin key configurada contra servidor que la requiere →
       verifica que .api-error es visible)

  test_historial.py — clase TestHistorialUI:
    - test_pagina_carga_sin_errores
    - test_lista_estudiantes_visible_si_hay_historial
    - test_click_en_estudiante_muestra_sesiones

  test_navegacion.py — clase TestNavegacion:
    - test_links_de_nav_funcionan  (parametrizado con las 5 páginas)
    - test_pagina_activa_tiene_clase_active

  test_persistencia_key.py — clase TestPersistenciaKey:
    - test_key_persiste_entre_paginas
      (escribe key en resultados.html, navega a historial.html,
       verifica que #api-key tiene el mismo valor)
    - test_key_se_guarda_en_localstorage
      (escribe key, verifica con page.evaluate que
       localStorage.getItem('api_key') coincide)
    - test_key_vacia_no_envia_header
      (intercepta el request con page.route y verifica que no
       lleva X-Api-Key cuando el campo está vacío)

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DATOS DE PRUEBA
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Usar estos datos mínimos válidos en todos los tests que lo necesiten:

    HISTORIAL = "Estudiante: Test | Curso: DMRE\nSesiones: 3 completadas."
    EXAMEN    = "Examen DMRE | Puntaje: 60\nPregunta 1: Incorrecta."
    RECURSOS  = "MÓDULO 1:\n  [DMRE-S01] Video: Introducción al reprocesamiento."

    PAYLOAD_ANALISIS = {
        "historial": HISTORIAL,
        "examen": EXAMEN,
        "conocimiento": RECURSOS,
        "perfil": "dmre"
    }

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONFIGURACIÓN pytest.ini
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [pytest]
  markers =
      integration: llama a Gemini o escribe en disco — requiere servidor real
      ui: tests de navegador con Playwright
  addopts = -m "not integration"

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  REGLAS DE IMPLEMENTACIÓN
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Todos los tests de API que no llaman a Gemini deben funcionar sin
     servidor corriendo (httpx contra TestClient no aplica aquí — sí
     necesitan servidor). Indicar en README cómo arrancarlo.

  2. Los tests de UI siempre necesitan el servidor corriendo. Agregar al
     conftest un skip automático si el servidor no responde en /health.

  3. No hardcodear BASE_URL ni API_KEY en el código. Siempre desde .env.

  4. Cada clase de test debe tener un docstring explicando qué cubre.

  5. Crear README.md con:
     - Prerequisitos
     - Cómo arrancar el servidor del proyecto original
     - Cómo instalar dependencias
     - Comandos para correr solo API, solo UI, solo integration,
       o todo junto

  ---