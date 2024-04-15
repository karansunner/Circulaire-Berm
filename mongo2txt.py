import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["ProjectMinor"]

cursor = collection.find({}, {"Weg": 1})
values = [doc["Weg"] for doc in cursor]

with open("data/highway_names.txt", "w", encoding="utf-8") as f:
    for name in values:
        f.write(name + "\n")

client.close()

