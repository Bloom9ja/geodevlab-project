# with open('wards.csv') as f:
#     lines = f.readlines()

# print('Number of lines is ',len(lines))

with open('wards.csv') as f:
    lines = f.readlines()

# for line in lines:
#     print(line.strip())

for line in lines[1:]:
    parts = line.strip().split(',')
    ward = parts[0]
    # area = parts[1]
    # print(ward, ' has an area of ',area)
    area_km2 = float(parts[1])
    # area_hectares = area_km2 * 100
    # print(ward, 'is', area_hectares, 'hectares')
    # print(ward, 'is', round(area_hectares,1), 'hectares')
    if area_km2 > 9:
        size = 'Large'
    else:
        size = 'Small'
    print(ward, 'is', size)