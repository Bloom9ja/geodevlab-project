import geopandas as gpd
import matplotlib.pyplot as plt

utm_epsg = 32631
polygons = gpd.read_file('data/processed/settlements_utm31.gpkg').to_crs(epsg=utm_epsg)
points = gpd.read_file('data/processed/schools.gpkg').to_crs(epsg=utm_epsg)

polygons['area_km2'] = polygons.area / 1_000_000

reach = points[['geometry']].copy()
reach['geometry'] = reach.buffer(1000)
reach = reach.dissolve()

uncovered = gpd.overlay(polygons, reach, how='difference')
uncovered['uncovered_km2'] = uncovered.area / 1_000_000

gaps = uncovered[['OBJECTID', 'uncovered_km2']]
result = polygons.merge(gaps, on='OBJECTID', how='left')
result['uncovered_km2'] = result['uncovered_km2'].fillna(0)
result['uncovered_pct'] = (result['uncovered_km2'] / result['area_km2']) * 100
result['covered_pct'] = 100 - result['uncovered_pct']

print(result[['OBJECTID', 'area_km2', 'uncovered_km2', 'uncovered_pct']].round(2).head(10))
print('Total uncovered settlement area (km2):', round(result['uncovered_km2'].sum(), 2))

result.to_file('data/processed/week11_school_reach.gpkg', layer='settlement_reach', driver='GPKG')
uncovered.to_file('data/processed/week11_school_reach.gpkg', layer='uncovered_areas', driver='GPKG')
print('Saved outputs to data/processed/week11_school_reach.gpkg')

# Make map
fig, ax = plt.subplots(figsize=(7, 8))
polygons.plot(ax=ax, color='#E6f2f3', edgecolor='#037e8e', linewidth=0.4)
uncovered.plot(ax=ax, color='#e63946', alpha=0.8)
points.plot(ax=ax, color='#094923', markersize=18)

ax.set_title('Settlement School Reach (1 km Buffer)')
ax.set_axis_off()

fig.savefig('month-03/week-11/new_my_map.png', dpi=300, bbox_inches='tight')
print('Map saved to month-03/week-11/new_my_map.png')
