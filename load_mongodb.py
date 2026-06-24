import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]

print("Loading categories...")
with open("categories.json") as f:
    db.categories.drop()
    db.categories.insert_many(json.load(f))
print("Categories done!")

print("Loading products...")
with open("products.json") as f:
    db.products.drop()
    db.products.insert_many(json.load(f))
print("Products done!")

print("Loading users...")
with open("users.json") as f:
    db.users.drop()
    db.users.insert_many(json.load(f))
print("Users done!")

print("Loading transactions...")
with open("transactions.json") as f:
    db.transactions.drop()
    db.transactions.insert_many(json.load(f))
print("Transactions done!")

print("Loading sessions (sample)...")
db.sessions.drop()
for i in [0, 1]:
    with open(f"sessions_{i}.json") as f:
        db.sessions.insert_many(json.load(f))
    print(f"sessions_{i} done!")

print("All data loaded into MongoDB!")
client.close()