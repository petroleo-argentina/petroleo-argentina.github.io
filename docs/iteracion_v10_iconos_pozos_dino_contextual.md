# Iteración V10 — Iconos de pozos por zoom y dinosaurio contextual independiente

## 1. Corrección de alcance respecto de V9

La intención del usuario fue interpretada incorrectamente en V9. Esta especificación reemplaza dos decisiones anteriores:

1. Los puntos de pozos deben convertirse en **iconos PNG transparentes de instalaciones petroleras** al acercarse. No son fotografías ni ubicaciones fotográficas nuevas.
2. El Argentinosaurus debe estar **fuera del panel superior izquierdo**, preferentemente abajo a la izquierda en un espacio libre. Su globo complementa la información del capítulo o aporta un concepto relacionado; no repite el título ni sustituye toda la información principal.

Conservar las mejoras ya realizadas: rueda para zoom, tipografías Alegreya + Archivo, transparencia reactiva de ambos paneles, siete capítulos y funcionamiento del inicio.

## 2. Puntos e iconos: dos representaciones de los mismos pozos

Usar el mismo conjunto de registros, identificadores y coordenadas que alimenta la capa actual de puntos.

| Escala | Representación |
|---|---|
| Lejana | Puntos pequeños con la codificación actual |
| Transición | Sustitución progresiva de puntos por iconos, según espacio disponible |
| Cercana | PNG transparentes de pozos, anclados a las coordenadas de cada registro |

No crear una colección nueva de lugares turísticos, fotografías o refinerías para cumplir este comportamiento. El pozo que era un punto debe seguir siendo el mismo pozo cuando se vea como icono.

### Recurso visual

Se adjunta `icono-pozo-petrolero.png`, un pictograma original generado para este proyecto con fondo transparente, que representa simbólicamente un equipo de bombeo. Utilizarlo como recurso de partida y preparar una versión optimizada para su tamaño real en pantalla.

Es un **símbolo genérico de pozo**: no afirma que todos los registros tengan ese mecanismo de extracción, ni que el equipo esté operando. No inferir tecnología, estado operativo o convencionalidad a partir del dibujo. Solo emplear variantes técnicas si la fuente contiene una clasificación verificable.

- Mostrar aproximadamente 24–36 px al acercarse, ajustando el tamaño al mapa real.
- Conservar nitidez, transparencia y contraste sobre distintos terrenos.
- Mantener la codificación de categoría/selección mediante una base o halo pequeño, sin confundir el dorado del dibujo con una categoría del dato.
- No introducir un círculo con foto dentro. La silueta del equipo debe verse directamente sobre el mapa.
- No animar cientos de equipos: los marcadores son estáticos.

### Implementación y densidad

- Preferir una capa de símbolos del motor cartográfico con un recurso compartido, sobre la misma fuente que los puntos; evitar crear un elemento HTML por cada pozo.
- Calibrar la transición con zoom y densidad reales, sin adoptar automáticamente el umbral 7 de la implementación fotográfica.
- Al cambiar representación, conservar filtros, fecha, identificación, coordenadas y selección.
- Evitar que punto e icono se superpongan indefinidamente o aparezcan como dos pozos distintos. La transición debe terminar en una representación principal clara.
- En zonas densas, conservar puntos para los elementos cuyo icono no cabe o utilizar agrupación con cantidad explícita. No ocultar registros silenciosamente por colisiones de símbolos.
- Dar prioridad al pozo seleccionado y permitir acercarse para separar elementos coincidentes. No desplazar las coordenadas analíticas para acomodar iconos.
- Mantener el anclaje del equipo en su base y comprobarlo con inclinación y rotación del mapa.
- Si falla la carga del PNG, conservar los puntos y su interacción.

## 3. El clic sigue mostrando la información disponible

Reutilizar la lógica actual de selección y popup del pozo, tanto sobre puntos como sobre iconos.

- Un clic identifica el registro correcto y abre la información disponible: nombre o código, operador, yacimiento, categoría, fecha, producción y unidad cuando esos campos existan.
- No inventar campos faltantes, confundir ausencias con cero ni reemplazar la ficha por una imagen ampliada.
- El año y las cifras del popup deben coincidir con el estado temporal y analítico mostrado.
- Evitar que un clic durante la transición abra dos popups o dispare eventos duplicados.
- Mantener la selección cuando el usuario cambia de zoom; cerrarla o actualizarla de forma clara si un filtro excluye el registro.
- Conservar un área de interacción cómoda, cursor reconocible y alternativa táctil.
- Reubicar o ajustar la cámara/popup cuando quede bajo un panel; no alterar la coordenada del pozo.

Retirar de la capa de pozos los marcadores `.map-photo-pin` y la apertura de `#photo-detail-modal` añadidos en V9 para esta función. No borrar la foto de portada ni recursos que tengan otros usos. La galería fotográfica no forma parte de este pedido y no debe seguir compitiendo con los pozos en el mapa.

## 4. Dinosaurio fuera del panel superior

La captura actual muestra el dinosaurio dentro del cuadro narrativo y un globo que repite «Generaciones de pozos». Corregir ambos aspectos.

### Distribución

- Panel superior izquierdo: número de capítulo, título, información principal breve y navegación.
- Guía independiente: Argentinosaurus y un globo contextual fuera de ese panel.
- Ubicación preferida: esquina inferior izquierda, por encima de la timeline y las atribuciones, con márgenes suficientes.
- El dinosaurio conserva fondo transparente; solo el globo lleva una superficie legible. No envolverlo en otra tarjeta grande.
- Reservar espacio real para el conjunto, teniendo en cuenta altura de la timeline, filtros abiertos, panel superior y tamaño del globo.
- Si no cabe abajo a la izquierda, elegir otra zona libre. Si tampoco hay espacio, plegar el globo detrás de un acceso discreto al guía, en vez de tapar datos o navegación.
- En móvil, usar un guía pequeño con globo desplegable; no devolverlo al interior del panel superior por comodidad de implementación.
- El área transparente alrededor del personaje no debe capturar clics ni gestos destinados al mapa. Solo botones y globo interactivo reciben eventos.
- Mantener ocultar/mostrar guía, preferencia de sesión, movimiento suave y respeto por movimiento reducido.

Al abrir una ficha de pozo, evitar que guía y popup se solapen. Se puede reubicar el globo o plegarlo mientras se consulta la ficha, sin perder la selección.

## 5. Contenido complementario, no repetido

El panel superior cuenta el hallazgo principal; el dinosaurio ayuda a entenderlo con una observación adicional, una definición o una sugerencia para explorar. No eliminar todo el texto superior ni duplicarlo abajo.

- Una idea por globo, idealmente 15–30 palabras, con opción de ampliar solo cuando sea necesario.
- Texto HTML independiente de la ilustración.
- Mensajes vinculados al capítulo real y a la selección, no al índice visual de forma frágil.
- No usar el título del capítulo como mensaje de respaldo.
- Si falta un mensaje contextual, mostrar una ayuda pertinente o plegar el globo. Nunca una caja vacía o un título duplicado.
- Los conceptos generales pueden permanecer al filtrar; las cifras y afirmaciones sobre el subconjunto deben recalcularse o retirarse cuando dejen de ser válidas.
- No afirmar causalidad a partir de una comparación visual ni copiar cifras de capturas como constantes.
- No añadir voz automática: en esta iteración el guía se comunica mediante el globo.

### Propuestas de mensajes conceptuales

Estas frases son propuestas editoriales para adaptar a las visualizaciones que existan; no son resultados calculados de los datos actuales.

| Capítulo | Mensaje complementario propuesto |
|---|---|
| Argentina | «El volumen anual suma todo lo producido en el año. El promedio diario reparte ese volumen entre sus días.» |
| Territorio | «Una región puede ganar participación aunque otra siga produciendo más. Compará porcentajes y volúmenes para distinguir esos cambios.» |
| Producción | «Convencional y no convencional describen cómo están alojados los hidrocarburos y cómo se extraen. Ambos son recursos naturales.» |
| Concentración | «Ordenar los pozos por producción permite ver cuánto aporta un grupo pequeño al total. El resultado depende del período elegido.» |
| Tecnología | «Longitud lateral y etapas de fractura son medidas distintas. Compararlas no demuestra, por sí solo, cuál causa un cambio de producción.» |
| Cohortes | «Una cohorte reúne pozos que comenzaron en un período similar. Compararlos a la misma edad ayuda a distinguir generaciones.» |
| Economía | «Antes de comparar valores económicos, fijate en la moneda, el período y si están ajustados por inflación.» |

Para una selección de pozo, puede aportar una aclaración breve sobre un campo de su ficha; no inventar características del equipo representado por el icono.

En el capítulo Cohortes de la captura, conservar «Generaciones de pozos» como título superior y usar el mensaje conceptual de cohortes en el globo inferior. Esto resuelve directamente la repetición observada.

## 6. Revisión de la implementación V9

El informe afirma que V9 fue verificada, pero esas pruebas evaluaban miniaturas fotográficas y un guía integrado al panel. Actualizar pruebas y documentación a la intención corregida; un resultado anterior en verde no valida V10.

Revisar además el paso del registro que copia el mismo archivo de fuente a nombres de distintos pesos. Renombrar un archivo no genera un peso tipográfico nuevo. Comprobar si los archivos son variables y qué rangos contienen; declarar sus rangos reales o usar los archivos estáticos correctos. No considerar el nombre del archivo prueba de que se cargó una familia o peso.

## 7. Verificación y entrega

| Comprobación | Resultado esperado |
|---|---|
| Mismo pozo a escala lejana/cercana | Punto y PNG conservan identificador, coordenada y datos |
| Clic en punto e icono | Misma ficha de información, sin modal fotográfico |
| Zona densa | Representación legible sin pérdida silenciosa de registros |
| PNG ausente | Puntos y clic siguen funcionando |
| Zoom, rueda y trackpad | No cambia el capítulo ni se restablece la cámara |
| Filtros y timeline | Marcadores y ficha siguen el estado analítico |
| Guía en escritorio | Fuera del panel superior, abajo a la izquierda si hay espacio |
| Guía y popup abiertos | No tapan controles ni se superponen de forma ilegible |
| Capítulo Cohortes | El globo explica el concepto; no repite el título |
| Móvil y ventana baja | Guía reubicado o plegado y navegación accesible |
| Guía oculto / movimiento reducido | Preferencias respetadas y mapa utilizable |
| Inicio y tipografías | Sin regresión del botón de portada; familias y pesos reales correctos |

Entregar capturas reales de un mismo pozo lejos y cerca, del popup sobre el icono, y de la disposición completa con guía inferior y panel superior. Informar qué comportamiento fotográfico se retiró y qué controles se conservaron. No declarar la tarea terminada por el solo hecho de que el PNG exista en el proyecto.
