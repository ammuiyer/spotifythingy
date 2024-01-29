import json
from dotenv import load_dotenv
import os
import base64
from requests import post

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id)

def get_token():
    #concatenate client id and client secret in base 64 to get auth token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_enconded = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded", 
        'Authorization': 'Basic ' + auth_enconded
        
    }

    data = {"grant_type": 'client_credentials'}

    #make a request
    result = post(url, headers=headers, data=data, json=True)
    json_result = json.loads(result.content)
    return json_result["access_token"]

def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token
    }


token = get_token()
print(token)
    
