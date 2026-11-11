# import pandas as pd
# import geopandas as gpd

# settlements = gpd.read_file('data/processed/settlements_utm31.gpkg')
# pop = pd.read_csv('data/raw/settlements_utm31.csv')

# first_try = settlements.merge(pop, left_on = 'OBJECTID', right_on = 'OBJECTID', how = 'left')
# matched = first_try['Population'].notna().sum()
# print("Matched on first try:", matched, 'of', len(settlements))

# def clean_name(name):
#     return name.strip().upper().replace("-", " ")

# settlements['join_key'] = settlements['OBJECTID'].apply(clean_name)
# pop['join_key'] = pop['OBJECTID'].apply(clean_name)

# joined = settlements.merge(pop, on = 'join_key', how = 'left')
# matched = joined['Population'].notna().sum()

# print('Matched after cleaning:', matched, 'of', len(settlements))
# print(joined[['OBJECTID', 'Population']])

# Above commented code threw error because all of the columns matched and it simply created
# Population_x and population_y

# USED AI to inspect and get below code.

import geopandas as gpd
import pandas as pd

settlements = gpd.read_file('data/processed/settlements_utm31.gpkg')
pop = pd.read_csv('data/raw/settlements_utm31.csv')

# Check if 'Population' exists (case-insensitive)
pop_matches = [c for c in pop.columns if 'pop' in c.lower()]
if not pop_matches:
  raise KeyError(
      f'No population column found. Available columns: {pop.columns.tolist()}'
  )
pop_col = pop_matches[0]

# 1. First try: merge on OBJECTID and check the '_y' column from the CSV
first_try = settlements.merge(pop, on='OBJECTID', how='left')
matched = first_try[f'{pop_col}_y'].notna().sum()
print('Matched on first try:', matched, 'of', len(settlements))


# 2. Clean join key (convert to string first so OBJECTID integers don't crash)
def clean_name(val):
  return str(val).strip().upper().replace('-', ' ')


settlements['join_key'] = settlements['OBJECTID'].apply(clean_name)
pop['join_key'] = pop['OBJECTID'].apply(clean_name)

# Drop duplicate columns from pop before merging so you don't get _x and _y suffixes
pop_subset = pop[['join_key', pop_col]].rename(
    columns={pop_col: f'{pop_col}_csv'}
)
joined = settlements.merge(pop_subset, on='join_key', how='left')

matched = joined[f'{pop_col}_csv'].notna().sum()
print('Matched after cleaning:', matched, 'of', len(settlements))
print(joined[['OBJECTID', f'{pop_col}_csv']])
