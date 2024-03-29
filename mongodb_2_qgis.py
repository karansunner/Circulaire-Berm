import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['bermen']

documents = collection.find({})

features = []
for doc in documents:
    feature = {
        "type": "Feature",
        "properties": {
            "ID": doc["ID"],  
            "Bermtype": doc["Bermtype"],
            "Toevoeging": doc["Toevoeging"],
            # Add other properties you want to include
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [0, 0], [doc["Shape_Leng"], 0], [doc["Shape_Leng"], doc["Shape_Area"]], [0, doc["Shape_Area"]], [0, 0]
                ]
            ]
        }
    }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

with open('output.geojson', 'w') as f:
    json.dump(geojson_data, f)

print("GeoJSON file created successfully.")
