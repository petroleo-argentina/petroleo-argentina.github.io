import re
"""
Automated Test Suite — Plataforma Petróleo en Argentina
Validates data integrity, analytical metrics, geo data layers, API endpoints,
and the audit requirements specified in Section 31 of reordenamiento_y_redisenio_petroleo_argentina.md.
"""

import json
import urllib.request
from pathlib import Path
import pytest
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DATA_DIR = BASE_DIR / "api" / "static_data"
EXPORTS_DIR = BASE_DIR / "analysis" / "exports"

def test_static_data_files_exist():
    required_files = [
        "timeline_1950_2025.json",
        "conv_vs_noconv_monthly.json",
        "cohorts_decay_curves.json",
        "technical_fractures_trends.json",
        "macro_employment_trends.json",
        "wells_map_sample.json",
        "geo_basins.json",
        "geo_concessions_vaca_muerta.json",
        "geo_trajectories_sample.json",
        "geo_pipelines_sample.json",
        "geo_refineries_ports.json",
        "geo_flaring_sample.json"
    ]
    for filename in required_files:
        p = STATIC_DATA_DIR / filename
        assert p.exists(), f"Missing required static data file: {filename}"
        assert p.stat().st_size > 0, f"File is empty: {filename}"

def test_historical_peak_1998_and_2025_expansion_metric():
    """
    Audits the historical series:
    1. 1998 was the all-time peak of the series with 49.147,7 miles de m3 (~846k bpd).
    2. 2025 reached 46.438,5 miles de m3 (~798.5k bpd), which is the 26-year high and shale record,
       but NOT an all-time historical record (as 1998 was higher).
    3. 2025 grew +12.84% vs 2024 (41.152,2 miles de m3).
    """
    timeline_path = STATIC_DATA_DIR / "timeline_1950_2025.json"
    data = json.loads(timeline_path.read_text(encoding="utf-8"))
    
    p1998 = next((d for d in data if d["anio"] == 1998), None)
    assert p1998 is not None, "1998 data missing from timeline"
    assert abs(p1998["prod_pet_miles_m3"] - 49147.7) < 1.0, f"Expected 1998 historical peak ~49147.7, got {p1998['prod_pet_miles_m3']}"
    
    p2024 = next((d for d in data if d["anio"] == 2024), None)
    assert p2024 is not None, "2024 data missing from timeline"
    assert abs(p2024["prod_pet_miles_m3"] - 41152.2) < 1.0
    
    p2025 = next((d for d in data if d["anio"] == 2025), None)
    assert p2025 is not None, "2025 data missing from timeline"
    assert abs(p2025["prod_pet_miles_m3"] - 46438.5) < 1.0, f"Unexpected 2025 production: {p2025['prod_pet_miles_m3']}"
    assert p2025["bpd"] > 790000, "2025 bpd should exceed 790k"
    
    # 2025 is higher than 2024 (+12.8%) but strictly lower than 1998 peak
    assert p2025["prod_pet_miles_m3"] < p1998["prod_pet_miles_m3"], "2025 cannot be claimed as an all-time record when 1998 is higher!"
    growth_vs_2024 = ((p2025["prod_pet_miles_m3"] / p2024["prod_pet_miles_m3"]) - 1) * 100
    assert abs(growth_vs_2024 - 12.84) < 0.2, f"Expected ~12.84% annual growth, got {growth_vs_2024:.2f}%"

def test_shale_share_62_92_pct():
    """Validates that 2025 national oil has ~62.92% non-conventional share."""
    monthly_path = STATIC_DATA_DIR / "conv_vs_noconv_monthly.json"
    data = json.loads(monthly_path.read_text(encoding="utf-8"))
    d2025 = [d for d in data if d["anio"] == 2025]
    assert len(d2025) == 12, "2025 should have 12 monthly records"
    total_2025 = sum(d["pet_total_miles_m3"] for d in d2025)
    shale_2025 = sum(d["pet_no_conv_miles_m3"] for d in d2025)
    share = (shale_2025 / total_2025) * 100
    assert 62.5 <= share <= 63.2, f"Expected 62.92% share in 2025, got {share:.2f}%"

def test_crossover_november_2023():
    """
    Validates that:
    1. In June 2023 no-conventional was < 50% (~47.09%).
    2. November 2023 was the first month with no-conventional > 50% (51.11%).
    3. The crossover remained permanent thereafter.
    """
    crossover_csv = EXPORTS_DIR / "crossover_monthly.csv"
    assert crossover_csv.exists(), "crossover_monthly.csv missing from analysis/exports"
    df = pd.read_csv(crossover_csv)
    
    # Check June 2023
    row_jun = df[df["fecha"] == "2023-06"].iloc[0]
    assert row_jun["share_no_convencional_pct"] < 50.0, "June 2023 was NOT the crossover month"
    assert abs(row_jun["share_no_convencional_pct"] - 47.09) < 0.5
    
    # Check November 2023
    row_nov = df[df["fecha"] == "2023-11"].iloc[0]
    assert row_nov["share_no_convencional_pct"] > 50.0, "November 2023 should exceed 50%"
    assert abs(row_nov["share_no_convencional_pct"] - 51.11) < 0.5
    
    # Check all months before 2023-11 had share < 50%
    pre_nov = df[df["fecha"] < "2023-11"]
    assert (pre_nov["share_no_convencional_pct"] < 50.0).all(), "Found premature crossover before Nov 2023"
    
    # Check all months after 2023-11 maintained share > 50%
    post_nov = df[df["fecha"] > "2023-11"]
    assert (post_nov["share_no_convencional_pct"] > 50.0).all(), "Crossover reverted after Nov 2023"

def test_pareto_top_milestones():
    """Validates the Pareto milestones: Top 1%, Top 5%, Top 10% from pareto_2025.csv."""
    pareto_csv = EXPORTS_DIR / "pareto_2025.csv"
    assert pareto_csv.exists(), "pareto_2025.csv missing from analysis/exports"
    df = pd.read_csv(pareto_csv)
    
    assert len(df) == 26219, f"Expected 26219 active oil wells, got {len(df)}"
    
    # Top 1% (262 wells)
    top1 = df.iloc[261]["pct_produccion_acum"]
    assert 22.0 <= top1 <= 23.5, f"Top 1% expected ~22.86%, got {top1:.2f}%"
    
    # Top 5% (1311 wells)
    top5 = df.iloc[1310]["pct_produccion_acum"]
    assert 57.5 <= top5 <= 59.0, f"Top 5% expected ~58.22%, got {top5:.2f}%"
    
    # Top 10% (2622 wells)
    top10 = df.iloc[2621]["pct_produccion_acum"]
    assert 70.0 <= top10 <= 72.0, f"Top 10% expected ~70.98%, got {top10:.2f}%"

def test_pareto_912_wells_explain_50_pct():
    """Validates that exactly 912 wells explain 50% of 2025 national oil production."""
    pareto_csv = EXPORTS_DIR / "pareto_2025.csv"
    df = pd.read_csv(pareto_csv)
    
    # Well 911 (0-indexed 910) should be < 50%
    assert df.iloc[910]["pct_produccion_acum"] < 50.0
    # Well 912 (0-indexed 911) should cross 50%
    assert df.iloc[911]["pct_produccion_acum"] >= 50.0
    
    pct_wells = df.iloc[911]["pct_pozos_acum"]
    assert abs(pct_wells - 3.48) < 0.1, f"Expected 3.48% of wells, got {pct_wells:.2f}%"

def test_endpoints_cohortes():
    """Validates cohorts API data integrity and structure."""
    cohorts_path = STATIC_DATA_DIR / "cohorts_decay_curves.json"
    data = json.loads(cohorts_path.read_text(encoding="utf-8"))
    assert len(data) >= 100, "Cohorts dataset too small"
    
    cohorts_present = set(d["cohorte"] for d in data if "cohorte" in d)
    for c in [2015, 2018, 2021, 2024]:
        assert c in cohorts_present, f"Cohorte {c} missing from cohorts dataset"
        
    c2024 = [d for d in data if d.get("cohorte") == 2024 and d.get("mes_vida") == 0]
    assert len(c2024) > 0
    assert c2024[0]["mediana_prod_m3"] > 0

def test_endpoints_macro():
    """Validates macro trends data properties."""
    macro_path = STATIC_DATA_DIR / "macro_employment_trends.json"
    data = json.loads(macro_path.read_text(encoding="utf-8"))
    assert len(data) >= 10
    for row in data:
        assert "year" in row
        assert "puestos_hidrocarburos_neuquen" in row
        assert "fuel_exports_pct" in row
        assert "fuel_imports_pct" in row

def test_charts_data_non_empty():
    """
    Validates that the JavaScript mapping logic for the three previously broken
    charts produces non-empty, non-null data series.
    """
    # 1. Crossover chart data mapping
    monthly_data = json.loads((STATIC_DATA_DIR / "conv_vs_noconv_monthly.json").read_text(encoding="utf-8"))
    crossover_filtered = monthly_data[::3]
    conv_vals = [d.get("pet_conv_miles_m3") or d.get("convencional_m3_mes") for d in crossover_filtered]
    noconv_vals = [d.get("pet_no_conv_miles_m3") or d.get("no_convencional_m3_mes") for d in crossover_filtered]
    assert all(v is not None and v > 0 for v in conv_vals), "Crossover chart conventional series has null or zero values"
    assert all(v is not None for v in noconv_vals), "Crossover chart non-conventional series has null values"
    
    # 2. Cohorts chart mapping
    cohorts_data = json.loads((STATIC_DATA_DIR / "cohorts_decay_curves.json").read_text(encoding="utf-8"))
    c2018 = [d for d in cohorts_data if (d.get("cohorte") or d.get("cohorte_anio")) == 2018]
    assert len(c2018) > 0, "Cohorte 2018 has no records"
    c2018_vals = [d.get("mediana_prod_m3") or d.get("media_prod_m3") for d in c2018]
    assert all(v is not None for v in c2018_vals), "Cohorte 2018 series has null values"
    
    # 3. Macro trade mapping
    macro_data = json.loads((STATIC_DATA_DIR / "macro_employment_trends.json").read_text(encoding="utf-8"))
    years = [d.get("year") or d.get("anio") for d in macro_data]
    exports = [d.get("fuel_exports_pct") or d.get("combustibles_export_pct_mercancias") for d in macro_data]
    assert all(y is not None and y > 2000 for y in years), "Macro chart years invalid"
    assert all(e is not None and e > 0 for e in exports), "Macro chart exports series has null or zero values"

def test_geo_trajectories_validity():
    traj_path = STATIC_DATA_DIR / "geo_trajectories_sample.json"
    trajs = json.loads(traj_path.read_text(encoding="utf-8"))
    assert len(trajs) >= 50, "Should have at least 50 representative trajectories"
    for t in trajs:
        assert "sigla" in t
        assert t["largo_m"] > 500, "Horizontal lateral length should be > 500m"
        assert len(t["path"]) > 2, "Path should have coordinates"

def test_geo_pipelines_connectivity():
    pipe_path = STATIC_DATA_DIR / "geo_pipelines_sample.json"
    pipes = json.loads(pipe_path.read_text(encoding="utf-8"))
    assert len(pipes) >= 3
    oldelval = next((p for p in pipes if p["id"] == "oldelval"), None)
    assert oldelval is not None
    assert len(oldelval["path"]) >= 5

def test_api_endpoints_live():
    endpoints = [
        "/api/kpis",
        "/api/timeline",
        "/api/production/monthly",
        "/api/cohorts",
        "/api/wells/map",
        "/api/geo/basins",
        "/api/geo/concessions",
        "/api/geo/trajectories",
        "/api/geo/pipelines",
        "/api/geo/facilities",
        "/api/geo/flaring"
    ]
    for ep in endpoints:
        url = f"http://127.0.0.1:8000{ep}"
        try:
            req = urllib.request.urlopen(url, timeout=3)
            assert req.status == 200, f"Endpoint {ep} returned HTTP {req.status}"
        except Exception as e:
            pytest.fail(f"Failed to query {url}: {e}")

def test_carto_config_and_fallback_style():
    """Validates Carto token handling, .gitignore security, and fallback vector style."""
    config_example = BASE_DIR / "frontend" / "config.example.js"
    assert config_example.exists(), "config.example.js missing"
    assert "CARTO_TOKEN" in config_example.read_text(encoding="utf-8")

    gitignore = BASE_DIR / ".gitignore"
    assert gitignore.exists(), ".gitignore missing"
    assert "frontend/config.js" in gitignore.read_text(encoding="utf-8")

    # Fallback style validation
    style_path = BASE_DIR / "frontend" / "styles" / "petroleo-map-style.json"
    assert style_path.exists(), "petroleo-map-style.json missing"
    style_data = json.loads(style_path.read_text(encoding="utf-8"))
    assert style_data.get("version") == 8
    assert "terrain-dem" in style_data.get("sources", {})
    assert "openmaptiles" in style_data.get("sources", {})
    
    # Check hillshade layer
    hills = next((l for l in style_data.get("layers", []) if l.get("type") == "hillshade"), None)
    assert hills is not None, "Hillshade layer missing in fallback style"
    assert hills.get("paint", {}).get("hillshade-illumination-direction") == 315

    # Check style served over HTTP 200
    style_url = "http://127.0.0.1:8000/styles/petroleo-map-style.json"
    req = urllib.request.urlopen(style_url, timeout=3)
    assert req.status == 200, f"Fallback style returned HTTP {req.status}"

    # Verify no token is hardcoded in app.js or index.html
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    assert "window.APP_CONFIG.CARTO_TOKEN" in app_js
    assert "CARTO basemap unavailable. Using fallback map style." in app_js

def test_pareto_api_endpoint_and_milestones():
    """Validates the /api/pareto endpoint returns accurate milestones from audited 2025 data."""
    url = "http://127.0.0.1:8000/api/pareto"
    req = urllib.request.urlopen(url, timeout=3)
    assert req.status == 200
    data = json.loads(req.read().decode("utf-8"))
    
    assert data["total_pozos"] == 26219
    assert data["pareto_wells_50_pct"] == 912
    assert abs(data["pareto_share_pct"] - 3.48) < 0.1
    assert "milestones" in data
    assert len(data["milestones"]) >= 4
    
    m50 = next((m for m in data["milestones"] if m["pct_prod"] == 50.0), None)
    assert m50 is not None
    assert m50["pozos"] == 912
    assert abs(m50["pct_pozos"] - 3.48) < 0.1

def test_v4_v5_dom_structure():
    """Validates that frontend/index.html includes all required DOM elements for the V4+V5 unified architecture."""
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    
    # Filter Bar elements
    assert 'id="global-filter-bar"' in html_content
    assert 'id="btn-mode-relato"' in html_content
    assert 'id="btn-mode-explorar"' in html_content
    assert 'id="filter-controls-container"' in html_content
    assert 'id="btn-reset-filters"' in html_content
    
    # Floating Overlay Panel elements
    assert 'id="chart-overlay-panel"' in html_content
    assert 'id="overlay-kpi-container"' in html_content
    assert 'id="overlay-chart-container"' in html_content
    assert 'id="overlay-micro-chart"' in html_content
    assert 'id="overlay-stacked-charts"' in html_content
    assert 'id="chart-canvas-length"' in html_content
    assert 'id="chart-canvas-fractures"' in html_content
    assert 'id="btn-restore-overlay"' in html_content
    
    # Global bottom timeline scrubber
    assert 'id="timeline-scrubber-bar"' in html_content
    assert 'id="global-year-slider"' in html_content
    assert 'id="btn-play-timeline"' in html_content
    assert 'id="scrubber-year-label"' in html_content
    assert 'id="scrubber-prod-label"' in html_content

def test_v4_v5_css_overlay_and_filter_styling():
    """Validates CSS definitions for the floating overlay, filter bar, stacked charts, and responsive rules."""
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    
    assert ".global-filter-bar" in css_content
    assert ".chart-overlay-panel" in css_content
    assert ".overlay-kpi-block" in css_content
    assert ".stacked-charts-box" in css_content
    assert ".mode-toggle-group" in css_content
    assert "@media (max-width: 1024px)" in css_content
    assert "@media (max-width: 768px)" in css_content

def test_v4_v5_app_js_state_and_chapter05_stacked_charts():
    """Validates that app.js manages reactive appState and implements Chapter 05 stacked charts without dual-axis."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    
    # Reactive appState
    assert "const appState = {" in app_js
    assert "paretoCutoff" in app_js
    assert "setupFilterBarEvents" in app_js
    assert "updateOverlayPanel" in app_js
    assert "updateTimelineUI" in app_js
    assert "updateAppForState" in app_js
    
    # Chapter 05 stacked charts (two independent synchronized charts)
    assert "stackedLengthChart" in app_js
    assert "stackedFracturesChart" in app_js
    assert "chart-canvas-length" in app_js
    assert "chart-canvas-fractures" in app_js
    
    # Ensure dual-axis y1 is not used in the stacked implementation
    assert "yAxisID: 'y1'" not in app_js

def test_v6_seven_chapters_and_synthesis_removed():
    """Validates that old generic synthesis is removed and the narrative has exactly 8 chapters with Chapter 08 being Argentina en el mundo."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    
    # 1. Old generic synthesis is not present
    assert "id: 'nuevo_mapa'" not in app_js
    assert "08   SÍNTESIS" not in app_js
    assert "08   SINTESIS" not in app_js
    
    # Check count of chapters in CHAPTERS array: 8 substantive chapters (01 to 08)
    ch_idx = app_js.find("const CHAPTERS =")
    end_idx = app_js.find("const JOURNEY_NODES")
    ch_matches = re.findall(r"num:\s*'(\d+)'", app_js[ch_idx:end_idx])
    assert ch_matches == ['01', '02', '03', '04', '05', '06', '07', '08'], f"Expected 8 chapters 01-08, found: {ch_matches}"
    
    # Chapter 08 is Argentina en el mundo
    assert "id: 'argentina_mundo'" in app_js
    assert "ESCALA GLOBAL · EIA 2024" in app_js
    
    # 2. Exactly 8 nodes in JOURNEY_NODES
    node_matches = re.findall(r"\{\s*x:\s*\d+,\s*y:\s*\d+,\s*ch:\s*(\d+)\s*\}", app_js[end_idx:end_idx+600])
    assert len(node_matches) == 8, f"Expected 8 journey nodes, found: {len(node_matches)}"

def test_v7_simplified_masthead_and_compact_layer_controls():
    """Validates V7 simplified header (only Relato continuo) and compact layer toggle integration."""
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    
    # Header buttons removed
    assert 'id="btn-preguntas"' not in html_content
    assert 'id="btn-toggle-layers"' not in html_content
    assert 'id="btn-metodologia"' not in html_content
    
    # Modals and drawers removed
    assert 'id="modal-preguntas"' not in html_content
    assert 'id="layers-drawer"' not in html_content
    assert 'id="modal-metodologia"' not in html_content
    
    # Relato continuo remains active
    assert 'id="btn-auto-tour"' in html_content
    assert 'Relato continuo' in html_content
    
    # Compact chapter layer toggle is integrated in updateFilterBar
    assert "layerConfigs" in app_js
    assert "layer-toggle-basins" in app_js

def test_v7_translucent_reactive_overlay_styling():
    """Validates V7 reactive translucent overlay styling in rest vs hover/focus-within."""
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    
    # Rest state translucency tokens
    assert "--panel-bg-translucent: rgba(13, 16, 21, 0.68);" in css_content
    assert "--panel-bg-opaque: rgba(13, 16, 21, 0.94);" in css_content
    
    # Panel rule uses background-color translucency, never container opacity
    assert "background-color: var(--panel-bg-translucent);" in css_content
    assert ".chart-overlay-panel:hover," in css_content
    assert ".chart-overlay-panel:focus-within" in css_content
    assert "background-color: var(--panel-bg-opaque);" in css_content
    
    # Overlay KPI card has subtle translucency
    assert "background: rgba(255, 255, 255, 0.02);" in css_content

def test_v7_islas_malvinas_cartography():
    """Validates that 'ISLAS MALVINAS' is present and English 'Falkland Islands' is excluded via filter."""
    style_content = (BASE_DIR / "frontend" / "styles" / "petroleo-map-style.json").read_text(encoding="utf-8")
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    
    # In style JSON
    assert "islas-malvinas-source" in style_content
    assert "islas-malvinas-label" in style_content
    assert "ISLAS MALVINAS" in style_content
    assert "-59.5" in style_content
    assert "-51.75" in style_content
    
    # Exclusion filter explicitly suppresses Falkland Islands
    assert 'Falkland Islands' in style_content
    assert '"!="' in style_content
    
    # In app.js layer builder
    assert "islas-malvinas-source" in app_js
    assert "islas-malvinas-label" in app_js
    assert "ISLAS MALVINAS" in app_js
    assert "Falkland Islands" in app_js

def test_v7_absence_of_false_record_claims_and_explicit_units():
    """Validates that '(Récord)' is removed, variation is dynamic vs prev year, and units are explicit."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    
    # No '(Récord)' badge
    assert "(Récord)" not in app_js
    
    # Dynamic annual variation logic
    assert "prevItem = timelineData.find(d => d.anio === yr - 1)" in app_js
    assert "% vs" in app_js
    
    # Scrubber label uses explicit units
    assert 'id="scrubber-prod-label">46.438,5 miles de m³<' in html_content
    assert "miles de m³" in app_js
    assert "barriles/día" in app_js
    
    # Ambiguous standalone 'Mm³' label removed from Chapter 01
    assert "${Number(item.prod_pet_miles_m3).toLocaleString('es-AR')} Mm³" not in app_js

def test_v6_reserved_right_rail_and_overlay_spacing():
    """Validates that the right rail has an exclusive strip at right: 18px and chart overlay is offset to right: 76px."""
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    
    # Right vertical index is at right: 18px and z-index: 50 (above overlays)
    assert "right: 18px;" in css_content
    assert "z-index: 50;" in css_content
    
    # Journey nodes have expanded touch/click area (32x32)
    assert "width: 32px;" in css_content
    assert "height: 32px;" in css_content
    
    # Chart overlay panel has reserved buffer (right: 76px and z-index: 40)
    assert "right: 76px;" in css_content
    assert "z-index: 40;" in css_content

def test_v6_unified_panel_design_tokens():
    """Validates that all panels share the exact same dark neutral background and design tokens."""
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    
    assert "--panel-bg: rgba(13, 16, 21, 0.92);" in css_content
    assert "--panel-border: 1px solid rgba(255, 255, 255, 0.08);" in css_content
    assert "--panel-radius: 8px;" in css_content
    
    # Verify story-column, chart-overlay-panel, filter-bar, and timeline use unified tokens
    assert "background: var(--panel-bg);" in css_content
    assert "backdrop-filter: var(--panel-backdrop);" in css_content
    
    # Verify olive/brown background is eliminated from chart overlay
    assert "background: rgba(26, 27, 22, 0.88);" not in css_content
    assert "background: rgba(20, 22, 17, 0.88);" not in css_content

def test_v6_filter_bar_labels_and_reset_view():
    """Validates that filter controls have explicit labels, custom styling, and reset button is 'Restablecer vista'."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    
    # Filter field groups and labels
    assert "filter-field-group" in app_js
    assert "filter-field-label" in app_js
    assert ".filter-field-group" in css_content
    assert ".filter-field-label" in css_content
    
    # Chapter 01 has 'Período' label
    assert "label: 'Período'" in app_js
    
    # Reset button label matches its effect: 'Restablecer vista'
    assert "Restablecer vista" in html_content

def test_v8_app_js_syntax_balance():
    """Validates that frontend/app.js has zero syntax/delimiter errors."""
    app_js_path = BASE_DIR / "frontend" / "app.js"
    content = app_js_path.read_text(encoding="utf-8")
    
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    in_single = False
    in_double = False
    in_backtick = False
    in_line_comment = False
    in_block_comment = False
    
    i = 0
    while i < len(content):
        c = content[i]
        nxt = content[i+1] if i + 1 < len(content) else ''
        
        if in_line_comment:
            if c == '\n': in_line_comment = False
        elif in_block_comment:
            if c == '*' and nxt == '/':
                in_block_comment = False
                i += 1
        elif in_single:
            if c == '\\': i += 1
            elif c == "'": in_single = False
        elif in_double:
            if c == '\\': i += 1
            elif c == '"': in_double = False
        elif in_backtick:
            if c == '\\': i += 1
            elif c == '`': in_backtick = False
        else:
            if c == '/' and nxt == '/':
                in_line_comment = True
                i += 1
            elif c == '/' and nxt == '*':
                in_block_comment = True
                i += 1
            elif c == "'": in_single = True
            elif c == '"': in_double = True
            elif c == '`': in_backtick = True
            elif c in '({[':
                stack.append(c)
            elif c in ')}]':
                assert stack, f"Unmatched closing delimiter {c}"
                top = stack.pop()
                assert top == pairs[c], f"Mismatched delimiter: {top} closed with {c}"
        i += 1
        
    assert not stack, f"Unclosed delimiters remaining: {stack}"

def test_v8_hero_photographic_assets_and_credits():
    """Validates real photographic background asset, fallback, and discreet credit in hero splash."""
    img_path = BASE_DIR / "frontend" / "assets" / "portada_vaca_muerta.jpg"
    assert img_path.exists(), "Missing photographic hero image asset"
    assert img_path.stat().st_size > 50000, "Hero image file size is too small"
    
    from PIL import Image
    im = Image.open(img_path)
    assert im.size[0] >= 1900, f"Expected panoramic image >= 1900px wide, got {im.size[0]}"
    assert im.size[1] >= 1000, f"Expected height >= 1000px, got {im.size[1]}"
    
    # Check HTML markup for credit
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    assert "hero-photo-credit" in html_content
    assert "Aguada Pichana, Añelo" in html_content
    assert "Horacio Fernandez" in html_content
    assert "CC BY 3.0" in html_content
    
    # Check CSS for photographic background, fallback and localized overlay
    css_content = (BASE_DIR / "frontend" / "index.css").read_text(encoding="utf-8")
    assert "url('./assets/portada_vaca_muerta.jpg')" in css_content
    assert "background-color: #0c1017;" in css_content
    assert ".hero-splash-backdrop" in css_content
    assert "radial-gradient" in css_content

def test_v8_hero_splash_accessibility_and_focus():
    """Validates keyboard accessibility, focus transfer, inert, aria-hidden, and double-click protection."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    html_content = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    
    # Hero splash has role and aria-label
    assert 'role="region"' in html_content
    assert 'aria-label="Portada editorial"' in html_content
    
    # Start button has accessibility title and aria-label
    assert 'aria-label="Comenzar el recorrido narrativo por los 7 capítulos"' in html_content
    
    # Double-click prevention and loading state
    assert "let isDataLoaded = false;" in app_js
    assert "let hasEnteredTour = false;" in app_js
    assert "let pendingTourEntry = false;" in app_js
    assert "function executeTourEntry()" in app_js
    assert "splash.setAttribute('aria-hidden', 'true')" in app_js
    assert "splash.setAttribute('inert', '')" in app_js
    assert "nextBtn.focus()" in app_js

def test_v8_headless_browser_entry_regression():
    """Live headless browser test: checks page load, absence of errors, click, and Chapter 01 transition."""
    from selenium import webdriver
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.common.by import By
    import time
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    
    driver = webdriver.Edge(options=options)
    try:
        driver.get('http://127.0.0.1:8000/')
        time.sleep(2.0)
        
        # Verify no severe console errors
        logs = driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE' and 'favicon' not in l['message']]
        assert len(severe) == 0, f"Found severe console errors: {severe}"
        
        # Verify hero splash and start button
        start_btn = driver.find_element(By.ID, 'btn-start-tour')
        assert start_btn.is_displayed()
        
        # Click start button
        start_btn.click()
        time.sleep(2.0)
        
        # Verify splash is hidden
        splash = driver.find_element(By.ID, 'hero-splash')
        assert 'hero-hidden' in splash.get_attribute('class')
        assert splash.get_attribute('aria-hidden') == 'true'
        
        # Verify active chapter 01
        ch_badge = driver.find_element(By.ID, 'chapter-num')
        ch_num = (ch_badge.text or ch_badge.get_attribute('textContent') or '').strip()
        assert ch_num == '01'
        
        # Verify focus shifted
        active_el = driver.switch_to.active_element
        assert active_el.tag_name == 'button'
        assert active_el.get_attribute('id') in ['btn-next-chapter', 'btn-auto-tour']
    finally:
        driver.quit()

def test_v9_typography_two_families_only():
    """Validates that exactly two typographic families (Alegreya + Archivo) are specified and available."""
    html_path = BASE_DIR / "frontend" / "index.html"
    css_path = BASE_DIR / "frontend" / "index.css"
    fonts_dir = BASE_DIR / "frontend" / "fonts"
    
    html = html_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    
    # Check HTML loads Alegreya and Archivo
    assert "family=Alegreya:ital,wght@0,400..900;1,400..900" in html
    assert "family=Archivo:ital,wght@0,100..900;1,100..900" in html
    assert "fonts_local.css" in html
    
    # Check CSS custom properties
    assert "--font-serif: 'Alegreya', Georgia, serif;" in css
    assert "--font-sans: 'Archivo'," in css
    assert "--font-mono: 'Archivo'," in css
    
    # Check local font files and licenses (legitimate Google Fonts variable subsets)
    assert (fonts_dir / "alegreya-variable-normal-latin.woff2").exists()
    assert (fonts_dir / "alegreya-variable-italic-latin.woff2").exists()
    assert (fonts_dir / "archivo-variable-normal-latin.woff2").exists()
    assert (fonts_dir / "archivo-variable-italic-latin.woff2").exists()
    assert (fonts_dir / "OFL_Alegreya.txt").exists()
    assert (fonts_dir / "OFL_Archivo.txt").exists()

def test_v9_no_scroll_wheel_navigation():
    """Validates removal of scroll wheel chapter navigation and presence of panel isolation."""
    app_js_path = BASE_DIR / "frontend" / "app.js"
    app_js = app_js_path.read_text(encoding="utf-8")
    
    assert "setupScrollWheelNavigation" not in app_js, "Scroll wheel chapter navigation must be completely removed"
    assert "setupPanelWheelIsolation" in app_js, "Panel wheel isolation must be implemented"
    assert "e.stopPropagation()" in app_js

def test_v11_dino_guide_data_commentary_and_hallazgos_reales():
    """Validates V11 Argentinosaurus data commentary with real verified figures, UN DATO MÁS label, and sources."""
    html_path = BASE_DIR / "frontend" / "index.html"
    dino_img_path = BASE_DIR / "frontend" / "assets" / "argentinosaurus-guia.png"
    app_js_path = BASE_DIR / "frontend" / "app.js"
    css_path = BASE_DIR / "frontend" / "index.css"
    
    assert dino_img_path.exists(), "Argentinosaurus mascot image missing"
    assert dino_img_path.stat().st_size > 50000, "Argentinosaurus mascot image appears incomplete or too small"
    
    html = html_path.read_text(encoding="utf-8")
    assert 'id="dino-guide-floating"' in html, "Independent floating dino guide container required"
    assert 'id="btn-toggle-dino"' in html
    assert 'id="dino-speech-bubble"' in html
    assert 'id="dino-speech-source"' in html, "Dino source attribution element required in V11"
    assert 'id="btn-dino-pill"' in html
    assert 'UN DATO MÁS' in html, "Header label must be UN DATO MÁS in V11"
    assert 'Un dato más' in html, "Pill button text must be Un dato más in V11"
    assert 'id="dino-guide-stage"' not in html, "Dino guide must NOT be inside active-story-card stage"
    
    css = css_path.read_text(encoding="utf-8")
    assert ".dino-highlight" in css, "Highlight class required in CSS"
    assert ".dino-source-hint" in css, "Source hint class required in CSS"
    assert "dinoBreathe" in css
    
    app_js = app_js_path.read_text(encoding="utf-8")
    assert "getDinoDataCommentary(" in app_js, "getDinoDataCommentary required in V11"
    assert "getDinoMessage(" in app_js
    assert "updateDinoGuide(" in app_js
    assert "dino-highlight" in app_js
    assert "dino-popup-active" in app_js
    
    # Generic V10 messages must be removed
    assert "Compará porcentajes y volúmenes" not in app_js
    assert "Ambos son recursos naturales" not in app_js
    assert "El volumen anual suma todo lo producido" not in app_js
    
    # Real verified figures must be present in commentary
    assert "${gapPct}% por debajo" in app_js
    assert "49.148 miles de m³" in app_js
    assert "91,8% del petróleo" in app_js
    assert "37,0 puntos porcentuales" in app_js
    assert "22,9% del crudo" in app_js
    assert "+218%" in app_js
    assert "1.590 m³/mes" in app_js
    assert "5,1% en 2024" in app_js

def test_v10_well_pump_icons_and_absence_of_photo_pins():
    """Validates transparent well pump icon layer, analytical popup, and removal of HTML photo pins."""
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    html = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    
    # Well pump icon asset exists
    icon_asset = BASE_DIR / "frontend" / "assets" / "icono-pozo-petrolero-opt.png"
    assert icon_asset.exists(), "Optimized well pump icon asset missing"
    assert icon_asset.stat().st_size > 1000, "Well pump icon asset too small"
    
    # Layer and registration in app.js
    assert "wells-icons" in app_js
    assert "well-pump-icon" in app_js
    assert "icono-pozo-petrolero-opt.png" in app_js
    assert "loadWellPumpIcon" in app_js
    assert "showWellPopup" in app_js
    assert "editorial-well-popup" in app_js
    
    # Absence of HTML photo markers and photo modal
    assert "map-photo-pin" not in html
    assert "photo-detail-modal" not in html
    assert "PHOTO_INVENTORY" not in app_js
    assert "setupPhotoMarkers" not in app_js

def test_v9_hero_photo_credits_active_links():
    """Validates active clickable links and verified metadata in the hero photo credit."""
    html = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    assert 'class="hero-photo-credit"' in html
    assert 'href="https://commons.wikimedia.org/wiki/File:%22Petrosaurios%22,_Aguada_Pichana,_A%C3%B1elo,_Neuquen,_ARG._-_panoramio_(1).jpg"' in html
    assert 'href="https://creativecommons.org/licenses/by/3.0/deed.es"' in html

def test_v12_periodos_modos_argentina_mundo():
    """Validates Iteration V12: period filter fix, Relato/Explorar modes, and Chapter 08 international data."""
    html = (BASE_DIR / "frontend" / "index.html").read_text(encoding="utf-8")
    app_js = (BASE_DIR / "frontend" / "app.js").read_text(encoding="utf-8")
    data_bundle = (BASE_DIR / "frontend" / "data_bundle.js").read_text(encoding="utf-8")
    
    # 1. Mode toggles have descriptive titles and ARIA labels
    assert 'title="Vista preparada de cada capítulo"' in html
    assert 'aria-label="Modo Relato: Vista preparada de cada capítulo"' in html
    assert 'title="Elegí filtros y períodos"' in html
    assert 'aria-label="Modo Explorar: Elegí filtros y períodos"' in html
    
    # 2. Centralized CHAPTER_DEFAULTS for all 8 chapters
    assert "CHAPTER_DEFAULTS = {" in app_js
    for ch_key in ['regreso', 'mapa_se_mueve', 'punto_quiebre', 'pocos_pozos', 'como_cambio_el_pozo', 'generaciones_pozos', 'del_pozo_al_pais', 'argentina_mundo']:
        assert f"{ch_key}:" in app_js, f"Missing default entry for {ch_key}"
        
    # 3. Chapter 01 period filter avoids type coercion bug
    assert "f.field === 'paretoCutoff'" in app_js
    assert "appState.filters[f.field] = String(val);" in app_js
    assert "timeRange === '2000'" in app_js
    assert "timeRange === '2017'" in app_js
    
    # 4. Verified international crude data (EIA 2024)
    world_json_path = STATIC_DATA_DIR / "world_crude_production.json"
    assert world_json_path.exists(), "world_crude_production.json missing"
    world_data = json.loads(world_json_path.read_text(encoding="utf-8"))
    
    meta = world_data["metadata"]
    assert meta["product_id"] == 57
    assert meta["activity_id"] == 1
    assert meta["year"] == 2024
    assert meta["total_countries_with_data"] == 99
    assert abs(meta["world_total_tbpd"] - 81958.2) < 0.1
    assert abs(meta["argentina_tbpd_2024"] - 700.8) < 0.1
    assert meta["argentina_global_rank_2024"] == 22
    assert abs(meta["argentina_global_share_pct"] - 0.86) < 0.05
    assert meta["argentina_latam_rank_2024"] == 5
    assert abs(meta["argentina_latam_share_pct"] - 8.0) < 0.1
    
    # Evolution Base 100 = 2017
    evo = world_data["evolution_base_2017"]
    evo_2024 = next(d for d in evo if d["year"] == 2024)
    assert abs(evo_2024["arg_index"] - 146.1) < 0.1, f"Expected 146.1 (+46.1%), got {evo_2024['arg_index']}"
    assert abs(evo_2024["world_index"] - 100.9) < 0.1, f"Expected 100.9 (+0.9%), got {evo_2024['world_index']}"
    
    # 5. World data bundled for offline resiliency
    assert "world_crude_production" in data_bundle
    
    # 6. Chapter 08 exists in app.js with renderWorldChart and dynamic callouts
    assert "id: 'argentina_mundo'" in app_js
    assert "renderWorldChart(state)" in app_js
    assert "worldScope === 'latam'" in app_js
    assert "worldView === 'evolution'" in app_js
    
    # 7. Dino data commentary has Chapter 01 timeRange and Chapter 08 EIA insights
    assert "num === '08' || id === 'argentina_mundo'" in app_js
    assert "puesto #22 global" in app_js
    assert "+46,1%" in app_js
    assert "700,8 miles de bpd" in app_js





