from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["eticaret_db"]

users = db["users"]
products = db["products"]
sepet= db["sepet"]
carts= db["carts"]