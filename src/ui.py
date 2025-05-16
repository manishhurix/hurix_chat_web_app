import streamlit as st
from .llm import get_available_models
from . import chat, utils
from . import auth
import os
from datetime import datetime
import re
import time

def reset_chat_state():
    st.session_state["selected_chat"] = None
    st.session_state["_chat_input"] = ""

def render_sidebar(user):
    logo_path = os.path.join("assets", "logo.png")
    st.sidebar.image(logo_path, width=180)
    st.sidebar.title("Hurix Chat")
    st.sidebar.write(f"Logged in as: {user['email']}")
    # Logout button
    if st.sidebar.button("Logout"):
        auth.logout()
        return
    # Model selector
    models = get_available_models()
    model_options = [f"{m['name']} ({v})" for m in models for v in m['versions']]
    if "selected_model" not in st.session_state:
        st.session_state["selected_model"] = model_options[0]
    st.sidebar.selectbox(
        "Select Model",
        model_options,
        index=model_options.index(st.session_state["selected_model"]),
        key="selected_model",
        on_change=reset_chat_state
    )
    # Chat history
    user_id = user.get("_id") or user.get("email")
    chats = chat.get_chat_history(user_id)
    chat_titles = [c.get("title", "Untitled") for c in chats]
    chat_ids = [c["_id"] for c in chats]
    if "selected_chat" not in st.session_state and chat_ids:
        st.session_state["selected_chat"] = chat_ids[0]
    selected = st.sidebar.radio("Chats", chat_ids, format_func=lambda cid: chat_titles[chat_ids.index(cid)] if cid in chat_ids else "Untitled",
                                index=chat_ids.index(st.session_state["selected_chat"]) if st.session_state.get("selected_chat") in chat_ids else 0) if chat_ids else None
    st.session_state["selected_chat"] = selected
    # New chat
    if st.sidebar.button("New Chat"):
        new_chat_id = chat.start_new_chat(user_id)
        st.session_state["selected_chat"] = new_chat_id
        st.rerun()
        return
    # Delete chat
    if st.sidebar.button("Delete Chat") and st.session_state.get("selected_chat"):
        chat.delete_chat(user_id, st.session_state["selected_chat"])
        st.session_state["selected_chat"] = chat_ids[0] if chat_ids else None
        st.rerun()
        return

def render_markdown_with_copy(md_text):
    # Find code blocks (```lang\n...\n```)
    code_block_pattern = r"```([\w]*)\n([\s\S]*?)```"
    last_end = 0
    for match in re.finditer(code_block_pattern, md_text):
        # Render markdown before code block
        if match.start() > last_end:
            st.markdown(md_text[last_end:match.start()])
        lang = match.group(1) or None
        code = match.group(2)
        st.code(code, language=lang)
        last_end = match.end()
    # Render any remaining markdown
    if last_end < len(md_text):
        st.markdown(md_text[last_end:])

def render_chat_window(user):
    st.header("Chat Window")
    user_id = user.get("_id") or user.get("email")
    chat_id = st.session_state.get("selected_chat")
    if not chat_id:
        st.info("Start a new chat to begin.")
        return
    # Show messages
    messages = chat.get_messages_for_chat(chat_id)
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        timestamp = m.get("timestamp")
        sender = "You" if role == "user" else "Assistant"
        ts_str = ""
        if timestamp:
            try:
                ts = datetime.fromisoformat(timestamp)
                ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                ts_str = timestamp
        with st.chat_message(role):
            st.markdown(f"**{sender}**  ")
            render_markdown_with_copy(content)
            if ts_str:
                st.caption(ts_str)
    st.markdown("---")
    chat_input_enabled = True

    # Show a message if a file is uploaded and will be used as context
    if "uploaded_file_content" in st.session_state and "uploaded_file_name" in st.session_state:
        st.info(f"Document '{st.session_state['uploaded_file_name']}' is attached and will be used as additional context for your queries.")

    # Remove upload icon and its HTML/CSS, keep only the hidden file uploader
    prompt = st.chat_input("Type your message...", disabled=not chat_input_enabled)

    # Hidden file uploader remains for programmatic use
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key="file_uploader_hidden"
    )
    if uploaded_file is not None:
        from . import utils
        file_content = utils.parse_uploaded_file(uploaded_file)
        file_name = uploaded_file.name
        if file_content and not file_content.startswith("Unsupported"):
            st.session_state["uploaded_file_content"] = file_content
            st.session_state["uploaded_file_name"] = file_name
            st.success(f"Uploaded: {file_name}")
        else:
            st.warning("Could not read file content.")

    # When user sends a prompt, include file content as context if available
    if prompt:
        try:
            # Add user message
            chat.add_message(user_id, chat_id, prompt, "user")
            # Show spinner only when waiting for LLM
            with st.spinner("Waiting for assistant response..."):
                from . import llm
                selected_model_str = st.session_state.get("selected_model")
                model_name, version = selected_model_str.split(" (")
                version = version.rstrip(")")
                if "ChatGPT" in model_name:
                    model = {"provider": "OpenAI", "name": "ChatGPT", "version": version}
                else:
                    model = {"provider": "Anthropic", "name": "Claude", "version": version}
                messages = chat.get_messages_for_chat(chat_id) + [{"role": "user", "content": prompt}]
                # Add file content as context if available
                files = None
                if "uploaded_file_content" in st.session_state:
                    files = [st.session_state["uploaded_file_content"]]
                llm_response = llm.chat_with_model(model, messages, files=files)
                st.write("DEBUG: LLM response:", llm_response)  # Debug output
                if llm_response.startswith("[LLM Error"):
                    st.error(llm_response)
                else:
                    chat.add_message(user_id, chat_id, llm_response, "assistant")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            import traceback
            st.text(traceback.format_exc())
        st.rerun()
        return 