import os
import sys
import json
import hashlib
import datetime
from pathlib import Path
import requests

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
RAW_PETRODB_DIR = BASE_DIR / "data" / "raw" / "petrodb"
MANIFEST_DIR = BASE_DIR / "data" / "manifests"

HF_BASE_URL = "https://huggingface.co/datasets/sumpalabs/petrodb/resolve/main"

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192 * 1024):
            h.update(chunk)
    return h.hexdigest()

def download_file(hf_rel_path: str, dest_path: Path) -> dict:
    url = f"{HF_BASE_URL}/{hf_rel_path}?download=true"
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    start_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"Downloading {hf_rel_path} from {url}...")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, stream=True, timeout=60)
    http_status = resp.status_code
    
    if resp.status_code != 200:
        print(f"Failed to download {hf_rel_path}: HTTP {resp.status_code}")
        return {
            "source_id": "petrodb",
            "resource_name": hf_rel_path,
            "original_url": url,
            "downloaded_at": start_time.isoformat(),
            "http_status": http_status,
            "success": False,
            "error": f"HTTP {http_status}"
        }
        
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                
    end_time = datetime.datetime.now(datetime.timezone.utc)
    file_size = dest_path.stat().st_size
    sha256 = compute_sha256(dest_path)
    
    manifest = {
        "source_id": "petrodb",
        "resource_name": hf_rel_path,
        "original_url": url,
        "downloaded_at": end_time.isoformat(),
        "http_status": http_status,
        "content_type": resp.headers.get("content-type", "application/octet-stream"),
        "size_bytes": file_size,
        "sha256": sha256,
        "local_path": str(dest_path.relative_to(BASE_DIR)),
        "success": True
    }
    
    manifest_name = f"manifest_petrodb_{dest_path.stem}.json"
    if "monthly_production" in hf_rel_path:
        manifest_name = f"manifest_petrodb_prod_{dest_path.parent.name}.json"
        
    with open(MANIFEST_DIR / manifest_name, "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2)
        
    print(f"Successfully downloaded {hf_rel_path} ({file_size / (1024*1024):.2f} MB)")
    return manifest

def main():
    RAW_PETRODB_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    
    core_files = [
        "argentina/wells.parquet",
        "argentina/well_operator_history.parquet",
        "argentina/well_events.parquet"
    ]
    
    results = []
    for cf in core_files:
        dest = RAW_PETRODB_DIR / Path(cf).name
        res = download_file(cf, dest)
        results.append(res)
        
    print(f"PetroDB core metadata download completed. Results: {len(results)}")

if __name__ == "__main__":
    main()
