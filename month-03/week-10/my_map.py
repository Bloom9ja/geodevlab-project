import geopandas as gpd
import matplotlib.pyplot as plt

settlements = gpd.read_file('data/processed/settlements_utm31.gpkg')
schools = gpd.read_file('data/processed/schools.gpkg', layer = 'schools')

fig, ax = plt.subplots(figsize = (7, 8))
settlements.plot(ax=ax, color = '#E6f2f3', edgecolor = '#037e8e')
schools.plot(ax=ax, color = '#094923', markersize = 18)
ax.set_title('Schools in Odeda LGA')
ax.set_axis_off()

fig.savefig('month-03/week-10/my_map.png', dpi = 300, bbox_inches = 'tight')
print('Map saved')