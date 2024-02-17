import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
from requests_oauthlib import OAuth2Session
import requests

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect = os.getenv("REDIRECT_URI")
# token_url = "https://accounts.spotify.com/api/token"
# spotify = OAuth2Session(client_id=client_id, scope=["playlist-modify-private", "playlist-modify-public"], redirect_uri=redirect)
# print('Please go here and authorize: ', spotify.authorization_url("https://accounts.spotify.com/authorize"))


# redirect_response = input('\n\nPaste the full redirect URL here: ')

# from requests.auth import HTTPBasicAuth

# auth = HTTPBasicAuth(client_id, client_secret)

# Fetch the access token


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

def create_playlist(user_id):
    url = 'https://api.spotify.com/v1/users/' + user_id +'/playlists'

    token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

    data = {
    "name": "New Test Playlist"}

    #make a post
    result = spotify.post(url, data=data, json=True)
    print(result.content)
    json_result = json.loads(result.content)
    return json_result
   

def request_token():

    #  1. Your application requests authorization
    auth_url = 'https://accounts.spotify.com/authorize'
    payload = {'client_id': client_id, 'response_type':'code','redirect_uri':redirect}
    auth = requests.get(auth_url,params = payload)
    print ('\nPlease go to this url to authorize ', auth.url)

    #  2. The user is asked to authorize access within the scopes
    #  3. The user is redirected back to your specified URI
    resp_url = input('\nThen please copy-paste the url you where redirected to: ')
    resp_code= resp_url.split("?code=")[1].split("&")[0]

    #  4. Your application requests refresh and access tokens
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {'redirect_uri': redirect,'code': resp_code, 'grant_type': 'authorization_code','scope':'playlist-modify-private playlist-modify-public playlist-read-private'}
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_enconded = str(base64.b64encode(auth_bytes), "utf-8")
    headers = {'Authorization': 'Basic %s' % auth_enconded}
    req = requests.post(token_url, data=payload, headers=headers, verify=True)
    response = req.json()

    return response
   
# token = get_token()
# print(search_for_track(token, "chase atlantic")["name"])
# print(create_playlist('ammuiyer'))

def create_playlist(username, list_name):
    token = request_token()
    access_token = token['access_token']
    auth_header = {'Authorization': 'Bearer {token}'.format(token=access_token), 'Content-Type': 'application/json'}
    api_url = 'https://api.spotify.com/v1/users/%s/playlists' % username
    data = {
    "name": "New Test Playlist"}
    r = requests.post(api_url, data=json.dumps(data), headers=auth_header)
    print(r.content)

print(create_playlist('ammuiyer', "new playlist"))





    
