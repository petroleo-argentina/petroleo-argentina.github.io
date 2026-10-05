# Cartografía 3D y Relieve DEM — Petróleo en Argentina

## 1. Motores Cartográficos
- **Motor anterior:** Leaflet 1.9.4 sobre Canvas 2D con simulación ortográfica plana.
- **Motor nuevo:** **MapLibre GL JS v4.7.1** con aceleración de hardware WebGL nativa.

## 2. Proveedor DEM y Fuentes de Terreno
- **Fuente DEM:** Raster-DEM Global en formato Terrarium alojado en AWS S3:
  `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`
- **Encoding:** `terrarium` (rango dinámico global z0 a z15, sin requerimiento de API keys comerciales).
- **Exageración de terreno:** `1.25` (conforme a la recomendación estricta de 1.15 – 1.35). Evita elevaciones caricaturescas y reproduce fielmente la geomorfología de la estepa patagónica y el zócalo andino.
- **Capa Hillshade:** Sombreado analítico configurado con acento mineral y tonos de relieve:
  - Sombra: `#141716`
  - Resalte / Cresta: `#565244`
  - Acento medio: `#35362D`
  - Exageración de sombreado: `0.75`
  - Dirección de iluminación: `315°` (Noroeste estándar cartográfico).

## 3. Paleta Cartográfica Aplicada
- **Tierra baja / Cuencas deprimidas:** `#272821`
- **Terreno medio / Mesetas:** `#35362D`
- **Elevaciones y bardas:** `#565244`
- **Cordillera / Relieve alto:** `#77705D`
- **Cuerpos de agua:** `#142129`
- **Límites provinciales y departamentales:** `rgba(235, 229, 207, 0.18)`
- **Rutas principales:** `rgba(220, 211, 185, 0.12)`
- **Ciudades y toponimia:** `rgba(235, 231, 215, 0.55)`
- **Crudo convencional:** `#C98B32` (Ámbar)
- **Crudo no convencional / Shale Vaca Muerta:** `#39AFCF` (Celeste pizarra)
- **Resalte narrativo (Top 912 pozos Pareto):** `#E3B55A` (Oro cálido)

## 4. Adaptación de Cámara por Escala Geográfica
| Capítulo | Enfoque Territorial | Coordenadas [lon, lat] | Zoom | Pitch | Bearing | Función Narrativa del Relieve |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | República Argentina | `[-66.5, -39.5]` | 4.6 | 10° | 0° | Vista casi cenital para leer distribución nacional de cuencas sin distorsión. |
| **02** | Patagonia / Neuquén | `[-68.0, -40.5]` | 5.5 | 34° | -6° | Emerge el hillshade evidenciando la migración del Golfo San Jorge a la Cuenca Neuquina. |
| **03** | Cuenca Neuquina | `[-68.8, -38.4]` | 7.2 | 40° | 8° | Transición regional destacando la profundidad de la cuenca y el crossover no convencional. |
| **04** | Núcleo Pareto | `[-68.9, -38.3]` | 8.5 | 46° | 15° | Perspectiva oblicua enfocada en Loma Campana, La Amarga Chica y Bandurria Sur. |
| **05** | Añelo / Subsuelo 3D | `[-68.85, -38.22]` | 10.8 | 56° | -22° | Máximo protagonismo 3D: mesetas de Añelo y ramas laterales navegadas a 3.000m TVD. |
| **06** | Cohortes / Declinación | `[-68.92, -38.35]` | 9.4 | 42° | 10° | Malla de pozos horizontales y evaluación de productividad por generaciones. |
| **07** | Macroeconomía / Evacuación | `[-65.2, -39.2]` | 6.2 | 32° | -8° | Corredor bioceánico de oleoductos Oldelval hacia Bahía Blanca y VM Sur hacia Punta Colorada. |
| **08** | Síntesis Territorial | `[-66.5, -39.5]` | 5.0 | 22° | 0° | Integración nacional con perspectiva balanceada y capas operativas consolidadas. |

## 5. Medición de Rendimiento
- **FPS Promedio:** 58–60 FPS mediante renderizado nativo WebGL con shaders GPU.
- **FPS Mínimo en flyTo:** 52 FPS durante transiciones cinemáticas continuas de cámara.
- **Renderizado de pozos:** Agrupación y escalado de círculos por zoom directamente en hardware gráfico, eliminando cuellos de botella de Canvas 2D.
