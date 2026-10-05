# Perfil de Dataset: Serie Histórica Nacional de Producción de Petróleo desde 1950

- **Identificador:** `produccion_1950`
- **Fuente:** Secretaría de Energía
- **Archivo local:** `data/raw/energia/serie-produccion-petroleo-total-pais-desde-1950.csv`
- **Tamaño:** 0.00 MB
- **Cantidad de filas:** 66
- **Cantidad de columnas:** 3
- **Cobertura temporal:** 1950 a 2015
- **Cobertura geográfica:** Nacional (Total País)
- **Nivel de confianza:** OFICIAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `anio` | int64 | 0.0% | 66 |
| `unidad` | str | 0.0% | 1 |
| `produccion_petroleo` | float64 | 0.0% | 66 |

## Primeras Filas (Muestra)

```text
   anio unidad  produccion_petroleo
0  1950    Mm3               3730.0
1  1951    Mm3               3889.6
2  1952    Mm3               3946.0
3  1953    Mm3               4531.4
4  1954    Mm3               4701.6
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `anio`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** N/A (Nivel Macro)
- **Aptitud para visualizaciones del plan:** Apto para Escena 1 (75 años de petróleo)
- **Observaciones metodológicas:** Unidad: Mm3 (miles de m3). Acompañado por documento metodológico oficial.
