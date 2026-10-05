# Diccionario de Datos — Plataforma Petróleo en Argentina

Este documento detalla las entidades, campos, tipos de datos, unidades de medida y reglas de validación del modelo de datos de la plataforma.

---

## 1. Entidades Principales (Core)

### 1.1 `core.dim_pozo` (Dimensión Maestra de Pozos)
Fuente: Secretaría de Energía de la Nación (`capitulo-iv-pozos.csv` / `wells.parquet` - PetroDB).

| Campo | Tipo SQL | Unidad | Descripción | Regla / Restricción |
|---|---|---|---|---|
| `idpozo` | INTEGER | - | Identificador único numérico del pozo emitido por Secretaría de Energía | PK, No nulo |
| `sigla` | VARCHAR(100) | - | Nombre técnico normalizado del pozo (ej. `VIS.Nq.BPO-2801(h)`) | Not null, indexado |
| `empresa_actual` | VARCHAR(150) | - | Operador o concesionario actual | Not null |
| `cuenca` | VARCHAR(80) | - | Cuenca sedimentaria (Neuquina, Golfo San Jorge, Cuyana, etc.) | Not null |
| `provincia` | VARCHAR(60) | - | Provincia donde se ubica la boca de pozo | Not null |
| `yacimiento` | VARCHAR(120) | - | Nombre del yacimiento o campo productor | Not null |
| `concesion` | VARCHAR(120) | - | Área o bloque de concesión hidrocarburífera | Nullable |
| `formacion` | VARCHAR(100) | - | Formación geológica objetivo (ej. Vaca Muerta, Quintuco) | Nullable |
| `tipo_recurso` | VARCHAR(30) | - | `CONVENCIONAL` o `NO CONVENCIONAL` | Check in list |
| `tipo_pozo` | VARCHAR(40) | - | `HORIZONTAL`, `VERTICAL`, `DESVIADO`, etc. | Nullable |
| `lat` | DOUBLE PRECISION | Grados decimales | Latitud (WGS84, EPSG:4326) | Rango: [-56.0, -21.0] |
| `lon` | DOUBLE PRECISION | Grados decimales | Longitud (WGS84, EPSG:4326) | Rango: [-74.0, -53.0] |
| `geom` | GEOMETRY(Point, 4326) | Coordenadas | Geometría PostGIS / DuckDB spatial | Not null |
| `fecha_primera_prod` | DATE | - | Fecha de inicio de producción efectiva observada | Formato YYYY-MM-DD |

---

### 1.2 `core.fact_produccion_pozo_mes` (Hechos de Producción Mensual)
Fuente: Secretaría de Energía de la Nación (`monthly_production` 2006-2025).

| Campo | Tipo SQL | Unidad | Descripción | Regla / Restricción |
|---|---|---|---|---|
| `idpozo` | INTEGER | - | Clave foránea referenciando `core.dim_pozo(idpozo)` | FK, Not null |
| `fecha` | DATE | - | Primer día del mes de producción (ej. `2024-06-01`) | Not null |
| `anio` | SMALLINT | Año | Año calendario | 2006 <= anio <= 2025 |
| `mes` | SMALLINT | Mes | Mes calendario | 1 <= mes <= 12 |
| `prod_pet_m3` | DOUBLE PRECISION | Metros cúbicos ($m^3$) | Volumen de petróleo crudo extraído en el mes | >= 0, Not null |
| `prod_gas_miles_m3` | DOUBLE PRECISION | Miles de $m^3$ ($km^3$) | Volumen de gas natural extraído en el mes | >= 0, Not null |
| `prod_agua_m3` | DOUBLE PRECISION | Metros cúbicos ($m^3$) | Volumen de agua de formación producida | >= 0 |
| `dias_produccion` | SMALLINT | Días | Días efectivos en que el pozo operó en el mes | 0 <= dias <= 31 |

**Clave Primaria:** `(idpozo, fecha)`

---

### 1.3 `core.fact_fractura_adjunto_iv` (Completación Hidráulica)
Fuente: Secretaría de Energía de la Nación (Resolución SE 2057 / Adjunto IV).

| Campo | Tipo SQL | Unidad | Descripción |
|---|---|---|---|
| `id_pozo` | INTEGER | - | Identificador del pozo enlazado con `core.dim_pozo` |
| `sigla` | VARCHAR(100) | - | Sigla oficial del pozo fracturado |
| `longitud_horizontal_mt` | DOUBLE PRECISION | Metros | Longitud de la rama lateral navegada en la roca generadora |
| `cantidad_fracturas` | INTEGER | Etapas | Número total de etapas o etapas de fractura inducidas |
| `arena_bombeada_tn` | DOUBLE PRECISION | Toneladas | Masa total de agente de sostén (arena silícea) inyectada |
| `volumen_inyectado_m3` | DOUBLE PRECISION | Metros cúbicos | Volumen total de fluido de fractura bombeado a presión |
| `fecha_completacion` | DATE | - | Fecha de fin de las operaciones de estimulación |

---

### 1.4 `core.dim_trayectoria_direccional` (Surveys 3D de Vaca Muerta)
Fuente: Secretaría de Energía de la Nación (`trayectorias-de-pozo-vaca-muerta.csv`).

| Campo | Tipo SQL | Unidad | Descripción |
|---|---|---|---|
| `sigla` | VARCHAR(100) | - | Sigla técnica del pozo |
| `idpo` | INTEGER | - | Identificador numérico de perforación |
| `profundidad_final_total_mt` | DOUBLE PRECISION | Metros | Profundidad medida total (MD) a lo largo del pozo |
| `profundidad_vertical_mt` | DOUBLE PRECISION | Metros | Profundidad vertical verdadera (TVD) |
| `largo_rama_horizontal_mt` | DOUBLE PRECISION | Metros | Longitud neta del tramo horizontal |
| `geojson` | JSON / TEXT | - | Cadena GeoJSON con las coordenadas de la traza tridimensional |

---

### 1.5 `core.fact_empleo_provincia` (Empleo Asalariado Registrado)
Fuente: Ministerio de Economía / CEP XXI (`puestos_priv_provincia_clae2.csv`).

| Campo | Tipo SQL | Unidad | Descripción |
|---|---|---|---|
| `fecha` | DATE | - | Fecha mensual del registro |
| `zona_prov` | VARCHAR(80) | - | Provincia |
| `clae2` | VARCHAR(10) | Código | `06` (Extracción de petróleo y gas) o `09` (Servicios de apoyo) |
| `puestos` | DOUBLE PRECISION | Puestos | Cantidad de puestos de trabajo registrados |

---

## 2. Vistas Analíticas Materializadas (Analytics)

### 2.1 `analytics.mv_produccion_nacional_mes`
Agregación nacional mensual que contrasta el volumen convencional vs no convencional:
- `fecha`: YYYY-MM-01
- `total_m3_mes`: Suma nacional mensual ($m^3$)
- `convencional_m3_mes`: Suma convencional ($m^3$)
- `no_convencional_m3_mes`: Suma shale/tight ($m^3$)
- `participacion_no_conv_pct`: $\frac{\text{no\_convencional}}{\text{total}} \times 100$

### 2.2 `analytics.mv_cohortes_pozo`
Desagregación normalizada por edad del pozo:
- `cohorte`: Año de primera producción observada (2015, 2016, ..., 2024).
- `mes_vida`: Meses transcurridos desde el inicio ($0, 1, 2, \dots, 36$).
- `mediana_prod_pet_m3`: Mediana de producción física ($m^3$) para la cohorte en ese mes de vida.
- `p25_prod_pet_m3`: Primer cuartil ($m^3$).
- `p75_prod_pet_m3`: Tercer cuartil ($m^3$).
- `pozos_activos_mes`: Cantidad de pozos evaluados en ese punto de la curva.
