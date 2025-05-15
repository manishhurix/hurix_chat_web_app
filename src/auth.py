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
# REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://hurixchatchat.streamlit.app/")

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
    if "code" not in st.query_params:
        # Use public URL for the logo
        logo_url = "https://www.hurix.com/wp-content/uploads/2025/01/newhurixlogo.png"
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
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh;">
                <div style="background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.07); padding: 40px 32px 24px 32px; min-width: 340px; max-width: 90vw; display: flex; flex-direction: column; align-items: center;">
                    <img src='{logo_url}' width='160' style='margin-bottom: 32px;'/>
                    <h2 style='margin-bottom: 20px; color: #222; font-weight: 600; letter-spacing: 0.5px;'>Sign in to Hurix Chat</h2>
                    <a href="{auth_url}" style="text-decoration: none;">
                        <div style="display: flex; align-items: center; justify-content: center; border: 1.5px solid #e0e0e0; border-radius: 8px; padding: 14px 28px; width: 280px; margin: 0; background: #fff; box-shadow: 0 2px 8px rgba(60,64,67,0.04); transition: box-shadow 0.2s; cursor: pointer; font-weight: 500; font-size: 17px; gap: 16px;">
                            <span style="color: #444; font-size: 17px; font-weight: 500; letter-spacing: 0.1px;">Continue with Google</span>
                        </div>
                    </a>
                    <style>
                    a[href^=\"https://accounts.google.com\"] div:hover {{
                        box-shadow: 0 4px 16px rgba(60,64,67,0.10);
                        border-color: #bdbdbd;
                    }}
                    </style>
                </div>
            </div>
        """, unsafe_allow_html=True)
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