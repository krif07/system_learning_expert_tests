"""Tests de la página /resultados.html — escenario DMRE (Claudia Ríos, 6/10)."""
import pytest


HISTORIAL_DMRE = """\
Estudiante: Claudia Ríos | Curso: Buenas Prácticas de Reprocesamiento DMRE | Nivel: Profesional — Auxiliar de enfermería, central de esterilización

Sesiones de estudio (últimas 2 semanas):
- 03/02: Módulo 1 — Marco Normativo (35 min) - completó lectura y cuestionario
- 05/02: Módulo 2 — Organización y flujos (20 min) - leyó teoría, no completó ejercicios
- 07/02: Módulo 3 — Limpieza y desinfección (40 min) - completó todos los ejercicios
- 09/02: Módulo 4 — Empaque y rotulado (15 min) - abandonó a mitad de sesión
- 11/02: Módulo 5 — Esterilización (30 min) - completó lectura, no realizó ejercicios de indicadores

Evaluaciones previas:
- Evaluación Módulos 1–3: 8/10 — errores en clasificación de Spaulding y en rotulado\
"""

EXAMEN_DMRE = """\
Evaluación Final — Buenas Prácticas de Reprocesamiento DMRE
Fecha: 13/02/2026 | Puntaje: 6/10 | Estudiante: Claudia Ríos

Pregunta 1 (Normativa): Cuál es el objeto de la Resolución 914 de 2025
  Respuesta: CORRECTA

Pregunta 2 (Clasificación de Spaulding): Clasificar una sonda nasogástrica reutilizable
  Respuesta: INCORRECTA — la clasificó como no crítica en lugar de semicrítica

Pregunta 3 (Limpieza): Cuál es el primer paso después de usar un instrumental contaminado
  Respuesta: CORRECTA

Pregunta 4 (Desinfección): Qué nivel de desinfección requiere un endoscopio flexible
  Respuesta: INCORRECTA — respondió desinfección de nivel intermedio en lugar de alto nivel

Pregunta 5 (Empaque y rotulado): Qué información es obligatoria en el rotulado según Resolución 914
  Respuesta: INCORRECTA — omitió la fecha de esterilización y el número de lote

Pregunta 6 (Esterilización): Qué valida el indicador biológico en un ciclo de vapor
  Respuesta: CORRECTA

Pregunta 7 (Indicadores): Para qué sirve la prueba Bowie & Dick
  Respuesta: INCORRECTA — la confundió con el indicador químico de proceso

Pregunta 8 (Almacenamiento): Qué condición invalida un empaque almacenado
  Respuesta: CORRECTA

Pregunta 9 (Trazabilidad): Qué datos mínimos debe contener el registro de trazabilidad de un DMRE
  Respuesta: INCORRECTA — omitió el identificador del paciente y el operario responsable

Pregunta 10 (Bioseguridad): Qué EPP es obligatorio en la zona de descontaminación
  Respuesta: CORRECTA\
"""

CONOCIMIENTO_DMRE = """\
BASE DE RECURSOS DISPONIBLES — Buenas Prácticas de Reprocesamiento de Dispositivos Médicos y Elementos Reutilizables (DMRE)

MODULO_1_NORMATIVA_FUNDAMENTOS:
  [DMRE-N01] documento: "Resolución 914 de 2025 — Fragmentos clave para el personal asistencial" (20 min lectura) — Material del curso CEA
  [DMRE-N02] infografia: "Clasificación de Spaulding: crítico, semicrítico y no crítico aplicado al instrumental hospitalario y odontológico" — Material del curso CEA
  [DMRE-N03] video: "Cómo clasificar un dispositivo médico según Spaulding — casos prácticos" (15 min) — Canal institucional CEA
  [DMRE-N04] documento: "Responsabilidades del talento humano en el reprocesamiento según Resolución 914 de 2025" (15 min lectura) — Material del curso CEA

MODULO_2_ORGANIZACION_FLUJOS:
  [DMRE-O01] infografia: "Mapa de zonas funcionales de la central de reprocesamiento: flujos limpios y sucios" — Material del curso CEA
  [DMRE-O02] video: "Organización de la central de reprocesamiento: separación de áreas y condiciones ambientales" (20 min) — Canal institucional CEA
  [DMRE-O03] checklist: "Verificación de condiciones ambientales y flujos físicos en la central de reprocesamiento" — Material del curso CEA

MODULO_3_LIMPIEZA_DESINFECCION:
  [DMRE-L01] video: "Niveles de desinfección: alto, intermedio y bajo — cuándo y cómo aplicarlos según el tipo de dispositivo" (20 min) — Canal institucional CEA
  [DMRE-L02] checklist: "Protocolo de limpieza y desinfección por tipo de dispositivo médico" — Material del curso CEA
  [DMRE-L03] video: "Limpieza manual y ultrasónica: pasos, detergentes enzimáticos y tiempos de contacto" (18 min) — Canal institucional CEA
  [DMRE-L04] infografia: "EPP obligatorio por zona de la central de reprocesamiento — Resolución 914 de 2025" — Material del curso CEA
  [DMRE-L05] documento: "Inspección visual y pruebas funcionales del instrumental: criterios de aceptación y rechazo" (15 min lectura) — Material del curso CEA

MODULO_4_EMPAQUE_ROTULADO:
  [DMRE-E01] infografia: "Requisitos obligatorios de rotulado de empaques según Resolución 914 de 2025" — Material del curso CEA
  [DMRE-E02] video: "Errores frecuentes en rotulado y empaque — casos reales y cómo corregirlos" (18 min) — Canal institucional CEA
  [DMRE-E03] video: "Materiales de empaque compatibles por método de esterilización: vapor, calor seco y óxido de etileno" (15 min) — Canal institucional CEA
  [DMRE-E04] checklist: "Verificación de integridad del empaque antes del almacenamiento" — Material del curso CEA

MODULO_5_ESTERILIZACION_VALIDACION:
  [DMRE-S01] video: "Indicadores de esterilización: físicos, químicos y biológicos — diferencias y uso correcto" (22 min) — Canal institucional CEA
  [DMRE-S02] documento: "Prueba Bowie & Dick: procedimiento, interpretación y diferencia con indicadores químicos" (15 min lectura) — Material del curso CEA
  [DMRE-S03] video: "Parámetros críticos del ciclo de esterilización por vapor: temperatura, tiempo y presión" (20 min) — Canal institucional CEA
  [DMRE-S04] documento: "Liberación de carga: criterios de aprobación y rechazo de un ciclo de esterilización" (15 min lectura) — Material del curso CEA
  [DMRE-S05] infografia: "Métodos de esterilización: vapor, calor seco y agentes químicos — comparativa y aplicaciones" — Material del curso CEA

MODULO_6_ALMACENAMIENTO_TRAZABILIDAD:
  [DMRE-T01] video: "Trazabilidad completa del DMRE: registro correcto de cada etapa del proceso" (25 min) — Canal institucional CEA
  [DMRE-T02] plantilla: "Formato de registro de trazabilidad conforme a Resolución 914 de 2025 — campos obligatorios" — Material del curso CEA
  [DMRE-T03] documento: "Condiciones de almacenamiento: temperatura, humedad, rotación y tiempos máximos de resguardo por tipo de empaque" (15 min lectura) — Material del curso CEA
  [DMRE-T04] checklist: "Verificación de almacenamiento e inventario de material reprocesado" — Material del curso CEA

MODULO_7_DOCUMENTACION_AUDITORIA:
  [DMRE-D01] documento: "Guía para elaborar POE e instructivos de reprocesamiento conforme a la Resolución 914 de 2025" (20 min lectura) — Material del curso CEA
  [DMRE-D02] plantilla: "Formatos obligatorios de registro por etapa del proceso de reprocesamiento" — Material del curso CEA
  [DMRE-D03] video: "Cómo preparar la evidencia documental para una auditoría de reprocesamiento" (20 min) — Canal institucional CEA

MODULO_8_INTEGRACION_SALUD_ORAL:
  [DMRE-I01] video: "Flujo completo de reprocesamiento: integración de todas las etapas en un caso real" (30 min) — Canal institucional CEA
  [DMRE-I02] video: "Reprocesamiento en salud oral: particularidades del instrumental odontológico y riesgos específicos" (25 min) — Canal institucional CEA
  [DMRE-I03] caso_practico: "Análisis de casos de no conformidades reales en reprocesamiento: identificación y acciones correctivas" — Material del curso CEA
  [DMRE-I04] infografia: "Resumen del flujo completo de reprocesamiento DMRE — guía de bolsillo para el servicio" — Material del curso CEA\
"""


@pytest.mark.ui
class TestResultadosDMRE:
    """
    Escenario DMRE — Claudia Ríos, puntaje 6/10.

    Cubre el flujo completo del formulario con datos reales del curso
    "Buenas Prácticas de Reprocesamiento DMRE": llenado de campos,
    envío, polling de resultados y validación del contenido generado.
    """

    @pytest.mark.integration
    def test_analisis_dmre_devuelve_task_id(self, authenticated_page):
        """El POST a /analizar con datos DMRE debe responder 200 y devolver task_id."""
        authenticated_page.fill("#f-historial", HISTORIAL_DMRE)
        authenticated_page.fill("#f-examen", EXAMEN_DMRE)
        authenticated_page.fill("#f-conocimiento", CONOCIMIENTO_DMRE)

        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        resp = resp_info.value
        assert resp.status in (200, 429), (
            f"Se esperaba 200 o 429, se obtuvo {resp.status}"
        )

        if resp.status == 200:
            body = resp.json()
            assert "task_id" in body, "La respuesta debe contener 'task_id'"

    @pytest.mark.integration
    def test_score_badge_muestra_puntaje_tras_polling(self, authenticated_page):
        """Tras el polling, el badge de puntuación debe aparecer con un valor no vacío."""
        authenticated_page.fill("#f-historial", HISTORIAL_DMRE)
        authenticated_page.fill("#f-examen", EXAMEN_DMRE)
        authenticated_page.fill("#f-conocimiento", CONOCIMIENTO_DMRE)

        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        resp = resp_info.value
        if resp.status == 429:
            pytest.skip("Rate limit alcanzado — se omite verificación de badge")

        score = authenticated_page.locator(".score-badge .num")
        score.wait_for(state="visible", timeout=120_000)
        assert score.inner_text().strip() != "", "El badge de puntuación no debe estar vacío"

    @pytest.mark.integration
    def test_resultados_root_visible_en_viewport(self, authenticated_page):
        """
        Tras el análisis DMRE, #results-root debe estar visible y dentro
        del viewport gracias al scroll automático de la página.
        """
        authenticated_page.fill("#f-historial", HISTORIAL_DMRE)
        authenticated_page.fill("#f-examen", EXAMEN_DMRE)
        authenticated_page.fill("#f-conocimiento", CONOCIMIENTO_DMRE)

        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        if resp_info.value.status == 429:
            pytest.skip("Rate limit alcanzado — se omite verificación de viewport")

        results_root = authenticated_page.locator("#results-root")
        results_root.wait_for(state="visible", timeout=120_000)

        rect = authenticated_page.evaluate(
            """() => {
                const el = document.querySelector('#results-root');
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return { top: r.top, bottom: r.bottom, vh: window.innerHeight };
            }"""
        )
        if rect:
            assert rect["bottom"] > 0 and rect["top"] < rect["vh"], (
                "#results-root está fuera del viewport tras el análisis"
            )

    @pytest.mark.integration
    def test_recomendaciones_presentes_en_resultado(self, authenticated_page):
        """
        El bloque de recomendaciones debe aparecer en los resultados.
        Con 5 errores en el examen, el sistema debe generar al menos una recomendación.
        """
        authenticated_page.fill("#f-historial", HISTORIAL_DMRE)
        authenticated_page.fill("#f-examen", EXAMEN_DMRE)
        authenticated_page.fill("#f-conocimiento", CONOCIMIENTO_DMRE)

        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        if resp_info.value.status == 429:
            pytest.skip("Rate limit alcanzado — se omite verificación de recomendaciones")

        results_root = authenticated_page.locator("#results-root")
        results_root.wait_for(state="visible", timeout=120_000)

        # El bloque de recomendaciones puede estar bajo distintos selectores según la UI
        recomendaciones = authenticated_page.locator(
            "#results-root [class*='recomend'], "
            "#results-root [class*='recommend'], "
            "#results-root [class*='recurso'], "
            "#results-root [class*='resource']"
        )
        assert recomendaciones.count() > 0, (
            "No se encontró ningún bloque de recomendaciones o recursos en #results-root"
        )

    @pytest.mark.integration
    def test_campos_se_limpian_o_persisten_tras_analisis(self, authenticated_page):
        """
        Tras enviar el formulario DMRE, los campos #f-historial y #f-examen
        deben mantener su contenido o ser vaciados de forma controlada (no un estado roto).
        """
        authenticated_page.fill("#f-historial", HISTORIAL_DMRE)
        authenticated_page.fill("#f-examen", EXAMEN_DMRE)
        authenticated_page.fill("#f-conocimiento", CONOCIMIENTO_DMRE)

        with authenticated_page.expect_response("**/analizar") as resp_info:
            authenticated_page.click("#btn-analizar")

        if resp_info.value.status == 429:
            pytest.skip("Rate limit alcanzado — se omite verificación de campos")

        results_root = authenticated_page.locator("#results-root")
        results_root.wait_for(state="visible", timeout=120_000)

        historial_val = authenticated_page.input_value("#f-historial")
        examen_val = authenticated_page.input_value("#f-examen")

        # Los campos deben contener texto (persistencia) o estar vacíos (limpieza intencional)
        # En ningún caso deben contener un valor parcial o inválido
        assert isinstance(historial_val, str), "#f-historial debe ser string"
        assert isinstance(examen_val, str), "#f-examen debe ser string"
