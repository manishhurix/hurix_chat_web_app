from .db import get_user, save_chat, get_chats, delete_chat as db_delete_chat, save_message, get_messages
from datetime import datetime

def start_new_chat(user_id, title="New Chat"):
    chat_data = {"title": title}
    return save_chat(user_id, chat_data)

def get_chat_history(user_id):
    return get_chats(user_id)

def delete_chat(user_id, chat_id):
    db_delete_chat(user_id, chat_id)

def add_message(user_id, chat_id, message, role):
    message_data = {
        "user_id": user_id,
        "role": role,
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    return save_message(chat_id, message_data)

def get_messages_for_chat(chat_id):
    return get_messages(chat_id) 