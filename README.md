# spotifythingy

This is a project designed to help import a large csv file of song reccomendations, in keyword/link form, into a customizable Spotify Playlist. I built this because we have a question on my college's hackathon application form regarding song reccommendations. 

To run this program, do the following:

First, clone this repository locally.

You'll need to go to the spotify web api, and make an app. Fill out the .env file (you'll have to make one, since it's in the .gitignore) with the following environment variables. 
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REDIRECT_URI = your_redirect_uri
PLAYLIST_NAME = your_custom_playlist_name
USERNAME = your_spotify_username
FILEPATH = localfilepath_to_your_csv_file
```


Then, run the following: 

```
pip install requirements.txt
```

```
python main.py
```

