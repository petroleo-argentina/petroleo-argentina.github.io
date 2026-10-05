import os
import json
import logging
import hashlib
import datetime
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("download_worldbank")

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_WB_DIR = BASE_DIR / "data" / "raw" / "worldbank"
MANIFEST_DIR = BASE_DIR / "data" / "manifests"

INDICATORS = {
    "oil_rents_gdp_pct": "NY.GDP.PETR.RT.ZS",
    "fuel_imports_merch_pct": "TM.VAL.FUEL.ZS.UN",
    "fuel_exports_merch_pct": "TX.VAL.FUEL.ZS.UN"
}

def download_indicator(name: str, code: str):
    url = f"https://api.worldbank.org/v2/country/ARG/indicator/{code}?format=json&per_page=1000"
    logger.info("Fetching World Bank indicator %s (%s) from %s", name, code, url)
    
    start_time = datetime.datetime.now(datetime.timezone.utc)
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        logger.error("Failed to fetch WB indicator %s: HTTP %s", code, resp.status_code)
        return False
        
    data = resp.json()
    if len(data) < 2:
        logger.warning("Empty response for WB indicator %s", code)
        return False
        
    records = []
    for item in data[1]:
        if item.get("value") is not None:
            records.append({
                "country": item.get("country", {}).get("value"),
                "countryiso3code": item.get("countryiso3code"),
                "date": item.get("date"),
                "year": int(item.get("date")),
                "value": item.get("value"),
                "indicator_id": item.get("indicator", {}).get("id"),
                "indicator_name": item.get("indicator", {}).get("value")
            })
            
    # Sort chronological
    records.sort(key=lambda x: x["year"])
    
    dest_file = RAW_WB_DIR / f"{name}.json"
    with open(dest_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    file_bytes = dest_file.read_bytes()
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    end_time = datetime.datetime.now(datetime.timezone.utc)
    
    manifest = {
        "source_id": f"worldbank_{name}",
        "resource_name": f"{name}.json",
        "original_url": url,
        "downloaded_at": end_time.isoformat(),
        "http_status": 200,
        "content_type": "application/json",
        "size_bytes": len(file_bytes),
        "sha256": sha256,
        "local_path": str(dest_file.relative_to(BASE_DIR)),
        "data_points": len(records),
        "min_year": records[0]["year"] if records else None,
        "max_year": records[-1]["year"] if records else None,
        "success": True
    }
    
    with open(MANIFEST_DIR / f"manifest_wb_{name}.json", "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2, ensure_ascii=False)
        
    logger.info("Saved %s with %d observations (%d-%d)", name, len(records), records[0]["year"], records[-1]["year"])
    return True

def main():
    RAW_WB_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    for name, code in INDICATORS.items():
        download_indicator(name, code)

if __name__ == "__main__":
    main()
