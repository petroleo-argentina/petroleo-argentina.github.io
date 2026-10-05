# Perfil de Dataset: Venteos Detectados por Sensores Remotos y Satelitales

- **Identificador:** `sensores_remotos_venteo`
- **Fuente:** Secretaría de Energía
- **Archivo local:** `data/raw/ambiente/sensores-remotos-venteos-detectados.csv`
- **Tamaño:** 4.57 MB
- **Cantidad de filas:** 33,691
- **Cantidad de columnas:** 10
- **Cobertura temporal:** 2007 a 2025
- **Cobertura geográfica:** Geolocalizado (Lat/Lon puntos calientes en Argentina)
- **Nivel de confianza:** OFICIAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `fecha` | DATE | 0.0% | N/A |
| `satelite_new` | VARCHAR | 0.0% | N/A |
| `sensor` | VARCHAR | 0.0% | N/A |
| `mes` | BIGINT | 0.0% | N/A |
| `anio` | BIGINT | 0.0% | N/A |
| `hora_utc` | BIGINT | 0.0% | N/A |
| `latitud` | DOUBLE | 0.0% | N/A |
| `longitud` | DOUBLE | 0.0% | N/A |
| `provincia` | VARCHAR | 0.0% | N/A |
| `geojson` | VARCHAR | 0.0% | N/A |

## Primeras Filas (Muestra)

```text
       fecha satelite_new sensor  mes  anio  hora_utc   latitud  longitud provincia                                                                      geojson
0 2022-11-01    Suomi NPP  VIIRS   11  2021       603 -38.45322 -68.49302   NEUQUEN  {"type":"MultiPoint","coordinates":[[-68.4930199997731,-38.4532199996033]]}
1 2022-11-01    Suomi NPP  VIIRS   11  2021       603 -38.45775 -68.49365   NEUQUEN  {"type":"MultiPoint","coordinates":[[-68.4936500000474,-38.4577499998626]]}
2 2022-11-01    Suomi NPP  VIIRS   11  2021       603 -38.51254 -68.60471   NEUQUEN  {"type":"MultiPoint","coordinates":[[-68.6047099999665,-38.5125400003207]]}
3 2022-11-01    Suomi NPP  VIIRS   11  2021       603 -38.89919 -68.20768   NEUQUEN  {"type":"MultiPoint","coordinates":[[-68.2076800001319,-38.8991899999185]]}
4 2022-11-02    Suomi NPP  VIIRS   11  2021       546 -38.10052 -68.66692   NEUQUEN    {"type":"MultiPoint","coordinates":[[-68.666919999958,-38.100519999898]]}
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `coordenadas`, `fecha`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Cruce espacial por proximidad a yacimientos / pozos
- **Aptitud para visualizaciones del plan:** Apto para Escena 8 (Infraestructura y ambiente)
- **Observaciones metodológicas:** Total detecciones satelitales: 33,691
