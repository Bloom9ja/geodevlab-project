import csv

# with open('odeda_settlements_singleparts.csv', encoding='utf-8-sig') as f:
#     reader = csv.DictReader(f)
#     rows = list(reader)
# print('Number of rows:', len(rows))
# print('Columns:', list(rows[0].keys()))

# with open('odeda_settlements_singleparts.csv', encoding='utf-8-sig') as f:
#     # reader = csv.DictReader(f)
#     rows = list(csv.DictReader(f))

# values = []
# for row in rows:
#     value = float(row['Shape__Are'])
#     values.append(value)

# print('Smallest:', min(values))
# print('Largest:', max(values))
# print('Count:', len(values))

# with open('odeda_settlements_singleparts.csv', encoding='utf-8-sig') as f:
#     rows = list(csv.DictReader(f))

# values = []
# for row in rows:
#     raw = row['Shape__Are'].strip()
#     if raw == '':
#         continue
#     values.append(float(raw))

# print('Smallest:', min(values))
# print('Largest:', max(values))
# print('Count:', len(values))

def inspect_column(filename, column):
    with open(filename, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    values = []
    for row in rows:
        raw = row[column].strip()
        if raw == '':
            continue
        values.append(float(raw))
    return {
        'Smallest': min(values),
        'Largest': max(values),
        'Count' : len(values),
    }
area_result = inspect_column('odeda_settlements_singleparts.csv', 'Shape__Are')
pop_result = inspect_column('odeda_settlements_singleparts.csv', 'Population')

print('Area:', area_result)
print('Population:', pop_result)