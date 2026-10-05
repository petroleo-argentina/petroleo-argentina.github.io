# Petróleo en Argentina: Del pozo al país
### Atlas Cartográfico 3D & Crónica de Datos (1950 – 2025)

[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue?style=flat-square&logo=github)](https://github.com)
[![Licencia](https://img.shields.io/badge/Datos-Secretar%C3%ADa%20de%20Energ%C3%ADa%20(Res.%20319%2F93)-green?style=flat-square)](#fuentes-de-datos)
[![WebGL](https://img.shields.io/badge/3D%20Terrain-MapLibre%20GL%20JS-orange?style=flat-square)](https://maplibre.org)

**Petróleo en Argentina: Del pozo al país** es una plataforma interactiva de periodismo de datos y cartografía 3D que reconstruye 75 años de producción petrolera nacional, la migración geográfica del centro productivo y la revolución técnica del shale en Vaca Muerta.

---

## 🗺️ Características Principales

- **Cartografía 3D y Relieve**: Motor WebGL (MapLibre GL JS v4.7.1) con modelo digital de elevación (DEM Terrarium de AWS) con sombreado de pendientes a 315° y exageración vertical de 1.22x.
- **7 Capítulos Narrativos (Scrollytelling)**:
  1. *El regreso* (1950–2025): Serie histórica nacional y comparación contra el récord de 1998.
  2. *El mapa se mueve*: Migración del Golfo San Jorge hacia la Cuenca Neuquina.
  3. *El punto de quiebre*: El cruce histórico donde el no convencional superó al convencional.
  4. *Pocos pozos, mucho petróleo*: Concentración de Pareto (el 1% de los pozos aporta el 22,9% del crudo).
  5. *Cómo cambió el pozo*: Evolución de ramas horizontales, toneladas de arena y etapas de fractura.
  6. *Generaciones de pozos*: Curvas de declino por cohorte de perforación (2015 a 2024).
  7. *Del pozo al país*: Balanza comercial energética, divisas y empleo formal.
- **Argentinosaurus Guía Conceptual**: Mascota ilustrada y comentarista de datos reactiva que aporta hallazgos concretos y cifras auditadas según los filtros activos.
- **Controles Interactivos**:
  - Línea temporal dinámica (scrubber de 1950 a 2025) con animación continua.
  - Filtros por cuenca, tipo de recurso, corte de Pareto y métricas de fracturación.
  - Modo relato guiado y modo exploración libre con aislamiento de scroll.
- **100% Autónomo**: Funciona tanto en servidores locales como desplegado de forma 100% estática en **GitHub Pages** (incluye bundle offline con 1.86 MB de datos oficiales precompilados).

---

## 🚀 Despliegue en GitHub Pages

Este repositorio incluye un flujo de trabajo automatizado de **GitHub Actions** (`.github/workflows/deploy.yml`) que publica la aplicación automáticamente en GitHub Pages.

### Pasos para publicar:
1. Crea un repositorio en tu cuenta de GitHub (por ejemplo: `petroleo-argentina`).
2. Sube el código a GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: publicación inicial de Petróleo en Argentina"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/petroleo-argentina.git
   git push -u origin main
   ```
3. En GitHub, ve a **Settings** > **Pages**:
   - En **Build and deployment > Source**, selecciona **GitHub Actions**.
4. ¡Listo! En 1 a 2 minutos la aplicación estará en vivo en:
   ```
   https://TU_USUARIO.github.io/petroleo-argentina/
   ```

*(Nota: si prefieres la opción clásica «Deploy from a branch», selecciona la rama `main` y la carpeta `/(root)`. El archivo `index.html` redirigirá automáticamente a la aplicación).*

---

## 💻 Ejecución Local

### Opción 1: Servidor estático rápido (sin dependencias)
Solo necesitas Python 3 instalado:
```bash
python -m http.server 8080 --directory frontend
```
Luego abre tu navegador en [http://localhost:8080](http://localhost:8080).

### Opción 2: Con Backend FastAPI
Para desarrollo completo con endpoints de API:
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor uvicorn:
   ```bash
   python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   *(En Windows puedes simplemente hacer doble clic en `iniciar_servidor.bat`).*
3. Accede a [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📊 Fuentes de Datos

- **Secretaría de Energía de la Nación**: Registros oficiales pozo por pozo bajo la Resolución 319/93 (Capítulo IV).
- **SESCO**: Sistema de Estadística y Control de Operaciones Hidrocarburíferas.
- **INDEC**: Estadísticas de Intercambio Comercial Argentino (ICA) y comercio exterior de combustibles y lubricantes.
- **MTEySS**: Estadísticas de empleo registrado en el sector hidrocarburífero de la provincia de Neuquén.

---

## 📄 Licencia y Créditos

- Datos públicos abiertos conforme a las normativas de acceso a la información de la República Argentina.
- Fotografías de portada y archivo bajo licencias Creative Commons (créditos detallados en la portada de la aplicación).
