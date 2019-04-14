import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask

# Setting up requests

SPOTIFY_CLIENT_ID = "fc28786916ef479b977f7dabacfb68ab"
SPOTIFY_SECRET = "764343631291468c9829c0274616b5f4"

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=
    SPOTIFY_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "cariboutheband"
playlist_id = "4Dg0J0ICj9kKTGDyFu0Cv4"

results = sp.user_playlist(username, playlist_id)

with open("caribou_tracks", 'w') as outfile:
    json.dump(results, outfile, indent=4)



