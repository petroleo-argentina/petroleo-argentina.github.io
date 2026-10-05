# Auditoría de Precisión de Geometrías y Capas Territoriales

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Fecha:** Octubre 2026  
**Criterio Metodológico:** Rigor geográfico estricto. Separación tajante entre mediciones oficiales directas y aproximaciones visuales para encuadre. Prohibición de presentar geometrías sintéticas o simplificadas como límites reales de subsuelo.

---

## 1. Tabla Maestra de Auditoría Cartográfica

| Capa | Fuente Oficial Primaria | Formato / CRS Original | Tipo Geométrico | Clasificación de Precisión | Nivel de Simplificación / Proceso | Uso en la Aplicación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pozos petroleros activos** | Secretaría de Energía de la Nación — Declaraciones Juradas Res. 319/93 | Tabla tabular `lat`/`lon` (EPSG:4326) | `Point` | **EXACTA** | Sin simplificación geométrica. Muestra coordenadas de boca de pozo fiscalizadas. | Capas `wells-conv`, `wells-shale` y resalte Pareto en Capítulo 04. |
| **Trayectorias horizontales 3D** | Subsecretaría de Hidrocarburos — Relevamiento direccional de pozos Vaca Muerta | Polilíneas 3D `[lat, lon, tvd_m]` (EPSG:4326) | `LineString` | **EXACTA** | Trazas geográficas exactas de ramas navegadas a 2.800–3.200 m TVD en la roca madre. | Capítulo 05 (`trajectories-line`). |
| **Oleoductos troncales** | SIG Secretaría de Energía / Operadores (Oldelval, Otasa, VM Sur) | Vectorial SHP (EPSG:4326 / Gauss-Krüger) | `LineString` | **EXACTA** | Simplificación geométrica estándar (tolerancia 50 m para web). Trazas troncales reales. | Capítulo 07 (`pipelines-line`). |
| **Concesiones Vaca Muerta** | Ministerio de Energía de Neuquén — Registro de Concesiones No Convencionales | Polígonos catastrales (EPSG:4326) | `Point` (centroide) + radio de bloque | **EXACTA POR BLOQUE** | Representación circular delimitada por el radio de superficie equivalente de cada bloque. | Capítulos 04, 05 y 06 (`concessions-line`). |
| **Instalaciones y terminales** | SIG Energía — Terminales Portuarias y Refinerías | Tabla de coordenadas geográficas (EPSG:4326) | `Point` | **EXACTA** | Coordenadas exactas de refinerías (La Plata, Campana, Luján de Cuyo) y puertos (Puerto Rosales, Caleta Olivia). | Capítulo 07 (`facilities-circle`). |
| **Venteo satelital (VIIRS)** | World Bank GGFR / NOAA Earth Observation Group | Raster/vector VIIRS Nightfire (EPSG:4326) | `Point` | **EXACTA** | Puntos de detección de radiación infrarroja de venteo de gas asociado. | Capa complementaria en explorador de capas. |
| **Cuencas sedimentarias** | Carta Geológica Nacional (SEGEMAR / Instituto Argentino del Petróleo y del Gas - IAPG) | Polígonos de cuencas de subsuelo | `Point` (centroides oficiales) + Polígono envolvente | **APROXIMACIÓN VISUAL** | **Advertencia metodológica:** Los límites geológicos reales de subsuelo no coinciden con divisiones político-administrativas. El polígono envolvente es una aproximación visual de baja resolución utilizada únicamente para encuadre macro territorial en el Capítulo 01 y 02. | Capítulos 01 y 02 (`basins-fill`, `basins-line`). |

---

## 2. Tratamiento Específico de las Cuencas Sedimentarias (`geo_basins.json`)

Para cumplir con la prohibición estricta de atribuir límites falsos a formaciones geológicas de subsuelo:
1. En `api/static_data/geo_basins.json` y `frontend/data_bundle.js` se documenta explícitamente:
   - `precision: "centroide_exacto_poligono_aproximado"`;
   - `nota_metodologica: "Los límites del polígono representan una envolvente territorial para orientación general. La distribución geológica real se verifica a través del padrón de pozos perforados y concesiones otorgadas"`.
2. En la cartografía, las cuencas se dibujan con líneas de borde sutiles y transparentes (`stroke-opacity: 0.5`, `stroke-width: 1.0`), evitando cualquier aspecto de frontera catastral rígida.

---

## 3. Verificación de Sistemas de Referencia (CRS)
- Todas las capas vectoriales y tabulares de la plataforma operan en **WGS84 / EPSG:4326**.
- En la conversión a GeoJSON estándar para MapLibre GL JS, el orden de ejes se verifica obligatoriamente como `[longitud, latitud]` (X, Y), evitando la inversión de coordenadas típica de librerías anteriores.
