from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://hemanth182004:h70iVn3ARYS2Hd8o@hemanthcluster1.b0mvbau.mongodb.net/")
db = client["bank"]
collection = db["user"]

def deposit(username_id, amount):
    try:
        collection.update_one({"username_id": username_id}, {"$inc": {"balance": amount}})
        print(f"Deposited {amount} to {username_id}'s account")
    except Exception as e:
        print(f"Error depositing amount: {e}")
