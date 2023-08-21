"""
One time use script to generate oauth token. Thereafter, Airflow refreshes the tokens
on a timely basis so the token never expires.

In case something breaks, run this again to generate a token.
"""

import os
import json

from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_SECRET")

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/spreadsheets/values"]
redirect_uri = "<YOUR_REDIRECT_URL>"
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Google for authorization
authorization_url, state = google.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

with open("token.json", "w") as f:
    json.dump(token, f)

print("Dumped token output to token.json")
