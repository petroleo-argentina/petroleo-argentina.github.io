import duckdb
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_PETRODB = BASE_DIR / "data" / "raw" / "petrodb"

def inspect():
    con = duckdb.connect()
    
    print("=== INSPECTING WELLS.PARQUET ===")
    wells_path = (RAW_PETRODB / "wells.parquet").as_posix()
    wells_count = con.execute(f"SELECT count(*) FROM '{wells_path}'").fetchone()[0]
    print(f"Total wells count: {wells_count:,}")
    
    schema = con.execute(f"DESCRIBE SELECT * FROM '{wells_path}'").df()
    print("\nSchema:")
    for _, row in schema.iterrows():
        print(f"  {row['column_name']:<30} {row['column_type']}")
        
    print("\nSample rows:")
    sample = con.execute(f"SELECT idpozo, sigla, formacion, tipo_recurso, provincia, cuenca, coordenadax, coordenaday FROM '{wells_path}' LIMIT 5").df()
    print(sample)
    
    print("\nBreakdown by Tipo Recurso:")
    recurso = con.execute(f"""
        SELECT 
            coalesce(tipo_recurso, 'DESCONOCIDO') as tipo_recurso, 
            count(*) as wells_count,
            round(count(*) * 100.0 / {wells_count}, 2) as pct
        FROM '{wells_path}'
        GROUP BY 1
        ORDER BY 2 DESC
    """).df()
    print(recurso)
    
    print("\nBreakdown by Provincia (Top 10):")
    prov = con.execute(f"""
        SELECT 
            coalesce(provincia, 'DESCONOCIDO') as provincia, 
            count(*) as wells_count,
            round(count(*) * 100.0 / {wells_count}, 2) as pct
        FROM '{wells_path}'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 10
    """).df()
    print(prov)

    print("\nBreakdown by Formacion (Top 10):")
    form = con.execute(f"""
        SELECT 
            coalesce(formacion, 'DESCONOCIDO') as formacion, 
            count(*) as wells_count
        FROM '{wells_path}'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 10
    """).df()
    print(form)

    print("\n=== INSPECTING WELL_EVENTS.PARQUET ===")
    events_path = (RAW_PETRODB / "well_events.parquet").as_posix()
    events_count = con.execute(f"SELECT count(*) FROM '{events_path}'").fetchone()[0]
    print(f"Total events count: {events_count:,}")
    schema_ev = con.execute(f"DESCRIBE SELECT * FROM '{events_path}'").df()
    for _, row in schema_ev.iterrows():
        print(f"  {row['column_name']:<30} {row['column_type']}")
    print("\nEvent types:")
    print(con.execute(f"SELECT coalesce(tipo_evento, 'NULL') as tipo_evento, count(*) FROM '{events_path}' GROUP BY 1 ORDER BY 2 DESC LIMIT 10").df())

if __name__ == "__main__":
    inspect()
