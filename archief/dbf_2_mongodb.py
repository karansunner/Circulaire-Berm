from dbfread import DBF
from pymongo import MongoClient

dbf_file_path = 'data/berm.dbf'

client = MongoClient('mongodb://localhost:27017')
db = client.mydb
collection = db.bermen

table = DBF(dbf_file_path)

for record in table:
    collection.insert_one(dict(record))

client.close()

print("Data uploaded to MongoDB successfully.")
