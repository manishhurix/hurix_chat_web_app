from dotenv import load_dotenv
load_dotenv()
import os


import streamlit as st
st.set_page_config(page_title="Hurix Chat LLM App", layout="wide")
from src import auth, chat, db, llm, ui, utils

def main():
    user = auth.get_logged_in_user()
    if not user:
        user = auth.login()
        if not user:
            st.stop()
    ui.render_sidebar(user)

    user_id = user.get("_id") or user.get("email")
    chat_id = st.session_state.get("selected_chat")
    uploaded_file = st.session_state.get(f"file_{chat_id}")
    file_text = None
    if uploaded_file:
        file_text = utils.parse_uploaded_file(uploaded_file)

    # Get messages for current chat
    if chat_id:
        messages = chat.get_messages_for_chat(chat_id)
    else:
        messages = []

    # Detect new user message
    prompt = st.session_state.get("_chat_input")
    if prompt:
        # Add user message
        chat.add_message(user_id, chat_id, prompt, "user")
        # Prepare model info
        selected_model_str = st.session_state.get("selected_model")
        model_name, version = selected_model_str.split(" (")
        version = version.rstrip(")")
        if "ChatGPT" in model_name:
            model = {"provider": "OpenAI", "name": "ChatGPT", "version": version}
        else:
            model = {"provider": "Anthropic", "name": "Claude", "version": version}
        # Call LLM
        files = [file_text] if file_text else None
        llm_response = llm.chat_with_model(model, messages + [{"role": "user", "content": prompt}], files=files)
        # Add LLM response
        chat.add_message(user_id, chat_id, llm_response, "assistant")
        # Clear input and rerun
        st.session_state["_chat_input"] = ""
        st.rerun()

    ui.render_chat_window(user)

if __name__ == "__main__":
    main() 