import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, session, redirect, url_for
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy


# ------ Setting up SQLAlchemy stuff/SQL table ------

# from project planning doc:
# I expect my database schema to include 3 tables. The entities each table will represent are: Playlist tracks, albums, and Pitchfork album reviews. There will be a many-to-one relationship between playlist tracks and the album table there will be a one-to-one relationship between the albums table and the Pitchfork reviews table.

app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./caribou_playlist.db'
## TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # For database use
session = db.session  # to make queries easy

# ------ Setting up Spotify requests ------

SPOTIFY_CLIENT_ID = "fc28786916ef479b977f7dabacfb68ab"
SPOTIFY_SECRET = "764343631291468c9829c0274616b5f4"

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=
    SPOTIFY_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "cariboutheband"
playlist_id = "4Dg0J0ICj9kKTGDyFu0Cv4"

results = sp.user_playlist(username, playlist_id)

# print statement for reference
with open("caribou_tracks", 'w') as outfile:
    json.dump(results, outfile, indent=4)

class Track:
    def __init__(self, track_title, artist_name, album_title):
       self.track_title = track_title
       self.artist_name = artist_name
       self.album_title = album_title

    def __repr__(self):
        return "{} by {}, from the album {}.".format(self.track_title, self.artist_name, self.album_title)

def create_track():
    return None



