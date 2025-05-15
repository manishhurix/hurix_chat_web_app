from .db import get_user, save_chat, get_chats, delete_chat as db_delete_chat, save_message, get_messages, update_chat_file_context, get_chat_file_context, add_file_to_chat, remove_file_from_chat, get_files_for_chat
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

def set_chat_file_context(chat_id, file_name, file_context):
    update_chat_file_context(chat_id, file_name, file_context)

def get_file_context_for_chat(chat_id):
    return get_chat_file_context(chat_id)

def add_file(chat_id, file_name, file_context):
    add_file_to_chat(chat_id, file_name, file_context)

def remove_file(chat_id, file_name):
    remove_file_from_chat(chat_id, file_name)

def get_files(chat_id):
    return get_files_for_chat(chat_id) 