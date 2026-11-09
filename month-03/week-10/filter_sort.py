import pandas as pd

pop = pd.read_csv('data/raw/ward_population.csv')

big = pop[pop['population_2024'] > 35000]
print(big)
print('wards over 35,ooo:', len(big))

ranked = pop.sort_values('population_2024', ascending=False)
print(ranked.head(12))

pop['population_thousands'] = pop['population_2024'] / 1000
print(pop.head(3))
print('Total population:', pop['population_2024'].sum())