# Informe de Implementación — Iteración V9: Zoom, Fotografías Progresivas, Tipografía Bipolar y Guía Argentinosaurus

**Proyecto:** Plataforma Cartográfica y Crónica Visual «Petróleo en Argentina: Del pozo al país»  
**Fecha de Entrega:** 4 de Octubre de 2026  
**Estado:** Implementación Completa, Auditada y Verificada (34/34 Tests Automatizados Pasados)

---

## 1. Resumen Ejecutivo de la Iteración V9

La Iteración V9 aborda de manera integral la ergonomía cartográfica, la autenticidad visual fotográfica, la cohesión tipográfica y la narrativa editorial de la plataforma, resolviendo los desacoples detectados en iteraciones previas:

1. **Rueda del ratón y trackpad para zoom cartográfico exclusivo:** Se eliminó por completo el avance de capítulos vinculado al evento `wheel` (`setupScrollWheelNavigation`), permitiendo un acercamiento y alejamiento fluido y sin saltos accidentales en MapLibre GL JS. El scroll de los paneles de texto y gráficos quedó aislado (`stopPropagation()`) para que el desplazamiento de contenido no interfiera con el mapa.
2. **Fotografías progresivas por escala y modal de inspección:** Los puntos vectoriales representan los pozos a nivel nacional/regional (`zoom < 7.0`), mientras que a escala local/yacimiento (`zoom >= 7.0`) emergen miniaturas circulares con fotos reales verificadas de pozos, complejos e instalaciones, con clic interactivo hacia un diálogo modal `#photo-detail-modal` con ficha de autoría, procedencia y licencia oficial.
3. **Inventario fotográfico riguroso y crédito de portada enriquecido:** Se confeccionó el documento normativo [`docs/inventario_fotografico.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/inventario_fotografico.md) con 5 fotografías reales verificadas de Wikimedia Commons y la ficha del guía editorial. La portada incorpora enlaces directos a la ficha original y a la licencia CC BY 3.0.
4. **Sistema tipográfico bipolar oficial (Alegreya + Archivo):** Reducción estricta a dos familias de alta legibilidad editorial: **Alegreya** para la gran titulación y capítulos; **Archivo** para cuerpo, etiquetas, micrográficos de Chart.js y cifras tabulares. Ambas familias cuentan con fuentes locales `.woff2` en `frontend/fonts/` y licencias Open Font License (OFL).
5. **Panel izquierdo reactivo y translúcido:** Adopción unificada de los tokens del panel derecho: superficie translúcida en reposo (`rgba(13, 16, 21, 0.68)`) que se torna opaca al interactuar o enfocar (`rgba(13, 16, 21, 0.94)`).
6. **Mascota guía Argentinosaurus:** Integración de la ilustración original estilizada `frontend/assets/argentinosaurus-guia.png` (512×512 px, canal alfa transparente), con animación de respiración sutil en CSS (`@keyframes dinoBreathe`), globos de diálogo concisos (15–30 palabras) ajustados reactivamente al capítulo y filtros, botón de alternancia `#btn-toggle-dino` con persistencia en `sessionStorage` y nota de respaldo compacta.

---

## 2. Comportamiento de Zoom y Control de Entrada de Rueda

### Diagnóstico Previo
En iteraciones anteriores, la función `setupScrollWheelNavigation()` interceptaba el evento `wheel` sobre el lienzo del mapa para saltar de capítulo. Esto impedía al usuario inspeccionar la topografía o los pozos mediante la rueda del ratón y provocaba saltos bruscos e involuntarios del relato.

### Solución Implementada
- **Desactivación de navegación por rueda:** Se removió `setupScrollWheelNavigation()`. La cámara de MapLibre responde de forma nativa a la rueda del ratón y gestos de pinza en trackpads.
- **Aislamiento de scroll en paneles (`setupPanelWheelIsolation`):** Se capturan los eventos `wheel` dentro de los paneles `#active-story-card`, `#chart-overlay-panel`, `#layer-selector-popup` y la barra de filtros, ejecutando `e.stopPropagation()` para evitar que el desplazamiento de listas o gráficos active el zoom del mapa de fondo.
- **Pausa automática del relato continuo:** Cuando el relato automático está en curso (`appState.isAutoTourActive`), cualquier interacción manual del usuario en el lienzo del mapa (`movestart`, arrastre o zoom manual) pausa inmediatamente la reproducción automática, devolviendo el botón a su estado inactivo para evitar desorientación espacial.

---

## 3. Miniaturas Fotográficas Progresivas y Modal de Inspección

### Estrategia de Representación Multiescala
| Rango de Zoom | Capas Activas | Comportamiento Visual |
|---|---|---|
| **Zoom < 7.0** (Nacional / Regional) | Puntos GPU WebGL (`wells-point-glow`, `wells-point-core`) | Puntos luminosos codificados por color (shale turquesa `#00E5FF`, convencional ámbar `#FFB300`). Densidad panorámica sin sobrecarga. |
| **Zoom >= 7.0** (Local / Yacimiento) | Capa WebGL atenuada + Pines HTML Circulares (`.map-photo-pin`) | Marcadores circulares con miniatura fotográfica de 44×44 px, halo dorado `#E5A93C`, efecto hover escalable a 50×50 px y etiqueta de yacimiento. |

### Inventario Fotográfico Verificado
| ID | Recurso / Instalación | Coordenadas | Autoría | Licencia | Procedencia Verificada |
|---|---|---|---|---|---|
| **F-01** | Aguada Pichana («Petrosaurios») | `[-68.788, -38.354]` | Horacio Fernandez | CC BY 3.0 | Wikimedia Commons (Panoramio) |
| **F-02** | Refinería YPF La Plata | `[-57.915, -34.872]` | KehDon | CC BY-SA 4.0 | Wikimedia Commons |
| **F-03** | Pozos Petroleros Lunlunta | `[-68.825, -33.055]` | Sergio D. Solier | CC BY-SA 4.0 | Wikimedia Commons |
| **F-04** | Yacimiento Los Perales | `[-68.980, -46.520]` | Marcelo Brandi | CC BY 3.0 | Wikimedia Commons (Panoramio) |
| **F-05** | Luces Nocturnas en Añelo | `[-68.785, -38.350]` | Sergio D. Solier | CC BY-SA 4.0 | Wikimedia Commons |
| **G-01** | Argentinosaurus Guía de Datos | — | Equipo del Proyecto | Proyecto (Propio) | Generación asistida con alfa transparente |

### Diálogo Modal `#photo-detail-modal`
Al hacer clic en cualquiera de las miniaturas fotográficas:
- Se abre una ventana modal con fondo oscurecido (`backdrop-filter: blur(8px)`).
- Muestra la imagen fotográfica en resolución optimizada, título del yacimiento, contexto técnico-histórico, autoría formal, enlace a la licencia y vínculo a la ficha original de Wikimedia Commons.
- Dispone de cierre mediante botón accesible `✕`, tecla `Escape` o clic fuera del contenedor.

---

## 4. Tipografía Bipolar: Alegreya + Archivo

Siguiendo las mejores directrices de diseño editorial y cartográfico, la plataforma descartó mezclas heterogéneas y unificó todos los textos en exactamente dos familias complementarias:

1. **Alegreya (Serif Editorial Clásica):**
   - **Aplicación:** Título principal de portada (`.hero-title`), subtítulo (`.hero-subtitle`) y títulos de los 7 capítulos (`.column-story-title`).
   - **Personalidad:** Evoca las grandes publicaciones editoriales, atlas geográficos y crónicas históricas argentinas.
2. **Archivo (Grotesque Sans-Serif Moderna & Tabular):**
   - **Aplicación:** Subtítulos, cuerpo de texto del relato, globos de diálogo del guía, barra de filtros, botones, etiquetas de ejes, cifras tabulares en KPIs y leyendas de micrográficos de Chart.js.
   - **Personalidad:** Geometría neutra, excelente legibilidad en pantallas táctiles y renderizado perfecto de números en columnas alineadas.

### Respaldo Local WOFF2 y Licencias OFL
- Archivos descargados en `frontend/fonts/`:
  - `alegreya-v35-latin-regular.woff2` (y variante 700)
  - `archivo-v19-latin-regular.woff2` (y variante 600)
- Definición de fallback local en `frontend/fonts_local.css`.
- Archivos de licencia Open Font License preservados: `frontend/fonts/OFL_Alegreya.txt` y `frontend/fonts/OFL_Archivo.txt`.
- Chart.js configurado con `Chart.defaults.font.family = "'Archivo', sans-serif"` y re-renderizado al resolverse `document.fonts.ready`.

---

## 5. Argentinosaurus como Guía del Relato y Panel Izquierdo

### Integración Visual de la Mascota
- **Archivo:** `frontend/assets/argentinosaurus-guia.png` (512×512 px, 242 KB, fondo transparente).
- **Animación CSS (`dinoBreathe`):**
  ```css
  @keyframes dinoBreathe {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-3px) scale(1.02); }
  }
  ```
  Se desactiva automáticamente ante la preferencia del sistema `@media (prefers-reduced-motion: reduce)`.

### Globos de Diálogo Sintéticos y Rigor Editorial
El bloque de texto largo y estático del panel izquierdo fue reemplazado por la explicación directa del dinosaurio en un globo de diálogo con pico estilizado.
- **Extensión controlada:** Entre 15 y 30 palabras por intervención.
- **Rigor de datos:**
  - En el Capítulo 01 explicita: *«En 2025 alcanzamos 46.438,5 miles de m³, la mayor extracción en 26 años. No es récord histórico absoluto porque 1998 fue mayor, pero Vaca Muerta cambió toda la curva.»*
  - En el Capítulo 03 detalla el cruce histórico: *«En noviembre de 2023 el no convencional superó por primera vez al convencional (51,1%). En 2025 ya explicó el 62,9% del crudo nacional.»*
  - Responde de forma reactiva al cambio de unidades (m³ / bpd) y a los filtros de cuenca y recurso.

### Control de Visibilidad y Respaldo
- **Botón `#btn-toggle-dino`:** Ubicado en la cabecera del panel junto al botón de colapsar. Permite ocultar la mascota si el usuario prefiere una lectura sobria.
- **Persistencia:** Almacena la preferencia del usuario en `sessionStorage.getItem('petroleo_dino_visible')`.
- **Nota compacta de respaldo (`#dino-fallback-note`):** Cuando el dinosaurio está oculto, el texto explicativo se muestra en una tarjeta compacta sin el gráfico del personaje.

---

## 6. Pruebas y Validación Automatizada

Se ejecutaron dos baterías completas de pruebas automatizadas:

### 1. Script de Interacción Selenium Headless (`scratch/test_v9_features.py`)
- **Resolución Desktop (1920×1080):**
  - Carga sin errores severos de consola (0 errores).
  - Tipografía computada: `Alegreya` en `.hero-title` y `Archivo` en `body`.
  - Créditos de portada con 2 enlaces activos a Wikimedia Commons y CC BY 3.0.
  - Clic en inicio y transición suave a Capítulo 01.
  - Carga verificada de la imagen del Argentinosaurus (`naturalWidth > 0`).
  - Prueba de scroll wheel en canvas: el mapa recibe el evento y el capítulo permanece en `01`.
  - Prueba de alternancia del botón del guía: toggle a oculto muestra `#dino-fallback-note`.
  - Prueba de marcadores fotográficos progresivos: 5 pines registrados en MapLibre; a zoom 9.0 sobre Añelo son visibles 2 pines; clic abre `#photo-detail-modal` con foto, autoría y licencia.
- **Resolución Mobile (390×844):**
  - Adaptabilidad responsiva del globo y la mascota sin desbordamientos de pantalla.

### 2. Suite Completa Pytest (`tests/test_platform.py`)
```text
tests/test_platform.py::test_static_data_files_exist PASSED              [  2%]
tests/test_platform.py::test_historical_peak_1998_and_2025_expansion_metric PASSED [  5%]
tests/test_platform.py::test_shale_share_62_92_pct PASSED                [  8%]
tests/test_platform.py::test_crossover_november_2023 PASSED              [ 11%]
tests/test_platform.py::test_pareto_top_milestones PASSED                [ 14%]
tests/test_platform.py::test_pareto_912_wells_explain_50_pct PASSED      [ 17%]
tests/test_platform.py::test_endpoints_cohortes PASSED                   [ 20%]
tests/test_platform.py::test_endpoints_macro PASSED                      [ 23%]
tests/test_platform.py::test_charts_data_non_empty PASSED                [ 26%]
tests/test_platform.py::test_geo_trajectories_validity PASSED            [ 29%]
tests/test_platform.py::test_geo_pipelines_connectivity PASSED           [ 32%]
tests/test_platform.py::test_api_endpoints_live PASSED                   [ 35%]
tests/test_platform.py::test_carto_config_and_fallback_style PASSED      [ 38%]
tests/test_platform.py::test_pareto_api_endpoint_and_milestones PASSED   [ 41%]
tests/test_platform.py::test_v4_v5_dom_structure PASSED                  [ 44%]
tests/test_platform.py::test_v4_v5_css_overlay_and_filter_styling PASSED [ 47%]
tests/test_platform.py::test_v4_v5_app_js_state_and_chapter05_stacked_charts PASSED [ 50%]
tests/test_platform.py::test_v6_seven_chapters_and_synthesis_removed PASSED [ 52%]
tests/test_platform.py::test_v7_simplified_masthead_and_compact_layer_controls PASSED [ 55%]
tests/test_platform.py::test_v7_translucent_reactive_overlay_styling PASSED [ 58%]
tests/test_platform.py::test_v7_islas_malvinas_cartography PASSED        [ 61%]
tests/test_platform.py::test_v7_absence_of_false_record_claims_and_explicit_units PASSED [ 64%]
tests/test_platform.py::test_v6_reserved_right_rail_and_overlay_spacing PASSED [ 67%]
tests/test_platform.py::test_v6_unified_panel_design_tokens PASSED       [ 70%]
tests/test_platform.py::test_v6_filter_bar_labels_and_reset_view PASSED  [ 73%]
tests/test_platform.py::test_v8_app_js_syntax_balance PASSED             [ 76%]
tests/test_platform.py::test_v8_hero_photographic_assets_and_credits PASSED [ 79%]
tests/test_platform.py::test_v8_hero_splash_accessibility_and_focus PASSED [ 82%]
tests/test_platform.py::test_v8_headless_browser_entry_regression PASSED [ 85%]
tests/test_platform.py::test_v9_typography_two_families_only PASSED      [ 88%]
tests/test_platform.py::test_v9_no_scroll_wheel_navigation PASSED        [ 91%]
tests/test_platform.py::test_v9_dino_guide_and_left_panel PASSED         [ 94%]
tests/test_platform.py::test_v9_photo_inventory_and_progressive_markers PASSED [ 97%]
tests/test_platform.py::test_v9_hero_photo_credits_active_links PASSED   [100%]

============================= 34 passed in 11.46s =============================
```

---

## 7. Galería de Verificación Visual

A continuación se presentan las capturas de pantalla obtenidas directamente del navegador en ejecución:

- **Portada Editorial con Crédito Enlazado y Tipografía Alegreya:**  
  [`v9_desktop_portada.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/screenshots/v9_desktop_portada.png)
- **Capítulo 01 con Guía Argentinosaurus y Panel Izquierdo Reactivo:**  
  [`v9_desktop_capitulo01_dino.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/screenshots/v9_desktop_capitulo01_dino.png)
- **Inspección de Foto Progresiva a Zoom 9.0 con Modal de Detalle:**  
  [`v9_desktop_zoom_fotomodal.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/screenshots/v9_desktop_zoom_fotomodal.png)
- **Vista Móvil (390×844) del Recorrido y Mascota Guía:**  
  [`v9_mobile_capitulo01_dino.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/screenshots/v9_mobile_capitulo01_dino.png)

---

## 8. Conclusión

La Iteración V9 consolida la plataforma en sus facetas más delicadas: la libertad de exploración cartográfica sin interferencias, la trazabilidad documental de sus fotografías reales, la armonía y jerarquía de sus fuentes y una mediación pedagógica atractiva y científicamente rigurosa a través del Argentinosaurus. El sistema se encuentra en estado óptimo de despliegue y producción.
