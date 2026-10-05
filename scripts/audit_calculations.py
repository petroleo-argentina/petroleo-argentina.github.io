"""
Comprehensive script to execute all analytical calculations and generate all CSV exports
for the external audit package requested in Untitled-2.
"""

import duckdb
import os
import pandas as pd
import numpy as np

def run_all_audit_calculations():
    con = duckdb.connect()
    os.makedirs('analysis/exports', exist_ok=True)
    
    print("=" * 60)
    print("1. INSPECTING FRACTURES DATASET")
    print("=" * 60)
    frac_csv = 'data/raw/energia/datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv'
    cols_frac = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{frac_csv}')").fetchall()
    for c in cols_frac:
        print(f"  {c[0]} ({c[1]})")

    print("\n" + "=" * 60)
    print("2. CONVENTIONAL VS NO CONVENCIONAL & SUBTIPO (SHALE VS TIGHT)")
    print("=" * 60)
    # Join wells with 2025 production
    res_2025 = con.execute("""
        SELECT 
            COALESCE(w.tipo_recurso, 'No informado') as tipo_recurso,
            COALESCE(w.sub_tipo_recurso, 'No informado') as sub_tipo_recurso,
            COUNT(DISTINCT p.idpozo) as pozos_activos,
            SUM(p.prod_pet) as petroleo_m3,
            ROUND(SUM(p.prod_pet) / 1000.0, 2) as petroleo_miles_m3,
            ROUND(SUM(p.prod_pet) * 100.0 / SUM(SUM(p.prod_pet)) OVER (), 2) as share_pct
        FROM 'data/raw/petrodb/monthly_production/anio=2025/data.parquet' p
        LEFT JOIN 'data/raw/petrodb/wells.parquet' w ON p.idpozo = w.idpozo
        WHERE p.prod_pet > 0
        GROUP BY 1, 2
        ORDER BY petroleo_m3 DESC
    """).df()
    print(res_2025.to_string())

    print("\n" + "=" * 60)
    print("3. CROSSOVER 2021-2024 (analysis/exports/crossover_monthly.csv)")
    print("=" * 60)
    # Monthly production 2021-01 to 2024-12
    crossover_df = con.execute("""
        WITH monthly AS (
            SELECT 
                strftime(p.fecha, '%Y-%m') as mes_id,
                p.fecha,
                SUM(CASE WHEN w.tipo_recurso = 'CONVENCIONAL' OR w.tipo_recurso IS NULL OR w.tipo_recurso NOT IN ('NO CONVENCIONAL') THEN p.prod_pet ELSE 0 END) as prod_conv_m3,
                SUM(CASE WHEN w.tipo_recurso = 'NO CONVENCIONAL' THEN p.prod_pet ELSE 0 END) as prod_no_conv_m3,
                SUM(p.prod_pet) as prod_total_m3
            FROM 'data/raw/petrodb/monthly_production/anio=*/data.parquet' p
            LEFT JOIN 'data/raw/petrodb/wells.parquet' w ON p.idpozo = w.idpozo
            WHERE p.anio BETWEEN 2021 AND 2024
            GROUP BY 1, 2
        )
        SELECT 
            mes_id as fecha,
            ROUND(prod_conv_m3 / 1000.0, 2) as produccion_convencional_miles_m3,
            ROUND(prod_no_conv_m3 / 1000.0, 2) as produccion_no_convencional_miles_m3,
            ROUND(prod_total_m3 / 1000.0, 2) as produccion_total_miles_m3,
            ROUND((prod_no_conv_m3 / NULLIF(prod_total_m3, 0)) * 100.0, 2) as share_no_convencional_pct,
            CASE WHEN prod_no_conv_m3 > prod_conv_m3 THEN 'NO CONVENCIONAL MAYOR' ELSE 'CONVENCIONAL MAYOR' END as estado_crossover
        FROM monthly
        ORDER BY fecha ASC
    """).df()
    crossover_csv_path = 'analysis/exports/crossover_monthly.csv'
    crossover_df.to_csv(crossover_csv_path, index=False, encoding='utf-8')
    print(f"Saved {len(crossover_df)} rows to {crossover_csv_path}")
    print(crossover_df.head(10).to_string())
    print("\nMonths where No Convencional > Convencional:")
    print(crossover_df[crossover_df['share_no_convencional_pct'] > 50.0].to_string())

    print("\n" + "=" * 60)
    print("4. PARETO 2025 (analysis/exports/pareto_2025.csv)")
    print("=" * 60)
    # Well-level production in 2025 (active wells with oil > 0)
    wells_2025 = con.execute("""
        SELECT 
            p.idpozo,
            w.sigla,
            COALESCE(w.tipo_recurso, 'No informado') as tipo_recurso,
            COALESCE(w.sub_tipo_recurso, 'No informado') as sub_tipo_recurso,
            w.yacimiento,
            w.provincia,
            w.cuenca,
            SUM(p.prod_pet) as petroleo_anual_m3
        FROM 'data/raw/petrodb/monthly_production/anio=2025/data.parquet' p
        LEFT JOIN 'data/raw/petrodb/wells.parquet' w ON p.idpozo = w.idpozo
        WHERE p.prod_pet > 0
        GROUP BY 1, 2, 3, 4, 5, 6, 7
        ORDER BY petroleo_anual_m3 DESC
    """).df()
    
    total_wells = len(wells_2025)
    total_oil = wells_2025['petroleo_anual_m3'].sum()
    print(f"Total active oil wells in 2025 (petroleo > 0): {total_wells}")
    print(f"Total oil in 2025: {total_oil:.2f} m3 ({total_oil/1000:.2f} miles m3)")

    wells_2025['rank_pozo'] = range(1, total_wells + 1)
    wells_2025['pct_pozos_acum'] = (wells_2025['rank_pozo'] / total_wells) * 100.0
    wells_2025['petroleo_acum_m3'] = wells_2025['petroleo_anual_m3'].cumsum()
    wells_2025['pct_produccion_acum'] = (wells_2025['petroleo_acum_m3'] / total_oil) * 100.0

    # Calculate milestones:
    for p_well in [1.0, 5.0, 10.0, 13.1, 20.0]:
        cutoff_idx = int(round(total_wells * (p_well / 100.0))) - 1
        pct_prod = wells_2025.iloc[cutoff_idx]['pct_produccion_acum']
        print(f"Top {p_well}% pozos ({cutoff_idx+1} pozos) -> {pct_prod:.2f}% de la producción")

    for p_prod in [50.0, 66.67, 75.0, 90.0]:
        match = wells_2025[wells_2025['pct_produccion_acum'] >= p_prod].iloc[0]
        print(f"Para explicar {p_prod}% de la producción: {match['rank_pozo']} pozos ({match['pct_pozos_acum']:.2f}% de los pozos)")

    pareto_csv_path = 'analysis/exports/pareto_2025.csv'
    wells_2025[['rank_pozo', 'idpozo', 'sigla', 'tipo_recurso', 'sub_tipo_recurso', 'yacimiento', 'provincia', 'petroleo_anual_m3', 'pct_pozos_acum', 'pct_produccion_acum']].to_csv(pareto_csv_path, index=False, encoding='utf-8')
    print(f"Saved Pareto export to {pareto_csv_path}")

    print("\n" + "=" * 60)
    print("5. PRODUCTIVIDAD POR GENERACION / COHORTES (analysis/exports/cohortes_productividad.csv)")
    print("=" * 60)
    # First production date per well, and cumulative production at 1m, 6m, 12m, 24m
    # Limit to unconventional wells or all wells? The audit says: "Crear cohortes por año de primera producción. Para cada cohorte: cantidad de pozos; producción mes 1; acumulada 6m; acumulada 12m; acumulada 24m; mediana; P25; P75."
    # Let's compute for NO CONVENCIONAL wells (Vaca Muerta / shale / tight) and overall.
    cohorts_df = con.execute("""
        WITH first_month AS (
            SELECT 
                p.idpozo,
                w.tipo_recurso,
                MIN(p.fecha) as primera_fecha,
                YEAR(MIN(p.fecha)) as anio_cohorte
            FROM 'data/raw/petrodb/monthly_production/anio=*/data.parquet' p
            LEFT JOIN 'data/raw/petrodb/wells.parquet' w ON p.idpozo = w.idpozo
            WHERE p.prod_pet > 0
            GROUP BY 1, 2
        ),
        well_monthly_ranked AS (
            SELECT 
                p.idpozo,
                fm.anio_cohorte,
                fm.tipo_recurso,
                p.prod_pet,
                ROW_NUMBER() OVER (PARTITION BY p.idpozo ORDER BY p.fecha ASC) as mes_relativo
            FROM 'data/raw/petrodb/monthly_production/anio=*/data.parquet' p
            JOIN first_month fm ON p.idpozo = fm.idpozo
            WHERE p.prod_pet > 0
        ),
        well_cumulatives AS (
            SELECT 
                idpozo,
                anio_cohorte,
                tipo_recurso,
                MAX(CASE WHEN mes_relativo = 1 THEN prod_pet ELSE NULL END) as prod_mes_1,
                SUM(CASE WHEN mes_relativo <= 6 THEN prod_pet ELSE 0 END) as prod_acum_6m,
                SUM(CASE WHEN mes_relativo <= 12 THEN prod_pet ELSE 0 END) as prod_acum_12m,
                SUM(CASE WHEN mes_relativo <= 24 THEN prod_pet ELSE 0 END) as prod_acum_24m,
                MAX(mes_relativo) as total_meses_obs
            FROM well_monthly_ranked
            GROUP BY 1, 2, 3
        )
        SELECT 
            anio_cohorte,
            tipo_recurso,
            COUNT(*) as cantidad_pozos,
            -- Mes 1
            ROUND(AVG(prod_mes_1), 2) as mes1_media,
            ROUND(MEDIAN(prod_mes_1), 2) as mes1_mediana,
            ROUND(QUANTILE_CONT(prod_mes_1, 0.25), 2) as mes1_p25,
            ROUND(QUANTILE_CONT(prod_mes_1, 0.75), 2) as mes1_p75,
            -- Acumulada 6m (solo pozos con >= 6 meses)
            ROUND(AVG(CASE WHEN total_meses_obs >= 6 THEN prod_acum_6m ELSE NULL END), 2) as acum_6m_media,
            ROUND(MEDIAN(CASE WHEN total_meses_obs >= 6 THEN prod_acum_6m ELSE NULL END), 2) as acum_6m_mediana,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 6 THEN prod_acum_6m ELSE NULL END, 0.25), 2) as acum_6m_p25,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 6 THEN prod_acum_6m ELSE NULL END, 0.75), 2) as acum_6m_p75,
            -- Acumulada 12m (solo pozos con >= 12 meses)
            ROUND(AVG(CASE WHEN total_meses_obs >= 12 THEN prod_acum_12m ELSE NULL END), 2) as acum_12m_media,
            ROUND(MEDIAN(CASE WHEN total_meses_obs >= 12 THEN prod_acum_12m ELSE NULL END), 2) as acum_12m_mediana,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 12 THEN prod_acum_12m ELSE NULL END, 0.25), 2) as acum_12m_p25,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 12 THEN prod_acum_12m ELSE NULL END, 0.75), 2) as acum_12m_p75,
            -- Acumulada 24m (solo pozos con >= 24 meses)
            ROUND(AVG(CASE WHEN total_meses_obs >= 24 THEN prod_acum_24m ELSE NULL END), 2) as acum_24m_media,
            ROUND(MEDIAN(CASE WHEN total_meses_obs >= 24 THEN prod_acum_24m ELSE NULL END), 2) as acum_24m_mediana,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 24 THEN prod_acum_24m ELSE NULL END, 0.25), 2) as acum_24m_p25,
            ROUND(QUANTILE_CONT(CASE WHEN total_meses_obs >= 24 THEN prod_acum_24m ELSE NULL END, 0.75), 2) as acum_24m_p75
        FROM well_cumulatives
        WHERE anio_cohorte >= 2012
        GROUP BY 1, 2
        ORDER BY anio_cohorte ASC, tipo_recurso ASC
    """).df()
    cohorts_csv_path = 'analysis/exports/cohortes_productividad.csv'
    cohorts_df.to_csv(cohorts_csv_path, index=False, encoding='utf-8')
    print(f"Saved Cohorts export to {cohorts_csv_path}")
    print(cohorts_df[cohorts_df['tipo_recurso'] == 'NO CONVENCIONAL'][['anio_cohorte', 'cantidad_pozos', 'mes1_mediana', 'acum_12m_mediana', 'acum_24m_mediana']].to_string())

    print("\n" + "=" * 60)
    print("6. FRACTURAS ANUALES (analysis/exports/fracturas_anuales.csv)")
    print("=" * 60)
    fractures_df = con.execute(f"""
        WITH noconv_wells_by_year AS (
            SELECT 
                anio,
                COUNT(DISTINCT p.idpozo) as pozos_noconv_activos
            FROM 'data/raw/petrodb/monthly_production/anio=*/data.parquet' p
            JOIN 'data/raw/petrodb/wells.parquet' w ON p.idpozo = w.idpozo
            WHERE w.tipo_recurso = 'NO CONVENCIONAL' AND p.prod_pet > 0
            GROUP BY 1
        ),
        frac_per_well_year AS (
            SELECT 
                YEAR(TRY_CAST(fecha_inicio_fractura AS DATE)) as anio,
                idpozo,
                MAX(TRY_CAST(longitud_rama_horizontal_m AS DOUBLE)) as rama_h_m,
                SUM(TRY_CAST(cantidad_fracturas AS DOUBLE)) as etapas,
                SUM(TRY_CAST(arena_bombeada_nacional_tn AS DOUBLE) + TRY_CAST(arena_bombeada_importada_tn AS DOUBLE)) as arena_tn
            FROM read_csv_auto('{frac_csv}')
            WHERE fecha_inicio_fractura IS NOT NULL
            GROUP BY 1, 2
        )
        SELECT 
            f.anio,
            COUNT(DISTINCT f.idpozo) as pozos_con_fractura,
            COALESCE(nc.pozos_noconv_activos, 0) as pozos_no_convencionales_activos,
            ROUND(COUNT(DISTINCT f.idpozo) * 100.0 / NULLIF(nc.pozos_noconv_activos, 0), 2) as cobertura_pct,
            -- Longitud Horizontal
            ROUND(AVG(f.rama_h_m), 1) as longitud_h_media_m,
            ROUND(MEDIAN(f.rama_h_m), 1) as longitud_h_mediana_m,
            ROUND(QUANTILE_CONT(f.rama_h_m, 0.25), 1) as longitud_h_p25_m,
            ROUND(QUANTILE_CONT(f.rama_h_m, 0.75), 1) as longitud_h_p75_m,
            -- Etapas
            ROUND(AVG(f.etapas), 1) as etapas_media,
            ROUND(MEDIAN(f.etapas), 1) as etapas_mediana,
            ROUND(QUANTILE_CONT(f.etapas, 0.25), 1) as etapas_p25,
            ROUND(QUANTILE_CONT(f.etapas, 0.75), 1) as etapas_p75,
            -- Arena (Tn)
            ROUND(AVG(f.arena_tn), 1) as arena_media_tn,
            ROUND(MEDIAN(f.arena_tn), 1) as arena_mediana_tn,
            ROUND(QUANTILE_CONT(f.arena_tn, 0.25), 1) as arena_p25_tn,
            ROUND(QUANTILE_CONT(f.arena_tn, 0.75), 1) as arena_p75_tn
        FROM frac_per_well_year f
        LEFT JOIN noconv_wells_by_year nc ON f.anio = nc.anio
        WHERE f.anio BETWEEN 2014 AND 2025
        GROUP BY f.anio, nc.pozos_noconv_activos
        ORDER BY f.anio ASC
    """).df()
    frac_csv_path = 'analysis/exports/fracturas_anuales.csv'
    fractures_df.to_csv(frac_csv_path, index=False, encoding='utf-8')
    print(f"Saved Fractures export to {frac_csv_path}")
    print(fractures_df.to_string())

    print("\n" + "=" * 60)
    print("7. VALIDACION PRODUCCION HISTORICA (analysis/exports/validacion_produccion_historica.csv)")
    print("=" * 60)
    hist_csv = 'data/raw/energia/serie-produccion-petroleo-total-pais-desde-1950.csv'
    hist_val_df = con.execute(f"""
        WITH serie_oficial AS (
            SELECT 
                TRY_CAST(anio AS BIGINT) as anio,
                TRY_CAST(produccion_petroleo AS DOUBLE) as serie_oficial_miles_m3
            FROM read_csv_auto('{hist_csv}')
            WHERE anio IS NOT NULL
        ),
        suma_pozos AS (
            SELECT 
                anio,
                ROUND(SUM(prod_pet) / 1000.0, 2) as suma_pozos_miles_m3
            FROM 'data/raw/petrodb/monthly_production/anio=*/data.parquet'
            GROUP BY 1
        )
        SELECT 
            COALESCE(s.anio, p.anio) as anio,
            s.serie_oficial_miles_m3 as serie_oficial,
            p.suma_pozos_miles_m3 as suma_pozos,
            ROUND(ABS(COALESCE(p.suma_pozos_miles_m3, 0) - COALESCE(s.serie_oficial_miles_m3, 0)), 2) as diferencia_absoluta,
            CASE 
                WHEN s.serie_oficial_miles_m3 IS NOT NULL AND p.suma_pozos_miles_m3 IS NOT NULL THEN
                    ROUND(ABS(p.suma_pozos_miles_m3 - s.serie_oficial_miles_m3) * 100.0 / s.serie_oficial_miles_m3, 2)
                ELSE NULL
            END as diferencia_pct,
            CASE 
                WHEN p.suma_pozos_miles_m3 IS NULL THEN 'SOLO SERIE OFICIAL AGREGADA (< 2006)'
                WHEN s.serie_oficial_miles_m3 IS NULL THEN 'SOLO SUMA DE POZOS CAPITULO IV (> 2015)'
                WHEN ABS(p.suma_pozos_miles_m3 - s.serie_oficial_miles_m3) * 100.0 / s.serie_oficial_miles_m3 > 1.0 THEN 'DIFERENCIA > 1%'
                ELSE 'VALIDADO (<= 1%)'
            END as estado_validacion
        FROM serie_oficial s
        FULL OUTER JOIN suma_pozos p ON s.anio = p.anio
        ORDER BY anio ASC
    """).df()
    hist_val_path = 'analysis/exports/validacion_produccion_historica.csv'
    hist_val_df.to_csv(hist_val_path, index=False, encoding='utf-8')
    print(f"Saved Historical Validation export to {hist_val_path}")
    print(hist_val_df[hist_val_df['anio'] >= 2006].to_string())

    print("\n" + "=" * 60)
    print("8. POZOS Y GEOGRAFIA")
    print("=" * 60)
    geo_stats = con.execute("""
        SELECT 
            COUNT(*) as total_pozos,
            COUNT(CASE WHEN coordenadax IS NOT NULL AND coordenaday IS NOT NULL AND coordenadax != 0 AND coordenaday != 0 THEN 1 END) as pozos_coords_validas,
            COUNT(CASE WHEN coordenadax IS NULL OR coordenaday IS NULL OR (coordenadax = 0 AND coordenaday = 0) THEN 1 END) as pozos_sin_coords,
            COUNT(*) - COUNT(DISTINCT (coordenadax, coordenaday)) as coords_duplicadas
        FROM 'data/raw/petrodb/wells.parquet'
    """).df()
    print("Resumen de coordenadas:")
    print(geo_stats.to_string())

    print("\nPozos por Cuenca:")
    cuencas = con.execute("""
        SELECT 
            COALESCE(cuenca, 'SIN CUENCA') as cuenca,
            COUNT(*) as total_pozos,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_pozos
        FROM 'data/raw/petrodb/wells.parquet'
        GROUP BY 1
        ORDER BY total_pozos DESC
    """).df()
    print(cuencas.to_string())

    print("\nPozos por Provincia:")
    provincias = con.execute("""
        SELECT 
            COALESCE(provincia, 'SIN PROVINCIA') as provincia,
            COUNT(*) as total_pozos,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_pozos
        FROM 'data/raw/petrodb/wells.parquet'
        GROUP BY 1
        ORDER BY total_pozos DESC
    """).df()
    print(provincias.to_string())

if __name__ == '__main__':
    run_all_audit_calculations()
