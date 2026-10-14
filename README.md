# Petróleo en Argentina · Del pozo al país

Una historia en mapas sobre la producción petrolera argentina entre 1950 y 2025, con ocho capítulos y filtros para explorar los datos.

[Ver la web](https://petroleo-argentina.github.io/) · [Repositorio](https://github.com/petroleo-argentina/petroleo-argentina.github.io)

## El recorrido

1. El regreso: la producción histórica y el máximo de 1998.
2. El mapa se mueve: el cambio entre cuencas.
3. El punto de quiebre: convencional y no convencional.
4. Pocos pozos, mucho petróleo: concentración de la producción.
5. Cómo cambió el pozo: longitud horizontal y fracturas.
6. Generaciones de pozos: producción a edades comparables.
7. Del pozo al país: comercio exterior y empleo.
8. Argentina en el mundo: comparación internacional de la EIA, con corte en 2024.

## Abrir en tu PC

Desde la carpeta del repositorio, con Python instalado:

```sh
python -m http.server 8080 --directory frontend
```

Abrí http://localhost:8080. Los datos están incluidos en `frontend/data_bundle.js`; los mapas de fondo y las bibliotecas de gráficos necesitan internet.

Para trabajar con la API:

```sh
pip install -r requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Abrí http://127.0.0.1:8000. También está disponible `iniciar_servidor.bat` en Windows.
Podés copiar `frontend/config.example.js` como `frontend/config.js` para configurar CARTO; sin token se utiliza el mapa de respaldo. No pongas credenciales privadas en archivos que recibe el navegador.

## Comprobar antes de publicar

```sh
python -m pytest tests -q
node --check frontend/app.js
node --test tests/frontend.test.cjs
```

Las pruebas de API se ejecutan sin levantar un servidor. La prueba antigua de Edge es opcional: requiere Selenium, su controlador, el servidor en el puerto 8000 y `RUN_BROWSER_TESTS=1`. Revisá también la interfaz en escritorio y celular cuando cambien los estilos.

GitHub Actions ejecuta las comprobaciones antes de publicar `frontend/` en Pages. En GitHub, elegí **Settings → Pages → Source → GitHub Actions**. Los cambios subidos a `main` o `master` activan ese proceso; también puede ejecutarse manualmente.

## Datos y estructura

- `frontend/`: web, estilos y datos empaquetados para publicación estática.
- `api/static_data/`: datos de la API. Las pruebas comparan estos archivos con el paquete de la web.
- `etl/` y `analysis/`: descarga, transformación y análisis.
- `docs/`: metodología, fuentes y decisiones.
- `tests/`: controles de datos, API y carga de la web.

Fuentes: Secretaría de Energía (Resolución 319/93 y SESCO), INDEC, estadísticas de empleo y EIA para la comparación internacional. Consultá las notas de cada gráfico para conocer su cobertura; las series no necesariamente terminan en el mismo año.

Fotografía de portada: Horacio Fernandez, «Petrosaurios», Aguada Pichana, Añelo, bajo CC BY 3.0. La portada conserva los enlaces a la imagen original y su licencia.
