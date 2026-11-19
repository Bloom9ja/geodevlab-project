import geopandas as gpd

polygons = gpd.read_file('data/processed/settlements_utm31.gpkg')

invalid_before = (~polygons.is_valid).sum()
print('Invalid geometries before:', invalid_before)

if invalid_before > 0:
    polygons['geometry'] = polygons.make_valid()
    invalid_after = (~polygons.is_valid).sum()
    print('Invalid geometrics after', invalid_after)
else:
    print('No invlaid geommeties found in the sttle ment ')