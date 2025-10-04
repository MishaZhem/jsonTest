import json
import h3

# Чтение GeoJSON файла
with open('./src/assets/collisions1601.json', 'r') as file:
    geojson = json.load(file)

# Извлечение фич (features)
features = geojson['features']

# Словарь для агрегации значений Casualty по шестиугольникам
hexagons = {}
for feature in features:
    lng, lat = feature['geometry']['coordinates']
    h3_index = h3.latlng_to_cell(lat, lng, 9)  # Исправлено на latlng_to_cell
    casualty = feature['properties'].get('Casualty', 0)
    if h3_index in hexagons:
        hexagons[h3_index] += casualty
    else:
        hexagons[h3_index] = casualty

# Создание фич для шестиугольников
hexagon_features = []
for h3_index in hexagons:
    polygon = h3.cell_to_boundary(h3_index)  # geo_json=True возвращает в формате GeoJSON
    hexagon_features.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [polygon]
        },
        'properties': {
            'Casualty': hexagons[h3_index]
        }
    })
# Запись результата в новый GeoJSON файл
with open('./src/assets/collisions_hexagons.json', 'w') as file:
    json.dump({
        'type': 'FeatureCollection',
        'features': hexagon_features
    }, file)