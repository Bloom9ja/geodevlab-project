import geopandas as gpd

utm_epsg = 32631
polygons = gpd.read_file('data/processed/settlements_utm31.gpkg').to_crs(epsg=utm_epsg)
points = gpd.read_file('data/processed/schools.gpkg').to_crs(epsg=utm_epsg)

joined = gpd.sjoin(
    points,
    polygons[['OBJECTID', 'geometry']],
    how = 'inner',
    predicate = 'within'
)

counts = joined.groupby('OBJECTID').size().rename('school_count').reset_index()

polygons = polygons.merge(counts, on = 'OBJECTID', how = 'left')
polygons['school_count'] = polygons['school_count'].fillna(0).astype(int)

print(polygons[['OBJECTID', 'school_count']].sort_values(by = 'school_count', ascending=False).head(10))
print('Settlements with at least 1 school:', (polygons['school_count'] > 0).sum())
print('Total counted:', polygons['school_count'].sum(), 'of', len(points))