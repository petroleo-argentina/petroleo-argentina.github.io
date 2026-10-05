import json
import logging
import requests
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CKAN_API_BASE = "https://datos.gob.ar/api/3/action"

HEADERS = {
    "User-Agent": "PetroleoArgentinaResearch/1.0 (Data Science Competition Exploration)"
}

def search_packages(query: str, rows: int = 20) -> Optional[Dict[str, Any]]:
    url = f"{CKAN_API_BASE}/package_search"
    params = {"q": query, "rows": rows}
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data.get("result", {})
        else:
            logger.warning("CKAN returned success=False: %s", data)
            return None
    except Exception as e:
        logger.error("Error searching CKAN for query '%s': %s", query, e)
        return None

def get_package_details(package_id: str) -> Optional[Dict[str, Any]]:
    url = f"{CKAN_API_BASE}/package_show"
    params = {"id": package_id}
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data.get("result", {})
        else:
            logger.warning("CKAN returned success=False for package '%s'", package_id)
            return None
    except Exception as e:
        logger.error("Error retrieving package '%s': %s", package_id, e)
        return None

if __name__ == "__main__":
    logger.info("Testing CKAN client...")
    res = search_packages("petroleo", rows=5)
    if res:
        count = res.get("count", 0)
        logger.info("Total packages matching 'petroleo': %d", count)
        for pkg in res.get("results", []):
            logger.info(" - [%s] %s (id: %s)", pkg.get("name"), pkg.get("title"), pkg.get("id"))
    else:
        logger.error("Search failed.")
