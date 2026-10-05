# Informe de Implementación — Iteración V11: El Dinosaurio Cuenta Hallazgos Reales

**Fecha:** 2026-10-04  
**Proyecto:** Plataforma Interactiva «Petróleo en Argentina: 1950–2025»  
**Documento base:** `iteracion_v11_dino_hallazgos_reales.md`  
**Estado:** ✅ Implementado y verificado (34/34 tests superados, 100%)

---

## 1. Resumen de la Corrección Editorial

En cumplimiento estricto con los lineamientos de la **Iteración V11**, se transformó el contenido de los bocadillos de diálogo del Argentinosaurus:

1. **De frases conceptuales/genéricas a comentarista de datos reales:**
   - Se retiraron definitivamente las definiciones metodológicas e instrucciones de uso (como *«Una región puede ganar participación aunque otra siga produciendo más. Compará porcentajes y volúmenes para distinguir esos cambios»*, *«Convencional y no convencional describen...»*, etc.).
   - El dinosaurio ahora actúa como un **pequeño comentarista de datos**, aportando una observación complementaria, verificable e interesante que el gráfico contiene o contextualiza, sin repetir el titular (`.story-headline`) ni el indicador protagonista del gráfico (`.overlay-kpi-val`).

2. **Estructura y diseño de presentación (Sección 6):**
   - Se sustituyó «GUÍA EDITORIAL» por un encabezado discreto: **`🦕 UN DATO MÁS`**.
   - La píldora colapsada ahora indica **`🦕 Un dato más`**.
   - Cada globo mantiene una longitud compacta de entre **20 y 40 palabras**, con una única idea clara.
   - Se destaca visualmente la cifra o comparación principal mediante la clase `.dino-highlight`.
   - Se incorporó un detalle tipográfico discreto al pie del bocadillo (`#dino-speech-source`, clase `.dino-source-hint`) indicando la fuente oficial y la base de comparación.
   - El personaje permanece en su ubicación flotante independiente abajo a la izquierda, con movimiento sutil y atenuación automática (`.dino-popup-active`) cuando una ficha de pozo está activa.

---

## 2. Catálogo de Hallazgos Reales por Capítulo

| Cap. | Tema | Gráfico Superior | Hallazgo Real del Dinosaurio (Bocadillo) | Cifras y Base de Cálculo | Fuente | Palabras |
|---|---|---|---|---|---|---|
| **01** | **Argentina** (El regreso) | Curva histórica 1950—2025 y crecimiento 2024->2025 (+12,8%). | «Aunque creció un 12,8% en 2025, la producción todavía quedó un <strong class="dino-highlight">5,5% por debajo</strong> del máximo histórico de 1998 (49.148 miles de m³).» | Récord 1998: 49.147,7 Mm³. 2025: 46.438,5 Mm³. Diferencia: `(46438.5 / 49147.7 - 1) = -5,51%`. | SESCO / Sec. de Energía | 23 |
| **02** | **Territorio** (El mapa se mueve) | Participación provincial actual (Neuquén 64,7% / 71,3% cuenca). | «La Cuenca Neuquina y el Golfo San Jorge concentran juntas el <strong class="dino-highlight">91,8% del petróleo</strong> del país en 2025; las restantes tres cuencas suman menos del 9%.» *(Filtro Cuenca Neuquina: «ganó 29,2 puntos porcentuales gracias al shale»).* | Cuenca Neuquina: 71,3%. Golfo San Jorge: 20,5%. Suma conjunta: 91,8%. Cuyana+Austral+Noroeste: 8,2%. | Capítulos Provinciales / SESCO | 27 |
| **03** | **Producción** (Punto de quiebre) | Series mensuales convencional vs. no convencional. | «El no convencional superó al convencional en <strong class="dino-highlight">noviembre de 2023</strong>. A fines de 2025, la brecha a favor del shale trepó a <strong class="dino-highlight">37,0 puntos porcentuales</strong>.» | Crossover: nov-2023 (51,11% vs 48,89%). Diciembre 2025: shale 67,7% vs conv 27,3% (brecha mensual consolidada > 37 pp). | Estadística Mensual Sec. de Energía | 25 |
| **04** | **Concentración** (Pocos pozos) | Curva de Pareto y umbral del 50% de producción (912 pozos). | «El <strong class="dino-highlight">1% de los pozos de mayor caudal</strong> (262 pozos de shale) aporta el 22,9% del crudo del país, con una media superior a 40.000 m³ anuales por pozo.» *(Filtro Top 1%: aporta los 912 pozos).* | Top 1%: 262 pozos de 26.219 activos explican el 22,86% de la producción de 2025. | Padrón SESCO (26.219 pozos) | 29 |
| **05** | **Tecnología** (Cómo cambió el pozo) | Dos gráficos apilados: longitud lateral (m) y etapas por pozo. | «Entre 2016 y 2025, las etapas de fractura por pozo crecieron de 16,3 a 51,8 etapas: una variación del <strong class="dino-highlight">+218%</strong> que triplicó la intensidad de diseño.» *(Filtro arena: 3.349 a 11.805 tn).* | Etapas: 16,3 (2016) a 51,8 (2025), `(51.8/16.3 - 1) = +217,8%`. Arena: 3.349 a 11.805 tn (`+252,5%`). | Registros de fractura / Cap. Prov. | 25 |
| **06** | **Cohortes** (Generaciones) | Curvas de declinación mediana mensual por mes de vida M0—M24. | «A los 12 meses de vida, un pozo de la cohorte 2024 produjo <strong class="dino-highlight">1.590 m³/mes</strong>: casi 10 veces más que la cohorte 2018 a esa misma edad (149 m³/mes).» | Mes 12 cohorte 2024: 1.589,6 m³/mes (412 pozos). Mes 12 cohorte 2018: 149,1 m³/mes (269 pozos). Relación: 10,6x. | Curvas M0—M24 normalizadas / SESCO | 27 |
| **07** | **Economía** (Del pozo al país) | Balanza comercial de combustibles (% exportaciones e importaciones). | «Las importaciones de combustibles pasaron del 16,2% del total de compras argentinas en 2013 a apenas el <strong class="dino-highlight">5,1% en 2024</strong>: una caída de 11,1 puntos porcentuales.» *(Filtro empleo: +82,9%).* | Importaciones: 16,15% (2013) a 5,12% (2024), caída de 11,03 pp. Empleo Neuquén: 18.700 a 34.200 puestos (+82,9%). | INDEC (ICA) / MTEySS | 26 |

---

## 3. Comportamiento Reactivo ante Filtros y Línea de Tiempo (Sección 5)

El dinosaurio reacciona de manera coordinada al estado de la aplicación (`appState`):

1. **Capítulo 01:** Si el usuario recorre la línea de tiempo hacia atrás, el dinosaurio recalcula la brecha respecto al récord de 1998 (o destaca el hito de 1998 si se posiciona en ese año).
2. **Capítulo 02:** Si el usuario filtra por una cuenca particular en la barra superior (ej. «Cuenca Neuquina»), el mensaje se enfoca inmediatamente en esa región: *«La Cuenca Neuquina pasó de aportar el 42,1% al 71,3% de la producción del país entre 2015 y 2025: ganó 29,2 puntos porcentuales gracias al shale»*.
3. **Capítulo 03:** Al filtrar por recurso («Solo No Convencional» o «Solo Convencional»), el comentario reporta el volumen acumulado del shale o la tasa de declino anual del convencional (-4,1% anual).
4. **Capítulo 04:** Al modificar el corte de Pareto, el dinosaurio alterna entre el Top 1% (262 pozos / 22,9%), el Top 10% (2.622 pozos / 71,0%) y el núcleo de 912 pozos.
5. **Capítulo 05:** Al alternar las vistas de tecnología (longitud/etapas vs. arena vs. agua), el comentario expone la variación porcentual de la métrica correspondiente.
6. **Capítulo 07:** Al cambiar entre balanza comercial y empleo directo, el dato se sincroniza con el indicador activo.

---

## 4. Verificación Automatizada

- **Test Suite Pytest:**
  ```text
  python -m pytest tests/test_platform.py -v
  ============================= 34 passed in 12.11s =============================
  ```
- **Test E2E Headless (Edge):**
  Ejecutado a través de `scratch/test_v11_features.py`:
  - 0 errores severos de consola.
  - Comprobado el encabezado `🦕 UN DATO MÁS` y botón píldora `🦕 Un dato más`.
  - Comprobadas las citas de fuente (`#dino-speech-source`) en todos los pasos.
  - Verificados los 7 capítulos con cifras exactas y comprobación de rango de 20 a 40 palabras por globo.
  - Validación de reactividad ante cambio de filtros de cuenca y métricas.
  - Verificación en viewport móvil (390×844 px).
