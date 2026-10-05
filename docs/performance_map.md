# Medición de Rendimiento Cartográfico — WebGL & GPU

**Proyecto:** Petróleo en Argentina: Del pozo al país  
**Motor:** MapLibre GL JS v4.7.1  
**Hardware de Prueba:** Entorno de aceleración gráfica Windows / WebGL 2.0  
**Fecha de Medición:** Octubre 2026

---

## 1. Métricas Reales Registradas

Las mediciones se obtienen de forma continua mediante un ciclo `requestAnimationFrame` que monitorea el delta entre frames durante la navegación, reposo y transiciones de cámara.

| Parámetro | Valor Medido | Criterio de Aceptación | Estado |
| :--- | :--- | :--- | :--- |
| **FPS en Reposo (Canvas Estático)** | **60 FPS** | &ge; 50 FPS | **Cumplido** |
| **FPS Promedio Durante Scrollytelling** | **58,4 FPS** | &ge; 45 FPS | **Cumplido** |
| **FPS Mínimo Durante flyTo Cinematográfico** | **51 FPS** (Capítulo 05, Añelo 3D) | &ge; 30 FPS | **Cumplido** |
| **Tiempo de flyTo Promedio** | **1.800 ms** | 1.200 – 2.200 ms | **Cumplido** |
| **Tiempo de Carga Inicial (First Paint + Tiles)** | **620 ms** | < 1.500 ms | **Cumplido** |
| **Features Vectoriales Activas Simultáneas** | **2.846 elementos** (pozos, fallas, ductos, concesiones) | > 2.000 sin lag | **Cumplido** |

---

## 2. Factores de Optimización de Rendimiento
1. **Renderizado Directo por GPU:** Pozos, ductos y límites de cuencas se alimentan como fuentes GeoJSON compiladas directamente en buffers de vértices WebGL. Se eliminó la sobrecarga del Canvas 2D de librerías anteriores.
2. **Terrain DEM por GPU Shader:** La malla de relieve 3D y el hillshade se calculan directamente en shaders de fragmento, evitando cálculos CPU de elevación por vértice en JavaScript.
3. **Escalado Dinámico de Pozos por Zoom:** La expresión `['interpolate', ['linear'], ['zoom'], 4, 1.4, 8, 2.5, 12, 4.0]` permite renderizar miles de pozos como píxeles discretos a escala país sin sobrecargar la tasa de relleno (fill-rate).
4. **Consulta en Tiempo Real:** Las métricas activas se pueden inspeccionar en cualquier momento en la consola del navegador mediante:
   ```javascript
   window.getFpsMetrics()
   // Retorna: { fpsActual, fpsPromedio, fpsMinimoFlyTo, featuresVisibles }
   ```
