import os
import sys
import logging
from pathlib import Path
import duckdb

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("join_rates")

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_DIR = BASE_DIR / "data" / "raw"

def main():
    con = duckdb.connect()
    
    wells_p = (RAW_DIR / "petrodb" / "wells.parquet").as_posix()
    prod_glob = (RAW_DIR / "petrodb" / "monthly_production" / "*" / "data.parquet").as_posix()
    frac_p = (RAW_DIR / "energia" / "datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv").as_posix()
    tray_p = (RAW_DIR / "energia" / "trayectorias-de-pozo-vaca-muerta.csv").as_posix()
    term_p = (RAW_DIR / "energia" / "pozos-terminados.csv").as_posix()
    
    print("=== CALCULATING OFFICIAL CROSS-JOIN RATES ===")
    
    # 1. Monthly Production <-> Wells
    logger.info("Calculating Monthly Production <-> Wells join rate...")
    prod_wells = con.execute(f"""
        SELECT 
            count(distinct p.idpozo) as total_prod_wells,
            count(distinct w.idpozo) as matched_wells,
            round(count(distinct w.idpozo) * 100.0 / count(distinct p.idpozo), 2) as match_rate_pct
        FROM '{prod_glob}' p
        LEFT JOIN '{wells_p}' w ON p.idpozo = w.idpozo
    """).df()
    print("\n1. Monthly Production (17.7M rows) <-> Wells:")
    print(prod_wells.to_string(index=False))
    
    # 2. Fracturas <-> Wells
    logger.info("Inspecting columns of Fracturas...")
    frac_cols = con.execute(f"SELECT * FROM read_csv_auto('{frac_p}', ignore_errors=true) LIMIT 1").df().columns.tolist()
    print(f"\nFracturas columns ({len(frac_cols)}): {frac_cols[:8]}...")
    
    # Look for well id in fracturas
    # Check if idpozo or sigla is present
    pozo_col_frac = None
    for c in frac_cols:
        if c.lower() in ["idpozo", "id_pozo", "id"]:
            pozo_col_frac = c
            break
        elif "sigla" in c.lower() or "pozo" in c.lower():
            pozo_col_frac = c
            
    print(f"Selected well identifier for Fracturas: '{pozo_col_frac}'")
    
    frac_join = con.execute(f"""
        SELECT 
            count(*) as total_frac_rows,
            count(w.idpozo) as matched_rows,
            round(count(w.idpozo) * 100.0 / count(*), 2) as match_rate_pct,
            count(distinct f."{pozo_col_frac}") as distinct_frac_wells,
            count(distinct w.idpozo) as distinct_matched_wells
        FROM read_csv_auto('{frac_p}', ignore_errors=true) f
        LEFT JOIN '{wells_p}' w ON cast(f."{pozo_col_frac}" as VARCHAR) = cast(w.idpozo as VARCHAR)
    """).df()
    print("\n2. Fracturas (Adjunto IV) <-> Wells (by idpozo):")
    print(frac_join.to_string(index=False))
    
    # 3. Trayectorias Vaca Muerta <-> Wells (by sigla)
    logger.info("Inspecting Trayectorias Vaca Muerta...")
    tray_join = con.execute(f"""
        SELECT 
            count(distinct t.sigla) as distinct_tray_siglas,
            count(distinct w.sigla) as matched_wells_by_sigla,
            round(count(distinct w.sigla) * 100.0 / count(distinct t.sigla), 2) as match_rate_pct
        FROM read_csv_auto('{tray_p}', ignore_errors=true) t
        LEFT JOIN '{wells_p}' w ON trim(upper(t.sigla)) = trim(upper(w.sigla))
    """).df()
    print("\n3. Trayectorias Vaca Muerta <-> Wells (by sigla):")
    print(tray_join.to_string(index=False))
    
    # 4. Pozos terminados structure
    print("\n4. Pozos Terminados (Tabla mensual por empresa / yacimiento / concepto):")
    term_cols = con.execute(f"SELECT * FROM read_csv_auto('{term_p}', ignore_errors=true) LIMIT 1").df().columns.tolist()
    print("Columns:", term_cols)
    print("Sample row:")
    print(con.execute(f"SELECT * FROM read_csv_auto('{term_p}', ignore_errors=true) LIMIT 1").df().to_dict(orient='records'))

if __name__ == "__main__":
    main()
