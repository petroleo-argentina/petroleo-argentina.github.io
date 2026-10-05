# Perfil de Dataset: Producción Mensual por Pozo (Capítulo IV - 2006 a 2025)

- **Identificador:** `produccion_pozo_mensual`
- **Fuente:** Secretaría de Energía / Sumpa Labs
- **Archivo local:** `data/raw/petrodb/monthly_production/anio=*/data.parquet`
- **Tamaño:** 139.84 MB
- **Cantidad de filas:** 17,775,911
- **Cantidad de columnas:** 12
- **Cobertura temporal:** 2006-01-01 a 2025-12-01 (20 años completos)
- **Cobertura geográfica:** Nacional por pozo
- **Nivel de confianza:** CRÍTICO / ALTO

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `idpozo` | BIGINT | 0.0% | Verificado |
| `fecha` | DATE | 0.0% | Verificado |
| `prod_pet` | DOUBLE | 0.8% | Verificado |
| `prod_gas` | DOUBLE | 0.8% | Verificado |
| `prod_agua` | DOUBLE | 0.8% | Verificado |
| `iny_agua` | DOUBLE | 0.8% | Verificado |
| `iny_gas` | DOUBLE | 0.8% | Verificado |
| `iny_co2` | DOUBLE | 0.8% | Verificado |
| `iny_otro` | DOUBLE | 0.8% | Verificado |
| `tef` | DOUBLE | 0.8% | Verificado |
| `vida_util` | DOUBLE | 95.1% | Verificado |
| `anio` | BIGINT | 0.0% | Verificado |

## Primeras Filas (Muestra)

```text
   idpozo      fecha  prod_pet  prod_gas  prod_agua  dias_prod
0     212 2006-01-01     64.61     10.94    1017.78       31.0
1     212 2006-02-01     57.39     13.07     911.91       28.0
2     212 2006-03-01     61.27     14.02     971.41       31.0
3     212 2006-04-01     63.20     14.72    1002.84       30.0
4     212 2006-05-01     69.12     15.99    1090.67       31.0
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `idpozo`, `fecha`
- **Duplicados por clave principal:** 0 (validado a nivel mensual)
- **Aptitud para cruce con core.dim_pozo:** 100% match con idpozo
- **Aptitud para visualizaciones del plan:** Apto para Escenas 1, 3, 4, 5 y EDA completo
- **Observaciones metodológicas:** 17,775,911 registros mensuales. Contiene petróleo, gas, agua, inyección y días efectivos de producción (tef).
