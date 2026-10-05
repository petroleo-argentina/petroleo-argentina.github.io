# Ajuste visual final — cartografía, navegación y lenguaje editorial

## Objetivo

Refinar el frontend actual para que la experiencia deje de sentirse como una interfaz generada por IA y pase a sentirse como una pieza editorial/cartográfica con identidad propia.

No modificar datos, queries ni conclusiones auditadas.

No volver a introducir estética SaaS.

La prioridad de esta iteración es:

1. mejorar sustancialmente la cartografía;
2. simplificar el lenguaje de interfaz;
3. eliminar textos que explican cómo mirar;
4. convertir la navegación lateral derecha en un recorrido visual;
5. reducir marcas/títulos artificiales;
6. hacer que cada visualización se explique por sí misma.

---

# 1. Cambio de motor cartográfico: Leaflet → MapLibre GL JS

La implementación actual usa Leaflet sobre Canvas.

Leaflet puede simular perspectiva, pero no ofrece terreno 3D real basado en DEM de forma nativa.

Para lograr relieve real y una experiencia cartográfica más expresiva, migrar SOLO la capa de visualización cartográfica a:

```text
MapLibre GL JS
```

Mantener:

- backend actual;
- FastAPI;
- endpoints;
- datasets;
- lógica narrativa;
- filtros;
- timeline;
- datos auditados.

No rehacer ETL ni API.

Evaluar Deck.gl únicamente para capas de muchos pozos si mejora rendimiento.

---

# 2. Terreno 3D real

Implementar soporte de:

```text
raster-dem
terrain
hillshade
pitch
bearing
fog/atmosphere sutil
```

El relieve debe ser geográfico, no decorativo.

## Exageración recomendada

```text
terrain exaggeration: 1.15 – 1.35
```

No exagerar montañas.

---

# 3. Uso del 3D por escala

## Vista nacional

Mantener una lectura casi cenital:

```text
pitch: 0–18°
```

Relieve muy sutil.

Objetivo:

leer Argentina, provincias, cuencas y distribución territorial con claridad.

## Patagonia / Cuenca Neuquina

Aumentar progresivamente:

```text
pitch: 30–45°
```

## Añelo / Vaca Muerta

Permitir:

```text
pitch: 45–58°
bearing variable
```

para mostrar mesetas, relieve y distribución de pozos.

No mantener toda la aplicación inclinada.

La cámara debe adaptarse al relato.

---

# 4. El mapa no debe ser monocromático gris

El mapa actual es demasiado gris y plano.

Crear un estilo cartográfico propio con color contenido.

No usar un mapa satelital como estilo principal.

## Paleta sugerida

### Tierra baja

```text
#272821
```

### Terreno medio

```text
#35362D
```

### Elevaciones

```text
#565244
```

### Cordillera / relieve alto

```text
#77705D
```

### Agua

```text
#142129
```

### Límites provinciales

```text
rgba(235,229,207,0.18)
```

### Rutas principales

```text
rgba(220,211,185,0.12)
```

### Ciudades

```text
rgba(235,231,215,0.55)
```

### Texto territorial secundario

```text
rgba(235,231,215,0.30)
```

### Convencional

```text
#C98B32
```

### No convencional

```text
#39AFCF
```

### Highlight narrativo

```text
#E3B55A
```

Estos valores son una dirección visual, no una obligación exacta.

Ajustar contraste después de probarlos sobre DEM/hillshade.

---

# 5. El relieve debe tener función narrativa

No agregar 3D solo porque queda atractivo.

Ejemplos:

## Capítulo 01

Argentina casi cenital.

El relieve apenas perceptible.

## Capítulo 02

Al desplazarse hacia Patagonia:

- aparece hillshade;
- aumenta ligeramente el pitch;
- se hace evidente la distribución territorial.

## Capítulo 03

Zoom hacia Cuenca Neuquina.

Mayor relieve y detalle.

## Capítulo 05

Vista oblicua sobre Añelo / Vaca Muerta.

Este es el capítulo donde el 3D puede tener mayor protagonismo.

---

# 6. Corregir cabecera superior izquierda

Eliminar completamente:

```text
ATLAS GEOGRÁFICO & CRÓNICA DE DATOS
```

No reemplazarlo por otra frase grandilocuente.

La marca superior debe ser simple.

Usar:

```text
Petróleo en Argentina
Del pozo al país
```

Ejemplo visual:

```text
Petróleo en Argentina   /Del pozo al país
```

o:

```text
PETRÓLEO EN ARGENTINA
Del pozo al país
```

Sin kicker tipo "atlas", "crónica", "laboratorio", "observatorio" o términos que parezcan generados artificialmente.

---

# 7. Corregir encabezados de capítulo

Actualmente aparece algo similar a:

```text
01 / 08
REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025
```

Eliminar el formato:

```text
01 / 08
```

No mostrar el total de capítulos en el encabezado.

Usar una sola línea:

```text
01  REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025
```

o visualmente:

```text
01   REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025
```

Para capítulo 02:

```text
02   CUENCAS SEDIMENTARIAS · MIGRACIÓN TERRITORIAL
```

Para capítulo 03:

```text
03   CUENCA NEUQUINA · CAMBIO DE COMPOSICIÓN
```

La numeración debe servir como referencia editorial, no como indicador de wizard.

---

# 8. Eliminar lenguaje de interfaz tipo IA

Eliminar frases del tipo:

```text
Qué observar en el mapa:
Utiliza el deslizador...
Observa cómo...
Mira cómo...
En este gráfico puedes ver...
```

No sustituirlas por instrucciones equivalentes.

La visualización debe comunicar la idea mediante:

- título;
- anotación;
- dato;
- highlight;
- transición;
- cambio de escala;
- leyenda mínima.

---

# 9. Sustituir instrucciones por hallazgos

Ejemplo actual a eliminar:

```text
Qué observar en el mapa:
Utiliza el deslizador temporal inferior para observar la migración...
```

Reemplazar por una frase que aporte información:

```text
Entre 2010 y 2025, Neuquén pasó de aportar el 20,4% al 64,7% del petróleo argentino.
```

O directamente no poner texto adicional si el gráfico ya lo muestra claramente.

Regla:

```text
si el texto explica cómo usar el gráfico → eliminarlo
si el texto aporta un hallazgo → conservarlo
```

---

# 10. Las visualizaciones deben ser el foco

Para cada capítulo revisar:

```text
¿El usuario entiende la idea principal sin leer instrucciones?
```

Si la respuesta es no:

NO agregar más texto.

Corregir:

- jerarquía;
- anotaciones;
- color;
- escala;
- transición;
- labeling;
- encuadre.

---

# 11. Rediseño de navegación lateral derecha

La navegación actual de puntos aislados se percibe como un stepper genérico.

Reemplazarla por un recorrido gráfico vertical.

Concepto:

```text
●
│
●
│
●
│
●
│
●
```

Pero evitar una línea perfectamente recta tipo formulario.

Crear un "camino" sutil:

```text
●
 ╲
  ●
  │
 ●
  ╲
   ●
```

Puede ser una línea SVG con pequeñas variaciones laterales.

Objetivo:

que parezca una ruta narrativa/cartográfica y no un wizard.

---

# 12. Navegación derecha más visible

Actualmente los puntos son demasiado pequeños y oscuros.

Aumentar ligeramente:

```text
inactive node: 8–10 px
active node: 11–14 px
```

Estados:

## Inactivo

```text
fill: #12161A
stroke: rgba(235,229,207,0.40)
```

## Visitado

```text
fill: rgba(201,139,50,0.30)
stroke: rgba(201,139,50,0.70)
```

## Activo

```text
fill: #D99A43
stroke: #E6BE78
```

Sin glow fuerte.

---

# 13. El camino lateral debe mostrar progreso

La línea debe tener dos estados:

```text
tramo recorrido
tramo pendiente
```

Ejemplo:

recorrido:

```text
rgba(217,154,67,0.70)
```

pendiente:

```text
rgba(235,229,207,0.12)
```

Al cambiar de capítulo, animar el trazado del siguiente tramo.

Duración aproximada:

```text
450–700 ms
```

---

# 14. Etiqueta del capítulo activo

La etiqueta actual:

```text
02. El mapa se mueve
```

puede mantenerse, pero debe integrarse al recorrido.

Ejemplo:

```text
        02
        El mapa se mueve
        ●
       ╱
      ●
```

No hacer una pill ni card.

Tipografía:

- mono pequeña para número;
- serif/sans para título;
- color marfil;
- acento ámbar en nodo.

---

# 15. Eliminar aspecto de wizard

No usar:

- 01 / 08;
- dots idénticos alineados;
- "Anterior / Siguiente" como botones de formulario;
- barras de progreso típicas de onboarding.

La navegación debe sentirse como recorrido editorial.

---

# 16. Botones inferior izquierdo

Los botones anterior/siguiente actuales son demasiado genéricos.

Reducirlos a controles mínimos.

Ejemplo:

```text
←
```

y:

```text
→
```

sin caja blanca dominante.

O:

```text
← capítulo anterior
siguiente capítulo →
```

con tipografía pequeña.

El mapa debe seguir siendo el elemento dominante.

---

# 17. Timeline inferior

Mantenerlo porque tiene función real.

Pero mejorar jerarquía:

- más contraste del año actual;
- recorrido temporal claramente visible;
- menos aspecto de reproductor multimedia;
- hitos relevantes marcados;
- tooltip de año.

No usar play si la reproducción automática no aporta al capítulo.

---

# 18. Etiquetas dentro del mapa

Usar anotaciones directas cuando hagan falta.

Ejemplo capítulo 02:

```text
Neuquén
20,4% → 64,7%
```

sobre el área correspondiente.

En lugar de explicar en un bloque externo qué se supone que el usuario debe mirar.

---

# 19. Mapas más vivos sin perder rigor

Agregar muy sutilmente:

- hillshade;
- elevación;
- cuerpos de agua;
- rutas principales;
- ciudades;
- fronteras;
- nombres geográficos;
- cuencas.

No usar demasiada saturación.

El color debe ayudar a orientarse, no competir con los datos.

---

# 20. Pozos

A escala nacional:

- puntos pequeños;
- opacidad moderada;
- tamaño mínimo suficientemente visible.

A escala regional:

- aumentar tamaño;
- permitir hover;
- diferenciar convencional/no convencional;
- agregar profundidad mediante perspectiva del mapa.

No usar glow azul fuerte.

---

# 21. Capítulo 02 — corrección específica

Título:

```text
El mapa se mueve
```

Subtítulo opcional:

```text
La producción argentina cambió de centro de gravedad.
```

Encabezado:

```text
02   CUENCAS SEDIMENTARIAS · MIGRACIÓN TERRITORIAL
```

Eliminar totalmente:

```text
Qué observar en el mapa:
...
```

Mantener como dato editorial:

```text
64,7%
Neuquén en 2025

20,4%
Neuquén en 2010
```

La transición temporal del mapa debe comunicar el resto.

---

# 22. Capítulo 01 — corrección específica

Encabezado:

```text
01   REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025
```

No:

```text
01 / 08
```

Título principal más corto:

```text
El regreso
```

Bajada:

```text
Después de décadas de caída, la producción volvió a crecer y alcanzó un nuevo máximo.
```

El gráfico histórico debe ser protagonista.

---

# 23. Capítulo 03 — corrección específica

Encabezado:

```text
03   ARGENTINA · CAMBIO DE COMPOSICIÓN
```

Título:

```text
El punto de quiebre
```

Destacar visualmente:

```text
NOV 2023
```

No agregar texto como:

```text
Observe el cruce entre las líneas...
```

El propio gráfico debe marcar la intersección.

---

# 24. Capítulo 04 — Pareto

Usar la navegación y animación del mapa como parte del descubrimiento.

No escribir:

```text
Observe cómo desaparecen los pozos...
```

Mostrar directamente:

```text
26.219
↓
912
```

y después:

```text
3,48% de los pozos
produce 50% del petróleo
```

---

# 25. Evitar textos redundantes

Regla para toda la aplicación:

Si:

- título;
- gráfico;
- dato grande;

ya dicen lo mismo,

NO repetirlo en un párrafo.

Preferir una experiencia con menos palabras.

---

# 26. Motion

Agregar más animación, pero con función.

Permitido:

- flyTo;
- pitch transition;
- bearing transition;
- fade de capas;
- aparición progresiva de pozos;
- morph de gráficos;
- animación del camino de capítulos;
- highlight sincronizado.

Evitar:

- partículas;
- glow pulsante;
- animaciones permanentes;
- fondos en movimiento;
- efectos de videojuego.

---

# 27. Performance

La migración a MapLibre debe mantener una experiencia fluida.

Medir FPS reales.

Usar:

- WebGL;
- vector tiles;
- clustering;
- Deck.gl si corresponde;
- simplificación según zoom.

No confiar únicamente en una estimación manual de FPS.

Registrar:

```text
FPS promedio
FPS mínimo durante flyTo
cantidad de features visibles
```

---

# 28. Validación visual

Después de implementar, generar screenshots de:

```text
01 vista nacional
02 Patagonia
03 Cuenca Neuquina
04 Pareto
05 Añelo 3D
```

Evaluar:

- legibilidad;
- contraste;
- profundidad;
- protagonismo del dato;
- exceso de texto;
- orientación geográfica.

---

# 29. Restricciones

No modificar:

- cifras;
- consultas;
- datasets;
- hallazgos auditados;
- endpoints.

No agregar texto instructivo para compensar una visualización confusa.

Primero mejorar la visualización.

---

# 30. Entregables

Actualizar:

```text
DESIGN.md
docs/redesign_plan.md
docs/historia_visual.md
```

Crear:

```text
docs/cartografia_3d.md
docs/revision_lenguaje_ui.md
```

Al finalizar informar:

1. motor cartográfico anterior;
2. motor cartográfico nuevo;
3. proveedor DEM utilizado;
4. estilo/basemap utilizado;
5. capítulos con terreno activo;
6. textos instructivos eliminados;
7. navegación lateral rediseñada;
8. archivos modificados;
9. screenshots;
10. medición real de rendimiento;
11. problemas pendientes.

---

# Resultado esperado

La aplicación debe dejar de parecer una interfaz que explica cómo usar un mapa.

Debe sentirse como una historia que se descubre mirando los datos.

El mapa debe aportar territorio, relieve y orientación.

Los gráficos deben señalar directamente el hallazgo.

La interfaz debe desaparecer todo lo posible.

La identidad visible principal debe ser simplemente:

```text
Petróleo en Argentina
Del pozo al país
```
