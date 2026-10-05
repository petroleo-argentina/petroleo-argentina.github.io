# Iteración V11 — El dinosaurio cuenta hallazgos reales

## 1. Corrección editorial

Mantener el personaje, su ubicación y su comportamiento actual. Cambiar el contenido de sus globos: el usuario quiere **datos interesantes que complementen el gráfico superior derecho**, no instrucciones para leerlo ni definiciones genéricas.

Esta instrucción reemplaza los mensajes conceptuales propuestos en V10. El ejemplo «Una región puede ganar participación aunque otra siga produciendo más. Compará porcentajes y volúmenes para distinguir esos cambios» debe retirarse.

El dinosaurio funciona como un pequeño comentarista de los datos: señala algo concreto que el gráfico contiene pero que no resulta evidente de inmediato. No describe los controles ni repite el KPI principal.

## 2. Qué debe decir

Elegir por capítulo una comparación, un cambio, una concentración o un hito comprobable. Cada globo debe incluir:

- Un sujeto identificable: región, operador, grupo de pozos, cohorte o variable.
- Una cifra o comparación concreta cuando los datos la permitan.
- El período y alcance necesarios para interpretarla.
- Una idea complementaria al gráfico, expresada en una o dos frases breves.

Ejemplos de estructuras, **no frases finales ni cifras para inventar**:

| Si el gráfico muestra… | El dino puede aportar… |
|---|---|
| Producción nacional y variación interanual | Cuánto falta para el máximo comparable de la serie y en qué año ocurrió |
| Participación territorial actual | Cuántos puntos porcentuales ganó la región líder desde el inicio del período comparable |
| Convencional frente a no convencional | Cuándo se cruzaron ambas series y cómo cambió la diferencia desde entonces |
| Curva de concentración | Qué porcentaje de pozos explica una proporción determinada de la producción |
| Longitud lateral y etapas | Cómo varió una medida adicional válida, como etapas por kilómetro, si ambas variables son comparables |
| Producción de cohortes por edad | Diferencia entre cohortes a la misma edad, con muestra suficiente |
| Una variable económica | Mayor cambio dentro del período, o comparación real disponible que no repita el indicador principal |

No utilizar mensajes de concentración, récord o cruces si no pueden calcularse en la fuente real.

## 3. Propuestas de redacción para construir con datos

Las siguientes plantillas usan campos entre llaves. **No renderizar ninguna llave ni rellenarla con una cifra estimada.** Primero calcular y verificar cada valor; luego producir la frase completa.

### Argentina

«Aunque creció en {año}, la producción todavía quedó {porcentaje}% por debajo del máximo de {año_del_máximo}.»

Usar solamente si el gráfico ya destaca el crecimiento y la serie comparable sostiene esa diferencia. Si se alcanzó un máximo, redactar el resultado correcto y precisar la cobertura histórica; no forzar esta plantilla.

### Territorio

«{Región} pasó del {participación_inicial}% al {participación_final}% de la producción entre {inicio} y {fin}: ganó {diferencia} puntos porcentuales.»

Si ese cambio ya está escrito en el gráfico, seleccionar otro hallazgo comprobado, como el cambio de posición de otra región o la concentración conjunta de las dos principales.

### Producción

«El no convencional superó al convencional en {mes_y_año}. En {fecha_actual}, la diferencia llegó a {brecha} puntos porcentuales.»

Usar el cruce calculado y aclarar el alcance territorial si hay filtros. Si no hay cruce en la serie seleccionada, elegir un hallazgo alternativo válido.

### Concentración

«El {porcentaje_de_pozos}% de los pozos concentra el {porcentaje_de_producción}% de la producción del conjunto seleccionado.»

No duplicar el umbral si ya es la única cifra protagonista del gráfico. Puede compararse con otro período solo si se mantiene una población y una metodología compatibles.

### Tecnología

«Entre {inicio} y {fin}, {métrica} cambió de {valor_inicial} a {valor_final} {unidad}: una variación del {porcentaje}%.»

Preferir una comparación que aporte algo a las dos curvas, sin atribuir causalidad. Etapas por kilómetro solo es válido si las medidas provienen de registros compatibles; no dividir medias o medianas de muestras distintas como si fuera un indicador por pozo.

### Cohortes

«A los {edad} meses, la cohorte {cohorte_a} produjo {porcentaje}% {más_o_menos} por pozo que la cohorte {cohorte_b}.»

Verificar que la métrica sea efectivamente por pozo y si representa producción del mes o acumulada. Comparar a igual edad, con cobertura suficiente y sin extrapolar cohortes recientes. Si la fuente no sostiene esa comparación, elegir otra verificable.

### Economía

«{Variable} registró su mayor {aumento_o_caída} del período en {fecha}: {variación} respecto de {base}.»

Calcular el hito y aclarar unidad, moneda y ajuste por inflación cuando corresponda. No inventar empleo, ingresos, exportaciones o efectos económicos si no forman parte de los datos disponibles.

## 4. Reglas de cálculo y selección

Crear un pequeño catálogo de hallazgos por capítulo, con prioridad editorial y condiciones de validez. Cada hallazgo debe tener identificador, fuente, cálculo, campos requeridos, cobertura y plantilla de texto.

- Utilizar el mismo estado compartido y los mismos datos que el gráfico superior derecho.
- Una diferencia entre porcentajes se expresa en puntos porcentuales; una variación relativa requiere su denominador correcto.
- Comprobar ceros, faltantes, años incompletos, unidades y tamaños de muestra antes de redactar.
- No convertir una correlación en explicación causal.
- No llamar récord histórico a un máximo de una ventana filtrada. Precisar «del período seleccionado» cuando ese sea el alcance.
- Cuando un hallazgo requiera comparar con un año fuera del período activo, indicar explícitamente ese contexto y no mezclar poblaciones distintas.
- Mantener redondeos consistentes con el gráfico y evitar aparentar precisión superior a la fuente.
- No seleccionar hallazgos de forma aleatoria ni hacer rotar mensajes mientras el usuario los está leyendo.
- Si varios cumplen las condiciones, elegir el que mejor complemente la información ya destacada en el gráfico.

No es necesario usar un modelo generativo en tiempo real. Los cálculos y las plantillas verificadas permiten mensajes reproducibles y reducen el riesgo de inventar datos.

## 5. Filtros, tiempo y ausencia de datos

Actualizar el mensaje cuando cambia capítulo, período, territorio o cualquier filtro que afecte su cálculo. La escala visual del mapa por sí sola no debe modificar el universo analítico salvo que exista un filtro espacial explícito.

Durante el arrastre de la timeline, actualizar de forma controlada al estabilizar la selección. No mantener un mensaje anterior con apariencia de vigencia mientras llegan otros datos.

Si no hay un hallazgo adicional válido:

1. Intentar otro hallazgo del mismo capítulo y conjunto filtrado.
2. Si tampoco existe, plegar el globo sin inventar una curiosidad ni volver a una frase genérica.
3. Si el usuario abre el guía en ese estado, mostrar un mensaje breve y honesto sobre la falta de datos comparables.

Las curiosidades externas sobre petróleo solo se incorporan si son relevantes al capítulo, están verificadas y tienen fuente identificada. No usarlas como relleno permanente para sustituir el análisis disponible.

## 6. Presentación

- Sustituir «GUÍA EDITORIAL» por un encabezado discreto como «Un dato más», o prescindir de encabezado si resulta redundante.
- Mantener el globo compacto: aproximadamente 20–40 palabras; una idea por mensaje.
- Destacar visualmente la cifra o comparación principal, sin colorear todo el párrafo.
- Permitir consultar la fuente y la base de comparación mediante un detalle pequeño, sin llenar el globo de metodología.
- Conservar el dinosaurio abajo a la izquierda o en el espacio libre ya resuelto; no moverlo otra vez al panel superior.
- Mantener ocultar/mostrar y movimiento reducido. No añadir voz automática.

## 7. Validación y entrega

Para cada capítulo, entregar al menos un mensaje final **con sus valores reales calculados**, acompañado en el informe de fuente, fórmula y selección utilizada. Si el capítulo no dispone de datos suficientes, documentarlo; las plantillas solas no constituyen una implementación terminada.

Verificar:

- El mensaje aporta información distinta del título, KPI y anotación principal del gráfico.
- Toda cifra coincide con un cálculo independiente sobre la fuente.
- Los cambios de filtros y tiempo producen mensajes consistentes.
- No hay divisiones por cero, períodos incompatibles ni afirmaciones de récord injustificadas.
- En Cohortes, se comparan edades y métricas equivalentes.
- No aparecen frases genéricas como «compará porcentajes y volúmenes», títulos repetidos ni campos entre llaves.
- Sin datos suficientes, el globo se pliega o informa la limitación cuando se lo abre.

Adjuntar capturas reales del gráfico y del dinosaurio juntos, para evaluar que se complementan, y ejemplos antes/después de aplicar un filtro. Esta iteración cambia el contenido editorial, no requiere rediseñar el mapa ni los iconos.
