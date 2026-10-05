import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
CKAN_CATALOG = BASE_DIR / "config" / "discovered_ckan.json"

def main():
    with open(CKAN_CATALOG, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} search targets.")
    
    selected_sources = {}
    
    # Let's inspect each target's found packages
    for target_key, info in data.items():
        print(f"\n==========================================")
        print(f"TARGET: {target_key} (Query: '{info['query']}')")
        pkgs = info.get("packages", [])
        print(f"Total packages discovered: {len(pkgs)}")
        for idx, p in enumerate(pkgs):
            print(f" [{idx}] Pkg Name: {p['name']}")
            print(f"     Title: {p['title']}")
            print(f"     Org: {p.get('organization')}")
            print(f"     Resources ({p.get('resources_count')}):")
            for r in p.get("resources", [])[:5]:
                print(f"       - {r['name']} | Format: {r['format']} | URL: {r['url']}")
            if p.get("resources_count", 0) > 5:
                print(f"       ... and {p['resources_count'] - 5} more resources")

if __name__ == "__main__":
    main()
