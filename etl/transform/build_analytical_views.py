import os
import json
import logging
from pathlib import Path
import duckdb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_analytics")

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
API_DATA_DIR = BASE_DIR / "api" / "static_data"

def build():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    API_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    con = duckdb.connect()
    
    wells_p = (RAW_DIR / "petrodb" / "wells.parquet").as_posix()
    prod_glob = (RAW_DIR / "petrodb" / "monthly_production" / "*" / "data.parquet").as_posix()
    p1950_p = (RAW_DIR / "energia" / "serie-produccion-petroleo-total-pais-desde-1950.csv").as_posix()
    frac_p = (RAW_DIR / "energia" / "datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv").as_posix()
    emp_p = (RAW_DIR / "empleo" / "puestos_priv_provincia_clae2.csv").as_posix()
    
    # 1. Timeline 1950-2025 (Long-term national production)
    logger.info("Building 1. timeline_1950_2025...")
    # 1950 to 2005 from official historical series
    hist_df = con.execute(f"""
        SELECT 
            anio,
            round(produccion_petroleo, 1) as prod_pet_miles_m3,
            round(produccion_petroleo * 1000.0 / 365.0 * 6.28981, 0) as bpd,
            'OFICIAL_HISTORICA' as fuente
        FROM read_csv_auto('{p1950_p}')
        WHERE anio < 2006
        ORDER BY anio
    """).df()
    
    # 2006 to 2025 from pozo-level aggregation
    modern_df = con.execute(f"""
        SELECT 
            year(fecha) as anio,
            round(sum(prod_pet) / 1000.0, 1) as prod_pet_miles_m3,
            round(sum(prod_pet) / (case when year(fecha) in (2008, 2012, 2016, 2020, 2024) then 366.0 else 365.0 end) * 6.28981, 0) as bpd,
            'CAPITULO_IV_POZOS' as fuente
        FROM '{prod_glob}'
        GROUP BY 1
        ORDER BY 1
    """).df()
    
    timeline_full = pd.concat([hist_df, modern_df], ignore_index=True)
    timeline_full.to_parquet(PROCESSED_DIR / "timeline_1950_2025.parquet", index=False)
    (API_DATA_DIR / "timeline_1950_2025.json").write_text(timeline_full.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("Timeline 1950-2025 created: %d years.", len(timeline_full))

    # 2. Convencional vs No Convencional Monthly Series (2006-2025)
    logger.info("Building 2. conv_vs_noconv_monthly...")
    monthly_type = con.execute(f"""
        SELECT 
            strftime(p.fecha, '%Y-%m') as mes_id,
            year(p.fecha) as anio,
            month(p.fecha) as mes,
            round(sum(CASE WHEN w.tipo_recurso = 'NO CONVENCIONAL' THEN p.prod_pet ELSE 0 END) / 1e3, 2) as pet_no_conv_miles_m3,
            round(sum(CASE WHEN w.tipo_recurso = 'CONVENCIONAL' THEN p.prod_pet ELSE 0 END) / 1e3, 2) as pet_conv_miles_m3,
            round(sum(p.prod_pet) / 1e3, 2) as pet_total_miles_m3,
            count(distinct CASE WHEN p.prod_pet > 0 AND w.tipo_recurso = 'NO CONVENCIONAL' THEN p.idpozo END) as pozos_no_conv_activos,
            count(distinct CASE WHEN p.prod_pet > 0 AND w.tipo_recurso = 'CONVENCIONAL' THEN p.idpozo END) as pozos_conv_activos,
            count(distinct CASE WHEN p.prod_pet > 0 THEN p.idpozo END) as total_pozos_activos
        FROM '{prod_glob}' p
        JOIN '{wells_p}' w ON p.idpozo = w.idpozo
        GROUP BY 1, 2, 3
        ORDER BY 1
    """).df()
    monthly_type["share_no_conv_pct"] = (monthly_type["pet_no_conv_miles_m3"] * 100.0 / monthly_type["pet_total_miles_m3"]).round(1)
    monthly_type.to_parquet(PROCESSED_DIR / "conv_vs_noconv_monthly.parquet", index=False)
    (API_DATA_DIR / "conv_vs_noconv_monthly.json").write_text(monthly_type.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("Conv vs No Conv monthly created: %d months.", len(monthly_type))

    # 3. Cohort Curves (Decline curves by generation)
    logger.info("Building 3. cohorts_decay_curves...")
    cohorts_df = con.execute(f"""
        WITH first_prod AS (
            SELECT 
                p.idpozo,
                min(p.fecha) as fecha_inicio,
                year(min(p.fecha)) as cohorte
            FROM '{prod_glob}' p
            JOIN '{wells_p}' w ON p.idpozo = w.idpozo
            WHERE w.tipo_recurso = 'NO CONVENCIONAL' AND p.prod_pet > 0
            GROUP BY 1
        ),
        pozo_age AS (
            SELECT 
                p.idpozo,
                fp.cohorte,
                cast(round(date_diff('month', fp.fecha_inicio, p.fecha)) as INT) as mes_vida,
                p.prod_pet
            FROM '{prod_glob}' p
            JOIN first_prod fp ON p.idpozo = fp.idpozo
            WHERE p.prod_pet > 0
        )
        SELECT 
            cohorte,
            mes_vida,
            count(*) as n_pozos,
            round(median(prod_pet), 1) as mediana_prod_m3,
            round(avg(prod_pet), 1) as media_prod_m3,
            round(quantile_cont(prod_pet, 0.25), 1) as p25_prod_m3,
            round(quantile_cont(prod_pet, 0.75), 1) as p75_prod_m3
        FROM pozo_age
        WHERE cohorte BETWEEN 2015 AND 2024 AND mes_vida BETWEEN 0 AND 36
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).df()
    cohorts_df.to_parquet(PROCESSED_DIR / "cohorts_decay_curves.parquet", index=False)
    (API_DATA_DIR / "cohorts_decay_curves.json").write_text(cohorts_df.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("Cohorts decay curves created: %d points.", len(cohorts_df))

    # 4. Geospatial Summary of Wells (Aggregated by 0.05 degree grid / cluster for map)
    logger.info("Building 4. wells_geo_binned...")
    wells_geo = con.execute(f"""
        WITH well_summary AS (
            SELECT 
                p.idpozo,
                year(min(p.fecha)) as anio_primera_prod,
                round(sum(p.prod_pet), 0) as prod_pet_acumulada_m3,
                round(sum(CASE WHEN year(p.fecha) = 2025 THEN p.prod_pet ELSE 0 END), 0) as prod_pet_2025_m3
            FROM '{prod_glob}' p
            GROUP BY 1
        )
        SELECT 
            w.idpozo,
            w.sigla,
            coalesce(w.empresa, 'OTRAS') as empresa,
            coalesce(w.provincia, 'DESCONOCIDA') as provincia,
            coalesce(w.cuenca, 'DESCONOCIDA') as cuenca,
            coalesce(w.yacimiento, 'DESCONOCIDO') as yacimiento,
            coalesce(w.formacion, 'DESCONOCIDA') as formacion,
            coalesce(w.tipo_recurso, 'CONVENCIONAL') as tipo_recurso,
            round(w.coordenaday, 5) as lat,
            round(w.coordenadax, 5) as lon,
            s.anio_primera_prod,
            coalesce(s.prod_pet_acumulada_m3, 0) as prod_acumulada_m3,
            coalesce(s.prod_pet_2025_m3, 0) as prod_2025_m3
        FROM '{wells_p}' w
        LEFT JOIN well_summary s ON w.idpozo = s.idpozo
        WHERE w.coordenaday BETWEEN -55.0 AND -20.0 
          AND w.coordenadax BETWEEN -75.0 AND -53.0
          AND (s.prod_pet_acumulada_m3 > 0 OR w.tipo_recurso = 'NO CONVENCIONAL')
    """).df()
    wells_geo.to_parquet(PROCESSED_DIR / "wells_geo.parquet", index=False)
    
    # Save a lighter JSON with top productive wells + non-conventional wells (~5,000 wells for instant web map rendering)
    top_map_wells = con.execute(f"""
        SELECT 
            idpozo,
            sigla,
            empresa,
            provincia,
            yacimiento,
            tipo_recurso,
            lat,
            lon,
            anio_primera_prod,
            prod_2025_m3
        FROM wells_geo
        WHERE tipo_recurso = 'NO CONVENCIONAL' OR prod_2025_m3 > 5000
        ORDER BY prod_2025_m3 DESC
        LIMIT 4000
    """).df()
    (API_DATA_DIR / "wells_map_sample.json").write_text(top_map_wells.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("Wells geo created (%d total wells in parquet, %d in web map JSON).", len(wells_geo), len(top_map_wells))

    # 5. Technical Fractures Trends
    logger.info("Building 5. technical_fractures_trends...")
    frac_trends = con.execute(f"""
        SELECT 
            anio,
            count(*) as total_fracturas,
            count(distinct idpozo) as pozos_fracturados,
            round(avg(longitud_rama_horizontal_m), 0) as avg_longitud_horizontal_m,
            round(avg(cantidad_fracturas), 1) as avg_etapas,
            round(avg(coalesce(arena_bombeada_nacional_tn, 0) + coalesce(arena_bombeada_importada_tn, 0)), 0) as avg_arena_tn,
            round(avg(agua_inyectada_m3), 0) as avg_agua_m3
        FROM read_csv_auto('{frac_p}', ignore_errors=true)
        WHERE longitud_rama_horizontal_m > 100 AND anio BETWEEN 2016 AND 2025
        GROUP BY 1
        ORDER BY 1
    """).df()
    frac_trends.to_parquet(PROCESSED_DIR / "technical_fractures_trends.parquet", index=False)
    (API_DATA_DIR / "technical_fractures_trends.json").write_text(frac_trends.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("Technical fractures trends created.")

    # 6. Macro & Employment Trends
    logger.info("Building 6. macro_employment_trends...")
    wb_oil = json.loads((RAW_DIR / "worldbank" / "oil_rents_gdp_pct.json").read_text(encoding="utf-8"))
    wb_exp = json.loads((RAW_DIR / "worldbank" / "fuel_exports_merch_pct.json").read_text(encoding="utf-8"))
    wb_imp = json.loads((RAW_DIR / "worldbank" / "fuel_imports_merch_pct.json").read_text(encoding="utf-8"))
    
    wb_dict = {}
    for item in wb_oil:
        wb_dict.setdefault(item["year"], {})["oil_rents_gdp_pct"] = round(item["value"], 2)
    for item in wb_exp:
        wb_dict.setdefault(item["year"], {})["fuel_exports_pct"] = round(item["value"], 2)
    for item in wb_imp:
        wb_dict.setdefault(item["year"], {})["fuel_imports_pct"] = round(item["value"], 2)
        
    emp_neuq_df = con.execute(f"""
        SELECT 
            year(fecha) as year,
            round(avg(CASE WHEN clae2 IN (6, 9) THEN puestos ELSE 0 END), 0) as puestos_hidrocarburos_neuquen
        FROM read_csv_auto('{emp_p}', ignore_errors=true)
        WHERE upper(zona_prov) LIKE '%NEUQU%'
        GROUP BY 1
        HAVING year >= 2010
        ORDER BY 1
    """).df()
    
    macro_records = []
    for _, row in emp_neuq_df.iterrows():
        y = int(row["year"])
        wb_val = wb_dict.get(y, {})
        macro_records.append({
            "year": y,
            "puestos_hidrocarburos_neuquen": int(row["puestos_hidrocarburos_neuquen"]),
            "oil_rents_gdp_pct": wb_val.get("oil_rents_gdp_pct"),
            "fuel_exports_pct": wb_val.get("fuel_exports_pct"),
            "fuel_imports_pct": wb_val.get("fuel_imports_pct")
        })
    (API_DATA_DIR / "macro_employment_trends.json").write_text(json.dumps(macro_records, indent=2), encoding="utf-8")
    logger.info("Macro employment trends created.")

    # 7. Top Operators and Fields
    logger.info("Building 7. top_fields_operators...")
    top_ops = con.execute(f"""
        SELECT 
            coalesce(w.empresa, 'OTRAS') as operador,
            round(sum(p.prod_pet) / 1e3, 1) as pet_2025_km3,
            count(distinct p.idpozo) as pozos_activos_2025,
            round(sum(p.prod_pet) * 100.0 / sum(sum(p.prod_pet)) over (), 1) as market_share_pct
        FROM '{prod_glob}' p
        JOIN '{wells_p}' w ON p.idpozo = w.idpozo
        WHERE year(p.fecha) = 2025 AND w.tipo_recurso = 'NO CONVENCIONAL'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 10
    """).df()
    (API_DATA_DIR / "top_operators_2025.json").write_text(top_ops.to_json(orient="records", indent=2), encoding="utf-8")
    logger.info("All analytical views and static API datasets generated successfully.")

if __name__ == "__main__":
    build()
