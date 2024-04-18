import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["ProjectMinor"]

cursor = collection.find({}, {"Weg": 1})  
values = [(doc["Weg"]) for doc in cursor]

with open("data/test.txt", "w", encoding="utf-8") as f:
    for weg, bloemenaanbod in values:
        f.write(weg)

client.close()
