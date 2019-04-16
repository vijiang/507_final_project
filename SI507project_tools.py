import spotipy
import os
import json
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, session, redirect, url_for
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from advanced_expiry_caching_fp import Cache


# ------ Setting up SQLAlchemy stuff/SQL table ------

# from project planning doc:
# I expect my database schema to include 3 tables. The entities each table will represent are: Playlist tracks, albums, and Pitchfork album reviews. There will be a many-to-one relationship between playlist tracks and the album table there will be a one-to-one relationship between the albums table and the Pitchfork reviews table.

app = Flask(__name__)
app.use_reloader = True

app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./caribou_playlist.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # For database use
session = db.session  # to make queries easy

class Tracks(db.Model):
    __tablename__= "playlist tracks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    album_name = db.relationship("Albums", backref = db.backref("name", lazy="dynamic"))

# many-to-one relationship 

class Albums(db.Model):
    __tablename__= "albums"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(100), nullable=False)

# one-to-one relationship

class Reviews(db.Model):
    __tablename__= "pitchfork reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    r_album = db.relationship("Albums", backref = db.backref("pitchfork reviews", uselist=False))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float(2), nullable=False)
    description = db.Column(db.String(200))

# ------ Setting up Spotify requests ------

SPOTIFY_CLIENT_ID = "fc28786916ef479b977f7dabacfb68ab"
SPOTIFY_SECRET = "764343631291468c9829c0274616b5f4"
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "cariboutheband"
playlist_id = "4Dg0J0ICj9kKTGDyFu0Cv4"

results = {}

# ------ Creating a simple cache of my data so I don't get blocked ------
try:
    cache = open("caribou_tracks", 'r')
    results = json.load(cache)
except FileNotFoundError:
    with open("caribou_tracks.json", 'w') as outfile:
        results = sp.user_playlist(username, playlist_id)
        tracks_info = results['tracks']
        tracks = tracks_info['items']
        while tracks_info['next']:
            tracks_info = sp.next(tracks_info)
            tracks.extend(tracks_info['items'])
        results['tracks']['items'] = tracks
        json.dump(results, outfile, indent=4)
    

# class Track:
#     def __init__(self, track_title, artist_name, album_title):
#        self.track_title = track_title
#        self.artist_name = artist_name
#        self.album_title = album_title

#     def __repr__(self):
#         return "{} by {}, from the album {}.".format(self.track_title, self.artist_name, self.album_title)

# ------ Formatting data for the database/making it readable ------

def get_or_create_album(album_name):
    album = Albums.query.filter_by(a_name=album_name).first()
    if album:
        # print("return A") checking which statement is passing
        return album
    else:
        album = Albums(a_name=album_name)
        # print("return B") checking which statement is passing
        session.add(album)
        session.commit()
        # album = Albums.query.filter_by(a_name=album_name).first()
        return album

def create_track():
    for song in results["tracks"]["items"]:
        s_album = song["track"]["album"]["name"]
        album = get_or_create_album(s_album)
        s_artist = song["track"]["artists"][0]["name"]
        s_title = song["track"]["name"]
        track = Tracks(name=s_title, artist=s_artist, album_name=album) 
        session.add(track)
        session.commit()
    return None


# ------ Setting up P4K album review scraping ------

START_URL = "https://pitchfork.com/reviews/albums/"
FILENAME = "pitchfork_albums_reviews.json"

PROGRAM_CACHE = Cache(FILENAME)  # kinda a constant

# assuming constants exist as such
# use a tool to build functionality here


def access_page_data(url):
    data = PROGRAM_CACHE.get(url)  # get data associated with that identifier
    # unique identifier is the URL where the data lives
    # get will return none or false if the url does not exist
    if not data:
        # get the stuff that lives in that place is there is currently nothing there
        data = requests.get(url).text
        # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
        PROGRAM_CACHE.set(url, data)
        # url is identifier; data is what you want to associate with identifier
    return data

all_pages = access_page_data(START_URL)  # front end code

# For each state, you should scrape data representing all National Sites (which come in many "types" -- National Parks, National Monuments, National Forests, National Military Parks… etc).

# creating a Soup item
main_soup = BeautifulSoup(all_pages, features="html.parser")

list_items = main_soup.find_all("div", {"class":"review"})
# print(list_items)
href_list = []
for review in list_items:
    href_list.append(review.find('a').get('href'))

## CHECK IF ALBUM EXISTS IN DATABASE!!! sometimes there are dual reviews
## or - new project idea - use existing reviews database --> take that url and scrape site for brief review paragraph

print(href_list)

# Making the program run

if __name__ == "__main__":
    db.create_all()
    create_track()
    # app.run()
