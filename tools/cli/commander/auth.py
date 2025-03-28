# tools/cli/auth.py
import os
import json

from dotenv import load_dotenv

# oath2 is a library for Google OAuth 2.0
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow


load_dotenv()
# get the environment variables
TOKEN_FILE = os.getenv("TOKEN_FILE")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def auth_login(url: str = None):
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
    )
    creds = flow.run_local_server()

    # Create a "google auth" request object
    request = requests.Request()
    # Decode ID Token
    idinfo = id_token.verify_oauth2_token(creds.id_token, request)

    with open(TOKEN_FILE, "w") as f:
        json.dump({"id_token": creds.id_token, "email": idinfo["email"]}, f)

    print(f"✅ Successfully authenticated as {idinfo['email']}")

    if url:
        print(f"🔗 Relay URL set to {url}")
    else:
        print(f"🔗 Relay URL set to http://safezone.omh.idv.tw")

    print(f"💾 Token saved to {TOKEN_FILE}")


def load_token():
    if not os.path.exists(TOKEN_FILE):
        print(f"Login Required.")
        raise Exception("Login required.")

    with open(TOKEN_FILE, "r") as f:
        token = json.load(f)
        id_token = token.get("id_token")
    return id_token
