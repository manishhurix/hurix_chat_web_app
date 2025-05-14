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
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/")


def login():
    if "user" in st.session_state:
        return st.session_state["user"]

    # Step 1: Get authorization code
    if "code" not in st.experimental_get_query_params():
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
        st.markdown(f"[Login with Google]({auth_url})")
        st.stop()

    # Step 2: Exchange code for token
    code = st.experimental_get_query_params()["code"][0]
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