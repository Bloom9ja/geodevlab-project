""" Convert every facility csv in a folder into a GeoPackage of points.
Run from the root of your repository:
    uv run month-03/week-13/batch_convert.py
"""

import logging
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd

INPUT_FOLDER = Path("data/raw/lga_facilities")
OUTPUT_FOLDER = Path("data/processed/lga_points")
SUMMARY_FILE = Path("month-03/week-13/batch_summary.csv")
LOG_FILE = Path("month-03/week-13/batch_run.log")
WORKING_CRS = "EPSG:32631"
OVERWRITE = False

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(message)s",
    handlers = [logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logging.getLogger("pyogrio").setLevel(logging.WARNING)

def csv_to_points(csv_path):
    table = pd.read_csv(csv_path)
    table = table.rename(
        columns = {"lat": "latitude", "lon": "longitude", "facility": "name"}
    )
    missing = {"latitude", "longitude"} - set(table.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    points = gpd.GeoDataFrame(
        table,
        geometry = gpd.points_from_xy(table["longitude"], table["latitude"]),
        crs = "EPSG:4326",
    )
    return points.to_crs(WORKING_CRS)

def process_one(csv_path):
    out_path = OUTPUT_FOLDER / f"{csv_path.stem}.gpkg"
    if out_path.exists() and not OVERWRITE:
        logging.info("Skipping %s, output already exists", csv_path.name)
        return {"file": csv_path.name, "status": "skipped", "points": None}
    points = csv_to_points(csv_path)
    points.to_file(out_path, layer = "facilities")
    logging.info("Converted %s: %d points", csv_path.name, len(points))
    return {"file": csv_path.name, "status": "done", "points": len(points)}

def main():
    start = time.perf_counter()
    OUTPUT_FOLDER.mkdir(parents = True, exist_ok = True)
    results = []
    for csv_path in sorted(INPUT_FOLDER.glob("*.csv")):
        try:
            results.append(process_one(csv_path))
        except Exception as error:
            logging.error("Failed on %s: %s", csv_path.name, error)
            results.append(
                {"file": csv_path.name, "status": "failed", "points": None}
            )
    summary = pd.DataFrame(results)
    summary["points"] = summary["points"].astype("Int64")
    summary.to_csv(SUMMARY_FILE, index=False)
    elapsed = time.perf_counter() - start
    logging.info("Finished %d files in %.lf seconds", len(results), elapsed)
    print(summary)

if __name__ == "__main__":
    main()