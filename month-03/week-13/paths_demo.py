from pathlib import Path

folder = Path("data/raw/lga_facilities")
print("Folder exists:", folder.exists())

for path in sorted(folder.glob("*.csv")):
    print(path.name, "| stem:", path.stem, "| suffix:", path.suffix)
output = Path("data/processed") / "lga_points"
output.mkdir(parents = True, exist_ok = True)
print("Output folder ready:", output)