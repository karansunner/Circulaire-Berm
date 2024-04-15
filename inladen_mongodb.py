import os, json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.mydb
collection = db.ProjectMinor

# Map van de JSON-bestanden
json_files_directory = 'json'

for file_name in os.listdir(json_files_directory):
    if file_name.endswith('.json'):
        file_path = os.path.join(json_files_directory, file_name)

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                collection.insert_many(data)
                print(f"Het bestand {file_name} is succesvol geïmporteerd in MongoDB.")
            except Exception as e:
                print(f"Fout bij het importeren van {file_name} in MongoDB:", e)

client.close()