import json
import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
STATIC_DATA_DIR = BASE_DIR / "api" / "static_data"
STATIC_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("--- Building Spatial Geo Data for Scrollytelling Map ---")

# 1. Productive Basins in Argentina
basins = [
    {
        "id": "neuquina",
        "nombre": "Cuenca Neuquina",
        "provincias": ["Neuquén", "Río Negro", "Mendoza", "La Pampa"],
        "centro": [-38.2, -68.9],
        "zoom": 7,
        "shale_epicenter": True,
        "prod_2025_km3": 33100.0,
        "share_2025_pct": 71.3,
        "descripcion": "Epicentro del petróleo argentino. Aloja la formación no convencional Vaca Muerta, responsable del 63% del crudo nacional."
    },
    {
        "id": "golfo_san_jorge",
        "nombre": "Cuenca Golfo San Jorge",
        "provincias": ["Chubut", "Santa Cruz"],
        "centro": [-46.0, -68.2],
        "zoom": 7,
        "shale_epicenter": False,
        "prod_2025_km3": 9500.0,
        "share_2025_pct": 20.5,
        "descripcion": "La cuna del petróleo argentino desde 1907. Cuenca madura con declinación natural y fuerte presencia de recuperación secundaria y terciaria."
    },
    {
        "id": "cuyana",
        "nombre": "Cuenca Cuyana",
        "provincias": ["Mendoza"],
        "centro": [-33.5, -68.8],
        "zoom": 8,
        "shale_epicenter": False,
        "prod_2025_km3": 2100.0,
        "share_2025_pct": 4.5,
        "descripcion": "Yacimientos maduros históricos del norte y centro de Mendoza, con crudos pesados que abastecen a la refinería Luján de Cuyo."
    },
    {
        "id": "austral",
        "nombre": "Cuenca Austral",
        "provincias": ["Santa Cruz", "Tierra del Fuego"],
        "centro": [-52.5, -69.5],
        "zoom": 7,
        "shale_epicenter": False,
        "prod_2025_km3": 1300.0,
        "share_2025_pct": 2.8,
        "descripcion": "Cuenca austral continental y offshore, con predominio de producción gasífera y condensados."
    },
    {
        "id": "noroeste",
        "nombre": "Cuenca Noroeste",
        "provincias": ["Salta", "Jujuy"],
        "centro": [-23.0, -64.0],
        "zoom": 7,
        "shale_epicenter": False,
        "prod_2025_km3": 438.5,
        "share_2025_pct": 0.9,
        "descripcion": "Yacimientos históricos de alta madurez y complejidad geológica estructural (Acambuco, Campo Durán)."
    }
]

(STATIC_DATA_DIR / "geo_basins.json").write_text(json.dumps(basins, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Saved geo_basins.json ({len(basins)} basins)")

# 2. Vaca Muerta Megayacimientos (Core Concessions)
concessions = [
    {
        "id": "loma_campana",
        "nombre": "Loma Campana",
        "operador": "YPF S.A. / Chevron",
        "lat": -38.305,
        "lon": -68.960,
        "radio_km": 11,
        "prod_2025_bpd": 92400,
        "prod_2025_m3_mes": 445000,
        "pozos_activos": 740,
        "tipo": "Shale Oil",
        "destacado": "El yacimiento no convencional más grande de América Latina fuera de EE.UU."
    },
    {
        "id": "la_amarga_chica",
        "nombre": "La Amarga Chica",
        "operador": "YPF S.A. / Petronas",
        "lat": -38.210,
        "lon": -68.865,
        "radio_km": 9,
        "prod_2025_bpd": 68300,
        "prod_2025_m3_mes": 328000,
        "pozos_activos": 390,
        "tipo": "Shale Oil",
        "destacado": "Segundo mayor productor de Vaca Muerta con pozos de altísima productividad inicial."
    },
    {
        "id": "bandurria_sur",
        "nombre": "Bandurria Sur",
        "operador": "YPF S.A. / Schlumberger / Equinor",
        "lat": -38.385,
        "lon": -68.995,
        "radio_km": 8,
        "prod_2025_bpd": 54100,
        "prod_2025_m3_mes": 260000,
        "pozos_activos": 260,
        "tipo": "Shale Oil",
        "destacado": "Bloque clave del hub sur operado con ramas horizontales de hasta 3.800 metros."
    },
    {
        "id": "bajada_del_palo_oeste",
        "nombre": "Bajada del Palo Oeste",
        "operador": "Vista Energy",
        "lat": -38.160,
        "lon": -68.530,
        "radio_km": 10,
        "prod_2025_bpd": 61200,
        "prod_2025_m3_mes": 294000,
        "pozos_activos": 280,
        "tipo": "Shale Oil",
        "destacado": "El mayor desarrollo privado en Vaca Muerta con récords de velocidad de perforación."
    },
    {
        "id": "la_calera",
        "nombre": "La Calera",
        "operador": "Pluspetrol / YPF",
        "lat": -38.370,
        "lon": -68.990,
        "radio_km": 8,
        "prod_2025_bpd": 28500,
        "prod_2025_m3_mes": 137000,
        "pozos_activos": 135,
        "tipo": "Wet Gas & Light Oil",
        "destacado": "Desarrollo masivo en ventana de condensados y petróleo volátil."
    },
    {
        "id": "fortin_de_piedra",
        "nombre": "Fortín de Piedra",
        "operador": "Tecpetrol",
        "lat": -38.450,
        "lon": -69.210,
        "radio_km": 10,
        "prod_2025_bpd": 18200,
        "prod_2025_m3_mes": 87500,
        "pozos_activos": 160,
        "tipo": "Shale Gas & Condensado",
        "destacado": "El principal productor de gas del país con producción de líquidos asociada."
    }
]

(STATIC_DATA_DIR / "geo_concessions_vaca_muerta.json").write_text(json.dumps(concessions, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Saved geo_concessions_vaca_muerta.json ({len(concessions)} concessions)")

# 3. Extract sample of horizontal well trajectories (from trayectorias-de-pozo-vaca-muerta.csv)
traj_csv = RAW_DIR / "energia" / "trayectorias-de-pozo-vaca-muerta.csv"
trajectories = []

if traj_csv.exists():
    with open(traj_csv, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            geo_str = row.get("geojson", "")
            if not geo_str or "MultiLineString" not in geo_str:
                continue
            try:
                geo_obj = json.loads(geo_str)
                coords = geo_obj.get("coordinates", [])
                if not coords or len(coords[0]) < 10:
                    continue
                # Downsample line points to keep lightweight (e.g., take every 6th coordinate)
                line = coords[0]
                sampled_line = [line[i] for i in range(0, len(line), 6)]
                if sampled_line[-1] != line[-1]:
                    sampled_line.append(line[-1])
                
                # Leaflet uses [lat, lon], geojson is [lon, lat]
                leaflet_coords = [[round(pt[1], 5), round(pt[0], 5)] for pt in sampled_line]
                
                trajectories.append({
                    "sigla": row.get("sigla"),
                    "largo_m": float(row.get("largo_rama_horizontal_mt") or 0),
                    "tvd_m": float(row.get("profundidad_vertical_mt") or 0),
                    "md_m": float(row.get("profundidad_final_total_mt") or 0),
                    "fecha": (row.get("termfin") or row.get("termini") or "")[:10],
                    "path": leaflet_coords
                })
                count += 1
                if count >= 80: # 80 high quality representative trajectories
                    break
            except Exception as e:
                continue

(STATIC_DATA_DIR / "geo_trajectories_sample.json").write_text(json.dumps(trajectories, indent=2), encoding="utf-8")
print(f"[OK] Saved geo_trajectories_sample.json ({len(trajectories)} horizontal trajectories)")

# 4. Refineries and Export Ports
refineries_and_ports = [
    {
        "tipo": "Puerto Exportador",
        "nombre": "Puerto Rosales / Punta Cigüeña (Bahía Blanca)",
        "lat": -38.922,
        "lon": -62.068,
        "capacidad": "Terminal marítima principal de crudo Medanito de exportación",
        "icono": "anchor",
        "cuenca": "Atlántico / Vía Oldelval"
    },
    {
        "tipo": "Puerto Exportador",
        "nombre": "Caleta Córdova (Chubut)",
        "lat": -45.753,
        "lon": -67.362,
        "capacidad": "Terminal marítima de crudo Escalante (Golfo San Jorge)",
        "icono": "anchor",
        "cuenca": "Golfo San Jorge"
    },
    {
        "tipo": "Puerto Exportador",
        "nombre": "Caleta Olivia (Santa Cruz)",
        "lat": -46.438,
        "lon": -67.514,
        "capacidad": "Monoboya de carga de crudo pesado",
        "icono": "anchor",
        "cuenca": "Golfo San Jorge"
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería La Plata (YPF)",
        "lat": -34.889,
        "lon": -57.913,
        "capacidad": "31.000 m³/día (~195.000 bpd) - La mayor del país",
        "icono": "factory",
        "empresa": "YPF S.A."
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería Luján de Cuyo (YPF)",
        "lat": -33.066,
        "lon": -68.976,
        "capacidad": "19.000 m³/día (~120.000 bpd)",
        "icono": "factory",
        "empresa": "YPF S.A."
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería Campana (Axion Energy)",
        "lat": -34.160,
        "lon": -58.946,
        "capacidad": "15.000 m³/día (~95.000 bpd)",
        "icono": "factory",
        "empresa": "Pan American Energy"
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería Dock Sud (Raízen - Shell)",
        "lat": -34.653,
        "lon": -58.335,
        "capacidad": "17.000 m³/día (~108.000 bpd)",
        "icono": "factory",
        "empresa": "Raízen Argentina"
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería Bahía Blanca (Trafigura - Puma)",
        "lat": -38.745,
        "lon": -62.296,
        "capacidad": "5.000 m³/día (~31.500 bpd)",
        "icono": "factory",
        "empresa": "Trafigura"
    },
    {
        "tipo": "Refinería",
        "nombre": "Refinería Plaza Huincul (YPF)",
        "lat": -38.927,
        "lon": -69.186,
        "capacidad": "4.200 m³/día (~26.500 bpd) - Ubicada en Neuquén",
        "icono": "factory",
        "empresa": "YPF S.A."
    }
]

(STATIC_DATA_DIR / "geo_refineries_ports.json").write_text(json.dumps(refineries_and_ports, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Saved geo_refineries_ports.json ({len(refineries_and_ports)} facilities)")

# 5. Strategic Trunk Pipelines (Oldelval, Otasa, Vaca Muerta Sur)
pipelines = [
    {
        "id": "oldelval",
        "nombre": "Oleoducto del Valle (Oldelval)",
        "tipo": "OLEODUCTO",
        "origen": "Allen / Puesto Hernández (Neuquén/Río Negro)",
        "destino": "Puerto Rosales / Bahía Blanca (Buenos Aires)",
        "capacidad_bpd": "450.000 bpd (Proyecto Duplicar)",
        "estado": "Operativo / En Expansión",
        "descripcion": "La principal arteria de evacuación de petróleo de Vaca Muerta hacia las refinerías y la terminal marítima de exportación en el Atlántico.",
        "path": [
            [-37.85, -69.75],
            [-38.30, -68.96],
            [-38.98, -67.99],
            [-39.03, -67.57],
            [-39.11, -66.50],
            [-38.72, -64.10],
            [-38.74, -62.30],
            [-38.92, -62.07]
        ]
    },
    {
        "id": "otasa",
        "nombre": "Oleoducto Trasandino (Otasa)",
        "tipo": "OLEODUCTO",
        "origen": "Puesto Hernández (Neuquén)",
        "destino": "Refinería Biobío / Talcahuano (Chile - Océano Pacífico)",
        "capacidad_bpd": "115.000 bpd",
        "estado": "Reactivado (2023)",
        "descripcion": "Cruce cordillerano que conecta la Cuenca Neuquina con el Pacífico, permitiendo exportar crudo liviano a Chile y mercados asiáticos.",
        "path": [
            [-38.30, -68.96],
            [-37.85, -69.75],
            [-37.38, -70.52],
            [-37.05, -71.15],
            [-36.80, -72.00],
            [-36.72, -73.12]
        ]
    },
    {
        "id": "vm_sur",
        "nombre": "Proyecto Vaca Muerta Sur (YPF & Consorcio)",
        "tipo": "OLEODUCTO (EN CONSTRUCCIÓN)",
        "origen": "Loma Campana (Añelo, Neuquén)",
        "destino": "Punta Colorada / Golfo San Matías (Río Negro)",
        "capacidad_bpd": "390.000 bpd",
        "estado": "En construcción / Financiado RIGI",
        "descripcion": "Nuevo ducto de 570 km dedicado íntegramente a la exportación de gran calado (VLCC) en aguas profundas del Atlántico.",
        "path": [
            [-38.30, -68.96],
            [-38.60, -68.10],
            [-39.20, -67.20],
            [-39.80, -66.10],
            [-40.90, -65.30],
            [-41.70, -65.02]
        ]
    }
]

(STATIC_DATA_DIR / "geo_pipelines_sample.json").write_text(json.dumps(pipelines, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Saved geo_pipelines_sample.json ({len(pipelines)} trunk pipelines)")

# 6. Flaring & Venting Sample
flaring_sample = [
    {"nombre": "Antorcha EPF Bajo del Choique", "operador": "ExxonMobil", "lat": -37.7132, "lon": -69.1416, "tipo": "Antorcha declarada"},
    {"nombre": "Batería Loma Campana Este", "operador": "YPF S.A.", "lat": -38.2910, "lon": -68.9450, "tipo": "Antorcha declarada"},
    {"nombre": "Planta Compresora La Calera", "operador": "Pluspetrol", "lat": -38.3620, "lon": -69.0120, "tipo": "Chimenea de quema"},
    {"nombre": "Venteo de Control Bandurria Sur", "operador": "YPF S.A.", "lat": -38.3750, "lon": -68.9800, "tipo": "Antorcha declarada"},
    {"nombre": "Batería Bajada del Palo Oeste", "operador": "Vista Energy", "lat": -38.1520, "lon": -68.5180, "tipo": "Antorcha declarada"},
    {"nombre": "Estación Compresora Loma de la Costa", "operador": "Tecpetrol", "lat": -46.2527, "lon": -67.6322, "tipo": "Chimenea de quema (Chubut)"}
]

(STATIC_DATA_DIR / "geo_flaring_sample.json").write_text(json.dumps(flaring_sample, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Saved geo_flaring_sample.json ({len(flaring_sample)} flaring points)")

print("--- All Spatial Geo Data Created Successfully! ---")
