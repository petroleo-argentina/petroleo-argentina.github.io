# Iteración V6 — Navegación visible, paneles homogéneos y filtros claros

## 1. Objetivo y alcance

Ajustar la interfaz actual de «Petróleo en Argentina» a partir de la captura revisada. Conservar las mejoras de gráficos, mapa y timeline; corregir la distribución, la coherencia visual y la claridad de los controles.

Esta iteración modifica la especificación V4 + V5 en cuatro puntos:

1. El gráfico derecho no puede tapar los puntos para recorrer la historia.
2. Todos los paneles deben compartir el mismo tratamiento visual.
3. Los filtros deben resultar más claros y fáciles de identificar.
4. Eliminar el capítulo «Síntesis».

Implementar los cambios sobre la aplicación existente. No rehacer el proyecto ni añadir nuevas secciones.

## 2. Reservar espacio para recorrer la historia

En la captura, el panel del gráfico derecho invade la columna vertical de puntos de navegación. Corregir la distribución, no solamente el orden de superposición.

- Reservar una franja exclusiva en el borde derecho para la navegación por capítulos, con separación suficiente respecto del gráfico.
- Desplazar el panel del gráfico hacia adentro y limitar su ancho según el espacio disponible.
- Ningún panel, tooltip del gráfico, desplegable o contenido expandido debe impedir usar esa navegación.
- Mantener los puntos visibles y clicables en todos los capítulos, incluso al cambiar el tamaño de ventana o ampliar el navegador.
- Destacar el capítulo activo y ofrecer nombre o número mediante foco, hover y una alternativa táctil apropiada.
- Dar a cada punto un área de interacción suficientemente amplia sin necesidad de aumentar mucho su diámetro visible.
- Conservar espacio libre para la barra superior y la timeline inferior.

En pantallas donde no entren gráfico y navegación lateral, cambiar la disposición: usar navegación compacta en una zona propia y un gráfico plegable o reubicado. No comprimirlos hasta hacerlos ilegibles ni ocultar el recorrido sin una alternativa accesible.

**Criterio de aceptación:** todos los capítulos se pueden abrir desde sus controles sin cerrar el gráfico, y las áreas ocupadas por gráfico y navegación no se intersectan.

## 3. Unificar el aspecto de los paneles

El panel izquierdo se percibe negro azulado y más recto; el derecho, marrón/oliva y redondeado. Deben pertenecer al mismo sistema visual.

Definir y reutilizar un único estilo base para panel narrativo, panel del gráfico, barra de filtros, timeline y popup cartográfico:

- Fondo oscuro neutro común, tomando como referencia el panel izquierdo.
- Misma familia de transparencias y desenfoque moderado.
- Bordes finos con igual color e intensidad.
- Radio de esquinas coherente, redondeado sin excesos.
- Sombras, separadores y espaciados consistentes.
- Tipografía y jerarquía de títulos, etiquetas, cifras y fuentes coordinadas.
- Botones de plegado y cierre con un tratamiento común.

Los paneles pueden tener tamaños y organización diferentes según su función, pero no parecer componentes de productos distintos. La transparencia puede mostrar variaciones del mapa debajo; ajustar la opacidad para que esas variaciones no produzcan diferencias marcadas de tono ni reduzcan el contraste.

Reservar el dorado para la serie principal, los indicadores destacados y las selecciones. No teñir de dorado u oliva todo el fondo del gráfico. Evitar multiplicar recuadros dentro del panel: integrar el KPI con el gráfico mediante espaciado y jerarquía.

**Criterio de aceptación:** panel izquierdo, gráfico, filtros y timeline se perciben como una misma interfaz sobre distintas zonas del mapa.

## 4. Hacer más claros los filtros

La barra superior debe permitir entender qué se puede cambiar y qué selección está activa sin requerir un texto explicativo.

### Etiquetas y alcance

- Mostrar una etiqueta breve para cada filtro: por ejemplo, «Período», «Cuenca» u «Operador», solamente si existe y aplica.
- Separar visualmente el selector de modo «Relato / Explorar» de los filtros de datos.
- Dar a campos y desplegables contraste suficiente frente a la barra.
- Hacer reconocibles las flechas de apertura, el foco y los estados seleccionados.
- Mostrar el valor completo o una abreviatura inequívoca; evitar que el truncado oculte la selección esencial.
- Para el selector histórico visible en la captura, usar «Período» como etiqueta y «1950–2025 · Todo el período» como valor solo si coincide con la cobertura real.
- Mostrar filtros activos de forma compacta, con posibilidad de quitar una selección individual.
- Usar «Restablecer filtros» si la acción solo cambia filtros, o «Restablecer vista» si también recupera tiempo, cámara y selección. La etiqueta debe coincidir con su efecto real.

### Comportamiento

- Sincronizar filtros con mapa, gráficos, KPIs y timeline mediante el estado compartido existente.
- No añadir filtros decorativos ni controles para campos ausentes.
- Mantener las opciones compatibles al cambiar de capítulo y comunicar ajustes necesarios de manera breve.
- Diferenciar claramente «Todos», una selección concreta y «Sin datos».
- Ofrecer estados de hover, foco, selección y deshabilitado legibles; no depender solo del dorado para distinguirlos.
- En pantalla pequeña, permitir plegar filtros secundarios sin ocultar que hay filtros activos.

**Criterio de aceptación:** se reconoce qué dimensión modifica cada control, cuál es su valor actual y cómo recuperar la vista inicial.

## 5. Eliminar el capítulo Síntesis

Quitar «08 · Argentina · Síntesis» como capítulo del recorrido, verificando su identificador real en el proyecto. Esta instrucción reemplaza su inclusión en la especificación V4 + V5.

- Retirar su punto de navegación, entrada de menú y configuración de capítulo.
- Quitar sus contenidos y visualizaciones exclusivas de la experiencia.
- Actualizar totales, índices, progreso, enlaces anterior/siguiente y cualquier referencia al número de capítulos.
- El recorrido debe finalizar en el último capítulo sustantivo; según el contexto disponible, «Economía». Confirmar el orden real antes de ajustar la navegación.
- En el último capítulo, no ofrecer un botón «Siguiente» que lleve a una pantalla inexistente. Puede ofrecerse una acción discreta «Volver al inicio».
- Actualizar el final del relato continuo y detener correctamente cualquier avance automático.
- Si existe un enlace directo antiguo a Síntesis, resolverlo hacia una vista válida sin dejar la aplicación vacía.
- Conservar componentes y datos que utilicen otros capítulos; eliminar solamente el contenido y las referencias exclusivas de Síntesis.

No reemplazar Síntesis por otra pantalla de resumen ni trasladar sus textos al último capítulo. El objetivo es acortar el recorrido y evitar un cierre redundante.

**Criterio de aceptación:** la historia termina limpiamente, sin Síntesis, navegación rota ni contadores desactualizados.

## 6. Validación y entrega

Verificar la aplicación real en escritorio, ventana intermedia y móvil, incluyendo ampliación del navegador y navegación por teclado.

| Comprobación | Resultado esperado |
|---|---|
| Recorrer todos los capítulos con el gráfico abierto | Navegación visible, accesible y sin solapamiento |
| Abrir filtros, tooltips y paneles | Contenido legible y controles esenciales utilizables |
| Comparar panel izquierdo, gráfico, popup y timeline | Fondo, bordes, radios y tipografía coherentes |
| Cambiar filtros y tiempo | Mapa, gráficos e indicadores consistentes |
| Restablecer | Efecto correspondiente a la etiqueta del botón |
| Llegar al final del relato | Último capítulo válido, sin paso a Síntesis |
| Abrir un enlace antiguo a Síntesis, si existe | Recuperación hacia una vista válida |
| Reducir el ancho y ampliar el navegador | Distribución adaptada sin esconder controles necesarios |

Entregar un informe breve con los cambios realizados, verificaciones y cualquier pendiente. Adjuntar capturas reales de la aplicación: composición general, filtros abiertos y final del recorrido. No sustituirlas por imágenes simuladas ni afirmar que una comprobación pasó si no pudo ejecutarse.
