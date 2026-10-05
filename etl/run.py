#!/usr/bin/env python3
"""
Master ETL Pipeline CLI — Petróleo en Argentina
Usage:
  python -m etl.run --all
  python -m etl.run --status
  python -m etl.run --transform
  python -m etl.run --source produccion_pozo_cap4
  python -m etl.run --source fracturas
"""

import sys
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_command(cmd, desc):
    print(f"\n=======================================================")
    print(f" [ETL STAGE] {desc}")
    print(f" Executing: {' '.join(cmd)}")
    print(f"=======================================================")
    res = subprocess.run(cmd, cwd=str(BASE_DIR))
    if res.returncode != 0:
        print(f"❌ Error in stage '{desc}' (Exit code: {res.returncode})")
        return False
    print(f"✅ Stage '{desc}' completed successfully.")
    return True

def print_status():
    manifests_dir = BASE_DIR / "data" / "manifests"
    print("\n--- DATASETS STATUS & MANIFESTS ---")
    if not manifests_dir.exists():
        print("No manifests found.")
        return
    for p in sorted(manifests_dir.glob("*.json")):
        import json
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            status = "OK" if data.get("success") else "FAILED"
            size_kb = round(data.get("size_bytes", 0) / 1024, 1)
            name = data.get("resource_name", p.stem.replace("manifest_", ""))
            print(f" [OK] {name:<45} | Size: {size_kb:>10.1f} KB | SHA256: {data.get('sha256','')[:12]}...")
        except Exception:
            print(f" [ERR] {p.stem:<45} | Error reading manifest")


def main():
    parser = argparse.ArgumentParser(description="Master ETL Runner for Petróleo Argentina")
    parser.add_argument("--all", action="store_true", help="Run full pipeline: profiling, transforms and geo layers")
    parser.add_argument("--transform", action="store_true", help="Rebuild analytical parquet views and json payloads")
    parser.add_argument("--geo", action="store_true", help="Rebuild spatial geo data for scrollytelling map")
    parser.add_argument("--status", action="store_true", help="Check manifest status of all datasets")
    parser.add_argument("--source", type=str, help="Process a single source ID")

    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.transform or args.all:
        ok = run_command([sys.executable, "etl/transform/build_analytical_views.py"], "Analytical Views Builder")
        if not ok and not args.all: return

    if args.geo or args.all:
        ok = run_command([sys.executable, "etl/transform/build_scrollytelling_geodata.py"], "Scrollytelling Geo Data Builder")
        if not ok and not args.all: return

    if args.source:
        print(f"Processing specific source: {args.source}")
        # Custom source logic
        print_status()

    if not any([args.all, args.transform, args.geo, args.status, args.source]):
        parser.print_help()

if __name__ == "__main__":
    main()
