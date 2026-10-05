# Perfil de Dataset: Puestos de Trabajo Asalariados Registrados por Departamento y Sector (CLAE 2)

- **Identificador:** `empleo_departamento`
- **Fuente:** Secretaría de Industria y Desarrollo Productivo / CEPXXI
- **Archivo local:** `data/raw/empleo/puestos_depto_priv_clae2.csv`
- **Tamaño:** 90.99 MB
- **Cantidad de filas:** 3,592,707
- **Cantidad de columnas:** 5
- **Cobertura temporal:** 2007 a 2025
- **Cobertura geográfica:** Departamentos/Partidos de todo el país (INDEC)
- **Nivel de confianza:** OFICIAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `fecha` | DATE | 0.0% | N/A |
| `codigo_departamento_indec` | BIGINT | 0.0% | N/A |
| `id_provincia_indec` | BIGINT | 0.0% | N/A |
| `clae2` | BIGINT | 0.0% | N/A |
| `puestos` | BIGINT | 0.0% | N/A |

## Primeras Filas (Muestra)

```text
       fecha  codigo_departamento_indec  id_provincia_indec  clae2  puestos
0 2014-01-01                       2000                   2      1     5448
1 2014-01-01                       2000                   2      2      114
2 2014-01-01                       2000                   2      3      571
3 2014-01-01                       2000                   2      5      -99
4 2014-01-01                       2000                   2      6     2701
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `departamento`, `clae2`, `fecha`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Nivel Departamental (Añelo, Confluencia, etc.)
- **Aptitud para visualizaciones del plan:** Apto para Escena 7 (Zoom territorial Vaca Muerta: Añelo)
- **Observaciones metodológicas:** Total registros a nivel departamental: 3,592,707
