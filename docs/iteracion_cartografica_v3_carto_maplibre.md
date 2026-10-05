# Iteración cartográfica V3 — CARTO autenticado, MapLibre 3D y refinamiento editorial

## Objetivo

Realizar una nueva iteración del frontend enfocada exclusivamente en:

1. corregir la integración con CARTO;
2. eliminar el watermark/error `API KEY REQUIRED`;
3. mantener MapLibre GL JS como motor cartográfico;
4. mejorar el terreno 3D real;
5. refinar el basemap y la lectura geográfica;
6. auditar la precisión de las geometrías;
7. simplificar la interfaz y el lenguaje;
8. mejorar tipografía, jerarquía y composición;
9. reforzar la experiencia map-first;
10. mantener intactos los datos y hallazgos ya auditados.

No modificar cifras, datasets, queries, endpoints, conclusiones auditadas ni estructura narrativa.

Esta iteración es de:

```text
CARTOGRAFÍA + DISEÑO + INTERACCIÓN + AUTENTICACIÓN
```

---

# 1. Seguridad del token CARTO

Tengo disponible un API Access Token de CARTO.

El token real NO debe:

- hardcodearse dentro de `frontend/app.js`;
- quedar versionado;
- aparecer en commits;
- aparecer en documentación;
- imprimirse en consola;
- aparecer en screenshots;
- almacenarse en archivos públicos.

Crear:

```text
frontend/config.example.js
```

con:

```js
window.APP_CONFIG = {
  CARTO_TOKEN: "",
  CARTO_API_BASE: ""
};
```

Crear localmente:

```text
frontend/config.js
```

con el token real.

Agregar a `.gitignore`:

```text
frontend/config.js
```

El HTML debe cargar `config.js` antes de `app.js`.

Si `config.js` no existe o el token está vacío:

- no romper la aplicación;
- activar un fallback cartográfico;
- registrar solo un warning genérico;
- jamás mostrar el token.

---

# 2. Alcance mínimo del token

Configuración CARTO recomendada:

```text
Maps API: ON
SQL API: OFF inicialmente
Exports API: OFF
LDS API: OFF
MCP Server: OFF
```

Si alguna funcionalidad necesita SQL API:

1. documentar por qué;
2. activarla solo si es necesaria;
3. no habilitarla por comodidad.

No usar `Allow access to all sources` si no hace falta.

Preferir grants específicos:

```text
Table, Tileset, Raster source or Pattern
```

y limitar el acceso a los recursos de este proyecto.

---

# 3. Restricción por origen

Configurar `Allowed Referers URLs`.

Desarrollo:

```text
http://127.0.0.1:8000
http://localhost:8000
```

Producción:

```text
https://<dominio-definitivo>
```

Documentar en:

```text
docs/carto_auth.md
```

sin incluir secretos.

---

# 4. Corregir el watermark actual

Actualmente el mapa muestra repetidamente:

```text
API KEY REQUIRED
carto.com/basemaps/apikey
```

No ocultarlo mediante CSS.

Identificar exactamente qué `source`, `layer` o URL de tiles lo produce.

Revisar Network y documentar:

```text
request URL
HTTP status
source id
layer id
```

Resultado esperado:

```text
HTTP 200
sin 401
sin 403
sin API KEY REQUIRED
```

---

# 5. Arquitectura cartográfica final

Mantener:

```text
MapLibre GL JS
```

Arquitectura:

```text
BASEMAP VECTORIAL
        +
TERRAIN DEM
        +
HILLSHADE
        +
DATOS DEL PROYECTO
```

Separar responsabilidades.

- CARTO: basemap/tiles si aporta valor.
- DEM: relieve.
- API propia: datos del proyecto.
- PostgreSQL/PostGIS: base principal cuando se despliegue en servidores.

No subir automáticamente todos los datos a CARTO.

---

# 6. Fallback cartográfico

Si CARTO falla, usar un fallback vectorial sin autenticación.

Referencia permitida:

```text
https://tiles.openfreemap.org/styles/liberty
```

No usar Liberty visualmente tal cual.

Crear:

```text
frontend/styles/petroleo-map-style.json
```

con estilo propio.

La app debe iniciar aunque CARTO no esté disponible.

---

# 7. Basemap propio

El mapa actual se siente demasiado oscuro, borroso y monocromático.

Debe mostrar con claridad:

- costa;
- provincias;
- países limítrofes;
- ciudades importantes;
- rutas principales;
- ríos principales;
- cuerpos de agua;
- relieve;
- topografía;
- cuencas cuando corresponda.

No saturar con POIs urbanos.

---

# 8. Paleta del mapa

Dirección visual sugerida:

```text
agua:               #13212A
tierra baja:         #262720
meseta:              #34352C
elevación media:     #504C40
relieve alto:        #706856

límites provinciales:
rgba(235,229,207,0.18)

fronteras nacionales:
rgba(235,229,207,0.30)

rutas:
rgba(220,211,185,0.13)

ciudades:
rgba(235,231,215,0.58)

labels secundarios:
rgba(235,231,215,0.32)

convencional:        #C98B32
no convencional:     #39AFCF
highlight:           #E3B55A
```

No usar:

- gris uniforme;
- cyan dominante;
- violeta;
- glow tech;
- gradientes artificiales.

---

# 9. Terreno 3D

Mantener terrain vía DEM.

Proveedor actual:

```text
AWS Terrarium
https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png
```

Encoding:

```text
terrarium
```

Exageración recomendada:

```text
1.15 – 1.30
```

Valor inicial:

```text
1.22
```

No exagerar sin prueba visual.

---

# 10. Comparar DEM

Realizar comparación A/B entre AWS Terrarium y otra fuente DEM compatible con MapLibre si está disponible.

Evaluar especialmente:

- Cordillera;
- Neuquén;
- Añelo;
- meseta patagónica.

Generar:

```text
dem_aws.png
dem_alternativo.png
```

No cambiar de proveedor por intuición.

---

# 11. Hillshade

Ajustar:

- shadow color;
- highlight color;
- accent color;
- illumination direction;
- exaggeration.

Comparar:

```text
300°
315°
330°
```

Elegir la iluminación que haga más legible Patagonia/Neuquén.

---

# 12. Cámara por capítulo

El 3D debe aparecer progresivamente.

```text
01 El regreso
pitch: 0–5°
bearing: 0°

02 El mapa se mueve
pitch: 18–24°
bearing: -5°

03 El punto de quiebre
pitch: 30–36°
bearing: 8°

04 Pocos pozos, mucho petróleo
pitch: 36–42°
bearing: 12°

05 Cómo cambió el pozo
pitch: 52–58°
bearing: -20°

06 Generaciones de pozos
pitch: 36–42°
bearing: 8°

07 Del pozo al país
pitch: 22–28°
bearing: -5°

08 Un nuevo mapa petrolero
pitch: 0–8°
bearing: 0°
```

---

# 13. Transiciones cinematográficas

Usar el cambio de cámara para narrar.

Ejemplo:

```text
Argentina
↓
Patagonia
↓
Neuquén
↓
Cuenca Neuquina
```

Durante la transición:

```text
zoom ↑
pitch ↑
detalle ↑
labels locales ↑
```

Duración sugerida:

```text
1200–2200 ms
```

---

# 14. Capítulo 05 como momento 3D principal

Mapa:

```text
Añelo / Vaca Muerta
```

Mostrar:

- relieve;
- locaciones;
- pozos;
- trayectorias horizontales seleccionadas.

No mostrar miles de trayectorias a la vez.

---

# 15. Trayectorias

Cuando se seleccione un pozo, representar conceptualmente:

```text
superficie
    ●
    │
    │
    ╰━━━━━━━━━━━━━━━━
```

La rama horizontal debe usar datos reales.

No inventar TVD o profundidad vertical.

Si no existe profundidad:

- indicarlo;
- o limitarse a trayectoria horizontal geográfica.

---

# 16. Pozos

## Escala nacional

- puntos pequeños;
- opacidad controlada;
- clustering/agregación;
- tamaño visible.

## Escala regional

- puntos individuales;
- convencional/no convencional;
- hover;
- selección;
- producción.

Sin glow fuerte.

---

# 17. Pareto

Capítulo 04:

```text
26.219 pozos
→
912 pozos
→
50% de la producción
```

En mapa:

- comenzar con todos;
- atenuar progresivamente;
- dejar visibles los 912;
- acompañar con curva de Pareto.

Sin textos instructivos.

---

# 18. Auditoría de geometrías

Revisar:

```text
api/static_data/geo_basins.json
```

Para cada cuenca informar:

```text
nombre
fuente original
URL/dataset
archivo original
CRS
fecha
proceso de transformación
nivel de simplificación
```

Si algún polígono fue dibujado o aproximado manualmente:

NO presentarlo como límite real.

Marcarlo como `APROXIMACIÓN VISUAL` o retirarlo.

---

# 19. Prohibición de geometrías inventadas

No construir polígonos de cuencas con coordenadas manuales solo para visualización.

Si no existe geometría confiable:

- usar centroides;
- usar etiquetas;
- usar puntos;
- omitir temporalmente el polígono.

Precisión geográfica > decoración.

---

# 20. Informe de geometrías

Crear:

```text
docs/auditoria_geometrias.md
```

Tabla:

| Capa | Fuente | CRS | Tipo | Exacta/Aprox | Uso |
|---|---|---|---|---|---|

Incluir:

- cuencas;
- provincias;
- pozos;
- ductos;
- concesiones;
- trayectorias;
- instalaciones.

---

# 21. Tipografía

Evaluar alternativa a:

```text
Newsreader
Inter
JetBrains Mono
```

Crear variante:

```text
Archivo
IBM Plex Mono
```

## Archivo

- títulos;
- subtítulos;
- cuerpo;
- navegación;
- números editoriales.

## IBM Plex Mono

solo:

- años;
- coordenadas;
- unidades;
- metadata;
- etiquetas técnicas.

---

# 22. Comparativa tipográfica

Generar screenshots A/B:

```text
A:
Newsreader + Inter + JetBrains Mono

B:
Archivo + IBM Plex Mono
```

Comparar:

- capítulo 01;
- capítulo 04;
- capítulo 05.

No decidir sin comparar.

---

# 23. Simplificar encabezados

Cambiar:

```text
01 REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025
```

por:

```text
01   ARGENTINA · 1950—2025
```

Capítulo 02:

```text
02   TERRITORIO · 2006—2025
```

Capítulo 03:

```text
03   PRODUCCIÓN · NOV 2023
```

Capítulo 04:

```text
04   CONCENTRACIÓN · 2025
```

Capítulo 05:

```text
05   TECNOLOGÍA · 2015—2025
```

Capítulo 06:

```text
06   COHORTES · 2015—2024
```

Capítulo 07:

```text
07   ECONOMÍA · 2007—2025
```

Capítulo 08:

```text
08   ARGENTINA · SÍNTESIS
```

---

# 24. Marca superior

Usar solamente:

```text
Petróleo en Argentina
Del pozo al país
```

No usar:

- Atlas geográfico;
- Crónica de datos;
- Laboratorio;
- Observatorio;
- Explorador inteligente.

---

# 25. Diseño map-first

Reducir panel desktop a:

```text
300–330 px
```

No mantener siempre el panel visible.

Permitir:

```text
A. panel izquierdo pequeño
B. mapa full screen
C. texto flotante
D. gráfico central
E. mapa + timeline
```

---

# 26. Capítulo 01

```text
01   ARGENTINA · 1950—2025

El regreso

Después de décadas de caída,
la producción volvió a crecer.
```

Gráfico histórico grande.

Mapa nacional discreto.

---

# 27. Capítulo 02

```text
02   TERRITORIO · 2006—2025

El mapa se mueve

La producción argentina cambió
de centro de gravedad.
```

Mostrar directamente:

```text
Neuquén
20,4% → 64,7%
```

No agregar `Qué observar...`.

---

# 28. Capítulo 03

```text
03   PRODUCCIÓN · NOV 2023

El punto de quiebre
```

Marcar:

```text
NOV 2023
51,11% no convencional
```

directamente en gráfico/mapa.

---

# 29. Capítulo 04

```text
04   CONCENTRACIÓN · 2025

Pocos pozos,
mucho petróleo
```

Número principal:

```text
912
```

Bajada:

```text
pozos explican
la mitad de la producción
```

---

# 30. Capítulo 05

```text
05   TECNOLOGÍA · 2015—2025

Cómo cambió el pozo
```

Usar la escena 3D más fuerte.

---

# 31. Navegación lateral

Mantener Journey Tracker, pero refinarlo.

Puntos:

```text
inactivo: 9 px
activo: 13 px
```

Camino SVG orgánico.

No alinearlo como wizard.

---

# 32. Camino lateral

Estados:

```text
recorrido
pendiente
```

Recorrido:

```text
rgba(217,154,67,0.70)
```

Pendiente:

```text
rgba(235,229,207,0.12)
```

Animar el avance.

---

# 33. Eliminar textos instructivos

Eliminar de toda la app:

```text
Qué observar
Utiliza...
Mira...
Observa...
Puedes ver...
```

Si una visualización requiere instrucciones para entender el hallazgo, corregir la visualización.

---

# 34. Anotaciones directas

Preferir:

```text
Neuquén
64,7% en 2025
```

o:

```text
NOV 2023
primer mes >50%
```

directamente sobre mapa/gráfico.

---

# 35. Timeline

Mantener.

Debe mostrar:

- año actual;
- hitos;
- progreso temporal.

No parecer un reproductor multimedia.

---

# 36. Performance

Medir de verdad:

```text
FPS promedio
FPS mínimo
features visibles
tiempo flyTo
tiempo carga inicial
```

Crear:

```text
docs/performance_map.md
```

No reportar estimaciones como mediciones.

---

# 37. Tests de CARTO

Agregar validaciones:

```text
CARTO token cargado
basemap responde HTTP 200
sin 401
sin 403
sin watermark API KEY REQUIRED
fallback funciona sin CARTO
```

No incluir token en logs.

---

# 38. Error handling

Si CARTO responde:

```text
401
403
429
5xx
```

activar fallback.

Mensaje de consola:

```text
CARTO basemap unavailable. Using fallback map style.
```

No mostrar errores técnicos al usuario.

---

# 39. Producción

En servidor:

- configurar token por entorno;
- restringir referers;
- separar DEV / PROD;
- no versionar secretos.

---

# 40. Comparativa visual final

Generar:

```text
docs/screenshots/
```

con:

```text
01_actual.png
01_nuevo.png
02_actual.png
02_nuevo.png
04_actual.png
04_nuevo.png
05_actual.png
05_nuevo.png

tipografia_A.png
tipografia_B.png

dem_A.png
dem_B.png
```

---

# 41. Entregables

Crear:

```text
docs/carto_auth.md
docs/auditoria_geometrias.md
docs/cartografia_v3.md
docs/performance_map.md
docs/comparativa_tipografica.md
```

Actualizar:

```text
DESIGN.md
docs/redesign_plan.md
docs/historia_visual.md
```

---

# 42. Informe final

Al terminar informar:

1. qué layer producía `API KEY REQUIRED`;
2. cómo se corrigió;
3. qué API de CARTO usa realmente el proyecto;
4. qué scopes/grants necesita;
5. si existe fallback;
6. proveedor basemap final;
7. proveedor DEM final;
8. geometrías confirmadas;
9. geometrías descartadas/aproximadas;
10. stack tipográfico elegido;
11. parámetros de cámara;
12. métricas reales de performance;
13. screenshots A/B;
14. problemas pendientes.

---

# 43. Restricciones finales

No:

- esconder errores CARTO con CSS;
- subir el token al repositorio;
- inventar polígonos;
- usar más texto para explicar visualizaciones confusas;
- convertir el mapa en un videojuego;
- exagerar el relieve;
- usar columnas 3D gigantes;
- saturar el mapa;
- copiar visualmente Milla 201.

Sí:

- tomar como referencia su jerarquía visual;
- hacer que el mapa sea protagonista;
- usar pocas palabras;
- mantener identidad propia;
- priorizar rigor geográfico;
- usar animaciones con función narrativa.

---

# Resultado esperado

La nueva versión debe sentirse como una pieza visual propia:

```text
Petróleo en Argentina
Del pozo al país
```

con:

- mapa auténticamente 3D;
- relieve legible;
- datos auditados;
- geometrías defendibles;
- basemap limpio;
- sin watermark;
- sin look de plantilla;
- sin instrucciones innecesarias;
- navegación editorial;
- identidad visual diferenciada.
