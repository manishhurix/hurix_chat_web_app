from .db import get_user, save_chat, get_chats, delete_chat as db_delete_chat, save_message, get_messages, get_messages_for_user, get_chat_with_user_verification, update_chat_file_context, get_chat_file_context, add_file_to_chat, remove_file_from_chat, get_files_for_chat
from datetime import datetime

def start_new_chat(user_id, title="New Chat"):
    chat_data = {"title": title}
    return save_chat(user_id, chat_data)

def get_chat_history(user_id):
    return get_chats(user_id)

def delete_chat(user_id, chat_id):
    # Verify user owns the chat before deleting
    if not get_chat_with_user_verification(chat_id, user_id):
        raise PermissionError("User does not have permission to delete this chat")
    db_delete_chat(user_id, chat_id)

def add_message(user_id, chat_id, message, role):
    # Verify user owns the chat before adding messages
    if not get_chat_with_user_verification(chat_id, user_id):
        raise PermissionError("User does not have permission to add messages to this chat")
    
    message_data = {
        "user_id": user_id,
        "role": role,
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    return save_message(chat_id, message_data)

def get_messages_for_chat(chat_id, user_id=None):
    """Get messages for a chat with optional user verification"""
    if user_id:
        return get_messages_for_user(chat_id, user_id)
    else:
        # Fallback to old method for backward compatibility (should be phased out)
        return get_messages(chat_id)

def set_chat_file_context(chat_id, user_id, file_name, file_context):
    # Verify user owns the chat before updating
    if not get_chat_with_user_verification(chat_id, user_id):
        raise PermissionError("User does not have permission to modify this chat")
    update_chat_file_context(chat_id, file_name, file_context)

def get_file_context_for_chat(chat_id, user_id):
    # Verify user owns the chat before retrieving file context
    if not get_chat_with_user_verification(chat_id, user_id):
        return None, None
    return get_chat_file_context(chat_id)

def add_file(chat_id, user_id, file_name, file_context):
    # Verify user owns the chat before adding files
    if not get_chat_with_user_verification(chat_id, user_id):
        raise PermissionError("User does not have permission to add files to this chat")
    add_file_to_chat(chat_id, file_name, file_context)

def remove_file(chat_id, user_id, file_name):
    # Verify user owns the chat before removing files
    if not get_chat_with_user_verification(chat_id, user_id):
        raise PermissionError("User does not have permission to remove files from this chat")
    remove_file_from_chat(chat_id, file_name)

def get_files(chat_id, user_id):
    # Verify user owns the chat before retrieving files
    if not get_chat_with_user_verification(chat_id, user_id):
        return []
    return get_files_for_chat(chat_id) 