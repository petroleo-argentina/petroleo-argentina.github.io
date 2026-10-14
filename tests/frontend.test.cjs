const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'frontend/app.js'), 'utf8');
const bundle = fs.readFileSync(path.join(root, 'frontend/data_bundle.js'), 'utf8');
function sandbox() {
  const elements = {};
  const context = vm.createContext({
    window: { location: { port: '' } },
    document: { addEventListener() {}, getElementById(id) {
      return elements[id] ||= { textContent: '', disabled: true, attributes: {},
        setAttribute(k,v) { this.attributes[k]=v; }, removeAttribute(k) { delete this.attributes[k]; } };
    } },
    console: { error() {}, warn() {} }, performance: { now: () => 0 },
    AbortController, setTimeout, clearTimeout,
  });
  vm.runInContext(bundle, context);
  vm.runInContext(source, context);
  return { context, elements };
}
test('bundled datasets match the API JSON files', () => {
  const { context } = sandbox();
  for (const [key, value] of Object.entries(context.window.DATA_BUNDLE)) {
    const file = path.join(root, 'api/static_data', key + '.json');
    if (fs.existsSync(file)) assert.equal(JSON.stringify(value), JSON.stringify(JSON.parse(fs.readFileSync(file))));
  }
});
test('2017 commentary follows the selected year and actual series', () => {
  const { context } = sandbox();
  vm.runInContext('timelineData = window.DATA_BUNDLE.timeline_1950_2025', context);
  const commentary = year => vm.runInContext(`getDinoDataCommentary({num:'01'}, {year:${year}, filters:{timeRange:'2017'}}).text`, context);
  assert.match(commentary(2025), /63,9%/);
  assert.match(commentary(2025), /28\.331/);
  assert.doesNotMatch(commentary(2020), /2025|63,9%/);
  assert.match(commentary(2017), /Avanzá/);
});
test('static hosting uses bundled data without an API request', async () => {
  const { context } = sandbox();
  context.fetch = () => { throw new Error('Unexpected request'); };
  const result = await vm.runInContext("loadResource('/api/timeline', 'timeline_1950_2025')", context);
  assert.equal(result.length, 76);
});
test('API failure falls back to bundle; missing data rejects', async () => {
  const { context } = sandbox();
  context.window.location.port = '8000';
  context.fetch = async () => ({ ok: false, status: 503 });
  assert.equal((await vm.runInContext("loadResource('/api/timeline', 'timeline_1950_2025')", context)).length, 76);
  await assert.rejects(vm.runInContext("loadResource('/api/missing', 'missing')", context), /503/);
});
test('failed data startup keeps the cover visible and offers retry', async () => {
  const { context, elements } = sandbox();
  context.maplibregl = {};
  context.Chart = {};
  context.window.DATA_BUNDLE = {};
  context.fetch = async () => ({ ok: false, status: 503 });
  vm.runInContext(`
    initMapLibreMap = () => {};
    initFpsTracker = setupTimelineScrubber = setupNavigationButtons =
    setupPanelWheelIsolation = setupDinoGuideToggle = setupKeyboardNavigation =
    setupAutoTour = setupHeroSplash = setupFilterBarEvents =
    setupOverlayPanelEvents = buildJourneyTrack = () => {};
    pendingTourEntry = true;
  `, context);
  await vm.runInContext('initScrollyPlatform()', context);
  assert.equal(vm.runInContext('isDataLoaded', context), false);
  assert.equal(vm.runInContext('hasEnteredTour', context), false);
  assert.equal(vm.runInContext('pendingTourEntry', context), false);
  assert.equal(elements['btn-start-tour'].disabled, false);
  assert.equal(elements['btn-start-tour'].textContent, 'Volver a intentar');
  assert.match(elements['hero-load-status'].textContent, /No pudimos cargar/);
});
