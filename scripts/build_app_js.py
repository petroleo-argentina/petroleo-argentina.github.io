"""
Builder script to generate the updated frontend/app.js according to
reordenamiento_y_redisenio_petroleo_argentina.md
"""

app_js_content = r'''/**
 * PETRÓLEO EN ARGENTINA: DEL POZO AL PAÍS
 * Atlas Cartográfico & Crónica Visual de Datos
 * Motor Scrollytelling y Capas de Información Territorial (1950 - 2025)
 */

// Application State
let map = null;
let currentStep = 0;
let isAutoTourRunning = false;
let autoTourTimer = null;
let activeQuestionId = null;
let activeYear = 2025;
let timelineInterval = null;

// Datasets Store
let kpisData = {};
let timelineData = [];
let monthlyData = [];
let cohortsData = [];
let wellsMapData = [];
let fracturesData = [];
let macroData = [];
let basinsData = [];
let concessionsData = [];
let trajectoriesData = [];
let pipelinesData = [];
let facilitiesData = [];
let flaringData = [];
let operatorsData = [];

// Leaflet Layer Groups
let layerBasins = L.layerGroup();
let layerWellsConv = L.layerGroup();
let layerWellsShale = L.layerGroup();
let layerConcessions = L.layerGroup();
let layerTrajectories = L.layerGroup();
let layerPipelines = L.layerGroup();
let layerFacilities = L.layerGroup();
let layerFlaring = L.layerGroup();
let layerHighlight = L.layerGroup();

// Chart.js Active Instance
let activeMicroChart = null;

// ========================================================
// STORY CHAPTER DEFINITIONS (8 Capítulos Reordenados)
// ========================================================
const CHAPTERS = [
  // -------------------------------------------------------------
  // 01 — EL REGRESO
  // -------------------------------------------------------------
  {
    id: 'regreso',
    title: 'El regreso: después de décadas de caída, un nuevo récord',
    location: 'REPÚBLICA ARGENTINA · PERSPECTIVA HISTÓRICA 1950–2025',
    center: [-39.5, -66.5],
    zoom: 4.8,
    layersActive: ['basins'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">SERIE HISTÓRICA NACIONAL · CAPÍTULO 01</div>
        <h2 class="story-headline">El regreso: después de décadas de caída, un nuevo récord</h2>
        <p class="story-prose">
          Argentina produce petróleo desde hace más de un siglo. Tras alcanzar su pico histórico en 1998 con 45.926 miles de m³, la producción convencional ingresó en dos décadas de declinación ininterrumpida hasta tocar su piso en 2017 (28.330 miles de m³). En 2025, la curva nacional no solo revirtió la caída sino que estableció un <strong>nuevo máximo histórico de 46.438,5 miles de m³</strong> (~798.500 barriles diarios).
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val">46.438 <span class="kpi-unit">Mm³</span></span>
            <span class="kpi-label">RÉCORD HISTÓRICO 2025 (~798.450 bpd)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val text-positive">+63,9%</span>
            <span class="kpi-label">CRECIMIENTO DESDE EL PISO DE 2017</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Producción Nacional (1950 – 2025) · Mm³ y bpd</span>
            <div class="chart-toggle-links">
              <button class="chart-link active" id="btn-t-m3">Miles m³</button>
              <button class="chart-link" id="btn-t-bpd">bpd</button>
            </div>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Qué observar en el mapa:</strong> Las 5 cuencas sedimentarias productivas del país. Observa cómo la <strong>Cuenca Neuquina</strong> (en azul) concentró casi la totalidad de la recuperación nacional.
        </div>
      `;
      setupTimelineMicroChart('m3');
      document.getElementById('btn-t-m3')?.addEventListener('click', (e) => {
        document.querySelectorAll('.chart-link').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        setupTimelineMicroChart('m3');
      });
      document.getElementById('btn-t-bpd')?.addEventListener('click', (e) => {
        document.querySelectorAll('.chart-link').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        setupTimelineMicroChart('bpd');
      });
    }
  },

  // -------------------------------------------------------------
  // 02 — EL MAPA SE MUEVE
  // -------------------------------------------------------------
  {
    id: 'mapa_se_mueve',
    title: 'El mapa se mueve: el crecimiento no fue parejo',
    location: 'CUENCAS SEDIMENTARIAS · MIGRACIÓN TERRITORIAL',
    center: [-42.0, -68.5],
    zoom: 5.6,
    layersActive: ['basins', 'wells-conv', 'wells-shale'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">MIGRACIÓN GEOGRÁFICA · CAPÍTULO 02</div>
        <h2 class="story-headline">El mapa se mueve: la concentración territorial</h2>
        <p class="story-prose">
          El crecimiento no ocurrió de manera uniforme. Mientras cuencas maduras centenarias como el Golfo San Jorge o la Cuenca Cuyana continuaron perdiendo peso relativo, la <strong>Cuenca Neuquina</strong> comenzó a concentrar una porción cada vez mayor de la extracción nacional.
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val">64,7%</span>
            <span class="kpi-label">CUOTA DE NEUQUÉN EN EL TOTAL PAÍS (2025)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val text-muted">20,4%</span>
            <span class="kpi-label">CUOTA DE NEUQUÉN EN 2010 (GOLFO LIDERABA CON 32,4%)</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Participación Provincial en la Producción (2010 vs 2025)</span>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Qué observar en el mapa:</strong> Utiliza el deslizador temporal inferior para observar la migración de pozos entre 2006 y 2025 desde Comodoro Rivadavia hacia el triángulo Añelo-Rincón de los Sauces.
        </div>
      `;
      setupBasinComparisonMicroChart();
    }
  },

  // -------------------------------------------------------------
  // 03 — EL PUNTO DE QUIEBRE
  // -------------------------------------------------------------
  {
    id: 'punto_quiebre',
    title: 'El punto de quiebre: noviembre de 2023',
    location: 'TRANSICIÓN ESTRUCTURAL · CONVENCIONAL VS NO CONVENCIONAL',
    center: [-38.3, -68.9],
    zoom: 7.8,
    layersActive: ['basins', 'wells-conv', 'wells-shale'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">EL CROSSOVER HISTÓRICO · CAPÍTULO 03</div>
        <h2 class="story-headline">El punto de quiebre: noviembre de 2023</h2>
        <p class="story-prose">
          ¿Cuándo el no convencional pasó a ser mayoritario? La auditoría mensual demuestra que en junio de 2023 el no convencional representaba el 47,09%. El cruce definitivo ocurrió en <strong>noviembre de 2023</strong> (51,11% no convencional), consolidándose en 2024 y alcanzando el <strong>62,92% en 2025</strong>.
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val">NOV 2023</span>
            <span class="kpi-label">MES DEL CROSSOVER NACIONAL DEFINITIVO (51,11%)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val text-positive">62,9%</span>
            <span class="kpi-label">CUOTA NO CONVENCIONAL 2025 (99,1% SHALE)</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Producción Mensual: Convencional vs No Convencional (Miles m³)</span>
            <div class="chart-toggle-links">
              <button class="chart-link active" id="btn-c-vol">Volumen</button>
              <button class="chart-link" id="btn-c-pct">Porcentaje</button>
            </div>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Aclaración técnica auditada:</strong> En 2025, el 99,06% del petróleo no convencional proviene de Shale Vaca Muerta y el 0,92% de Tight. En el mapa se aprecian los pozos no convencionales (celeste) superando en volumen a la densa malla convencional (ámbar).
        </div>
      `;
      setupCrossoverMicroChart('volume');
      document.getElementById('btn-c-vol')?.addEventListener('click', (e) => {
        document.querySelectorAll('.chart-link').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        setupCrossoverMicroChart('volume');
      });
      document.getElementById('btn-c-pct')?.addEventListener('click', (e) => {
        document.querySelectorAll('.chart-link').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        setupCrossoverMicroChart('share');
      });
    }
  },

  // -------------------------------------------------------------
  // 04 — POCOS POZOS, MUCHO PETRÓLEO
  // -------------------------------------------------------------
  {
    id: 'pocos_pozos',
    title: 'Pocos pozos, mucho petróleo: la asimetría del subsuelo',
    location: 'CONCENTRACIÓN PRODUCTIVA · ANÁLISIS DE PARETO 2025',
    center: [-38.25, -68.85],
    zoom: 8.5,
    layersActive: ['basins', 'wells-shale', 'concessions'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">DISTRIBUCIÓN PARETO · CAPÍTULO 04</div>
        <h2 class="story-headline">Pocos pozos, mucho petróleo: la asimetría extrema</h2>
        <p class="story-prose">
          De los 26.219 pozos petroleros que produjeron en Argentina durante 2025, una fracción mínima explica el grueso de la oferta nacional. La mitad exacta del petróleo del país provino de apenas <strong>912 pozos</strong> ubicados en el corazón de Vaca Muerta.
        </p>

        <div class="big-number-single">
          <div class="big-number-hero-val">912</div>
          <div class="big-number-hero-label">POZOS EXPLICAN LA MITAD DEL PETRÓLEO ARGENTINO</div>
          <div class="big-number-hero-sub">Representan apenas el 3,48% de los 26.219 pozos activos en 2025. El Top 5% (1.311 pozos) genera el 58,22%.</div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Curva de Concentración de Pareto (% Pozos vs % Producción)</span>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Qué observar en el mapa:</strong> Al ingresar a este capítulo se atenúan los miles de pozos marginales y quedan iluminados los 912 pozos del núcleo hiper-productivo en Loma Campana, La Amarga Chica, Bandurria Sur y Bajada del Palo.
        </div>
      `;
      setupParetoMicroChart();
      applyParetoMapEffect(true);
    }
  },

  // -------------------------------------------------------------
  // 05 — CÓMO CAMBIÓ EL POZO
  // -------------------------------------------------------------
  {
    id: 'como_cambio_el_pozo',
    title: 'Cómo cambió el pozo: navegar a 3.000 metros',
    location: 'INGENIERÍA Y FRACTURAS · GEOMETRÍA SUBTERRÁNEA 3D',
    center: [-38.22, -68.82],
    zoom: 10.5,
    layersActive: ['concessions', 'trajectories'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">INGENIERÍA DE SUBSUELO · CAPÍTULO 05</div>
        <h2 class="story-headline">Cómo cambió el pozo: ramas laterales y fractura masiva</h2>
        <p class="story-prose">
          El crecimiento no provino de perforar más pozos sino de cambiar radicalmente su arquitectura física. Las ramas laterales triplicaron su longitud y la estimulación hidráulica se intensificó por diez.
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val">3.036 m</span>
            <span class="kpi-label">LONGITUD LATERAL PROMEDIO EN 2025 (MEDIANA 2.999 m)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val text-positive">51,2</span>
            <span class="kpi-label">ETAPAS DE FRACTURA PROMEDIO (FRENTE A 5,3 EN 2014)</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Evolución de Longitud Lateral (m) y Etapas (2014 – 2025)</span>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Qué observar en el mapa:</strong> Líneas cyan con las trayectorias horizontales 3D reales navegadas a 3.000 metros de profundidad vertical (TVD) en la roca madre de Vaca Muerta.
        </div>
      `;
      setupFracturesTrendsMicroChart();
      applyParetoMapEffect(false);
    }
  },

  // -------------------------------------------------------------
  // 06 — GENERACIONES DE POZOS
  // -------------------------------------------------------------
  {
    id: 'generaciones_pozos',
    title: 'Generaciones de pozos: la curva de aprendizaje',
    location: 'CURVAS DE DECLINO · COHORTES 2015 – 2024',
    center: [-38.28, -68.90],
    zoom: 9.8,
    layersActive: ['concessions', 'wells-shale'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">PRODUCTIVIDAD NORMALIZADA · CAPÍTULO 06</div>
        <h2 class="story-headline">Generaciones de pozos: la curva de aprendizaje</h2>
        <p class="story-prose">
          ¿Produce igual un pozo de 2015 que uno de 2024? La comparación por cohortes revela que un pozo moderno acumula en sus primeros 12 meses más de <strong>33.400 m³</strong> de petróleo, multiplicando por 14 el caudal de los pioneros.
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val">33.427 m³</span>
            <span class="kpi-label">MEDIANA ACUMULADA 12 MESES (COHORTE 2024)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val text-positive">14x</span>
            <span class="kpi-label">MULTIPLICADOR DE CAUDAL FRENTE A COHORTE 2015 (2.297 m³)</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Curvas de Producción Mediana por Mes de Vida (m³/mes)</span>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Regla metodológica:</strong> Se grafican medianas por edad relativa (mes 1 a 24) a partir de <code>analysis/exports/cohortes_productividad.csv</code> para evitar distorsiones por pozos atípicos.
        </div>
      `;
      setupCohortsMicroChart();
      applyParetoMapEffect(false);
    }
  },

  // -------------------------------------------------------------
  // 07 — DEL POZO AL PAÍS
  // -------------------------------------------------------------
  {
    id: 'del_pozo_al_pais',
    title: 'Del pozo al país: oleoductos, divisas y empleo',
    location: 'MACROECONOMÍA Y TERRITORIO · EVACUACIÓN Y EMPLEO',
    center: [-39.2, -65.5],
    zoom: 6.2,
    layersActive: ['pipelines', 'facilities', 'basins'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">IMPACTO TERRITORIAL Y EXTERNO · CAPÍTULO 07</div>
        <h2 class="story-headline">Del pozo al país: oleoductos, divisas y empleo</h2>
        <p class="story-prose">
          La expansión productiva coincidió temporalmente con un crecimiento sostenido del empleo privado registrado en hidrocarburos en Neuquén y la reversión de la balanza comercial de combustibles, impulsando la ampliación de oleoductos de evacuación como Oldelval y Vaca Muerta Sur.
        </p>

        <div class="editorial-kpis">
          <div class="kpi-entry">
            <span class="kpi-val text-positive">+83%</span>
            <span class="kpi-label">EXPANSIÓN DEL EMPLEO REGISTRADO EN NEUQUÉN (2010–2025)</span>
          </div>
          <div class="kpi-entry">
            <span class="kpi-val">Superávit</span>
            <span class="kpi-label">BALANZA COMERCIAL DE COMBUSTIBLES EN DÓLARES</span>
          </div>
        </div>

        <div class="editorial-chart-box">
          <div class="editorial-chart-head">
            <span class="chart-caption">Exportaciones e Importaciones de Combustibles (% Mercaderías)</span>
          </div>
          <div class="editorial-canvas-holder">
            <canvas id="micro-chart-canvas"></canvas>
          </div>
        </div>

        <div class="editorial-map-note">
          <strong>Qué observar en el mapa:</strong> Trazas de oleoductos: verde para los ductos troncales operativos (Oldelval a Puerto Rosales y Otasa a Chile) y línea punteada magenta para el megaproyecto Vaca Muerta Sur hacia Punta Colorada.
        </div>
      `;
      setupMacroTradeMicroChart();
      applyParetoMapEffect(false);
    }
  },

  // -------------------------------------------------------------
  // 08 — UN NUEVO MAPA PETROLERO
  // -------------------------------------------------------------
  {
    id: 'nuevo_mapa',
    title: 'Un nuevo mapa petrolero: qué aprendimos',
    location: 'SÍNTESIS CARTOGRÁFICA · EXPLORADOR LIBRE',
    center: [-39.5, -67.0],
    zoom: 5.2,
    layersActive: ['basins', 'wells-conv', 'wells-shale', 'pipelines', 'concessions', 'facilities'],
    renderContent: (container) => {
      container.innerHTML = `
        <div class="story-kicker">CONCLUSIONES AUDITADAS · CAPÍTULO 08</div>
        <h2 class="story-headline">Un nuevo mapa petrolero: cuatro respuestas</h2>
        <p class="story-prose">
          La evidencia empírica de 75 años de datos responde qué cambió estructuralmente en la matriz energética argentina:
        </p>

        <div class="editorial-conclusions-grid" style="display: flex; flex-direction: column; gap: 12px; margin: 16px 0;">
          <div class="conclusion-item" style="border-left: 2px solid var(--accent-crude); padding-left: 10px;">
            <strong style="color: var(--accent-crude); font-family: var(--font-mono); font-size: 0.75rem;">1. DÓNDE</strong>
            <p style="margin: 2px 0 0; font-size: 0.85rem; color: var(--ink-secondary);">Concentración geográfica absoluta: Neuquén genera casi el 65% del crudo del país (96% no convencional).</p>
          </div>
          <div class="conclusion-item" style="border-left: 2px solid var(--accent-cyan); padding-left: 10px;">
            <strong style="color: var(--accent-cyan); font-family: var(--font-mono); font-size: 0.75rem;">2. CÓMO</strong>
            <p style="margin: 2px 0 0; font-size: 0.85rem; color: var(--ink-secondary);">Ramas laterales que superan los 3.000 metros navegados en subsuelo y 50 etapas de estimulación.</p>
          </div>
          <div class="conclusion-item" style="border-left: 2px solid var(--accent-crude); padding-left: 10px;">
            <strong style="color: var(--accent-crude); font-family: var(--font-mono); font-size: 0.75rem;">3. CUÁNTO</strong>
            <p style="margin: 2px 0 0; font-size: 0.85rem; color: var(--ink-secondary);">Asimetría extrema: apenas 912 pozos (el 3,48%) explican el 50% de la producción de toda la República Argentina.</p>
          </div>
          <div class="conclusion-item" style="border-left: 2px solid var(--accent-emerald); padding-left: 10px;">
            <strong style="color: var(--accent-emerald); font-family: var(--font-mono); font-size: 0.75rem;">4. QUÉ LUGAR OCUPA</strong>
            <p style="margin: 2px 0 0; font-size: 0.85rem; color: var(--ink-secondary);">Nuevo récord histórico en 2025 (46.438 Mm³) con 62,9% no convencional (99,1% Shale Vaca Muerta).</p>
          </div>
        </div>

        <div style="margin-top: 16px; display: flex; flex-direction: column; gap: 8px;">
          <button id="btn-re-tour" class="editorial-nav-btn" style="width: 100%; text-align: center; justify-content: center;">
            &larr; Reiniciar Recorrido
          </button>
          <button id="btn-open-q-from-story" class="editorial-nav-btn" style="width: 100%; text-align: center; justify-content: center; border-color: var(--accent-crude); color: var(--accent-crude);">
            Explorar Índice de Preguntas &rarr;
          </button>
        </div>
      `;
      setupConcessionsRankingMicroChart();
      applyParetoMapEffect(false);

      document.getElementById('btn-re-tour')?.addEventListener('click', () => goToStep(0));
      document.getElementById('btn-open-q-from-story')?.addEventListener('click', () => {
        document.getElementById('modal-preguntas')?.classList.remove('hidden');
      });
    }
  }
];

// ========================================================
// INITIALIZATION WITH DUAL API / STANDALONE BUNDLE RESILIENCE
// ========================================================
async function initScrollyPlatform() {
  setupModal();
  setupLayersDrawer();
  setupQuestionsModal();
  setupTimelineScrubber();
  setupNavigationButtons();
  setupScrollWheelNavigation();
  setupKeyboardNavigation();
  setupAutoTour();
  setupHeroSplash();
  buildVerticalStepper();

  // Initialize Map
  initLeafletMap();

  try {
    // Parallel Fetch with transparent fallback to window.DATA_BUNDLE
    const [kpis, timeline, monthly, cohorts, wells, fractures, macro, basins, concessions, trajectories, pipelines, facilities, flaring, operators] = await Promise.all([
      loadResource('/api/kpis', 'kpis'),
      loadResource('/api/timeline', 'timeline_1950_2025'),
      loadResource('/api/production/monthly', 'conv_vs_noconv_monthly'),
      loadResource('/api/cohorts', 'cohorts_decay_curves'),
      loadResource('/api/wells/map', 'wells_map_sample'),
      loadResource('/api/fractures/trends', 'technical_fractures_trends'),
      loadResource('/api/macro/trends', 'macro_employment_trends'),
      loadResource('/api/geo/basins', 'geo_basins'),
      loadResource('/api/geo/concessions', 'geo_concessions_vaca_muerta'),
      loadResource('/api/geo/trajectories', 'geo_trajectories_sample'),
      loadResource('/api/geo/pipelines', 'geo_pipelines_sample'),
      loadResource('/api/geo/facilities', 'geo_refineries_ports'),
      loadResource('/api/geo/flaring', 'geo_flaring_sample'),
      loadResource('/api/operators', 'top_operators_2025')
    ]);

    kpisData = kpis;
    timelineData = timeline;
    monthlyData = monthly;
    cohortsData = cohorts;
    wellsMapData = wells;
    fracturesData = fractures;
    macroData = macro;
    basinsData = basins;
    concessionsData = concessions;
    trajectoriesData = trajectories;
    pipelinesData = pipelines;
    facilitiesData = facilities;
    flaringData = flaring;
    operatorsData = operators;

    // Populate Map Layers
    buildMapLayers();

    // Start with Chapter 0
    goToStep(0);

  } catch (error) {
    console.error("Error loading scrollytelling data:", error);
  }
}

// Resilient Loader: Uses API when online, Bundled JS data when offline / file protocol
async function loadResource(url, bundleKey) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    if (window.DATA_BUNDLE && window.DATA_BUNDLE[bundleKey] !== undefined) {
      return window.DATA_BUNDLE[bundleKey];
    }
    throw err;
  }
}

// Hero Splash Setup
function setupHeroSplash() {
  const splash = document.getElementById('hero-splash');
  const startBtn = document.getElementById('btn-start-tour');
  if (startBtn && splash) {
    startBtn.addEventListener('click', () => {
      splash.classList.add('hero-hidden');
      goToStep(0);
    });
  }
}

let currentBaseLayer = null;
let currentLabelsLayer = null;

const BASEMAP_STYLES = {
  'dark-esri': {
    base: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    labels: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}',
    maxZoom: 16,
    attribution: '&copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
  },
  'satellite': {
    base: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    labels: 'https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    maxZoom: 18,
    attribution: '&copy; Esri, Maxar, Earthstar Geographics'
  },
  'carto-dark': {
    base: 'https://basemaps.cartocdn.com/rastertiles/dark_nolabels/{z}/{x}/{y}.png',
    labels: 'https://basemaps.cartocdn.com/rastertiles/dark_only_labels/{z}/{x}/{y}.png',
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
  }
};

function setBasemapStyle(styleKey) {
  const cfg = BASEMAP_STYLES[styleKey] || BASEMAP_STYLES['dark-esri'];
  if (currentBaseLayer) map.removeLayer(currentBaseLayer);
  if (currentLabelsLayer) map.removeLayer(currentLabelsLayer);

  currentBaseLayer = L.tileLayer(cfg.base, {
    maxZoom: cfg.maxZoom,
    attribution: cfg.attribution
  }).addTo(map);

  if (cfg.labels) {
    currentLabelsLayer = L.tileLayer(cfg.labels, {
      maxZoom: cfg.maxZoom,
      pane: 'shadowPane'
    }).addTo(map);
  }
}

function initLeafletMap() {
  map = L.map('scrolly-map', {
    center: [-39.5, -66.5],
    zoom: 4.8,
    zoomControl: false,
    attributionControl: false,
    preferCanvas: true
  });

  setBasemapStyle('dark-esri');

  L.control.attribution({ position: 'bottomright', prefix: false })
    .addAttribution('Sec. Energía / PetroDB · 1950–2025')
    .addTo(map);

  L.control.zoom({ position: 'topright' }).addTo(map);

  layerBasins.addTo(map);
  layerWellsConv.addTo(map);
  layerWellsShale.addTo(map);
  layerConcessions.addTo(map);
  layerTrajectories.addTo(map);
  layerPipelines.addTo(map);
  layerFacilities.addTo(map);
  layerFlaring.addTo(map);
  layerHighlight.addTo(map);
}

// Build Map Layers
function buildMapLayers() {
  const canvasRenderer = L.canvas({ padding: 0.5 });

  // 1. Basins Layer
  basinsData.forEach(b => {
    const isNeuquina = b.id === 'neuquina';
    const poly = L.polygon(b.coords, {
      color: isNeuquina ? '#38bdf8' : '#c98a3c',
      weight: isNeuquina ? 2 : 1,
      opacity: isNeuquina ? 0.9 : 0.45,
      fillColor: isNeuquina ? '#38bdf8' : '#c98a3c',
      fillOpacity: isNeuquina ? 0.12 : 0.04
    });
    poly.bindTooltip(`<strong>${b.nombre}</strong><br>${b.cuota_2025}`, {
      className: 'custom-leaflet-popup'
    });
    poly.on('click', () => showInspector('CUENCA SEDIMENTARIA', {
      'Nombre': b.nombre,
      'Participación 2025': b.cuota_2025,
      'Producción 2025': b.prod_2025,
      'Tipo de petróleo': b.tipo_crudo,
      'Descripción': b.descripcion
    }));
    layerBasins.addLayer(poly);
  });

  // 2. Concessions Layer (Vaca Muerta Megayacimientos)
  concessionsData.forEach(c => {
    const concessionCircle = L.circle([c.lat, c.lon], {
      radius: c.radio_km * 1000,
      color: '#d48b38',
      weight: 1.5,
      fillColor: '#d48b38',
      fillOpacity: 0.18,
      dashArray: '4, 4'
    });
    concessionCircle.bindTooltip(`<strong>${c.nombre}</strong> (${c.operador})<br>Producción: ${Number(c.prod_2025_bpd).toLocaleString('es-AR')} bpd`, {
      className: 'custom-leaflet-popup'
    });
    concessionCircle.on('click', () => showInspector('CONCESIÓN DE EXPLOTACIÓN', {
      'Área': c.nombre,
      'Operador': c.operador,
      'Producción estimada': `${Number(c.prod_2025_bpd).toLocaleString('es-AR')} barriles/día`,
      'Pozos activos': c.pozos_activos,
      'Destacado': c.destacado
    }));
    layerConcessions.addLayer(concessionCircle);
  });

  // 3. Trajectories Layer (3D Horizontal Wells)
  trajectoriesData.forEach(t => {
    if (t.path && t.path.length > 1) {
      const line = L.polyline(t.path, {
        color: '#38bdf8',
        weight: 2.2,
        opacity: 0.9
      });
      line.bindTooltip(`<strong>Pozo: ${t.sigla}</strong><br>Longitud lateral: ${t.largo_m} m`, {
        className: 'custom-leaflet-popup'
      });
      line.on('click', () => showInspector('TRAYECTORIA HORIZONTAL 3D', {
        'Identificador': t.sigla,
        'Yacimiento': t.yacimiento,
        'Longitud horizontal': `${t.largo_m} metros`,
        'Profundidad vertical (TVD)': `${t.tvd_m} metros`,
        'Profundidad total (MD)': `${t.md_m} metros`,
        'Fecha completación': t.fecha
      }));
      layerTrajectories.addLayer(line);
    }
  });

  // 4. Pipelines Layer (Oleoductos Oldelval, Otasa, VM Sur)
  pipelinesData.forEach(p => {
    const isUnderConstruction = p.estado.includes('construcción');
    const poly = L.polyline(p.path, {
      color: isUnderConstruction ? '#c25e3e' : '#10b981',
      weight: 2.5,
      opacity: 0.85,
      dashArray: isUnderConstruction ? '6, 6' : null
    });
    poly.bindTooltip(`<strong>${p.nombre}</strong><br>Capacidad: ${p.capacidad_bpd}<br>Estado: ${p.estado}`, {
      className: 'custom-leaflet-popup'
    });
    poly.on('click', () => showInspector('OLEODUCTO TRONCAL', {
      'Ducto': p.nombre,
      'Origen': p.origen,
      'Destino': p.destino,
      'Capacidad': p.capacidad_bpd,
      'Estado': p.estado,
      'Descripción': p.descripcion
    }));
    layerPipelines.addLayer(poly);
  });

  // 5. Facilities Layer (Refineries & Export Ports)
  facilitiesData.forEach(f => {
    const isPort = f.tipo.includes('Puerto');
    const marker = L.circleMarker([f.lat, f.lon], {
      renderer: canvasRenderer,
      radius: isPort ? 6.5 : 5.5,
      color: '#fff',
      fillColor: isPort ? '#38bdf8' : '#d48b38',
      fillOpacity: 0.9,
      weight: 1.2
    });
    marker.bindTooltip(`<strong>${f.nombre}</strong><br>${f.tipo}`, {
      className: 'custom-leaflet-popup'
    });
    marker.on('click', () => showInspector(f.tipo.toUpperCase(), {
      'Instalación': f.nombre,
      'Tipo': f.tipo,
      'Capacidad / Función': f.capacidad,
      'Operador': f.empresa || 'Consorcio Portuario'
    }));
    layerFacilities.addLayer(marker);
  });

  // 6. Flaring Points Layer
  flaringData.forEach(fl => {
    const marker = L.circleMarker([fl.lat, fl.lon], {
      renderer: canvasRenderer,
      radius: 4,
      color: '#c25e3e',
      fillColor: '#c25e3e',
      fillOpacity: 0.8,
      weight: 1
    });
    marker.bindTooltip(`<strong>${fl.nombre}</strong><br>${fl.tipo} (${fl.operador})`, {
      className: 'custom-leaflet-popup'
    });
    marker.on('click', () => showInspector('VENTEO / FLARING DECLARADO', {
      'Punto': fl.nombre,
      'Operador': fl.operador,
      'Tipo de instalación': fl.tipo,
      'Fuente': 'Res. Secretaría de Energía'
    }));
    layerFlaring.addLayer(marker);
  });

  // 7. Render Wells Layer with initial year
  filterWellsByYear(activeYear);
}

// Render and filter wells by year for high 60fps performance
function filterWellsByYear(year) {
  layerWellsConv.clearLayers();
  layerWellsShale.clearLayers();

  const canvasRenderer = L.canvas({ padding: 0.5 });

  wellsMapData.forEach(w => {
    if (w.anio_primera_prod <= year) {
      const isShale = (w.tipo_recurso === 'NO CONVENCIONAL');
      const radius = Math.min(5.0, Math.max(2.0, Math.sqrt(w.prod_2025_m3 || 1000) / 80));

      const marker = L.circleMarker([w.lat, w.lon], {
        renderer: canvasRenderer,
        radius: isShale ? radius : 2.0,
        color: isShale ? '#38bdf8' : '#d48b38',
        fillColor: isShale ? '#38bdf8' : '#d48b38',
        fillOpacity: isShale ? 0.75 : 0.45,
        weight: 0.5
      });

      marker.bindTooltip(`<strong>${w.sigla}</strong><br>${w.empresa}<br>${w.yacimiento} (${w.tipo_recurso})`, {
        className: 'custom-leaflet-popup'
      });

      marker.on('click', () => showInspector('POZO PRODUCTOR', {
        'Sigla': w.sigla,
        'Operador': w.empresa,
        'Yacimiento': w.yacimiento,
        'Provincia': w.provincia,
        'Tipo de Recurso': w.tipo_recurso,
        'Año primera prod': w.anio_primera_prod,
        'Producción anual 2025': `${Number(w.prod_2025_m3 || 0).toLocaleString('es-AR')} m³`
      }));

      if (isShale) {
        layerWellsShale.addLayer(marker);
      } else {
        layerWellsConv.addLayer(marker);
      }
    }
  });

  const yrLabel = document.getElementById('scrubber-year-label');
  if (yrLabel) yrLabel.textContent = year;
}

// Pareto visual effect: Highlight top producing wells in Vaca Muerta, dim marginal wells
function applyParetoMapEffect(enable) {
  if (!wellsMapData.length) return;

  layerWellsConv.clearLayers();
  layerWellsShale.clearLayers();

  const canvasRenderer = L.canvas({ padding: 0.5 });

  if (enable) {
    // Sort wells by 2025 production descending
    const sorted = [...wellsMapData].sort((a, b) => (b.prod_2025_m3 || 0) - (a.prod_2025_m3 || 0));
    // Top 15% in sample represents the core high-producing wells (equivalent to the 912 top wells)
    const cutoffProd = sorted[Math.floor(sorted.length * 0.15)]?.prod_2025_m3 || 10000;

    wellsMapData.forEach(w => {
      const isTopProducer = (w.prod_2025_m3 || 0) >= cutoffProd;
      const isShale = (w.tipo_recurso === 'NO CONVENCIONAL');

      const marker = L.circleMarker([w.lat, w.lon], {
        renderer: canvasRenderer,
        radius: isTopProducer ? 4.5 : 1.5,
        color: isTopProducer ? '#38bdf8' : '#475569',
        fillColor: isTopProducer ? '#38bdf8' : '#475569',
        fillOpacity: isTopProducer ? 0.95 : 0.12,
        weight: isTopProducer ? 1.0 : 0.2
      });

      marker.bindTooltip(`<strong>${w.sigla}</strong><br>${isTopProducer ? '⭐ POZO TOP PRODUCTOR' : 'Pozo Convencional Maduro'}<br>Producción 2025: ${Number(w.prod_2025_m3 || 0).toLocaleString('es-AR')} m³`, {
        className: 'custom-leaflet-popup'
      });

      if (isTopProducer) {
        layerWellsShale.addLayer(marker);
      } else {
        layerWellsConv.addLayer(marker);
      }
    });
  } else {
    filterWellsByYear(activeYear);
  }
}

// ========================================================
// SCROLLYTELLING CHAPTER NAVIGATION
// ========================================================
function goToStep(stepIndex) {
  if (stepIndex < 0 || stepIndex >= CHAPTERS.length) return;
  currentStep = stepIndex;
  activeQuestionId = null;
  layerHighlight.clearLayers();
  const chapter = CHAPTERS[currentStep];

  // 1. Update Camera
  map.flyTo(chapter.center, chapter.zoom, {
    duration: 1.4,
    easeLinearity: 0.25
  });

  // 2. Synchronize Layers
  syncLayersForChapter(chapter.layersActive);

  // 3. Update Narrative Content Card
  const badgeEl = document.getElementById('chapter-badge');
  const locEl = document.getElementById('chapter-location');
  const contentEl = document.getElementById('chapter-content');
  
  if (badgeEl) badgeEl.textContent = `0${currentStep + 1} / 0${CHAPTERS.length}`;
  if (locEl) locEl.textContent = chapter.location;
  if (contentEl) chapter.renderContent(contentEl);

  // 4. Update Navigation Buttons
  const prevBtns = [document.getElementById('btn-prev-step'), document.getElementById('btn-prev-chapter')];
  const nextBtns = [document.getElementById('btn-next-step'), document.getElementById('btn-next-chapter')];

  prevBtns.forEach(btn => {
    if (btn) btn.disabled = (currentStep === 0);
  });

  nextBtns.forEach(btn => {
    if (btn) {
      if (currentStep === CHAPTERS.length - 1) {
        btn.disabled = true;
      } else {
        btn.disabled = false;
      }
    }
  });

  // 5. Update Stepper & Progress Bar
  updateStepperState();
  const progressBar = document.getElementById('story-progress-bar');
  if (progressBar) {
    const pct = ((currentStep + 1) / CHAPTERS.length) * 100;
    progressBar.style.width = `${pct}%`;
  }

  // 6. Show/Hide Bottom Scrubber
  const scrubberBar = document.getElementById('timeline-scrubber-bar');
  if (scrubberBar) {
    if (currentStep === 1) {
      scrubberBar.style.opacity = '1';
      scrubberBar.style.pointerEvents = 'auto';
    } else {
      scrubberBar.style.opacity = '0';
      scrubberBar.style.pointerEvents = 'none';
    }
  }
}

function syncLayersForChapter(activeKeys) {
  const layerMap = {
    'wells-conv': layerWellsConv,
    'wells-shale': layerWellsShale,
    'basins': layerBasins,
    'concessions': layerConcessions,
    'trajectories': layerTrajectories,
    'pipelines': layerPipelines,
    'facilities': layerFacilities,
    'flaring': layerFlaring
  };

  Object.keys(layerMap).forEach(k => {
    if (activeKeys.includes(k)) {
      if (!map.hasLayer(layerMap[k])) map.addLayer(layerMap[k]);
    } else {
      if (map.hasLayer(layerMap[k])) map.removeLayer(layerMap[k]);
    }
  });
}

function buildVerticalStepper() {
  const container = document.getElementById('stepper-nodes');
  if (!container) return;
  container.innerHTML = '';

  CHAPTERS.forEach((ch, idx) => {
    const node = document.createElement('div');
    node.className = `index-tick-item ${idx === 0 ? 'active' : ''}`;
    node.dataset.step = idx;
    node.innerHTML = `
      <span class="index-tick-label">0${idx + 1}. ${ch.title.split(':')[0]}</span>
      <div class="index-tick-point"></div>
    `;
    node.addEventListener('click', () => goToStep(idx));
    container.appendChild(node);
  });
}

function updateStepperState() {
  const nodes = document.querySelectorAll('.index-tick-item');
  nodes.forEach((n, idx) => {
    if (idx === currentStep) {
      n.classList.add('active');
    } else {
      n.classList.remove('active');
    }
  });
}

function setupNavigationButtons() {
  const handlePrev = () => { if (currentStep > 0) goToStep(currentStep - 1); };
  const handleNext = () => { if (currentStep < CHAPTERS.length - 1) goToStep(currentStep + 1); };

  document.getElementById('btn-prev-step')?.addEventListener('click', handlePrev);
  document.getElementById('btn-prev-chapter')?.addEventListener('click', handlePrev);
  document.getElementById('btn-next-step')?.addEventListener('click', handleNext);
  document.getElementById('btn-next-chapter')?.addEventListener('click', handleNext);
}

function setupScrollWheelNavigation() {
  let isThrottled = false;
  window.addEventListener('wheel', (e) => {
    const qModal = document.getElementById('modal-preguntas');
    const mModal = document.getElementById('modal-metodologia');
    const splash = document.getElementById('hero-splash');
    if ((qModal && !qModal.classList.contains('hidden')) || 
        (mModal && !mModal.classList.contains('hidden')) ||
        (splash && !splash.classList.contains('hero-hidden'))) {
      return;
    }

    const card = document.getElementById('active-story-card');
    if (card && card.contains(e.target)) {
      const isAtBottom = (card.scrollHeight - card.scrollTop <= card.clientHeight + 5);
      const isAtTop = (card.scrollTop <= 5);
      if (e.deltaY > 0 && !isAtBottom) return;
      if (e.deltaY < 0 && !isAtTop) return;
    }

    if (isThrottled) return;

    if (e.deltaY > 35) {
      if (currentStep < CHAPTERS.length - 1) {
        goToStep(currentStep + 1);
        isThrottled = true;
        setTimeout(() => { isThrottled = false; }, 900);
      }
    } else if (e.deltaY < -35) {
      if (currentStep > 0) {
        goToStep(currentStep - 1);
        isThrottled = true;
        setTimeout(() => { isThrottled = false; }, 900);
      }
    }
  }, { passive: true });
}

function setupKeyboardNavigation() {
  window.addEventListener('keydown', (e) => {
    if (['ArrowDown', 'ArrowRight', 'Space'].includes(e.code)) {
      if (currentStep < CHAPTERS.length - 1) {
        e.preventDefault();
        goToStep(currentStep + 1);
      }
    } else if (['ArrowUp', 'ArrowLeft'].includes(e.code)) {
      if (currentStep > 0) {
        e.preventDefault();
        goToStep(currentStep - 1);
      }
    } else if (e.code === 'Escape') {
      document.getElementById('modal-preguntas')?.classList.add('hidden');
      document.getElementById('modal-metodologia')?.classList.add('hidden');
      document.getElementById('layers-drawer')?.classList.add('hidden');
    }
  });
}

function setupAutoTour() {
  const btn = document.getElementById('btn-auto-tour');
  const txt = document.getElementById('auto-tour-text');
  if (!btn) return;

  btn.addEventListener('click', () => {
    isAutoTourRunning = !isAutoTourRunning;
    if (isAutoTourRunning) {
      btn.classList.add('active');
      if (txt) txt.textContent = 'Pausar relato';
      scheduleNextAutoTour();
    } else {
      btn.classList.remove('active');
      if (txt) txt.textContent = 'Relato continuo';
      clearTimeout(autoTourTimer);
    }
  });
}

function scheduleNextAutoTour() {
  if (!isAutoTourRunning) return;
  autoTourTimer = setTimeout(() => {
    if (!isAutoTourRunning) return;
    if (currentStep < CHAPTERS.length - 1) {
      goToStep(currentStep + 1);
      scheduleNextAutoTour();
    } else {
      isAutoTourRunning = false;
      document.getElementById('btn-auto-tour')?.classList.remove('active');
      const txt = document.getElementById('auto-tour-text');
      if (txt) txt.textContent = 'Relato continuo';
    }
  }, 10000);
}

function setupQuestionsModal() {
  const modal = document.getElementById('modal-preguntas');
  const openBtn = document.getElementById('btn-preguntas');
  const closeBtn = document.getElementById('modal-preguntas-close');

  openBtn?.addEventListener('click', () => modal?.classList.remove('hidden'));
  closeBtn?.addEventListener('click', () => modal?.classList.add('hidden'));

  document.querySelectorAll('.q-editorial-entry').forEach(entry => {
    entry.addEventListener('click', () => {
      const chIdx = parseInt(entry.dataset.chapterIndex || '0');
      modal?.classList.add('hidden');
      document.getElementById('hero-splash')?.classList.add('hero-hidden');
      goToStep(chIdx);
    });
  });
}

function setupTimelineScrubber() {
  const slider = document.getElementById('global-year-slider');
  const playBtn = document.getElementById('btn-play-timeline');
  const playIcon = document.getElementById('play-icon');
  const pauseIcon = document.getElementById('pause-icon');

  if (slider) {
    slider.addEventListener('input', (e) => {
      activeYear = parseInt(e.target.value);
      filterWellsByYear(activeYear);
      updateScrubberProdBadge(activeYear);
    });
  }

  if (playBtn) {
    playBtn.addEventListener('click', () => {
      if (timelineInterval) {
        stopTimelinePlayback();
      } else {
        startTimelinePlayback();
      }
    });
  }

  function startTimelinePlayback() {
    if (playIcon) playIcon.classList.add('hidden');
    if (pauseIcon) pauseIcon.classList.remove('hidden');

    timelineInterval = setInterval(() => {
      if (activeYear >= 2025) {
        activeYear = 2006;
      } else {
        activeYear += 1;
      }
      if (slider) slider.value = activeYear;
      filterWellsByYear(activeYear);
      updateScrubberProdBadge(activeYear);
    }, 700);
  }

  function stopTimelinePlayback() {
    if (playIcon) playIcon.classList.remove('hidden');
    if (pauseIcon) pauseIcon.classList.add('hidden');
    clearInterval(timelineInterval);
    timelineInterval = null;
  }
}

function updateScrubberProdBadge(year) {
  const prodLabel = document.getElementById('scrubber-prod-label');
  if (!prodLabel || !timelineData.length) return;
  const match = timelineData.find(d => d.anio === year);
  if (match) {
    prodLabel.textContent = `${Number(match.prod_pet_miles_m3).toLocaleString('es-AR')} Mm³`;
  }
}

// ========================================================
// EMBEDDED MICRO-CHARTS ENGINE (Chart.js Inside Card)
// ========================================================
function destroyActiveChart() {
  if (activeMicroChart) {
    activeMicroChart.destroy();
    activeMicroChart = null;
  }
}

// 1. Timeline Chart (1950 – 2025)
function setupTimelineMicroChart(metric = 'm3') {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx || !timelineData.length) return;

  const labels = timelineData.map(d => d.anio);
  const dataVals = timelineData.map(d => metric === 'm3' ? d.prod_pet_miles_m3 : d.bpd);

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: dataVals,
        borderColor: '#d48b38',
        borderWidth: 2,
        fill: true,
        backgroundColor: 'rgba(212, 139, 56, 0.12)',
        tension: 0.2,
        pointRadius: (c) => [1998, 2017, 2023, 2025].includes(labels[c.dataIndex]) ? 3.5 : 0,
        pointBackgroundColor: '#d48b38',
        pointBorderColor: '#fff',
        pointBorderWidth: 1.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#171c24',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          padding: 8,
          callbacks: {
            label: (ctx) => `${metric === 'm3' ? Number(ctx.parsed.y).toLocaleString('es-AR') + ' Mm³' : Number(ctx.parsed.y).toLocaleString('es-AR') + ' bpd'}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#64748b', maxTicksLimit: 8 }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.04)' },
          ticks: {
            color: '#64748b',
            callback: (v) => metric === 'm3' ? `${(v/1000).toFixed(0)}k` : `${(v/1000).toFixed(0)}k bpd`
          }
        }
      }
    }
  });
}

// 2. Basin Share Comparison (2010 vs 2025)
function setupBasinComparisonMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx) return;

  activeMicroChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Neuquén', 'Chubut', 'Santa Cruz', 'Mendoza', 'Otras'],
      datasets: [
        { label: '2010', data: [20.4, 32.4, 21.8, 14.2, 11.2], backgroundColor: 'rgba(212, 139, 56, 0.45)' },
        { label: '2025', data: [64.7, 15.5, 9.8, 6.2, 3.8], backgroundColor: 'rgba(56, 189, 248, 0.85)' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ea8b6', font: { size: 10 } } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#64748b', callback: v => `${v}%` } }
      }
    }
  });
}

// 3. Monthly Crossover (2006 – 2025) [CORREGIDO AUDITORÍA: Noviembre 2023]
function setupCrossoverMicroChart(mode = 'volume') {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx || !monthlyData.length) return;

  // Downsample to quarterly for snappy rendering
  const filtered = monthlyData.filter((_, idx) => idx % 3 === 0);
  const labels = filtered.map(d => `${d.anio}-${String(d.mes).padStart(2, '0')}`);
  
  // Use audited keys: pet_conv_miles_m3 & pet_no_conv_miles_m3 (with fallback)
  const conv = filtered.map(d => {
    if (mode === 'volume') return d.pet_conv_miles_m3 ?? d.convencional_m3_mes;
    return d.share_no_conv_pct ? (100 - d.share_no_conv_pct) : (d.convencional_share_pct ?? 100);
  });
  const noconv = filtered.map(d => {
    if (mode === 'volume') return d.pet_no_conv_miles_m3 ?? d.no_convencional_m3_mes;
    return d.share_no_conv_pct ?? d.no_convencional_share_pct ?? 0;
  });

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Convencional',
          data: conv,
          borderColor: '#d48b38',
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.2
        },
        {
          label: 'No Convencional (Shale)',
          data: noconv,
          borderColor: '#38bdf8',
          borderWidth: 2.2,
          pointRadius: (c) => labels[c.dataIndex] === '2023-11' ? 4 : 0,
          pointBackgroundColor: '#38bdf8',
          pointBorderColor: '#fff',
          pointBorderWidth: 1.5,
          tension: 0.2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ea8b6', font: { size: 10 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString('es-AR')} ${mode === 'volume' ? 'Miles m³' : '%'}`
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b', maxTicksLimit: 6 } },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', callback: v => mode === 'volume' ? `${(v/1000).toFixed(0)}k` : `${v}%` }
        }
      }
    }
  });
}

// 4. Pareto Concentración MicroChart
function setupParetoMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx) return;

  const percentiles = ['Top 1%', 'Top 5%', 'Top 10%', 'Top 13,1%', 'Top 20%', 'Top 35,5%', 'Total'];
  const prodPct = [22.86, 58.22, 70.98, 75.14, 81.50, 90.00, 100.00];

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: percentiles,
      datasets: [{
        label: '% Producción Acumulada',
        data: prodPct,
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.12)',
        fill: true,
        borderWidth: 2.5,
        tension: 0.2,
        pointRadius: (c) => c.dataIndex === 1 ? 5 : 3,
        pointBackgroundColor: (c) => c.dataIndex === 1 ? '#d48b38' : '#38bdf8',
        pointBorderColor: '#fff',
        pointBorderWidth: 1.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Producción acumulada: ${ctx.parsed.y}%`
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b' } },
        y: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', callback: v => `${v}%` }
        }
      }
    }
  });
}

// 5. Fractures Engineering Trends Chart
function setupFracturesTrendsMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx) return;

  const years = ['2014', '2016', '2018', '2020', '2022', '2024', '2025'];
  const lateralLength = [70, 577, 1084, 1623, 1784, 2629, 3036];
  const stages = [5.3, 9.5, 15.7, 28.1, 31.2, 43.4, 51.2];

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: years,
      datasets: [
        {
          label: 'Longitud Lateral (m)',
          data: lateralLength,
          borderColor: '#38bdf8',
          borderWidth: 2,
          yAxisID: 'y',
          pointRadius: 2.5
        },
        {
          label: 'Etapas de Fractura',
          data: stages,
          borderColor: '#d48b38',
          borderWidth: 2,
          yAxisID: 'y1',
          pointRadius: 2.5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ea8b6', font: { size: 9.5 } } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b' } },
        y: {
          position: 'left',
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#38bdf8', callback: v => `${v}m` }
        },
        y1: {
          position: 'right',
          grid: { display: false },
          ticks: { color: '#d48b38' }
        }
      }
    }
  });
}

// 6. Cohorts Decline Curves Chart [CORREGIDO AUDITORÍA: d.cohorte & d.mediana_prod_m3]
function setupCohortsMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx || !cohortsData.length) return;

  const cohorts2015 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2015);
  const cohorts2018 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2018);
  const cohorts2021 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2021);
  const cohorts2024 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2024);

  const maxMonths = 24;
  const labels = Array.from({ length: maxMonths }, (_, i) => `M${i + 1}`);

  const extractCurve = (list) => {
    return labels.map((_, idx) => {
      const match = list.find(d => (d.mes_vida ?? d.mes_relativo) === idx);
      return match ? (match.mediana_prod_m3 ?? match.media_prod_m3 ?? match.prod_pet_m3_dia_promedio ?? 0) : null;
    });
  };

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Cohorte 2015 (Piloto)',
          data: extractCurve(cohorts2015),
          borderColor: '#64748b',
          borderDash: [3, 3],
          borderWidth: 1.5,
          pointRadius: 0
        },
        {
          label: 'Cohorte 2018',
          data: extractCurve(cohorts2018),
          borderColor: '#d48b38',
          borderDash: [4, 4],
          borderWidth: 1.8,
          pointRadius: 0
        },
        {
          label: 'Cohorte 2021',
          data: extractCurve(cohorts2021),
          borderColor: '#10b981',
          borderWidth: 2,
          pointRadius: 0
        },
        {
          label: 'Cohorte 2024 (Moderno)',
          data: extractCurve(cohorts2024),
          borderColor: '#38bdf8',
          borderWidth: 2.5,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ea8b6', font: { size: 9 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString('es-AR')} m³/mes`
          }
        }
      },
      scales: {
        x: { ticks: { color: '#64748b', maxTicksLimit: 8 }, grid: { display: false } },
        y: { ticks: { color: '#64748b' }, grid: { color: 'rgba(255,255,255,0.04)' } }
      }
    }
  });
}

// 7. Macro Trade & Employment Chart [CORREGIDO AUDITORÍA: d.year & d.fuel_exports_pct]
function setupMacroTradeMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx || !macroData.length) return;

  const labels = macroData.map(d => d.year ?? d.anio);
  const exp = macroData.map(d => d.fuel_exports_pct ?? d.combustibles_export_pct_mercancias ?? 0);
  const imp = macroData.map(d => d.fuel_imports_pct ?? d.combustibles_import_pct_mercancias ?? 0);

  activeMicroChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Exportaciones Combustibles (%)',
          data: exp,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.12)',
          fill: true,
          tension: 0.2,
          pointRadius: 2.5
        },
        {
          label: 'Importaciones Combustibles (%)',
          data: imp,
          borderColor: '#c25e3e',
          borderWidth: 1.8,
          borderDash: [3, 3],
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ea8b6', font: { size: 9 } } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b' } },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', callback: v => `${v}%` }
        }
      }
    }
  });
}

// 8. Concessions Ranking Bar Chart
function setupConcessionsRankingMicroChart() {
  destroyActiveChart();
  const ctx = document.getElementById('micro-chart-canvas');
  if (!ctx || !concessionsData.length) return;

  const top6 = concessionsData.slice(0, 6);
  activeMicroChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: top6.map(c => c.nombre.replace(' Oeste', '')),
      datasets: [{
        data: top6.map(c => c.prod_2025_bpd),
        backgroundColor: ['#d48b38', '#38bdf8', '#10b981', '#a855f7', '#64748b', '#ec4899']
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#64748b', callback: v => `${(v/1000).toFixed(0)}k` } },
        y: { grid: { display: false }, ticks: { color: '#fff', font: { size: 9 } } }
      }
    }
  });
}

// Inspector Side Panel
function showInspector(title, props) {
  let content = `<div class="inspector-box"><h4 class="inspector-title">${title}</h4><div class="inspector-table">`;
  Object.keys(props).forEach(k => {
    content += `<div class="inspector-row"><span class="inspector-k">${k}</span><span class="inspector-v">${props[k]}</span></div>`;
  });
  content += `</div></div>`;

  const noteEl = document.querySelector('.editorial-map-note');
  if (noteEl) {
    noteEl.innerHTML = content;
  }
}

// Layers Drawer & Toggles
function setupLayersDrawer() {
  const drawer = document.getElementById('layers-drawer');
  const openBtn = document.getElementById('btn-toggle-layers');
  const closeBtn = document.getElementById('btn-close-layers');

  openBtn?.addEventListener('click', () => drawer?.classList.toggle('hidden'));
  closeBtn?.addEventListener('click', () => drawer?.classList.add('hidden'));

  // Basemap switcher
  document.querySelectorAll('.basemap-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.basemap-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const style = e.target.dataset.style;
      if (style === 'dark-esri') setBasemapStyle('dark-esri');
      else if (style === 'satellite') setBasemapStyle('satellite');
      else if (style === 'carto') setBasemapStyle('carto-dark');
    });
  });

  // Layer checkboxes
  setupLayerCheckbox('chk-layer-wells', layerWellsConv);
  setupLayerCheckbox('chk-layer-wells', layerWellsShale);
  setupLayerCheckbox('chk-layer-basins', layerBasins);
  setupLayerCheckbox('chk-layer-concessions', layerConcessions);
  setupLayerCheckbox('chk-layer-trajectories', layerTrajectories);
  setupLayerCheckbox('chk-layer-pipelines', layerPipelines);
  setupLayerCheckbox('chk-layer-facilities', layerFacilities);
  setupLayerCheckbox('chk-layer-flaring', layerFlaring);
}

function setupLayerCheckbox(chkId, layer) {
  const chk = document.getElementById(chkId);
  if (!chk) return;
  chk.addEventListener('change', (e) => {
    if (e.target.checked) {
      if (!map.hasLayer(layer)) map.addLayer(layer);
    } else {
      if (map.hasLayer(layer)) map.removeLayer(layer);
    }
  });
}

// Methodology Modal
function setupModal() {
  const modal = document.getElementById('modal-metodologia');
  const openBtn = document.getElementById('btn-metodologia');
  const closeBtn = document.getElementById('modal-metodologia-close');

  openBtn?.addEventListener('click', () => modal?.classList.remove('hidden'));
  closeBtn?.addEventListener('click', () => modal?.classList.add('hidden'));
}

// DOM Ready Init
document.addEventListener('DOMContentLoaded', initScrollyPlatform);
'''

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js_content)

print("Generated frontend/app.js successfully!")
