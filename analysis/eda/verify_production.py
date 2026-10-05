import duckdb
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
PROD_GLOB = (BASE_DIR / "data" / "raw" / "petrodb" / "monthly_production" / "*" / "data.parquet").as_posix()
WELLS_PATH = (BASE_DIR / "data" / "raw" / "petrodb" / "wells.parquet").as_posix()

def main():
    con = duckdb.connect()
    
    print("=== DUCKDB VERIFICATION OF FULL 2006-2025 MONTHLY PRODUCTION ===")
    total_rows = con.execute(f"SELECT count(*) FROM '{PROD_GLOB}'").fetchone()[0]
    print(f"Total production records: {total_rows:,}")
    
    stats = con.execute(f"""
        SELECT 
            min(fecha) as min_date,
            max(fecha) as max_date,
            count(distinct idpozo) as unique_wells,
            round(sum(prod_pet) / 1e6, 2) as total_oil_million_m3,
            round(sum(prod_gas) / 1e6, 2) as total_gas_million_m3,
            round(sum(prod_agua) / 1e6, 2) as total_water_million_m3
        FROM '{PROD_GLOB}'
    """).df()
    print("\nProduction Aggregates:")
    print(stats)
    
    print("\nSchema of monthly production:")
    schema = con.execute(f"DESCRIBE SELECT * FROM '{PROD_GLOB}'").df()
    for _, row in schema.iterrows():
        print(f"  {row['column_name']:<25} {row['column_type']}")
        
    print("\nProduction by Year (Oil Mm3, Gas Mm3, Active Wells):")
    yearly = con.execute(f"""
        SELECT 
            year(fecha) as anio,
            count(distinct idpozo) as pozos_activos,
            round(sum(prod_pet) / 1e3, 1) as petroleo_miles_m3,
            round(sum(prod_gas) / 1e3, 1) as gas_miles_m3
        FROM '{PROD_GLOB}'
        WHERE prod_pet > 0 OR prod_gas > 0
        GROUP BY 1
        ORDER BY 1
    """).df()
    print(yearly.to_string(index=False))

if __name__ == "__main__":
    main()
