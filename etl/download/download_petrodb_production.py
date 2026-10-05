import os
import sys
import json
import hashlib
import datetime
from pathlib import Path
import requests

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
PROD_DIR = BASE_DIR / "data" / "raw" / "petrodb" / "monthly_production"
MANIFEST_DIR = BASE_DIR / "data" / "manifests"

HF_BASE_URL = "https://huggingface.co/datasets/sumpalabs/petrodb/resolve/main"

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192 * 1024):
            h.update(chunk)
    return h.hexdigest()

def download_year(year: int):
    rel_hf = f"argentina/monthly_production/anio={year}/data.parquet"
    url = f"{HF_BASE_URL}/{rel_hf}?download=true"
    dest_dir = PROD_DIR / f"anio={year}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "data.parquet"
    
    if dest_file.exists() and dest_file.stat().st_size > 1000:
        print(f"Year {year} already downloaded ({dest_file.stat().st_size / (1024*1024):.2f} MB), skipping.")
        return True
        
    start_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"Downloading year {year} from {url}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        resp = requests.get(url, headers=headers, stream=True, timeout=60)
        if resp.status_code != 200:
            print(f"Failed year {year}: HTTP {resp.status_code}")
            return False
            
        with open(dest_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    
        file_size = dest_file.stat().st_size
        sha256 = compute_sha256(dest_file)
        end_time = datetime.datetime.now(datetime.timezone.utc)
        
        manifest = {
            "source_id": "petrodb_monthly_production",
            "year": year,
            "resource_name": rel_hf,
            "original_url": url,
            "downloaded_at": end_time.isoformat(),
            "http_status": resp.status_code,
            "size_bytes": file_size,
            "sha256": sha256,
            "local_path": str(dest_file.relative_to(BASE_DIR)),
            "success": True
        }
        
        with open(MANIFEST_DIR / f"manifest_petrodb_prod_{year}.json", "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, indent=2)
            
        print(f"Downloaded year {year}: {file_size / (1024*1024):.2f} MB")
        return True
    except Exception as e:
        print(f"Error downloading year {year}: {e}")
        return False

def main():
    PROD_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download 2006 to 2025
    years = list(range(2006, 2026))
    print(f"Starting download of {len(years)} years (2006-2025)...")
    successes = 0
    for y in years:
        ok = download_year(y)
        if ok:
            successes += 1
            
    print(f"PetroDB monthly production download finished: {successes}/{len(years)} years OK.")

if __name__ == "__main__":
    main()
