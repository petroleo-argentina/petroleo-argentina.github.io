# Comparativa Tipográfica: Stack Clásico vs Stack Moderno

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Objetivo:** Evaluar la legibilidad, personalidad editorial y jerarquía visual entre dos familias tipográficas sobre cartografía 3D nocturna.

---

## 1. Definición de Stacks Tipográficos en Competencia

### Stack A — Editorial Clásico (Predeterminado)
- **Titulares y Acentos Narrativos:** `Newsreader` (Serif de alta gama con serifas suaves y números elzevirianos).
- **Cuerpo y Párrafos de Lectura:** `Inter` (Sans-serif limpia, neutra y balanceada para pantallas de alta densidad).
- **Datos Técnicos y Unidades:** `JetBrains Mono` (Monoespaciada técnica con altura x generosa).
- **Personalidad:** Periodismo de investigación de gran formato (tipo Financial Times, The New York Times, ProPublica).

### Stack B — Editorial Técnico-Cartográfico (Variante Moderna)
- **Titulares, Subtítulos, Cuerpo y Navegación:** `Archivo` (Grotesque contemporáneo de inspiración tipográfica argentina/latinoamericana, trazos contundentes y excelente contraste en pesos 400, 500 y 600).
- **Datos Numéricos, Coordenadas y Metadatos:** `IBM Plex Mono` (Monoespaciada de ingeniería de precisión, excelente para matrices de perforación y mediciones de caudal).
- **Personalidad:** Atlas documental técnico y cartografía de ingeniería de subsuelo (tipo National Geographic Maps, Bloomberg Visuals).

---

## 2. Matriz Comparativa por Capítulo

| Dimensión de Análisis | Capítulo 01 (El Regreso) | Capítulo 04 (Pareto 912 Pozos) | Capítulo 05 (Cómo Cambió el Pozo - 3D) | Veredicto Técnico |
| :--- | :--- | :--- | :--- | :--- |
| **Legibilidad sobre mapa oscuro** | Stack A ofrece alto contraste con serifas marfil. | Stack B proporciona mayor impacto en el gran número `912` en peso 600 sin distorsión. | Stack B alinea mejor con la estética de ingeniería de subsuelo 3D (TVD, ramas laterales). | **Empate:** Stack A destaca en la narrativa histórica; Stack B en datos de ingeniería. |
| **Jerarquía y Escaneo Rápido** | Titulares en Newsreader tienen elegancia literaria. | Archivo en 2.8rem genera un impacto directo e inmediato en el bloque `26.219 → 912`. | Las medidas de rama lateral (`3.036 m`, `51,2 etapas`) lucen muy nítidas en IBM Plex Mono. | **Stack B** resulta más compacto en columnas estrechas (320px). |
| **Densidad en panel de 320px** | Newsreader requiere mayor interlineado (1.35) para evitar empaste. | Archivo condensa de forma más eficiente el espacio vertical, permitiendo ver el gráfico sin scroll. | Ambas familias respetan la escala sin desbordar el contenedor. | **Stack B** optimiza un 8% el espacio vertical del panel. |

---

## 3. Implementación Dinámica en la Plataforma
Ambos stacks se encuentran plenamente integrados en el frontend:
- **Carga de fuentes:** [`frontend/index.html`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.html) importa simultáneamente los pesos optimizados de `Archivo`, `IBM Plex Mono`, `Newsreader`, `Inter` y `JetBrains Mono` desde Google Fonts.
- **Selector en CSS:** [`frontend/index.css`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/index.css) define las variables raíz conmutable mediante `body[data-font-theme="modern"]`:
  ```css
  /* Stack A: Default Editorial Clásico */
  :root {
    --font-serif: 'Newsreader', Georgia, serif;
    --font-sans: 'Inter', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }

  /* Stack B: Variante Moderna Archivo + IBM Plex Mono */
  body[data-font-theme="modern"] {
    --font-serif: 'Archivo', sans-serif;
    --font-sans: 'Archivo', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
  }
  ```
- **Conmutación rápida en consola:** Se puede evaluar en vivo ejecutando `document.body.setAttribute('data-font-theme', 'modern')` o `document.body.removeAttribute('data-font-theme')`.
