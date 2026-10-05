import os
import sys
import json
import logging
import hashlib
import datetime
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("download_official")

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_DIR = BASE_DIR / "data" / "raw"
MANIFEST_DIR = BASE_DIR / "data" / "manifests"
LOGS_DIR = BASE_DIR / "logs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192 * 1024):
            h.update(chunk)
    return h.hexdigest()

def log_error(source_id: str, url: str, error_type: str, message: str, retry_count: int = 1):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    err_obj = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_id": source_id,
        "url": url,
        "stage": "download",
        "error_type": error_type,
        "message": str(message),
        "retry_count": retry_count,
        "resolved": False,
        "fallback_used": None
    }
    with open(LOGS_DIR / "download_errors.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(err_obj, ensure_ascii=False) + "\n")

def download_resource(source_id: str, subfolder: str, filename: str, url: str, timeout: int = 60, retries: int = 3) -> dict:
    dest_dir = RAW_DIR / subfolder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / filename
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    
    start_time = datetime.datetime.now(datetime.timezone.utc)
    logger.info("Downloading [%s] -> %s from %s", source_id, filename, url)
    
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, stream=True, timeout=timeout)
            if resp.status_code == 200:
                with open(dest_file, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                            
                size_bytes = dest_file.stat().st_size
                sha256 = compute_sha256(dest_file)
                end_time = datetime.datetime.now(datetime.timezone.utc)
                
                manifest = {
                    "source_id": source_id,
                    "resource_name": filename,
                    "original_url": url,
                    "downloaded_at": end_time.isoformat(),
                    "http_status": 200,
                    "content_type": resp.headers.get("content-type", "application/octet-stream"),
                    "size_bytes": size_bytes,
                    "sha256": sha256,
                    "local_path": str(dest_file.relative_to(BASE_DIR)),
                    "success": True
                }
                
                manifest_file = MANIFEST_DIR / f"manifest_{dest_file.stem}.json"
                with open(manifest_file, "w", encoding="utf-8") as mf:
                    json.dump(manifest, mf, indent=2, ensure_ascii=False)
                    
                logger.info("Successfully downloaded %s (%0.2f MB, SHA256: %s...)", filename, size_bytes / (1024*1024), sha256[:8])
                return manifest
            else:
                logger.warning("Attempt %d failed: HTTP %s", attempt, resp.status_code)
                if attempt == retries:
                    log_error(source_id, url, f"HTTP_{resp.status_code}", f"Failed after {retries} attempts with HTTP {resp.status_code}", retries)
                    return {"source_id": source_id, "resource_name": filename, "url": url, "success": False, "error": f"HTTP_{resp.status_code}"}
        except Exception as e:
            logger.warning("Attempt %d exception: %s", attempt, e)
            if attempt == retries:
                log_error(source_id, url, type(e).__name__, str(e), retries)
                return {"source_id": source_id, "resource_name": filename, "url": url, "success": False, "error": str(e)}
                
    return {"source_id": source_id, "resource_name": filename, "url": url, "success": False, "error": "unknown"}

if __name__ == "__main__":
    logger.info("Testing official downloader with 1950 production series...")
    r1 = download_resource(
        "produccion_1950",
        "energia",
        "serie-produccion-petroleo-total-pais-desde-1950.csv",
        "http://www.energia.gob.ar/contenidos/archivos/Reorganizacion/informacion_del_mercado/mercado_hidrocarburos/informacion_estadistica/serie-produccion-petroleo-total-pais-desde-1950.csv"
    )
    r2 = download_resource(
        "produccion_1950",
        "energia",
        "serieproducciondepetroleoenargentinadesde1950.pdf",
        "http://www.energia.gob.ar/contenidos/archivos/Reorganizacion/informacion_del_mercado/publicaciones/mercado_hidrocarburos/produccion_desde_1950/serieproducciondepetroleoenargentinadesde1950.pdf"
    )
    print("Download results:", r1.get("success"), r2.get("success"))
