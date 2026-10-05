# Informe de Implementación — Iteración V12: Períodos, Modos y Argentina en el Mundo

**Fecha:** 2026-10-04  
**Proyecto:** Plataforma Cartográfica y Crónica de Datos «Petróleo en Argentina: 1950–2025»  
**Documento base:** `iteracion_v12_periodos_modos_argentina_mundo.md`  
**Estado:** ✅ Implementado, verificado visualmente y auditado (35/35 tests superados, 100%)

---

## 1. Resumen Ejecutivo de la Iteración V12

La Iteración V12 aborda tres dimensiones críticas para elevar la solidez analítica y la experiencia interactiva de la plataforma antes de su publicación en GitHub:

1. **Corrección del filtro de período en el Capítulo 01 (`timeRange`):**
   - Se erradicó el bug de coerción de tipos donde `'2017'` y `'2000'` se convertían a valores numéricos en `updateFilterBar`, impidiendo que la serie temporal se recortara en `renderChart` debido a comparaciones de igualdad estricta (`=== '2017'`).
   - Ahora, al seleccionar un período, la serie histórica, los ticks del slider y los textos dinámicos responden con precisión matemática.

2. **Diferenciación funcional real entre los modos `Relato` y `Explorar`:**
   - Se incorporaron subtítulos descriptivos y atributos de accesibilidad (`title` y `aria-label`):
     - **Relato:** «Vista preparada de cada capítulo»
     - **Explorar:** «Elegí filtros y períodos»
   - Cambiar cualquier filtro o deslizar la línea de tiempo conmuta automáticamente al modo `Explorar`, preservando la posición actual de cámara (`keepCamera: true`).
   - Presionar **`Relato`** o el botón **`Restablecer vista`** restaura la configuración original curada del capítulo (`CHAPTER_DEFAULTS`), su año inicial y devuelve la cámara cartográfica a su ángulo y encuadre editorial.

3. **Incorporación sustantiva del Capítulo 08: «Argentina en el mundo»:**
   - La plataforma pasa de 7 a **8 capítulos completos** (`01` al `08`), actualizando la guía visual vertical derecha con 8 nodos de trayectoria cartográfica.
   - Sustentado en la serie primaria internacional oficial de la **U.S. Energy Information Administration (EIA) International Energy Statistics (2024)** para *Crude oil including lease condensate* (Producto 57, Actividad 1), garantizando una comparación homogénea entre 99 países sin mezclar biocombustibles ni gas licuado de petróleo (GLP).

---

## 2. Métricas y Datos Internacionales Verificados (EIA 2024)

| Indicador | Valor Oficial EIA (2024) | Contexto y Homogeneidad |
|---|---|---|
| **Definición de producto** | Crudo + Condensado de arrendamiento (Product 57) | Cobertura homogénea para 99 países productores |
| **Producción mundial total** | 81.958,2 kb/d (miles de barriles/día) | Promedio diario del último año calendario completo |
| **Producción Argentina 2024** | 700,8 kb/d | Equivalente a 41.152,2 miles de m³ anuales |
| **Puesto mundial Argentina** | **Puesto #22 global** | Entre 99 países productores de petróleo |
| **Participación global** | **0,86%** del crudo mundial | 700,8 / 81.958,2 kb/d |
| **Producción América Latina** | 8.790,8 kb/d | Total de países productores sudamericanos y centroamericanos |
| **Puesto regional Argentina** | **Puesto #5 en América Latina** | Detrás de Brasil (#1), México (#2), Venezuela (#3) y Colombia (#4) |
| **Participación regional** | **8,0%** del crudo latinoamericano | 700,8 / 8.790,8 kb/d |
| **Crecimiento Argentina (2017—2024)** | **+46,1%** (Índice Base 100 = 146,1) | De 479,7 kb/d en 2017 a 700,8 kb/d en 2024 |
| **Crecimiento Mundial (2017—2024)** | **+0,9%** (Índice Base 100 = 100,9) | De 81.258,2 kb/d en 2017 a 81.958,2 kb/d en 2024 |

### Ranking Top 10 Mundial + Argentina (EIA 2024)
1. **Estados Unidos:** 13.266,8 kb/d (16,19%)
2. **Rusia:** 9.891,9 kb/d (12,07%)
3. **Arabia Saudita:** 9.208,7 kb/d (11,24%)
4. **Canadá:** 4.776,4 kb/d (5,83%)
5. **Irak:** 4.458,7 kb/d (5,44%)
6. **China:** 4.234,0 kb/d (5,17%)
7. **Irán:** 3.946,5 kb/d (4,82%)
8. **Emiratos Árabes Unidos:** 3.674,9 kb/d (4,48%)
9. **Brasil:** 3.356,5 kb/d (4,10%) — *#1 en América Latina*
10. **Kuwait:** 2.508,4 kb/d (3,06%)
...
22. **★ Argentina:** 700,8 kb/d (0,86%) — *#5 en América Latina*

### Ranking Principales Productores de América Latina (EIA 2024)
1. **Brasil:** 3.356,5 kb/d (38,18%)
2. **México:** 1.841,8 kb/d (20,95%)
3. **Venezuela:** 863,5 kb/d (9,82%)
4. **Colombia:** 772,7 kb/d (8,79%)
5. **★ Argentina:** 700,8 kb/d (7,97%)
6. **Guyana:** 617,3 kb/d (7,02%)
7. **Ecuador:** 475,3 kb/d (5,41%)
8. **Trinidad y Tobago:** 51,9 kb/d (0,59%)
9. **Perú:** 41,5 kb/d (0,47%)

---

## 3. Implementación Técnica y Componentes

### 3.1. Corrección del Bug de Coerción de Tipos (`frontend/app.js`)
- En `updateFilterBar`, se aisló el parsing de tipos: únicamente `f.field === 'paretoCutoff'` se convierte en número. Todos los selectores de período (`timeRange`), cuenca, recurso, métricas y ámbitos geográficos se preservan estrictamente como `String`.
- Si el usuario conmuta a `2017`, el valor del slider temporal se limita dinámicamente (`appState.year < 2017 -> 2017`). Si conmuta a `2000`, se limita a `2000`.
- El gráfico `overlay-micro-chart` segmenta la serie a los años seleccionados (1950–2025, 2000–2025 o 2017–2025), ajustando las escalas y la línea de tiempo inferior en concordancia.

### 3.2. Centralización de Estados por Defecto (`CHAPTER_DEFAULTS`)
- Se implementó un diccionario unificado `CHAPTER_DEFAULTS` que agrupa el estado canónico de los 8 capítulos.
- Al hacer clic en el botón `Relato` o en `Restablecer vista`, se invocan estos valores predeterminados y se restituye la cámara orbital del capítulo.

### 3.3. Gráfico y KPIs del Capítulo 08
- **Vista Ranking (Barras horizontales):** Muestra el Top 10 mundial + Argentina destacada en color ámbar/dorado (`#E3B55A`), o los países de América Latina cuando el filtro de ámbito se coloca en `latam`.
- **Vista Evolución (Líneas Base 100):** Muestra la aceleración de Argentina (+46,1%, Índice 146,1) en contraste con el estancamiento mundial (+0,9%, Índice 100,9) entre 2017 y 2024.
- **Cartografía Global y Callouts:** Posiciona la cámara en `center: [15.0, 20.0]`, `zoom: 1.5`, renderizando marcadores editoriales dinámicos para los polos globales o las capitales petroleras latinoamericanas.

### 3.4. Comentarios Dinámicos del Argentinosaurus
- **Capítulo 01:** Ofrece tres variantes de lectura según el período:
  - `all`: Destaca el récord histórico de 1998 y la brecha del 5,5% en 2025.
  - `2000`: Resume el declino del 33% hasta el piso de 2014 y la recuperación posterior.
  - `2017`: Subraya el salto vertical del +65,8% de la producción en el ciclo no convencional.
- **Capítulo 08:** Sintetiza los hitos verificados de la EIA:
  - Ranking global: Argentina #22 global con 700,8 kb/d (0,86% mundial).
  - Ranking regional: Argentina #5 en LatAm con 8,0% regional.
  - Evolución Base 100: Crecimiento comparado del +46,1% vs +0,9% global.

---

## 4. Auditoría de Calidad y Resultados de Testing

- **Ejecución completa de Pytest:**
  ```text
  python -m pytest tests/ -v
  ============================= 35 passed in 11.59s =============================
  ```
- **Tests nuevos y actualizados:**
  - `test_v6_seven_chapters_and_synthesis_removed`: Actualizado para verificar la estructura de 8 capítulos sustantivos (sin la síntesis vieja) y 8 nodos en el camino vertical.
  - `test_v12_periodos_modos_argentina_mundo`: Audita las descripciones y roles ARIA de modos, la consistencia de `CHAPTER_DEFAULTS`, la resolución de `timeRange`, la existencia de la serie EIA 2024 y los comentarios del dinosaurio.
- **Verificación visual con Selenium en Microsoft Edge Headless:**
  - `v12_ch01_periodo_todo.png`: Vista canónica del relato en 1950–2025.
  - `v12_ch01_periodo_2017_explorar.png`: Recorte temporal a 2017–2025, activación de modo Explorar y actualización del dinosaurio.
  - `v12_ch08_argentina_mundo_ranking.png`: Gráfico horizontal de ranking mundial con Argentina #22 y callouts globales.
  - `v12_ch08_argentina_mundo_evolucion.png`: Gráfico de evolución Base 100 (Argentina +46,1% vs Mundo +0,9%).
  - `v12_ch08_latam_ranking.png`: Ranking regional latinoamericano con Argentina #5 (8,0% regional) y callouts sudamericanos.
