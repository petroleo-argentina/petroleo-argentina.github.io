# Iteración unificada V4 + V5 — Gráficos, overlays, timeline y exploración

## 1. Encargo y alcance

Rediseñar la experiencia de «Petróleo en Argentina» para contar la historia mediante datos: mapa protagonista, gráficos claros sobre el mapa, filtros compactos, indicadores reactivos y una línea temporal inferior compartida. Reducir al mínimo el texto explicativo.

Esta es una única intervención: V4 todavía no se ejecutó. Implementar gráficos, overlays, timeline y filtros como un sistema integrado, sin construir primero una interfaz V4 que luego haya que rehacer para V5.

**Nota de procedencia:** este documento consolida todos los requisitos recuperables de los mensajes de V4 y V5 de la conversación «Concurso de datos», además del informe de Antigravity adjunto. Los archivos Markdown originales y las referencias visuales no estuvieron disponibles para cotejo íntegro. Por ello, no se puede certificar equivalencia literal ni ausencia de requisitos que solo figuraran en esos archivos. Las decisiones operativas siguientes desarrollan los requisitos recuperados; no son transcripciones de los originales. Los nombres de capítulos provienen del informe y deben verificarse en el proyecto.

### Resultado buscado

Cada capítulo debe entenderse con esta composición:

**Título corto + un hallazgo breve cuando aporte valor + mapa + gráfico + filtros.**

El texto mínimo no implica eliminar unidades, fuentes, fechas, leyendas ni etiquetas necesarias para interpretar los datos. La metodología puede quedar en un detalle desplegable.

Mantener el proyecto existente, su navegación y la base cartográfica que funcione. Esta iteración se concentra en la lectura visual y la interacción; no exige rehacer la infraestructura cartográfica.

## 2. Auditoría inicial y contrato de datos

Antes de modificar la interfaz, revisar la implementación real de todos los capítulos. No dar por verificado lo que afirme el informe anterior.

Registrar por capítulo, en una única matriz:

| Campo | Qué documentar |
|---|---|
| Pregunta visual | Qué debe poder descubrir el usuario |
| Gráfico actual | Tipo, tamaño y problema de lectura |
| Datos | Fuente, campos, cobertura temporal y territorial |
| Métrica | Unidad, agregación, denominador y tratamiento de faltantes |
| Mapa | Capas y correspondencia con el conjunto analizado |
| Interacciones | Filtros posibles, selección y comportamiento temporal |
| Cambio propuesto | Gráfico, KPI y anotación que expresan mejor el hallazgo |

Comprobar si los gráficos parecen planos por su tamaño, rango temporal, dominio del eje, normalización, agregación, datos faltantes o errores de cálculo. No resolverlo exagerando diferencias o inventando variación.

Definir identificadores comunes entre registros, mapa y gráficos. Diferenciar cero, dato ausente y combinación sin resultados. No rellenar vacíos con ceros ni interpolar silenciosamente.

Las cifras, porcentajes y trayectorias mencionados en informes previos deben comprobarse contra los datos. No incorporarlos como constantes editoriales sin esa validación.

## 3. Composición de la pantalla

### Mapa y paneles

- Mantener el mapa como superficie principal y conservar visible el territorio relevante.
- Ubicar los gráficos **superpuestos al mapa**, en paneles flotantes legibles. No confinarlos a una columna lateral estrecha ni colocarlos únicamente fuera del área cartográfica.
- Usar un panel lateral sintético para título, hallazgo y navegación. Evitar repetir allí los mismos gráficos, cifras y explicaciones.
- Situar la barra de filtros en la parte superior del área de contenido y la timeline en la parte inferior.
- Reservar espacio para leyendas, atribuciones, controles del mapa, tooltips y navegación. Los overlays no deben tapar el foco geográfico del capítulo.
- Establecer una jerarquía visual: territorio, visualización principal, KPI y controles. Evitar que todas las tarjetas tengan el mismo peso.

### Paneles translúcidos

Crear un tratamiento compartido de fondo translúcido, desenfoque moderado, borde fino, esquinas redondeadas y sombra suave. Ajustar la opacidad según contraste real sobre el mapa: la transparencia no debe hacer ilegibles ejes, etiquetas o cifras.

Usar espaciado y tamaños consistentes, pocos contenedores y suficiente superficie útil para el gráfico. Evitar cajas dentro de cajas y tarjetas decorativas vacías. Ofrecer un fondo más opaco si el desenfoque no está disponible o perjudica el rendimiento.

### Adaptación a pantallas pequeñas

Reubicar los overlays y plegar controles secundarios cuando sea necesario. Mantener accesibles mapa, gráfico, filtros y tiempo sin solapamientos ni desplazamiento horizontal. El usuario debe poder cerrar o contraer un panel para recuperar superficie de mapa sin perder la selección.

## 4. Sistema de gráficos y KPIs

Elegir cada gráfico por la pregunta analítica, no por uniformidad estética:

| Pregunta | Representación preferente |
|---|---|
| Evolución temporal | Línea con fechas, unidad y referencias directas |
| Comparación entre categorías | Barras ordenadas o puntos comparables |
| Participación en un total | Barras de participación o composición, con denominador explícito |
| Concentración | Curva acumulada o ranking con umbral destacado |
| Variables de distinta unidad | Pequeños gráficos separados y alineados |
| Evolución de cohortes | Series por cohorte sobre una edad común |

Estas opciones se validan contra los datos disponibles; no crear series ni categorías para completar el diseño.

### Reglas de lectura

- Dar al gráfico tamaño suficiente para entenderlo sin abrir un tooltip.
- Mostrar unidad y período; usar pocas marcas de eje, legibles y bien distribuidas.
- Conservar una semántica de color común entre mapa, gráfico, leyenda y selección.
- Destacar la serie o categoría relevante y atenuar el contexto sin borrarlo.
- Usar etiquetas y anotaciones directas en puntos relevantes; eliminar párrafos que repitan lo visible.
- En barras, partir de cero. En líneas, cualquier dominio recortado debe quedar claro y no inducir comparaciones engañosas.
- Mantener escalas comparables cuando se comparan períodos o categorías; si el dominio cambia con un filtro, hacer visible ese cambio.
- No añadir volumen 3D, sombras de barras ni animaciones ornamentales para que los gráficos parezcan menos planos.
- Los tooltips deben aportar valor exacto, unidad, fecha y categoría, con acceso equivalente mediante foco o toque.

### KPIs reactivos

Usar pocos indicadores, de gran legibilidad. Cada uno debe indicar qué mide, su unidad y el alcance temporal necesario. Actualizar cifra, comparación y anotación al cambiar el estado.

Toda variación debe identificar su base de comparación. No mostrar porcentajes con denominador cero ni mantener un hallazgo fijo cuando los filtros ya no lo sostienen. Cuando no exista una comparación válida, mostrar el valor disponible o una ausencia explícita.

## 5. Aplicación por capítulo

La siguiente matriz fija una dirección de trabajo a verificar en el código y los datos. No cambia los hechos ni impone información que el proyecto no tenga.

| Capítulo según el informe | Objetivo visual y rediseño | Interacción propuesta, si hay datos |
|---|---|---|
| 01 · Argentina | Mostrar la evolución general con una serie amplia, hitos comprobados y un KPI principal. Hacer visible qué período se está mirando. | Período y dimensiones nacionales realmente disponibles. El mapa debe declarar si representa un corte temporal o el período agregado. |
| 02 · Territorio | Mostrar cómo cambia la distribución territorial. Vincular la evolución de participaciones o valores con las mismas regiones del mapa. | Selección de territorio y tiempo; trasladar la timeline existente al sistema global. |
| 03 · Producción | Hacer legible la distribución o comparación de producción en el corte elegido, con unidad y agregación explícitas. | Período, territorio y entidades presentes en la fuente. Selección coordinada de puntos, barras o categorías. |
| 04 · Concentración | Mostrar qué proporción de entidades explica qué proporción del total mediante curva acumulada o ranking. | Recalcular orden, total y umbral con los filtros. Si es posible, resaltar en el mapa las entidades que integran el tramo seleccionado. |
| 05 · Tecnología | Separar longitud lateral y etapas de fractura en dos gráficos apilados con una base temporal común. | Compartir filtros, período y selección entre ambos gráficos y el mapa; preservar unidades independientes. |
| 06 · Cohortes | Comparar cohortes sobre una edad común, distinguiendo edad del pozo y fecha calendario. Mostrar hasta dónde llega cada serie observada. | Selección de cohortes y filtros compatibles. El período global selecciona cohortes o registros según una regla documentada; no sustituye silenciosamente el eje de edad. |
| 07 · Economía | Mostrar las métricas económicas existentes con moneda, unidad y base de precios identificables. Separar magnitudes incompatibles. | Filtros y períodos respaldados por la fuente; no sugerir una correspondencia geográfica inexistente. |
| 08 · Síntesis | Cerrar con pocos indicadores y visualizaciones que sinteticen hallazgos verificados, sin repetir bloques narrativos. | Mantener visible el alcance elegido y permitir volver al relato o continuar explorando. |

### Prioridad especial: capítulo 05

Colocar arriba **longitud lateral** y debajo **etapas de fractura**. Cada gráfico tendrá su eje vertical y unidad; ambos compartirán eje temporal, alineación y selección. Evitar un único gráfico de doble eje.

Definir si cada valor representa media, mediana, suma u otra medida y cuántos registros lo respaldan. Si las dos variables tienen distinta cobertura, señalarla; no presentar las muestras como idénticas sin verificarlo.

Si el mapa muestra trayectorias, distinguir medición y representación esquemática. No deducir geometría real a partir de una longitud agregada ni presentar una asociación visual como causalidad.

## 6. Filtros y exploración guiada

### Barra superior

Crear una barra compacta con filtros relevantes para el capítulo activo. Considerar período, territorio, cuenca, provincia, operador, tipo de recurso o cohorte **únicamente cuando existan esos campos y tengan sentido analítico**.

- Mostrar la selección activa y una acción clara para restablecerla.
- Mantener pocas opciones prioritarias visibles; agrupar las secundarias.
- Generar opciones desde los datos y explicar brevemente las opciones deshabilitadas.
- Evitar combinaciones imposibles y filtros que no afecten ninguna visualización.
- Distinguir filtros globales y específicos del capítulo.
- Conservar los filtros compatibles al navegar. Si uno deja de ser válido, comunicar su ajuste de forma breve y visible.
- Una selección cartográfica o gráfica debe poder quitarse sin borrar todos los demás filtros.

No duplicar controles temporales independientes: cualquier selector de fechas debe modificar el mismo estado que la timeline.

### Relato y Explorar

La V5 planteó este cambio como posibilidad. Se propone incorporarlo como dos comportamientos de la misma interfaz, sin duplicar pantallas ni componentes:

| Modo | Comportamiento |
|---|---|
| Relato | Entrada guiada por capítulos, con vista inicial, período y selección editorial comprobada. Texto limitado al título y, cuando aporte, un hallazgo. |
| Explorar | Permite variar filtros, tiempo y selección para investigar los datos. Mantiene contexto y navegación. |

Al modificar manualmente un filtro durante el relato, permitir la exploración y dejar claro el estado actual. Volver al relato debe restablecer explícitamente la vista editorial del capítulo. Si se adopta una única interfaz sin selector de modo, conservar estas dos capacidades mediante una acción visible de «Restablecer vista del capítulo» y documentar la decisión.

## 7. Timeline inferior global

Implementar una única `GlobalTimeline` para toda la experiencia; no dejarla aislada en el capítulo 02.

- Mostrar período activo, límites disponibles y resolución temporal apropiada.
- Permitir elegir un instante o un rango según lo que soporte el análisis del capítulo.
- Mantener posición y lenguaje visual coherentes entre capítulos.
- Actualizar conjuntamente mapa, gráficos, KPIs y anotaciones al mover la selección.
- Ajustar el dominio a la cobertura real. Cuando un capítulo tenga un único corte, mostrarlo como tal; no simular una serie ni habilitar un control sin efecto.
- Cuando no haya dimensión temporal aplicable, conservar el contexto e indicar esa condición de forma compacta.
- Si cambia la cobertura al navegar, conservar la selección cuando sea válida y mostrar cualquier ajuste necesario.
- Admitir teclado y toque. Si se incluye reproducción automática, ofrecer pausa y respetar la preferencia de movimiento reducido.

En gráficos de evolución, distinguir el dominio histórico visible de la ventana seleccionada: puede conservarse una serie de contexto atenuada, siempre que el usuario pueda identificar qué parte determina el mapa y los KPIs. Un gráfico filtrado por completo también es válido; adoptar una regla coherente y documentarla.

## 8. Estado compartido y componentes reutilizables

Usar una única fuente de verdad para capítulo, modo, filtros, selección temporal y entidad seleccionada. Adaptar la implementación a la tecnología existente; los nombres siguientes describen responsabilidades, no obligan a migrar de framework.

| Componente | Responsabilidad |
|---|---|
| `OverlayPanel` | Contenedor común: transparencia, borde, radio, espaciado y adaptación de tamaño |
| `OverlayChart` | Presentación común de gráficos, ejes, unidades, leyendas, tooltips y estados |
| `ReactiveOverlayChart` | Conexión de `OverlayChart` con los datos derivados y la selección compartida |
| `OverlayBigNumber` | Presentación tipográfica reutilizable de un indicador |
| `DynamicKPI` | Cálculo y actualización de indicadores, usando `OverlayBigNumber` |
| `FilterBar` | Filtros contextuales, selecciones activas y restablecimiento |
| `GlobalTimeline` | Control temporal común y cobertura disponible |

No mantener dos sistemas paralelos para gráficos estáticos y reactivos, ni para cifras grandes y KPIs. Componer las responsabilidades anteriores.

Flujo común:

```text
Filtro / timeline / selección / cambio de capítulo
                        ↓
                 Estado compartido
                        ↓
        Datos derivados y agregaciones consistentes
                        ↓
       Mapa + gráficos + KPIs + anotaciones + leyendas
```

Evitar filtros calculados con reglas distintas en cada componente. No es necesario que todas las vistas tengan la misma agregación, pero sí deben representar el mismo alcance y declarar sus diferencias.

Resolver respuestas fuera de orden para que una consulta anterior no reemplace el estado más reciente. Mostrar carga, error y ausencia de datos sin conservar cifras antiguas como si fueran actuales. Limitar trabajo durante el arrastre de la timeline y reutilizar datos cuando sea posible.

## 9. Texto, accesibilidad y desempeño

### Texto mínimo

Eliminar introducciones largas, explicaciones redundantes e instrucciones como «qué observar» cuando la interacción y las etiquetas ya resulten claras. Usar títulos concretos, anotaciones directas y mensajes de estado breves. Reservar fuente y metodología para un acceso discreto y disponible.

El hallazgo puede omitirse si no añade información. Si se genera a partir de datos, debe reaccionar a filtros y tiempo, y desaparecer cuando deje de ser válido.

### Accesibilidad

Verificar contraste de paneles y gráficos sobre distintas zonas del mapa, foco visible, etiquetas de controles, navegación por teclado, objetivos táctiles utilizables y significado independiente del color. Hacer accesibles los valores esenciales sin depender exclusivamente del hover. Evitar animaciones que impidan leer o interactuar.

### Desempeño

Reutilizar la instancia del mapa y actualizar sus capas sin recrearlo por cada filtro. Medir respuesta de controles, carga de datos y fluidez temporal en la aplicación real. Registrar dispositivo, navegador, volumen de datos y método. No afirmar objetivos de rendimiento cumplidos sin medición.

## 10. Validación y criterios de aceptación

Realizar una auditoría visual y de interacción sobre la aplicación ejecutándose. Las capturas del informe previo incluyen imágenes generadas para simular pantallas; no deben aceptarse como evidencia visual de la interfaz implementada. Capturar pantallas reales. Si el entorno bloquea una verificación, declararla pendiente.

| Caso | Resultado exigido |
|---|---|
| Abrir cada capítulo | Pregunta visual comprensible, gráfico legible, unidad y alcance visibles |
| Cambiar un filtro | Mapa, gráfico, KPI, leyenda y hallazgo representan el nuevo estado |
| Combinar filtros | Opciones coherentes y resultados con el mismo alcance analítico |
| Arrastrar la timeline | Actualización consistente, sin saltos a respuestas antiguas |
| Elegir un período vacío | Estado sin datos; no ceros inventados ni cifras anteriores |
| Seleccionar una entidad | Resaltado coordinado donde exista correspondencia verificable |
| Cambiar de capítulo | Filtros compatibles conservados y ajustes temporales visibles |
| Restablecer la vista | Recuperación reproducible de los valores iniciales del capítulo |
| Revisar capítulo 05 | Dos gráficos apilados, unidades separadas y tiempo compartido |
| Revisar cohortes | Edad y fecha calendario distinguibles; sin prolongar series no observadas |
| Pantalla pequeña y teclado | Controles accesibles y ausencia de elementos críticos tapados |
| Carga o error | Estado explícito y recuperación sin valores engañosos |

Contrastar al menos una combinación filtrada y una selección temporal con cálculos independientes de la interfaz. Verificar denominadores, agregaciones y faltantes. Ejecutar las comprobaciones existentes pertinentes y añadir pruebas de sincronización y cálculo cuando sean necesarias.

La implementación se considera terminada cuando:

- [ ] Todos los capítulos fueron auditados y tienen una visualización adecuada a su pregunta.
- [ ] Los gráficos tienen protagonismo y se integran como overlays sobre el mapa.
- [ ] Los paneles comparten transparencia controlada, borde fino y esquinas redondeadas.
- [ ] La timeline pertenece al sistema global y expresa las limitaciones temporales de cada capítulo.
- [ ] Los filtros, el mapa, los gráficos, los KPIs y las anotaciones están sincronizados.
- [ ] La exploración conserva contexto y ofrece una forma clara de volver a la vista editorial.
- [ ] El capítulo 05 separa longitud lateral y etapas de fractura.
- [ ] Se redujo el texto sin eliminar información indispensable para interpretar los datos.
- [ ] Los estados vacíos, errores y cambios de cobertura funcionan de forma coherente.
- [ ] La validación usa la aplicación real y distingue pruebas realizadas de pendientes.

## 11. Orden de implementación y entrega

Trabajar en este orden para evitar duplicaciones:

1. Auditar capítulos, datos, cálculos e interacciones existentes.
2. Definir el estado común y los contratos de filtro, tiempo y selección.
3. Implementar los componentes visuales y reactivos compartidos.
4. Aplicar el diseño por capítulo, priorizando la legibilidad del 05.
5. Integrar filtros, timeline y exploración guiada sobre ese mismo sistema.
6. Reducir textos, ajustar diseño adaptable y revisar accesibilidad.
7. Validar interacciones, cálculos y desempeño; corregir fallos antes de cerrar.

Entregar la implementación junto con **un único informe consolidado** que incluya:

- Matriz de auditoría inicial y cambios finales por capítulo.
- Reglas de filtros, tiempo, selección y agregación; fuentes y cobertura efectiva.
- Componentes creados o reutilizados y decisiones de diseño relevantes.
- Capturas reales antes/después cuando se disponga del estado anterior, incluyendo capítulo 05, filtros activos, timeline y pantalla pequeña.
- Resultados de pruebas y mediciones, con condiciones y evidencia.
- Limitaciones, verificaciones pendientes y ubicación de los archivos modificados.

Actualizar la documentación existente que corresponda sin crear informes V4 y V5 separados ni duplicar la misma especificación. No presentar la intervención como completa si faltan interacciones esenciales o la evidencia no corresponde a la aplicación real.
