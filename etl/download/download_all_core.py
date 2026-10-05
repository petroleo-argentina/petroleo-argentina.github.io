import os
import sys
import json
import logging
from pathlib import Path
from download_official import download_resource

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("download_core")

DATASETS_TO_DOWNLOAD = [
    # 1. Producción No Convencional y Padrón de Pozos Oficial (Capítulo IV)
    {
        "source_id": "produccion_no_convencional_oficial",
        "subfolder": "energia",
        "filename": "produccion-de-pozos-de-gas-y-petroleo-no-convencional.csv",
        "url": "http://datos.energia.gob.ar/dataset/c846e79c-026c-4040-897f-1ad3543b407c/resource/b5b58cdc-9e07-41f9-b392-fb9ec68b0725/download/produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv"
    },
    {
        "source_id": "padron_pozos_cap4_oficial",
        "subfolder": "energia",
        "filename": "capitulo-iv-pozos.csv",
        "url": "http://datos.energia.gob.ar/dataset/c846e79c-026c-4040-897f-1ad3543b407c/resource/cb5c0f04-7835-45cd-b982-3e25ca7d7751/download/capitulo-iv-pozos.csv"
    },
    # 2. Fractura de pozos (Adjunto IV) - CRÍTICA
    {
        "source_id": "fractura_pozos",
        "subfolder": "energia",
        "filename": "datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv.csv",
        "url": "http://datos.energia.gob.ar/dataset/71fa2e84-0316-4a1b-af68-7f35e41f58d7/resource/2280ad92-6ed3-403e-a095-50139863ab0d/download/datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv"
    },
    # 3. Trayectorias de pozo Vaca Muerta
    {
        "source_id": "trayectorias_vaca_muerta",
        "subfolder": "energia",
        "filename": "trayectorias-de-pozo-vaca-muerta.csv",
        "url": "http://datos.energia.gob.ar/dataset/f5c0b5a5-b402-44d7-8fe0-f9e4fcb78b8d/resource/94741ac7-4f46-4efe-b112-d3f82a4ef7c5/download/trayectorias-de-pozo-vaca-muerta.csv"
    },
    # 4. Inversiones Upstream (Res. 2057)
    {
        "source_id": "inversiones_upstream",
        "subfolder": "energia",
        "filename": "resolucion-2057-inversiones-realizadas-mensual.csv",
        "url": "http://datos.energia.gob.ar/dataset/83fd2c3f-e0f5-4d56-a3ef-828eac226ba9/resource/c0a6f94a-6052-48db-9dc8-4d6ce64ecf62/download/resolucin-2057-inversiones-realizadas-mensual.csv"
    },
    {
        "source_id": "inversiones_upstream",
        "subfolder": "energia",
        "filename": "resolucion-2057-inversiones-realizadas-anio-anterior.csv",
        "url": "http://datos.energia.gob.ar/dataset/83fd2c3f-e0f5-4d56-a3ef-828eac226ba9/resource/285d45e5-1b88-4dae-8e5c-c01843c7c8c0/download/resolucin-2057-inversiones-realizadas-ao-anterior.csv"
    },
    {
        "source_id": "inversiones_upstream",
        "subfolder": "energia",
        "filename": "resolucion-2057-inversiones-previstas-anio-actual.csv",
        "url": "http://datos.energia.gob.ar/dataset/83fd2c3f-e0f5-4d56-a3ef-828eac226ba9/resource/8ab4098a-842b-42f7-bf1a-b7b3637d226d/download/resolucin-2057-inversiones-previstas-ao-actual.csv"
    },
    # 5. Reservas de petróleo y gas
    {
        "source_id": "reservas_hidrocarburos",
        "subfolder": "energia",
        "filename": "reservas_al_31-12-2025.zip",
        "url": "http://www.energia.gob.ar/contenidos/archivos/Reorganizacion/informacion_del_mercado/mercado_hidrocarburos/informacion_estadistica/reservas/reservas_al_31-12-2025.zip"
    },
    {
        "source_id": "reservas_hidrocarburos",
        "subfolder": "energia",
        "filename": "reservas_al_31-12-2024.zip",
        "url": "http://www.energia.gob.ar/contenidos/archivos/Reorganizacion/informacion_del_mercado/mercado_hidrocarburos/informacion_estadistica/reservas/reservas_al_31-12-2024.zip"
    },
    # 6. Perforación de pozos (pozos terminados, en perforación, metros perforados)
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "pozos-terminados-2009-en-adelante.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/9f365d8c-c689-42b7-a3aa-1ce98c691379/download/pozos-terminados-2009-en-adelante.csv"
    },
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "pozos-terminados-anterior-al-2009.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/7d1948c6-6944-4563-bab7-4e2a30fd22b7/download/pozos-terminados-anterior-al-2009.csv"
    },
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "pozos-en-perforacion-2009-en-adelante.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/034b7f43-7f2e-4b2a-a9e9-b003a2745cf0/download/pozos-en-perforacion-2009-en-adelante.csv"
    },
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "pozos-en-perforacion-anterior-al-2009.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/7ce5fe75-3501-44eb-bd41-118c7bc76f5b/download/pozos-en-perforacion-anterior-al-2009.csv"
    },
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "metros-perforados-2009-en-adelante.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/c0bdf731-0cf8-4c92-ad57-0a25697ea3fc/download/metros-perforados-2009-en-adelante.csv"
    },
    {
        "source_id": "perforacion_pozos",
        "subfolder": "energia",
        "filename": "metros-perforados-anterior-al-2009.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ea2ac77-d7a0-4129-9fbf-6f1a25d94e21/resource/e3f4340d-d40b-410a-b30f-e2213d28eb44/download/metros-perforados-anterior-al-2009.csv"
    },
    # 7. Empleo registrado por provincia y departamento
    {
        "source_id": "empleo_provincia",
        "subfolder": "empleo",
        "filename": "puestos_priv_provincia_clae2.csv",
        "url": "https://cdn.produccion.gob.ar/cdn-cep/datos-por-provincia/por-provincia-clae2/puestos/puestos_priv.csv"
    },
    {
        "source_id": "empleo_departamento",
        "subfolder": "empleo",
        "filename": "puestos_depto_priv_clae2.csv",
        "url": "https://cdn.produccion.gob.ar/cdn-cep/datos-por-departamento/puestos/puestos_depto_priv_por_clae2.csv"
    },
    # 8. Venteos de gas (Declarados y detectados satelitalmente)
    {
        "source_id": "puntos_venteo",
        "subfolder": "ambiente",
        "filename": "produccion-hidrocarburos-puntos-de-venteo-declarados.csv",
        "url": "http://datos.energia.gob.ar/dataset/530bb019-32f4-4eaf-b550-1fc05f8b129f/resource/c3812323-0c38-43b7-8bc6-f05fb5113626/download/produccin-hidrocarburos-puntos-de-venteo-declarados.csv"
    },
    {
        "source_id": "puntos_venteo",
        "subfolder": "ambiente",
        "filename": "sensores-remotos-venteos-detectados.csv",
        "url": "http://datos.energia.gob.ar/dataset/7ef45681-a7de-440c-a343-b7d989261b58/resource/a094f5c6-3ba9-4faf-88f3-726e4ef03a98/download/sensores-remotos-venteos-detectados.csv"
    },
    # 9. Refinerías de hidrocarburos
    {
        "source_id": "refinacion",
        "subfolder": "energia",
        "filename": "refinacion-hidrocarburos-refinerias.csv",
        "url": "http://datos.energia.gob.ar/dataset/a9eed347-78ab-45c0-a489-b227fe42ee1b/resource/fcad1e1a-1cb1-4ef8-8529-ea4ee5ef548a/download/refinacin-hidrocarburos-refineras.csv"
    },
    # 10. Ductos de transporte
    {
        "source_id": "instalaciones",
        "subfolder": "energia",
        "filename": "instalaciones-hidrocarburos-ductos-res-319-93.csv",
        "url": "http://datos.energia.gob.ar/dataset/84681f81-dbbb-49eb-be30-e61778736ad9/resource/857bd3ad-9a8b-4cf9-8e25-a8bc73f3282f/download/instalaciones-hidrocarburos-ductos-res-319-93.csv"
    }
]

def main():
    logger.info("Starting download of core official datasets (%d resources)...", len(DATASETS_TO_DOWNLOAD))
    success_count = 0
    fail_count = 0
    
    for item in DATASETS_TO_DOWNLOAD:
        # Check if already downloaded
        dest = BASE_DIR / "data" / "raw" / item["subfolder"] / item["filename"]
        if dest.exists() and dest.stat().st_size > 500:
            logger.info("File %s already exists (%0.2f MB), skipping.", item["filename"], dest.stat().st_size / (1024*1024))
            success_count += 1
            continue
            
        res = download_resource(
            source_id=item["source_id"],
            subfolder=item["subfolder"],
            filename=item["filename"],
            url=item["url"]
        )
        if res.get("success"):
            success_count += 1
        else:
            fail_count += 1
            
    logger.info("Finished downloading core datasets: %d SUCCESS, %d FAILED.", success_count, fail_count)

if __name__ == "__main__":
    main()
