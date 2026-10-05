# Auditoría Analítica y Contrato de Datos — V4 + V5 Unificada
**Proyecto:** Petróleo en Argentina — Del pozo al país  
**Fecha:** Octubre 2026  
**Documento base:** `docs/iteracion_v4_v5_unificada.md`

---

## 1. Matriz de Auditoría por Capítulo (Sección 2)

| Capítulo | Pregunta visual | Gráfico anterior (V3) | Datos y Cobertura | Métrica y Agregación | Mapa y Capas | Interacciones V4+V5 | Cambio Propuesto (V4+V5) |
|---|---|---|---|---|---|---|---|
| **01 · Argentina**<br>`1950—2025` | ¿Cómo evolucionó la producción nacional y cuándo se alcanzó el récord? | Línea en columna lateral estrecha (280px). Eje comprimido. | `timeline_1950_2025.json`<br>1950 a 2025 (76 años). Cobertura nacional. | `prod_pet_miles_m3` (miles m³) y `bpd`. Suma anual de producción. Sin faltantes. | Cuencas sedimentarias nacionales (fill + border). | Rango temporal (1950-2025, 2000-2025, 2017-2025), Selector de Unidad (`Mm³` vs `bpd`), timeline anual activa. | **Overlay flotante sobre el mapa (460px)** con línea amplia, marcadores de hito (1998, 2017, 2025). DynamicKPI: 46.438 Mm³ (+63,9% vs 2017). |
| **02 · Territorio**<br>`2006—2025` | ¿Cómo se desplazó geográficamente el centro de gravedad del crudo hacia Neuquén? | Barras horizontales estrechas fijas en sidebar (2010 vs 2025). | `wells_map_sample.json`, `geo_basins.json`. 2006 a 2025. | Cuota porcentual provincial y por cuenca (%) sobre producción nacional del año activo. | Cuencas + Pozos activos filtrados por año (`anio_primera_prod <= year`). | Filtro de Cuenca (Todas, Neuquina, Golfo San Jorge, etc.), Timeline 2006–2025. | **Overlay flotante con barras de participación ordenadas** que mutan con el año seleccionado. DynamicKPI reactivo al año activo: Neuquén % vs Golfo San Jorge %. |
| **03 · Producción**<br>`Nov 2023` | ¿Cuándo y cómo el no convencional superó al convencional (crossover)? | Línea mensual pequeña en sidebar (difícil distinguir el cruce exacto). | `conv_vs_noconv_monthly.json`<br>2015-01 a 2025-12 (132 meses). | `pet_conv_miles_m3`, `pet_no_conv_miles_m3`, share %. Mensual. | Pozos coloreados por recurso (Convencional ámbar `#C98B32`, No Convencional celeste `#39AFCF`). | Filtro de Recurso (Todos, No Conv, Convencional), Vista Volumen vs Share %, Timeline mensual/anual. | **Overlay con doble línea temporal y área sombreada**. Hito vertical destacado en **NOV-2023 (51,11%)**. Tooltip exacto por mes. |
| **04 · Concentración**<br>`2025` | ¿Cuántos pozos explican la mitad de la producción nacional (Pareto)? | Curva de Pareto estática confinada a sidebar. | `pareto_2025.csv`<br>26.219 pozos productores activos en 2025. | Acumulado ordenado descendente. Pozos acumulados (%) vs Producción acumulada (%). | Pozos en mapa con efecto foco: Top 912 pozos iluminados (`#E3B55A`), resto atenuados (`opacity 0.10`). | Selector de Umbral: Top 50% (912 pozos), Top 66,7% (2.021 pozos), Top 1% (262 pozos), Todos (26.219). | **Overlay con Curva de Lorenz / Pareto amplia**, umbral vertical del 50% interactivo. DynamicKPI: 912 pozos (3,48% del parque). |
| **05 · Tecnología**<br>`2015—2025` | ¿Cómo cambiaron la longitud de la rama lateral navegada y las etapas de fractura? | Gráfico combinado con ejes saturados en panel angosto. | `technical_fractures_trends.json`<br>2016 a 2025. 432 pozos muestreados en 2025. | `avg_longitud_horizontal_m` (metros) y `avg_etapas` (conteo). Medias anuales auditadas. | Trazas 3D de pozos horizontales en Añelo con inclinación pitch 55°, bearing -20°. | Métrica activa: Longitud & Etapas simultáneas, Arena (tn), Agua (m³). Timeline anual. | **PRIORIDAD ESPECIAL: Dos gráficos apilados y sincronizados verticalmente**. Superior: Longitud (m); Inferior: Etapas. Eje temporal común (2016–2025). |
| **06 · Cohortes**<br>`2015—2024` | ¿Cómo mejoró la curva de aprendizaje de caudal inicial mes a mes entre generaciones de pozos? | Curva de declino en sidebar con ejes poco legibles. | `cohorts_decay_curves.json`<br>Cohortes 2015, 2018, 2021, 2024. Meses de vida 0 a 24. | `mediana_prod_m3` acumulada por mes relativo de vida. Denominador: pozos con >= N meses de producción. | Concesiones + Pozos de la cohorte seleccionada. | Selector de Cohortes visibles (Todas, 2024 vs 2015, etc.). | **Overlay con curvas de declinación superpuestas sobre eje de edad del pozo (Mes 1 a 24)**. Anotación directa: Cohorte 2024 acumuló 33.427 m³ (14x vs 2015). |
| **07 · Economía**<br>`2007—2025` | ¿Qué correlación temporal existió entre producción, divisas energéticas y empleo en Neuquén? | Gráfico de barras/líneas en sidebar sin separación clara de magnitudes. | `macro_employment_trends.json`<br>2007 a 2024. | Empleo (puestos registrados) y Balanza (% de exportaciones e importaciones de mercaderías). | Oleoductos troncales + refinerías + puertos exportadores. | Selector de serie: Comercio exterior (% divisas) vs Empleo registrado Neuquén. | **Overlay con gráfico de balanza comercial (superávit US$ 5.600M en 2024) y empleo (+83%)**, con nota de correlación sin causalidad espuria. |
| **08 · Síntesis**<br>`Perspectiva` | ¿Cuáles son las 4 conclusiones estructurales de los 75 años de datos? | 4 bloques de texto apilados en sidebar. | Datasets consolidados 1950–2025. | Indicadores clave síntesis (64,7% Neuquén, 3.036m lateral, 912 pozos = 50%, récord 46.438 Mm³). | Vista nacional integral con todas las capas activables. | Navegación libre, toggle de capas, botón de reinicio de relato. | **Overlay de síntesis visual con 4 indicadores dinámicos interconectados** y acceso libre a capas territoriales. |

---

## 2. Contrato de Estado y Flujo Unidireccional (Sección 8)

```text
Usuario interactúa (Filtro / Timeline / Selector de Modo / Click en entidad)
                              │
                              ▼
                       `appState` único
       { chapter, mode, year, filters: {cuenca, recurso, ...}, selectedEntity }
                              │
                              ▼
                  `deriveDataForState(appState)`
                 (Filtrado y agregaciones consistentes)
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
MapLibre Canvas        OverlayPanel          Story Column
- Capas visibles       - ReactiveChart       - Título sintetizado
- Pitch/bearing        - Stacked charts 05   - Hallazgo conciso
- Filtro de pozos      - DynamicKPIs         - Controles ant/sig
- Highlight entidad    - Unidades y ejes
```

---

## 3. Reglas de Tratamiento de Faltantes y Normalización
1. **Ausencia vs Cero:** No se imputan ceros arbitrarios en series donde no hay registro oficial. Si una cohorte no alcanzó los 24 meses (e.g. Cohorte 2024 a mes 12), la línea se corta en su último mes observado real.
2. **Cálculo de Porcentajes:** Denominador explícito en cada cálculo (producción total del período o parque total de pozos activos).
3. **Escalas en Líneas:** Ejes verticales parten de cero en gráficos de barras. En series temporales de líneas con valores elevados, el recorte de escala se señaliza con corte visible y etiqueta clara.
