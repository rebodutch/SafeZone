# tools/cli/auth.py
import os
import json

from dotenv import load_dotenv

# oath2 is a library for Google OAuth 2.0
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow


def auth_login(url: str = None):
    load_dotenv()
    # get the environment variables
    RELAY_URL = os.getenv("RELAY_URL")
    CONFIG_FILE = os.getenv("CONFIG_FILE")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    if not os.path.exists(CONFIG_FILE):
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET,
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
        )
        creds = flow.run_local_server()

        # Create a "google auth" request object
        request = requests.Request()
        # Decode ID Token
        idinfo = id_token.verify_oauth2_token(creds.id_token, request)

        with open(CONFIG_FILE, "w") as f:
            json.dump({"id_token": creds.id_token, "email": idinfo["email"]}, f)

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if "relay_url" not in config:
        config["relay_url"] = RELAY_URL
    else:
        config["relay_url"] = url

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

    print(f"✅ Successfully authenticated as {config['email']}")

    print(f"🔗 Relay URL set to {config["relay_url"]}")

    print(f"💾 Token saved to {CONFIG_FILE}")
