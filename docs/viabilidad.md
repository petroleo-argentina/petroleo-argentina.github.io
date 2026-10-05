# Informe de Viabilidad de Datos y Visualizaciones

Conforme a la Sección 23 del Plan de Implementación, este informe dictamina qué visualizaciones son metodológicamente viables a partir de los datos crudos descargados, validados y auditados.

---

## Resumen Ejecutivo de Viabilidad

| Componente Visual / Escena | Viabilidad | Dataset Principal de Soporte | Nivel de Confianza |
|---|---|---|---|
| **Escena 1: 75 Años de Petróleo (1950-2025)** | **VIABLE (100%)** | `produccion_1950` + `produccion_pozo_mensual` | ALTO |
| **Escena 2: Mapa Temporal de Pozos (2006-2025)** | **VIABLE (100%)** | `petrodb_wells` (85.417 pozos con coordenadas) | ALTO |
| **Escena 3: Convencional vs No Convencional** | **VIABLE (100%)** | `produccion_pozo_mensual` + `tipo_recurso` | ALTO |
| **Escena 4: Más Pozos o Mejores Pozos** | **VIABLE (100%)** | Pozos activos mensuales × producción media | ALTO |
| **Escena 5: La Vida de un Pozo (Cohortes 2016-2024)** | **VIABLE (100%)** | Declinación por mes de vida (0 a 36 meses) | ALTO |
| **Escena 6: Cómo Cambió el Pozo (Diseño Técnico)** | **VIABLE (100%)** | `fractura_pozos` (Adjunto IV: longitud, etapas, arena) | ALTO (Match 96.06%) |
| **Escena 7: Del Pozo al País (Macro, Empleo, Inversión)** | **VIABLE (100%)** | `inversiones_upstream` + `empleo_provincia` + `worldbank` | ALTO |
| **Escena 8: Infraestructura y Venteos Satelitales** | **VIABLE (100%)** | `sensores_remotos_venteo` + `refinerias` + `ductos` | ALTO |

---

## Evaluación Detallada por Dataset

### 1. Producción Mensual por Pozo (Capítulo IV)
- **Estado:** ✅ OK
- **Cobertura:** Enero 2006 a Diciembre 2025 (20 años completos).
- **Filas:** 17.775.911 registros mensuales.
- **Pozos únicos:** 85.305 pozos.
- **Nulos en variables críticas (prod_pet, prod_gas):** 0%.
- **Cruce con padrón de pozos:** **100.0% match**.
- **Aptitud visual:**
  - Mapa temporal: Sí.
  - Cohortes: Sí.
  - Productividad por edad: Sí.
  - Curvas por operador y yacimiento: Sí.

### 2. Padrón Maestro de Pozos (`wells.parquet`)
- **Estado:** ✅ OK
- **Filas:** 85.417 pozos.
- **Pozos georreferenciados:** 85.417 (100%).
- **Variables geográficas:** Latitud, Longitud, Provincia, Cuenca, Yacimiento, Formación.
- **Identificación no convencional:** 4.833 pozos identificados (3.382 en Vaca Muerta).
- **Aptitud visual:** Coordenadas listas para MapLibre GL JS / Deck.gl.

### 3. Registro Oficial de Fracturas (Adjunto IV)
- **Estado:** ✅ OK
- **Filas:** 4.922 registros técnicos.
- **Variables disponibles:** Longitud de rama horizontal (m), cantidad de etapas, arena bombeada (tn), agua inyectada (m3), presión máxima.
- **Cruce con padrón de pozos (`idpozo`):** **96.06% match**.
- **Aptitud visual:** Dispersión y distribuciones de ingeniería vs producción acumulada 12 meses.

### 4. Serie Histórica 1950-2015
- **Estado:** ✅ OK
- **Filas:** 66 registros anuales oficiales.
- **Conexión con datos modernos:** Se enlaza en 2006-2015 con diferencia menor al 0,5% metodológica documentada en el informe de la Secretaría de Energía.

### 5. Empleo Registrado (CEP XXI)
- **Estado:** ✅ OK
- **Filas:** 10.69 MB (provincial) y 90.99 MB (departamental).
- **Cobertura temporal:** 2007 a 2025.
- **Sectores clave:** CLAE 06 (Extracción de petróleo y gas) y CLAE 09 (Servicios de apoyo).
- **Departamentos petroleros identificados:** Añelo, Pehuenches, Confluencia (Neuquén), Escalante (Chubut), Deseado (Santa Cruz).

---

## Qué preguntas NO se pueden responder con los datos actuales
1. **Costos exactos y rentabilidad financiera por pozo individual:** La Secretaría de Energía no publica el OPEX ni el CAPEX auditado por pozo (solo inversiones agregadas por concesión). No debe inferirse rentabilidad financiera individual sin costos declarados.
2. **Atribución causal estricta de emisiones a pozos específicos:** Las detecciones satelitales de venteo registran anomalías térmicas en un radio de pixeles. No debe imputarse una antorcha a un pozo particular sin cruce de coordenadas de alta precisión.
