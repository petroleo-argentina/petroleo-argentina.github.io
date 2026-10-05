# Perfil de Dataset: Inversiones Upstream Mensuales Declaradas (Res. 2057)

- **Identificador:** `inversiones_upstream`
- **Fuente:** Secretaría de Energía
- **Archivo local:** `data/raw/energia/resolucion-2057-inversiones-realizadas-mensual.csv`
- **Tamaño:** 10.11 MB
- **Cantidad de filas:** 45,486
- **Cantidad de columnas:** 23
- **Cobertura temporal:** 2015 a 2026
- **Cobertura geográfica:** Nacional por Cuenca, Provincia y Empresa Operadora
- **Nivel de confianza:** OFICIAL

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `Año de presentación de la DDJJ` | BIGINT | 0.0% | N/A |
| `Empresa informante` | VARCHAR | 0.0% | N/A |
| `idempresa` | BIGINT | 0.0% | N/A |
| `Área/Permiso/Concesión` | VARCHAR | 0.0% | N/A |
| `idconcesion` | BIGINT | 0.0% | N/A |
| `Yacimiento` | VARCHAR | 0.0% | N/A |
| `Cuenca` | VARCHAR | 0.0% | N/A |
| `Ubicación` | VARCHAR | 0.0% | N/A |
| `Provincia` | VARCHAR | 0.0% | N/A |
| `Período del plan de acción` | VARCHAR | 0.0% | N/A |
| `Estado de la DDJJ` | VARCHAR | 0.0% | N/A |
| `Mes de la inversión` | VARCHAR | 0.0% | N/A |
| `Descripción del plan de acción (Conceptos)` | VARCHAR | 0.0% | N/A |
| `Cant. Exploracion` | DOUBLE | 0.0% | N/A |
| `Millones u$s Exploracion` | DOUBLE | 0.0% | N/A |
| `Cant. Explotacion` | DOUBLE | 0.0% | N/A |
| `Millones u$s Explotacion` | DOUBLE | 0.0% | N/A |
| `Cant. Exploracion Complementaria` | DOUBLE | 0.0% | N/A |
| `Millones u$s Exp. Complementaria` | DOUBLE | 0.0% | N/A |
| `Hombres hora` | DOUBLE | 0.0% | N/A |
| `Fecha Inicio Tareas` | DATE | 0.0% | N/A |
| `Fecha Fin Tareas` | DATE | 0.0% | N/A |
| `Tipo de explotación` | VARCHAR | 0.0% | N/A |

## Primeras Filas (Muestra)

```text
   Año de presentación de la DDJJ        Empresa informante  idempresa    Área/Permiso/Concesión  idconcesion                Yacimiento    Cuenca Ubicación Provincia        Período del plan de acción Estado de la DDJJ Mes de la inversión         Descripción del plan de acción (Conceptos)  Cant. Exploracion  Millones u$s Exploracion  Cant. Explotacion  Millones u$s Explotacion  Cant. Exploracion Complementaria  Millones u$s Exp. Complementaria  Hombres hora Fecha Inicio Tareas Fecha Fin Tareas Tipo de explotación
0                            2013                  YPF S.A.        360  EL MANZANO OESTE (RESTO)         3390  EL MANZANO OESTE (RESTO)  NEUQUINA  On Shore   Mendoza  Inversiones mensuales realizadas           Cerrada          Septiembre   Perforación Pozos Productores de Petróleo(pozos)                0.0                  0.000000                0.0                  0.000000                               0.0                          0.168002           0.0          2013-01-01       2013-12-31        Convencional
1                            2013                  YPF S.A.        360                CHACHAHUEN         3364                CHACHAHUEN  NEUQUINA  On Shore   Mendoza  Inversiones mensuales realizadas           Cerrada          Septiembre                                  Otras Inversiones                0.0                  0.000000                0.0                  0.967143                               0.0                          0.000000           0.0          2013-01-01       2013-12-31        Convencional
2                            2013                  YPF S.A.        360                CHACHAHUEN         3364                CHACHAHUEN  NEUQUINA  On Shore   Mendoza  Inversiones mensuales realizadas           Cerrada          Septiembre   Perforación Pozos Productores de Petróleo(pozos)                0.0                  0.000000                0.0                  3.871429                               0.0                          0.000000           0.0          2013-01-01       2013-12-31        Convencional
3                            2013  PETROLERA EL TREBOL S.A.       1011         REFUGIO TUPUNGATO          549                 TUPUNGATO    CUYANA  On Shore   Mendoza  Inversiones mensuales realizadas           Cerrada               Enero  Baterias y Plantas de Deshidratación y/o Desalado                NaN                       NaN                1.0                  0.034700                               NaN                               NaN           NaN          2013-01-01       2013-12-31        Convencional
4                            2013                  YPF S.A.        360              CERRO AVISPA         3362              CERRO AVISPA  NEUQUINA  On Shore   Neuquén  Inversiones mensuales realizadas           Cerrada          Septiembre             Perforación Pozos Exploratorios(pozos)                0.0                  0.274742                0.0                  0.000000                               0.0                          0.000000           0.0          2013-01-01       2013-12-31     No Convencional
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `empresa`, `anio`, `mes`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Nivel Concesión / Empresa
- **Aptitud para visualizaciones del plan:** Apto para Escena 7 (Del pozo al país: inversión vs producción con lag)
- **Observaciones metodológicas:** Total registros: 45,486
