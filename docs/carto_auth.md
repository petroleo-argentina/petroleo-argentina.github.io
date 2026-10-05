# Guía de Autenticación y Seguridad CARTO

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Propósito:** Especificar el protocolo de autenticación, alcance mínimo de permisos (least privilege) y protección de credenciales para la cartografía base del proyecto.

---

## 1. Protocolo de Credenciales y Cero Secretos en Repositorio

El API Access Token de CARTO es una credencial de acceso que **nunca debe quedar expuesta ni versionada**:
- **Prohibido:** Hardcodear el token dentro de `frontend/app.js`, archivos JSON o documentación.
- **Prohibido:** Versionar el archivo `frontend/config.js` en Git.
- **Configuración local:**
  1. Existe una plantilla pública versionada: [`frontend/config.example.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/config.example.js):
     ```javascript
     window.APP_CONFIG = {
       CARTO_TOKEN: "",
       CARTO_API_BASE: ""
     };
     ```
  2. Cada desarrollador o entorno de despliegue genera su propio [`frontend/config.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/config.js) local.
  3. [`frontend/config.js`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/frontend/config.js) está expresamente ignorado en [`.gitignore`](file:///C:/Users/ESCRITORIO/.gemini/antigravity-ide/scratch/petroleo-argentina/.gitignore).

---

## 2. Alcance Mínimo del Token (Least Privilege Grants)

En la consola de CARTO Workspace (*Developers -> API Access Tokens*):

| Servicio | Estado Recomendado | Justificación de Seguridad |
| :--- | :--- | :--- |
| **Maps API** | **ON** | Requerido exclusivamente para la descarga de teselas vectoriales/raster del basemap. |
| **SQL API** | **OFF** | Innecesario. Los datos del proyecto se sirven localmente mediante FastAPI y archivos Parquet/JSON estáticos auditados. |
| **Exports API** | **OFF** | Innecesario en la aplicación de frontend. |
| **LDS API** | **OFF** | Innecesario (no se utilizan servicios de geocodificación en vivo). |
| **MCP Server** | **OFF** | Innecesario para la visualización pública. |

### Grants de Recursos
- **No activar:** `Allow access to all sources`.
- **Configurar:** Acceso de lectura únicamente al basemap o capa cartográfica específica asignada.

---

## 3. Restricción por Origen (Allowed Referers URLs)

Para impedir el uso no autorizado del token desde dominios ajenos, configurar en CARTO:

### Entorno de Desarrollo Local
```text
http://127.0.0.1:8000
http://127.0.0.1:8000/*
http://localhost:8000
http://localhost:8000/*
```

### Entorno de Producción
```text
https://<dominio-definitivo>
https://<dominio-definitivo>/*
```

---

## 4. Fallback Automático sin Autenticación

Si `frontend/config.js` no existe, el token está vacío o CARTO responde con códigos de error (401 Unauthorized, 403 Forbidden, 429 Too Many Requests):
1. La aplicación detecta automáticamente la ausencia o falla del token.
2. Se activa de inmediato el estilo vectorial propio:
   `./styles/petroleo-map-style.json`
3. Se registra únicamente una advertencia técnica neutra en consola:
   `CARTO basemap unavailable. Using fallback map style.`
4. La experiencia visual del usuario permanece 100% operativa, sin bloqueos ni marcas de agua `API KEY REQUIRED`.
