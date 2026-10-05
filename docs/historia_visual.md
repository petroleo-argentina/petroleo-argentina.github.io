# Storyboard y Guion de la Historia Visual: Atlas Petróleo en Argentina

**Título:** Petróleo en Argentina: Del pozo al país  
**Subtítulo:** 75 años de producción para entender cómo cambió el mapa energético nacional.  
**Enfoque de diseño:** Atlas cartográfico interactivo / Periodismo visual y scrollytelling documental sobrio (sin formato SaaS ni dashboard corporativo).  
**Motor Cartográfico:** MapLibre GL JS v4.7.1 con terreno 3D Raster-DEM Terrarium AWS (exageración 1.22), Hillshade analítico a 315° y cámara con pitch/bearing adaptativo por capítulo.  
**Trazabilidad:** [`docs/revision_analitica.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/revision_analitica.md) | [`DESIGN.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/DESIGN.md) | [`docs/cartografia_v3.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/cartografia_v3.md) | [`docs/auditoria_geometrias.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/auditoria_geometrias.md)

---

## Portada Inicial (Home Splash)
- **Visual:** Lienzo completo a pantalla completa con mapa de relieve cenital de Argentina.
- **Titular:** `PETRÓLEO EN ARGENTINA` / `Del pozo al país` (sin kickers artificiales como 'Atlas Geográfico & Crónica de Datos').
- **Bajada:** `75 años de producción para entender cómo cambió el mapa petrolero argentino.`
- **Interacción:** Botón sutil `Comenzar el recorrido` que desliza la cámara suavemente hacia la vista nacional del Capítulo 01.

---

## Capítulo 01 — 01   ARGENTINA · 1950—2025
- **Pregunta:** *¿Cómo evolucionó la producción histórica de petróleo en Argentina?*
- **Cámara:** Center `[-65.0, -38.5]`, Zoom `4.2`, Pitch `4°`, Bearing `0°`.
- **Mensaje:** Tras la prolongada caída que siguió al pico histórico de 1998 (49.147,7 miles de m³), la producción nacional revirtió su declino a partir de 2017 y alcanzó en 2025 su mayor nivel en 26 años con 46.438,5 miles de m³ (~798.500 barriles/día, +12,8% vs 2024), traccionada por el despegue no convencional de Vaca Muerta.
- **Cifras auditadas:**
  - Producción 2025: **46.438,5 miles de m³** (+12,8% vs 2024; +63,9% acumulado vs 2017).
  - Pico histórico oficial (1998): **49.147,7 miles de m³** (~846.930 barriles/día).
- **Visual:** Serie temporal histórica nacional continua (1950–2025) con panel flotante reactivo translúcido en reposo (`rgba(13, 16, 21, 0.68)`) y oscurecido al interactuar (`rgba(13, 16, 21, 0.94)`). Marcadores editoriales en 1998, 2017 y 2025.

---

## Capítulo 02 — EL MAPA SE MUEVE
- **Pregunta:** *¿Dónde ocurrió la recuperación del crudo?*
- **Mensaje:** El crecimiento no fue uniforme en todo el país. Mientras cuencas tradicionales maduras mantuvieron su curva de declino natural, la Cuenca Neuquina concentró casi la totalidad del volumen incremental.
- **Cifras auditadas:**
  - 2010: Golfo San Jorge lideraba con 32,4%; Neuquén aportaba el 20,4%.
  - 2025: Neuquén genera el **64,68% del petróleo del país** (30.036,7 miles m³).
- **Visual:** Mapa interactivo de cuencas sedimentarias y pozos activos con control cronológico (2006, 2010, 2015, 2020, 2025).

---

## Capítulo 03 — EL PUNTO DE QUIEBRE
- **Pregunta:** *¿Cuándo el petróleo no convencional pasó a ser la fuente mayoritaria del país?*
- **Hito auditado:** **Noviembre de 2023** (51,11% no convencional). Se eliminó la referencia errónea a junio de 2023.
- **Cifras auditadas:**
  - Junio 2023: No convencional 47,09% / Convencional 52,91%.
  - Noviembre 2023: No convencional **51,11%** / Convencional 48,89% (Crossover definitivo).
  - 2025: No convencional **62,92%** (del cual 99,06% es Shale Vaca Muerta y 0,92% es Tight).
- **Visual:** Gráfico de dos series temporales mensuales con anotación en NOV-2023 y punto de cruce iluminado.

---

## Capítulo 04 — POCOS POZOS, MUCHO PETRÓLEO (Momento Pareto)
- **Pregunta:** *¿Cuántos pozos explican realmente la producción argentina?*
- **Mensaje central:** *La mitad del petróleo argentino provino de apenas el 3,48% de los pozos activos en 2025.*
- **Cifras auditadas (sobre 26.219 pozos activos con petróleo):**
  - **912 pozos** (3,48% del total) explican el **50% de la producción nacional**.
  - **2.021 pozos** (7,71% del total) explican **2/3 de la producción (66,7%)**.
  - **3.405 pozos** (12,99% del total) explican el **75% de la producción**.
  - **3.564 pozos no convencionales** (13,1% del total de pozos) generan el **62,9% del volumen total**.
- **Visual:** Big Number tipográfico limpio en Newsreader (`912 pozos = 50% de la producción`) y mapa donde se atenúan los miles de pozos marginales y resalta el núcleo hiper-productivo de Vaca Muerta.

---

## Capítulo 05 — CÓMO CAMBIÓ EL POZO
- **Pregunta:** *¿Qué cambió físicamente en la ingeniería de perforación?*
- **Fórmula de diseño:** Título corto + un hallazgo breve ("El crecimiento provino de multiplicar la escala del pozo: ramas laterales de más de 3.000 metros...") + mapa oblicuo en 3D (pitch 55°, bearing -20°) + dos gráficos apilados y sincronizados verticalmente en el panel flotante (`OverlayPanel`) + filtros (`GlobalFilterBar`).
- **Mensaje:** La productividad no creció por perforar más pozos, sino por una transformación radical en el diseño del pozo: ramas horizontales extensas y fracturación masiva de alta intensidad.
- **Cifras auditadas (Adjunto IV):**
  - Longitud horizontal: de 69,7 m (2014) y ~1.084 m (2018) a **mediana de 2.999 m (media 3.036 m)** en 2025.
  - Etapas de fractura: de 5,3 etapas (2014) a **mediana de 50 etapas (media 51,2)** en 2025.
  - Arena total bombeada: de 769 tn a **11.655 tn promedio por pozo**.
- **Visualización Obligatoria:** **Dos gráficos apilados y sincronizados verticalmente** (`stacked-charts-box`) compartiendo la misma escala cronológica horizontal (2016–2025). Gráfico superior: Longitud horizontal navegada en metros (1.000m – 3.400m); Gráfico inferior: Etapas de fractura (0 – 60 etapas). Queda terminantemente prohibido el uso de gráficos con doble eje Y superpuesto.


---

## Capítulo 06 — GENERACIONES DE POZOS
- **Pregunta:** *¿Un pozo nuevo produce igual que uno perforado hace diez años?*
- **Mensaje:** El aprendizaje operativo permitió que cada nueva cohorte de pozos comience su vida productiva con caudales iniciales y acumulados drásticamente superiores.
- **Cifras auditadas (Acumulado a 12 meses de vida):**
  - Cohorte 2015: 2.297 m³ (mediana).
  - Cohorte 2018: 2.405 m³ (mediana).
  - Cohorte 2021: 30.456 m³ (mediana).
  - Cohorte 2024: **33.427 m³ (mediana)**.
- **Visual:** Curvas de declino por cohorte con meses relativos (M1 a M24) mapeando mediana y percentiles.

---

## Capítulo 07 — DEL POZO AL PAÍS (Cierre del Recorrido)
- **Pregunta:** *¿Qué cambios macroeconómicos y territoriales acompañaron la expansión?*
- **Regla metodológica:** Correlación temporal estricta sin afirmaciones de causalidad indemostrables ("coincidió temporalmente con", "evolucionó junto con").
- **Cifras auditadas:**
  - Empleo privado registrado en hidrocarburos en Neuquén: expansión sostenida junto con la actividad de subsuelo (+83% en la última década).
  - Balanza comercial externa de combustibles: de una década deficitaria neta a saldo comercial positivo exportador (+USD 5.480M).
- **Visual:** Micro-gráfico de balanza exportadora/importadora y trazado de oleoductos de evacuación (Oldelval, Vaca Muerta Sur, Otasa).
- **Cierre del Relato:** En este capítulo finaliza el recorrido guiado. El botón de navegación ofrece la acción `volver al inicio ↺` para reiniciar la exploración sin callejones sin salida.

