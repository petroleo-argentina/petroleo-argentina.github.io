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

## Datos y estructura

- `frontend/`: web, estilos y datos empaquetados para publicación estática.
- `api/static_data/`: datos de la API. Las pruebas comparan estos archivos con el paquete de la web.
- `etl/` y `analysis/`: descarga, transformación y análisis.
- `docs/`: metodología, fuentes y decisiones.
- `tests/`: controles de datos, API y carga de la web.

Fuentes: Secretaría de Energía (Resolución 319/93 y SESCO), INDEC, estadísticas de empleo y EIA para la comparación internacional. Consultá las notas de cada gráfico para conocer su cobertura; las series no necesariamente terminan en el mismo año.

Fotografía de portada: Horacio Fernandez, «Petrosaurios», Aguada Pichana, Añelo, bajo CC BY 3.0. La portada conserva los enlaces a la imagen original y su licencia.
