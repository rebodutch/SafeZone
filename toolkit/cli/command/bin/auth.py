import os
import json
from typing import Optional

from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow

def auth_login(
    relay_url: Optional[str] = None,
    token_file: Optional[str] = None,
    client_secret_file: Optional[str] = None,
    verbose: bool = True,
):
    load_dotenv()
    relay_url = relay_url or os.getenv("RELAY_URL")
    token_file = token_file or os.getenv("TOKEN_FILE")
    client_secret_file = client_secret_file or os.getenv("CLIENT_SECRET_FILE")

    if not relay_url or not token_file or not client_secret_file:
        print("❌ Required environment variable missing: RELAY_URL, TOKEN_FILE, CLIENT_SECRET_FILE.")
        raise ValueError("Missing required environment variables.")

    if not os.path.exists(token_file):
        if not os.path.exists(client_secret_file):
            print("Please create a client secret file and set CLIENT_SECRET_FILE env.")
            raise FileNotFoundError(f"❌ Client secret file not found: {client_secret_file}")
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file,
                scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
            )
            creds = flow.run_local_server()
            req = requests.Request()
            idinfo = id_token.verify_oauth2_token(creds.id_token, req)
        except Exception as e:
            raise Exception(f"❌ Google OAuth2 error: {e}")
        try:
            with open(token_file, "w") as token_out:
                json.dump(
                    {
                        "id_token": creds.id_token,
                        "email": idinfo["email"],
                        "relay_url": relay_url,
                    },
                    token_out,
                )
            if verbose:
                print(f"✅ Successfully authenticated as {idinfo['email']}")
                print(f"🔗 Relay URL set to {relay_url}")
                print(f"💾 Token saved to {token_file}")
        except Exception as e:
            raise Exception(f"Failed to save token: {e}")
    else:
        if verbose:
            print(f"✅ Token already exists. Loading from {token_file}")
            print(f"🔗 Accessing Relay URL: {relay_url}")
