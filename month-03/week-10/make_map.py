import geopandas as gpd
import matplotlib.pyplot as plt

wards = gpd.read_file('data/processed/wards.gpkg', layer = 'wards')
facilities = gpd.read_file('data/processed/facilities.gpkg', layer = 'facilities')

fig, ax = plt.subplots(figsize = (7,8))
wards.plot(ax=ax, color= '#E6F2F3', edgecolor ='#037e8e')
facilities.plot(ax=ax, color='#E08986', markersize=18)
ax.set_title('Health facilities in Ibadan North')
ax.set_axis_off()

fig.savefig('month-03/week-10/facilities_map.png', dpi=300, bbox_inches='tight')
print('Map Saved')