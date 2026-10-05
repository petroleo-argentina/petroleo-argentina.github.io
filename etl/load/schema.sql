-- ====================================================================
-- DDL Schema — Plataforma de Datos Petróleo en Argentina
-- Compatible con PostgreSQL 15+ / PostGIS 3.3+ y DuckDB
-- ====================================================================

-- 1. Crear esquemas organizacionales
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS meta;

-- ====================================================================
-- 2. Esquema CORE (Modelo Dimensional y Relacional)
-- ====================================================================

-- Dimensión Pozo (Padrón Maestro)
CREATE TABLE IF NOT EXISTS core.dim_pozo (
    idpozo INTEGER PRIMARY KEY,
    sigla VARCHAR(100) NOT NULL,
    empresa_actual VARCHAR(150) NOT NULL,
    cuenca VARCHAR(80) NOT NULL,
    provincia VARCHAR(60) NOT NULL,
    yacimiento VARCHAR(120) NOT NULL,
    concesion VARCHAR(120),
    formacion VARCHAR(100),
    tipo_recurso VARCHAR(30) NOT NULL, -- 'CONVENCIONAL' o 'NO CONVENCIONAL'
    tipo_pozo VARCHAR(40),             -- 'HORIZONTAL', 'VERTICAL', 'DESVIADO'
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    fecha_primera_prod DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_pozo_sigla ON core.dim_pozo(sigla);
CREATE INDEX IF NOT EXISTS idx_dim_pozo_cuenca ON core.dim_pozo(cuenca);
CREATE INDEX IF NOT EXISTS idx_dim_pozo_provincia ON core.dim_pozo(provincia);
CREATE INDEX IF NOT EXISTS idx_dim_pozo_recurso ON core.dim_pozo(tipo_recurso);

-- Hecho: Producción Pozo Mes (17.7M filas)
CREATE TABLE IF NOT EXISTS core.fact_produccion_pozo_mes (
    idpozo INTEGER NOT NULL,
    fecha DATE NOT NULL,
    anio SMALLINT NOT NULL,
    mes SMALLINT NOT NULL,
    prod_pet_m3 DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    prod_gas_miles_m3 DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    prod_agua_m3 DOUBLE PRECISION DEFAULT 0.0,
    dias_produccion SMALLINT DEFAULT 0,
    PRIMARY KEY (idpozo, fecha),
    FOREIGN KEY (idpozo) REFERENCES core.dim_pozo(idpozo)
);

CREATE INDEX IF NOT EXISTS idx_fact_prod_fecha ON core.fact_produccion_pozo_mes(fecha);
CREATE INDEX IF NOT EXISTS idx_fact_prod_anio_mes ON core.fact_produccion_pozo_mes(anio, mes);
CREATE INDEX IF NOT EXISTS idx_fact_prod_idpozo ON core.fact_produccion_pozo_mes(idpozo);

-- Hecho: Fracturas Hidráulicas y Completación (Adjunto IV)
CREATE TABLE IF NOT EXISTS core.fact_fractura_adjunto_iv (
    id SERIAL PRIMARY KEY,
    id_pozo INTEGER,
    sigla VARCHAR(100) NOT NULL,
    longitud_horizontal_mt DOUBLE PRECISION,
    cantidad_fracturas INTEGER,
    arena_bombeada_tn DOUBLE PRECISION,
    volumen_inyectado_m3 DOUBLE PRECISION,
    fecha_completacion DATE
);

CREATE INDEX IF NOT EXISTS idx_fractura_idpozo ON core.fact_fractura_adjunto_iv(id_pozo);
CREATE INDEX IF NOT EXISTS idx_fractura_sigla ON core.fact_fractura_adjunto_iv(sigla);

-- Dimensión: Trayectorias de Pozo Vaca Muerta (Surveys 3D)
CREATE TABLE IF NOT EXISTS core.dim_trayectoria_direccional (
    sigla VARCHAR(100) PRIMARY KEY,
    idpo INTEGER,
    profundidad_final_total_mt DOUBLE PRECISION,
    profundidad_vertical_mt DOUBLE PRECISION,
    largo_rama_horizontal_mt DOUBLE PRECISION,
    drilini DATE,
    drilfin DATE,
    geojson TEXT
);

-- Hecho: Empleo Sectorial Registrado (CEP XXI)
CREATE TABLE IF NOT EXISTS core.fact_empleo_provincia (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    zona_prov VARCHAR(80) NOT NULL,
    clae2 VARCHAR(10) NOT NULL,
    puestos DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_empleo_fecha ON core.fact_empleo_provincia(fecha);
CREATE INDEX IF NOT EXISTS idx_empleo_prov ON core.fact_empleo_provincia(zona_prov);

-- ====================================================================
-- 3. Esquema ANALYTICS (Vistas Analíticas Agregadas)
-- ====================================================================

-- 3.1 Producción Nacional Mensual Convencional vs No Convencional
CREATE TABLE IF NOT EXISTS analytics.mv_produccion_nacional_mes AS
SELECT 
    f.fecha,
    f.anio,
    f.mes,
    SUM(f.prod_pet_m3) AS total_m3_mes,
    SUM(CASE WHEN p.tipo_recurso = 'NO CONVENCIONAL' THEN f.prod_pet_m3 ELSE 0 END) AS no_convencional_m3_mes,
    SUM(CASE WHEN p.tipo_recurso != 'NO CONVENCIONAL' OR p.tipo_recurso IS NULL THEN f.prod_pet_m3 ELSE 0 END) AS convencional_m3_mes,
    ROUND(
        SUM(CASE WHEN p.tipo_recurso = 'NO CONVENCIONAL' THEN f.prod_pet_m3 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(f.prod_pet_m3), 0), 2
    ) AS share_no_conv_pct
FROM core.fact_produccion_pozo_mes f
LEFT JOIN core.dim_pozo p ON f.idpozo = p.idpozo
GROUP BY f.fecha, f.anio, f.mes
ORDER BY f.fecha;

-- 3.2 Pozos Activos Mensuales
CREATE TABLE IF NOT EXISTS analytics.mv_pozos_activos_mes AS
SELECT 
    f.fecha,
    f.anio,
    COUNT(DISTINCT f.idpozo) AS pozos_activos_total,
    COUNT(DISTINCT CASE WHEN p.tipo_recurso = 'NO CONVENCIONAL' THEN f.idpozo END) AS pozos_activos_shale,
    COUNT(DISTINCT CASE WHEN p.tipo_recurso != 'NO CONVENCIONAL' THEN f.idpozo END) AS pozos_activos_conv
FROM core.fact_produccion_pozo_mes f
LEFT JOIN core.dim_pozo p ON f.idpozo = p.idpozo
WHERE (f.prod_pet_m3 > 0 OR f.prod_gas_miles_m3 > 0)
GROUP BY f.fecha, f.anio
ORDER BY f.fecha;
