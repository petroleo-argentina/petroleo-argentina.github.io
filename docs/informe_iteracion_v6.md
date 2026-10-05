# Informe Consolidado — Iteración V6: Navegación Visible, Paneles Homogéneos y Filtros Claros

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Iteración:** V6 (Layout, Paneles, Filtros y Cierre Narrativo)  
**Fecha de Implementación:** 2026-10-04  
**Estado:** Implementación y validación completadas al 100% (21/21 pruebas unitarias e integrales superadas).

---

## 1. Resumen Ejecutivo de la Intervención

A partir de la revisión visual sobre la captura de pantalla de la iteración previa, la **Iteración V6** corrigió cuatro aspectos clave de diseño, distribución espacial y narrativa sin alterar el núcleo cartográfico ni los cálculos analíticos auditados:

1. **Despeje y protección de la navegación vertical de capítulos (`#journey-tracker-nav`):** Se reservó una franja exclusiva en el lateral derecho de la pantalla (`right: 18px; z-index: 50;`) y se desplazó el panel flotante de visualización hacia el interior (`right: 76px; width: 440px; z-index: 40;`). Las dos áreas quedan físicamente separadas por un margen de seguridad de más de 50px, eliminando cualquier colisión o solapamiento.
2. **Unificación estética de todos los paneles:** Se homogeneizaron los fondos, bordes y curvaturas entre la columna editorial de lectura, el panel de gráficos, la barra de filtros y la línea de tiempo. Se eliminó por completo el fondo pardusco/oliva del gráfico y de los desplegables, aplicando un único fondo carbón neutro translúcido (`rgba(13, 16, 21, 0.92)`) con desenfoque de 18px, borde micrométrico de 1px y esquinas redondeadas uniformes de 8px.
3. **Filtros contextuales claros y explícitos:** Cada selector en la barra superior (`#global-filter-bar`) ahora cuenta con una etiqueta breve y visible (`Período`, `Cuenca`, `Recurso`, `Umbral Pareto`, etc.), indicador de flecha desplegable (`▾`), opciones con texto completo (`1950–2025 · Todo el período`) y un botón con rótulo fiel a su comportamiento: `Restablecer vista` (recupera modo, filtros, tiempo y cámara original del capítulo).
4. **Eliminación del capítulo redundante «Síntesis»:** El atlas se condensó en **7 capítulos sustantivos** (01 a 07), finalizando limpiamente en el Capítulo 07: *Del pozo al país (Economía & Macro)*. Se actualizaron los contadores de capítulos a 7, el carril de navegación a 7 puntos y el modal de preguntas a 7 interrogantes. En el Capítulo 07, el botón de avance ofrece la acción `volver al inicio ↺` para un reinicio fluido.

---

## 2. Matriz de Cambios por Componente

| Componente | Estado Anterior (V4+V5) | Estado Final Refinado (V6) | Criterio de Aceptación Cumplido |
|---|---|---|---|
| **Carril de Navegación (`#journey-tracker-nav`)** | `right: 24px`, `z-index: 30`. Los tooltips y puntos se solapaban con el gráfico flotante. | `right: 18px`, `z-index: 50`. Nodos con área de clic táctil de `32px x 32px` (`role="button"`, `tabindex="0"`). Tooltip badge oscuro a `right: 36px`. | Navegación visible e interactuable en todos los capítulos sin colisión con gráficos. |
| **Panel Flotante (`#chart-overlay-panel`)** | `right: 48px`, `width: 470px`, `z-index: 40`. Fondo oliva `rgba(26, 27, 22, 0.88)` y radio 12px. | `right: 76px`, `width: 440px`, `z-index: 40`. Fondo neutral idéntico a la columna editorial `var(--panel-bg)` y radio de 8px. | Homogeneidad visual total con el panel izquierdo; corredor libre de > 50px con el carril. |
| **Barra Superior (`#global-filter-bar`)** | Controles tipo select sin etiquetas visibles; selector de modo pegado a los selectores; botón `Restablecer`. | Separador visual `.filter-separator`; cada filtro encapsulado en `.filter-field-group` con etiqueta en mayúscula mono (`.filter-field-label`) y flecha (`▾`). Botón `Restablecer vista`. | Es inmediato reconocer qué modifica cada control y cuál es su valor actual. |
| **Capítulo 01 Filtros** | Etiqueta genérica `Rango Temporal` con textos `Serie Completa (1950—2025)`. | Etiqueta `Período:` con valor predeterminado `1950–2025 · Todo el período`. | Cumple con la formulación unívoca exigida por la especificación V6. |
| **Capítulo 08 (Síntesis)** | Existía como 8vo capítulo redundante con tabla de operadores y zoom nacional. | **Eliminado por completo.** El recorrido concluye en el Capítulo 07 (*Economía*). | Se acorta el relato evitando redundancias; no hay contadores desfasados ni pantallas rotas. |
| **Cierre del Recorrido** | El botón `siguiente →` quedaba deshabilitado en el último capítulo. | El botón se transforma en `volver al inicio ↺`, permitiendo un bucle fluido de exploración. | Experiencia continua sin callejones sin salida. |

---

## 3. Tokens del Sistema de Diseño Unificado

```css
:root {
  /* Unified Panel System Tokens (Iteración V6) */
  --panel-bg: rgba(13, 16, 21, 0.92);
  --panel-bg-elevated: rgba(22, 27, 36, 0.78);
  --panel-border: 1px solid rgba(255, 255, 255, 0.08);
  --panel-border-subtle: 1px solid rgba(255, 255, 255, 0.14);
  --panel-radius: 8px;
  --panel-radius-sm: 4px;
  --panel-backdrop: blur(18px) saturate(180%);
  --panel-shadow: 0 20px 48px rgba(0, 0, 0, 0.65);
}
```

- **Columna de Historia (`.story-column`):** Fondo `var(--panel-bg)`, borde `var(--panel-border)`, radio `var(--panel-radius)`.
- **Panel de Gráfico (`.chart-overlay-panel`):** Fondo `var(--panel-bg)`, borde `var(--panel-border)`, radio `var(--panel-radius)`.
- **Barra de Filtros (`.global-filter-bar`):** Fondo `var(--panel-bg)`, borde inferior de 1px.
- **Bandeja de Timeline (`.timeline-bar-inner`):** Fondo `var(--panel-bg)`, borde `var(--panel-border)`, radio `var(--panel-radius)`.

---

## 4. Registro de Pruebas Automatizadas (21 de 21 Aprobadas)

```text
============================= test session starts =============================
platform win32 -- Python 3.12.2, pytest-9.1.1, pluggy-1.6.0
rootdir: petroleo-argentina
plugins: anyio-4.15.1, asyncio-1.4.0, typeguard-4.5.2

tests/test_platform.py::test_static_data_files_exist PASSED              [  4%]
tests/test_platform.py::test_2025_record_production_metric PASSED        [  9%]
tests/test_platform.py::test_shale_share_62_92_pct PASSED                [ 14%]
tests/test_platform.py::test_crossover_november_2023 PASSED              [ 19%]
tests/test_platform.py::test_pareto_top_milestones PASSED                [ 23%]
tests/test_platform.py::test_pareto_912_wells_explain_50_pct PASSED      [ 28%]
tests/test_platform.py::test_endpoints_cohortes PASSED                   [ 33%]
tests/test_platform.py::test_endpoints_macro PASSED                      [ 38%]
tests/test_platform.py::test_charts_data_non_empty PASSED                [ 42%]
tests/test_platform.py::test_geo_trajectories_validity PASSED            [ 47%]
tests/test_platform.py::test_geo_pipelines_connectivity PASSED           [ 52%]
tests/test_platform.py::test_api_endpoints_live PASSED                   [ 57%]
tests/test_platform.py::test_carto_config_and_fallback_style PASSED      [ 61%]
tests/test_platform.py::test_pareto_api_endpoint_and_milestones PASSED   [ 66%]
tests/test_platform.py::test_v4_v5_dom_structure PASSED                  [ 71%]
tests/test_platform.py::test_v4_v5_css_overlay_and_filter_styling PASSED [ 76%]
tests/test_platform.py::test_v4_v5_app_js_state_and_chapter05_stacked_charts PASSED [ 80%]
tests/test_platform.py::test_v6_seven_chapters_and_synthesis_removed PASSED [ 85%]
tests/test_platform.py::test_v6_reserved_right_rail_and_overlay_spacing PASSED [ 90%]
tests/test_platform.py::test_v6_unified_panel_design_tokens PASSED       [ 95%]
tests/test_platform.py::test_v6_filter_bar_labels_and_reset_view PASSED  [100%]

============================= 21 passed in 0.87s ==============================
```

---

## 5. Archivos Modificados

1. [`frontend/app.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/app.js):
   - Reducción de capítulos a 7; eliminación del objeto `nuevo_mapa`.
   - Ajuste de `JOURNEY_NODES` a 7 coordenadas espaciadas verticalmente a lo largo de 360px.
   - Envoltura de filtros en `.filter-field-group` con `<label>` explícito y flecha chevron.
   - Manejo de fin de relato con botón `volver al inicio ↺` y detención limpia del auto-tour.
   - Clampeo estricto de índices de capítulo entre 0 y 6 para prevenir desbordes o enlaces antiguos a Síntesis.
2. [`frontend/index.html`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.html):
   - Actualización de título del modal a *Índice de 7 preguntas clave* y titular *Siete interrogantes sobre el subsuelo argentino*.
   - Eliminación del item 08 del modal de preguntas.
   - Cambio de rótulo de botón a `Restablecer vista`.
3. [`frontend/index.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.css):
   - Definición de tokens unificados `--panel-bg`, `--panel-border`, `--panel-radius`.
   - Reubicación de `.editorial-vertical-index` a `right: 18px; z-index: 50;` con nodos táctiles de `32px`.
   - Reubicación de `.chart-overlay-panel` a `right: 76px; width: 440px; z-index: 40;` con fondo carbón neutro.
   - Estilizado de `.filter-field-group`, `.filter-field-label`, `.filter-select-wrap` y `.filter-select-arrow`.
   - Media queries responsivas actualizadas para monitores ultra-wide, laptops intermedias y dispositivos móviles.
4. [`tests/test_platform.py`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/tests/test_platform.py):
   - Inclusión de 4 nuevos casos de prueba específicos de la Iteración V6, alcanzando 21 pruebas automáticas.
5. [`DESIGN.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/DESIGN.md) & [`docs/historia_visual.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/historia_visual.md):
   - Documentación de las directrices V6 (espacio reservado de navegación, tokens homogéneos, etiquetas y final en Capítulo 07).
