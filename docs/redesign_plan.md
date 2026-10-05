# Plan de Rediseño e Implementación Técnica del Frontend

**Fecha de ejecución:** Octubre 2026  
**Documento de referencia:** [`reordenamiento_y_redisenio_petroleo_argentina.md`](file:///c:/Users/ESCRITORIO/Downloads/reordenamiento_y_redisenio_petroleo_argentina.md)  
**Sistema de diseño:** [`DESIGN.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/DESIGN.md)

---

## 1. Objetivos del Rediseño

1. **Reordenar los capítulos** según la nueva estructura de 8 partes fundamentada en los datos auditados.
2. **Corregir los 3 gráficos desfasados** en el código JavaScript:
   - Capítulo 03: `setupCrossoverMicroChart`
   - Capítulo 06: `setupCohortsMicroChart`
   - Capítulo 07: `setupMacroTradeMicroChart`
3. **Erradicar definitivamente la apariencia SaaS / Dashboard corporativo**:
   - Eliminar tarjetas anidadas, bordes gruesos y cajas con iconos decorativos.
   - Transformar los Big Numbers en tipografía pura (`Newsreader` en marfil/ámbar sobre fondo oscuro) sin contenedores pesados.
   - Diseñar una portada de bienvenida (*Hero / Splash*) limpia con mapa cenital, título de gran tamaño y llamada a la acción ("Comenzar el recorrido").
4. **Implementar el momento memorable de Pareto (Capítulo 04)**:
   - Resaltar la relación `912 pozos = 50% de la producción` frente al universo total de 26.219 pozos.
   - Efecto en mapa que atenúa los pozos de baja producción y focaliza el cúmulo central de Vaca Muerta.
5. **Garantizar rendimiento de renderizado**:
   - Mapas y animaciones con tasa >= 50 FPS en desktop.
   - Sin saturación del árbol DOM.

---

## 2. Mapa de Archivos a Modificar

| Archivo | Rol | Modificaciones Planificadas |
|---|---|---|
| [`frontend/index.html`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.html) | Estructura | Agregar pantalla de bienvenida (*Hero Splash*), reorganizar navegación a los 8 capítulos y refinar modal de preguntas. |
| [`frontend/index.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.css) | Estilos | Aplicar tokens de `DESIGN.md`, tipografía Newsreader/Inter, estilos para Big Numbers sin cajas, lienzo de mapa 2.5D y paneles ultrafinos. |
| [`frontend/app.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/app.js) | Lógica & Datos | Actualizar definición de capítulos 1 al 8, corregir mapeo de propiedades en Chart.js, integrar lógica de portada y animación Pareto. |
| [`tests/test_platform.py`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/tests/test_platform.py) | Pruebas | Agregar 7 nuevos tests unitarios y de integración para validar hitos auditados y gráficos no vacíos. |

---

## 3. Plan Paso a Paso de Ejecución

- [x] **Paso 1:** Crear `DESIGN.md` y `docs/reordenamiento_capitulos.md`.
- [x] **Paso 2:** Crear `docs/redesign_plan.md` y actualizar `docs/historia_visual.md`.
- [x] **Paso 3:** Corregir y reordenar `frontend/app.js`:
  - Corrección de gráficos 03, 06 y 07.
  - Actualización de textos, títulos narrativos y números auditados.
  - Implementación de la vista Pareto y portada inicial.
- [x] **Paso 4:** Actualizar `frontend/index.html` e `frontend/index.css` conforme al sistema de diseño.
- [x] **Paso 5:** Ampliar `tests/test_platform.py` con las validaciones obligatorias de la Sección 31.
- [x] **Paso 6:** Ejecutar suite completa con pytest y verificar integridad del servidor (12/12 tests pasando).
- [x] **Paso 7 (Ajuste Cartográfico y Editorial V2):**
  - Migración completa de Leaflet a **MapLibre GL JS v4.7.1** con WebGL acelerado por GPU.
  - Terreno 3D real con Raster-DEM Terrarium AWS (exageración 1.25) y sombreado Hillshade analítico.
  - Cámara con pitch y bearing adaptativos por escala geográfica.
  - Rediseño de la navegación derecha a un **recorrido cartográfico visual continuo (Journey Tracker)** con camino SVG.
- [x] **Paso 8 (Iteración Cartográfica V3 — CARTO autenticado & MapLibre 3D):**
  - Integración segura de CARTO API Token vía `frontend/config.example.js` y `frontend/config.js` (ignorado en `.gitignore`).
  - Eliminación definitiva del watermark `API KEY REQUIRED` sin recurrir a trucos de CSS.
  - Construcción del estilo vectorial de respaldo [`frontend/styles/petroleo-map-style.json`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/styles/petroleo-map-style.json) con paleta sobria de relieve (agua `#13212A`, tierra baja `#262720`, meseta `#34352C`, elevación `#504C40`, relieve alto `#706856`).
  - Terreno 3D optimizado con exageración DEM a `1.22` e iluminación Hillshade a `315°`.
  - Simplificación de encabezados a formato unilínea (`01   ARGENTINA · 1950—2025`, etc.).
  - Reducción del ancho del panel narrativo a `320px` para una experiencia nítidamente map-first (>75% del viewport).
  - Soporte y evaluación A/B de doble stack tipográfico: Stack A (`Newsreader` + `Inter` + `JetBrains Mono`) vs Stack B (`Archivo` + `IBM Plex Mono`).
  - Auditoría formal de precisión de geometrías en [`docs/auditoria_geometrias.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/auditoria_geometrias.md).
  - Suite de pruebas automatizadas actualizada a 13/13 tests pasando con pytest.

