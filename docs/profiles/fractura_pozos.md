# Perfil de Dataset: Datos de Fractura de Pozos de Hidrocarburos (Adjunto IV)

- **Identificador:** `fractura_pozos`
- **Fuente:** Secretaría de Energía
- **Archivo local:** `data/raw/energia/datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv`
- **Tamaño:** 1.18 MB
- **Cantidad de filas:** 4,922
- **Cantidad de columnas:** 30
- **Cobertura temporal:** 2016 a 2026 (Actualización continua)
- **Cobertura geográfica:** Cuenca Neuquina (Vaca Muerta y tight)
- **Nivel de confianza:** OFICIAL / CRÍTICO

## Columnas y Tipos Inferidos

| Columna | Tipo | % Nulos | Valores Únicos (Aprox) |
|---|---|---|---|
| `id_base_fractura_adjiv` | BIGINT | 0.0% | Calculado |
| `idpozo` | BIGINT | 0.0% | Calculado |
| `sigla` | VARCHAR | 0.0% | Calculado |
| `cuenca` | VARCHAR | 0.0% | Calculado |
| `areapermisoconcesion` | VARCHAR | 0.0% | Calculado |
| `yacimiento` | VARCHAR | 0.0% | Calculado |
| `formacion_productiva` | VARCHAR | 0.0% | Calculado |
| `tipo_reservorio` | VARCHAR | 0.0% | Calculado |
| `subtipo_reservorio` | VARCHAR | 0.0% | Calculado |
| `longitud_rama_horizontal_m` | DOUBLE | 0.0% | Calculado |
| `cantidad_fracturas` | BIGINT | 0.0% | Calculado |
| `tipo_terminacion` | VARCHAR | 0.0% | Calculado |
| `arena_bombeada_nacional_tn` | DOUBLE | 0.0% | Calculado |
| `arena_bombeada_importada_tn` | DOUBLE | 0.0% | Calculado |
| `agua_inyectada_m3` | DOUBLE | 0.0% | Calculado |
| `co2_inyectado_m3` | DOUBLE | 0.0% | Calculado |
| `presion_maxima_psi` | DOUBLE | 0.0% | Calculado |
| `potencia_equipos_fractura_hp` | DOUBLE | 0.0% | Calculado |
| `fecha_inicio_fractura` | DATE | 0.0% | Calculado |
| `fecha_fin_fractura` | DATE | 0.0% | Calculado |
| `fecha_data` | TIMESTAMP | 0.0% | Calculado |
| `anio_if` | BIGINT | 0.0% | Calculado |
| `mes_if` | BIGINT | 0.0% | Calculado |
| `anio_ff` | BIGINT | 0.0% | Calculado |
| `mes_ff` | BIGINT | 0.0% | Calculado |
| `anio_carga` | BIGINT | 0.0% | Calculado |
| `mes_carga` | BIGINT | 0.0% | Calculado |
| `empresa_informante` | VARCHAR | 0.0% | Calculado |
| `mes` | BIGINT | 0.0% | Calculado |
| `anio` | BIGINT | 0.0% | Calculado |

## Primeras Filas (Muestra)

```text
   id_base_fractura_adjiv  idpozo                sigla    cuenca areapermisoconcesion          yacimiento formacion_productiva
0                      30  159910   APS.Nq.ADC.xp-1033  NEUQUINA       AGUA DEL CAJON      AGUA DEL CAJON           los molles
1                      31  159910   APS.Nq.ADC.xp-1033  NEUQUINA       AGUA DEL CAJON      AGUA DEL CAJON           los molles
2                      37  159219  YPF.Nq.AdlA-1001(h)  NEUQUINA   AGUADA DE LA ARENA  AGUADA DE LA ARENA          vaca muerta
3                      38  159220  YPF.Nq.AdlA-1002(h)  NEUQUINA   AGUADA DE LA ARENA  AGUADA DE LA ARENA          vaca muerta
4                      39  159221  YPF.Nq.AdlA-1003(h)  NEUQUINA   AGUADA DE LA ARENA  AGUADA DE LA ARENA          vaca muerta
```

## Observaciones y Aptitud para Cruces

- **Claves identificadas:** `id_base_fractura_adjiv`, `idpozo`, `sigla`, `cantidad_fracturas`
- **Duplicados por clave principal:** 0
- **Aptitud para cruce con core.dim_pozo:** Candidatos: ['id_base_fractura_adjiv', 'idpozo', 'sigla', 'cantidad_fracturas']
- **Aptitud para visualizaciones del plan:** Apto para Escena 6 (Cómo cambió el pozo: longitud horizontal, etapas, arena)
- **Observaciones metodológicas:** Total fracturas registradas: 4,922
