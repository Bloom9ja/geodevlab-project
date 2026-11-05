import csv

def read_rows(filename):
    with open(filename, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def clean_values(rows, column):
    values = []
    for row in rows:
        raw = row[column].strip()
        if raw == "":
            continue
        values.append(float(raw))
    return values

def summarise(values):
    if len(values) == 0:
        return{'count': 0, 'smallest': None, 'largest': None, 'average': None}
    return{
        'count': len(values),
        'smallest': min(values),
        'largest': max(values),
        'average': sum(values) / len(values),
    }

rows = read_rows('Odeda_Settlements_singleparts.csv')
values = clean_values(rows, 'Shape__Are')
result = summarise(values)
print(result)

def summarise_all(filename, columns):
    rows = read_rows(filename)
    report = {}
    for column in columns:
        values = clean_values(rows, column)
        report[column] = summarise(values)
    return report

report = summarise_all('Odeda_Settlements_singleparts.csv', ['Shape__Are', 'Population'])

for column, stats in report.items():
    print(column, '>', stats)