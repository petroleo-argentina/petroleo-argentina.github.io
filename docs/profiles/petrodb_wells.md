# Perfil de Dataset: Padrón Maestro de Pozos de Argentina (PetroDB / Sumpa Labs)

- **Identificador:** `petrodb_wells`
- **Fuente:** Secretaría de Energía / Sumpa Labs
- **Archivo local:** `data/raw/petrodb/wells.parquet`
- **Tamaño:** 7.90 MB
- **Cantidad de filas:** 85,417
- **Cantidad de columnas:** 44
- **Cobertura temporal:** Histórico acumulado hasta 2025
- **Cobertura geográfica:** Nacional (13 provincias, 10 cuencas sedimentarias, coordenadas Gauss-Kruger / WGS84)
- **Nivel de confianza:** ALTO (Espejo oficial auditado)

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `idpozo` | BIGINT | 0.0% | Verificado |
| `sigla` | VARCHAR | 0.0% | Verificado |
| `formprod` | VARCHAR | 4.5% | Verificado |
| `codigopropio` | VARCHAR | 10.7% | Verificado |
| `nombrepropio` | VARCHAR | 6.7% | Verificado |
| `area` | VARCHAR | 0.0% | Verificado |
| `cod_area` | VARCHAR | 0.0% | Verificado |
| `yacimiento` | VARCHAR | 0.0% | Verificado |
| `cod_yacimiento` | VARCHAR | 0.0% | Verificado |
| `cuenca` | VARCHAR | 0.0% | Verificado |
| `provincia` | VARCHAR | 0.0% | Verificado |
| `idcuenca` | VARCHAR | 1.4% | Verificado |
| `idprovincia` | VARCHAR | 1.4% | Verificado |
| `formacion` | VARCHAR | 3.3% | Verificado |
| `cota` | DOUBLE | 0.0% | Verificado |
| `profundidad` | DOUBLE | 0.0% | Verificado |
| `clasificacion` | VARCHAR | 0.0% | Verificado |
| `subclasificacion` | VARCHAR | 0.0% | Verificado |
| `tipo_recurso` | VARCHAR | 0.0% | Verificado |
| `sub_tipo_recurso` | VARCHAR | 0.0% | Verificado |
| `gasplus` | VARCHAR | 0.0% | Verificado |
| `proyecto` | VARCHAR | 0.1% | Verificado |
| `empresa` | VARCHAR | 1.1% | Verificado |
| `coordenadax` | DOUBLE | 1.4% | Verificado |
| `coordenaday` | DOUBLE | 1.4% | Verificado |
| `geom` | BLOB | 0.0% | Verificado |
| `adjiv_fecha_inicio_perf` | DATE | 39.9% | Verificado |
| `adjiv_fecha_fin_perf` | DATE | 40.0% | Verificado |
| `adjiv_fecha_inicio_term` | DATE | 42.8% | Verificado |
| `adjiv_fecha_fin_term` | DATE | 42.7% | Verificado |
| `adjiv_fecha_inicio` | DATE | 40.6% | Verificado |
| `adjiv_fecha_fin` | DATE | 40.7% | Verificado |
| `adjiv_fecha_abandono` | DATE | 95.2% | Verificado |
| `adjiv_equipo_utilizar` | VARCHAR | 40.6% | Verificado |
| `adjiv_capacidad_perf` | DOUBLE | 41.1% | Verificado |
| `pet_inicial` | DOUBLE | 1.4% | Verificado |
| `gas_inicial` | DOUBLE | 1.4% | Verificado |
| `agua_inicial` | DOUBLE | 1.4% | Verificado |
| `iny_agua_inicial` | DOUBLE | 1.4% | Verificado |
| `iny_gas_inicial` | DOUBLE | 1.4% | Verificado |
| `iny_otros_inicial` | DOUBLE | 1.4% | Verificado |
| `iny_co2_inicial` | DOUBLE | 1.4% | Verificado |
| `vida_util_inicial` | DOUBLE | 1.4% | Verificado |
| `has_production` | BOOLEAN | 0.0% | Verificado |

## Primeras Filas (Muestra)

```text
   idpozo          sigla               formacion  tipo_recurso provincia           cuenca  coordenadax  coordenaday
0     351           M-46  formación improductiva  No informado    Chubut  GOLFO SAN JORGE   -67.353469   -45.614988
1     355           M-58           glauconitico   No informado    Chubut  GOLFO SAN JORGE   -67.394564   -45.580341
2     358           M-61  formación improductiva  No informado    Chubut  GOLFO SAN JORGE   -67.387084   -45.569821
3     364           M-32  formación improductiva  No informado    Chubut  GOLFO SAN JORGE   -67.466426   -45.618200
4     387  YPF.Ch.MMO-29                castillo  No informado    Chubut  GOLFO SAN JORGE   -69.967870   -45.965400
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `idpozo`, `sigla`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Clave primaria directa (idpozo)
- **Aptitud para visualizaciones del plan:** Apto para Escena 2 (Mapa temporal) y dimension central
- **Observaciones metodológicas:** 85,417 pozos totales, 3,382 pozos en Vaca Muerta, 4,833 no convencionales.
