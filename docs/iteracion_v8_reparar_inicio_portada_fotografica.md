# Iteración V8 — Reparar el inicio y añadir una portada fotográfica

## 1. Prioridad: recuperar el acceso al recorrido

El botón «Comenzar el recorrido» no funciona. Reparar primero el arranque de la aplicación y después incorporar la imagen de portada. Mantener las mejoras V6/V7 y los siete capítulos existentes.

### Hallazgo comprobado

Se realizó una comprobación de sintaxis sobre el archivo local:

```text
C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina\frontend\app.js

node --check frontend/app.js
SyntaxError: Unexpected end of input
```

El error se informó al final del archivo, en la línea 2378 de la versión inspeccionada. Esa posición indica dónde el analizador agotó el archivo; **no identifica necesariamente dónde se originó el error**. Hay que localizar la estructura incompleta, no añadir una llave al final por ensayo.

Un error de sintaxis impide ejecutar el archivo completo, incluido el registro de eventos de la portada. Esto constituye una causa concreta del fallo observado; una vez resuelto, comprobar si quedan errores de ejecución adicionales.

En la versión inspeccionada existen:

- El botón HTML `#btn-start-tour`.
- La función `setupHeroSplash()`, que registra el clic, añade `hero-hidden` a `#hero-splash` y llama a `goToStep(0)`.
- Una llamada a `setupHeroSplash()` dentro de `initScrollyPlatform()`.
- El registro de `initScrollyPlatform` en `DOMContentLoaded`.

Por tanto, no crear un segundo botón ni duplicar su manejador como primera solución.

## 2. Reparación del código y del flujo de entrada

1. Reproducir el error de sintaxis en el estado actual antes de editar.
2. Revisar los cambios recientes de V7 y localizar llaves, paréntesis, cadenas, plantillas o comentarios sin cerrar. Prestar atención a bloques eliminados junto con Preguntas, Capas y Fuentes, sin dar por confirmado que allí esté el origen.
3. Corregir la estructura exacta y volver a ejecutar la comprobación de sintaxis hasta que pase.
4. Abrir la aplicación en un navegador real y revisar la consola desde una recarga completa.
5. Comprobar que las funciones ejecutadas antes de `setupHeroSplash()` no fallan y abortan el registro del botón.
6. Verificar el clic, la desaparición de la portada y la entrada efectiva al capítulo 01, con mapa, gráfico y controles utilizables.

No ocultar excepciones con un `try/catch` vacío ni borrar llamadas hasta que el botón parezca responder. Identificar y documentar la causa concreta del error.

### Carga y recuperación

- El control de entrada debe registrarse sin depender de que termine una descarga de tiles o imágenes.
- Al pulsarlo, la aplicación debe responder inmediatamente. Si los datos esenciales siguen cargando, mostrar un estado breve y accesible de carga antes de presentar el capítulo completo.
- Si se necesita esperar para ejecutar `goToStep(0)`, gestionar explícitamente ese estado y completar la entrada una sola vez cuando corresponda.
- Evitar dobles inicializaciones, manejadores duplicados y carreras entre el clic y la carga del mapa.
- Si falla una fuente cartográfica, utilizar la alternativa disponible o comunicar el fallo con posibilidad de reintentar; no dejar un botón aparentemente inerte.
- Al ocultarse, la portada no debe conservar una capa invisible que capture clics ni controles ocultos accesibles mediante Tab.
- Llevar el foco a un elemento apropiado del recorrido y conservar navegación por teclado.

## 3. Portada con fotografía real

Sustituir el fondo casi negro y vacío por una **fotografía panorámica real de Vaca Muerta o del paisaje petrolero neuquino**. Priorizar una imagen donde se vean territorio, meseta y alguna instalación o pozo, con luz natural y una composición amplia.

Si no se consigue una imagen adecuada de Vaca Muerta, utilizar una fotografía verificada de la Patagonia argentina vinculada visualmente al tema. No rotular una imagen genérica como si fuera de Vaca Muerta ni usar una imagen generada como fotografía documental del lugar.

### Selección del recurso

- Buscar una imagen con permiso de uso adecuado y procedencia verificable; preferir recursos existentes del proyecto cuando cumplan estos requisitos.
- Registrar autor, ubicación identificada, página de origen, licencia y crédito requerido.
- No tomar como permiso una imagen encontrada en un buscador o una captura de una noticia.
- Guardar el recurso autorizado dentro de los recursos del proyecto, evitando depender de una URL temporal o de hotlinking.
- No incorporar una imagen de baja resolución, estirada o con una marca de agua.

### Composición visual

- Fotografía a pantalla completa, con encuadre adaptable a escritorio y móvil.
- Mantener el título «PETRÓLEO EN ARGENTINA», el subtítulo «Del pozo al país» y un único botón principal «Comenzar el recorrido».
- Conservar el texto introductorio breve; no añadir párrafos para explicar la fotografía.
- Aplicar un degradado oscuro localizado detrás del texto y controles. El paisaje debe seguir siendo visible y conservar sus colores, sin quedar sepultado bajo una capa negra uniforme.
- Mantener el acento dorado del botón y la tipografía editorial existente.
- Elegir el punto focal de la imagen para evitar cortar el motivo principal en móvil. Adaptar el recorte o usar una variante vertical si hace falta.
- Incorporar el crédito necesario de forma discreta y legible, sin recuperar el menú Fuentes eliminado.
- No añadir carrusel, video automático, parallax ni animaciones que distraigan del inicio.

La fotografía debe actuar como fondo decorativo si no aporta información adicional al texto; en ese caso, usar semántica accesible acorde. Si se presenta como contenido informativo, incluir una descripción alternativa fiel.

### Rendimiento y resistencia a fallos

- Exportar tamaños apropiados y formatos comprimidos compatibles, conservando suficiente detalle.
- Cargar la imagen principal con prioridad adecuada; no diferirla como si estuviera fuera de pantalla.
- Evitar cambios de posición del título o botón cuando termine la descarga.
- Mantener un fondo alternativo coherente si la imagen falla.
- La imagen nunca debe ser una condición para que funcione «Comenzar el recorrido».
- Los elementos decorativos superpuestos no deben interceptar clics.

## 4. Comprobaciones obligatorias

El informe V7 indica que la revisión de navegador no se completó por un problema de infraestructura. Sus 25 pruebas y la respuesta HTTP 200 no prueban que el JavaScript pueda ejecutarse ni que el botón funcione. Añadir verificación real de este flujo.

| Prueba | Resultado esperado |
|---|---|
| Sintaxis de `app.js` | Sin errores |
| Recarga completa | Sin excepciones de arranque en consola |
| Clic en «Comenzar el recorrido» | Entrada efectiva al capítulo 01 |
| Foco + Enter o Espacio | Misma entrada mediante teclado |
| Clic antes de completar la carga | Respuesta visible y entrada al quedar listo, sin carrera ni bloqueo |
| Clics repetidos | Sin mapas, eventos o transiciones duplicados |
| Imagen bloqueada o ausente | Fondo alternativo y botón funcional |
| Fallo de tiles o datos | Estado explícito y recuperación; sin fallo silencioso |
| Entrada al capítulo | Portada oculta sin interceptar clics ni foco |
| Escritorio y móvil | Foto bien recortada, texto legible y botón accesible |
| Navegación posterior | Siete capítulos, filtros, timeline y relato continuo funcionales |

Incluir una prueba de regresión de navegador que abra la portada, pulse el botón y compruebe tanto la salida de la portada como la visibilidad y funcionamiento del capítulo inicial. Verificar también errores de página. Una prueba que solo busca el identificador del botón en el HTML no cubre este fallo.

Si el navegador automatizado no está disponible, realizar la prueba manual en un navegador accesible y registrar lo realmente observado. Si tampoco puede verificarse manualmente, dejarlo expresamente pendiente; no afirmar que el botón quedó reparado basándose solo en pruebas estáticas.

## 5. Entrega

Entregar la corrección y la fotografía integrada junto con un informe breve:

- Causa exacta del error de sintaxis y cambio que lo resuelve.
- Resultado de la comprobación de sintaxis y del flujo real de entrada.
- Imagen elegida, procedencia, permiso y crédito.
- Capturas reales de portada en escritorio y móvil, y del capítulo 01 después de pulsar el botón.
- Verificaciones pendientes o limitaciones, si existen.

No sustituir capturas de la aplicación por composiciones simuladas ni declarar el trabajo completo si el recorrido sigue inaccesible.
