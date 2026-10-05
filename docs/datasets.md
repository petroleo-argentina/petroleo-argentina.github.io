# Catálogo de Fuentes de Datos del Proyecto

Este documento reúne el inventario oficial de datasets incorporados al proyecto, detallando la entidad emisora, metodología de descubrimiento, formato, cobertura y prioridad.

---

| ID | Dataset | Emisor | Prioridad | Formato | Cobertura Temporal | Estado Local |
|---|---|---|---|---|---|---|
| `produccion_pozo_cap4` | **Producción de petróleo y gas por pozo (Capítulo IV)** | Secretaría de Energía de la Nación | `CRITICAL` | Parquet (PetroDB mirror) + CSV oficial | 1950 - 2026 | DISPONIBLE |
| `petrodb_wells` | **Padrón Maestro de Pozos de Argentina (PetroDB)** | Secretaría de Energía / Sumpa Labs | `CRITICAL` | Parquet | 1950 - 2026 | DISPONIBLE |
| `produccion_1950` | **Producción nacional de petróleo desde 1950** | Secretaría de Energía de la Nación | `HIGH` | CSV + PDF Metodológico | 1950 - 2026 | DISPONIBLE |
| `fractura_pozos` | **Datos de fractura de pozos de hidrocarburos (Adjunto IV)** | Secretaría de Energía de la Nación | `CRITICAL` | CSV | 1950 - 2026 | DISPONIBLE |
| `trayectorias_vaca_muerta` | **Trayectorias de Pozo Vaca Muerta** | Secretaría de Energía de la Nación | `HIGH` | CSV | 1950 - 2026 | DISPONIBLE |
| `perforacion_pozos` | **Perforación y terminación de pozos de petróleo y gas** | Secretaría de Energía de la Nación | `CRITICAL` | CSV | 1950 - 2026 | DISPONIBLE |
| `inversiones_upstream` | **Inversiones en mercado de hidrocarburos upstream (Res. 2057)** | Secretaría de Energía de la Nación | `HIGH` | CSV | 1950 - 2026 | DISPONIBLE |
| `reservas_hidrocarburos` | **Reservas de Petróleo y Gas** | Secretaría de Energía de la Nación | `HIGH` | XLSX (ZIP) | 1950 - 2026 | DISPONIBLE |
| `empleo_provincia` | **Puestos de trabajo asalariados registrados por provincia y sector** | Secretaría de Industria y Desarrollo Productivo / CEPXXI | `HIGH` | CSV | 1950 - 2026 | DISPONIBLE |
| `empleo_departamento` | **Puestos de trabajo por departamento/partido y sector de actividad** | Secretaría de Industria y Desarrollo Productivo / CEPXXI | `HIGH` | CSV | 1950 - 2026 | DISPONIBLE |
| `puntos_venteo` | **Venteos de hidrocarburos (Declarados y Sensores Satelitales)** | Secretaría de Energía de la Nación | `MEDIUM` | CSV | 1950 - 2026 | DISPONIBLE |
| `refinacion_instalaciones` | **Refinerías y ductos de transporte de hidrocarburos** | Secretaría de Energía de la Nación | `MEDIUM` | CSV | 1950 - 2026 | DISPONIBLE |
| `worldbank_macro` | **Indicadores macroeconómicos de hidrocarburos y comercio (World Bank)** | The World Bank Open Data | `MEDIUM` | JSON | 1950 - 2026 | DISPONIBLE |

---

## Detalle Metodológico por Dataset

### `produccion_pozo_cap4` — Producción de petróleo y gas por pozo (Capítulo IV)

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/produccion-de-petroleo-y-gas-por-pozo](https://datos.gob.ar/dataset/produccion-de-petroleo-y-gas-por-pozo)
- **Ruta local:** `data/raw/petrodb/monthly_production/`
- **Prioridad metodológica:** `CRITICAL` (Requerido: True)
- **Descripción funcional:** Serie mensual pozo a pozo de producción de petróleo (m3), gas (miles m3), agua (m3) y días efectivos (2006-2025).

### `petrodb_wells` — Padrón Maestro de Pozos de Argentina (PetroDB)

- **Publicador:** Secretaría de Energía / Sumpa Labs
- **Catálogo / Portal:** [https://huggingface.co/datasets/sumpalabs/petrodb](https://huggingface.co/datasets/sumpalabs/petrodb)
- **Ruta local:** `data/raw/petrodb/wells.parquet`
- **Prioridad metodológica:** `CRITICAL` (Requerido: True)
- **Descripción funcional:** Padrón de 85,417 pozos con coordenadas geográficas, cuenca, provincia, yacimiento, formación productiva y tipo de recurso.

### `produccion_1950` — Producción nacional de petróleo desde 1950

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/produccion-de-petroleo-desde-1950](https://datos.gob.ar/dataset/produccion-de-petroleo-desde-1950)
- **Ruta local:** `data/raw/energia/serie-produccion-petroleo-total-pais-desde-1950.csv`
- **Prioridad metodológica:** `HIGH` (Requerido: True)
- **Descripción funcional:** Serie histórica de producción petrolera nacional desde 1950 hasta 2015 en miles de m3.

### `fractura_pozos` — Datos de fractura de pozos de hidrocarburos (Adjunto IV)

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/datos-de-fractura-de-pozos-adjunto-iv](https://datos.gob.ar/dataset/datos-de-fractura-de-pozos-adjunto-iv)
- **Ruta local:** `data/raw/energia/datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv`
- **Prioridad metodológica:** `CRITICAL` (Requerido: True)
- **Descripción funcional:** Detalle técnico de etapas de fractura, toneladas de arena, volumen de agua y presión por pozo no convencional.

### `trayectorias_vaca_muerta` — Trayectorias de Pozo Vaca Muerta

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.energia.gob.ar/dataset/f5c0b5a5-b402-44d7-8fe0-f9e4fcb78b8d](https://datos.energia.gob.ar/dataset/f5c0b5a5-b402-44d7-8fe0-f9e4fcb78b8d)
- **Ruta local:** `data/raw/energia/trayectorias-de-pozo-vaca-muerta.csv`
- **Prioridad metodológica:** `HIGH` (Requerido: False)
- **Descripción funcional:** Estaciones direccionales 3D de pozos en Vaca Muerta con profundidad vertical y longitud de rama horizontal (mt).

### `perforacion_pozos` — Perforación y terminación de pozos de petróleo y gas

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/perforacion-de-pozos-de-petroleo-y-gas](https://datos.gob.ar/dataset/perforacion-de-pozos-de-petroleo-y-gas)
- **Ruta local:** `data/raw/energia/pozos-terminados.csv`
- **Prioridad metodológica:** `CRITICAL` (Requerido: True)
- **Descripción funcional:** Pozos terminados, en perforación y metros perforados por empresa, cuenca, provincia y tipo (2009 en adelante y series pre-2009).

### `inversiones_upstream` — Inversiones en mercado de hidrocarburos upstream (Res. 2057)

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/inversiones-en-mercado-de-hidrocarburos-upstream](https://datos.gob.ar/dataset/inversiones-en-mercado-de-hidrocarburos-upstream)
- **Ruta local:** `data/raw/energia/resolucion-2057-inversiones-realizadas-mensual.csv`
- **Prioridad metodológica:** `HIGH` (Requerido: False)
- **Descripción funcional:** Inversiones mensuales realizadas y programas anuales previstos por empresa operadora y área de concesión.

### `reservas_hidrocarburos` — Reservas de Petróleo y Gas

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/reservas-de-petroleo-y-gas](https://datos.gob.ar/dataset/reservas-de-petroleo-y-gas)
- **Ruta local:** `data/raw/energia/reservas/reservas al 31-12-2025.xlsx`
- **Prioridad metodológica:** `HIGH` (Requerido: False)
- **Descripción funcional:** Reservas comprobadas, probables y posibles por yacimiento, cuenca y provincia al 31/12/2024 y 31/12/2025.

### `empleo_provincia` — Puestos de trabajo asalariados registrados por provincia y sector

- **Publicador:** Secretaría de Industria y Desarrollo Productivo / CEPXXI
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/produccion-puestos-trabajo-asalariados-registrados-por-provincia-sector-actividad](https://datos.gob.ar/dataset/produccion-puestos-trabajo-asalariados-registrados-por-provincia-sector-actividad)
- **Ruta local:** `data/raw/empleo/puestos_priv_provincia_clae2.csv`
- **Prioridad metodológica:** `HIGH` (Requerido: True)
- **Descripción funcional:** Evolución mensual de empleo registrado en minería y extracción de hidrocarburos (CLAE 06 y 09) en Neuquén y demás provincias (2007-2025).

### `empleo_departamento` — Puestos de trabajo por departamento/partido y sector de actividad

- **Publicador:** Secretaría de Industria y Desarrollo Productivo / CEPXXI
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/produccion-puestos-trabajo-departamento-partido-sector-actividad](https://datos.gob.ar/dataset/produccion-puestos-trabajo-departamento-partido-sector-actividad)
- **Ruta local:** `data/raw/empleo/puestos_depto_priv_clae2.csv`
- **Prioridad metodológica:** `HIGH` (Requerido: False)
- **Descripción funcional:** Empleo desagregado a nivel departamental (foco en Departamento Añelo, Pehuenches y Confluencia).

### `puntos_venteo` — Venteos de hidrocarburos (Declarados y Sensores Satelitales)

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.gob.ar/dataset/produccion-hidrocarburos-puntos-de-venteo-declarados](https://datos.gob.ar/dataset/produccion-hidrocarburos-puntos-de-venteo-declarados)
- **Ruta local:** `data/raw/ambiente/sensores-remotos-venteos-detectados.csv`
- **Prioridad metodológica:** `MEDIUM` (Requerido: False)
- **Descripción funcional:** Detección satelital de venteos y puntos de venteo declarados por operadoras con geolocalización.

### `refinacion_instalaciones` — Refinerías y ductos de transporte de hidrocarburos

- **Publicador:** Secretaría de Energía de la Nación
- **Catálogo / Portal:** [https://datos.energia.gob.ar/dataset/a9eed347-78ab-45c0-a489-b227fe42ee1b](https://datos.energia.gob.ar/dataset/a9eed347-78ab-45c0-a489-b227fe42ee1b)
- **Ruta local:** `data/raw/energia/refinacion-hidrocarburos-refinerias.csv`
- **Prioridad metodológica:** `MEDIUM` (Requerido: False)
- **Descripción funcional:** Capacidad de refinación e infraestructura de ductos (Res. 319/93).

### `worldbank_macro` — Indicadores macroeconómicos de hidrocarburos y comercio (World Bank)

- **Publicador:** The World Bank Open Data
- **Catálogo / Portal:** [https://data.worldbank.org/country/argentina](https://data.worldbank.org/country/argentina)
- **Ruta local:** `data/raw/worldbank/`
- **Prioridad metodológica:** `MEDIUM` (Requerido: False)
- **Descripción funcional:** Oil rents (% PIB), Importaciones de combustibles (% merch), Exportaciones de combustibles (% merch).

