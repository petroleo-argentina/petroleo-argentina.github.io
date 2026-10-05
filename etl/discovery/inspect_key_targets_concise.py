import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ESCRITORIO\.gemini\antigravity-ide\scratch\petroleo-argentina")
CKAN_CATALOG = BASE_DIR / "config" / "discovered_ckan.json"

def main():
    with open(CKAN_CATALOG, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    targets = [
        "fractura_pozos", 
        "perforacion_pozos", 
        "reservas_hidrocarburos", 
        "inversiones_upstream", 
        "refinacion_comercializacion",
        "empleo_provincia",
        "empleo_departamento"
    ]
    
    for t in targets:
        info = data.get(t, {})
        print(f"\n==========================================")
        print(f"TARGET: {t}")
        for p in info.get("packages", [])[:2]:
            print(f"  Pkg Name: {p['name']} | Title: {p['title']}")
            print(f"  Resources count: {p.get('resources_count')}")
            for r in p.get("resources", [])[:6]:
                print(f"    * {r['name']} ({r.get('format')}) -> {r['url']}")

if __name__ == "__main__":
    main()
