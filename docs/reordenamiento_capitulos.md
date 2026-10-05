# Reordenamiento Narrativo de Capítulos — Petróleo en Argentina

**Fecha de implementación:** Octubre 2026  
**Referencia:** [`reordenamiento_y_redisenio_petroleo_argentina.md`](file:///c:/Users/ESCRITORIO/Downloads/reordenamiento_y_redisenio_petroleo_argentina.md)  
**Trazabilidad analítica:** [`docs/revision_analitica.md`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/docs/revision_analitica.md) | [`analysis/exports/`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/analysis/exports/)

---

## Estructura Consolidada de 8 Capítulos

```text
01 — EL REGRESO
02 — EL MAPA SE MUEVE
03 — EL PUNTO DE QUIEBRE
04 — POCOS POZOS, MUCHO PETRÓLEO
05 — CÓMO CAMBIÓ EL POZO
06 — GENERACIONES DE POZOS
07 — DEL POZO AL PAÍS
08 — UN NUEVO MAPA PETROLERO
```

---

### Capítulo 01 — EL REGRESO
- **Pregunta:** *¿Cómo volvió Argentina a niveles récord de producción de petróleo?*
- **Objetivo:** Dar perspectiva histórica de largo plazo (1950-2025) antes de entrar en Vaca Muerta.
- **Visual principal:** Serie histórica nacional continua de 75 años con hitos clave (Pico 1998, Mínimo 2017 y Récord 2025).
- **Cifras auditadas:**
  - Producción 2025: **46.438,5 miles de m³** (~798.450 bpd).
  - Crecimiento desde 2017: **+63,9%** (+18.107,7 miles m³ adicionales).
- **Mensaje narrativo:** Tras casi dos décadas de declinación ininterrumpida desde el récord de 1998, la curva nacional no solo revirtió su tendencia sino que quebró su máximo histórico.
- **Fuente:** Secretaría de Energía (Serie histórica 1950-2015 + Capítulo IV Res. 319/93 para 2006-2025).

---

### Capítulo 02 — EL MAPA SE MUEVE
- **Pregunta:** *¿Dónde ocurrió la recuperación territorial del crudo?*
- **Objetivo:** Demostrar que el crecimiento no fue homogéneo y evidenció una migración geográfica drástica.
- **Visual principal:** Cartografía temporal de cuencas y pozos con selector cronológico (2006, 2010, 2015, 2020, 2025) y aproximación de cámara desde el mapa nacional hacia la Cuenca Neuquina.
- **Cifras auditadas:**
  - En 2010: Golfo San Jorge lideraba con 32,4% de la producción y Neuquén aportaba el 20,4%.
  - En 2025: Neuquén concentra el **64,68% del petróleo argentino**, mientras las cuencas maduras pierden peso relativo.
- **Mensaje narrativo:** El mapa energético se desplazó: el centro de gravedad del petróleo se concentró en la Cuenca Neuquina mientras las cuencas del Golfo San Jorge, Cuyana y Austral mantuvieron un régimen maduro.

---

### Capítulo 03 — EL PUNTO DE QUIEBRE
- **Pregunta:** *¿Cuándo el petróleo no convencional pasó a ser la fuente mayoritaria del país?*
- **Objetivo:** Determinar con rigor empírico el momento del cruce estructural (*crossover*).
- **Corrección obligatoria auditada:**
  - Se eliminó la referencia errónea a "Junio 2023" (en junio 2023 el no convencional fue 47,09%).
  - **Hito oficial confirmado:** **Noviembre de 2023** (primer mes donde el no convencional alcanzó el **51,11%**).
  - En 2025, el no convencional alcanzó el **62,92%** nacional (29.217,8 miles m³), del cual el **99,06% es Shale Vaca Muerta** y el 0,92% es Tight.
- **Visual principal:** Serie mensual sincronizada de crudo convencional vs no convencional con punto de quiebre en NOV-2023.
- **Gráfico corregido:** `setupCrossoverMicroChart` consumiendo `pet_conv_miles_m3` y `pet_no_conv_miles_m3`.
- **Dataset exportado:** [`analysis/exports/crossover_monthly.csv`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/analysis/exports/crossover_monthly.csv).

---

### Capítulo 04 — POCOS POZOS, MUCHO PETRÓLEO (Momento Pareto)
- **Pregunta:** *¿Cuántos pozos explican realmente la producción petrolera de Argentina?*
- **Objetivo:** Revelar la extrema asimetría de productividad entre pozos tradicionales y no convencionales.
- **Universo analizado:** 26.219 pozos activos con producción de petróleo en 2025.
- **Hallazgos auditados:**
  - **Top 1% de pozos (262 pozos):** Produce el 22,86% del petróleo.
  - **Top 5% de pozos (1.311 pozos):** Produce el 58,22% del petróleo.
  - **Top 10% de pozos (2.622 pozos):** Produce el 70,98% del petróleo.
  - **Hito Central:** **Apenas 912 pozos (el 3,48% del total) explican el 50% de todo el petróleo del país**.
- **Visual principal:** Curva de Pareto y secuencia interactiva en mapa donde los miles de pozos marginales se atenúan y quedan encendidos los 912 pozos de alta productividad en Vaca Muerta.
- **Big Number tipográfico:** `912 pozos = 50% del crudo nacional (3,48% del parque activo)`.
- **Dataset exportado:** [`analysis/exports/pareto_2025.csv`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/analysis/exports/pareto_2025.csv).

---

### Capítulo 05 — CÓMO CAMBIÓ EL POZO
- **Pregunta:** *¿Qué cambió físicamente en la ingeniería de subsuelo y la estimulación?*
- **Objetivo:** Explicar la revolución tecnológica subterránea con métricas no distorsionadas por medias simples.
- **Hallazgos auditados (Adjunto IV):**
  - **Longitud horizontal:** Pasó de ~1.084 m en 2018 a una **mediana de 2.999 m (media 3.036 m)** en 2025, con ramas récord de hasta 4.000 m.
  - **Etapas de fractura:** De 5,3 etapas (2014) a una **mediana de 50 etapas (media 51,2)** en 2025.
  - **Arena bombeada:** De 769 tn a **11.655 tn promedio por pozo**.
- **Visual principal:** Distribución con bandas de dispersión P25-P75 y mediana anual, visualizando la geometría 3D de un pozo horizontal.
- **Dataset exportado:** [`analysis/exports/fracturas_anuales.csv`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/analysis/exports/fracturas_anuales.csv).

---

### Capítulo 06 — GENERACIONES DE POZOS
- **Pregunta:** *¿Un pozo perforado recientemente produce igual que uno de hace diez años?*
- **Objetivo:** Comparar la productividad normalizada por edad del pozo a lo largo de las distintas generaciones de completación.
- **Cohortes analizadas:** 2015, 2018, 2021, 2024.
- **Hallazgos auditados:**
  - Cohorte 2015 (mediana acum. 12 meses): 2.297 m³.
  - Cohorte 2018 (mediana acum. 12 meses): 2.404 m³.
  - Cohorte 2021 (mediana acum. 12 meses): 30.456 m³.
  - Cohorte 2024 (mediana acum. 12 meses): **33.427 m³** (multiplicación por 14 frente a 2015).
- **Gráfico corregido:** `setupCohortsMicroChart` consumiendo `d.cohorte` y `d.mediana_prod_m3`.
- **Dataset exportado:** [`analysis/exports/cohortes_productividad.csv`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/analysis/exports/cohortes_productividad.csv).

---

### Capítulo 07 — DEL POZO AL PAÍS
- **Pregunta:** *¿Qué cambios macroeconómicos y territoriales acompañaron la expansión?*
- **Objetivo:** Conectar el dato de subsuelo con empleo e inserción externa bajo estricta prudencia metodológica (correlación temporal, no causalidad directa indemostrable).
- **Variables auditadas:**
  - Empleo privado registrado en hidrocarburos en Neuquén (crecimiento sostenido).
  - Balanza comercial de combustibles: de déficit estructural a saldo superavitario exportador.
- **Gráfico corregido:** `setupMacroTradeMicroChart` consumiendo `d.year`, `d.fuel_exports_pct` y `d.fuel_imports_pct`.
- **Dataset:** `api/static_data/macro_employment_trends.json`.

---

### Capítulo 08 — UN NUEVO MAPA PETROLERO
- **Objetivo:** Síntesis conclusiva que reúne las 4 dimensiones clave demostradas por los datos:
  1. **Dónde:** Concentración geográfica en la Cuenca Neuquina (96% no convencional en Neuquén).
  2. **Cómo:** Perforación horizontal extrema (>3.000 m) y estimulación de alta densidad (50+ etapas).
  3. **Cuánto:** Asimetría Pareto extrema (912 pozos aportan el 50% de la producción nacional).
  4. **Qué lugar ocupa:** Superación del récord de 1998 con 46.438,5 miles de m³ y 62,9% no convencional.
- **Visual:** Lienzo cartográfico interactivo final con capas activas y modo de exploración libre.
