# Documento Metodológico del Proyecto

**Título de trabajo:** Argentina vuelve a producir petróleo: ¿qué cambió?  
**Subtítulo:** Del pozo al país: 75 años de producción, expansión territorial, inversión, empleo y comercio energético.

---

## 1. Fuentes Oficiales y Primarias

1. **Secretaría de Energía de la Nación:**
   - Producción mensual de petróleo, gas y agua por pozo (Capítulo IV).
   - Serie histórica nacional de petróleo desde 1950.
   - Datos técnicos de fractura de pozos no convencionales (Adjunto IV).
   - Trayectorias direccionales de pozo en Vaca Muerta (Res. 319/93).
   - Estadísticas de pozos terminados, en perforación y metros perforados.
   - Declaraciones juradas de inversiones upstream (Res. 2057).
   - Reservas comprobadas, probables y posibles al 31/12/2024 y 31/12/2025.
   - Puntos de venteo declarados y detección satelital de venteos.

2. **Centro de Estudios para la Producción (CEP XXI) / Secretaría de Industria:**
   - Puestos de trabajo asalariados registrados del sector privado por provincia y sector de actividad (CLAE 2 dígitos).
   - Puestos de trabajo a nivel departamental (INDEC).

3. **The World Bank (Open Data):**
   - Rentas del petróleo como % del PIB (*Oil rents, % of GDP*).
   - Participación de combustibles en comercio exterior (importaciones y exportaciones).

---

## 2. Definiciones Operativas y Reglas de Negocio

### Pozo Activo
Un pozo se clasifica como **activo** en el mes t si y solo si:
`prod_pet(i,t) > 0 OR prod_gas(i,t) > 0`

### Clasificación Convencional vs No Convencional
- **No Convencional:** Pozos catalogados en el padrón oficial como `NO CONVENCIONAL` o cuya formación productiva principal corresponde a `Vaca Muerta`, `Los Molles`, u otras formaciones tight/shale declaradas por la operadora bajo concesión de explotación no convencional (CENCH).
- **Convencional:** Pozos catalogados como `CONVENCIONAL` en yacimientos tradicionales.

### Unidades de Medida
- **Petróleo:** Metros cúbicos (m3) en datos primarios. En visualizaciones macro se reporta en miles de metros cúbicos (Mm3 o km3) o barriles diarios (bpd), utilizando la equivalencia estándar de la industria: `1 m3 = 6.28981 barriles`.
- **Gas:** Miles de metros cúbicos (miles m3 o dam3).
- **Agua:** Metros cúbicos (m3).
- **Arena de fractura:** Toneladas (tn).

### Definición de Cohortes de Pozos
La **cohorte** de un pozo se define por el año civil de su primera producción comercial registrada:
`Cohorte(i) = min [ year(fecha(i,t)) | prod_pet(i,t) > 0 ]`

El **mes de vida** (age) de un pozo se calcula como los meses transcurridos desde dicha fecha inicial:
`Mes de vida(i,t) = meses(fecha(i,t) - fecha_inicio(i))`

---

## 3. Tasas de Match en Cruces de Datos Auditadas

| Cruce | Clave de Enlace | Cobertura / Tasa de Match | Observaciones |
|---|---|---|---|
| **Producción Mensual ↔ Padrón Pozos** | `idpozo` (BIGINT) | **100,0%** (85.305 de 85.305 pozos) | Sin pérdidas de datos. |
| **Fracturas Adjunto IV ↔ Padrón Pozos** | `idpozo` (BIGINT) | **96,06%** (4.728 de 4.922 registros) | 4.484 pozos únicos enlazados. |
| **Trayectorias Vaca Muerta ↔ Padrón Pozos** | `sigla` (VARCHAR) | **97,26%** (1.879 de 1.932 siglas) | Limpieza de espacios y mayúsculas. |

---

## 4. Limitaciones del Estudio

1. **No causalidad sin modelo contrafáctico:** La coincidencia temporal entre la expansión de Vaca Muerta y el crecimiento del empleo o superávit comercial no implica que el 100% de la variación macroeconómica sea atribuible exclusivamente a la actividad hidrocarburífera. Se documenta como evolución concomitante.
2. **Ausencia de costos unitarios:** La Secretaría de Energía publica volúmenes físicos e inversiones globales, pero no el desglose de lifting cost por pozo. Toda métrica de productividad se refiere a eficiencia física (volumen por etapa, volumen por metro horizontal), nunca a rentabilidad financiera neta.
