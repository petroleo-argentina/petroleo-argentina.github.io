# Iteración V7 — Mapa a color, paneles reactivos y corrección editorial

## 1. Alcance

Aplicar estos cambios sobre la implementación V6 de «Petróleo en Argentina». Mantener los siete capítulos, la ausencia de Síntesis, la sincronización de filtros y la navegación visible.

Las capturas y el informe de V6 son referencias del estado observado, no evidencia de que todos los comportamientos estén verificados. Esta iteración requiere revisar la aplicación y los datos reales.

Prioridades:

1. Paneles de gráficos más translúcidos en reposo y más oscuros al interactuar.
2. Mapa con color natural y relieve legible, cercano a la referencia satelital aportada.
3. Corregir la comparación con 2017, la afirmación de récord y las unidades.
4. Mostrar «ISLAS MALVINAS» en la cartografía.
5. Eliminar «Preguntas», «Capas» y «Fuentes» del menú superior; integrar únicamente controles de capas útiles en los filtros principales.

## 2. Paneles que se oscurecen al interactuar

Implementar ambos estados como un único comportamiento: mayor transparencia en reposo y mayor opacidad de fondo cuando el usuario consulta el gráfico.

- En reposo, dejar percibir el mapa a través del panel, conservando legibilidad de datos y etiquetas.
- Al pasar el mouse por cualquier parte del panel del gráfico, oscurecer su fondo de manera suave.
- Mantener ese estado mientras se interactúa con botones, leyenda, tooltip o controles del propio panel.
- Aplicar el mismo tratamiento cuando un elemento interior recibe foco de teclado (`:focus-within`).
- Al salir del panel y perder el foco, recuperar el estado translúcido.
- En dispositivos sin hover, utilizar por defecto una opacidad suficiente para leer e interactuar, sin exigir un primer toque que bloquee los controles.

Como punto de partida visual, probar un fondo oscuro neutro con alfa entre 0,60 y 0,72 en reposo, y entre 0,92 y 0,96 al interactuar; transición de 150–220 ms. Son valores orientativos: ajustar sobre el nuevo mapa a color y comprobar contraste real.

Modificar exclusivamente la opacidad del fondo. **No aplicar `opacity` al contenedor completo**, porque también desvanecería líneas, textos, cifras y botones. No oscurecer el mapa entero al pasar sobre el gráfico.

Mantener los tokens compartidos de tono, borde y radio de V6. No introducir un panel marrón u oliva distinto del resto. Revisar los fondos internos del KPI y del lienzo del gráfico para que no oculten por completo el efecto de transparencia. El desenfoque debe ser moderado y no borrar innecesariamente el mapa; revisar el `blur(18px) saturate(180%)` informado en V6 según el resultado visual y el rendimiento.

La transición no debe mover el panel, cambiar sus dimensiones, recrear el gráfico ni tapar la navegación. Respetar la preferencia de movimiento reducido.

## 3. Mapa con color natural

Tomar de la referencia aportada el color y la textura del territorio: agua azul, vegetación verde, zonas áridas en tonos tierra y relieve reconocible. No copiar la acumulación de líneas y puntos de esa referencia ni añadir datos que el proyecto no tenga.

- Sustituir el aspecto gris/oliva apagado por una base satelital o de imagen natural a color que se aproxime a la referencia.
- Revisar primero si hay velos oscuros, filtros de desaturación, tintes o capas de sombreado excesivas que estén apagando toda la escena.
- Mantener MapLibre como motor y conservar el terreno/DEM separado del mapa base.
- Usar una fuente autorizada para el proyecto, con atribución visible y configuración adecuada. No inventar URLs de tiles ni asumir que una imagen de referencia habilita reutilizar su proveedor.
- Si no hay una fuente de imágenes disponible, implementar una base vectorial a color como alternativa e informar esa diferencia; no presentarla como satelital.
- Mantener etiquetas legibles sobre la imagen, evitando duplicar rótulos de una base ya etiquetada.
- Reducir el hillshade si ensucia el color natural o duplica sombras del fondo.
- Ajustar la opacidad de polígonos y capas analíticas para que no pinten extensas regiones con una mancha uniforme que oculte la base.
- Conservar selección, filtros, tiempo, cámara y capas analíticas al cambiar o recargar el estilo.

Priorizar una mejora visible del territorio sin convertir la pantalla en un mosaico de colores saturados. Los paneles oscuros siguen proporcionando contraste a los gráficos.

## 4. Revisar «+63,9% vs 2017 (Récord)»

### Qué muestra la captura

El distintivo pertenece al KPI del gráfico; no es una propiedad de la timeline. Con las cifras visibles, la cuenta es:

```text
(46.438,5 / 28.330 − 1) × 100 = 63,9199...
```

Esto explica el redondeo a +63,9%, siempre que ambos valores correspondan a la misma magnitud, unidad, cobertura y duración. **No demuestra un récord.**

La narración actual presenta 2017 como punto de recuperación, pero la captura no prueba que sea un mínimo relevante. Además, la curva muestra un pico anterior más alto que el valor de 2025. Por tanto, la afirmación de récord histórico es inconsistente con lo que se ve y debe retirarse mientras se auditan los datos.

### Corrección requerida

- Retirar inmediatamente «(Récord)» del distintivo y la afirmación no verificada de récord en el texto izquierdo y otros lugares.
- Buscar también identificadores, anotaciones, valores precalculados y pruebas que asuman ese récord. El test citado como `test_2025_record_production_metric` no constituye evidencia: revisar qué comprueba y corregir cualquier expectativa fundada en una afirmación incorrecta.
- Comprobar fuente, magnitud, unidad, frecuencia, cobertura y condición provisional o definitiva de cada observación.
- Distinguir total anual, promedio diario anual, dato de un mes y tasa diaria de un mes. Un récord mensual no permite afirmar un récord de producción anual.
- Calcular el máximo de la serie comparable y registrar año y valor. Solo utilizar «récord» cuando el dato lo sostenga, especificando el alcance exacto y la cobertura disponible.
- No cambiar los datos ni recortar la serie para hacer coincidir el gráfico con el relato.

### Comparación comprensible y reactiva

Como comportamiento predeterminado, mostrar el valor del año activo y, si hay un año anterior comparable, la variación **respecto del año anterior**. Identificar ambos años o el año base en el distintivo. Si no hay base válida, omitir la variación.

La comparación con 2017 puede conservarse únicamente como anotación editorial específica del capítulo si existe una razón analítica comprobada para elegir ese año. En ese caso, rotular «Crecimiento 2017–2025: +63,9%», recalcular el porcentaje desde los datos y explicar el motivo de la base en un detalle breve. No mantenerla fija en todos los años, filtros y capítulos.

No llamar a 2017 «mínimo histórico», «inicio del no convencional» o «piso» sin respaldo. Revisar también la opción de filtro «2017–2025 · Ciclo no convencional» citada en el informe V6: usar fechas neutrales si esa periodización no está justificada.

### Unidades

La captura combina el selector «Miles m³» con la cifra «46.438,5 Mm³». Auditar esa correspondencia: una etiqueta de miles de metros cúbicos no debe confundirse con millones de metros cúbicos.

- Preferir unidades escritas explícitamente: «miles de m³», «millones de m³» o «barriles/día».
- Aplicar conversiones consistentes a KPI, ejes, tooltip, texto y timeline.
- Si se convierte un volumen anual a barriles/día, usar los días reales del año y documentar el factor de conversión; no compararlo sin aclaración con una tasa de cierre de año.
- Mostrar la unidad y la naturaleza del dato sin exigir que el usuario interprete una abreviatura ambigua.

## 5. Toponimia: ISLAS MALVINAS

Mostrar exactamente **«ISLAS MALVINAS»** como nombre del archipiélago en la interfaz cartográfica del proyecto, sustituyendo el rótulo inglés visible en la captura.

- Localizar la capa y el atributo que originan ese rótulo.
- Preferir etiquetas en español; si el proveedor no ofrece ese nombre, aplicar una sustitución específica por identificador geográfico estable o una capa de etiquetas propia.
- Evitar que el rótulo original y el nuevo aparezcan juntos.
- Si el nombre viene incrustado en tiles ráster, no se puede corregir cambiando un campo de texto: elegir una base sin etiquetas e incorporar rotulación propia, o una base adecuada. No usar un parche rectangular sobre la imagen.
- Verificar la sustitución en los niveles de zoom pertinentes y después de recargar el estilo, activar una alternativa de mapa o navegar por capítulos.
- Esta modificación es de rotulación; no requiere alterar las geometrías o los datos analíticos.

## 6. Menú superior y controles de capas

Eliminar del encabezado **Preguntas**, **Capas** y **Fuentes**, junto con sus accesos y paneles exclusivos. Mantener «Relato continuo», que no fue solicitado eliminar, y los modos Relato/Explorar existentes.

Revisar los manejadores y referencias de los elementos retirados para no dejar eventos rotos, espacios vacíos ni controles invisibles que reciban foco.

### Capas dentro de la pantalla principal, solo si aportan

Inventariar los controles existentes del panel Capas. Integrar en la barra principal únicamente los que sean útiles para interpretar o explorar el capítulo activo, mediante un selector compacto «Mostrar» o interruptores breves.

- Las opciones deben corresponder a capas reales y disponibles en ese capítulo.
- Mantenerlas sincronizadas con el estado compartido.
- Diferenciar visibilidad y filtro: ocultar una capa no debe cambiar silenciosamente los totales; filtrar registros sí puede recalcularlos, según una regla clara.
- No trasladar todo el panel técnico a un nuevo desplegable saturado.
- Si esos controles no encajan de forma clara y compacta en la barra principal, dejarlos fuera de la interfaz y mantener una selección predeterminada coherente por capítulo.

### Fuentes

Retirar el botón y la sección de navegación «Fuentes». Mantener la atribución cartográfica necesaria y las referencias breves de datos en gráficos o detalles discretos; no reemplazar el botón por otro menú equivalente. Eliminar un acceso del encabezado no requiere borrar la procedencia de las cifras.

## 7. Validación y entregables

Verificar en la aplicación real:

| Caso | Resultado esperado |
|---|---|
| Gráfico en reposo / hover / foco | Fondo translúcido / oscuro / oscuro; texto y series siempre nítidos |
| Moverse dentro del panel y usar tooltips | Sin parpadeo, pérdida de interacción ni cambios de tamaño |
| Dispositivo táctil | Lectura y controles utilizables sin depender del hover |
| Mapa a escala nacional y de detalle | Color natural visible, relieve proporcionado y etiquetas legibles |
| Cambiar capítulos o estilo | Estado conservado y navegación sin solapamientos |
| Acercarse a las islas | «ISLAS MALVINAS», sin rótulo inglés duplicado |
| Cambiar año, unidad o filtros | KPI, variación, ejes y timeline consistentes |
| Revisar el máximo de la serie | Ninguna afirmación de récord contradice los datos mostrados |
| Menú superior | Sin Preguntas, Capas ni Fuentes; Relato continuo funcional |
| Controles de capas, si se integran | Compactos, pertinentes y con efecto claro |

Entregar un informe breve con capturas reales del gráfico en reposo y hover, mapa a color, nombre de las islas y encabezado simplificado. Incluir la auditoría de la comparación con 2017, el máximo de la serie y las unidades: origen, cálculo, hallazgo y corrección aplicada.

Las pruebas deben comprobar comportamiento y cálculos; encontrar cadenas de texto o valores CSS no sustituye la verificación visual e interactiva. Declarar explícitamente las comprobaciones pendientes y las limitaciones del proveedor cartográfico si las hubiera.
