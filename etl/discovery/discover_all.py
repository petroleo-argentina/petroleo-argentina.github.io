import json
import logging
from pathlib import Path
from ckan_client import search_packages, get_package_details

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("discover")

TARGET_SEARCHES = {
    "produccion_pozo_cap4": "produccion de petroleo y gas por pozo",
    "produccion_1950": "produccion de petroleo desde 1950",
    "perforacion_pozos": "perforacion de pozos",
    "fractura_pozos": "fractura",
    "reservas_hidrocarburos": "reservas de petroleo",
    "inversiones_upstream": "inversiones en mercado de hidrocarburos upstream",
    "refinacion_comercializacion": "refinacion",
    "empleo_provincia": "puestos de trabajo asalariados registrados provincia sector",
    "empleo_departamento": "puestos de trabajo departamento",
    "puntos_venteo": "venteo",
    "instalaciones_hidrocarburos": "instalaciones de hidrocarburos",
    "emisiones_gei": "gases de efecto invernadero"
}

def discover():
    discovered = {}
    
    for key, query in TARGET_SEARCHES.items():
        logger.info("Searching for target: %s (query: '%s')", key, query)
        res = search_packages(query, rows=10)
        if not res or res.get("count", 0) == 0:
            logger.warning("No packages found for '%s' with query '%s'", key, query)
            discovered[key] = {"query": query, "found": False, "packages": []}
            continue
            
        packages = []
        for pkg_summary in res.get("results", []):
            pkg_id = pkg_summary.get("id")
            pkg_name = pkg_summary.get("name")
            pkg_title = pkg_summary.get("title")
            logger.info("  Found package: %s | %s", pkg_name, pkg_title)
            
            # Fetch full details
            pkg_full = get_package_details(pkg_id)
            if not pkg_full:
                continue
                
            resources = []
            for r in pkg_full.get("resources", []):
                resources.append({
                    "id": r.get("id"),
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "format": r.get("format"),
                    "url": r.get("url"),
                    "size": r.get("size"),
                    "created": r.get("created"),
                    "last_modified": r.get("last_modified")
                })
                
            packages.append({
                "id": pkg_id,
                "name": pkg_name,
                "title": pkg_title,
                "notes": pkg_full.get("notes"),
                "organization": pkg_full.get("organization", {}).get("title"),
                "url": pkg_full.get("url"),
                "resources_count": len(resources),
                "resources": resources
            })
            
        discovered[key] = {
            "query": query,
            "found": len(packages) > 0,
            "total_matches": res.get("count", 0),
            "packages": packages
        }
        
    out_path = Path(__file__).resolve().parent.parent.parent / "config" / "discovered_ckan.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(discovered, f, indent=2, ensure_ascii=False)
    logger.info("Discovery complete. Saved catalog to %s", out_path)

if __name__ == "__main__":
    discover()
