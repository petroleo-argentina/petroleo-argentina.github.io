# Iteración V9 — Zoom libre, fotos de pozos y guía Argentinosaurus

## 1. Alcance

Implementar sobre la versión actual: rueda exclusivamente para zoom del mapa, miniaturas fotográficas progresivas, Alegreya + Archivo, panel izquierdo translúcido y un Argentinosaurus que reemplace parte de la explicación. Mantener siete capítulos, el inicio reparado, la cartografía a color y las correcciones editoriales anteriores.

Recursos adjuntos a esta especificación:

CARPETA C:\Users\ESCRITORIO\Documents\Codex\2026-10-04\referenced-chatgpt-conversation-this-is-an\outputs

- `argentinosaurus-guia.png`: ilustración original generada para el proyecto, con fondo transparente.
- `demo_argentinosaurus.html`: demostración autónoma de movimiento suave, globo separado y controles. No es la aplicación integrada ni contiene los hallazgos finales de sus capítulos.

## 2. Rueda y trackpad: zoom, nunca avance de capítulo

El usuario quiere acercarse o alejarse sin cambiar el relato.

- Retirar el avance de capítulos asociado a `wheel`, incluyendo la llamada y el comportamiento de `setupScrollWheelNavigation()` identificados en versiones anteriores.
- Revisar listeners globales y locales, acumuladores de desplazamiento y cualquier `preventDefault` que bloquee el zoom nativo del mapa.
- Conservar el scroll zoom de MapLibre sobre el lienzo, incluyendo gestos compatibles de trackpad.
- Una interacción de zoom no puede modificar `chapterIndex`, año, filtros o selección editorial, ni disparar una cámara que deshaga el encuadre elegido.
- Sobre un panel con contenido desplazable, la rueda desplaza su contenido, sin avanzar capítulos ni atravesarlo para mover el mapa.
- Conservar los botones anterior/siguiente y los puntos de navegación como acciones explícitas del relato.
- El relato automático solo avanza cuando fue activado expresamente. Pausarlo al iniciar una exploración manual del mapa para evitar que la cámara o el capítulo cambien mientras el usuario hace zoom; permitir reanudarlo explícitamente.

Verificar un recorrido prolongado con rueda y trackpad: cambia la escala y permanece el mismo capítulo. No resolver el problema deshabilitando todo el zoom ni exigiendo una tecla modificadora.

## 3. Fotos de pozos al acercarse

Usar una representación progresiva según escala y densidad:

| Vista | Representación |
|---|---|
| Nacional o regional | Puntos o agrupaciones legibles |
| Acercamiento intermedio | Puntos individuales; miniaturas en selección si hay fotografía |
| Detalle local | Miniaturas pequeñas de los pozos con fotografías verificadas, según espacio disponible |

Los umbrales de zoom se calibran en el mapa real, no con números arbitrarios que produzcan superposición.

- Cada fotografía debe vincularse a un identificador de pozo o instalación. No repetir una foto genérica como si documentara cada ubicación.
- Si solo existe una imagen de la zona, mostrarla en el popup con la etiqueta «Imagen de contexto: [lugar]»; no convertirla en una foto atribuida al pozo.
- Cuando no exista una foto autorizada y verificada, conservar el punto. Un icono de instalación también puede usarse si se distingue claramente de una fotografía.
- Mantener el anclaje exacto a la coordenada y un borde que conserve el significado de categoría o selección.
- Limitar cantidad de miniaturas simultáneas, gestionar colisiones y priorizar el elemento seleccionado. No llenar la pantalla de cientos de imágenes.
- Cargar solo miniaturas visibles, reutilizar recursos y mantener una alternativa si falla la descarga.
- El clic abre información y la imagen ampliada con autor, procedencia y licencia. La selección mantiene la correspondencia con gráficos y filtros.
- Si un punto representa datos agregados o desplazados visualmente, no presentarlo como posición fotográfica exacta de un pozo.

Crear un inventario fotográfico con identificador, URL o ruta local, lugar, autor, página original, licencia y condición de uso. No inventar fotos de instalaciones reales con IA para llenar vacíos documentales.

## 4. Foto actual de portada: verificación y crédito

El informe V8 identifica la foto como «Petrosaurios», Aguada Pichana, de Horacio Fernandez y declara CC BY 3.0:

https://commons.wikimedia.org/wiki/File:%22Petrosaurios%22,_Aguada_Pichana,_A%C3%B1elo,_Neuquen,_ARG._-_panoramio_(1).jpg

En esta revisión se pudo leer la declaración local, pero no recuperar la ficha original de Commons. **La licencia de esta imagen concreta queda pendiente de confirmación en su página de origen.** No considerar la atribución escrita por la aplicación una prueba independiente.

La licencia CC BY 3.0 permite compartir y adaptar, también comercialmente, bajo sus condiciones. Consultar:

https://creativecommons.org/licenses/by/3.0/deed.es

Antes de publicar, comprobar que archivo, autor y licencia coinciden. Completar el crédito con título, autor, enlace a la ficha, enlace a la licencia y una nota sobre el recorte/tratamiento aplicado cuando corresponda. El crédito actual en texto plano no incluye estos enlaces.

Ejemplo a utilizar solo una vez confirmada la ficha:

> «Petrosaurios», Aguada Pichana — Horacio Fernandez. CC BY 3.0. Imagen recortada; superposición oscura para facilitar la lectura.

Enlazar título y licencia. Revisar también el contexto de uso por la persona identificable y las obras o marcas visibles; la licencia fotográfica no garantiza por sí sola todos los derechos posibles. No afirmar «sin copyright» ni «sin restricciones».

Editorialmente, la foto muestra una escultura, un cartel y una persona. Puede usarse como contexto del lugar si se verifica su permiso, pero no describe visualmente un pozo operativo. Si se busca una portada más limpia, preferir un paisaje petrolero autorizado y correctamente identificado; no reemplazarla por una imagen sin procedencia.

## 5. Tipografías elegidas

Adoptar exactamente dos familias:

| Familia | Uso |
|---|---|
| Alegreya | Título de portada, subtítulo en cursiva y títulos editoriales de capítulos |
| Archivo | Filtros, botones, texto breve, globos del dinosaurio, cifras, ejes y tooltips |

Fuentes de los proyectos:

- https://github.com/huertatipografica/Alegreya
- https://github.com/Omnibus-Type/Archivo

Usar distribuciones oficiales con licencia OFL y conservar sus avisos y archivos de licencia junto con las fuentes. Alojar los archivos web localmente cuando sea posible, cargar solamente los pesos necesarios y configurar fuentes alternativas coherentes.

Revisar ñ, tildes, signos, m³, porcentajes, separadores numéricos y alineación de cifras. Comprobar que títulos, botones y filtros no se desbordan. En gráficos sobre canvas, aplicar explícitamente Archivo y actualizar el dibujo cuando la fuente esté lista. No limitar el cambio al CSS del cuerpo de la página.

## 6. Panel izquierdo con el mismo comportamiento del derecho

- Reutilizar los tokens de superficie del gráfico: fondo oscuro neutro translúcido en reposo y más opaco en hover y `focus-within`.
- Como referencia inicial, alfa 0,68 en reposo y 0,94 al interactuar; ajustar tras comprobar contraste sobre el mapa.
- Modificar el fondo, nunca la opacidad completa del panel. Textos, controles y personaje deben conservar nitidez.
- Mantener el estado mientras el usuario interactúa con sus controles o con el globo asociado.
- En táctil, usar una superficie suficientemente opaca para leer sin depender del hover.
- Conservar tamaños durante la transición y respetar movimiento reducido.

## 7. Argentinosaurus como guía del relato

Usar `argentinosaurus-guia.png` como base visual. Es una ilustración estilizada generada mediante la herramienta integrada de imágenes para este proyecto, sin referencia a personajes comerciales existentes. No es una reconstrucción paleontológica científica ni se certifica como obra de dominio público o de exclusividad garantizada.

El PNG es estático; el movimiento de la demo se produce mediante CSS. Para esta primera integración, animar una respiración/oscilación muy leve y una aparición breve al cambiar de capítulo. No afirmar que existe una animación articulada de ojos, boca o extremidades: eso requeriría poses adicionales o un personaje preparado por partes.

### Función editorial

El dinosaurio debe **reemplazar texto**, no sumar otro bloque a la pantalla.

- Reducir el panel izquierdo a número de capítulo, título, contexto mínimo y navegación.
- Trasladar la explicación principal a un globo breve del guía, de aproximadamente 15–30 palabras y una sola idea.
- No repetir el KPI, el párrafo del panel y el mismo mensaje en el globo.
- Conservar unidades, fuentes y metodología accesibles en sus lugares correspondientes.
- Usar tono argentino natural y claro, sin exagerar modismos ni infantilizar el análisis.
- Mostrar el texto como HTML separado del PNG, para actualizarlo, seleccionarlo y permitir su lectura asistida.
- Por ahora «que lo diga el dino» significa un globo escrito. No reproducir voz o audio automáticamente.

### Ubicación e interacción

- Integrar el guía junto al panel izquierdo, en una zona reservada. Probar un ancho visual de aproximadamente 90–130 px, ajustando por pantalla.
- No cubrir el territorio relevante, controles, timeline, filtros ni recorrido lateral.
- Permitir «Ocultar guía» y un acceso discreto para recuperarlo. Recordar esa preferencia durante la sesión.
- Al ocultarlo, conservar acceso opcional a la explicación breve del capítulo; no restaurar automáticamente un párrafo largo.
- El globo no captura scroll del mapa fuera de su propia área ni se convierte en un paso obligatorio.
- En móvil, plegar la explicación y abrirla a pedido si falta espacio.
- Con movimiento reducido, mostrar la ilustración quieta. Mantener opción de pausar la animación.

### Relato conectado a datos

Crear mensajes por identificador de capítulo y derivarlos del estado compartido. Los nombres siguientes deben cotejarse con el proyecto:

| Capítulo | Papel del guía |
|---|---|
| Argentina | Explicar una comparación temporal comprobada sin afirmar falsos récords |
| Territorio | Señalar el cambio territorial que sostiene la selección actual |
| Producción | Aclarar convencional/no convencional y la comparación mostrada |
| Concentración | Explicar qué representa el tramo o umbral seleccionado |
| Tecnología | Distinguir longitud lateral y etapas, sin confundir unidades |
| Cohortes | Aclarar edad del pozo frente a fecha calendario |
| Economía | Conectar la métrica mostrada con su alcance, sin inventar causalidad |

No copiar cifras de capturas al guion. Al cambiar filtros o tiempo, actualizar el hallazgo; si deja de estar sustentado, sustituirlo por una frase descriptiva o retirarlo. Sin datos, mostrar una ausencia clara. No anunciar cambios en cada paso del arrastre de la timeline; actualizar al estabilizar la selección.

Puede incluir una presentación inicial breve: «Soy un Argentinosaurus de la Patagonia. Te acompaño por los datos: el petróleo no viene de dinosaurios». Verificar el texto científico final y no convertirlo en una explicación repetida en cada capítulo.

## 8. Pruebas y entrega

- Comprobar sintaxis antes de abrir la aplicación y probar «Comenzar el recorrido» para no repetir la regresión anterior.
- Hacer zoom repetidamente: el capítulo no cambia y la cámara no se restablece sola.
- Probar scroll dentro de paneles y la pausa del relato automático al explorar el mapa.
- Verificar miniaturas en distintas densidades, asociaciones correctas, licencias, ausencia de fotos y fallos de carga.
- Confirmar Alegreya y Archivo realmente cargadas, también en gráficos y tooltips.
- Comparar ambos paneles en reposo, hover, teclado y táctil.
- Comprobar que el dinosaurio reduce el texto total y que sus mensajes responden a tiempo y filtros.
- Verificar ocultar/recuperar guía, movimiento reducido y uso en móvil.

Entregar capturas reales y un informe breve con cambios, verificaciones y pendientes. No considerar la demo adjunta como prueba de integración. Mantener expresamente pendiente la validación de la foto de portada hasta acceder a su fuente original.
