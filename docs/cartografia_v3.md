# Cartografía V3 — MapLibre GL 3D, Basemap Vectorial y Relieve Analítico

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Iteración:** V3 (Refinamiento Cartográfico y Arquitectura Robusta)  
**Fecha:** Octubre 2026

---

## 1. Diagnóstico y Eliminación del Watermark `API KEY REQUIRED`

### Causa Raíz Identificada
El mapa anterior solicitaba teselas raster directamente a `https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}@2x.png` sin un parámetro de API Key ni token de sesión. La infraestructura actual de CARTO intercepta estas peticiones anónimas y devuelve imágenes pre-estampadas con la advertencia:
```text
API KEY REQUIRED
carto.com/basemaps/apikey
```

### Solución Implementada
1. **Soporte Autenticado con Token Privado:** Si existe [`frontend/config.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/config.js) con un `CARTO_TOKEN` válido, las peticiones incluyen el parámetro `?api_key=${window.APP_CONFIG.CARTO_TOKEN}` o se canalizan por la Maps API correspondiente.
2. **Estilo Vectorial Propio como Fallback Automático:** Si `CARTO_TOKEN` no está configurado o el servicio devuelve un código no 200, MapLibre GL carga de inmediato:
   `./styles/petroleo-map-style.json`
   Este estilo consume teselas vectoriales OpenMapTiles / OpenFreeMap (`https://tiles.openfreemap.org/planet`) sin requerir API keys, completamente limpio, sin watermarks y con la paleta mineral del proyecto.

---

## 2. Comparativa de Fuentes DEM (Elevación 3D)

| Parámetro | Opción A: AWS Terrarium (Seleccionada) | Opción B: MapLibre Demo DEM / Mapterhorn | Evaluación en Territorio Argentino |
| :--- | :--- | :--- | :--- |
| **Fuente URL** | `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png` | `https://demotiles.maplibre.org/terrain-tiles/{z}/{x}/{y}.png` | AWS Terrarium dispone de cobertura global continua a zooms de meseta (z0 a z15). |
| **Encoding** | `terrarium` (MapLibre nativo) | `mapbox` (RGB) | Terrarium procesa elevaciones negativas y fosas oceánicas con mayor fidelidad. |
| **Respuesta en Cordillera y Vaca Muerta** | Excelente resolución en las bardas de Añelo y el talud de la Cuenca Neuquina. | Menor densidad de detalle en escalas locales z10+. | AWS Terrarium reproduce con mayor nitidez las mesetas escalonadas de Neuquén. |
| **Exageración recomendada** | **1.22** | 1.30 | 1.22 equilibra la lectura geomorfológica sin crear pendientes irreales. |

---

## 3. Calibración del Sombreado Analítico (Hillshade)

Se evaluaron tres acimuts de iluminación para el relieve patagónico:
- **300° (Oeste-Noroeste):** Genera sombras demasiado extendidas hacia el Este que oscurecen la zona de pozos en Loma Campana.
- **315° (Noroeste Clásico - Seleccionado):** Iluminación óptima. Resalta la falla del frente andino y las mesetas del río Neuquén sin tapar la simbología de las locaciones petroleras.
- **330° (Nor-Noroeste):** Aplana ligeramente el contraste en los valles transversales de Río Negro y Chubut.

**Configuración final en el estilo:**
```json
{
  "id": "hills",
  "type": "hillshade",
  "source": "terrain-dem",
  "paint": {
    "hillshade-shadow-color": "#141716",
    "hillshade-highlight-color": "#565244",
    "hillshade-accent-color": "#34352C",
    "hillshade-exaggeration": 0.75,
    "hillshade-illumination-direction": 315
  }
}
```

---

## 4. Parámetros de Cámara por Capítulo

| Capítulo | Pitch (Inclinación) | Bearing (Rotación) | Zoom | Encuadre Territorial |
| :--- | :--- | :--- | :--- | :--- |
| **01 Argentina · 1950—2025** | **0° – 5°** | **0°** | 4.6 | Vista cenital nacional; orientación Norte estricta. |
| **02 Territorio · 2006—2025** | **18° – 24°** | **-5°** | 5.5 | Comienza a revelarse el relieve de la estepa patagónica. |
| **03 Producción · Nov 2023** | **30° – 36°** | **8°** | 7.2 | Transición oblicua enfocada en la Cuenca Neuquina. |
| **04 Concentración · 2025** | **36° – 42°** | **12°** | 8.5 | Foco angular en el clúster de los 912 pozos Pareto. |
| **05 Tecnología · 2015—2025** | **52° – 58°** | **-20°** | 10.8 | **Cúspide tridimensional:** mesetas de Añelo y ramas subterráneas 3D. |
| **06 Cohortes · 2015—2024** | **36° – 42°** | **8°** | 9.4 | Malla de pads y espaciamiento de pozos. |
| **07 Economía · 2007—2025** | **22° – 28°** | **-5°** | 6.2 | Corredor de evacuación Neuquén &rarr; Atlántico (Oldelval / VM Sur). |
| **08 Argentina · Síntesis** | **0° – 8°** | **0°** | 5.0 | Retorno a perspectiva balanceada para exploración libre. |

---

## 5. Diseño Map-First y Experiencia de Usuario
- **Ancho del panel izquierdo:** Reducido a **320 px** (objetivo 300–330 px). Esto libera más del 75% del ancho de pantalla para la cartografía en monitores estándar.
- **Anotaciones directas:** En lugar de párrafos explicativos fuera del mapa, los hallazgos se indican con callouts in-situ:
  - *Capítulo 02:* `NEUQUÉN: 20,4% → 64,7% de la producción nacional`.
  - *Capítulo 03:* `CROSSOVER NACIONAL: Noviembre 2023 (51,11% No Convencional)`.
  - *Capítulo 04:* `NÚCLEO PARETO: 912 pozos generan el 50%`.
  - *Capítulo 05:* `AÑELO 3D: 3.036 m de longitud lateral promedio`.
