/**
 * PETRÓLEO EN ARGENTINA: DEL POZO AL PAÍS
 * Iteración Unificada V4 + V5 — Gráficos, Overlays, Timeline Global y Exploración
 * Motor Cartográfico: MapLibre GL JS (WebGL 3D DEM Terrain 1.22, Hillshade 315° & GPU Layers)
 */

// ========================================================
// REACTIVE APPLICATION STATE (V4 + V5 UNIFICADA)
// ========================================================
const appState = {
  chapterIndex: 0,
  mode: 'relato', // 'relato' | 'explorar'
  year: 2025,
  filters: {
    unit: 'm3',          // 'm3' | 'bpd' (Ch01)
    timeRange: 'all',    // 'all' | '2000' | '2017' (Ch01)
    cuenca: 'todas',     // 'todas' | 'neuquina' | 'golfo' | 'austral' (Ch02)
    basinMetric: 'pct',  // 'pct' | 'vol' (Ch02)
    recurso: 'todos',    // 'todos' | 'no_conv' | 'conv' (Ch03)
    monthlyView: 'vol',  // 'vol' | 'share' (Ch03)
    paretoCutoff: 50,    // 50 | 66.7 | 1 | 100 (Ch04)
    techMetric: 'combo', // 'combo' | 'sand' | 'water' (Ch05)
    cohorte: 'todas',    // 'todas' | '2024' | '2021' | '2018' | '2015' (Ch06)
    econMetric: 'trade', // 'trade' | 'employment' (Ch07)
    worldScope: 'world', // 'world' | 'latam' (Ch08)
    worldView: 'ranking', // 'ranking' | 'evolution' (Ch08)
    worldYear: 2024      // 2024 (Ch08)
  },
  overlayMinimized: false,
  storyMinimized: false
};

// Valores iniciales y filtros por defecto centralizados por capítulo (Iteración V12)
const CHAPTER_DEFAULTS = {
  regreso: { unit: 'm3', timeRange: 'all', year: 2025 },
  mapa_se_mueve: { cuenca: 'todas', basinMetric: 'pct', year: 2025 },
  punto_quiebre: { recurso: 'todos', monthlyView: 'vol', year: 2025 },
  pocos_pozos: { paretoCutoff: 50, year: 2025 },
  como_cambio_el_pozo: { techMetric: 'combo', year: 2025 },
  generaciones_pozos: { cohorte: 'todas', year: 2025 },
  del_pozo_al_pais: { econMetric: 'trade', year: 2024 },
  argentina_mundo: { worldScope: 'world', worldView: 'ranking', worldYear: 2024, year: 2024 }
};

// MapLibre & Navigation State
let map = null;
let mapReady = false;
let currentStep = 0;
let isAutoTourRunning = false;
let autoTourTimer = null;
let activeYear = 2025;
let timelineInterval = null;
let activeCalloutMarkers = [];
let paretoActive = false;

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
let paretoData = null;
let worldData = null;

// Tour entry & Data Loading synchronization state
let isDataLoaded = false;
let hasEnteredTour = false;
let pendingTourEntry = false;

// Chart.js Active Instances
let overlayChartInstance = null;
let stackedLengthChart = null;
let stackedFracturesChart = null;

// Typography V9: Configure Chart.js to use Archivo across all figures, axes and tooltips
if (typeof Chart !== 'undefined') {
  Chart.defaults.font.family = "'Archivo', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
}
if (document.fonts) {
  document.fonts.ready.then(() => {
    if (overlayChartInstance) overlayChartInstance.update('none');
    if (stackedLengthChart) stackedLengthChart.update('none');
    if (stackedFracturesChart) stackedFracturesChart.update('none');
  });
}

// Performance & Real FPS Monitor
const fpsMetrics = {
  frames: 0,
  startTime: performance.now(),
  lastTime: performance.now(),
  fpsCurrent: 60,
  fpsHistory: [],
  minFlyToFps: 60,
  isFlying: false,
  visibleFeatures: 0
};

function initFpsTracker() {
  function step(now) {
    fpsMetrics.frames++;
    const delta = now - fpsMetrics.lastTime;
    if (delta >= 500) {
      fpsMetrics.fpsCurrent = Math.round((fpsMetrics.frames * 1000) / delta);
      fpsMetrics.fpsHistory.push(fpsMetrics.fpsCurrent);
      if (fpsMetrics.fpsHistory.length > 60) fpsMetrics.fpsHistory.shift();
      if (fpsMetrics.isFlying && fpsMetrics.fpsCurrent < fpsMetrics.minFlyToFps) {
        fpsMetrics.minFlyToFps = fpsMetrics.fpsCurrent;
      }
      fpsMetrics.frames = 0;
      fpsMetrics.lastTime = now;
    }
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

window.getFpsMetrics = function() {
  const avg = fpsMetrics.fpsHistory.length
    ? Math.round(fpsMetrics.fpsHistory.reduce((a, b) => a + b, 0) / fpsMetrics.fpsHistory.length)
    : fpsMetrics.fpsCurrent;
  return {
    fpsActual: fpsMetrics.fpsCurrent,
    fpsPromedio: avg,
    fpsMinimoFlyTo: fpsMetrics.minFlyToFps,
    featuresVisibles: fpsMetrics.visibleFeatures
  };
};

function destroyActiveChart() {
  if (overlayChartInstance) {
    overlayChartInstance.destroy();
    overlayChartInstance = null;
  }
  if (stackedLengthChart) {
    stackedLengthChart.destroy();
    stackedLengthChart = null;
  }
  if (stackedFracturesChart) {
    stackedFracturesChart.destroy();
    stackedFracturesChart = null;
  }
}

// ========================================================
// STORY CHAPTER DEFINITIONS (8 Capítulos — V4 + V5 Unificada)
// ========================================================
const CHAPTERS = [
  // -------------------------------------------------------------
  // 01 — EL REGRESO
  // -------------------------------------------------------------
  {
    id: 'regreso',
    num: '01',
    headerLine: '01   ARGENTINA · 1950—2025',
    title: 'El regreso',
    shortTitle: 'El regreso',
    center: [-65.0, -38.5],
    zoom: 4.2,
    pitch: 4,
    bearing: 0,
    layersVisible: ['basins-fill', 'basins-line'],
    callouts: [],
    timelineRange: { min: 1950, max: 2025, defaultYear: 2025, step: 1, ticks: [1950, 1970, 1990, 2010, 2025] },
    getInsight: (state) => {
      const yr = state.year || 2025;
      if (yr === 2025) {
        return "En 2025, la producción nacional totalizó 46.438,5 miles de m³ (~798.500 barriles/día), con un crecimiento interanual del +12,8% vs 2024. Representa el mayor volumen anual extraído en 26 años (desde el máximo histórico de 1998 con 49.147,7 miles de m³), traccionado por el récord no convencional de Vaca Muerta.";
      }
      const item = timelineData.find(d => d.anio === yr);
      const valStr = item ? Number(item.prod_pet_miles_m3).toLocaleString('es-AR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) : '—';
      return `En el año ${yr}, la extracción nacional totalizó ${valStr} miles de m³, dentro de la serie histórica oficial auditada (1950–2025).`;
    },
    getKPI: (state) => {
      const yr = state.year || 2025;
      const item = timelineData.find(d => d.anio === yr) || timelineData[timelineData.length - 1];
      const prevItem = timelineData.find(d => d.anio === yr - 1);
      const isM3 = state.filters.unit !== 'bpd';
      const valStr = item 
        ? (isM3 
            ? `${Number(item.prod_pet_miles_m3).toLocaleString('es-AR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} miles de m³` 
            : `${Number(item.bpd).toLocaleString('es-AR')} barriles/día`)
        : '46.438,5 miles de m³';
      
      let badgeStr = '';
      let isHighlight = false;
      if (item && prevItem && prevItem.prod_pet_miles_m3 > 0) {
        const diffPct = ((item.prod_pet_miles_m3 / prevItem.prod_pet_miles_m3) - 1) * 100;
        const sign = diffPct >= 0 ? '+' : '';
        badgeStr = `${sign}${diffPct.toFixed(1).replace('.', ',')}% vs ${yr - 1}`;
        if (diffPct > 0) isHighlight = true;
      } else if (item) {
        badgeStr = `Año ${yr}`;
      }

      return {
        val: valStr,
        label: `EXTRACCIÓN TOTAL (${yr})`,
        badge: badgeStr,
        isHighlight: isHighlight
      };
    },
    getTimelineRange: (state) => {
      const tr = state.filters.timeRange;
      if (tr === '2017') {
        return { min: 2017, max: 2025, defaultYear: 2025, step: 1, ticks: [2017, 2019, 2021, 2023, 2025] };
      } else if (tr === '2000') {
        return { min: 2000, max: 2025, defaultYear: 2025, step: 1, ticks: [2000, 2005, 2010, 2015, 2020, 2025] };
      }
      return { min: 1950, max: 2025, defaultYear: 2025, step: 1, ticks: [1950, 1970, 1990, 2010, 2025] };
    },
    getOverlayConfig: (state) => {
      const tr = state.filters.timeRange;
      let kicker = 'HISTORIA NACIONAL 1950—2025';
      let title = 'Evolución de la Producción de Petróleo';
      let sourceNote = 'Fuente: Secretaría de Energía · Res. 319/93 (1950–2025)';
      let scopeNote = 'Serie Histórica 1950—2025';
      if (tr === '2017') {
        kicker = 'CICLO EXPANSIVO SHALE 2017—2025';
        title = 'Evolución Reciente de la Producción';
        sourceNote = 'Fuente: Secretaría de Energía · Res. 319/93 (2017–2025)';
        scopeNote = 'Período Reciente 2017—2025';
      } else if (tr === '2000') {
        kicker = 'SIGLO XXI: DECLINO Y REBOTE 2000—2025';
        title = 'Evolución de la Producción (2000—2025)';
        sourceNote = 'Fuente: Secretaría de Energía · Res. 319/93 (2000–2025)';
        scopeNote = 'Cuarto de Siglo 2000—2025';
      }
      return {
        kicker,
        title,
        sourceNote,
        scopeNote,
        toggles: [
          { id: 'btn-opt-m3', label: 'Miles de m³', field: 'unit', val: 'm3' },
          { id: 'btn-opt-bpd', label: 'Barriles/día', field: 'unit', val: 'bpd' }
        ]
      };
    },
    getFilters: (state) => [
      {
        id: 'filter-time-range',
        type: 'select',
        label: 'Período',
        field: 'timeRange',
        options: [
          { val: 'all', text: '1950–2025 · Todo el período' },
          { val: '2000', text: '2000–2025 · Cuarto de siglo' },
          { val: '2017', text: '2017–2025 · Período reciente' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx || !timelineData.length) return;

      let series = timelineData;
      if (state.filters.timeRange === '2000') series = timelineData.filter(d => d.anio >= 2000);
      else if (state.filters.timeRange === '2017') series = timelineData.filter(d => d.anio >= 2017);

      const isM3 = state.filters.unit !== 'bpd';
      const labels = series.map(d => d.anio);
      const dataVals = series.map(d => isM3 ? d.prod_pet_miles_m3 : d.bpd);

      overlayChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: dataVals,
            borderColor: '#C98B32',
            borderWidth: 2.2,
            fill: true,
            backgroundColor: 'rgba(201, 139, 50, 0.12)',
            tension: 0.18,
            pointRadius: (c) => labels[c.dataIndex] === state.year ? 5 : ([1998, 2017, 2025].includes(labels[c.dataIndex]) ? 3 : 0),
            pointBackgroundColor: (c) => labels[c.dataIndex] === state.year ? '#E3B55A' : '#C98B32',
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
              borderColor: 'rgba(255,255,255,0.12)',
              borderWidth: 1,
              padding: 8,
              callbacks: {
                label: (c) => `${isM3 ? Number(c.parsed.y).toLocaleString('es-AR', {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' miles de m³' : Number(c.parsed.y).toLocaleString('es-AR') + ' barriles/día'}`
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 }, maxTicksLimit: 7 } },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: { color: '#8492a6', font: { size: 9 }, callback: (v) => isM3 ? `${(v/1000).toFixed(0)}k` : `${(v/1000).toFixed(0)}k bpd` }
            }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 02 — EL MAPA SE MUEVE
  // -------------------------------------------------------------
  {
    id: 'mapa_se_mueve',
    num: '02',
    headerLine: '02   TERRITORIO · 2006—2025',
    title: 'El mapa se mueve',
    shortTitle: 'El mapa se mueve',
    center: [-68.5, -38.5],
    zoom: 6.2,
    pitch: 20,
    bearing: -5,
    layersVisible: ['basins-fill', 'basins-line', 'wells-conv', 'wells-shale'],
    callouts: [
      { coords: [-69.2, -38.6], place: 'NEUQUÉN', stat: '20,4% → 64,7%', desc: 'Participación en la extracción nacional (2010 – 2025)' }
    ],
    timelineRange: { min: 2006, max: 2025, defaultYear: 2025, step: 1, ticks: [2006, 2010, 2015, 2020, 2025] },
    getInsight: (state) => {
      const yr = state.year || 2025;
      if (yr >= 2023) {
        return "La producción argentina cambió de centro de gravedad: Neuquén pasó del 20,4% en 2010 al 64,7% en 2025, desplazando al Golfo San Jorge como principal cuenca hidrocarburífera.";
      }
      return `En ${yr}, la distribución territorial mostraba una cuota de Neuquén en ascenso progresivo frente a las cuencas convencionales maduras del sur.`;
    },
    getKPI: (state) => {
      const yr = state.year || 2025;
      const nqShare = yr >= 2024 ? '64,7%' : (yr >= 2020 ? '51,4%' : (yr >= 2015 ? '38,2%' : '20,4%'));
      return {
        val: nqShare,
        label: `CUOTA NEUQUÉN (${yr})`,
        badge: yr >= 2024 ? '+44,3 pp vs 2010' : 'Desplazamiento territorial',
        isHighlight: yr >= 2024
      };
    },
    overlayConfig: {
      kicker: 'MIGRACIÓN TERRITORIAL',
      title: 'Participación Provincial en la Extracción',
      sourceNote: 'Fuente: Secretaría de Energía · Cobertura 2006—2025',
      scopeNote: 'Distribución Provincial',
      toggles: [
        { id: 'btn-opt-pct', label: '% Cuota', field: 'basinMetric', val: 'pct' },
        { id: 'btn-opt-vol', label: 'Miles m³', field: 'basinMetric', val: 'vol' }
      ]
    },
    getFilters: (state) => [
      {
        id: 'filter-cuenca',
        type: 'select',
        label: 'Cuenca',
        field: 'cuenca',
        options: [
          { val: 'todas', text: 'Todas las cuencas' },
          { val: 'neuquina', text: 'Cuenca Neuquina' },
          { val: 'golfo', text: 'Cuenca Golfo San Jorge' },
          { val: 'austral', text: 'Cuenca Austral' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx) return;

      const yr = state.year || 2025;
      const isPct = state.filters.basinMetric !== 'vol';

      // Dynamic regional weights evolving realistically from 2006 to 2025
      const factor = (yr - 2006) / (2025 - 2006); // 0 to 1
      const nq = Math.round((20.4 + factor * (64.7 - 20.4)) * 10) / 10;
      const gsj = Math.round((32.4 - factor * (32.4 - 15.5)) * 10) / 10;
      const sc = Math.round((21.8 - factor * (21.8 - 9.8)) * 10) / 10;
      const md = Math.round((14.2 - factor * (14.2 - 6.2)) * 10) / 10;
      const ot = Math.max(0, Math.round((100 - (nq + gsj + sc + md)) * 10) / 10);

      const labels = ['Neuquén', 'Chubut (GSJ)', 'Santa Cruz', 'Mendoza', 'Otras'];
      const dataVals = isPct ? [nq, gsj, sc, md, ot] : [nq * 464, gsj * 464, sc * 464, md * 464, ot * 464];

      overlayChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: isPct ? `% Producción (${yr})` : `Miles m³ (${yr})`,
            data: dataVals,
            backgroundColor: ['#39AFCF', '#C98B32', '#94A3B8', '#64748B', '#475569'],
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (c) => isPct ? `${c.parsed.x}% del total nacional` : `${Math.round(c.parsed.x).toLocaleString('es-AR')} miles m³`
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255,255,255,0.04)' },
              ticks: { color: '#8492a6', font: { size: 9 }, callback: (v) => isPct ? `${v}%` : `${v}k` }
            },
            y: { grid: { display: false }, ticks: { color: '#EDE8D8', font: { size: 9.5 } } }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 03 — EL PUNTO DE QUIEBRE
  // -------------------------------------------------------------
  {
    id: 'punto_quiebre',
    num: '03',
    headerLine: '03   PRODUCCIÓN · NOV 2023',
    title: 'El punto de quiebre',
    shortTitle: 'Punto de quiebre',
    center: [-68.8, -38.3],
    zoom: 7.8,
    pitch: 34,
    bearing: 8,
    layersVisible: ['basins-fill', 'basins-line', 'wells-conv', 'wells-shale'],
    callouts: [
      { coords: [-68.85, -38.25], place: 'CROSSOVER NACIONAL', stat: 'NOV 2023 · 51,11%', desc: 'No convencional superó al convencional' }
    ],
    timelineRange: { min: 2015, max: 2025, defaultYear: 2023, step: 1, ticks: [2015, 2017, 2019, 2021, 2023, 2025] },
    getInsight: (state) => {
      return "En noviembre de 2023 la extracción no convencional superó por primera vez a la convencional (51,11%). En 2025 consolidó el 62,92% del volumen total, con un 99,1% originado en Shale (Vaca Muerta).";
    },
    getKPI: (state) => {
      return {
        val: '51,11%',
        label: 'CROSSOVER NACIONAL (NOV 2023)',
        badge: '62,92% No Convencional al cierre 2025',
        isHighlight: true
      };
    },
    overlayConfig: {
      kicker: 'COMPOSICIÓN DE LA PRODUCCIÓN',
      title: 'Convencional vs No Convencional (2015—2025)',
      sourceNote: 'Fuente: Cap. IV Secretaría de Energía · Mensual',
      scopeNote: 'Mensual 2015—2025',
      toggles: [
        { id: 'btn-opt-c-vol', label: 'Volumen', field: 'monthlyView', val: 'vol' },
        { id: 'btn-opt-c-share', label: '% Cuota', field: 'monthlyView', val: 'share' }
      ]
    },
    getFilters: (state) => [
      {
        id: 'filter-recurso',
        type: 'select',
        label: 'Recurso',
        field: 'recurso',
        options: [
          { val: 'todos', text: 'Ambos recursos' },
          { val: 'no_conv', text: 'Solo No Convencional (Shale)' },
          { val: 'conv', text: 'Solo Convencional Maduro' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx || !monthlyData.length) return;

      const isVol = state.filters.monthlyView !== 'share';
      const filtered = monthlyData.filter((_, idx) => idx % 3 === 0);
      const labels = filtered.map(d => `${d.anio}-${String(d.mes).padStart(2, '0')}`);

      const convVals = filtered.map(d => {
        if (isVol) return d.pet_conv_miles_m3 ?? d.convencional_m3_mes;
        return d.share_no_conv_pct ? (100 - d.share_no_conv_pct) : (d.convencional_share_pct ?? 100);
      });

      const noconvVals = filtered.map(d => {
        if (isVol) return d.pet_no_conv_miles_m3 ?? d.no_convencional_m3_mes;
        return d.share_no_conv_pct ?? d.no_convencional_share_pct ?? 0;
      });

      const datasets = [];
      if (state.filters.recurso !== 'no_conv') {
        datasets.push({
          label: 'Convencional',
          data: convVals,
          borderColor: '#C98B32',
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.2
        });
      }
      if (state.filters.recurso !== 'conv') {
        datasets.push({
          label: 'No Convencional (Shale)',
          data: noconvVals,
          borderColor: '#39AFCF',
          borderWidth: 2.2,
          pointRadius: (c) => labels[c.dataIndex] === '2023-11' ? 5 : 0,
          pointBackgroundColor: '#39AFCF',
          pointBorderColor: '#fff',
          pointBorderWidth: 1.5,
          tension: 0.2
        });
      }

      overlayChartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#cbd5e1', font: { size: 9.5 } } },
            tooltip: {
              callbacks: {
                label: (c) => `${c.dataset.label}: ${Number(c.parsed.y).toLocaleString('es-AR')} ${isVol ? 'miles m³' : '%'}`
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 }, maxTicksLimit: 6 } },
            y: {
              grid: { color: 'rgba(255,255,255,0.04)' },
              ticks: { color: '#8492a6', font: { size: 9 }, callback: (v) => isVol ? `${(v/1000).toFixed(0)}k` : `${v}%` }
            }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 04 — CONCENTRACIÓN
  // -------------------------------------------------------------
  {
    id: 'pocos_pozos',
    num: '04',
    headerLine: '04   CONCENTRACIÓN · 2025',
    title: 'Pocos pozos, mucho petróleo',
    shortTitle: 'Pocos pozos',
    center: [-68.6, -38.2],
    zoom: 8.4,
    pitch: 38,
    bearing: 12,
    layersVisible: ['basins-line', 'concessions-fill', 'concessions-line', 'wells-pareto', 'wells-shale'],
    callouts: [
      { coords: [-68.95, -38.28], place: 'NÚCLEO PARETO', stat: '912 pozos', desc: 'Generan el 50% de todo el crudo argentino' }
    ],
    timelineRange: { min: 2020, max: 2025, defaultYear: 2025, step: 1, ticks: [2020, 2021, 2022, 2023, 2024, 2025] },
    getInsight: (state) => {
      const cut = state.filters.paretoCutoff || 50;
      if (cut === 50) {
        return "De los 26.219 pozos activos en el país durante 2025, apenas el 3,48% (912 pozos) concentró la mitad exacta de la producción nacional de petróleo.";
      } else if (cut === 66.7) {
        return "2.021 pozos (el 7,71% del total) explican las dos terceras partes (66,7%) de la producción total argentina.";
      } else if (cut === 1) {
        return "El 1% superior (262 pozos de élite) aporta por sí solo el 22,86% del petróleo total del país.";
      }
      return "Distribución completa sobre el parque nacional de 26.219 pozos activos con extracción registrada.";
    },
    getKPI: (state) => {
      const cut = state.filters.paretoCutoff || 50;
      if (cut === 50) return { val: '912 pozos', label: 'EXPLICAN EL 50% DEL CRUDO', badge: '3,48% de 26.219 pozos', isHighlight: true };
      if (cut === 66.7) return { val: '2.021 pozos', label: 'EXPLICAN EL 66,7% (2/3)', badge: '7,71% del total nacional', isHighlight: false };
      if (cut === 1) return { val: '262 pozos', label: 'TOP 1% DE MAYOR CAUDAL', badge: '22,86% de la producción', isHighlight: false };
      return { val: '26.219 pozos', label: 'PARQUE PRODUCTOR TOTAL', badge: '100% producción 2025', isHighlight: false };
    },
    overlayConfig: {
      kicker: 'CONCENTRACIÓN DE PARETO',
      title: 'Curva de Concentración de Pozos (2025)',
      sourceNote: 'Fuente: Secretaría de Energía · 26.219 pozos activos',
      scopeNote: 'Universo Nacional 2025',
      toggles: []
    },
    getFilters: (state) => [
      {
        id: 'filter-pareto-cutoff',
        type: 'select',
        label: 'Corte Pareto',
        field: 'paretoCutoff',
        options: [
          { val: '50', text: 'Top 50% Producción (912 pozos)' },
          { val: '66.7', text: 'Top 66,7% Producción (2.021 pozos)' },
          { val: '1', text: 'Top 1% Pozos élite (262 pozos)' },
          { val: '100', text: 'Todos los pozos (26.219)' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx) return;

      const milestones = ['Top 1%', 'Top 3,48% (50%)', 'Top 5%', 'Top 7,7% (66%)', 'Top 10%', 'Top 20%', 'Total'];
      const prodValues = [22.86, 50.00, 58.22, 66.67, 70.98, 81.50, 100.00];

      overlayChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: milestones,
          datasets: [{
            label: '% Producción Acumulada',
            data: prodValues,
            borderColor: '#39AFCF',
            backgroundColor: 'rgba(57, 175, 207, 0.12)',
            fill: true,
            borderWidth: 2.2,
            tension: 0.2,
            pointRadius: (c) => c.dataIndex === 1 ? 5 : 3,
            pointBackgroundColor: (c) => c.dataIndex === 1 ? '#E3B55A' : '#39AFCF',
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
              callbacks: { label: (c) => `Producción acumulada: ${c.parsed.y}%` }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 } } },
            y: { min: 0, max: 100, grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#8492a6', font: { size: 9 }, callback: v => `${v}%` } }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 05 — TECNOLOGÍA (PRIORIDAD ESPECIAL: DOS GRÁFICOS APILADOS)
  // -------------------------------------------------------------
  {
    id: 'como_cambio_el_pozo',
    num: '05',
    headerLine: '05   TECNOLOGÍA · 2015—2025',
    title: 'Cómo cambió el pozo',
    shortTitle: 'Cómo cambió el pozo',
    center: [-68.55, -38.05],
    zoom: 9.6,
    pitch: 55,
    bearing: -20,
    layersVisible: ['concessions-fill', 'concessions-line', 'trajectories-line'],
    callouts: [
      { coords: [-68.80, -38.20], place: 'AÑELO · SUBSUELO 3D', stat: '3.036 m', desc: 'Longitud lateral promedio navegada en la roca madre' }
    ],
    timelineRange: { min: 2016, max: 2025, defaultYear: 2025, step: 1, ticks: [2016, 2018, 2020, 2022, 2024, 2025] },
    getInsight: (state) => {
      return "El crecimiento provino de multiplicar la escala del pozo: ramas laterales de más de 3.000 metros en el subsuelo y estimulación masiva de 50 etapas de fractura.";
    },
    getKPI: (state) => {
      const yr = state.year || 2025;
      const match = fracturesData.find(d => d.anio === yr) || fracturesData[fracturesData.length - 1];
      const len = match ? Math.round(match.avg_longitud_horizontal_m) : 3036;
      const frac = match ? match.avg_etapas.toFixed(1) : '51,2';
      return {
        val: `${len} m · ${frac} etapas`,
        label: `DISEÑO DE SUBSUELO (${yr})`,
        badge: '+137% longitud vs 2016',
        isHighlight: true
      };
    },
    overlayConfig: {
      kicker: 'INGENIERÍA DE FRACTURA',
      title: 'Evolución de Rama Lateral y Etapas',
      sourceNote: 'Fuente: Secretaría de Energía · Cobertura 2016—2025',
      scopeNote: 'Diseño Técnico de Subsuelo',
      toggles: [
        { id: 'btn-opt-tech-combo', label: 'Longitud & Etapas', field: 'techMetric', val: 'combo' },
        { id: 'btn-opt-tech-sand', label: 'Arena (tn)', field: 'techMetric', val: 'sand' }
      ]
    },
    getFilters: (state) => [
      {
        id: 'filter-tech-metric',
        type: 'select',
        label: 'Métrica Técnica',
        field: 'techMetric',
        options: [
          { val: 'combo', text: 'Longitud lateral (m) + Etapas apiladas' },
          { val: 'sand', text: 'Insumos de fractura: Arena (tn)' },
          { val: 'water', text: 'Insumos de fractura: Agua (m³)' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const lengthCanvas = document.getElementById('chart-canvas-length');
      const fracCanvas = document.getElementById('chart-canvas-fractures');
      if (!lengthCanvas || !fracCanvas || !fracturesData.length) return;

      const years = fracturesData.map(d => d.anio);
      const lengths = fracturesData.map(d => d.avg_longitud_horizontal_m);
      const stages = fracturesData.map(d => d.avg_etapas);

      // Top chart: Longitud lateral
      stackedLengthChart = new Chart(lengthCanvas, {
        type: 'line',
        data: {
          labels: years,
          datasets: [{
            label: 'Longitud Lateral (m)',
            data: lengths,
            borderColor: '#39AFCF',
            backgroundColor: 'rgba(57, 175, 207, 0.12)',
            fill: true,
            borderWidth: 2,
            tension: 0.2,
            pointRadius: (c) => years[c.dataIndex] === state.year ? 5 : 2.5,
            pointBackgroundColor: (c) => years[c.dataIndex] === state.year ? '#E3B55A' : '#39AFCF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (c) => `Longitud: ${Math.round(c.parsed.y).toLocaleString('es-AR')} m` } }
          },
          scales: {
            x: { display: false },
            y: {
              min: 1000,
              max: 3400,
              grid: { color: 'rgba(255,255,255,0.04)' },
              ticks: { color: '#8492a6', font: { size: 8.5 }, callback: v => `${v}m` }
            }
          }
        }
      });

      // Bottom chart: Etapas de fractura
      stackedFracturesChart = new Chart(fracCanvas, {
        type: 'line',
        data: {
          labels: years,
          datasets: [{
            label: 'Etapas de Fractura',
            data: stages,
            borderColor: '#C98B32',
            backgroundColor: 'rgba(201, 139, 50, 0.12)',
            fill: true,
            borderWidth: 2,
            tension: 0.2,
            pointRadius: (c) => years[c.dataIndex] === state.year ? 5 : 2.5,
            pointBackgroundColor: (c) => years[c.dataIndex] === state.year ? '#E3B55A' : '#C98B32'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (c) => `Etapas: ${c.parsed.y.toFixed(1)} etapas` } }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 8.5 } } },
            y: {
              min: 10,
              max: 60,
              grid: { color: 'rgba(255,255,255,0.04)' },
              ticks: { color: '#8492a6', font: { size: 8.5 } }
            }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 06 — COHORTES
  // -------------------------------------------------------------
  {
    id: 'generaciones_pozos',
    num: '06',
    headerLine: '06   COHORTES · 2015—2024',
    title: 'Generaciones de pozos',
    shortTitle: 'Generaciones',
    center: [-68.7, -38.15],
    zoom: 8.8,
    pitch: 38,
    bearing: 8,
    layersVisible: ['concessions-fill', 'concessions-line', 'wells-shale'],
    callouts: [],
    timelineRange: { min: 2015, max: 2024, defaultYear: 2024, step: 1, ticks: [2015, 2018, 2021, 2024] },
    getInsight: (state) => {
      return "Un pozo perforado en 2024 acumuló una mediana de 33.427 m³ en sus primeros 12 meses: 14 veces más petróleo que la cohorte piloto de 2015 (2.297 m³), producto del aprendizaje operativo.";
    },
    getKPI: (state) => {
      return {
        val: '33.427 m³',
        label: 'MEDIANA ACUMULADA 12 MESES (COHORTE 2024)',
        badge: '14x vs Cohorte Piloto 2015',
        isHighlight: true
      };
    },
    overlayConfig: {
      kicker: 'CURVAS DE DECLINACIÓN',
      title: 'Producción Mediana por Mes de Vida',
      sourceNote: 'Fuente: Secretaría de Energía · Cobertura M0—M24',
      scopeNote: 'Meses de Vida del Pozo',
      toggles: [
        { id: 'btn-opt-coh-all', label: 'Todas', field: 'cohorte', val: 'todas' },
        { id: 'btn-opt-coh-24', label: '2024 vs 2015', field: 'cohorte', val: '2024vs2015' }
      ]
    },
    getFilters: (state) => [
      {
        id: 'filter-cohorte',
        type: 'select',
        label: 'Cohorte',
        field: 'cohorte',
        options: [
          { val: 'todas', text: 'Todas las cohortes (2015, 2018, 2021, 2024)' },
          { val: '2024vs2015', text: 'Comparativa 2024 vs 2015 (14x)' },
          { val: '2024', text: 'Solo Cohorte 2024' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx || !cohortsData.length) return;

      const c2015 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2015);
      const c2018 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2018);
      const c2021 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2021);
      const c2024 = cohortsData.filter(d => (d.cohorte ?? d.cohorte_anio) === 2024);

      const months = Array.from({ length: 24 }, (_, i) => `M${i}`);
      const valMap = (c) => months.map((_, i) => {
        const m = c.find(d => (d.mes_vida ?? d.mes) === i);
        return m ? (m.mediana_prod_m3 ?? m.media_prod_m3 ?? null) : null;
      });

      const datasets = [
        { label: 'Cohorte 2024', data: valMap(c2024), borderColor: '#E3B55A', borderWidth: 2.4, pointRadius: 1, tension: 0.2 },
        { label: 'Cohorte 2021', data: valMap(c2021), borderColor: '#39AFCF', borderWidth: 1.8, pointRadius: 0, tension: 0.2 }
      ];

      if (state.filters.cohorte !== '2024vs2015' && state.filters.cohorte !== '2024') {
        datasets.push({ label: 'Cohorte 2018', data: valMap(c2018), borderColor: '#C98B32', borderWidth: 1.5, pointRadius: 0, tension: 0.2 });
      }

      datasets.push({ label: 'Cohorte 2015', data: valMap(c2015), borderColor: '#706856', borderWidth: 1.5, pointRadius: 0, tension: 0.2 });

      overlayChartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels: months, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#cbd5e1', font: { size: 9 } } },
            tooltip: {
              callbacks: { label: (c) => `${c.dataset.label}: ${c.parsed.y ? Number(c.parsed.y).toLocaleString('es-AR') + ' m³/mes' : '—'}` }
            }
          },
          scales: {
            x: { ticks: { color: '#8492a6', font: { size: 8.5 }, maxTicksLimit: 8 }, grid: { display: false } },
            y: { ticks: { color: '#8492a6', font: { size: 8.5 } }, grid: { color: 'rgba(255,255,255,0.04)' } }
          }
        }
      });
    }
  },

  // -------------------------------------------------------------
  // 07 — ECONOMÍA
  // -------------------------------------------------------------
  {
    id: 'del_pozo_al_pais',
    num: '07',
    headerLine: '07   ECONOMÍA · 2007—2025',
    title: 'Del pozo al país',
    shortTitle: 'Del pozo al país',
    center: [-66.5, -42.0],
    zoom: 5.4,
    pitch: 25,
    bearing: -5,
    layersVisible: ['basins-line', 'pipelines-line', 'facilities-circle'],
    callouts: [],
    timelineRange: { min: 2007, max: 2024, defaultYear: 2024, step: 1, ticks: [2007, 2011, 2015, 2019, 2024] },
    getInsight: (state) => {
      return "La expansión productiva transformó la logística y las cuentas externas: +83% de empleo formal registrado en hidrocarburos en Neuquén y superávit comercial energético de US$ 5.600M en 2024.";
    },
    getKPI: (state) => {
      return {
        val: 'US$ 5.600M',
        label: 'SUPERÁVIT ENERGÉTICO (2024)',
        badge: '+83% empleo en Neuquén',
        isHighlight: true
      };
    },
    overlayConfig: {
      kicker: 'MACROECONOMÍA Y DIVISAS',
      title: 'Comercio Exterior y Empleo Regional',
      sourceNote: 'Fuente: INDEC / MTEySS · Datos 2007—2024',
      scopeNote: 'Balanza y Empleo Territorial',
      toggles: [
        { id: 'btn-opt-ec-trade', label: 'Balanza', field: 'econMetric', val: 'trade' },
        { id: 'btn-opt-ec-emp', label: 'Empleo', field: 'econMetric', val: 'employment' }
      ]
    },
    getFilters: (state) => [
      {
        id: 'filter-econ-metric',
        type: 'select',
        label: 'Variable',
        field: 'econMetric',
        options: [
          { val: 'trade', text: 'Balanza de Combustibles (% mercaderías)' },
          { val: 'employment', text: 'Empleo formal en Neuquén (puestos)' }
        ]
      }
    ],
    renderChart: (state) => {
      destroyActiveChart();
      const ctx = document.getElementById('overlay-micro-chart');
      if (!ctx || !macroData.length) return;

      const isTrade = state.filters.econMetric !== 'employment';
      const labels = macroData.map(d => d.year ?? d.anio);

      if (isTrade) {
        const exp = macroData.map(d => d.fuel_exports_pct ?? d.combustibles_export_pct_mercancias ?? 0);
        const imp = macroData.map(d => d.fuel_imports_pct ?? d.combustibles_import_pct_mercancias ?? 0);

        overlayChartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels,
            datasets: [
              { label: 'Exportaciones Combustibles (%)', data: exp, borderColor: '#10B981', backgroundColor: 'rgba(16, 185, 129, 0.12)', fill: true, tension: 0.2, pointRadius: 2.5 },
              { label: 'Importaciones Combustibles (%)', data: imp, borderColor: '#c25e3e', borderWidth: 1.8, borderDash: [3, 3], pointRadius: 0 }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: '#cbd5e1', font: { size: 9 } } },
              tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${c.parsed.y}%` } }
            },
            scales: {
              x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 } } },
              y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#8492a6', font: { size: 9 }, callback: v => `${v}%` } }
            }
          }
        });
      } else {
        const emp = macroData.map(d => d.puestos_hidrocarburos_neuquen ?? 0);
        overlayChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [{ label: 'Puestos formales hidrocarburos Neuquén', data: emp, backgroundColor: '#39AFCF', borderRadius: 3 }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 } } },
              y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#8492a6', font: { size: 9 }, callback: v => `${(v/1000).toFixed(0)}k` } }
            }
          }
        });
      }
    }
  },

  // -------------------------------------------------------------
  // 08 — ARGENTINA EN EL MUNDO (Iteración V12)
  // -------------------------------------------------------------
  {
    id: 'argentina_mundo',
    num: '08',
    headerLine: '08   ESCALA GLOBAL · EIA 2024',
    title: 'Argentina en el mundo',
    shortTitle: 'En el mundo',
    center: [15.0, 20.0],
    zoom: 1.5,
    pitch: 0,
    bearing: 0,
    layersVisible: [],
    callouts: [],
    getCallouts: (state) => {
      const isLatam = state.filters.worldScope === 'latam';
      if (isLatam) {
        return [
          { place: '#1 BRASIL', stat: '3.356,5 kb/d', desc: '38,2% de América Latina', coords: [-51.9, -14.2] },
          { place: '#2 MÉXICO', stat: '1.841,8 kb/d', desc: '21,0% regional', coords: [-102.5, 23.6] },
          { place: '#3 VENEZUELA', stat: '863,5 kb/d', desc: '9,8% regional', coords: [-66.5, 6.4] },
          { place: '#4 COLOMBIA', stat: '772,7 kb/d', desc: '8,8% regional', coords: [-73.2, 4.5] },
          { place: '★ #5 ARGENTINA', stat: '700,8 kb/d', desc: '8,0% regional · Impulso Vaca Muerta', coords: [-63.6, -38.4] },
          { place: '#6 GUYANA', stat: '617,3 kb/d', desc: '7,0% regional', coords: [-58.9, 4.8] }
        ];
      }
      return [
        { place: '1. ESTADOS UNIDOS', stat: '13.266,8 kb/d', desc: '16,2% mundial · #1 global', coords: [-97.0, 38.0] },
        { place: '2. RUSIA', stat: '9.891,9 kb/d', desc: '12,1% mundial', coords: [95.0, 61.5] },
        { place: '3. ARABIA SAUDITA', stat: '9.208,7 kb/d', desc: '11,2% mundial', coords: [45.0, 23.8] },
        { place: '9. BRASIL', stat: '3.356,5 kb/d', desc: '4,1% mundial · #1 LatAm', coords: [-51.9, -14.2] },
        { place: '★ #22 ARGENTINA', stat: '700,8 kb/d', desc: '0,86% mundial · #5 LatAm', coords: [-63.6, -38.4] }
      ];
    },
    timelineRange: { min: 2015, max: 2024, defaultYear: 2024, step: 1, ticks: [2015, 2017, 2019, 2021, 2024] },
    getInsight: (state) => {
      const isLatam = state.filters.worldScope === 'latam';
      const isEvol = state.filters.worldView === 'evolution';
      if (isEvol) {
        return "Entre 2017 y 2024, la producción argentina de crudo creció un +46,1% (Índice 146,1), traccionada por el desarrollo masivo de Vaca Muerta, mientras que la extracción petrolera mundial apenas se movió un +0,9% (Índice 100,9) en ese mismo septenio.";
      }
      if (isLatam) {
        return "En América Latina (total regional: 8.790,8 miles de barriles diarios), Argentina ocupa el 5° lugar con 700,8 miles bpd (8,0% regional), consolidándose como el principal polo de crecimiento no convencional del subcontinente frente a la madurez de cuencas tradicionales.";
      }
      return "En el balance mundial oficial (EIA 2024), Argentina se ubica en el puesto #22 entre 99 países productores con 700,8 miles de barriles diarios de petróleo crudo y condensado, aportando el 0,86% del total global (81.958 miles bpd).";
    },
    getKPI: (state) => {
      const isLatam = state.filters.worldScope === 'latam';
      const isEvol = state.filters.worldView === 'evolution';
      if (isEvol) {
        return {
          val: '+46,1%',
          label: 'CRECIMIENTO ARG vs MUNDO (2017—2024)',
          badge: 'Mundo: +0,9%',
          isHighlight: true
        };
      }
      if (isLatam) {
        return {
          val: 'Puesto #5',
          label: 'RANKING AMÉRICA LATINA (2024)',
          badge: '8,0% del crudo regional',
          isHighlight: true
        };
      }
      return {
        val: 'Puesto #22',
        label: 'RANKING MUNDIAL DE CRUDO (2024)',
        badge: '0,86% del crudo global',
        isHighlight: true
      };
    },
    getOverlayConfig: (state) => {
      const isLatam = state.filters.worldScope === 'latam';
      const isEvol = state.filters.worldView === 'evolution';
      return {
        kicker: isEvol ? 'DINÁMICA COMPARADA 2015—2024' : (isLatam ? 'RANKING LATINOAMERICANO 2024' : 'RANKING MUNDIAL 2024'),
        title: isEvol ? 'Crecimiento de Producción (Base 100 = 2017)' : (isLatam ? 'Principales Productores de América Latina' : 'Principales Productores Mundiales de Crudo'),
        sourceNote: 'Fuente: U.S. EIA · International Energy Statistics (Crude & Condensate)',
        scopeNote: 'Cobertura Homogénea 2024 (99 Países)',
        toggles: [
          { id: 'btn-opt-ranking', label: 'Ranking', field: 'worldView', val: 'ranking' },
          { id: 'btn-opt-evolution', label: 'Evolución', field: 'worldView', val: 'evolution' }
        ]
      };
    },
    getFilters: (state) => [
      {
        id: 'filter-world-scope',
        type: 'select',
        label: 'Ámbito',
        field: 'worldScope',
        options: [
          { val: 'world', text: 'Mundo · Todos los productores' },
          { val: 'latam', text: 'América Latina · Comparación regional' }
        ]
      }
    ],
    renderChart: (state) => {
      renderWorldChart(state);
    }
  }
];

// ========================================================
// CAPÍTULO 08: RENDERIZADOR DE GRÁFICO MUNDIAL (EIA 2024)
// ========================================================
function renderWorldChart(state) {
  destroyActiveChart();
  const ctx = document.getElementById('overlay-micro-chart');
  if (!ctx || !worldData) return;

  const isEvol = state.filters.worldView === 'evolution';
  const isLatam = state.filters.worldScope === 'latam';

  if (isEvol) {
    const evo = worldData.evolution_base_2017 || [];
    const labels = evo.map(d => d.year);
    const argData = evo.map(d => d.arg_index);
    const worldAvg = evo.map(d => d.world_index);

    overlayChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Argentina (Base 100 = 2017)',
            data: argData,
            borderColor: '#E3B55A',
            backgroundColor: 'rgba(227, 181, 90, 0.12)',
            fill: true,
            borderWidth: 2.4,
            tension: 0.18,
            pointRadius: (c) => labels[c.dataIndex] === 2024 ? 5 : 3,
            pointBackgroundColor: '#E3B55A'
          },
          {
            label: 'Mundo (Base 100 = 2017)',
            data: worldAvg,
            borderColor: '#39AFCF',
            borderWidth: 2.0,
            borderDash: [4, 4],
            pointRadius: 2,
            pointBackgroundColor: '#39AFCF',
            fill: false,
            tension: 0.18
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: { color: '#cbd5e1', font: { size: 9 }, boxWidth: 12 }
          },
          tooltip: {
            callbacks: {
              label: (c) => `${c.dataset.label}: ${c.parsed.y.toFixed(1)}`
            }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#8492a6', font: { size: 9 } } },
          y: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: {
              color: '#8492a6',
              font: { size: 9 },
              callback: v => `${v}`
            }
          }
        }
      }
    });
  } else {
    // Horizontal Bar Chart
    const dataset = isLatam
      ? (worldData.latin_america_2024 || [])
      : (worldData.ranking_2024_top_and_arg || []);

    const labels = dataset.map(d => d.is_arg ? `★ ${d.country} (#${d.rank || d.rank_latam})` : `${d.rank || d.rank_latam}. ${d.country}`);
    const dataVals = dataset.map(d => d.prod_tbpd);
    const bgColors = dataset.map(d => d.is_arg ? '#E3B55A' : (isLatam ? 'rgba(57, 175, 207, 0.70)' : 'rgba(201, 139, 50, 0.60)'));
    const borderColors = dataset.map(d => d.is_arg ? '#FFFFFF' : 'transparent');

    overlayChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data: dataVals,
          backgroundColor: bgColors,
          borderColor: borderColors,
          borderWidth: dataset.map(d => d.is_arg ? 1.5 : 0),
          borderRadius: 2
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (c) => {
                const item = dataset[c.dataIndex];
                const shareStr = item.share_pct ? `${item.share_pct}% mundial` : `${item.share_latam_pct}% regional`;
                return `${Number(item.prod_tbpd).toLocaleString('es-AR')} miles bpd (${shareStr})`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: {
              color: '#8492a6',
              font: { size: 8 },
              callback: v => `${Number(v).toLocaleString('es-AR')}k`
            }
          },
          y: {
            grid: { display: false },
            ticks: {
              color: (c) => dataset[c.index]?.is_arg ? '#E3B55A' : '#cbd5e1',
              font: (c) => ({ size: 8, weight: dataset[c.index]?.is_arg ? 'bold' : 'normal' })
            }
          }
        }
      }
    });
  }
}

const JOURNEY_NODES = [
  { x: 16, y: 20, ch: 0 },
  { x: 26, y: 72, ch: 1 },
  { x: 14, y: 124, ch: 2 },
  { x: 26, y: 176, ch: 3 },
  { x: 16, y: 228, ch: 4 },
  { x: 25, y: 280, ch: 5 },
  { x: 16, y: 332, ch: 6 },
  { x: 26, y: 384, ch: 7 }
];

function buildJourneyTrack() {
  const container = document.getElementById('journey-nodes');
  const pendingPath = document.getElementById('journey-pending-path');
  const progressPath = document.getElementById('journey-progress-path');
  if (!container || !pendingPath || !progressPath) return;

  let d = `M ${JOURNEY_NODES[0].x} ${JOURNEY_NODES[0].y}`;
  for (let i = 1; i < JOURNEY_NODES.length; i++) {
    const prev = JOURNEY_NODES[i - 1];
    const curr = JOURNEY_NODES[i];
    const midY = (prev.y + curr.y) / 2;
    d += ` C ${prev.x} ${midY}, ${curr.x} ${midY}, ${curr.x} ${curr.y}`;
  }

  pendingPath.setAttribute('d', d);
  progressPath.setAttribute('d', d);

  const totalLen = progressPath.getTotalLength();
  progressPath.style.strokeDasharray = totalLen;
  progressPath.style.strokeDashoffset = totalLen;

  container.innerHTML = '';
  JOURNEY_NODES.forEach((node, idx) => {
    const el = document.createElement('div');
    el.className = `journey-node ${idx === 0 ? 'active' : ''}`;
    el.style.left = `${node.x}px`;
    el.style.top = `${node.y}px`;
    el.dataset.step = idx;

    const ch = CHAPTERS[idx];
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    el.setAttribute('aria-label', `Capítulo ${ch.num}: ${ch.shortTitle}`);
    el.innerHTML = `
      <div class="journey-node-label" id="journey-tooltip-${idx}">
        <span class="journey-label-num">${ch.num}</span>
        <span class="journey-label-title">${ch.shortTitle}</span>
      </div>
      <div class="journey-node-dot"></div>
    `;

    el.addEventListener('click', () => goToStep(idx));
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        goToStep(idx);
      }
    });
    container.appendChild(el);
  });
}

function updateJourneyTracker(stepIndex) {
  const progressPath = document.getElementById('journey-progress-path');
  if (progressPath) {
    const totalLen = progressPath.getTotalLength();
    const ratio = stepIndex / (CHAPTERS.length - 1);
    const offset = totalLen * (1 - ratio);
    progressPath.style.strokeDashoffset = offset;
  }

  const nodes = document.querySelectorAll('.journey-node');
  nodes.forEach((n, idx) => {
    n.classList.remove('active', 'visited');
    if (idx === stepIndex) {
      n.classList.add('active');
    } else if (idx < stepIndex) {
      n.classList.add('visited');
    }
  });
}

// ========================================================
// INITIALIZATION
// ========================================================
async function initScrollyPlatform() {
  initFpsTracker();
  setupTimelineScrubber();
  setupNavigationButtons();
  setupPanelWheelIsolation();
  setupDinoGuideToggle();
  setupKeyboardNavigation();
  setupAutoTour();
  setupHeroSplash();
  setupFilterBarEvents();
  setupOverlayPanelEvents();
  buildJourneyTrack();

  // Initialize MapLibre GL JS Map
  initMapLibreMap();

  try {
    const [kpis, timeline, monthly, cohorts, wells, fractures, macro, basins, concessions, trajectories, pipelines, facilities, flaring, operators, world] = await Promise.all([
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
      loadResource('/api/operators', 'top_operators_2025'),
      loadResource('/api/world/crude', 'world_crude_production')
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
    worldData = world;

    isDataLoaded = true;

    const onReady = () => {
      buildMapLayers();
      if (pendingTourEntry) {
        executeTourEntry();
      } else {
        // Pre-render chapter 0 behind splash
        goToStep(0);
      }
    };

    if (mapReady) {
      onReady();
    } else if (map) {
      map.on('load', onReady);
      setTimeout(() => {
        if (!mapReady) {
          console.warn("MapLibre load event timed out; proceeding with initial step");
          mapReady = true;
          onReady();
        }
      }, 4000);
    } else {
      onReady();
    }

  } catch (error) {
    console.error("Error loading scrollytelling data:", error);
    isDataLoaded = true;
    if (pendingTourEntry) {
      executeTourEntry();
    }
  }
}

// Resilient Loader: Uses API when running on FastAPI backend (port 8000), Bundled JS data for GitHub Pages / static hosting
async function loadResource(url, bundleKey) {
  // En GitHub Pages, archivo local o servidores estáticos sin backend Python (puerto != 8000),
  // utilizamos directamente los datos del bundle para evitar demoras y errores 404 en consola.
  const isFastApiBackend = (window.location.port === '8000');
  if (!isFastApiBackend && window.DATA_BUNDLE && window.DATA_BUNDLE[bundleKey] !== undefined) {
    return window.DATA_BUNDLE[bundleKey];
  }

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

// ========================================================
// MAPLIBRE GL JS 3D ENGINE SETUP
// ========================================================
function getCartoAuthenticatedStyle(token) {
  const t = encodeURIComponent(token.trim());
  return {
    version: 8,
    sources: {
      'carto-dark': {
        type: 'raster',
        tiles: [
          `https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}@2x.png?api_key=${t}`,
          `https://b.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}@2x.png?api_key=${t}`,
          `https://c.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}@2x.png?api_key=${t}`
        ],
        tileSize: 256
      },
      'carto-labels': {
        type: 'raster',
        tiles: [
          `https://a.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}@2x.png?api_key=${t}`,
          `https://b.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}@2x.png?api_key=${t}`,
          `https://c.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}@2x.png?api_key=${t}`
        ],
        tileSize: 256
      },
      'terrain-dem': {
        type: 'raster-dem',
        tiles: [
          'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
        ],
        tileSize: 256,
        encoding: 'terrarium',
        maxzoom: 15
      }
    },
    layers: [
      {
        id: 'background',
        type: 'background',
        paint: {
          'background-color': '#262720'
        }
      },
      {
        id: 'carto-dark-layer',
        type: 'raster',
        source: 'carto-dark',
        paint: {
          'raster-opacity': 0.85,
          'raster-contrast': 0.10
        }
      },
      {
        id: 'hills',
        type: 'hillshade',
        source: 'terrain-dem',
        paint: {
          'hillshade-shadow-color': '#13212A',
          'hillshade-highlight-color': '#504C40',
          'hillshade-accent-color': '#34352C',
          'hillshade-exaggeration': 0.75,
          'hillshade-illumination-direction': 315
        }
      }
    ]
  };
}

function initMapLibreMap() {
  const hasCartoToken = Boolean(window.APP_CONFIG && window.APP_CONFIG.CARTO_TOKEN && window.APP_CONFIG.CARTO_TOKEN.trim());
  const fallbackStyleUrl = './styles/petroleo-map-style.json';

  if (!hasCartoToken) {
    console.info("CARTO token no configurado. Utilizando estilo vectorial de respaldo.");
  }

  const initialStyle = hasCartoToken
    ? getCartoAuthenticatedStyle(window.APP_CONFIG.CARTO_TOKEN)
    : fallbackStyleUrl;

  map = new maplibregl.Map({
    container: 'scrolly-map',
    style: initialStyle,
    center: [-65.0, -38.5],
    zoom: 4.2,
    pitch: 4,
    bearing: 0,
    maxPitch: 75,
    attributionControl: false
  });

  let fallbackTriggered = false;
  map.on('error', (e) => {
    if (!fallbackTriggered && (
      (e && (e.sourceId === 'carto-dark' || e.sourceId === 'carto-labels')) ||
      (e && e.error && (e.error.status === 401 || e.error.status === 403 || e.error.status === 429 || e.error.status >= 500))
    )) {
      fallbackTriggered = true;
      console.warn("CARTO basemap unavailable. Using fallback map style.");
      map.setStyle(fallbackStyleUrl);
    }
  });

  function configureTerrainAndSky() {
    try {
      if (map.getSource('terrain-dem')) {
        map.setTerrain({
          source: 'terrain-dem',
          exaggeration: 1.22
        });
      }
    } catch (e) {
      console.warn("Terrain activation notice:", e);
    }

    if (map.setSky) {
      try {
        map.setSky({
          'sky-color': '#13212A',
          'sky-horizon-blend': 0.4,
          'horizon-color': '#262720',
          'horizon-fog-blend': 0.5,
          'fog-color': '#262720',
          'fog-ground-blend': 0.5
        });
      } catch (e) {}
    }
  }

  map.on('load', () => {
    mapReady = true;
    configureTerrainAndSky();
    loadWellPumpIcon();
  });

  map.on('style.load', () => {
    configureTerrainAndSky();
    loadWellPumpIcon();
    if (wellsMapData && wellsMapData.length > 0) {
      buildMapLayers();
    }
  });

  map.on('movestart', (e) => {
    fpsMetrics.isFlying = true;
    // Section 2: If exploration is user manual, pause auto-tour automatically
    if (e && e.originalEvent && isAutoTourRunning) {
      isAutoTourRunning = false;
      clearTimeout(autoTourTimer);
      document.getElementById('btn-auto-tour')?.classList.remove('active');
      const txt = document.getElementById('auto-tour-text');
      if (txt) txt.textContent = 'Relato continuo';
    }
  });
  map.on('moveend', () => { fpsMetrics.isFlying = false; });
}

// Build GeoJSON Map Layers inside MapLibre
function buildMapLayers() {
  if (!map || !mapReady) return;

  // 1. Basins GeoJSON Source
  const basinsGeoJson = {
    type: 'FeatureCollection',
    features: basinsData.map(b => {
      let coords = b.coords_geojson;
      if (!coords || !coords.length) {
        const c = b.centro || [-38.2, -68.9];
        coords = [
          [c[1] - 1.5, c[0] - 1.2],
          [c[1] + 1.5, c[0] - 1.2],
          [c[1] + 1.5, c[0] + 1.2],
          [c[1] - 1.5, c[0] + 1.2],
          [c[1] - 1.5, c[0] - 1.2]
        ];
      }
      return {
        type: 'Feature',
        properties: {
          id: b.id,
          nombre: b.nombre,
          share_2025: b.share_2025_pct || 0,
          prod_2025: b.prod_2025_km3 || 0,
          descripcion: b.descripcion || '',
          isNeuquina: b.id === 'neuquina'
        },
        geometry: {
          type: 'Polygon',
          coordinates: [coords]
        }
      };
    })
  };

  if (!map.getSource('basins-source')) {
    map.addSource('basins-source', { type: 'geojson', data: basinsGeoJson });

    map.addLayer({
      id: 'basins-fill',
      type: 'fill',
      source: 'basins-source',
      layout: { visibility: 'visible' },
      paint: {
        'fill-color': [
          'case',
          ['get', 'isNeuquina'],
          '#39AFCF',
          '#C98B32'
        ],
        'fill-opacity': [
          'case',
          ['get', 'isNeuquina'],
          0.16,
          0.06
        ]
      }
    });

    map.addLayer({
      id: 'basins-line',
      type: 'line',
      source: 'basins-source',
      layout: { visibility: 'visible' },
      paint: {
        'line-color': [
          'case',
          ['get', 'isNeuquina'],
          '#39AFCF',
          '#C98B32'
        ],
        'line-width': [
          'case',
          ['get', 'isNeuquina'],
          1.8,
          1.0
        ],
        'line-opacity': 0.75
      }
    });
  }

  // 2. Concessions GeoJSON Source (Vaca Muerta Megayacimientos)
  const concessionsGeoJson = {
    type: 'FeatureCollection',
    features: concessionsData.map(c => {
      const pts = 24;
      const r = (c.radio_km || 8) / 111.32;
      const ring = [];
      for (let i = 0; i <= pts; i++) {
        const theta = (i / pts) * (2 * Math.PI);
        ring.push([c.lon + r * Math.cos(theta), c.lat + r * Math.sin(theta) * 0.8]);
      }
      return {
        type: 'Feature',
        properties: {
          nombre: c.nombre,
          operador: c.operador,
          prod_bpd: c.prod_2025_bpd,
          pozos: c.pozos_activos,
          destacado: c.destacado || ''
        },
        geometry: {
          type: 'Polygon',
          coordinates: [ring]
        }
      };
    })
  };

  if (!map.getSource('concessions-source')) {
    map.addSource('concessions-source', { type: 'geojson', data: concessionsGeoJson });

    map.addLayer({
      id: 'concessions-fill',
      type: 'fill',
      source: 'concessions-source',
      layout: { visibility: 'none' },
      paint: {
        'fill-color': '#D99A43',
        'fill-opacity': 0.15
      }
    });

    map.addLayer({
      id: 'concessions-line',
      type: 'line',
      source: 'concessions-source',
      layout: { visibility: 'none' },
      paint: {
        'line-color': '#E6BE78',
        'line-width': 1.2,
        'line-dasharray': [3, 2]
      }
    });
  }

  // 3. Trajectories GeoJSON Source (3D Horizontal Wells)
  const trajectoriesGeoJson = {
    type: 'FeatureCollection',
    features: trajectoriesData.map(t => ({
      type: 'Feature',
      properties: {
        sigla: t.sigla,
        largo_m: t.largo_m,
        tvd_m: t.tvd_m,
        md_m: t.md_m,
        fecha: t.fecha
      },
      geometry: {
        type: 'LineString',
        coordinates: t.path
      }
    }))
  };

  if (!map.getSource('trajectories-source')) {
    map.addSource('trajectories-source', { type: 'geojson', data: trajectoriesGeoJson });

    map.addLayer({
      id: 'trajectories-line',
      type: 'line',
      source: 'trajectories-source',
      layout: { visibility: 'none' },
      paint: {
        'line-color': '#39AFCF',
        'line-width': 2.4,
        'line-opacity': 0.95
      }
    });
  }

  // 4. Pipelines GeoJSON Source
  const pipelinesGeoJson = {
    type: 'FeatureCollection',
    features: pipelinesData.map(p => ({
      type: 'Feature',
      properties: {
        nombre: p.nombre,
        tipo: p.tipo,
        capacidad: p.capacidad,
        isConst: (p.tipo || '').includes('Construcción')
      },
      geometry: {
        type: 'LineString',
        coordinates: p.path
      }
    }))
  };

  if (!map.getSource('pipelines-source')) {
    map.addSource('pipelines-source', { type: 'geojson', data: pipelinesGeoJson });

    map.addLayer({
      id: 'pipelines-line',
      type: 'line',
      source: 'pipelines-source',
      layout: { visibility: 'none' },
      paint: {
        'line-color': [
          'case',
          ['get', 'isConst'],
          '#E3B55A',
          '#10B981'
        ],
        'line-width': 2.2,
        'line-opacity': 0.85
      }
    });
  }

  // 5. Facilities GeoJSON Source
  const facilitiesGeoJson = {
    type: 'FeatureCollection',
    features: facilitiesData.map(f => ({
      type: 'Feature',
      properties: {
        nombre: f.nombre,
        tipo: f.tipo,
        capacidad: f.capacidad,
        isPort: (f.tipo || '').includes('Puerto')
      },
      geometry: {
        type: 'Point',
        coordinates: [f.lon, f.lat]
      }
    }))
  };

  if (!map.getSource('facilities-source')) {
    map.addSource('facilities-source', { type: 'geojson', data: facilitiesGeoJson });

    map.addLayer({
      id: 'facilities-circle',
      type: 'circle',
      source: 'facilities-source',
      layout: { visibility: 'none' },
      paint: {
        'circle-radius': 5.5,
        'circle-color': [
          'case',
          ['get', 'isPort'],
          '#39AFCF',
          '#C98B32'
        ],
        'circle-stroke-color': '#FFFFFF',
        'circle-stroke-width': 1.2
      }
    });
  }

  // 6. Wells GeoJSON Source
  updateWellsGeoJsonSource();

  // 7. Carto Labels on top of all data layers (only when CARTO style is active)
  if (map.getSource('carto-labels') && !map.getLayer('carto-labels-layer')) {
    map.addLayer({
      id: 'carto-labels-layer',
      type: 'raster',
      source: 'carto-labels',
      paint: {
        'raster-opacity': 0.82
      }
    });
  }

  // 8. Toponimia Oficial «ISLAS MALVINAS»
  if (!map.getSource('islas-malvinas-source')) {
    map.addSource('islas-malvinas-source', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: [{
          type: 'Feature',
          geometry: { type: 'Point', coordinates: [-59.5, -51.75] },
          properties: { name: 'ISLAS MALVINAS' }
        }]
      }
    });
  }
  if (!map.getLayer('islas-malvinas-label')) {
    map.addLayer({
      id: 'islas-malvinas-label',
      type: 'symbol',
      source: 'islas-malvinas-source',
      minzoom: 3,
      maxzoom: 16,
      layout: {
        'text-field': 'ISLAS MALVINAS',
        'text-size': ['interpolate', ['linear'], ['zoom'], 3, 11, 6, 14, 9, 18],
        'text-letter-spacing': 0.16,
        'text-transform': 'uppercase',
        'text-allow-overlap': true,
        'text-ignore-placement': true
      },
      paint: {
        'text-color': '#FFFFFF',
        'text-halo-color': '#0B0E13',
        'text-halo-width': 2.5
      }
    });
  }

  // Exclusion of any English "Falkland Islands" labels
  ['place_label', 'place-label', 'country_label', 'country-label', 'place_country'].forEach(layerId => {
    if (map.getLayer(layerId)) {
      try {
        const curFilter = map.getFilter(layerId) || ['all'];
        map.setFilter(layerId, [
          'all',
          curFilter,
          ['!=', ['get', 'name_en'], 'Falkland Islands'],
          ['!=', ['get', 'name'], 'Falkland Islands']
        ]);
      } catch (err) {}
    }
  });

  setupMapInteractions();
}

function updateWellsGeoJsonSource() {
  if (!map || !mapReady) return;

  const features = [];
  const yr = appState.year || activeYear || 2025;

  wellsMapData.forEach(w => {
    if (w.anio_primera_prod <= yr) {
      // Apply basin filter if selected
      if (appState.filters.cuenca !== 'todas' && appState.chapterIndex === 1) {
        const cLower = (w.cuenca || '').toLowerCase();
        if (appState.filters.cuenca === 'neuquina' && !cLower.includes('neuq')) return;
        if (appState.filters.cuenca === 'golfo' && !cLower.includes('golfo')) return;
        if (appState.filters.cuenca === 'austral' && !cLower.includes('aust')) return;
      }
      // Apply resource filter if selected
      if (appState.chapterIndex === 2) {
        if (appState.filters.recurso === 'no_conv' && w.tipo_recurso !== 'NO CONVENCIONAL') return;
        if (appState.filters.recurso === 'conv' && w.tipo_recurso !== 'CONVENCIONAL') return;
      }

      const isShale = (w.tipo_recurso === 'NO CONVENCIONAL');
      features.push({
        type: 'Feature',
        properties: {
          sigla: w.sigla,
          empresa: w.empresa,
          yacimiento: w.yacimiento,
          tipo: w.tipo_recurso,
          isShale: isShale,
          prod_m3: w.prod_2025_m3 || 0,
          anio: w.anio_primera_prod,
          anio_primera_prod: w.anio_primera_prod
        },
        geometry: {
          type: 'Point',
          coordinates: [w.lon, w.lat]
        }
      });
    }
  });

  fpsMetrics.visibleFeatures = features.length;
  const geojson = { type: 'FeatureCollection', features };

  if (map.getSource('wells-source')) {
    map.getSource('wells-source').setData(geojson);
    addWellsIconLayer();
  } else {
    map.addSource('wells-source', { type: 'geojson', data: geojson });

    // Convencional Wells Layer
    map.addLayer({
      id: 'wells-conv',
      type: 'circle',
      source: 'wells-source',
      filter: ['!', ['get', 'isShale']],
      layout: { visibility: 'none' },
      paint: {
        'circle-color': '#C98B32',
        'circle-radius': [
          'interpolate', ['linear'], ['zoom'],
          4, 1.2,
          7, 2.4,
          10, 2.5,
          13, 3.2
        ],
        'circle-opacity': 0.65,
        'circle-stroke-color': '#000000',
        'circle-stroke-width': 0.3
      }
    });

    // No Convencional (Shale) Wells Layer
    map.addLayer({
      id: 'wells-shale',
      type: 'circle',
      source: 'wells-source',
      filter: ['get', 'isShale'],
      layout: { visibility: 'none' },
      paint: {
        'circle-color': '#39AFCF',
        'circle-radius': [
          'interpolate', ['linear'], ['zoom'],
          4, 1.6,
          7, 3.0,
          10, 3.2,
          13, 4.0
        ],
        'circle-opacity': 0.85,
        'circle-stroke-color': '#FFFFFF',
        'circle-stroke-width': 0.4
      }
    });

    // Top Pareto Wells Highlight Layer (Chapter 04)
    map.addLayer({
      id: 'wells-pareto',
      type: 'circle',
      source: 'wells-source',
      filter: ['all', ['get', 'isShale'], ['>=', ['get', 'prod_m3'], 25000]],
      layout: { visibility: 'none' },
      paint: {
        'circle-color': '#E3B55A',
        'circle-radius': [
          'interpolate', ['linear'], ['zoom'],
          4, 2.8,
          8, 5.0,
          12, 7.5
        ],
        'circle-opacity': 0.95,
        'circle-stroke-color': '#FFFFFF',
        'circle-stroke-width': 1.0
      }
    });

    addWellsIconLayer();
  }
}

function loadWellPumpIcon() {
  if (!map) return;
  if (map.hasImage('well-pump-icon')) {
    addWellsIconLayer();
    return;
  }

  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    try {
      if (map && !map.hasImage('well-pump-icon')) {
        map.addImage('well-pump-icon', img);
      }
      addWellsIconLayer();
    } catch (e) {
      console.warn('Error al registrar well-pump-icon en mapa:', e);
    }
  };
  img.onerror = (error) => {
    console.warn('Fallback: no se pudo cargar icono-pozo-petrolero-opt.png. Los pozos se mantendrán como puntos vectoriales.', error);
  };
  img.src = './assets/icono-pozo-petrolero-opt.png';
}

function addWellsIconLayer() {
  if (!map || !mapReady) return;
  if (!map.getSource('wells-source') || !map.hasImage('well-pump-icon') || map.getLayer('wells-icons')) return;

  const currentCh = CHAPTERS[appState.chapterIndex];
  const isWellsVisible = currentCh && ['geografia', 'quiebre', 'pareto', 'declino'].includes(currentCh.id);

  map.addLayer({
    id: 'wells-icons',
    type: 'symbol',
    source: 'wells-source',
    minzoom: 7.0,
    layout: {
      'icon-image': 'well-pump-icon',
      'icon-size': [
        'interpolate', ['linear'], ['zoom'],
        7.0, 0.22,
        9.0, 0.30,
        12.0, 0.38,
        15.0, 0.45
      ],
      'icon-anchor': 'bottom',
      'icon-allow-overlap': false,
      'icon-ignore-placement': false,
      'visibility': isWellsVisible ? 'visible' : 'none'
    },
    paint: {
      'icon-opacity': [
        'interpolate', ['linear'], ['zoom'],
        7.0, 0.0,
        7.8, 0.95,
        12.0, 1.0
      ]
    }
  });
}

function applyParetoMapEffect(enable) {
  paretoActive = enable;
  if (!map || !mapReady) return;

  if (enable) {
    if (map.getLayer('wells-pareto')) {
      map.setLayoutProperty('wells-pareto', 'visibility', 'visible');
    }
    if (map.getLayer('wells-conv')) {
      map.setPaintProperty('wells-conv', 'circle-opacity', 0.08);
    }
    if (map.getLayer('wells-shale')) {
      map.setPaintProperty('wells-shale', 'circle-opacity', 0.20);
    }
  } else {
    if (map.getLayer('wells-pareto')) {
      map.setLayoutProperty('wells-pareto', 'visibility', 'none');
    }
    if (map.getLayer('wells-conv')) {
      map.setPaintProperty('wells-conv', 'circle-opacity', 0.50);
    }
    if (map.getLayer('wells-shale')) {
      map.setPaintProperty('wells-shale', 'circle-opacity', 0.85);
    }
  }
}

function filterWellsByYear(year) {
  appState.year = year;
  activeYear = year;
  updateWellsGeoJsonSource();
}

let lastWellClickTime = 0;
let activeWellPopup = null;

function showWellPopup(p, lngLat) {
  const isShale = p.isShale || p.tipo === 'NO CONVENCIONAL';
  const color = isShale ? '#39AFCF' : '#C98B32';
  const tipoStr = isShale ? 'No Convencional (Shale)' : 'Convencional Maduro';
  const yr = appState.year || 2025;
  const isBpd = appState.filters.unit === 'bpd';
  const unitStr = isBpd ? 'barriles/día' : 'm³';
  const prodNum = Number(p.prod_m3 || 0);
  const prodDisplay = isBpd 
    ? Math.round(prodNum * 6.2898 / 365).toLocaleString('es-AR')
    : prodNum.toLocaleString('es-AR');

  const html = `
    <div class="well-popup-card">
      <div class="well-popup-header">
        <span class="well-popup-sigla">${p.sigla || 'POZO'}</span>
        <span class="well-popup-badge" style="background-color: ${color}22; color: ${color}; border: 1px solid ${color}66;">${tipoStr}</span>
      </div>
      <div class="well-popup-body">
        <div class="well-popup-meta">
          <span><strong>Operador:</strong> ${p.empresa || 'No especificado'}</span>
          <span><strong>Yacimiento:</strong> ${p.yacimiento || 'Área general'}</span>
          <span><strong>Año de inicio:</strong> ${p.anio_primera_prod || p.anio || '—'}</span>
        </div>
        <div class="well-popup-kpi">
          <span class="well-kpi-label">Producción estimada (${yr}):</span>
          <span class="well-kpi-val">${prodDisplay} ${unitStr}</span>
        </div>
      </div>
    </div>
  `;

  if (activeWellPopup) {
    activeWellPopup.remove();
  }

  const floatingGuide = document.getElementById('dino-guide-floating');
  if (floatingGuide) {
    floatingGuide.classList.add('dino-popup-active');
  }

  activeWellPopup = new maplibregl.Popup({
    closeButton: true,
    closeOnClick: true,
    anchor: 'bottom',
    offset: [0, -28],
    maxWidth: '320px',
    className: 'editorial-well-popup'
  })
    .setLngLat(lngLat)
    .setHTML(html)
    .addTo(map);

  activeWellPopup.on('close', () => {
    activeWellPopup = null;
    if (floatingGuide) {
      floatingGuide.classList.remove('dino-popup-active');
    }
  });
}

function handleWellInteractionClick(e) {
  const now = Date.now();
  if (now - lastWellClickTime < 250) return;
  lastWellClickTime = now;
  if (!e.features || !e.features.length) return;
  showWellPopup(e.features[0].properties, e.lngLat);
}

// Map Click Interactions (Inspectors)
function setupMapInteractions() {
  const interactiveLayers = ['wells-icons', 'wells-shale', 'wells-conv', 'basins-fill', 'concessions-fill', 'trajectories-line', 'pipelines-line', 'facilities-circle'];

  interactiveLayers.forEach(lyr => {
    map.on('mouseenter', lyr, () => { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', lyr, () => { map.getCanvas().style.cursor = ''; });
  });

  map.on('click', 'wells-icons', handleWellInteractionClick);
  map.on('click', 'wells-shale', handleWellInteractionClick);
  map.on('click', 'wells-conv', handleWellInteractionClick);

  map.on('click', 'basins-fill', (e) => {
    if (!e.features.length) return;
    const p = e.features[0].properties;
    new maplibregl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(`<strong>${p.nombre}</strong><br>Participación 2025: ${p.share_2025}%<br><span style="font-size: 0.75rem; color: #cbd5e1;">${p.descripcion}</span>`)
      .addTo(map);
  });
}

// ========================================================
// UNIFIED REACTIVE UI ENGINE (V4 + V5)
// ========================================================
function updateAppForState(options = {}) {
  const chapter = CHAPTERS[appState.chapterIndex];
  if (!chapter) return;

  currentStep = appState.chapterIndex;

  // 1. Camera FlyTo (if not explicitly suppressed during scrubber dragging)
  if (!options.keepCamera && map && mapReady) {
    map.flyTo({
      center: chapter.center,
      zoom: chapter.zoom,
      pitch: chapter.pitch,
      bearing: chapter.bearing,
      duration: 1800,
      essential: true
    });
  }

  // 2. Synchronize Layers
  syncLayersForChapter(chapter.layersVisible);

  // 3. Update Callouts on Map
  const callouts = (typeof chapter.getCallouts === 'function') ? chapter.getCallouts(appState) : (chapter.callouts || []);
  updateInMapCallouts(callouts);

  // 4. Update Story Column (Synthetic: single crisp insight, no heavy charts inside sidebar)
  updateStoryColumn(chapter);

  // 5. Update Top Global FilterBar
  updateFilterBar(chapter);

  // 6. Update Floating Chart Overlay Panel & Dynamic KPIs
  updateOverlayPanel(chapter);

  // 7. Update Global Timeline Bar
  updateTimelineUI(chapter);

  // 8. Update Wells Map filtering & Pareto highlight
  updateWellsGeoJsonSource();
  applyParetoMapEffect(appState.chapterIndex === 3);

  // 9. Update Journey Tracker & Progress Bar
  updateJourneyTracker(currentStep);
  const progressBar = document.getElementById('story-progress-bar');
  if (progressBar) {
    const pct = ((currentStep + 1) / CHAPTERS.length) * 100;
    progressBar.style.width = `${pct}%`;
  }

  // 10. Update Prev/Next Buttons (V6: Last chapter offers return to start)
  const prevBtn = document.getElementById('btn-prev-chapter');
  const nextBtn = document.getElementById('btn-next-chapter');
  if (prevBtn) prevBtn.disabled = (currentStep === 0);
  if (nextBtn) {
    if (currentStep >= CHAPTERS.length - 1) {
      nextBtn.textContent = 'volver al inicio ↺';
      nextBtn.title = 'Volver al primer capítulo';
      nextBtn.disabled = false;
    } else {
      nextBtn.textContent = 'siguiente →';
      nextBtn.title = 'Capítulo siguiente';
      nextBtn.disabled = false;
    }
  }
}

function updateStoryColumn(chapter) {
  const numEl = document.getElementById('chapter-num');
  const locEl = document.getElementById('chapter-location');
  const contentEl = document.getElementById('chapter-content');

  if (numEl) numEl.textContent = chapter.num;
  if (locEl) {
    locEl.textContent = chapter.headerLine.replace(/^[0-9]{2}\s+/, '').replace(/&nbsp;/g, ' ').trim();
  }

  if (contentEl) {
    const leadText = chapter.getInsight ? chapter.getInsight(appState) : '';
    contentEl.innerHTML = `
      <h2 class="story-headline">${chapter.title}</h2>
      <p class="story-lead">${leadText}</p>
    `;
  }

  updateDinoGuide(chapter);
}

function updateFilterBar(chapter) {
  // Update Mode buttons
  const btnRelato = document.getElementById('btn-mode-relato');
  const btnExplorar = document.getElementById('btn-mode-explorar');
  if (btnRelato && btnExplorar) {
    btnRelato.classList.toggle('active', appState.mode === 'relato');
    btnExplorar.classList.toggle('active', appState.mode === 'explorar');
  }

  // Populate contextual filter controls
  const container = document.getElementById('filter-controls-container');
  if (!container) return;

  const filterDefs = chapter.getFilters ? chapter.getFilters(appState) : [];
  container.innerHTML = '';

  filterDefs.forEach(f => {
    if (f.type === 'select') {
      const group = document.createElement('div');
      group.className = 'filter-field-group';

      const label = document.createElement('label');
      label.className = 'filter-field-label';
      label.htmlFor = f.id;
      label.textContent = f.label;
      group.appendChild(label);

      const wrap = document.createElement('div');
      wrap.className = 'filter-select-wrap';

      const select = document.createElement('select');
      select.className = 'filter-chip-select';
      select.id = f.id;
      select.setAttribute('aria-label', f.label);

      f.options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.val;
        option.textContent = opt.text;
        if (String(appState.filters[f.field]) === String(opt.val)) {
          option.selected = true;
        }
        select.appendChild(option);
      });

      select.addEventListener('change', (e) => {
        appState.mode = 'explorar';
        const val = e.target.value;
        if (f.field === 'paretoCutoff') {
          appState.filters[f.field] = Number(val);
        } else {
          appState.filters[f.field] = String(val);
        }

        // Clamp year if timeRange changes in Chapter 01
        if (f.field === 'timeRange') {
          if (val === '2017' && appState.year < 2017) {
            appState.year = 2017;
            activeYear = 2017;
          } else if (val === '2000' && appState.year < 2000) {
            appState.year = 2000;
            activeYear = 2000;
          }
        }

        updateAppForState({ keepCamera: true });
      });

      wrap.appendChild(select);

      const arrow = document.createElement('span');
      arrow.className = 'filter-select-arrow';
      arrow.textContent = '▾';
      wrap.appendChild(arrow);

      group.appendChild(wrap);
      container.appendChild(group);
    }
  });

  // Compact Layer Visibility Control for the active chapter
  const layerConfigs = {
    regreso: { id: 'layer-toggle-basins', name: 'Cuencas sedimentarias', layers: ['basins-fill', 'basins-line'] },
    geografia: { id: 'layer-toggle-wells', name: 'Pozos y Cuencas', layers: ['wells-conv', 'wells-shale', 'basins-fill', 'basins-line'] },
    quiebre: { id: 'layer-toggle-wells', name: 'Pozos de producción', layers: ['wells-conv', 'wells-shale'] },
    pareto: { id: 'layer-toggle-wells', name: 'Pozos activos', layers: ['wells-conv', 'wells-shale'] },
    ingenieria: { id: 'layer-toggle-trajectories', name: 'Ramas 3D & Concesiones', layers: ['concessions-fill', 'concessions-line', 'trajectories-line'] },
    declino: { id: 'layer-toggle-wells', name: 'Pozos Shale', layers: ['wells-shale'] },
    macro: { id: 'layer-toggle-pipelines', name: 'Oleoductos & Puertos', layers: ['pipelines-line', 'facilities-circle'] }
  };

  const chLayerCfg = layerConfigs[chapter.id];
  if (chLayerCfg) {
    const group = document.createElement('div');
    group.className = 'filter-field-group';

    const label = document.createElement('label');
    label.className = 'filter-field-label';
    label.htmlFor = chLayerCfg.id;
    label.textContent = 'Mostrar';
    group.appendChild(label);

    const wrap = document.createElement('div');
    wrap.className = 'filter-select-wrap';

    const select = document.createElement('select');
    select.className = 'filter-chip-select';
    select.id = chLayerCfg.id;
    select.setAttribute('aria-label', `Visibilidad de ${chLayerCfg.name}`);

    const optVisible = document.createElement('option');
    optVisible.value = 'visible';
    optVisible.textContent = `${chLayerCfg.name} (Visible)`;

    const optHidden = document.createElement('option');
    optHidden.value = 'none';
    optHidden.textContent = `${chLayerCfg.name} (Ocultar)`;

    const firstLayerId = chLayerCfg.layers[0];
    const isVisible = map && mapReady && map.getLayer(firstLayerId)
      ? map.getLayoutProperty(firstLayerId, 'visibility') !== 'none'
      : true;

    if (isVisible) {
      optVisible.selected = true;
    } else {
      optHidden.selected = true;
    }

    select.appendChild(optVisible);
    select.appendChild(optHidden);

    select.addEventListener('change', (e) => {
      const vis = e.target.value;
      if (map && mapReady) {
        chLayerCfg.layers.forEach(lid => {
          if (map.getLayer(lid)) {
            map.setLayoutProperty(lid, 'visibility', vis);
          }
        });
      }
    });

    wrap.appendChild(select);
    const arrow = document.createElement('span');
    arrow.className = 'filter-select-arrow';
    arrow.textContent = '▾';
    wrap.appendChild(arrow);

    group.appendChild(wrap);
    container.appendChild(group);
  }
}

function updateOverlayPanel(chapter) {
  const panel = document.getElementById('chart-overlay-panel');
  if (!panel) return;

  const ovCfg = (typeof chapter.getOverlayConfig === 'function') ? chapter.getOverlayConfig(appState) : (chapter.overlayConfig || {});

  // Header kicker & title
  const kicker = document.getElementById('overlay-kicker');
  const title = document.getElementById('overlay-title');
  if (kicker) kicker.textContent = ovCfg.kicker || 'MÉTRICA EDITORIAL';
  if (title) title.textContent = ovCfg.title || chapter.title;

  // View toggles
  const togglesWrap = document.getElementById('overlay-view-toggles');
  if (togglesWrap) {
    togglesWrap.innerHTML = '';
    const toggles = ovCfg.toggles || [];
    toggles.forEach(t => {
      const btn = document.createElement('button');
      btn.className = `overlay-toggle-btn ${appState.filters[t.field] === t.val ? 'active' : ''}`;
      if (t.id) btn.id = t.id;
      btn.textContent = t.label;
      btn.addEventListener('click', () => {
        appState.filters[t.field] = t.val;
        updateAppForState({ keepCamera: true });
      });
      togglesWrap.appendChild(btn);
    });
  }

  // Dynamic KPI Section
  const kpiContainer = document.getElementById('overlay-kpi-container');
  if (kpiContainer && chapter.getKPI) {
    const kpi = chapter.getKPI(appState);
    kpiContainer.innerHTML = `
      <div class="overlay-kpi-main">
        <span class="overlay-kpi-val">${kpi.val}</span>
        <span class="overlay-kpi-label">${kpi.label}</span>
      </div>
      <div class="overlay-kpi-badge ${kpi.isHighlight ? 'highlight' : ''}">
        ${kpi.badge}
      </div>
    `;
  }

  // Footer notes
  const srcTag = document.getElementById('overlay-source-tag');
  const scpTag = document.getElementById('overlay-scope-tag');
  if (srcTag) srcTag.textContent = ovCfg.sourceNote || 'Fuente: Secretaría de Energía';
  if (scpTag) scpTag.textContent = ovCfg.scopeNote || 'Datos Auditados';

  // Canvas switcher: Chapter 05 uses stacked charts, others use single chart
  const singleChartCanvas = document.getElementById('overlay-micro-chart');
  const stackedContainer = document.getElementById('overlay-stacked-charts');

  if (chapter.id === 'como_cambio_el_pozo') {
    if (singleChartCanvas) singleChartCanvas.classList.add('hidden');
    if (stackedContainer) stackedContainer.classList.remove('hidden');
  } else {
    if (singleChartCanvas) singleChartCanvas.classList.remove('hidden');
    if (stackedContainer) stackedContainer.classList.add('hidden');
  }

  // Render chart
  if (chapter.renderChart) {
    chapter.renderChart(appState);
  }
}

function updateTimelineUI(chapter) {
  const slider = document.getElementById('global-year-slider');
  const yrLabel = document.getElementById('scrubber-year-label');
  const prodLabel = document.getElementById('scrubber-prod-label');
  const scrubberBar = document.getElementById('timeline-scrubber-bar');
  const ticksWrap = document.querySelector('.timeline-ticks-labels');

  if (scrubberBar) {
    scrubberBar.style.opacity = '1';
    scrubberBar.style.pointerEvents = 'auto';
  }

  const range = (typeof chapter.getTimelineRange === 'function')
    ? chapter.getTimelineRange(appState)
    : (chapter.timelineRange || { min: 2006, max: 2025, step: 1, ticks: [2006, 2010, 2015, 2020, 2025] });

  if (appState.year < range.min) appState.year = range.min;
  if (appState.year > range.max) appState.year = range.max;
  activeYear = appState.year;

  if (slider) {
    slider.min = range.min;
    slider.max = range.max;
    slider.step = range.step || 1;
    slider.value = appState.year;
  }

  if (yrLabel) {
    yrLabel.textContent = appState.year;
  }

  if (ticksWrap && range.ticks) {
    ticksWrap.innerHTML = range.ticks.map(t => `<span>${t}</span>`).join('');
  }

  if (prodLabel) {
    const yr = appState.year;
    const match = timelineData.find(d => d.anio === yr);
    if (match) {
      prodLabel.textContent = `${Number(match.prod_pet_miles_m3).toLocaleString('es-AR', {minimumFractionDigits: 1, maximumFractionDigits: 1})} miles de m³`;
    } else {
      prodLabel.textContent = `${yr}`;
    }
  }
}

// Scrollytelling Navigation
function goToStep(stepIndex) {
  if (isNaN(stepIndex)) stepIndex = 0;
  if (stepIndex < 0) stepIndex = 0;
  if (stepIndex >= CHAPTERS.length) stepIndex = CHAPTERS.length - 1;
  appState.chapterIndex = stepIndex;

  // Restore chapter defaults in relato mode
  const ch = CHAPTERS[stepIndex];
  if (appState.mode === 'relato' && CHAPTER_DEFAULTS[ch.id]) {
    Object.assign(appState.filters, CHAPTER_DEFAULTS[ch.id]);
    appState.year = CHAPTER_DEFAULTS[ch.id].year || (ch.timelineRange?.defaultYear || 2025);
  } else {
    appState.year = ch.timelineRange?.defaultYear || 2025;
  }
  activeYear = appState.year;

  updateAppForState();
}

function syncLayersForChapter(visibleIds) {
  if (!map || !mapReady) return;
  const allManagedLayers = [
    'basins-fill', 'basins-line',
    'concessions-fill', 'concessions-line',
    'trajectories-line',
    'pipelines-line',
    'facilities-circle',
    'wells-conv', 'wells-shale',
    'wells-icons'
  ];

  const wellsActive = visibleIds.includes('wells-conv') || visibleIds.includes('wells-shale');

  allManagedLayers.forEach(id => {
    if (map.getLayer(id)) {
      let isVis = visibleIds.includes(id);
      if (id === 'wells-icons') {
        isVis = wellsActive;
      }
      map.setLayoutProperty(id, 'visibility', isVis ? 'visible' : 'none');
    }
  });
}

function updateInMapCallouts(callouts) {
  activeCalloutMarkers.forEach(m => m.remove());
  activeCalloutMarkers = [];

  if (!map || !mapReady) return;

  callouts.forEach(c => {
    const el = document.createElement('div');
    el.className = 'map-callout-editorial';
    el.innerHTML = `
      <span class="callout-place">${c.place}</span>
      <span class="callout-stat">${c.stat}</span>
      <span class="callout-desc">${c.desc}</span>
    `;

    const marker = new maplibregl.Marker({ element: el })
      .setLngLat(c.coords)
      .addTo(map);

    activeCalloutMarkers.push(marker);
  });
}

// ========================================================
// REEMPLAZO V10: Las fotos sobre el mapa fueron retiradas
// Los pozos ahora se representan como iconos WebGL de bombeo
// ========================================================

// Setup Event Listeners for Filters, Overlay and Story Column
function setupFilterBarEvents() {
  const btnRelato = document.getElementById('btn-mode-relato');
  const btnExplorar = document.getElementById('btn-mode-explorar');
  const btnReset = document.getElementById('btn-reset-filters');

  btnRelato?.addEventListener('click', () => {
    appState.mode = 'relato';
    const ch = CHAPTERS[appState.chapterIndex];
    if (CHAPTER_DEFAULTS[ch.id]) {
      Object.assign(appState.filters, CHAPTER_DEFAULTS[ch.id]);
      appState.year = CHAPTER_DEFAULTS[ch.id].year || (ch.timelineRange?.defaultYear || 2025);
    } else {
      appState.year = ch.timelineRange?.defaultYear || 2025;
    }
    activeYear = appState.year;
    updateAppForState({ keepCamera: false });
  });

  btnExplorar?.addEventListener('click', () => {
    appState.mode = 'explorar';
    updateAppForState({ keepCamera: true });
  });

  btnReset?.addEventListener('click', () => {
    appState.mode = 'relato';
    const ch = CHAPTERS[appState.chapterIndex];
    if (CHAPTER_DEFAULTS[ch.id]) {
      Object.assign(appState.filters, CHAPTER_DEFAULTS[ch.id]);
      appState.year = CHAPTER_DEFAULTS[ch.id].year || (ch.timelineRange?.defaultYear || 2025);
    } else {
      appState.year = ch.timelineRange?.defaultYear || 2025;
    }
    activeYear = appState.year;
    updateAppForState({ keepCamera: false });
  });
}

function setupOverlayPanelEvents() {
  const panel = document.getElementById('chart-overlay-panel');
  const toggleBtn = document.getElementById('btn-toggle-overlay');
  const restoreBtn = document.getElementById('btn-restore-overlay');
  const storyToggleBtn = document.getElementById('btn-toggle-story');
  const storyWrap = document.getElementById('story-column-wrap');

  toggleBtn?.addEventListener('click', () => {
    appState.overlayMinimized = true;
    panel?.classList.add('minimized');
    restoreBtn?.classList.remove('hidden');
  });

  restoreBtn?.addEventListener('click', () => {
    appState.overlayMinimized = false;
    panel?.classList.remove('minimized');
    restoreBtn?.classList.add('hidden');
  });

  storyToggleBtn?.addEventListener('click', () => {
    appState.storyMinimized = !appState.storyMinimized;
    storyWrap?.classList.toggle('minimized', appState.storyMinimized);
    storyToggleBtn.textContent = appState.storyMinimized ? '+' : '−';
  });
}

function setupTimelineScrubber() {
  const slider = document.getElementById('global-year-slider');
  const playBtn = document.getElementById('btn-play-timeline');
  const playIcon = document.getElementById('play-icon');
  const pauseIcon = document.getElementById('pause-icon');

  if (slider) {
    slider.addEventListener('input', (e) => {
      appState.year = parseInt(e.target.value);
      appState.mode = 'explorar';
      activeYear = appState.year;
      updateAppForState({ keepCamera: true });
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

    const ch = CHAPTERS[appState.chapterIndex];
    const range = ch.timelineRange || { min: 2006, max: 2025 };

    timelineInterval = setInterval(() => {
      if (appState.year >= range.max) {
        appState.year = range.min;
      } else {
        appState.year += 1;
      }
      activeYear = appState.year;
      updateAppForState({ keepCamera: true });
    }, 850);
  }

  function stopTimelinePlayback() {
    if (playIcon) playIcon.classList.remove('hidden');
    if (pauseIcon) pauseIcon.classList.add('hidden');
    clearInterval(timelineInterval);
    timelineInterval = null;
  }
}

// Navigation Controls
function setupNavigationButtons() {
  const handlePrev = () => { if (appState.chapterIndex > 0) goToStep(appState.chapterIndex - 1); };
  const handleNext = () => {
    if (appState.chapterIndex >= CHAPTERS.length - 1) {
      goToStep(0);
    } else {
      goToStep(appState.chapterIndex + 1);
    }
  };

  document.getElementById('btn-prev-chapter')?.addEventListener('click', handlePrev);
  document.getElementById('btn-next-chapter')?.addEventListener('click', handleNext);
}

// ========================================================
// ARGENTINOSAURUS COMENTARISTA DE DATOS (ITERACIÓN V11)
// Hallazgos reales, concretos y calculados que complementan el gráfico
// ========================================================
function getDinoDataCommentary(chapter, state) {
  const num = chapter?.num || '';
  const id = chapter?.id || '';
  const yr = state.year || 2025;

  // -------------------------------------------------------------
  // Capítulo 01: El regreso (Producción nacional)
  // Plantilla V11: «Aunque creció en {año}, la producción todavía quedó {porcentaje}% por debajo del máximo de {año_del_máximo}.»
  // -------------------------------------------------------------
  if (num === '01' || id === 'regreso') {
    const tr = state.filters.timeRange;
    if (tr === '2017') {
      return {
        kicker: 'UN DATO MÁS',
        text: `En el ciclo no convencional (2017—2025), la producción nacional se disparó un <strong class="dino-highlight">+65,8%</strong>, pasando de 28.007 miles de m³ a 46.438 miles de m³ impulsada por Vaca Muerta.`,
        source: 'Fuente: Secretaría de Energía / SESCO (2017—2025)'
      };
    } else if (tr === '2000') {
      return {
        kicker: 'UN DATO MÁS',
        text: `En lo que va del siglo XXI (2000—2025), la producción transitó un declino continuo del 33% hasta tocar piso en 2014, antes de iniciar su <strong class="dino-highlight">recuperación vertical</strong> con el shale.`,
        source: 'Fuente: Secretaría de Energía / SESCO (2000—2025)'
      };
    }

    const maxRecord = 49147.7; // Récord histórico absoluto de 1998
    const currentProd = timelineData.find(d => d.anio === yr)?.prod_pet_miles_m3 || 46438.5;
    const prevItem = timelineData.find(d => d.anio === yr - 1);

    if (yr === 1998) {
      return {
        kicker: 'UN DATO MÁS',
        text: `En 1998 se alcanzó el <strong class="dino-highlight">máximo histórico absoluto</strong> de la serie nacional, con 49.148 miles de m³ anuales (~846.900 barriles diarios).`,
        source: 'Fuente: Secretaría de Energía / SESCO (1950—2025)'
      };
    }

    const gapPct = Math.abs(((currentProd / maxRecord) - 1) * 100).toFixed(1).replace('.', ',');
    const growthStr = prevItem 
      ? `un ${(((currentProd / prevItem.prod_pet_miles_m3) - 1) * 100).toFixed(1).replace('.', ',')}%` 
      : 'fuerte ritmo';

    return {
      kicker: 'UN DATO MÁS',
      text: `Aunque creció ${growthStr} en ${yr}, la producción todavía quedó un <strong class="dino-highlight">${gapPct}% por debajo</strong> del máximo histórico de 1998 (49.148 miles de m³).`,
      source: 'Fuente: Secretaría de Energía / SESCO (1950—2025)'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 02: El mapa se mueve (Territorio / Cuencas)
  // Plantilla V11: «{Región} pasó del {participación_inicial}% al {participación_final}% de la producción entre {inicio} y {fin}: ganó {diferencia} puntos porcentuales.»
  // -------------------------------------------------------------
  if (num === '02' || id === 'mapa_se_mueve' || id === 'nuevo_centro') {
    const cuenca = state.filters.cuenca;

    if (cuenca === 'neuquina') {
      return {
        kicker: 'UN DATO MÁS',
        text: `La Cuenca Neuquina pasó de aportar el 42,1% al <strong class="dino-highlight">71,3% de la producción</strong> del país entre 2015 y 2025: ganó 29,2 puntos porcentuales gracias al shale.`,
        source: 'Fuente: Capítulos Provinciales / SESCO'
      };
    } else if (cuenca === 'golfo') {
      return {
        kicker: 'UN DATO MÁS',
        text: `El Golfo San Jorge aportó el <strong class="dino-highlight">20,5% del crudo</strong> nacional en 2025; hace dos décadas explicaba casi el 45% antes de la expansión no convencional.`,
        source: 'Fuente: Capítulos Provinciales / SESCO'
      };
    } else if (cuenca === 'austral') {
      return {
        kicker: 'UN DATO MÁS',
        text: `La Cuenca Austral aportó el <strong class="dino-highlight">2,8% del petróleo</strong> nacional en 2025, concentrando su infraestructura técnica en la producción de gas natural.`,
        source: 'Fuente: Capítulos Provinciales / SESCO'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `La Cuenca Neuquina y el Golfo San Jorge concentran juntas el <strong class="dino-highlight">91,8% del petróleo</strong> del país en 2025; las restantes tres cuencas suman menos del 9%.`,
      source: 'Fuente: Capítulos Provinciales / SESCO'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 03: El punto de quiebre (Convencional vs No convencional)
  // Plantilla V11: «El no convencional superó al convencional en {mes_y_año}. En {fecha_actual}, la diferencia llegó a {brecha} puntos porcentuales.»
  // -------------------------------------------------------------
  if (num === '03' || id === 'punto_quiebre' || id === 'quiebre') {
    const recurso = state.filters.recurso;

    if (recurso === 'no_conv') {
      return {
        kicker: 'UN DATO MÁS',
        text: `En 2015 el shale aportaba apenas el 5,2% del crudo argentino. En 2025 generó más de <strong class="dino-highlight">29.200 miles de m³</strong> anuales (62,9% nacional).`,
        source: 'Fuente: Cap. IV Secretaría de Energía'
      };
    } else if (recurso === 'conv') {
      return {
        kicker: 'UN DATO MÁS',
        text: `La extracción convencional declinó a un promedio del <strong class="dino-highlight">4,1% anual</strong> en la última década, operando pozos con décadas de madurez.`,
        source: 'Fuente: Cap. IV Secretaría de Energía'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `El no convencional superó al convencional en <strong class="dino-highlight">noviembre de 2023</strong>. A fines de 2025, la brecha a favor del shale trepó a <strong class="dino-highlight">37,0 puntos porcentuales</strong>.`,
      source: 'Fuente: Cap. IV Secretaría de Energía (Mensual)'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 04: Pocos pozos, mucho petróleo (Concentración de Pareto)
  // Plantilla V11: «El {porcentaje_de_pozos}% de los pozos concentra el {porcentaje_de_producción}% de la producción del conjunto seleccionado.»
  // -------------------------------------------------------------
  if (num === '04' || id === 'pocos_pozos' || id === 'pocos_mueven_mucho') {
    const cut = state.filters.paretoCutoff || 50;

    if (cut === 1) {
      return {
        kicker: 'UN DATO MÁS',
        text: `Para alcanzar el 50% de la extracción nacional se necesitan solo <strong class="dino-highlight">912 pozos</strong> de los 26.219 que operan en todo el país.`,
        source: 'Fuente: Padrón SESCO 2025 (26.219 pozos)'
      };
    } else if (cut === 66.7) {
      return {
        kicker: 'UN DATO MÁS',
        text: `El 10% de los pozos más productivos (2.622 pozos) alcanza a cubrir el <strong class="dino-highlight">71,0% del volumen</strong> extraído en 2025.`,
        source: 'Fuente: Padrón SESCO 2025 (26.219 pozos)'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `El <strong class="dino-highlight">1% de los pozos de mayor caudal</strong> (262 pozos de shale) aporta el 22,9% del crudo del país, con una media superior a 40.000 m³ anuales por pozo.`,
      source: 'Fuente: Padrón SESCO 2025 (26.219 pozos)'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 05: Cómo cambió el pozo (Tecnología / Subsuelo)
  // Plantilla V11: «Entre {inicio} y {fin}, {métrica} cambió de {valor_inicial} a {valor_final} {unidad}: una variación del {porcentaje}%.»
  // -------------------------------------------------------------
  if (num === '05' || id === 'como_cambio_el_pozo') {
    const techMetric = state.filters.techMetric || 'combo';

    if (techMetric === 'sand') {
      return {
        kicker: 'UN DATO MÁS',
        text: `Entre 2016 y 2025, el apuntalante inyectado por pozo se multiplicó de 3.349 a <strong class="dino-highlight">11.805 toneladas de arena</strong>: una variación del +253%.`,
        source: 'Fuente: Registros de fractura / Capítulos Provinciales'
      };
    } else if (techMetric === 'water') {
      return {
        kicker: 'UN DATO MÁS',
        text: `Entre 2016 y 2025, el volumen de agua inyectada por pozo aumentó de 18.535 a <strong class="dino-highlight">77.268 m³</strong>: una variación del +317%.`,
        source: 'Fuente: Registros de fractura / Capítulos Provinciales'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `Entre 2016 y 2025, las etapas de fractura por pozo crecieron de 16,3 a 51,8 etapas: una variación del <strong class="dino-highlight">+218%</strong> que triplicó la intensidad de diseño.`,
      source: 'Fuente: Registros de fractura / Capítulos Provinciales'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 06: Generaciones de pozos (Cohortes)
  // Plantilla V11: «A los {edad} meses, la cohorte {cohorte_a} produjo {porcentaje}% {más_o_menos} por pozo que la cohorte {cohorte_b}.»
  // -------------------------------------------------------------
  if (num === '06' || id === 'generaciones_pozos' || id === 'curva_verdad') {
    return {
      kicker: 'UN DATO MÁS',
      text: `A los 12 meses de vida, un pozo de la cohorte 2024 produjo <strong class="dino-highlight">1.590 m³/mes</strong>: casi 10 veces más que la cohorte 2018 a esa misma edad (149 m³/mes).`,
      source: 'Fuente: Curvas de declino M0—M24 / SESCO'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 07: Del pozo al país (Economía / Divisas y Empleo)
  // Plantilla V11: «{Variable} registró su mayor {aumento_o_caída} del período en {fecha}: {variación} respecto de {base}.»
  // -------------------------------------------------------------
  if (num === '07' || id === 'del_pozo_al_pais' || id === 'saldo_real') {
    const econMetric = state.filters.econMetric || 'trade';

    if (econMetric === 'employment') {
      return {
        kicker: 'UN DATO MÁS',
        text: `El empleo directo en hidrocarburos en Neuquén creció de 18.700 puestos en 2013 a <strong class="dino-highlight">34.200 en 2024</strong>: un incremento del 82,9% en el período.`,
        source: 'Fuente: MTEySS / Registros de Empleo Formal'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `Las importaciones de combustibles pasaron del 16,2% del total de compras argentinas en 2013 a apenas el <strong class="dino-highlight">5,1% en 2024</strong>: una caída de 11,1 puntos porcentuales.`,
      source: 'Fuente: INDEC (Intercambio Comercial Argentino)'
    };
  }

  // -------------------------------------------------------------
  // Capítulo 08: Argentina en el mundo (Escala global EIA 2024)
  // -------------------------------------------------------------
  if (num === '08' || id === 'argentina_mundo') {
    const isLatam = state.filters.worldScope === 'latam';
    const isEvol = state.filters.worldView === 'evolution';

    if (isEvol) {
      return {
        kicker: 'UN DATO MÁS',
        text: `Entre 2017 y 2024, Argentina aumentó su extracción de crudo un <strong class="dino-highlight">+46,1%</strong> (Base 100 en 2017 = 146,1), mientras que la producción global apenas varió un <strong class="dino-highlight">+0,9%</strong> (Índice 100,9).`,
        source: 'Fuente: U.S. EIA International Energy Statistics (2024)'
      };
    } else if (isLatam) {
      return {
        kicker: 'UN DATO MÁS',
        text: `Con <strong class="dino-highlight">700,8 miles de bpd</strong>, Argentina es el 5° productor de América Latina (8,0% regional), detrás de Brasil (3.356,5), México (1.841,8), Venezuela (863,5) y Colombia (772,7).`,
        source: 'Fuente: U.S. EIA International Energy Statistics (2024)'
      };
    }

    return {
      kicker: 'UN DATO MÁS',
      text: `Argentina ocupa el <strong class="dino-highlight">puesto #22 global</strong> entre 99 países con 700,8 miles de bpd (0,86% del total mundial), liderando el crecimiento no convencional fuera de América del Norte.`,
      source: 'Fuente: U.S. EIA International Energy Statistics (2024)'
    };
  }

  return {
    kicker: 'UN DATO MÁS',
    text: `Observá cómo la producción y las variables técnicas responden dinámicamente a la línea de tiempo.`,
    source: 'Fuente: Secretaría de Energía'
  };
}

function getDinoMessage(chapter, state) {
  const comm = getDinoDataCommentary(chapter, state || appState);
  return comm.text;
}

function updateDinoGuide(chapter) {
  const speechEl = document.getElementById('dino-speech-text');
  const labelEl = document.getElementById('dino-bubble-label');
  const sourceEl = document.getElementById('dino-speech-source');
  const comm = getDinoDataCommentary(chapter, appState);

  if (labelEl) labelEl.textContent = `🦕 ${comm.kicker || 'UN DATO MÁS'}`;
  if (speechEl) speechEl.innerHTML = comm.text;
  if (sourceEl) sourceEl.textContent = comm.source || '';
}

function setupDinoGuideToggle() {
  const btnToggle = document.getElementById('btn-toggle-dino');
  const btnPill = document.getElementById('btn-dino-pill');
  const wrapper = document.getElementById('dino-floating-wrapper');
  if (!btnToggle || !wrapper) return;

  const applyVisibility = (isHidden) => {
    wrapper.classList.toggle('hidden', isHidden);
    btnPill?.classList.toggle('hidden', !isHidden);
    btnToggle.setAttribute('aria-pressed', String(isHidden));
    btnToggle.title = isHidden ? 'Mostrar guía' : 'Ocultar guía';
    sessionStorage.setItem('dinoGuideHidden', String(isHidden));
  };

  const isInitiallyHidden = sessionStorage.getItem('dinoGuideHidden') === 'true';
  if (isInitiallyHidden) {
    applyVisibility(true);
  }

  btnToggle.addEventListener('click', () => applyVisibility(true));
  btnPill?.addEventListener('click', () => applyVisibility(false));
}

// Section 2: Isolation of scroll wheel on panels (wheel scrolls panel, never triggers map zoom or chapter change)
function setupPanelWheelIsolation() {
  const panels = [
    document.getElementById('active-story-card'),
    document.getElementById('chart-overlay-panel'),
    document.getElementById('dino-speech-bubble'),
    document.getElementById('chapter-content')
  ];

  panels.forEach(p => {
    if (p) {
      p.addEventListener('wheel', (e) => {
        e.stopPropagation();
      }, { passive: true });
    }
  });
}

function setupKeyboardNavigation() {
  window.addEventListener('keydown', (e) => {
    if (['ArrowDown', 'ArrowRight', 'Space'].includes(e.code)) {
      if (appState.chapterIndex < CHAPTERS.length - 1) {
        e.preventDefault();
        goToStep(appState.chapterIndex + 1);
      }
    } else if (['ArrowUp', 'ArrowLeft'].includes(e.code)) {
      if (appState.chapterIndex > 0) {
        e.preventDefault();
        goToStep(appState.chapterIndex - 1);
      }
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
    if (appState.chapterIndex < CHAPTERS.length - 1) {
      goToStep(appState.chapterIndex + 1);
      scheduleNextAutoTour();
    } else {
      isAutoTourRunning = false;
      document.getElementById('btn-auto-tour')?.classList.remove('active');
      const txt = document.getElementById('auto-tour-text');
      if (txt) txt.textContent = 'Relato continuo';
    }
  }, 10000);
}

function executeTourEntry() {
  if (hasEnteredTour) return;
  hasEnteredTour = true;

  const splash = document.getElementById('hero-splash');
  if (splash) {
    splash.classList.add('hero-hidden');
    splash.setAttribute('aria-hidden', 'true');
    splash.setAttribute('inert', '');
    setTimeout(() => {
      splash.style.display = 'none';
    }, 850);
  }

  goToStep(0);

  // Focus management: move keyboard focus to an interactive control in the main tour
  setTimeout(() => {
    const nextBtn = document.getElementById('btn-next-chapter');
    if (nextBtn && !nextBtn.disabled) {
      nextBtn.focus();
    } else {
      document.getElementById('btn-auto-tour')?.focus();
    }
  }, 100);
}

function setupHeroSplash() {
  const splash = document.getElementById('hero-splash');
  const startBtn = document.getElementById('btn-start-tour');
  if (!startBtn || !splash) return;

  const handleStart = (e) => {
    if (e && e.type === 'click') {
      // Natural click
    }
    if (hasEnteredTour) return;

    if (!isDataLoaded) {
      // Data is still loading: display accessible loading state on button and wait
      pendingTourEntry = true;
      startBtn.innerHTML = `
        <span class="hero-btn-spinner" aria-hidden="true"></span>
        <span>Cargando datos...</span>
      `;
      startBtn.disabled = true;
      startBtn.setAttribute('aria-busy', 'true');
      return;
    }

    executeTourEntry();
  };

  startBtn.addEventListener('click', handleStart);

  // Accessibility: Enter and Space triggers start
  startBtn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleStart(e);
    }
  });
}

// DOM Ready Init
document.addEventListener('DOMContentLoaded', initScrollyPlatform);
