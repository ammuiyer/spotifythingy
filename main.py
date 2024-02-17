import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


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

def search_for_track(token, keyword):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token=token)
    query = f"?q={keyword}&type=track&limit=1"

    query_url = url + query 
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No tracks exist under this artist!")
        return None
    return json_result[0]

    # use the get method for this endpoint

def create_playlist(token, user_id):
    url = 'https://api.spotify.com/v1/users/' + user_id +'/playlists'

    headers = get_auth_header(token)

    data = {
    "name": "New Test Playlist"}

    #make a request
    result = post(url, headers=headers, data=data, json=True)
    json_result = json.loads(result.content)
    return json_result
   
   


token = get_token()
print(search_for_track(token, "chase atlantic")["name"])
print(create_playlist(token, 'ammuiyer'))


    
