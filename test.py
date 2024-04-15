import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["wegen"]
cursor = collection.find({}, {"Straatnaam/Weg": 1})
values = [doc["Straatnaam/Weg"] for doc in cursor]
print(type(values))
client.close()