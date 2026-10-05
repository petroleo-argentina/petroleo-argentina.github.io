# Informe de Implementación — Iteración V10: Iconos de Pozos, Guía Dino Contextual y Tipografía Variable

**Fecha:** 2026-10-04  
**Proyecto:** Plataforma Interactiva «Petróleo en Argentina: 1950–2025»  
**Documento base:** `iteracion_v10_iconos_pozos_dino_contextual.md`  
**Estado:** ✅ Implementado y verificado (34/34 tests superados, 100%)

---

## 1. Resumen de Correcciones Implementadas

En cumplimiento estricto con los lineamientos de la **Iteración V10**, se corrigieron las desviaciones introducidas en iteraciones previas respetando la coherencia editorial, cartográfica y técnica del proyecto:

1. **Pozos en el mapa (sustitución de fotos por iconos de bombeo mecánico):**
   - Se eliminaron por completo los marcadores HTML circulares con fotos recortadas (`.map-photo-pin`) y el diálogo modal fotográfico `#photo-detail-modal`.
   - Se incorporó el pictograma original generado para el proyecto (`icono-pozo-petrolero.png`, 1254×1254 px) y se preparó una versión optimizada retina [`frontend/assets/icono-pozo-petrolero-opt.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/assets/icono-pozo-petrolero-opt.png) (96×96 px, fondo transparente, anclaje en la base y halo de contraste).
   - Se implementó como capa nativa WebGL de MapLibre (`wells-icons` de tipo `symbol` sobre `wells-source`) con filtro de zoom mínimo (`minzoom: 7.0`), interpolación suave de escala (`icon-size: 0.22` a `0.45`), anclaje inferior (`icon-anchor: 'bottom'`) y atenuación de opacidad.
   - A escala lejana (zoom < 7) los pozos se mantienen representados por sus puntos vectoriales con pedestal/halo coloreado según recurso (`#39AFCF` no convencional / shale y `#C98B32` convencional).
   - La interacción de clic (tanto sobre el punto como sobre el icono) abre la **ficha técnica-analítica estándar** en popup (`sigla`, `empresa`, `yacimiento`, `tipo_recurso`, `anio_primera_prod` y producción anual estimada).
   - La foto panorámica de portada de Vaca Muerta y su crédito verificado se mantienen intactos.

2. **Dinosaurio fuera del panel superior:**
   - Se trasladó el Argentinosaurus fuera de `#active-story-card`, suprimiendo los contenedores internos `#dino-guide-stage` y `#dino-fallback-note`.
   - Se implementó como componente flotante independiente abajo a la izquierda (`#dino-guide-floating`), ubicado en `left: 24px; bottom: 84px` (desktop) con elevación visual (`z-index: 45`).
   - Se incorporó botón de cierre/colapso (`#btn-toggle-dino`), botón de píldora de reapertura (`#btn-dino-pill`), y persistencia del estado en `sessionStorage`.
   - En caso de solapamiento visual con popups de pozos, se programó una regla de atenuación reactiva (`.dino-popup-active`) que reduce la opacidad al 25% y desactiva eventos del puntero mientras el popup está abierto.

3. **Contenido complementario, no repetido:**
   - La tarjeta superior izquierda (`#active-story-card`) presenta el hallazgo principal del capítulo con su título editorial (`.story-headline`) y su bajada analítica (`.story-lead`), utilizando `chapter.getInsight(appState)`.
   - El globo del dinosaurio (`#dino-speech-bubble`) presenta conceptos metodológicos complementarios según la Sección 5 de la especificación:
     - **Capítulo 01:** *«El volumen anual suma todo lo producido en el año. El promedio diario reparte ese volumen entre sus días.»*
     - **Capítulo 02:** *«Una región puede ganar participación aunque otra siga produciendo más. Compará porcentajes y volúmenes para distinguir esos cambios.»*
     - **Capítulo 03:** *«Convencional y no convencional describen cómo están alojados los hidrocarburos y cómo se extraen. Ambos son recursos naturales.»*
     - **Capítulo 04:** *«Ordenar los pozos por producción permite ver cuánto aporta un grupo pequeño al total. El resultado depende del período elegido.»*
     - **Capítulo 05:** *«Longitud lateral y etapas de fractura son medidas distintas. Compararlas no demuestra, por sí solo, cuál causa un cambio de producción.»*
     - **Capítulo 06:** *«Una cohorte reúne pozos que comenzaron en un período similar. Compararlos a la misma edad ayuda a distinguir generaciones.»*
     - **Capítulo 07:** *«Antes de comparar valores económicos, fijate en la moneda, el período y si están ajustados por inflación.»*
   - Se resolvió definitivamente la duplicación en Cohortes (Panel: «Generaciones de pozos» vs. Dinosaurio: concepto de cohorte y comparación a misma edad).

4. **Tipografía variable legítima:**
   - Se conservaron las dos familias tipográficas: **Alegreya** (titulares, serif humanista) y **Archivo** (cuerpo, datos, UI y monoespaciado técnico).
   - Se eliminaron los archivos estáticos clonados artificialmente y se instalaron los archivos variables oficiales de Google Fonts en [`frontend/fonts/`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/fonts/):
     - `alegreya-variable-normal-latin.woff2` (43 KB, wght 400..900)
     - `alegreya-variable-italic-latin.woff2` (44 KB, wght 400..900)
     - `archivo-variable-normal-latin.woff2` (35 KB, wght 100..900)
     - `archivo-variable-italic-latin.woff2` (39 KB, wght 100..900)
   - Se actualizó [`frontend/fonts_local.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/fonts_local.css) con descriptores `font-weight: 400 900;` y `font-weight: 100 900;`, eliminando redundancias sintéticas.

---

## 2. Registro de Archivos Modificados

| Archivo | Tipo de Cambio | Descripción |
|---|---|---|
| [`frontend/assets/icono-pozo-petrolero-opt.png`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/assets/icono-pozo-petrolero-opt.png) | Creación / Optimización | Pictograma de equipo de bombeo optimizado a 96×96 px con transparencia y halo de contraste |
| [`frontend/fonts/`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/fonts/) | Limpieza y reemplazo | Subsets variables oficiales de Alegreya y Archivo (`normal` e `italic`) |
| [`frontend/fonts_local.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/fonts_local.css) | Modificación | Reglas `@font-face` con rangos variables legítimos |
| [`frontend/index.html`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.html) | Refactorización DOM | Eliminados `#dino-guide-stage`, `#dino-fallback-note` y `#photo-detail-modal`. Añadido `#dino-guide-floating` independiente |
| [`frontend/index.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.css) | Estilos | Reglas para guía flotante, píldora colapsada, `.dino-popup-active` y `.editorial-well-popup` |
| [`frontend/app.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/app.js) | Lógica interactiva | Registro de `well-pump-icon`, capa `wells-icons`, textos conceptuales V10, toggle independiente y ficha analítica |
| [`tests/test_platform.py`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/tests/test_platform.py) | Suite de pruebas | Incorporación de tests V10 (fuentes variables, guía dino independiente y capa de iconos de pozos) |

---

## 3. Verificación Automatizada y Evidencias Visuales

1. **Pruebas de Integración y Regresión:**
   ```bash
   python -m pytest tests/test_platform.py -v
   ============================= 34 passed in 12.07s =============================
   ```
   - 34 pruebas ejecutadas, **100% exitosas**, 0 fallos.

2. **Pruebas E2E en Navegador Headless (Microsoft Edge):**
   - `scratch/test_v10_features.py` ejecutó los 9 pasos de verificación completa:
     - 0 errores severos de consola.
     - Tipografía computada: `Alegreya` en titulares y `Archivo` en cuerpo/UI.
     - Separación espacial comprobada: `#active-story-card` contiene titular + lead y **0** elementos de dino adentro.
     - Elemento flotante `#dino-guide-floating` activo e independiente abajo a la izquierda.
     - Textos conceptuales verificados en Ch01 y Ch06 (cero repetición de titulares).
     - Comprobada capa `wells-icons` con `well-pump-icon` registrado.
     - Ausencia total de marcadores `.map-photo-pin` y diálogo `#photo-detail-modal`.
     - Ficha técnica-analítica emergente comprobada con datos de operador, yacimiento, tipo y producción.
     - Atenuación de guía dino (`.dino-popup-active`) validada durante apertura de popup.
     - Botón de alternancia y píldora con persistencia en `sessionStorage` verificados.
     - Vista responsive mobile (390×844) verificada.
