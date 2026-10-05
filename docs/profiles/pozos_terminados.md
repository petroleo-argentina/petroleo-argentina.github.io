# Perfil de Dataset: Pozos Terminados de Hidrocarburos (2009 en adelante)

- **Identificador:** `pozos_terminados`
- **Fuente:** Secretaría de Energía
- **Archivo local:** `data/raw/energia/pozos-terminados.csv`
- **Tamaño:** 178.27 MB
- **Cantidad de filas:** 1,159,197
- **Cantidad de columnas:** 22
- **Cobertura temporal:** 2009 a 2026
- **Cobertura geográfica:** Nacional por pozo, cuenca, provincia
- **Nivel de confianza:** OFICIAL / CRÍTICO

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `indice_tiempo` | VARCHAR | 0.0% | N/A |
| `anio` | BIGINT | 0.0% | N/A |
| `mes` | BIGINT | 0.0% | N/A |
| `idempresa` | VARCHAR | 0.0% | N/A |
| `empresa` | VARCHAR | 0.0% | N/A |
| `idareapermisoconcesion` | VARCHAR | 0.0% | N/A |
| `areapermisoconcesion` | VARCHAR | 0.0% | N/A |
| `idareayacimiento` | VARCHAR | 0.0% | N/A |
| `areayacimiento` | VARCHAR | 0.0% | N/A |
| `idcuenca` | VARCHAR | 0.0% | N/A |
| `cuenca` | VARCHAR | 0.0% | N/A |
| `idprovincia` | VARCHAR | 0.0% | N/A |
| `provincia` | VARCHAR | 0.0% | N/A |
| `idubicacion` | BIGINT | 0.0% | N/A |
| `ubicacion` | VARCHAR | 0.0% | N/A |
| `idtipodepozoterminado` | BIGINT | 0.0% | N/A |
| `tipodepozoterminado` | VARCHAR | 0.0% | N/A |
| `idconcepto` | BIGINT | 0.0% | N/A |
| `concepto` | VARCHAR | 0.0% | N/A |
| `cantidad` | DOUBLE | 0.0% | N/A |
| `observaciones` | VARCHAR | 0.0% | N/A |
| `fecha_data` | DATE | 0.0% | N/A |

## Primeras Filas (Muestra)

```text
  indice_tiempo  anio  mes idempresa                           empresa idareapermisoconcesion               areapermisoconcesion
0       2009-01  2009    1       ALP  ALIANZA PETROLERA ARGENTINA S.A.                    CAL      CALMUCO - BARREALES COLORADOS
1       2009-01  2009    1       PEL        PETROLERA ENTRE LOMAS S.A.                    ELO                        ENTRE LOMAS
2       2009-01  2009    1       CHE          CHEVRON ARGENTINA S.R.L.                    HUA             EL TRAPIAL - CURAMCHED
3       2009-01  2009    1       YPF                          YPF S.A.                    CPG  CERRO PIEDRA - CERRO GUADAL NORTE
4       2009-01  2009    1       ALP  ALIANZA PETROLERA ARGENTINA S.A.                    CAL      CALMUCO - BARREALES COLORADOS
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `idempresa`, `idareapermisoconcesion`, `idareayacimiento`, `idcuenca`, `idprovincia`, `idubicacion`, `idtipodepozoterminado`, `tipodepozoterminado`, `idconcepto`, `cantidad`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Directo por idpozo
- **Aptitud para visualizaciones del plan:** Apto para Escena 4 (Más pozos o mejores pozos)
- **Observaciones metodológicas:** Total pozos terminados registrados: 1,159,197
