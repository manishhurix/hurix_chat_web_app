from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["hurix_chat"]

users_col = db["users"]
chats_col = db["chats"]
messages_col = db["messages"]

# Collections: users, chats, messages

# Placeholder functions

def get_user(email):
    user = users_col.find_one({"email": email})
    if not user:
        user_id = users_col.insert_one({"email": email}).inserted_id
        user = users_col.find_one({"_id": user_id})
    return user

def save_chat(user_id, chat_data):
    chat_data["user_id"] = user_id
    chat_id = chats_col.insert_one(chat_data).inserted_id
    return str(chat_id)

def get_chats(user_id):
    chats = list(chats_col.find({"user_id": user_id}))
    for c in chats:
        c["_id"] = str(c["_id"])
    return chats

def delete_chat(user_id, chat_id):
    chats_col.delete_one({"_id": ObjectId(chat_id), "user_id": user_id})
    messages_col.delete_many({"chat_id": chat_id})

def save_message(chat_id, message_data):
    message_data["chat_id"] = chat_id
    msg_id = messages_col.insert_one(message_data).inserted_id
    return str(msg_id)

def get_messages(chat_id):
    messages = list(messages_col.find({"chat_id": chat_id}))
    for m in messages:
        m["_id"] = str(m["_id"])
    return messages

def update_chat_file_context(chat_id, file_name, file_context):
    chats_col.update_one({"_id": ObjectId(chat_id)}, {"$set": {"file_name": file_name, "file_context": file_context}})

def get_chat_file_context(chat_id):
    chat = chats_col.find_one({"_id": ObjectId(chat_id)})
    if chat:
        return chat.get("file_name"), chat.get("file_context")
    return None, None

def add_file_to_chat(chat_id, file_name, file_context):
    chats_col.update_one(
        {"_id": ObjectId(chat_id)},
        {"$push": {"files": {"file_name": file_name, "file_context": file_context}}}
    )

def remove_file_from_chat(chat_id, file_name):
    chats_col.update_one(
        {"_id": ObjectId(chat_id)},
        {"$pull": {"files": {"file_name": file_name}}}
    )

def get_files_for_chat(chat_id):
    chat = chats_col.find_one({"_id": ObjectId(chat_id)})
    if chat and "files" in chat:
        return chat["files"]
    return [] 