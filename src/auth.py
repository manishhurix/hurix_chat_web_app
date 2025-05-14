import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req
from urllib.parse import urlencode

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://hurixchatchat.streamlit.app/")
# REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/")


# st.write("REDIRECT URI:", REDIRECT_URI)

def login():
    if "user" in st.session_state:
        return st.session_state["user"]

    # Step 1: Get authorization code
    if "code" not in st.query_params:
        # Show logo
        logo_path = os.path.join("assets", "logo.png")
        st.image(logo_path, width=200)
        # Google login button with icon
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?" +
            urlencode({
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "scope": "openid email profile",
                "access_type": "offline",
                "prompt": "select_account"
            })
        )
        google_icon = "https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png"
        st.markdown(f'''
            <a href="{auth_url}" style="text-decoration: none;">
                <div style="display: flex; align-items: center; justify-content: center; border: 1px solid #ccc; border-radius: 6px; padding: 10px 20px; width: 260px; margin: 20px auto; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                    <img src="{google_icon}" alt="Google" style="width: 24px; height: 24px; margin-right: 12px;"/>
                    <span style="font-size: 16px; color: #444;">Continue with Google</span>
                </div>
            </a>
        ''', unsafe_allow_html=True)
        st.stop()

    # Step 2: Exchange code for token
    code = st.query_params["code"][0]
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    resp = req.post(token_url, data=data)
    if resp.status_code != 200:
        st.write("CLIENT_ID:", CLIENT_ID)
        st.write("CLIENT_SECRET:", CLIENT_SECRET)
        st.write("REDIRECT URI:", REDIRECT_URI)
        st.error("Failed to authenticate with Google.")
        st.stop()
    tokens = resp.json()
    idinfo = id_token.verify_oauth2_token(tokens["id_token"], requests.Request(), CLIENT_ID)
    email = idinfo.get("email", "")
    if not email.endswith("@hurix.com"):
        st.error("Only hurix.com email addresses are allowed.")
        st.stop()
    user = {"email": email, "name": idinfo.get("name", "")}
    st.session_state["user"] = user
    return user 