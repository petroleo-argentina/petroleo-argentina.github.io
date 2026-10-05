import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DATA_DIR = BASE_DIR / "api" / "static_data"
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Petróleo en Argentina: Del Pozo al País",
    description="API de datos y visualizaciones para la plataforma de historia visual",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json(filename: str):
    p = STATIC_DATA_DIR / filename
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    return json.loads(p.read_text(encoding="utf-8"))

@app.get("/api/kpis")
def get_kpis():
    return {
        "record_year": 2025,
        "total_oil_2025_km3": 46438.5,
        "total_oil_2025_bpd": 798450,
        "growth_since_2017_pct": 63.9,
        "shale_share_pct": 62.9,
        "total_active_wells": 27165,
        "shale_active_wells": 3564,
        "avg_horizontal_length_m": 3078,
        "avg_frac_stages": 51.8,
        "neuquen_share_pct": 64.7
    }

@app.get("/api/timeline")
def get_timeline():
    return load_json("timeline_1950_2025.json")

@app.get("/api/production/monthly")
def get_production_monthly():
    return load_json("conv_vs_noconv_monthly.json")

@app.get("/api/cohorts")
def get_cohorts():
    return load_json("cohorts_decay_curves.json")

@app.get("/api/wells/map")
def get_wells_map():
    return load_json("wells_map_sample.json")

@app.get("/api/fractures/trends")
def get_fractures_trends():
    return load_json("technical_fractures_trends.json")

@app.get("/api/macro/trends")
def get_macro_trends():
    return load_json("macro_employment_trends.json")

@app.get("/api/operators")
def get_operators():
    return load_json("top_operators_2025.json")

@app.get("/api/geo/basins")
def get_geo_basins():
    return load_json("geo_basins.json")

@app.get("/api/geo/concessions")
def get_geo_concessions():
    return load_json("geo_concessions_vaca_muerta.json")

@app.get("/api/geo/trajectories")
def get_geo_trajectories():
    return load_json("geo_trajectories_sample.json")

@app.get("/api/geo/pipelines")
def get_geo_pipelines():
    return load_json("geo_pipelines_sample.json")

@app.get("/api/geo/facilities")
def get_geo_facilities():
    return load_json("geo_refineries_ports.json")

@app.get("/api/geo/flaring")
def get_geo_flaring():
    return load_json("geo_flaring_sample.json")

@app.get("/api/pareto")
def get_pareto_curve():
    return {
        "total_pozos": 26219,
        "pareto_wells_50_pct": 912,
        "pareto_share_pct": 3.48,
        "milestones": [
            {"milestone": "Top 1%", "pozos": 262, "pct_pozos": 1.0, "pct_prod": 22.86},
            {"milestone": "Top 50%", "pozos": 912, "pct_pozos": 3.48, "pct_prod": 50.0},
            {"milestone": "Top 5%", "pozos": 1311, "pct_pozos": 5.0, "pct_prod": 58.22},
            {"milestone": "Top 66,7%", "pozos": 2021, "pct_pozos": 7.71, "pct_prod": 66.67},
            {"milestone": "Top 10%", "pozos": 2622, "pct_pozos": 10.0, "pct_prod": 70.98},
            {"milestone": "Total", "pozos": 26219, "pct_pozos": 100.0, "pct_prod": 100.0}
        ]
    }

@app.get("/api/world/crude")
def get_world_crude_production():
    return load_json("world_crude_production.json")

@app.get("/api/carto/config")
def get_carto_config():
    carto_cfg_path = BASE_DIR / "config" / "carto.json"
    if carto_cfg_path.exists():
        return json.loads(carto_cfg_path.read_text(encoding="utf-8"))
    return {
        "account": "",
        "accessToken": "",
        "apiBaseUrl": "https://gcp-us-east1.api.carto.com"
    }


# Serve frontend static assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
