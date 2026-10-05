# Plan de Implementación — Proyecto Visual de Petróleo en Argentina

## 0. Objetivo general

Construir una plataforma web de visualización de datos sobre la evolución del petróleo en Argentina, con foco en explicar **cómo cambió la producción, qué rol tuvo el desarrollo no convencional, cómo evolucionaron la perforación y la productividad, y qué relación observable existe con inversión, reservas, empleo, refinación, comercio exterior e impactos operativos/ambientales medibles**.

La meta NO es hacer un dashboard genérico.

La meta es construir una **historia visual basada en datos**, reproducible, verificable y defendible metodológicamente, apta para presentar en un concurso de visualización de datos.

Título de trabajo:

> **Argentina vuelve a producir petróleo: ¿qué cambió?**

Subtítulo posible:

> **Del pozo al país: 75 años de producción, expansión territorial, inversión, empleo y comercio energético.**

---

# 1. Principios obligatorios del proyecto

1. No inventar datos.
2. No completar huecos con supuestos sin documentarlos.
3. Mantener siempre la fuente original de cada dato.
4. Diferenciar claramente:
   - dato observado;
   - dato calculado;
   - estimación;
   - proyección;
   - inferencia.
5. Toda métrica calculada debe tener fórmula documentada.
6. Toda transformación debe ser reproducible por código.
7. No depender de URLs internas frágiles si puede descubrirse el recurso por API/catalogo.
8. Si una descarga falla:
   - NO ignorarla;
   - registrar el error;
   - intentar fuente alternativa;
   - dejar constancia del dataset faltante.
9. No reemplazar una fuente oficial por una secundaria silenciosamente.
10. Si se usa PetroDB, Hugging Face, GitHub, Kaggle u otra fuente secundaria, conservar la relación con la fuente primaria oficial.

---

# 2. Infraestructura objetivo

El proyecto se desplegará en dos servidores separados.

## Servidor APP

Responsabilidades:

- frontend web;
- backend/API;
- generación de visualizaciones;
- mapas;
- endpoints de consulta;
- caché si fuera necesario;
- archivos estáticos;
- documentación técnica.

Stack sugerido:

- Frontend:
  - React / Next.js o equivalente;
  - D3.js;
  - Observable Plot;
  - MapLibre GL JS;
  - Deck.gl para capas de muchos puntos si hace falta;
  - ECharts o Plotly solo para gráficos donde simplifique el desarrollo.
  - La visualicacion tiene que ser un mapa que muestre una historia y responda preguntas ejemplo
  https://jsantarelli.github.io/649/public/
  https://milla201.com/

- Backend:
  - FastAPI o Node.js;
  - preferencia por FastAPI si el ETL/análisis principal se hace en Python.

## Servidor DB

Responsabilidades:

- datos crudos catalogados;
- datos normalizados;
- tablas analíticas;
- geometrías;
- agregaciones;
- materialized views;
- metadatos de descarga;
- logs ETL.

Stack recomendado:

- PostgreSQL;
- PostGIS;
- opcional: TimescaleDB si resulta útil;
- DuckDB para procesamiento batch/local;
- Parquet como formato intermedio.

No guardar millones de registros en JSON dentro de PostgreSQL si existe estructura tabular clara.

---

# 3. Arquitectura de carpetas

Crear una estructura equivalente a:

```text
petroleo-argentina/
│
├── README.md
├── docs/
│   ├── datasets.md
│   ├── metodologia.md
│   ├── historia_visual.md
│   ├── diccionario_datos.md
│   ├── decisiones.md
│   └── incidencias.md
│
├── config/
│   ├── sources.yml
│   ├── database.example.env
│   └── app.example.env
│
├── data/
│   ├── raw/
│   │   ├── energia/
│   │   ├── empleo/
│   │   ├── comercio/
│   │   ├── ambiente/
│   │   ├── worldbank/
│   │   ├── petrodb/
│   │   └── external/
│   │
│   ├── staging/
│   ├── processed/
│   ├── geospatial/
│   └── manifests/
│
├── etl/
│   ├── discovery/
│   ├── download/
│   ├── transform/
│   ├── quality/
│   └── load/
│
├── analysis/
│   ├── eda/
│   ├── notebooks/
│   ├── indicators/
│   └── models/
│
├── api/
├── frontend/
├── tests/
├── logs/
└── scripts/
```

---

# 4. Inventario inicial de fuentes

Antigravity debe tratar esto como un catálogo inicial, NO como una lista rígida.

Antes de descargar, debe validar cada fuente.

---

## 4.1 Producción de petróleo y gas por pozo — FUENTE PRINCIPAL

Nombre oficial:

**Producción de petróleo y gas por pozo (Capítulo IV)**

Portal:

https://datos.gob.ar/dataset/produccion-de-petroleo-y-gas-por-pozo

Contenido esperado:

- producción mensual;
- pozo;
- yacimiento;
- concesión;
- provincia;
- petróleo;
- gas;
- agua;
- recursos convencionales/no convencionales;
- padrón de pozos;
- fechas de primera producción;
- recursos anuales.

Debe buscar y descargar todos los recursos útiles.

Prioridad:

**CRÍTICA**

Objetivo:

- tabla mensual por pozo;
- maestro de pozos;
- series por año;
- recurso no convencional;
- cualquier recurso geográfico disponible;
- diccionario/metodología si existe.

---

## 4.2 PetroDB — espejo/normalización útil

GitHub / documentación:

https://github.com/sumpalabs/petrodb

Dataset:

https://huggingface.co/datasets/sumpalabs/petrodb

Documentación Argentina detectada:

https://github.com/oskrgab/petrodb/blob/main/parquet/argentina/README.md

Objetivo:

- usar como acelerador;
- consultar Parquet;
- contrastar estructura;
- utilizar DuckDB para exploración rápida;
- NO considerar automáticamente PetroDB como reemplazo de los datos oficiales.

Contenido esperado para Argentina:

```text
wells.parquet
well_operator_history.parquet
well_events.parquet
monthly_production/
```

Validar cantidad de pozos, años y esquema.

Registrar:

- commit/hash;
- fecha de descarga;
- licencia;
- diferencias con fuente oficial.

Prioridad:

**ALTA**

---

## 4.3 Producción nacional de petróleo desde 1950

Fuente:

https://datos.gob.ar/dataset/produccion-de-petroleo-desde-1950

Objetivo:

Construir la serie histórica de largo plazo que permita abrir la historia visual:

```text
1950 → actualidad
```

Campos a identificar:

- año;
- producción;
- unidad;
- fuente/metodología.

Descargar también el documento metodológico.

Prioridad:

**ALTA**

---

## 4.4 Perforación de pozos

Fuente:

https://datos.gob.ar/dataset/perforacion-de-pozos-de-petroleo-y-gas

Contenido esperado:

- pozos terminados;
- pozos en perforación;
- metros perforados;
- empresa;
- cuenca;
- provincia;
- mes/año;
- series anteriores a 2009;
- series desde 2009.

Objetivo analítico:

Separar:

> crecimiento por más actividad

de

> crecimiento por mayor productividad.

Prioridad:

**CRÍTICA**

---

## 4.5 Datos de fractura de pozos

Buscar por nombre exacto en Datos Argentina:

**Datos de fractura de pozos de hidrocarburos - Adjunto IV**

Portal base:

https://datos.gob.ar/

No depender de una ruta profunda fija.

Variables esperadas:

- identificador de pozo;
- empresa;
- formación;
- yacimiento;
- concesión;
- provincia;
- longitud horizontal;
- cantidad de etapas;
- toneladas de arena;
- agua;
- presión;
- fechas;
- tipo de terminación.

Objetivo:

Relacionar diseño técnico con productividad.

Prioridad:

**CRÍTICA**

---

## 4.6 Reservas de petróleo y gas

Buscar por nombre:

**Reservas de petróleo y gas**

Portal:

https://datos.gob.ar/

Objetivo:

- reservas comprobadas;
- probables;
- posibles;
- recursos;
- provincia;
- cuenca;
- concesión;
- yacimiento;
- año.

Indicadores posibles:

```text
R/P = reservas comprobadas / producción anual
```

Prioridad:

**ALTA**

---

## 4.7 Inversiones upstream

Fuente validada:

https://datos.gob.ar/dataset/inversiones-en-mercado-de-hidrocarburos-upstream

Contenido esperado:

- inversión prevista;
- inversión realizada;
- inversión mensual;
- empresa;
- año;
- recursos históricos.

Objetivo:

Explorar:

```text
inversión(t)
    ↓
perforación(t + lag)
    ↓
producción(t + lag)
```

No asumir causalidad.

Prioridad:

**MEDIA/ALTA**

---

## 4.8 Refinación y comercialización

Buscar por nombre exacto:

**Refinación y Comercialización de petróleo, gas y derivados (Tablas Dinámicas)**

Portal:

https://datos.gob.ar/

Buscar recursos de:

- petróleo procesado;
- refinerías;
- importaciones;
- exportaciones;
- ventas;
- existencias;
- subproductos;
- compras;
- consumo propio.

Objetivo:

Contar qué ocurre después de la extracción.

Pregunta posible:

> ¿La capacidad de producción creció al mismo ritmo que la capacidad de procesamiento?

Prioridad:

**ALTA**

---

## 4.9 Empleo registrado

Buscar en Datos Argentina:

**Puestos de trabajo asalariados registrados por provincia y sector de actividad**

Portal:

https://datos.gob.ar/

Objetivo:

- Neuquén;
- extracción de petróleo y gas;
- construcción;
- transporte;
- servicios;
- otras actividades asociadas.

Serie mensual deseable:

2007 → actualidad.

Importante:

No llamar automáticamente a esto "empleo generado por Vaca Muerta".

Hablar de:

> evolución del empleo en sectores relacionados durante el período de expansión.

Causalidad solo si existe metodología suficiente.

Prioridad:

**ALTA**

---

## 4.10 Empleo por departamento/partido

Buscar por nombre:

**Puestos de trabajo por departamento/partido y sector de actividad**

Portal:

https://datos.gob.ar/

Objetivo:

Acercarse geográficamente a:

- Añelo;
- departamentos petroleros;
- comparación territorial.

Prioridad:

**MEDIA/ALTA**

---

## 4.11 Puntos de venteo

Buscar por nombre exacto:

**Producción de hidrocarburos - Puntos de venteo declarados**

Portal:

https://datos.gob.ar/

Objetivo:

Construir capa geográfica.

Esperado:

- CSV;
- SHP;
- coordenadas;
- instalaciones/puntos.

No asumir volumen de emisiones salvo que el dataset efectivamente lo contenga.

Prioridad:

**MEDIA**

---

## 4.12 Instalaciones de hidrocarburos

Buscar por nombre:

**Instalaciones de hidrocarburos - Instalaciones Res. 319/1993 y puntos característicos**

Portal:

https://datos.gob.ar/

Objetivo:

Mapa de infraestructura.

Prioridad:

**MEDIA**

---

## 4.13 Gas flaring satelital — World Bank

Fuente:

https://www.worldbank.org/en/programs/gasflaringreduction/global-flaring-data

Objetivo:

Obtener:

- flare locations;
- volumen estimado;
- año;
- coordenadas;
- Argentina;
- 2012 en adelante si está disponible.

Cruzar espacialmente con:

- pozos;
- yacimientos;
- concesiones;
- producción.

No asumir que una antorcha pertenece a un pozo particular salvo que la proximidad y metodología lo permitan.

Prioridad:

**ALTA para historia ambiental**
**MEDIA si el foco final queda puramente económico/productivo**

---

## 4.14 Emisiones GEI

Buscar en Datos Argentina:

**Emisiones de gases de efecto invernadero (GEI)**

Portal:

https://datos.gob.ar/

Objetivo:

Contexto sectorial nacional.

No usar para atribución a pozo individual.

Prioridad:

**BAJA/MEDIA**

---

## 4.15 World Bank — contexto macro

Oil rents:

https://data.worldbank.org/indicator/NY.GDP.PETR.RT.ZS

Fuel imports:

https://data.worldbank.org/indicator/TM.VAL.FUEL.ZS.UN

Nota: usar la página general del indicador y filtrar Argentina dentro de World Bank Data. Evitar depender del parámetro `?locations=AR` si el navegador/red lo resuelve con error.

Fuel exports:

https://data.worldbank.org/indicator/TX.VAL.FUEL.ZS.UN

Uso:

Contexto internacional o macro.

No reemplazar estadísticas argentinas más granulares si existen.

Prioridad:

**BAJA/MEDIA**

---

# 5. Estrategia de descubrimiento de datasets

No depender solamente de URLs pegadas manualmente.

Datos Argentina utiliza CKAN, pero **la URL base de la API no es una página navegable útil por sí sola**.

Documentación oficial de CKAN de Datos Argentina:

https://www.datos.gob.ar/acerca/ckan

Usar endpoints completos únicamente después de resolver el ID real del dataset.

Formato documentado oficialmente para obtener metadatos de un dataset:

```text
http://datos.gob.ar/api/3/action/package_show?id=<id_del_dataset>
```

Formato documentado oficialmente para consultar un recurso que esté publicado en el DataStore:

```text
http://datos.gob.ar/api/3/action/datastore_search?resource_id=<id_del_recurso>
```

Ejemplo de flujo recomendado:

```text
1. Abrir o descubrir la página pública del dataset.
2. Obtener el ID/slug real del dataset.
3. Probar package_show con ese ID.
4. Leer la lista de resources devuelta por CKAN.
5. Descargar directamente la URL real de cada CSV/ZIP/SHP.
6. Usar datastore_search solamente si ese recurso soporta DataStore.
```

No usar como URL de descarga:

```text
https://datos.gob.ar/api/3/action/
```

porque es solo la raíz conceptual de los endpoints y no identifica ninguna acción ni dataset.

Para búsqueda automática, Antigravity puede intentar `package_search`, por ejemplo:

```text
http://datos.gob.ar/api/3/action/package_search?q=petroleo
```

pero debe validar que la respuesta sea JSON válido antes de continuar.

IMPORTANTE:

- No asumir que todos los datasets soportan `datastore_search`.
- No asumir que el slug visible en la URL pública es necesariamente el mismo ID interno de CKAN.
- Preferir siempre las URLs de recursos que devuelve `package_show`.
- Si CKAN devuelve error, HTML, timeout o un recurso inexistente, hacer fallback a la página pública del dataset.

Si CKAN API no responde:

1. registrar error;
2. intentar la página pública del catálogo;
3. extraer desde allí las URLs reales de descarga;
4. buscar fuente oficial alternativa;
5. NO ocultar el fallo.

---

# 6. Archivo de configuración de fuentes

Crear:

```text
config/sources.yml
```

Formato mínimo:

```yaml
sources:
  - id: produccion_pozo_cap4
    name: Producción de petróleo y gas por pozo (Capítulo IV)
    publisher: Secretaría de Energía
    catalog_url: https://datos.gob.ar/dataset/produccion-de-petroleo-y-gas-por-pozo
    discovery_method: ckan
    priority: critical
    required: true

  - id: petrodb
    name: PetroDB Argentina
    publisher: Sumpa Labs
    catalog_url: https://huggingface.co/datasets/sumpalabs/petrodb
    discovery_method: huggingface
    priority: high
    required: false
```

No hardcodear cientos de resource URLs si CKAN las puede resolver dinámicamente.

---

# 7. Descarga reproducible

Cada archivo descargado debe generar metadata.

Crear para cada recurso:

```json
{
  "source_id": "produccion_pozo_cap4",
  "resource_name": "...",
  "original_url": "...",
  "downloaded_at": "...",
  "http_status": 200,
  "content_type": "...",
  "size_bytes": 12345,
  "sha256": "...",
  "local_path": "...",
  "success": true
}
```

Guardar manifests en:

```text
data/manifests/
```

---

# 8. Política de errores

Crear:

```text
logs/download_errors.jsonl
logs/etl_errors.jsonl
docs/incidencias.md
```

Cada error debe incluir:

```json
{
  "timestamp": "...",
  "source_id": "...",
  "url": "...",
  "stage": "download",
  "error_type": "HTTP_404",
  "message": "...",
  "retry_count": 3,
  "resolved": false,
  "fallback_used": null
}
```

Nunca considerar un ETL correcto si falta un dataset marcado `required: true`.

Al finalizar cada ejecución producir un resumen:

```text
OK: 12
WARNING: 3
FAILED: 2
```

y listar exactamente cuáles fallaron.

---

# 9. Validaciones obligatorias

Para cada archivo:

## Integridad física

- archivo existe;
- tamaño > 0;
- checksum;
- descompresión correcta;
- encoding válido.

## Esquema

- columnas detectadas;
- tipos inferidos;
- duplicados;
- nulos;
- rango temporal;
- filas;
- unidades.

## Geografía

- coordenadas dentro de Argentina cuando corresponda;
- CRS detectado;
- lat/lon válidos;
- geometrías reparables;
- no intercambiar latitud/longitud silenciosamente.

## Series temporales

- meses faltantes;
- años faltantes;
- duplicados por clave;
- huecos inesperados.

---

# 10. Perfil automático de cada dataset

Generar:

```text
docs/profiles/<source_id>.md
```

Debe incluir:

- nombre;
- fuente;
- fecha;
- filas;
- columnas;
- tamaño;
- cobertura temporal;
- cobertura geográfica;
- porcentaje de nulos;
- claves candidatas;
- duplicados;
- unidades;
- primeras 10 filas;
- observaciones;
- aptitud para cruces;
- nivel de confianza.

---

# 11. Modelo de datos propuesto

Esquema PostgreSQL/PostGIS:

```text
raw
staging
core
analytics
app
meta
```

---

## 11.1 core.dim_pozo

Campos deseables:

```text
id_pozo
sigla
empresa_actual
cuenca
provincia
yacimiento
concesion
formacion
tipo_recurso
tipo_pozo
lat
lon
geom
fecha_primera_produccion
```

---

## 11.2 core.fact_produccion_pozo_mes

```text
id_pozo
fecha
anio
mes
prod_pet_m3
prod_gas_miles_m3
prod_agua_m3
dias_produccion
```

PK tentativa:

```text
(id_pozo, fecha)
```

Validar antes.

---

## 11.3 core.fact_fractura_pozo

```text
id_pozo
fecha
longitud_horizontal_m
etapas
arena_tn
agua_m3
presion
tipo_terminacion
```

---

## 11.4 core.fact_perforacion

```text
fecha
empresa
provincia
cuenca
pozos_terminados
pozos_en_perforacion
metros_perforados
```

---

## 11.5 core.fact_inversion

```text
fecha
empresa
tipo
inversion_usd
fuente
```

No asumir moneda/unidad.

Validar metadatos.

---

## 11.6 core.fact_reservas

```text
anio
provincia
cuenca
yacimiento
concesion
reservas_comprobadas
reservas_probables
reservas_posibles
recursos
unidad
```

---

## 11.7 core.fact_empleo

```text
fecha
provincia
departamento
sector
puestos
```

---

## 11.8 core.fact_comercio_energia

```text
fecha
producto
tipo_operacion
volumen
valor_usd
unidad
```

---

# 12. Claves de cruce

Construir y documentar un mapa real de relaciones.

Prioridad:

```text
id_pozo
```

Luego:

```text
empresa
yacimiento
concesion
cuenca
provincia
fecha
```

Nunca unir por nombre textual sin normalizar y medir tasa de match.

Para cada join importante generar:

```text
match_rate
unmatched_left
unmatched_right
duplicated_keys
```

Ejemplo:

```text
fracturas ↔ producción

match_rate = 93.4%
```

El valor real debe calcularse.

---

# 13. Indicadores derivados

Crear solo después de validar datos.

---

## 13.1 Producción nacional anual

```text
SUM(prod_pet_m3)
```

---

## 13.2 Participación no convencional

```text
produccion_no_convencional
/
produccion_total
```

---

## 13.3 Pozos activos

Definir explícitamente qué significa "activo".

Ejemplo tentativo:

```text
prod_pet > 0 OR prod_gas > 0
```

No implementar sin revisar semántica del dataset.

---

## 13.4 Producción por pozo activo

```text
produccion_total_mes / pozos_activos_mes
```

---

## 13.5 Producción inicial

Analizar:

- mes 1;
- primeros 3 meses;
- primeros 6 meses;
- primeros 12 meses.

Evitar usar un único mes si es muy ruidoso.

---

## 13.6 Producción acumulada por edad

Normalizar cada pozo:

```text
mes_vida = meses_desde_primera_produccion
```

Permitir curvas:

```text
cohorte 2015
cohorte 2018
cohorte 2021
cohorte 2024
```

---

## 13.7 Intensidad de perforación

```text
metros_perforados
pozos_terminados
```

---

## 13.8 Productividad física

Explorar métricas como:

```text
produccion_12m / longitud_horizontal
produccion_12m / etapas
produccion_12m / arena_tn
```

Advertencia:

Estas métricas NO equivalen automáticamente a eficiencia económica.

---

## 13.9 R/P

```text
reservas_comprobadas / produccion_anual
```

Documentar unidad.

---

# 14. EDA obligatorio antes de diseñar la historia

No diseñar la narrativa final antes de ejecutar EDA.

Generar un reporte:

```text
analysis/eda/eda_v1.md
```

Debe responder:

1. ¿Cuándo comienza a crecer fuertemente la producción no convencional?
2. ¿Qué provincias explican el crecimiento?
3. ¿Qué yacimientos explican el crecimiento?
4. ¿Cuántos pozos explican X% de la producción?
5. ¿Cambió la productividad por pozo?
6. ¿Cambió la longitud horizontal?
7. ¿Cambió el número de etapas?
8. ¿Cambió la producción de los primeros 12 meses?
9. ¿Más pozos o mejores pozos explican el crecimiento?
10. ¿Cómo evolucionó la perforación?
11. ¿Cómo evolucionaron las reservas?
12. ¿Cómo evolucionó la inversión?
13. ¿Cómo evolucionó el empleo en Neuquén?
14. ¿Cómo evolucionaron importaciones/exportaciones?
15. ¿Hay eventos/anomalías que deban explicarse?
16. ¿Existen diferencias fuertes entre operadores?
17. ¿Existen diferencias fuertes entre yacimientos?
18. ¿Qué hallazgo NO era obvio antes de procesar los datos?

---

# 15. Hipótesis a probar

Estas son preguntas, NO conclusiones.

## H1

> El crecimiento reciente de la producción argentina no se explica únicamente por una mayor cantidad de pozos.

Probar con:

```text
cantidad de pozos
vs
producción por pozo/cohorte
```

---

## H2

> Las generaciones recientes de pozos presentan perfiles de producción diferentes a las anteriores.

Probar curvas por cohorte.

---

## H3

> El diseño técnico del pozo cambió junto con la productividad.

Probar:

```text
longitud horizontal
etapas
arena
vs
producción 6/12/24 meses
```

---

## H4

> La geografía de la producción argentina se concentró progresivamente en determinadas áreas.

Probar con mapas y participación por provincia/yacimiento.

---

## H5

> La expansión productiva coincide temporalmente con cambios observables en empleo, inversión y comercio energético.

IMPORTANTE:

Coincidencia temporal ≠ causalidad.

---

# 16. Estructura visual preliminar

La plataforma debe estar pensada como una historia.

No como menú con 30 gráficos.

---

# Escena 1 — 75 años de petróleo

Título:

> **Argentina produce petróleo desde mucho antes de Vaca Muerta. Pero su geografía y su forma de producir cambiaron.**

Visual:

Serie histórica:

```text
1950 ───────────────────────────── actualidad
```

Mostrar:

- producción anual;
- máximos/mínimos;
- hitos;
- inicio del desarrollo no convencional.

Interacción:

hover + anotaciones.

---

# Escena 2 — El mapa se mueve

Mapa temporal.

Mostrar pozos/producción:

```text
2006
2010
2014
2018
2022
2025
```

Usar:

- puntos;
- clusters;
- hexbin;
- densidad;
- yacimientos.

Objetivo:

Ver cómo cambia espacialmente la producción.

---

# Escena 3 — Convencional vs no convencional

Visual:

área/stream/stacked chart.

Pregunta:

> ¿Cuándo empieza el no convencional a cambiar la curva nacional?

---

# Escena 4 — Más pozos o mejores pozos

Esta puede convertirse en la escena central.

Descomponer:

```text
Producción
   =
cantidad de pozos
   ×
producción media por pozo
```

Mostrar ambos componentes a través del tiempo.

Objetivo:

Encontrar qué explica el crecimiento.

---

# Escena 5 — La vida de un pozo

Curvas de cohortes.

```text
mes 0
mes 6
mes 12
mes 24
mes 36
```

Comparar:

```text
2012
2016
2020
2024
```

Mediana y percentiles.

No usar solamente promedios si existen outliers fuertes.

---

# Escena 6 — Cómo cambió el pozo

Mostrar:

- longitud horizontal;
- etapas;
- arena;
- producción inicial;
- producción acumulada 12m.

Ideal:

scatter plots / distributions / small multiples.

---

# Escena 7 — Del pozo al país

Alejar la escala.

Mostrar temporalmente:

```text
producción
inversión
empleo
reservas
exportaciones/importaciones
```

No apilar métricas incompatibles en el mismo eje.

Preferir small multiples sincronizados.

---

# Escena 8 — Infraestructura / ambiente

Opcional según datos.

Mostrar:

- instalaciones;
- venteo;
- flaring satelital;
- producción.

Debe estar metodológicamente documentado.

---

# Escena 9 — Qué aprendimos

No escribir conclusión hasta completar EDA.

La aplicación debe construir la conclusión a partir de hallazgos reales.

---

# 17. Primera versión visual mínima

Antes de construir toda la app, generar un prototipo con solo 4 piezas:

```text
1. Producción Argentina 1950-actualidad
2. Mapa temporal de pozos 2006-actualidad
3. Convencional vs no convencional
4. Cohortes de producción por edad del pozo
```

Si estas cuatro piezas no cuentan una historia coherente, revisar el enfoque antes de seguir.

---

# 18. APIs internas sugeridas

Ejemplos:

```text
GET /api/timeline/production
GET /api/map/wells?year=2024
GET /api/production/type
GET /api/cohorts?start_year=2015&end_year=2024
GET /api/wells/{id}
GET /api/fracture/trends
GET /api/investment/timeline
GET /api/employment/timeline
GET /api/trade/timeline
GET /api/reserves/timeline
```

No enviar millones de puntos al navegador.

Para mapas usar:

- tiles;
- MVT;
- agregaciones;
- clustering;
- hexbin;
- simplificación.

---

# 19. Views/materialized views sugeridas

```text
analytics.mv_produccion_nacional_mes
analytics.mv_produccion_provincia_mes
analytics.mv_produccion_tipo_recurso_mes
analytics.mv_pozos_activos_mes
analytics.mv_cohortes_pozo
analytics.mv_productividad_cohorte
analytics.mv_fractura_anio
analytics.mv_perforacion_anio
analytics.mv_reservas_anio
analytics.mv_empleo_petroleo_mes
analytics.mv_comercio_energia_mes
```

---

# 20. Performance

DB:

- índices por fecha;
- índices por id_pozo;
- GiST sobre geom;
- particionar fact_produccion por año si mejora performance;
- evitar consultas completas en runtime.

Frontend:

- lazy load;
- tiles;
- precálculo;
- caché;
- no renderizar decenas de miles de SVG individuales.

---

# 21. Calidad visual

La identidad visual debe sentirse editorial, no corporativa.

Evitar:

- grillas llenas de KPIs;
- 20 tarjetas;
- gauges;
- tortas innecesarias;
- sombras exageradas;
- estilo Power BI por defecto.

Priorizar:

- mapas;
- líneas;
- áreas;
- distribuciones;
- anotaciones;
- transiciones temporales;
- scrollytelling;
- tipografía limpia;
- narrativa progresiva.

---

# 22. Documentación metodológica

Crear:

```text
docs/metodologia.md
```

Debe explicar:

- fuentes;
- fechas de descarga;
- variables;
- unidades;
- limpieza;
- exclusiones;
- joins;
- tasas de match;
- fórmulas;
- definición de pozo activo;
- definición convencional/no convencional;
- definición de cohortes;
- conversión de unidades;
- tratamiento de nulos;
- tratamiento de outliers;
- limitaciones.

---

# 23. Informe de viabilidad automático

Al finalizar la fase de ingesta generar:

```text
docs/viabilidad.md
```

Formato:

```text
## Dataset: producción por pozo

Estado: OK

Cobertura: 2006-2025
Filas: X
Pozos únicos: X
Nulos críticos: X%
Geografía: OK
Join con fracturas: X%
Join con padrón: X%

Apto:
- mapa temporal: sí
- cohortes: sí
- productividad: sí

Problemas:
- ...
```

Repetir por dataset.

---

# 24. Informe final de descargas

Crear:

```text
docs/descargas.md
```

Debe listar TODOS los datasets:

| Dataset | Estado | Fuente | Archivo | Filas | Cobertura | Observaciones |
|---|---|---|---|---:|---|---|
| Producción por pozo | OK | Secretaría Energía | ... | ... | ... | ... |
| Fracturas | FAILED | ... | - | - | - | HTTP 404 |
| Reservas | OK | ... | ... | ... | ... | ... |

Si algo falla, mostrarlo.

NO esconder datasets fallidos.

---

# 25. Backups y reproducibilidad

Guardar:

- manifests;
- checksums;
- SQL migrations;
- esquema;
- seeds mínimos;
- scripts de actualización.

Nunca depender exclusivamente de una descarga manual.

---

# 26. Actualizaciones

Diseñar un comando:

```bash
python -m etl.run --all
```

o equivalente.

Y comandos parciales:

```bash
python -m etl.run --source produccion_pozo_cap4
python -m etl.run --source perforacion
python -m etl.run --source fracturas
```

Opcional:

```bash
python -m etl.run --only-new
```

---

# 27. Logs

Cada corrida:

```text
logs/run_YYYYMMDD_HHMMSS.log
```

Debe reportar:

- dataset;
- URL resuelta;
- HTTP;
- bytes;
- filas;
- duración;
- validaciones;
- inserts;
- updates;
- errores.

---

# 28. Fases de implementación

## Fase 1 — Descubrimiento

Objetivo:

Resolver URLs reales y recursos.

Entregables:

```text
sources.yml
datasets.md
```

---

## Fase 2 — Descarga

Objetivo:

Descargar raw sin modificar.

Entregables:

```text
data/raw/
data/manifests/
descargas.md
```

---

## Fase 3 — Perfilado

Objetivo:

Entender calidad y estructura.

Entregables:

```text
docs/profiles/
docs/viabilidad.md
```

---

## Fase 4 — Base de datos

Objetivo:

Cargar staging/core.

Entregables:

- migrations;
- schema;
- índices;
- PostGIS.

---

## Fase 5 — EDA

Objetivo:

Encontrar la historia real.

Entregable:

```text
analysis/eda/eda_v1.md
```

---

## Fase 6 — Storyboard

Solo después del EDA.

Entregable:

```text
docs/historia_visual.md
```

Debe indicar:

```text
escena
pregunta
dataset
métrica
gráfico
mensaje
limitación
```

---

## Fase 7 — MVP web

Implementar:

1. serie 1950-presente;
2. mapa temporal;
3. convencional/no convencional;
4. cohortes.

---

## Fase 8 — Capas macro

Agregar:

- inversión;
- empleo;
- reservas;
- comercio;
- infraestructura/ambiente.

Solo si pasan validación.

---

# 29. Restricciones metodológicas

No usar frases como:

> Vaca Muerta generó X empleos.

salvo análisis causal válido.

Preferir:

> El empleo registrado del sector evolucionó de X a Y durante el período en que la producción pasó de A a B.

No afirmar:

> las fracturas más largas son más rentables.

si solo medimos producción.

Preferir:

> los pozos con mayor longitud horizontal muestran X comportamiento productivo.

No inferir rentabilidad si no existen costos sólidos.

---

# 30. Resultado esperado para Antigravity

Al terminar la primera gran ejecución, NO quiero solamente archivos descargados.

Quiero recibir:

```text
1. Inventario completo de fuentes
2. Qué descargó
3. Qué falló
4. Por qué falló
5. Qué fallback usó
6. Cantidad de filas
7. Cobertura temporal
8. Cobertura geográfica
9. Columnas clave
10. Calidad
11. Tasa de cruce entre datasets
12. Hallazgos preliminares
13. Qué visualizaciones son viables
14. Qué preguntas NO se pueden responder
15. Recomendación de historia visual
```

---

# 31. Criterio de éxito

El proyecto está listo para pasar a diseño visual cuando podamos responder con datos:

> **¿Qué cambió estructuralmente en la producción petrolera argentina y cómo se manifiesta ese cambio desde el pozo hasta el país?**

Y tengamos evidencia suficiente para construir al menos:

- una serie histórica;
- un mapa temporal;
- una comparación convencional/no convencional;
- una comparación por cohortes;
- un análisis de productividad;
- una conexión macroeconómica/territorial defendible.

---

# 32. Instrucción final para Antigravity

Trabajar primero en modo de **descubrimiento, descarga, validación y análisis**.

No diseñar conclusiones antes de procesar los datos.

No modificar datos raw.

No eliminar fuentes fallidas del inventario.

No convertir hipótesis en hechos.

Toda afirmación que luego se use en la aplicación debe poder trazarse hasta:

```text
fuente
→ archivo
→ transformación
→ consulta
→ métrica
→ visualización
```

El objetivo no es producir muchas gráficas.

El objetivo es encontrar una historia que **los datos realmente demuestren** y luego construir una visualización de calidad suficiente para competir en un concurso nacional de visualización de datos.
