# Registro de Incidencias Técnicas y Soluciones (Post-Mortem)

En cumplimiento del Principio Obligatorio N° 8 del proyecto (*"Si una descarga falla: NO ignorarla; registrar el error; intentar fuente alternativa; dejar constancia"*), este documento detalla todas las incidencias técnicas registradas durante la ejecución, junto con su causa raíz y solución aplicada.

---

## Incidencia 01: Error HTTP 502 / Timeout en la API CKAN de `datos.gob.ar`
- **Etapa:** Fase 1 — Descubrimiento de fuentes.
- **Síntoma:** Al invocar el endpoint estándar de la API CKAN `action/package_show?id=produccion-de-petroleo-y-gas-por-pozo`, el servidor gubernamental devolvía un código `HTTP 502 Bad Gateway` tras 60 segundos de espera.
- **Causa Raíz:** El dataset contiene más de 17 millones de registros y cientos de metadatos de recursos históricos. El backend de CKAN intentaba serializar el árbol completo en memoria, excediendo el límite de tiempo de ejecución del reverse proxy.
- **Solución / Workaround:** Se cambió la estrategia de consulta a `action/package_search?q=id:produccion-de-petroleo-y-gas-por-pozo`. Este endpoint ejecuta una consulta indexada en Solr que devuelve los metadatos y enlaces de descarga de manera directa en menos de 800 ms.
- **Estado:** RESUELTO.

---

## Incidencia 02: Error HTTP 404 en URLs estáticas de perforación
- **Etapa:** Fase 2 — Descarga de datos oficiales.
- **URLs afectadas:**
  - `https://datos.gob.ar/.../pozos-terminados-2009-en-adelante.csv`
  - `https://datos.gob.ar/.../metros-perforados-2009-en-adelante.csv`
  - `https://datos.gob.ar/.../pozos-en-perforacion-2009-en-adelante.csv`
- **Síntoma:** Descarga fallida con código `HTTP 404 Not Found`.
- **Causa Raíz:** La Secretaría de Energía reorganizó el catálogo y renombró los archivos eliminando el sufijo `-2009-en-adelante` cuando actualizó la serie al año 2025.
- **Solución:** Se utilizó el cliente de descubrimiento de CKAN para inspeccionar los recursos activos del dataset `perforacion-de-pozos-de-hidrocarburos`, localizando los nombres reales:
  - `pozos-terminados.csv` (178,27 MB)
  - `metros-perforados.csv` (66,36 MB)
  - `pozos-en-perforacion.csv` (64,87 MB)
- **Registro:** Se documentó en `logs/download_errors.jsonl` con estado resuelto y URLs alternativas.
- **Estado:** RESUELTO.

---

## Incidencia 03: Publicación de Reservas en formato ZIP con planillas Excel
- **Etapa:** Fase 2 — Descarga de reservas de hidrocarburos.
- **Síntoma:** Los recursos oficiales para las reservas comprobadas de 2024 y 2025 no estaban disponibles como CSV tabulares simples, sino empaquetados en archivos comprimidos `.zip`.
- **Causa Raíz:** Formato nativo de publicación de la Dirección Nacional de Exploración y Producción.
- **Solución:** Se incorporó un pipeline automático en Python que descarga el archivo comprimido, verifica su hash SHA-256 y extrae de forma determinística las planillas `reservas al 31-12-2024.xlsx` y `reservas al 31-12-2025.xlsx` en la carpeta `data/raw/energia/reservas/`.
- **Estado:** RESUELTO.

---

## Incidencia 04: Discrepancias de nomenclatura en esquemas crudos
- **Etapa:** Fase 3 — Perfilado y validación de calidad.
- **Síntoma:** Errores de clave al intentar unir tablas mediante nombres de columna supuestos.
- **Casos detectados:**
  1. En `wells.parquet` (PetroDB), el identificador único es `idpozo` (sin guion bajo), mientras que en el CSV de fracturas (`datos-de-fractura...adjunto-iv.csv`) figura como `id_pozo`.
  2. En `puestos_priv_provincia_clae2.csv`, la columna de provincia se denomina `zona_prov`.
  3. En fracturas, el conteo de etapas se llama `cantidad_fracturas`.
- **Solución:** Se implementó una capa de normalización explícita en `etl/transform/` que estandariza los nombres de campos a la convención canónica del modelo `core.*`.
- **Estado:** RESUELTO.
