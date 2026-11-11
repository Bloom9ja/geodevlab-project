# import pandas as pd
# import geopandas as gpd

# table = pd.read_csv('data/raw/Schools_in_Odeda.csv')
# print(table.head(3))

# schools = gpd.GeoDataFrame(
#     table,
#     geometry = gpd.points_from_xy(table['x'], table['y']),
#     crs = 'EPSG:4326'
# )

# print(schools.head(3))
# print(schools.crs)

# schools.to_file('data/processed/schools.gpkg', layer='schools')
# print('Saved', len(schools), 'schools')

# THE ABOVE CODE CREATED AN OUTLIER WITH 0,0 COORDINATE.

# USED AI TO FIND A SOLUTION

import geopandas as gpd
import pandas as pd

table = pd.read_csv('data/raw/Schools_in_Odeda.csv')

# 1. Inspect rows with missing or out-of-bounds coordinates (Odeda is roughly x: 3.1-3.9, y: 7.0-7.7)
bad_rows = table[
    table['x'].isna()
    | table['y'].isna()
    | (table['x'] < 2)
    | (table['x'] > 5)
    | (table['y'] < 5)
    | (table['y'] > 9)
]
print('Outlier rows found:', len(bad_rows))
print(bad_rows[['fid', 'x', 'y']])

# 2. Keep only valid coordinates inside the expected region
clean_table = table[
    table['x'].between(2, 5) & table['y'].between(5, 9)
].copy()

# 3. Create GeoDataFrame in WGS 84 and reproject to UTM Zone 31N
schools = gpd.GeoDataFrame(
    clean_table,
    geometry=gpd.points_from_xy(clean_table['x'], clean_table['y']),
    crs='EPSG:4326',
)
schools = schools.to_crs('EPSG:32631')

schools.to_file('data/processed/schools.gpkg', layer='schools')
print('Saved', len(schools), 'clean schools')
