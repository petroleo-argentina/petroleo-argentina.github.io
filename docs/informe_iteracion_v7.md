# Informe Técnico y Auditoría — Iteración V7

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Iteración:** V7 — Mapa a color, paneles reactivos translúcidos y corrección editorial  
**Fecha:** Octubre 2026  
**Ambiente:** MapLibre GL JS 4.7.1 + FastAPI / Uvicorn + Python 3.12 (25/25 tests superados)

---

## 1. Resumen Ejecutivo de Implementación

En esta iteración se completaron las cinco directrices de diseño, cartografía, arquitectura de interfaz y rigor editorial solicitadas en la especificación de Iteración V7:

1. **Paneles Reactivos Translúcidos con Oscurecimiento Suave:**
   - En estado de reposo, el panel flotante `#chart-overlay-panel` adopta un fondo translúcido neutro con token `--panel-bg-translucent: rgba(13, 16, 21, 0.68)` y `backdrop-filter: blur(10px)`, permitiendo percibir el territorio y el relieve montañoso que subyacen al gráfico sin interferir con la legibilidad tipográfica.
   - Al interactuar (`:hover` del puntero o `:focus-within` por navegación de teclado de cualquier control, botón o canvas interior), el fondo transiciona de forma suave (180 ms) hacia `--panel-bg-opaque: rgba(13, 16, 21, 0.94)`.
   - **Regla crítica respetada:** Se alteró exclusivamente el canal alfa del color de fondo (`background-color`), sin modificar jamás la propiedad CSS `opacity` del contenedor, garantizando que textos, curvas, números y botones conserven 100% de nitidez y contraste.
   - En pantallas táctiles sin capacidad de hover (`@media (hover: none)`), se define una opacidad fija adecuada (`rgba(13, 16, 21, 0.88)`), evitando clics ciegos o bloqueos.

2. **Cartografía Base Satelital con Color Natural y Relieve 3D Armónico:**
   - Se reemplazó el tono monocromático gris/oliva oscuro por imágenes satelitales de alta resolución a color real provistas por **ESRI World Imagery** (`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`), libres de rótulos de texto incrustados en inglés.
   - Se conservó la malla de elevación 3D Terrarium (`raster-dem`) sobre MapLibre GL JS, pero se redujo la exageración del hillshade a 0.32 con sombras atenuadas (`#13212A` al 35%), evitando ensuciar los tonos vivos del mar azul, los valles verdes y las mesetas patagónicas.

3. **Toponimia Oficial: «ISLAS MALVINAS»:**
   - Se suprimió de raíz cualquier rótulo o referencia en inglés ("Falkland Islands") mediante un filtro de exclusión compuesto `['!=', ['get', 'name_en'], 'Falkland Islands']` aplicado a todas las capas vectoriales de toponimia.
   - Se incorporó la capa de símbolos protagonista `islas-malvinas-label` vinculada a la fuente GeoJSON `islas-malvinas-source` en coordenadas `[-59.5, -51.75]`, renderizando **«ISLAS MALVINAS»** en mayúsculas, tamaño dinámico interpolado por zoom (11px a 18px), halo oscuro de alto contraste (`#0B0E13`, ancho 2.5px) y superposición garantizada (`text-allow-overlap: true`).

4. **Auditoría Editorial: Corrección del Máximo Histórico, Variación Interanual y Unidades:**
   - **Retiro de «(Récord)»:** Se auditó la serie histórica oficial (1950–2025). El récord histórico absoluto de producción petrolera nacional de la serie pertenece al año **1998 con 49.147,7 miles de m³** (~846.930 bpd). La cifra de 2025 (**46.438,5 miles de m³**, ~798.500 bpd) representa el mayor nivel en 26 años y el récord histórico del petróleo no convencional (shale), pero no el récord absoluto del país. La etiqueta «(Récord)» contradecía la propia curva del gráfico y fue removida en su totalidad.
   - **Variación Dinámica Interanual:** El distintivo del KPI ahora calcula de forma reactiva la variación porcentual **respecto del año anterior comparable**: para 2025 muestra `+12,8% vs 2024` (46.438,5 vs 41.152,2 miles de m³). Al mover la barra temporal, recalcula dinámicamente (`+10,0% vs 2023` en 2024, `-11,6% vs 2019` en 2020, etc.).
   - **Unidades Explícitas:** Se eliminó la abreviatura ambigua "Mm³" en favor de «miles de m³» (y «barriles/día» en modo alternativo), unificando el indicador del scrubber (`46.438,5 miles de m³`), los tooltips y los ejes del gráfico.

5. **Header Depurado & Control Compacto de Capas:**
   - Se eliminaron del menú superior los botones «Preguntas», «Capas» y «Fuentes», junto con los modales y cajones extensos (`#modal-preguntas`, `#layers-drawer`, `#modal-metodologia`).
   - Se preservó «Relato continuo» (`#btn-auto-tour`) y los modos Relato / Explorar.
   - Se integró un selector compacto y contextual «Mostrar» dentro de `#filter-controls-container`, permitiendo alternar la visibilidad de la capa operativa protagonista del capítulo (cuencas, pozos, concesiones, oleoductos) de forma directa, sin alterar los filtros ni los totales calculados.

---

## 2. Auditoría Analítica y Conciliación Numérica

### 2.1. Conciliación del Máximo Histórico y Producción 2025
| Métrica | 1998 (Pico Histórico) | 2017 (Piso Pre-Shale) | 2024 (Año Previo) | 2025 (Consolidado) |
|---|---|---|---|---|
| **Producción Anual (miles de m³)** | **49.147,7** | 28.330,9 | 41.152,2 | **46.438,5** |
| **Caudal Promedio (barriles/día)** | 846.930 bpd | 488.225 bpd | 707.592 bpd | 798.500 bpd |
| **Variación Anual vs Año Anterior** | +0,2% vs 1997 | -6,0% vs 2016 | +10,0% vs 2023 | **+12,8% vs 2024** |
| **Variación Acumulada vs 2017** | — | Base | +45,3% | +63,9% |
| **Condición del Dato** | Máximo histórico serie oficial | Mínimo local prepandemia | Oficial consolidado | Oficial Res. 319/93 |

**Conclusión:**
La afirmación «+63,9% vs 2017 (Récord)» confundía dos conceptos: el crecimiento acumulado del ciclo shale 2017–2025 (+63,91%) con un récord absoluto de la serie. En los hechos, 1998 superó a 2025 en 2.709,2 miles de m³ (+5,8%). En V7 la narrativa precisa con rigor: *«mayor nivel en 26 años y récord histórico no convencional»*, eliminando toda contradicción visual con el gráfico.

### 2.2. Unidades y Factores de Conversión
- **Volumen:** $1\text{ m}^3 = 6,28981\text{ barriles}$.
- **Días calendario:** 2024 (bisiesto: 366 días); 2025 (365 días).
- **Cálculo diario 2025:**
  $$\frac{46.438.500\text{ m}^3 \times 6,28981}{365\text{ días}} = 798.498,6\approx 798.500\text{ barriles/día}$$
- Se uniformó la notación en la interfaz a «miles de m³» (con separador de miles y un decimal en español: `46.438,5 miles de m³`) y «barriles/día».

---

## 3. Matriz de Validación de Requisitos V7

| Caso / Requisito | Comportamiento Implementado | Estado de Verificación |
|---|---|---|
| **Overlay en reposo** | Fondo `rgba(13, 16, 21, 0.68)` con `backdrop-filter: blur(10px)`. El mapa y relieve se perciben por detrás. | ✅ Verificado en CSS y tests automatizados |
| **Overlay en interacción** | Transición a `rgba(13, 16, 21, 0.94)` al `:hover` o `:focus-within`. Sin alterar `opacity` de contenedor. | ✅ Verificado en CSS y tests automatizados |
| **Dispositivos táctiles** | Media query `(hover: none)` con opacidad predeterminada `0.88`. | ✅ Verificado en CSS |
| **Mapa a color natural** | Satélite ESRI World Imagery sin rótulos en inglés + hillshade suave (0.32). | ✅ Verificado en MapLibre style JSON |
| **Toponimia Malvinas** | Layer `islas-malvinas-label` (`[-59.5, -51.75]`), halo 2.5px, exclusión de "Falkland Islands". | ✅ Verificado en estilo y app.js |
| **KPI y unidades** | Unidad explícita «miles de m³» / «barriles/día». Sin «Mm³» ambiguo. | ✅ Verificado en app.js y DOM |
| **Variación interactiva** | Variación calculada respecto del año anterior (`+12,8% vs 2024`). | ✅ Verificado en app.js y tests |
| **Máximo de serie** | 1998 documentado como pico histórico (49.147,7 miles m³); retiro total de falso récord. | ✅ Verificado en test suite |
| **Encabezado simplificado** | Retirados «Preguntas», «Capas» y «Fuentes»; «Relato continuo» activo. | ✅ Verificado en index.html y app.js |
| **Control de capas compacto** | Selector «Mostrar» por capítulo integrado en barra de filtros. | ✅ Verificado en app.js y test suite |

---

## 4. Estado de los Tests Automatizados

La suite de pruebas en `tests/test_platform.py` fue ampliada para auditar exhaustivamente las directrices de la Iteración V7.
Resultado de la ejecución (`pytest tests/test_platform.py -v`):
```text
tests/test_platform.py::test_static_data_files_exist PASSED              [  4%]
tests/test_platform.py::test_historical_peak_1998_and_2025_expansion_metric PASSED [  8%]
tests/test_platform.py::test_shale_share_62_92_pct PASSED                [ 12%]
tests/test_platform.py::test_crossover_november_2023 PASSED              [ 16%]
tests/test_platform.py::test_pareto_top_milestones PASSED                [ 20%]
tests/test_platform.py::test_pareto_912_wells_explain_50_pct PASSED      [ 24%]
tests/test_platform.py::test_endpoints_cohortes PASSED                   [ 28%]
tests/test_platform.py::test_endpoints_macro PASSED                      [ 32%]
tests/test_platform.py::test_charts_data_non_empty PASSED                [ 36%]
tests/test_platform.py::test_geo_trajectories_validity PASSED            [ 40%]
tests/test_platform.py::test_geo_pipelines_connectivity PASSED           [ 44%]
tests/test_platform.py::test_api_endpoints_live PASSED                   [ 48%]
tests/test_platform.py::test_carto_config_and_fallback_style PASSED      [ 52%]
tests/test_platform.py::test_pareto_api_endpoint_and_milestones PASSED   [ 56%]
tests/test_platform.py::test_v4_v5_dom_structure PASSED                  [ 60%]
tests/test_platform.py::test_v4_v5_css_overlay_and_filter_styling PASSED [ 64%]
tests/test_platform.py::test_v4_v5_app_js_state_and_chapter05_stacked_charts PASSED [ 68%]
tests/test_platform.py::test_v6_seven_chapters_and_synthesis_removed PASSED [ 72%]
tests/test_platform.py::test_v7_simplified_masthead_and_compact_layer_controls PASSED [ 76%]
tests/test_platform.py::test_v7_translucent_reactive_overlay_styling PASSED [ 80%]
tests/test_platform.py::test_v7_islas_malvinas_cartography PASSED        [ 84%]
tests/test_platform.py::test_v7_absence_of_false_record_claims_and_explicit_units PASSED [ 88%]
tests/test_platform.py::test_v6_reserved_right_rail_and_overlay_spacing PASSED [ 92%]
tests/test_platform.py::test_v6_unified_panel_design_tokens PASSED       [ 96%]
tests/test_platform.py::test_v6_filter_bar_labels_and_reset_view PASSED  [100%]

============================= 25 passed in 0.98s ==============================
```

---

## 5. Declaración de Limitaciones Cartográficas y del Entorno de Navegación

1. **Subagente de Navegación Headless / Playwright:**
   - La herramienta automatizada de subagente browser reportó un error de red externo al intentar descargar el binario `playwright-1.57.0-win32_x64.zip` desde los servidores Azure CDN (código 404 de upstream). El servidor de la aplicación (`uvicorn api.main:app`) se encuentra corriendo localmente en `http://127.0.0.1:8000/` respondiendo con estado HTTP 200 de forma ininterrumpida.
2. **Proveedor Cartográfico ESRI World Imagery:**
   - Los tiles satelitales a color provienen del servicio oficial de Esri ArcGIS Online sin capas de etiquetas anglosajonas incrustadas. La atribución reglamentaria se encuentra declarada en los metadatos de la fuente en `petroleo-map-style.json` conforme a las normas de uso de ArcGIS.
   - En niveles de zoom extremos (> 18), la resolución satelital depende de la cobertura ortofotográfica disponible en zonas remotas de la estepa patagónica.
