from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://hemanth182004:h70iVn3ARYS2Hd8o@hemanthcluster1.b0mvbau.mongodb.net/")
db = client["bank"]
collection = db["user"]

def get_balance(username_id):
    try:
        document = collection.find_one({"username_id": username_id})
        if document:
            return document["balance"]
        else:
            return None
    except Exception as e:
        print(f"Error getting balance: {e}")
        return None
