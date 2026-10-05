# Registro de Decisiones de Arquitectura y Metodología (ADR)

Este documento registra las decisiones clave tomadas durante el diseño, ingestión, procesamiento y visualización de la plataforma.

---

## ADR 01: Paradigma Visual — Scrollytelling Cartográfico Inmersivo
- **Contexto:** El usuario solicitó explícitamente evitar dashboards genéricos o corporativos y adoptar un estilo similar a proyectos galardonados como *Milla 201* (`milla201.com`) y *649 Héroes* (`jsantarelli.github.io/649/public/`).
- **Decisión:** 
  1. El mapa interactivo ocupa el 100% de la pantalla (`100vw` $\times$ `100vh`) como lienzo espacial principal.
  2. El relato editorial se despliega en un cajón flotante de vidrio esmerilado (*glassmorphism*) en el margen izquierdo.
  3. Un stepper vertical a la derecha rastrea el progreso en 8 capítulos secuenciales.
  4. Los capítulos activan vuelos cinemáticos de cámara (`flyTo`) que van desde la visión nacional (75 años) hasta el nivel de subsuelo en Añelo (ramas horizontales a 3.000 m de profundidad) y las rutas de exportación hacia el Atlántico y el Pacífico.
- **Consecuencia:** Experiencia de usuario inmersiva, de calidad editorial y apta para competir en certámenes de periodismo y visualización de datos.

---

## ADR 02: Procesamiento Analítico Híbrido — DuckDB + Precomputación JSON
- **Contexto:** Los datos de producción mensual abarcan 17.775.911 filas entre 2006 y 2025. Enviar millones de filas al navegador congelaría la interfaz de usuario.
- **Decisión:**
  1. Usar **DuckDB** en local para procesar particiones Parquet, ejecutar agregaciones masivas, calcular percentiles de cohortes y auditar uniones relacionales.
  2. Generar vistas agregadas analíticas persistidas en Parquet (`data/processed/`) y serializar payloads JSON optimizados en `api/static_data/`.
  3. Muestrear de forma estratificada 4.000 pozos representativos (cubriendo las 5 cuencas y el 100% de los megayacimientos de Vaca Muerta) con sus coordenadas para el mapa temporal interactivo.
- **Consecuencia:** Respuestas HTTP instantáneas (<15 ms), cero carga innecesaria en el cliente y 60 fps constantes en el navegador.

---

## ADR 03: Motor Cartográfico — Leaflet con Renderizado Canvas
- **Contexto:** Renderizar 4.000 marcadores SVG individuales en el DOM genera sobrecarga de memoria y caídas de frames al desplazar el mapa.
- **Decisión:** Utilizar Leaflet 1.9.4 configurado con `preferCanvas: true` y un renderer `L.canvas()`. Combinarlo con el mapa base *CartoDB Dark Matter* para un contraste visual óptimo con los puntos cian (shale) y ámbar (convencional).
- **Consecuencia:** Fluidez en paneos y zooms, soporte para líneas de oleoductos y trayectorias 3D con tooltips interactivos e inspectores al hacer clic.

---

## ADR 04: Definición Operativa de "Pozo Activo"
- **Contexto:** En la literatura petrolera coexisten múltiples criterios para catalogar un pozo como activo (capacidad instalada, días con bomba encendida, etc.).
- **Decisión:** Se definió con rigor físico y trazable:
  $$\text{Activo}_t \iff (\text{prod\_pet}_{i,t} > 0) \lor (\text{prod\_gas}_{i,t} > 0)$$
  Si un pozo no produjo hidrocarburos en el mes $t$, se contabiliza como inactivo o cerrado.
- **Consecuencia:** Medición consistente y auditable a lo largo de los 240 meses analizados (2006-2025).

---

## ADR 05: Trazabilidad de Fuentes y Clasificación No Convencional
- **Contexto:** El plan prohíbe el uso de fuentes no verificadas o clasificaciones tácitas.
- **Decisión:** Se utilizó la etiqueta oficial `tipo_recurso` presente en los registros del Capítulo IV de la Secretaría de Energía. Se validó cruzando con la formación geológica objetivo (`Vaca Muerta`, `Los Molles`) y las listas de concesiones de explotación no convencional (CENCH).
- **Consecuencia:** La cifra récord de participación shale en 2025 (**62,9%**, 29.218 Mm³) es 100% verificable contra los datos oficiales.

---

## ADR 06: Restricciones de Causalidad Económica
- **Contexto:** El plan prohíbe inferir rentabilidad económica individual por pozo o atribuir linealmente impactos macroeconómicos sin modelos de identificación causal.
- **Decisión:** 
  1. No calcular "costo por barril" ni "ganancia neta" por pozo, dado que la Secretaría de Energía no publica OPEX auditado por pozo.
  2. Presentar la relación entre producción, empleo formal en Neuquén (CEP XXI) y comercio exterior (Banco Mundial) como **concomitancias temporales observables**, documentando con transparencia las fuentes de cada serie.
- **Consecuencia:** Integridad metodológica inatacable ante jurados evaluadores.
