# Perfil de Dataset: Puestos de Trabajo Asalariados Registrados por Provincia y Sector (CLAE 2)

- **Identificador:** `empleo_provincia`
- **Fuente:** Secretaría de Industria y Desarrollo Productivo / CEPXXI
- **Archivo local:** `data/raw/empleo/puestos_priv_provincia_clae2.csv`
- **Tamaño:** 10.69 MB
- **Cantidad de filas:** 387,234
- **Cantidad de columnas:** 4
- **Cobertura temporal:** 2007 a 2025
- **Cobertura geográfica:** 24 Provincias de Argentina
- **Nivel de confianza:** OFICIAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `fecha` | DATE | 0.0% | N/A |
| `zona_prov` | VARCHAR | 0.0% | N/A |
| `clae2` | BIGINT | 0.0% | N/A |
| `puestos` | BIGINT | 0.0% | N/A |

## Primeras Filas (Muestra)

```text
       fecha     zona_prov  clae2  puestos
0 2007-01-01  BUENOS AIRES      1    72723
1 2007-01-01  BUENOS AIRES      2      646
2 2007-01-01  BUENOS AIRES      3     3092
3 2007-01-01  BUENOS AIRES      5       72
4 2007-01-01  BUENOS AIRES      6     1137
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `provincia`, `clae2`, `fecha`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Nivel Territorial / Sectorial
- **Aptitud para visualizaciones del plan:** Apto para Escena 7 (Evolución de empleo petrolero y conexos en Neuquén)
- **Observaciones metodológicas:** Permite filtrar CLAE 06 (Extracción de petróleo y gas natural) y CLAE 09 (Servicios de apoyo a la extracción).
