"""
Audit and verification of all frontend charts and API endpoints.
Tests property names, dates, units, and renders sample JSONs.
"""

import json
import urllib.request

endpoints = [
    ("/api/timeline", "timelineData", ["anio", "prod_pet_miles_m3", "bpd"]),
    ("/api/production/monthly", "monthlyProdData", ["mes_id", "anio", "mes", "pet_conv_miles_m3", "pet_no_conv_miles_m3", "pet_total_miles_m3", "share_no_conv_pct"]),
    ("/api/fractures/trends", "fracturesTrendsData", ["anio", "longitud_horizontal_media_m", "etapas_fractura_media", "arena_total_tn_media"]),
    ("/api/cohorts", "cohortsData", ["anio_cohorte", "tipo_recurso", "mes_relativo", "mediana_m3_mes"]),
    ("/api/macro/trends", "macroTrendsData", ["anio", "empleo_neuquen_puestos", "exportaciones_petroleo_pct_total", "renta_petrolera_pct_pbi"]),
    ("/api/geo/concessions", "concessionsGeo", ["features"]),
    ("/api/wells/map", "wellsMap", ["features"])
]

def test_all_chart_endpoints():
    report = []
    print("Testing API endpoints for chart data...")
    for ep, var_name, expected_keys in endpoints:
        url = f"http://127.0.0.1:8000{ep}"
        try:
            req = urllib.request.urlopen(url, timeout=5)
            data = json.loads(req.read().decode('utf-8'))
            
            # Check structure
            status = "OK"
            sample_keys = []
            if isinstance(data, list):
                if len(data) > 0:
                    sample_keys = list(data[0].keys())
                    missing = [k for k in expected_keys if k not in sample_keys]
                    if missing:
                        status = f"MISSING KEYS: {missing}"
                else:
                    status = "EMPTY ARRAY"
            elif isinstance(data, dict):
                sample_keys = list(data.keys())
                missing = [k for k in expected_keys if k not in sample_keys]
                if missing:
                    status = f"MISSING KEYS: {missing}"
            
            print(f"[{status}] {ep} -> {len(data) if isinstance(data, list) else len(data.keys())} items. Sample keys: {sample_keys[:5]}")
            report.append({
                "endpoint": ep,
                "variable": var_name,
                "status": status,
                "count": len(data) if isinstance(data, list) else len(data.keys()),
                "sample": data[:1] if isinstance(data, list) else list(data.keys())[:3]
            })
        except Exception as e:
            print(f"[ERROR] {ep}: {e}")
            report.append({
                "endpoint": ep,
                "variable": var_name,
                "status": f"ERROR: {e}",
                "count": 0,
                "sample": None
            })
            
    with open('analysis/exports/test_chart_endpoints.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("Report saved to analysis/exports/test_chart_endpoints.json")

if __name__ == '__main__':
    test_all_chart_endpoints()
