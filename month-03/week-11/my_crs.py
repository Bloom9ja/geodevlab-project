import geopandas as gpd

polygons = gpd.read_file('data/processed/settlements_utm31.gpkg')
points = gpd.read_file('data/processed/schools.gpkg',)

print('Polygons original CRS:', polygons.crs)
print('Points original CRS:', points.crs)
print('Estimated UTM CRS:', polygons.estimate_utm_crs())

utm_epsg = 32631
polygons_utm = polygons.to_crs(epsg = utm_epsg)

polygons_utm['area_km2'] = (polygons_utm.area / 1_000_000).round(2)
print(polygons_utm[['OBJECTID', 'area_km2']])
print('Total area (km2):', round(polygons_utm['area_km2'].sum(),2))