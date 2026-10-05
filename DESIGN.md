# Sistema de Diseño Editorial: Atlas Petróleo en Argentina

**Referencia de inspiración metodológica:** Guía de sistemas de diseño de alta gama y visualización periodística (tipo FT Visual Journalism, NYT Graphics, Bloomberg Graphics).  
**Identidad:** Atlas interactivo de datos territoriales, cartografía editorial sobria y narrativa documental.  
**Evitar absolutamente:** Plantillas SaaS, tableros B2B corporativos, cards con border-radius excesivo, sombras pesadas, botones de píldora de colores estridentes, glow neón y paletas violeta/cyan tipo dashboard de IA.

---

## 1. Theme & Atmosphere (Atmósfera y Concepto)
- **Concepto:** Subsuelo, relieve geográfico real, fluido, ingeniería y memoria energética argentina.
- **Tono:** Editorial periodístico de alta gama, sobrio, preciso. La interfaz es un marco cartográfico y tipográfico que no compite con la información territorial.
- **Motor Cartográfico:** **MapLibre GL JS v4.7.1** con aceleración de hardware WebGL, terreno 3D basado en Raster-DEM (Terrarium AWS) y sombreado analítico Hillshade.

---

## 2. Color Roles (Paleta de Color y Relieve DEM)

### Paleta Cartográfica de Relieve y Superficie (Auditoría V3)
| Token | Valor Hex | Uso Cartográfico |
|---|---|---|
| `--terrain-water` | `#13212A` | Agua, ríos, lagos y cuerpos oceánicos |
| `--terrain-lowland` | `#262720` | Tierra baja, fondo base continental y valles |
| `--terrain-mid` | `#34352C` | Meseta patagónica y terreno medio |
| `--terrain-elevation` | `#504C40` | Elevación media, bardas y estribaciones |
| `--terrain-high` | `#706856` | Relieve alto y Cordillera de los Andes |
| `--border-provincial` | `rgba(235, 229, 207, 0.18)` | Límites provinciales |
| `--border-national` | `rgba(235, 229, 207, 0.30)` | Fronteras nacionales |
| `--road-primary` | `rgba(220, 211, 185, 0.13)` | Rutas troncales y conexiones |
| `--city-label` | `rgba(235, 231, 215, 0.58)` | Ciudades y toponimia principal |
| `--city-label-sec` | `rgba(235, 231, 215, 0.32)` | Toponimia y labels secundarios |

### Acentos Categóricos de Hidrocarburos
| Token | Valor Hex | Rol Semántico |
|---|---|---|
| `--accent-crude` | `#C98B32` | Crudo / Ámbar: Convencional maduro, serie histórica total |
| `--accent-shale` | `#39AFCF` | Vaca Muerta / Azul pizarra: No convencional, ramas 3D |
| `--accent-highlight` | `#E3B55A` | Oro cálido: Crossover Nov-2023, 912 pozos Pareto |
| `--accent-flora` | `#10B981` | Esmeralda sobrio: Oleoductos operativos (Oldelval, Otasa) |
| `--accent-subsoil` | `#C084FC` | Lavanda: Concesiones Vaca Muerta |
| `--accent-flare` | `#F43F5E` | Infrarrojo: Puntos térmicos satelitales VIIRS |

---

## 3. Typography (Jerarquías Tipográficas Evaluadas)

### Stack A (Editorial Clásico — Activo por defecto)
- **Titulares y Acentos Narrativos:** `Newsreader` (Google Fonts, serif editorial de alta gama).
- **Cuerpo y Narrativa de Lectura:** `Inter` (sans-serif sobria y neutral).
- **Cifras Técnicas y Ejes:** `JetBrains Mono` (monospaced técnico de alta precisión).

### Stack B (Moderno Geométrico / Técnico — Vía `data-font-theme="modern"`)
- **Titulares, Subtítulos y Cuerpo:** `Archivo` (sans-serif geométrica con gran peso visual).
- **Cifras Técnicas, Unidades y Metadatos:** `IBM Plex Mono` (monospace industrial y legible).

---

## 4. Layout & Composición Dinámica (Map-First)
- **Ancho del panel lateral:** Reducido a **320px** (dentro del rango meta de 300–330px), otorgando más del 75% del viewport a la cartografía interactiva.
- **Encabezados simplificados a una sola línea:**
  - `01   ARGENTINA · 1950—2025`
  - `02   TERRITORIO · 2006—2025`
  - `03   PRODUCCIÓN · NOV 2023`
  - `04   CONCENTRACIÓN · 2025`
  - `05   TECNOLOGÍA · 2015—2025`
  - `06   COHORTES · 2015—2024`
  - `07   ECONOMÍA · 2007—2025`
  - `08   ARGENTINA · SÍNTESIS`
- **Cámara progresiva con pitch y bearing:** Transición de vista cenital nacional (pitch 4°, bearing 0°) a perspectiva oblicua del subsuelo en Vaca Muerta (pitch 55°, bearing -20°).

---

## 5. Big Numbers (Cifras Destacadas)
- **Regla obligatoria:** Nunca colocar una cifra dentro de una caja con fondo, borde grueso o ícono decorativo.
- **Formato:** Cifra grande en `Newsreader` (`2.6rem`, color ámbar o marfil), con etiqueta superior monospaced en `JetBrains Mono` (`0.7rem`, tracking amplio) y leyenda inferior en `Inter` (`0.82rem`, color secundario).

```text
912
pozos explican la mitad de la producción nacional
(3,48% del parque de pozos activos en 2025)
```

---

## 6. Cartografía & Visores 2.5D
- **Mapa Base:** Esri World Dark Gray Canvas con relieve y elevación sutil. Libre de marcas de agua diagonales.
- **Alturas y Profundidades:** No abusar de columnas 3D extravagantes. Utilizar altura o radio proporcional a la producción exclusivamente en escenas de aproximación a Vaca Muerta para ilustrar la disparidad frente al pozo convencional.
- **Ductos e Infraestructura:** Trazas finas semitransparentes (1,5px de ancho) con halo atenuado.
- **Transiciones de Cámara:** Suaves, entre 800ms y 1.400ms (`ease-in-out`), sin saltos bruscos.

---

## 7. Gráficos (Chart.js Integrado)
- **Filosofía:** El gráfico debe sentirse tallado sobre el panel oscuro, sin marco ni recuadro contenedor.
- **Rejilla:** Líneas punteadas casi invisibles (`rgba(255, 255, 255, 0.04)`).
- **Tooltips:** Etiquetas directas minimalistas con tipografía `Inter` y fondo carbón sólido.
- **Sin leyendas redundantes:** Usar etiquetas directas sobre la línea o color en el texto explicativo.

---

## 8. Do / Don't (Reglas Terminantes)

### ❌ DON'T (Prohibido)
- No usar glassmorphism con resplandores neón (*neon glow*).
- No encerrar cada número o párrafo en una "card".
- No usar violeta, fucsia o cyan estridente.
- No colocar gauges, velocímetros o gráficos de torta/dona sin propósito.
- No citar palabras como "concurso", "hackathon" o "jurado".
- No bloquear el mapa con barras laterales de 600px.

### ✅ DO (Obligatorio)
- Mantener la sobriedad documental de un atlas geográfico de investigación.
- Priorizar el mapa y la relación territorial del dato.
- Explicar las fuentes primarias y limitaciones metodológicas en el botón accesible de Fuentes.
- Asegurar rendimiento fluido (>= 50 FPS) sin renderizar miles de nodos DOM superfluos.

---

## 9. Arquitectura V4 + V5: Overlays Flotantes, FilterBar y Timeline Global

### 9.1. Fórmula Editorial-Cartográfica
Cada capítulo aplica rigurosamente la secuencia:
**Título corto + un hallazgo breve cuando aporte valor + mapa + gráfico flotante + filtros**.
La columna lateral izquierda se preserva puramente sintética (`width: 320px`, plegable con `-`/`+`), dejando el 80% del mapa despejado.

### 9.2. Panel Flotante de Visualización (`#chart-overlay-panel`)
- **Ubicación:** Flotante en el cuadrante superior derecho (`top: 102px; right: 48px; width: 470px; max-width: calc(100vw - 420px)`), posicionado estratégicamente sobre el Atlántico/área libre de Argentina continental.
- **Acabado:** Fondo carbón translúcido (`rgba(19, 21, 23, 0.88)`), desenfoque de fondo (`backdrop-filter: blur(14px)`), borde micrométrico (`rgba(255, 255, 255, 0.08)`) y radio de curvatura uniforme (`8px`).
- **Plegado:** Botón minimalista de minimizado (`-`) con píldora flotante de restauración (`#btn-restore-overlay`).

### 9.3. Barra Superior de Filtros y Modos (`#global-filter-bar`)
- **Dual-Mode:** Selector articulado entre **Relato** (narrativa guiada con parámetros editoriales óptimos) y **Explorar** (control libre de filtros, unidades y agregaciones).
- **Controles Contextuales:** Chips de selección inyectados reactivamente según el capítulo activo (p.ej., unidad m³ vs bpd en Ch01, cuencas en Ch02, corte Pareto en Ch04, cohorte en Ch06).
- **Botón de Restablecer:** Permite regresar instantáneamente al estado editorial original del capítulo.

### 9.4. Regla Terminante para Capítulo 05: Dos Gráficos Apilados
- **Prohibición:** Se prohíben categóricamente los gráficos de doble eje Y superpuestos con escalas artificiales dispares.
- **Implementación:** Dos lienzos independientes sincronizados verticalmente en `.stacked-charts-box`:
  1. *Lienzo Superior (`#chart-canvas-length`):* Longitud lateral en metros (1.000m – 3.400m), color `--accent-shale` (`#39AFCF`). Eje X oculto para evitar redundancia.
  2. *Lienzo Inferior (`#chart-canvas-fractures`):* Etapas de fractura (0 – 60 etapas), color `--accent-crude` (`#C98B32`). Eje X visible con marcas anuales compartidas (2016–2025).
  3. *Sincronización Temporal:* Al posicionarse o reproducir un año, ambos gráficos resaltan simultáneamente el punto correspondiente en color oro cálido (`#E3B55A`).

### 9.5. Timeline Global Unificada (`#timeline-scrubber-bar`)
- La bandeja inferior de control temporal está anclada globalmente a nivel de sistema y comparte estado reactivo con todos los capítulos.
- Adapta dinámicamente sus límites (`min`, `max`, `step`, `ticks`) según la cobertura histórica real de cada capítulo (p.ej., 1950–2025 en Ch01; 2006–2025 en Ch02; 2016–2025 en Ch05; 2015–2024 en Ch06).

---

## 10. Iteración V6: Navegación Visible, Paneles Homogéneos y Filtros Claros

### 10.1. Franja Exclusiva para Recorrer la Historia (`#journey-tracker-nav`)
- **Espacio Reservado:** La columna vertical de puntos de navegación se posiciona en el borde derecho (`position: fixed; right: 18px; top: 50%; transform: translateY(-50%); z-index: 50;`), asegurando una franja exclusiva intocable e inaccesible para solapamientos.
- **Buffer de Seguridad:** El panel flotante del gráfico (`#chart-overlay-panel`) se retira hacia adentro a `right: 76px; width: 440px; max-width: calc(100vw - 420px); z-index: 40;`, dejando un corredor despejado de más de 50px.
- **Accesibilidad y Área de Clic:** Cada nodo `.journey-node` posee un área de interacción táctil/ratón expandida (`32px x 32px`) con `role="button"`, `tabindex="0"` y `aria-label="Capítulo XX: Título"`, activable con teclado (`Enter` / `Space`). El punto visible mide `10px` (en reposo) y `13px` con halo áureo (`#C98B32` / `#E3B55A`) en estado activo.
- **Tooltip de Capítulo:** La etiqueta identificatoria flota limpiamente hacia la izquierda del punto (`right: 36px`), formateada como badge oscuro de alto contraste que nunca intersecta el gráfico.

### 10.2. Sistema Unificado de Paneles (Estilo Base Idéntico)
Todos los componentes de superficie (`.story-column`, `.chart-overlay-panel`, `.global-filter-bar`, `.timeline-bar-inner`, cajones y modales) comparten estrictamente el mismo juego de tokens:
- **Fondo Neutro Común:** `--panel-bg: rgba(13, 16, 21, 0.92);` (se eliminan por completo los fondos pardos/oliva o tintes disonantes).
- **Sub-bloques Elevados:** `--panel-bg-elevated: rgba(22, 27, 36, 0.78);`
- **Bordes Finos Coherentes:** `--panel-border: 1px solid rgba(255, 255, 255, 0.08);`
- **Radio de Esquinas:** `--panel-radius: 8px;` y `--panel-radius-sm: 4px;`
- **Desenfoque y Sombra:** `--panel-backdrop: blur(18px) saturate(180%);` y `--panel-shadow: 0 20px 48px rgba(0, 0, 0, 0.65);`
- **Regla del Oro/Ámbar:** El dorado se reserva exclusivamente para los datos y series principales, las métricas destacadas y las selecciones activas. Nunca se tiñe el fondo general del panel.

### 10.3. Filtros Contextuales Claros con Etiquetas Explícitas
- **Estructura:** Cada control se encapsula en `.filter-field-group` compuesto por:
  1. `<label class="filter-field-label">`: Nombre breve y unívoco de la dimensión (p.ej., `Período`, `Cuenca`, `Recurso`, `Umbral Pareto`, `Ingeniería`, `Cohorte`, `Dimensión`).
  2. `<div class="filter-select-wrap">`: Contenedor estilizado con el desplegable `.filter-chip-select` y el glifo chevron `.filter-select-arrow` (`▾`).
- **Separación de Modos:** El selector de modo `Relato / Explorar` se encuentra estrictamente delimitado por el separador vertical `.filter-separator`.
- **Valores Completos:** En el Capítulo 01, la opción predeterminada declara con total fidelidad: `1950–2025 · Todo el período`.
- **Botón Restablecer Vista:** Identificado de forma fiel a su comportamiento integral: recupera el modo relato, el año por defecto, los filtros iniciales y la cámara cartográfica predefinida del capítulo.

### 10.4. Recorrido Narrativo en Siete Capítulos (Eliminación de Síntesis)
- Se eliminó el capítulo redundante `08 · Argentina · Síntesis`.
- El atlas culmina en el **Capítulo 07: Del pozo al país (Economía & Macro)**.
- Se actualizaron todos los contadores a 7 capítulos (`01` a `07`), el track SVG a 7 nodos y el modal de preguntas a 7 interrogantes.
- En el Capítulo 07, el botón de navegación hacia adelante cambia dinámicamente su rótulo a `volver al inicio ↺`, reiniciando el viaje sin callejones sin salida ni estados rotos.

---

## 11. Iteración V7: Mapa a Color, Paneles Reactivos y Rigor Editorial

### 11.1. Paneles de Gráficos Translúcidos Reactivos
- **Estado de Reposo:** El panel `#chart-overlay-panel` adopta `--panel-bg-translucent: rgba(13, 16, 21, 0.68)` con `backdrop-filter: blur(10px)`. Deja percibir la cartografía y el relieve montañoso del subsuelo sin perder legibilidad tipográfica.
- **Estado Activo (Hover / Foco):** Al pasar el cursor por cualquier parte del panel o recibir foco en un control interno (`:focus-within`), el fondo se oscurece suavemente (180ms) a `--panel-bg-opaque: rgba(13, 16, 21, 0.94)`.
- **Regla Estricta:** Solo se altera `background-color`, nunca la propiedad `opacity` del contenedor (para preservar la nitidez absoluta de textos, cifras, ejes y botones).
- **Dispositivos Táctiles:** `@media (hover: none)` mantiene una opacidad intermedia fija (`rgba(13, 16, 21, 0.88)`).

### 11.2. Cartografía Base con Color Natural y Relieve Armónico
- **Imágenes Satelitales ESRI World Imagery:** Base satelital continua de alta resolución sin rotulación en inglés incrustada.
- **Relieve 3D Suave:** DEM Terrarium integrado con sombreado de colinas atenuado (exageración de 0.32 y sombras en `#13212A` al 35%), preservando los azules marinos, verdes de la vegetación y tonos tierra de la meseta.

### 11.3. Toponimia Oficial: «ISLAS MALVINAS»
- Capa de símbolos exclusiva `islas-malvinas-label` en `[-59.5, -51.75]` con halo de contraste oscuro (`#0B0E13`, 2.5px), tipografía destacada y filtro de exclusión que erradica por completo la etiqueta en inglés ("Falkland Islands").

### 11.4. Rigor Editorial: Retiro de Falsos Récords y Unidades Inequívocas
- **Auditoría de Serie Histórica:** 1998 fue el verdadero pico histórico (49.147,7 miles de m³ / 846k bpd). 2025 (46.438,5 miles de m³) es el mayor nivel en 26 años y récord shale, pero no récord absoluto. Se retiró la etiqueta «(Récord)».
- **Variación Dinámica Interanual:** El KPI calcula en tiempo real la variación vs año anterior (`+12,8% vs 2024` para 2025; reactivo al año de la timeline).
- **Unidades Explícitas:** Sustitución de «Mm³» por «miles de m³» y «barriles/día» en panel, timeline, tooltips y ejes.

### 11.5. Header Simplificado y Control Compacto de Capas
- **Header Limpio:** Se retiraron «Preguntas», «Capas» y «Fuentes», manteniendo únicamente «Relato continuo».
- **Control de Capas en Filtros:** Se integró un selector contextual «Mostrar» dentro de `#filter-controls-container` para alternar la visibilidad de la capa operativa de cada capítulo sin alterar los cálculos analíticos.



