# Perfil de Dataset: Indicadores Macroeconómicos Petroleros de Argentina (Banco Mundial)

- **Identificador:** `worldbank_macro`
- **Fuente:** World Bank Open Data
- **Archivo local:** `data/raw/worldbank/*.json`
- **Tamaño:** 0.05 MB
- **Cantidad de filas:** 52
- **Cantidad de columnas:** 7
- **Cobertura temporal:** 1970 a 2024
- **Cobertura geográfica:** Nacional / Comparativa Internacional
- **Nivel de confianza:** OFICIAL / INTERNACIONAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `year` | INTEGER | 0.0% | 52 |
| `oil_rents_gdp_pct` | DOUBLE | 0.0% | 52 |
| `fuel_imports_merch_pct` | DOUBLE | 0.0% | 52 |
| `fuel_exports_merch_pct` | DOUBLE | 0.0% | 52 |

## Primeras Filas (Muestra)

```text
[
  {
    "country": "Argentina",
    "countryiso3code": "ARG",
    "date": "2017",
    "year": 2017,
    "value": 0.663565866238942,
    "indicator_id": "NY.GDP.PETR.RT.ZS",
    "indicator_name": "Oil rents (% of GDP)"
  },
  {
    "country": "Argentina",
    "countryiso3code": "ARG",
    "date": "2018",
    "year": 2018,
    "value": 1.31095340723836,
    "indicator_id": "NY.GDP.PETR.RT.ZS",
    "indicator_name": "Oil rents (% of GDP)"
  },
  {
    "country": "Argentina",
    "countryiso3code": "ARG",
    "date": "2019",
    "year": 2019,
    "value": 1.29099565501431,
    "indicator_id": "NY.GDP.PETR.RT.ZS",
    "indicator_name": "Oil rents (% of GDP)"
  },
  {
    "country": "Argentina",
    "countryiso3code": "ARG",
    "date": "2020",
    "year": 2020,
    "value": 0.677055565819106,
    "indicator_id": "NY.GDP.PETR.RT.ZS",
    "indicator_name": "Oil rents (% of GDP)"
  },
  {
    "country": "Argentina",
    "countryiso3code": "ARG",
    "date": "2021",
    "year": 2021,
    "value": 1.54438228879011,
    "indicator_id": "NY.GDP.PETR.RT.ZS",
    "indicator_name": "Oil rents (% of GDP)"
  }
]
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `year`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** N/A (Nivel Macro)
- **Aptitud para visualizaciones del plan:** Apto para Escena 7 (Contexto macroeconómico y balance comercial)
- **Observaciones metodológicas:** Rentas del petróleo como % del PIB y evolución del comercio exterior de combustibles.
