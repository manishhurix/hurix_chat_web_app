import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req
from urllib.parse import urlencode
from streamlit_cookies_manager import EncryptedCookieManager
import json

def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
    cookies["user"] = ""
    cookies.save()
    st.query_params.clear()
    st.rerun()
    return

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/")
# REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/")

cookies = EncryptedCookieManager(
    prefix="hurix_chat",
    password=os.environ.get("COOKIE_SECRET", "some-random-secret"),
)
if not cookies.ready():
    st.stop()

# st.write("CLIENT_ID:", CLIENT_ID)
# st.write("REDIRECT_URI:", REDIRECT_URI)
# st.write("CLIENT_SECRET:", CLIENT_SECRET)

def login_success(user):
    cookies["user"] = json.dumps(user)
    cookies.save()
    st.session_state["user"] = user

def get_logged_in_user():
    if "user" in st.session_state:
        return st.session_state["user"]
    if "user" in cookies and cookies["user"]:
        user = json.loads(cookies["user"])
        st.session_state["user"] = user
        return user
    return None

def login():
    user = get_logged_in_user()
    if user:
        return user
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
    code_param = st.query_params.get("code")
    if isinstance(code_param, list):
        code = code_param[0]
    else:
        code = code_param
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
        st.stop()
    tokens = resp.json()
    idinfo = id_token.verify_oauth2_token(tokens["id_token"], requests.Request(), CLIENT_ID)
    email = idinfo.get("email", "")
    if not email.endswith("@hurix.com"):
        st.error("Only hurix.com email addresses are allowed.")
        st.stop()
    user = {"email": email, "name": idinfo.get("name", "")}
    login_success(user)
    return user 