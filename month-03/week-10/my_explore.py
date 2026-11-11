import pandas as pd

pop = pd.read_csv('data/raw/settlements_utm31.csv')

print(pop.head(5))
print('Shape:', pop.shape)
print('Columns:', list(pop.columns))
print(pop.dtypes)
print(pop['Population'].describe())

import geopandas as gpd

print(gpd.list_layers('data/processed/settlements_utm31.gpkg'))

settlements = gpd.read_file('data/processed/settlements_utm31.gpkg')

print(settlements.head(5))
print('Rows and columns:', settlements.shape)
print(settlements.geom_type.value_counts())
print('CRS:', settlements.crs)
print('Bounds:', settlements.total_bounds)

first = settlements.geometry.iloc[0]
print(type(first))
print(first)
print('Valid:', first.is_valid)
print('Centroid:', first.centroid)
