# Revisión de Lenguaje de Interfaz y Ajuste Editorial

## 1. Principio Rector
Eliminar todo tono explicativo, condescendiente o artificial típico de interfaces sintéticas generadas por IA. La visualización debe comunicar la idea directamente a través de jerarquía, escala, contrastes cromáticos y anotaciones geográficas directas.

Regla aplicada:
> *Si el texto explica cómo mirar el gráfico o usar el mapa &rarr; se elimina.*  
> *Si el texto aporta un hallazgo empírico auditado &rarr; se conserva y resalta.*

---

## 2. Textos Instructivos y Artificiales Erradicados

| Ubicación | Texto Eliminado (Estilo IA / Tutorial) | Reemplazo Editorial Aplicado |
| :--- | :--- | :--- |
| **Cabecera General** | `ATLAS GEOGRÁFICO & CRÓNICA DE DATOS` | **`Petróleo en Argentina / Del pozo al país`** (Kicker artificial suprimido por completo). |
| **Encabezado de Capítulos** | `01 / 08`<br>`REPÚBLICA ARGENTINA · PERSPECTIVA NACIONAL` | **`01   REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025`** (Formato wizard suprimido; numeración editorial de una línea). |
| **Capítulo 01** | `Qué observar en el mapa: Las 5 cuencas sedimentarias productivas del país. Observa cómo la Cuenca Neuquina...` | Eliminado. El gráfico de serie histórica (1950–2025) y los KPIs (46.438 Mm³, +63,9%) hablan directamente. |
| **Capítulo 02** | `Qué observar en el mapa: Utiliza el deslizador temporal inferior para observar la migración de pozos...` | Anotación geográfica directa en el mapa sobre Neuquén: `20,4% → 64,7%` de cuota nacional. |
| **Capítulo 03** | `Aclaración técnica auditada: En 2025, el 99,06% del petróleo no convencional proviene de Shale... En el mapa se aprecian...` | Destacado directo en tarjeta y gráfico del hito **`NOV 2023`** (51,11% no convencional) y cuota 62,9% en 2025. |
| **Capítulo 04** | `Qué observar en el mapa: Al ingresar a este capítulo se atenúan los miles de pozos marginales y quedan iluminados...` | Impacto directo de descubrimiento: bloque visual `26.219 → 912` pozos (3,48% de pozos = 50% del petróleo nacional). |
| **Capítulo 05** | `Qué observar en el mapa: Líneas cyan con las trayectorias horizontales 3D reales navegadas a 3.000 metros...` | Métricas de ingeniería directas: `3.036 m` longitud lateral y `51,2` etapas de fractura; cámara oblicua 3D a 56°. |
| **Capítulo 06** | `Regla metodológica: Se grafican medianas por edad relativa a partir de analysis/exports/...` | Curvas de declinación por cohortes que muestran el multiplicador de `14x` entre la cohorte 2015 y la cohorte 2024. |
| **Capítulo 07** | `Qué observar en el mapa: Trazas de oleoductos: verde para los ductos troncales operativos...` | Reemplazado por los datos clave: `+83%` empleo formal en Neuquén y superávit de `US$ 5.600M`. |
| **Navegación Inferior** | Botones cuadrados genéricos con flechas de formulario. | Enlaces mínimos de tipografía mono: `← anterior` y `siguiente →`. |

---

## 3. Rediseño del Recorrido Lateral Derecho (Journey Tracker)
- **Concepto:** En lugar de puntos aislados o un stepper de formulario de 8 pasos, se construyó un recorrido geográfico continuo con un camino SVG orgánico con variaciones laterales sutiles (`x: 14 &rarr; 25 &rarr; 13 &rarr; 24 &rarr; 27 &rarr; 13 &rarr; 23 &rarr; 16`).
- **Estados de los Nodos:**
  - *Inactivo:* Diámetro 9px, fondo `#12161A`, borde `rgba(235, 229, 207, 0.40)`.
  - *Visitado:* Fondo `rgba(201, 139, 50, 0.30)`, borde `rgba(201, 139, 50, 0.70)`.
  - *Activo:* Diámetro 13px, fondo `#D99A43`, borde `#E6BE78`, resalte sutil.
- **Progreso del Trazo:**
  - *Tramo recorrido:* `rgba(217, 154, 67, 0.70)`, grosor 2px, con animación progresiva `stroke-dashoffset`.
  - *Tramo pendiente:* `rgba(235, 229, 207, 0.12)`, grosor 1.5px.
- **Etiqueta Integrada:**
  - Número de capítulo en fuente mono (`01`, `02`, etc.) en tono ámbar `#C98B32`.
  - Título editorial en serif/sans marfil `#EDE8D8`. Sin pills ni cajas flotantes.
