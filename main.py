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
playlist_name = os.getenv("PLAYLIST_NAME")
username = os.getenv("USERNAME")
filepath = os.getenv("FILEPATH")


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
    return json_result[0]['uri']

    # use the get method for this endpoint



   

def request_token_auth_flow():


    auth_url = 'https://accounts.spotify.com/authorize'
    payload = {'client_id': client_id, 'response_type':'code','redirect_uri':redirect, 'scope': "playlist-modify-private  playlist-modify-public playlist-read-private"}
    auth = requests.get(auth_url,params = payload)
    print ('\nPlease go to this url to authorize ', auth.url)

    resp_url = input('\nThen please copy-paste the url you where redirected to: ')
    resp_code= resp_url.split("?code=")[1].split("&")[0]


    token_url = 'https://accounts.spotify.com/api/token'
    payload = {'redirect_uri': redirect,'code': resp_code, 'grant_type': 'authorization_code'}
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_enconded = str(base64.b64encode(auth_bytes), "utf-8")
    headers = {'Authorization': 'Basic %s' % auth_enconded}
    req = requests.post(token_url, data=payload, headers=headers, verify=True)
    response = req.json()

    return response
   

#returns spotify id of da playlist
def create_playlist(username, token):
    auth_header = get_auth_header(token)
    api_url = 'https://api.spotify.com/v1/users/' + username + '/playlists'
    data = {
    "name": playlist_name}
    r = requests.post(api_url, data=json.dumps(data), headers=auth_header)
    response = r.json()
    return response["id"]

def add_song_to_playlist(playlist_id, songs_list=None):
    auth_header = get_auth_header(token)
    api_url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'
    data = {
    "playlist_id": playlist_id
    }
    body = {
        "uris": songs_list
    }
    r = requests.post(api_url, data=json.dumps(data), headers=auth_header, params=body)


token1 = get_token()

token = request_token_auth_flow()['access_token']
playlist_id = create_playlist(username=username, token=token)

#importing csv
import pandas as pd
df = pd.read_csv(filepath).dropna()

for index, row in df.iterrows():
    song_unparsed = row[0]
    if(song_unparsed.startswith("https://")):
        #get song w link input
        add_song_to_playlist(playlist_id=playlist_id, songs_list = [song_unparsed[30:]])


    else:
        #get song with keyword input
        add_song_to_playlist(playlist_id=playlist_id, songs_list = [search_for_track(token1, song_unparsed)])










    

