from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://hemanth182004:h70iVn3ARYS2Hd8o@hemanthcluster1.b0mvbau.mongodb.net/")
db = client["bank"]
collection = db["user"]

def withdraw(username_id, amount):
    try:
        document = collection.find_one({"username_id": username_id})
        if document and document["balance"] >= amount:
            collection.update_one({"username_id": username_id}, {"$inc": {"balance": -amount}})
            print(f"Withdrew {amount} from {username_id}'s account")
        else:
            print(f"Insufficient balance or user not found for {username_id}")
    except Exception as e:
        print(f"Error withdrawing amount: {e}")
